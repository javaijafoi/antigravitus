# -*- coding: utf-8 -*-
"""auditar_sessao.py - confere um transcript de sessão contra as diretivas, mecanicamente.

Por que existe: ler as regras uma vez não garante segui-las. Este script lê o
`automato/runtime/transcript_*.jsonl` (uma linha JSON por comando, com `cmd`, `text`, `vitals`,
`in_combat`) e aponta o que quebrou regra escrita. Não substitui julgamento: um AVISO pede
explicação; uma FALHA pede correção ou justificativa registrada no plano.

Cada achado cita a regra de origem. Desde o driver v1.7.9 cada comando traz o campo `origem`
(`play` = play.py, à mão; `navegar`, `xadrez_cascata`, `turno:<rotina>`... = script). Com ele o
auditor cobra a forma de jogar do automato (README, diretiva §23): andar muito ou caçar muito
pelo play.py é FALHA. Transcripts mais antigos não têm origem e ficam fora dessas duas regras.
Para mapear área nova à mão (diretiva §9.1), `MUD_ORIGEM=mapear` antes do play.py.

Uso:
    python scripts/auditar_sessao.py                      # o transcript mais recente
    python scripts/auditar_sessao.py <arquivo.jsonl> ...  # um ou mais
Saída: 0 limpo | 1 há FALHA | 2 só AVISO.
"""
import json
import re
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
RUNTIME = RAIZ / 'automato' / 'runtime'

FALHA, AVISO = 'FALHA', 'AVISO'
DIRECOES = {'n', 's', 'e', 'w', 'u', 'd', 'north', 'south', 'east', 'west', 'up', 'down'}
VERBAIS = ('say', 'ask', 'whisper', 'tell', 'reply', "'")
ASSINATURAS_FALHA = ('não pode ir', 'Em que você deseja', 'muito relaxado', 'carregando muito peso',
                     'Como?!?', 'Você não tem', 'Você não vê', 'A porta está fechada',
                     'não tem experiência')
ENTREGA = 'Você deve entregar objeto'
# magias que começam uma luta: pedem consider antes (diretiva §2; morte #10 foi charm sem consider)
OFENSIVAS = ('burning hands', 'magic missile', 'chill touch', 'shocking grasp', 'lightning bolt',
             'color spray', 'fireball', 'sleep', 'curse', 'blindness', 'poison', 'charm person')
ORIGENS_A_MAO = {'play'}
# revisão de 16 a 20/10: ~80 mil comandos à mão e nenhuma rotina supervisionada
LIMITE_MOV_A_MAO = 80
LIMITE_ATAQUE_A_MAO = 30


def _rx(frase):
    """Regex tolerante a acento perdido: cada caractere não-ASCII vira um curinga de 1 caractere."""
    return re.compile(''.join('.' if ord(c) > 127 else re.escape(c) for c in frase), re.I)


_FALHAS = [_rx(s) for s in ASSINATURAS_FALHA]
_ENTREGA = _rx(ENTREGA)
_MORTE = _rx('Você está morto')
_ALINH = re.compile(r'Alinhamento:\s*\{[^}]*\}\s*(-?\d+)')
_PRECO = re.compile(r'(\d[\d\.]*)\s*moedas', re.I)


def ler(caminho):
    regs = []
    for linha in Path(caminho).read_text(encoding='utf-8', errors='replace').splitlines():
        try:
            regs.append(json.loads(linha))
        except ValueError:
            continue
    return regs


def _falhou(texto):
    return any(r.search(texto or '') for r in _FALHAS)


def _primeira_palavra(cmd):
    return (cmd or '').strip().split(' ')[0].lower()


def _alvo(texto):
    """'2.torre negra' -> 'torre': o consider de 'torre' vale para '1.torre' e '2.torre'."""
    primeiro = (texto or '').strip().lower().split(' ')[0]
    return re.sub(r'^\d+\.', '', primeiro)


def alvo_de_ataque(cmd):
    """Alvo de um comando que começa luta (kill/hit ou magia ofensiva), ou None."""
    c = (cmd or '').strip().lower()
    p = _primeira_palavra(c)
    if p in {'kill', 'hit', 'attack', 'k'}:
        return _alvo(c.split(' ', 1)[1]) if ' ' in c else None
    m = re.match(r"cast\s+'([^']+)'\s+(\S+)", c)
    if p == 'cast' and m and m.group(1) in OFENSIVAS:
        return _alvo(m.group(2))
    return None


def auditar(regs):
    """Recebe a lista de registros e devolve achados: dicts {nivel, regra, onde, detalhe}."""
    achados = []

    def achar(nivel, regra, i, detalhe):
        achados.append({'nivel': nivel, 'regra': regra, 'onde': i, 'detalhe': detalhe})

    comandos = [(i, r) for i, r in enumerate(regs) if r.get('kind') == 'command']
    wimpy = next((r.get('wimpy') for r in regs if r.get('kind') == 'open' and r.get('wimpy')), 45)
    hp_max, ultimo_score_entrega, alinh_ant = 0, False, None
    consideradas, identificadas, cobradas = set(), set(), set()
    seq_falha, seq_cmd = 0, None
    verbais_recentes = []
    por_origem = {}
    mov_mao = ataque_mao = 0

    for n, (i, r) in enumerate(comandos):
        cmd = (r.get('cmd') or '').strip()
        texto = r.get('text') or ''
        p = _primeira_palavra(cmd)
        alvo = ' '.join(cmd.lower().split(' ')[1:])
        origem = r.get('origem')
        if origem:
            por_origem[origem] = por_origem.get(origem, 0) + 1
        a_mao = origem in ORIGENS_A_MAO
        atacado = alvo_de_ataque(cmd)

        # 0. a forma de jogar (diretiva §23, README do automato): rota e caça vão por script/rotina
        if a_mao and p in DIRECOES:
            mov_mao += 1
            if mov_mao == LIMITE_MOV_A_MAO + 1:
                achar(FALHA, 'andar-a-mao (diretiva §23)', i,
                      'mais de %d passos pelo play.py: rota conhecida vai por navegar.py; área nova '
                      'à mão com MUD_ORIGEM=mapear e a rota gravada no mapa.json' % LIMITE_MOV_A_MAO)
        if a_mao and atacado:
            ataque_mao += 1
            if ataque_mao == LIMITE_ATAQUE_A_MAO + 1:
                achar(FALHA, 'caca-a-mao (diretiva §23)', i,
                      'mais de %d ataques pelo play.py: caça e XP vão por turno.py --rotina <x>, '
                      'supervisionado; se não há rotina para a zona, escrever a rotina' % LIMITE_ATAQUE_A_MAO)
        vitals = r.get('vitals') or {}
        hp = vitals.get('hp') if isinstance(vitals.get('hp'), int) else None
        if hp:
            hp_max = max(hp_max, hp)

        # 1. mesma recusa repetida (diretiva §12, guarda de repetição)
        if _falhou(texto) and p not in {'look', 'score', 'inventory', 'exits'}:
            seq_falha = seq_falha + 1 if cmd == seq_cmd else 1
            seq_cmd = cmd
            if seq_falha == 3:
                achar(FALHA, 'repeticao-de-recusa (diretiva §12)', i,
                      '%r recusado 3 vezes seguidas; a guarda de repetição pararia aqui' % cmd)
        else:
            seq_falha, seq_cmd = 0, None

        # 2. quit (AGENTS #8)
        if p == 'quit':
            achar(FALHA, 'quit (AGENTS #8)', i, 'quit apaga o progresso de missões; usar save e fechar o socket')

        # 3. give sem etapa de entrega no último score tudo (AGENTS #13, diretiva §19/§21)
        if p == 'give':
            if not ultimo_score_entrega:
                achar(FALHA, 'give-sem-etapa (AGENTS #13)', i,
                      '%r sem "%s" no último score tudo' % (cmd, ENTREGA))
            ultimo_score_entrega = False
        if cmd.lower().startswith('score tudo'):
            ultimo_score_entrega = bool(_ENTREGA.search(texto))

        # 4. fala de missão em lote (AGENTS #14, diretiva §20)
        if ';' in cmd and any(cmd.lower().lstrip().startswith(v) or (';' + v) in cmd.lower() for v in VERBAIS[:4]):
            achar(FALHA, 'fala-em-lote (AGENTS #14)', i, 'vários comandos verbais na mesma linha: %r' % cmd)
        if p in VERBAIS[:4]:
            verbais_recentes.append((r.get('at'), i, cmd))
            if len(verbais_recentes) >= 2:
                a, b = verbais_recentes[-2], verbais_recentes[-1]
                if a[0] and b[0] and _seg(b[0]) - _seg(a[0]) < 2.0:
                    achar(AVISO, 'fala-em-rajada (AGENTS #14)', i,
                          '%r e %r com menos de 2 s de intervalo: pode ter sido automático' % (a[2], b[2]))

        # 5. atacar sem consider (diretiva §2, §22): FALHA uma vez por alvo nunca considerado na sessão
        if p == 'consider':
            consideradas.add(_alvo(alvo))
        if atacado and atacado not in consideradas and atacado not in cobradas:
            cobradas.add(atacado)
            achar(FALHA, 'ataque-sem-consider (diretiva §2/§22)', i,
                  '%r sem consider prévio de %s nesta sessão' % (cmd, atacado))

        # 6. get sem identify (diretiva §15)
        if p == 'identify' or (p == 'cast' and 'identify' in cmd.lower()):
            identificadas.add(alvo.replace("'identify'", '').strip().split(' ')[0] or 'x')
        if p == 'get' and alvo:
            primeiro = alvo.split(' ')[0]
            if primeiro == 'all' or primeiro.startswith('all.'):
                achar(AVISO, 'get-all (diretiva §15)', i, '%r recolhe sem triagem; amaldiçoados são proibidos' % cmd)
            elif primeiro not in identificadas and 'mochila' not in alvo and 'pao' not in primeiro:
                achar(AVISO, 'get-sem-identify (diretiva §15)', i, '%r sem identify prévio' % cmd)

        # 7. compra cara (AGENTS #13)
        if p == 'buy':
            for m in _PRECO.finditer(texto):
                valor = int(m.group(1).replace('.', ''))
                if valor >= 1000:
                    achar(AVISO, 'compra-cara (AGENTS #13)', i, '%r gastou %d moedas; a etapa estava confirmada?' % (cmd, valor))
                    break

        # 8. alinhamento caiu (AGENTS #15, diretiva §22)
        m = _ALINH.search(texto)
        if m:
            v = int(m.group(1))
            if alinh_ant is not None and v < alinh_ant:
                achar(FALHA, 'alinhamento-caiu (diretiva §22)', i, 'de %d para %d: parar e auditar a causa' % (alinh_ant, v))
            alinh_ant = v

        # 9. vida baixa e depois andando em vez de recall/flee (diretiva §2, §6)
        if hp is not None and hp_max and (hp / hp_max < 0.45 or hp <= wimpy):
            proximos = [(_primeira_palavra(c.get('cmd')) if c else '') for _, c in comandos[n + 1:n + 4]]
            if proximos and proximos[0] in DIRECOES:
                achar(AVISO, 'recuo-a-pe (diretiva §2)', i,
                      'vida %d/%d e o próximo comando foi andar; recall ou flee primeiro' % (hp, hp_max))

        # 10. morte registrada
        if _MORTE.search(texto):
            achar(AVISO, 'morte', i, 'a personagem morreu; autoquest ativa foi cancelada (conhecimento §59)')

    # 11. encerramento
    tipos = {r.get('kind') for r in regs}
    fecho = next((r for r in regs if r.get('kind') == 'close'), None)
    if comandos and 'close' not in tipos and 'shutdown' not in tipos:
        achar(AVISO, 'sessao-sem-fecho (AGENTS #11)', len(regs) - 1, 'sem registro de close/shutdown; save e sleep foram confirmados?')
    elif fecho is not None and not fecho.get('save_confirmed', fecho.get('save', True)):
        achar(FALHA, 'save-nao-confirmado (AGENTS #11)', regs.index(fecho), 'close sem save_confirmed')

    # 12. de onde vieram os comandos
    if comandos and not por_origem:
        achados.append({'nivel': 'INFO', 'regra': 'origem-ausente', 'onde': None,
                        'detalhe': 'transcript sem campo origem (driver anterior a v1.7.9): '
                                   'andar-a-mao e caca-a-mao não auditáveis aqui'})
    elif por_origem:
        achados.append({'nivel': 'INFO', 'regra': 'origem', 'onde': None,
                        'detalhe': 'comandos por origem: ' + ', '.join(
                            '%s=%d' % kv for kv in sorted(por_origem.items(), key=lambda kv: -kv[1]))})
    return achados


def _seg(iso):
    from datetime import datetime
    try:
        return datetime.fromisoformat(iso).timestamp()
    except Exception:
        return 0.0


def relatorio(caminho, achados):
    linhas = ['== %s ==' % Path(caminho).name]
    por_nivel = {FALHA: [], AVISO: [], 'INFO': []}
    for a in achados:
        por_nivel[a['nivel']].append(a)
    for nivel in (FALHA, AVISO, 'INFO'):
        for a in por_nivel[nivel]:
            linhas.append('[%s] %s (registro %s): %s' % (nivel, a['regra'], a['onde'], a['detalhe']))
    linhas.append('Resumo: %d falha(s), %d aviso(s)' % (len(por_nivel[FALHA]), len(por_nivel[AVISO])))
    return '\n'.join(linhas), len(por_nivel[FALHA]), len(por_nivel[AVISO])


def main(argv=None):
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    args = list(argv if argv is not None else sys.argv[1:])
    if not args:
        todos = sorted(RUNTIME.glob('transcript_*.jsonl'), key=lambda p: p.stat().st_mtime)
        todos = [p for p in todos if p.stat().st_size > 0]
        if not todos:
            print('nenhum transcript em %s' % RUNTIME, file=sys.stderr)
            return 2
        args = [str(todos[-1])]
    falhas = avisos = 0
    for a in args:
        texto, f, w = relatorio(a, auditar(ler(a)))
        print(texto)
        falhas, avisos = falhas + f, avisos + w
    return 1 if falhas else (2 if avisos else 0)


if __name__ == '__main__':
    sys.exit(main())
