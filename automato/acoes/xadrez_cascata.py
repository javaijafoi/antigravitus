# -*- coding: utf-8 -*-
"""xadrez_cascata.py - a cascata da autoquest Xeque-mate no Grande Tabuleiro, com rastreio de posicao.

Por que existe (Dia 157): os lacos em PowerShell do scratchpad perderam a posicao por respostas de `look`
atrasadas e mataram a personagem duas vezes (morte #10: Rainha + cavaleiro; morte #12: parada em E1, a
casa do REI BRANCO, que mata quem esta na Xeque-mate: "Herege! Voce deu xeque-mate no rei errado!").

Regras desta rotina:
  * cada passo e' verificado com o texto DA PROPRIA resposta do movimento (nunca com um look separado):
    cor da casa, frase da peca da casa ("casa do Bispo do Rei Branco") e numero de saidas;
  * a rota nunca passa por E8, E1, B1, G1 (casas proibidas) a menos que seja o destino explicito;
  * recall a qualquer divergencia; nunca anda "de volta" com a posicao incerta;
  * fala de NPC nao e' automatizada (AGENTS #14): o Bispo Branco e' aceito a mao; aqui so' se le o log.

Uso (o driver tem de estar no ar, a Xeque-mate ja' aceita com o Bispo Branco):
    python automato/acoes/xadrez_cascata.py --etapa peoes|bispos|cavalos|torres|rainha
    python automato/acoes/xadrez_cascata.py --etapa rei --rei     # kite no Rei Negro (exige --rei)
    python automato/acoes/xadrez_cascata.py --etapa f1            # leva a F1 e espera a ordem do Bispo
"""
import argparse
import re
import sys
import time
import unicodedata
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(RAIZ / 'automato' / 'nucleo'))
sys.path.insert(0, str(RAIZ / 'automato' / 'camadas'))

COLUNAS = 'ABCDEFGH'
DIRS = {'n': (0, 1), 's': (0, -1), 'e': (1, 0), 'w': (-1, 0)}
PROIBIDAS = {'E8', 'A1', 'B1', 'C1', 'D1', 'E1', 'G1'}   # Rei Negro, Rei Branco (E1 mata quem entra visivel) e a fileira 1 inteira (menos F1 e H1)
ROTA_F1 = ['s', 's', 's', 'w', 'w', 's']                  # de H5: H4, H3, H2, G2, F2, F1 (nunca pela fileira 1)
RECUSAS = ('nao pode ir', 'muito relaxado', 'muito ocupado', 'voce esta dormindo', 'nao pode fazer isso dormindo')

# frase que a casa mostra depois de "casa " (normalizada, sem acento); None = casa sem peca (fileiras 3 a 6)
HOME = {
    'A1': 'da torre da rainha branca', 'B1': 'do cavalo da rainha branca', 'C1': 'do bispo da rainha branca',
    'D1': 'da rainha branca', 'E1': 'do rei branco', 'F1': 'do bispo do rei branco',
    'G1': 'do cavalo do rei branco', 'H1': 'da torre do rei branco',
    'A8': 'da torre da rainha negra', 'B8': 'do cavalo da rainha negra', 'C8': 'do bispo da rainha negra',
    'D8': 'da rainha negra', 'E8': 'do rei negro', 'F8': 'do bispo do rei negro',
    'G8': 'do cavalo do rei negro', 'H8': 'da torre do rei negro',
}


class Perdida(Exception):
    """A posicao ficou incerta; o chamador faz recall."""


def normalizar(texto):
    t = unicodedata.normalize('NFKD', texto or '')
    return ''.join(c for c in t if not unicodedata.combining(c)).lower()


def nome_casa(col, fil):
    return '%s%d' % (COLUNAS[col], fil)


def parse_casa(nome):
    return COLUNAS.index(nome[0].upper()), int(nome[1])


def cor_casa(col, fil):
    """Soma (coluna + fileira), A=1: par = Preta, impar = Branca (H1 = 9 e' Branca)."""
    return 'Branca' if ((col + 1) + fil) % 2 == 1 else 'Preta'


def saidas_esperadas(col, fil):
    n = 0
    n += 1 if fil < 8 else 0
    n += 1 if fil > 1 else 0
    n += 1 if col < 7 else 0
    n += 1 if col > 0 else 0
    if nome_casa(col, fil) in ('H5', 'D8', 'D1'):
        n += 1  # H5: o portao a leste; D8 e D1 (rainhas): a escada oculta `!baixo` para a tesouraria
    return n


def frase_da_casa(texto):
    """'do Bispo do Rei Branco' (normalizada) a partir de '... normalmente e a casa do Bispo do Rei Branco.'"""
    t = ' '.join(normalizar(texto).split())
    m = re.search(r'normalmente e a casa (.+?)\.', t)
    return m.group(1).strip() if m else None


def titulo_sala(texto):
    for linha in (texto or '').splitlines():
        limpa = re.sub(r'^\s*\d+hp\s+\d+mn\s+\d+mv\s*>\s*', '', linha).strip()
        if limpa and not limpa.startswith('DICA') and not limpa.startswith('>>>') and not limpa.startswith('['):
            return limpa
    return ''


def contar_saidas(texto):
    m = re.search(r'Sa.{1,2}das:\s*([^\]]*)\]', texto or '')
    if not m:
        return None
    return len([p for p in re.split(r',| e ', m.group(1)) if p.strip()])


def titulo_casa(texto):
    """'Uma Casa Branca' ou 'Uma Casa Preta' onde quer que apareca (avisos de sede/fome podem vir antes)."""
    m = re.search(r'Uma Casa (Branca|Preta)', texto or '')
    return m.group(0) if m else titulo_sala(texto)


def verificar_casa(texto, col, fil):
    """Levanta Perdida se o texto de chegada nao e' o da casa (col, fil). Pura: testavel sem jogo."""
    t = titulo_casa(texto)
    if normalizar(t) != normalizar('Uma Casa %s' % cor_casa(col, fil)):
        raise Perdida('titulo "%s" nao e a cor de %s' % (t, nome_casa(col, fil)))
    nome = nome_casa(col, fil)
    frase = frase_da_casa(texto)
    if nome in HOME and frase != HOME[nome]:
        raise Perdida('%s deveria mostrar "%s", mostrou "%s"' % (nome, HOME[nome], frase))
    if nome not in HOME and fil in (2, 7):
        if not frase or 'peao' not in frase and 'peoes' not in frase:
            raise Perdida('%s deveria ser casa de peao, mostrou "%s"' % (nome, frase))
        lado = 'rainha' if col < 4 else 'rei'
        if lado not in frase:
            raise Perdida('%s: peao do lado errado ("%s")' % (nome, frase))
    if nome not in HOME and fil in (3, 4, 5, 6) and frase:
        raise Perdida('%s nao deveria ter peca, mostrou "%s"' % (nome, frase))
    n = contar_saidas(texto)
    if n is not None and n != saidas_esperadas(col, fil):
        raise Perdida('%s: %d saidas, esperava %d' % (nome, n, saidas_esperadas(col, fil)))


def caminho_grade(origem, destino, proibidas=PROIBIDAS):
    """Menor caminho (BFS) entre duas casas, sem pisar nas proibidas (exceto o destino). Lista de direcoes."""
    o, d = parse_casa(origem), parse_casa(destino)
    fila, visto = [(o, [])], {o}
    while fila:
        (c, f), rota = fila.pop(0)
        if (c, f) == d:
            return rota
        for letra, (dc, df) in DIRS.items():
            nc, nf = c + dc, f + df
            if not (0 <= nc < 8 and 1 <= nf <= 8) or (nc, nf) in visto:
                continue
            if nome_casa(nc, nf) in proibidas and (nc, nf) != d:
                continue
            visto.add((nc, nf))
            fila.append(((nc, nf), rota + [letra]))
    return None


class Tabuleiro:
    """Dead-reckoning com verificacao a cada passo."""

    def __init__(self, casa, run):
        self.col, self.fil = parse_casa(casa)
        self.run = run

    @property
    def casa(self):
        return nome_casa(self.col, self.fil)

    def passo(self, d):
        dc, df = DIRS[d]
        nc, nf = self.col + dc, self.fil + df
        if not (0 <= nc < 8 and 1 <= nf <= 8):
            raise Perdida('passo %s sai do tabuleiro a partir de %s' % (d, self.casa))
        texto, vitals, combate = self.run(d)
        baixo = normalizar(texto)
        # "muito ocupado, lutando": o peao pode ter fugido em panico e o combate ainda nao fechou; espera e repete
        for _ in range(3):
            if 'muito ocupado' not in baixo:
                break
            time.sleep(2.5)
            texto, vitals, combate = self.run(d)
            baixo = normalizar(texto)
        if any(r in baixo for r in RECUSAS):
            raise Perdida('passo %s recusado: %r' % (d, titulo_sala(texto)[:60]))
        if 'Uma Casa' not in texto:
            # resposta perdida ou atrasada: um look decide se andou (nova casa) ou nao (casa antiga)
            time.sleep(1.5)
            texto2, vitals2, combate2 = self.run('look')
            try:
                verificar_casa(texto2, nc, nf)
                texto, vitals, combate = texto2, vitals2, combate2
            except Perdida:
                try:
                    verificar_casa(texto2, self.col, self.fil)
                except Perdida:
                    raise Perdida('resposta vazia no passo %s e o look nao bate nem com %s nem com %s'
                                  % (d, nome_casa(nc, nf), self.casa))
                texto, vitals, combate = self.run(d)      # nao andou: repete uma vez
        verificar_casa(texto, nc, nf)
        self.col, self.fil = nc, nf
        hp = (vitals or {}).get('hp')
        if isinstance(hp, int) and 0 < hp < 100:
            raise Perdida('vida %d < 100: so recall, nada de andar' % hp)
        return texto, vitals, combate

    def ir(self, destino, proibidas=PROIBIDAS):
        rota = caminho_grade(self.casa, destino, proibidas)
        if rota is None:
            raise Perdida('sem caminho de %s a %s' % (self.casa, destino))
        ultimo = ('', {}, False)
        for d in rota:
            ultimo = self.passo(d)
            time.sleep(0.15)
        return ultimo


# ---------------------------------------------------------------- jogo (precisa do driver)

def _jogo():
    import config  # noqa: F401
    from base import run
    import navegar as nav
    return run, nav


def log_atual():
    import config
    logs = sorted(Path(config.DIR_LOGS).glob('session_live_*.log'), key=lambda p: p.stat().st_mtime)
    return logs[-1] if logs else None


def contar_no_log(padrao):
    p = log_atual()
    if not p:
        return 0
    return len(re.findall(padrao, p.read_text(encoding='utf-8', errors='replace')))


def desde_aceite(padrao):
    """Mortes (regex) contadas so' DEPOIS da ultima aceitacao da missao no log da sessao."""
    p = log_atual()
    if not p:
        return 0
    txt = p.read_text(encoding='utf-8', errors='replace')
    i = txt.rfind('participar da aventura')
    return len(re.findall(padrao, txt[i:] if i >= 0 else txt))


def desde_marca(marca, padrao):
    """Ocorrencias de `padrao` depois da ULTIMA `marca` no log da sessao (toda a sessao se nao houver marca)."""
    p = log_atual()
    if not p:
        return 0
    txt = p.read_text(encoding='utf-8', errors='replace')
    i = txt.rfind(marca)
    return len(re.findall(padrao, txt[i:] if i >= 0 else txt))


def mortes(tipo):
    return contar_no_log(r'%s Negr[oa] est.{1,2} mort[oa]!' % tipo)


# O kite no Rei serve aos dois lados. O BRANCO e' excecao de moralidade do autor (2026-10-22, DECISOES §17): exige --excecao-rei-branco.
LADOS = {
    'negro': {'nome': 'Negro', 'acesso': ('E7', 'n'), 'casa': 'E8', 'morte': r'Rei Negr[oa] est.{1,2} mort[oa]!'},
    'branco': {'nome': 'Branco', 'acesso': ('E2', 's'), 'casa': 'E1', 'morte': r'Rei Branc[oa] est.{1,2} mort[oa]!'},
}


def mortes_do_lado(lado):
    return contar_no_log(lado['morte'])


def vida(vitals):
    return (vitals or {}).get('hp') or 0


def mana(vitals):
    return (vitals or {}).get('mana') or (vitals or {}).get('mn') or 0


# ---------------------------------------------------------------- etapas

# casa, palavra-chave do alvo, tipo no log, magias antes dos raios, quantas pecas podem empilhar
ETAPAS = {
    'bispos':  [('F8', 'bispo', 'Bispo', ['blindness', 'curse'], False), ('C8', 'bispo', 'Bispo', ['blindness', 'curse'], False)],
    'cavalos': [('G8', 'cavaleiro', 'Cavaleiro', ['blindness', 'curse'], False), ('B8', 'cavaleiro', 'Cavaleiro', ['blindness', 'curse'], False)],
    'torres':  [('A8', 'torre', 'Torre', [], True), ('H8', 'torre', 'Torre', [], True)],
    'rainha':  [('D8', 'rainha', 'Rainha', ['curse', 'blindness'], True)],
}
PRESENCA = {
    'bispo': r'(?m)^(o|a) bispo negro est.{1,2} aqui',
    'cavaleiro': r'(?m)^(aqui est.{1,2} um magn.fico cavaleiro negro|(o|a) cavaleiro negro est.{1,2} aqui)',
    'torre': r'castelo negro',
    'rainha': r'(?m)^a rainha negra est.{1,2} (aqui|dormindo)',
}
# frase com que o Bispo Branco abre cada etapa: as mortes valem so' depois da ultima vez que ele a disse
ORDEM = {'bispos': 'Elimine os dois bispos', 'cavalos': 'elimine os cavaleiros negros',
         'torres': 'Elimine as duas torres', 'rainha': 'elimine a Rainha Negra'}
LIMITE_VIDA = 190   # plano 043: a Rainha dá ate' ~100 por rodada; recall a 190 deixa margem de uma rodada
VIDA_PISO_LANCE = 100   # conhecimento par.73: a ida tem de parar ANTES do proximo lance, nao depois
HP_MIN_ENTRAR = 215
MANA_MIN_ENTRAR = 250   # uma ida gasta 100 a 170; descansar ate' 440 so' desperdicava minutos


def alvo_de_vida(hp_max, fracao=0.95, piso=150):
    """Vida-alvo para descansar: 95% da barra, nunca abaixo do `piso`.

    Antes era 215/222 fixos; com a vida maxima em 211 (penalidade de morte) o alvo
    era inalcancavel e cada ida parava os 420 s inteiros do `descansar` (conhecimento
    §89). Pura: nao fala com o MUD. ID: descanso_por_fracao_da_barra.
    """
    if not hp_max:
        return HP_MIN_ENTRAR
    return min(int(hp_max), max(int(piso), int(hp_max * fracao)))


def pode_lancar(vitals, piso=VIDA_PISO_LANCE):
    """False se a vida conhecida esta abaixo do piso: nada de outro lance, so' recall. Pura."""
    h = (vitals or {}).get('hp')
    return not (isinstance(h, int) and 0 < h < piso)


class Ctx:
    def __init__(self):
        self.run, self.nav = _jogo()
        self.salas = self.nav.carregar_mapa()

    def considerar(self, alvo, log=print):
        """consider uma vez por peca e por processo (diretiva par.2); devolve o perigo duro ou None."""
        import base
        perigo = base.considerar(alvo)
        log('  consider %s: %s' % (alvo, perigo or 'sem perigo duro'))
        return perigo

    def cmd(self, c, espera=1.0):
        r = self.run(c)
        time.sleep(espera)
        return r

    def sala(self):
        return self.run('look')[0]

    def no_templo(self):
        return 'templo de midgaard' in normalizar(titulo_sala(self.sala()))

    def garantir_templo(self, tentativas=3):
        """Confere o Templo; se nao estiver, faz recall e confere de novo (o look pode chegar atrasado)."""
        for i in range(tentativas):
            texto = self.sala()
            if not texto.strip():
                raise Perdida('driver desconectado (resposta vazia): reinicie o live_daemon so pelo PID e confira a missao')
            if 'templo de midgaard' in normalizar(titulo_sala(texto)):
                return True
            self.cmd('recall', 4)
            time.sleep(2)
        return self.no_templo()

    def comer_beber(self):
        """Come, bebe e REPOE pao e agua pelas tarefas padrao do `aproveitar_tempo` (prepara.comer_beber, repor_pao, encher_cantil,
        estas duas so' se a pre-condicao de falta valer). Ordem do autor, Dia 163: pao e agua vao pelo preparar/cuidar, nao por
        gambiarra do modulo. Nao usa o `cuidar.manter_magias` aqui: ele manda `visible` e tiraria a invisibilidade do kite."""
        try:
            import aproveitar_tempo
            aproveitar_tempo.aproveitar(2, tarefas=aproveitar_tempo.por_nome(['comer_beber', 'repor_pao', 'encher_cantil']), ctx=self)
        except Exception as e:      # noqa: BLE001 - nunca derruba a etapa; o auditor acusa fome/sede
            print('[XADREZ] ATENCAO: comer_beber falhou (%s); seguindo' % e, flush=True)
        self.garantir_templo()      # repor_pao e encher_cantil passam pela cidade

    def _vida_maxima(self):
        """Vida máxima lida do `score tudo` (o alvo de descanso tem de caber na barra)."""
        texto, _vit, _c = self.run('score tudo')
        m = re.search(r'Vida:\s*(?:\{[^}]*\})?\s*\d+\s+de\s+(\d+)', texto or '')
        return int(m.group(1)) if m else None

    def descansar(self, hp_min=None, mn_min=MANA_MIN_ENTRAR, max_s=180):
        """Descansa até os VITAIS dizerem que está pronta; `max_s` é só a rede de segurança.

        Diretiva do autor (2026-10-21): a rotina dura até estar recuperada, medida nos
        números — e se passar do teto, para e avisa o agente em vez de esperar cego.
        O alvo padrão é 95% da vida máxima: antes era 215/222 fixos, inalcançáveis com a
        barra em 211, e cada ida parava os 420 s inteiros (conhecimento §89).
        """
        _t, vit0, _c = self.run('look')
        if hp_min is None:
            hp_min = alvo_de_vida(self._vida_maxima())
        if vida(vit0) >= hp_min and mana(vit0) >= mn_min:
            return vit0          # ja' pronta: nada de descansar
        self.cmd('wake', 0.5)
        self.cmd('sleep', 0.5)       # dormir regenera 3 a 4x mais que `rest` (conhecimento §4); no Templo e' seguro
        t0, vit, vida_ant = time.time(), {}, vida(vit0)
        while time.time() - t0 < max_s:
            time.sleep(5)
            texto, vit, combate = self.run('look')
            # o driver mantem "em combate" por alguns segundos depois de um recall: so' conta como ataque o que o texto
            # diz ou uma queda de vida durante o descanso
            if 'lutando contra voce' in normalizar(texto) or (vida(vit) and vida_ant and vida(vit) < vida_ant - 5):
                raise Perdida('atacada enquanto descansava')
            vida_ant = vida(vit) or vida_ant
            if vida(vit) >= hp_min and mana(vit) >= mn_min:
                break
        else:
            print('[XADREZ] ATENCAO: descanso de %d s sem chegar a vida %s/mana %s '
                  '(vida %s, mana %s) — agente: ver o que travou'
                  % (max_s, hp_min, mn_min, vida(vit), mana(vit)), flush=True)
        self.cmd('wake', 0.5)
        self.cmd('stand', 1.5)
        return vit

    def ir_h5(self):
        # logo apos um recall o driver pode manter "em combate" por alguns segundos; o navegar para com Parada(4).
        # Espera, recolhe de novo ao Templo e repete (ate' 3 tentativas) em vez de abortar a etapa.
        for tentativa in range(3):
            try:
                self.nav.navegar(self.salas, 'templo_midgaard', 'xadrez_H5', self.run)
                return
            except Exception as e:                      # navegar.Parada
                if getattr(e, 'codigo', None) not in (3, 4) and 'combate' not in str(e) and 'esperava' not in str(e):
                    raise
                if tentativa == 2:
                    raise
                time.sleep(8)
                self.recall()
                time.sleep(6)

    def recall(self):
        self.cmd('recall', 3)

    def armor(self):
        """Garante a magia armor (CA >= 140) pelo prepara.garantir_armor; ele deixa a personagem na Praca, entao volta ao Templo."""
        import sys as _s
        _s.path.insert(0, str(Path(__file__).resolve().parents[1] / 'camadas'))
        try:
            import prepara
            if prepara.garantir_armor():
                self.recall()
                time.sleep(2)
        except Exception as e:          # nunca derruba a etapa por causa disto; o auditor acusa se a CA ficar baixa
            print('[XADREZ] armor nao confirmado: %s' % e, flush=True)


ESPERA_PRESENCA_S = 60      # diretiva 2026-10-21: peca ausente nao se espera 12 min parado
ESPERA_POLL_S = 10


def tarefa_de_espera(ctx=None):
    """O que fazer enquanto a peca nao volta: empilha tarefas curtas (aproveitar_tempo)."""
    try:
        import aproveitar_tempo
        return aproveitar_tempo.aproveitar(2)
    except Exception as e:      # noqa: BLE001 - tarefa nunca derruba a cascata
        print('[XADREZ] ATENCAO: tarefa de espera falhou (%s); seguindo' % e, flush=True)
        return None


def esperar_presenca(ctx, tipo, max_s=ESPERA_PRESENCA_S, tarefa=None):
    """Espera a peca por `max_s` (default 60 s). Se nao vier, roda `tarefa` e devolve None.

    Quem chama decide o que fazer com o None: `atacar_peca` devolve 'tarefa' e a cascata
    recomeca a ida (a personagem pode ter saido do tabuleiro para trabalhar).
    """
    padrao = re.compile(PRESENCA[normalizar(tipo)] if normalizar(tipo) in PRESENCA else PRESENCA['bispo'])
    ctx.cmd('rest', 1)
    t0 = time.time()
    while time.time() - t0 < max_s:
        texto, vit, combate = ctx.run('look')
        if combate or 'lutando contra voce' in normalizar(texto):
            ctx.cmd('stand', 1)
            return texto
        if padrao.search(normalizar(texto)):
            ctx.cmd('stand', 1)
            return texto
        time.sleep(ESPERA_POLL_S)
    ctx.cmd('stand', 1)
    if tarefa is not None:
        print('[XADREZ] %s nao apareceu em %d s; aproveitando o tempo' % (tipo, max_s), flush=True)
        try:
            tarefa(ctx)
        except Exception as e:      # noqa: BLE001
            print('[XADREZ] ATENCAO: tarefa falhou (%s)' % e, flush=True)
    return None


def atacar_peca(ctx, tab, casa, alvo, tipo, magias, dorme, meta, log=print, espera=True,
                tarefa=tarefa_de_espera):
    """Uma ida: chega na casa, dorme (se for o caso), debuffs, raios com limite de vida. Devolve o resultado."""
    tab.ir(casa)
    m0 = mortes(tipo)
    entrada, ultimo, _c = ctx.cmd('look', 0.5)
    pat = PRESENCA[alvo]
    if not re.search(pat, normalizar(entrada)):
        if not espera:
            log('  %s: sem %s agora; tento a outra casa' % (casa, alvo))
            return 'ausente'
        log('  %s: sem %s agora; esperando o repop' % (casa, alvo))
        entrada = esperar_presenca(ctx, alvo, tarefa=tarefa)
        if entrada is None:
            return 'tarefa'      # a personagem pode ter saido: a cascata recomeca a ida
    mira = '1.' + alvo if alvo == 'torre' else alvo
    if ctx.considerar(mira, log):
        ctx.recall()
        return 'perigo'

    def lance(magia, alvo_magia, espera):
        nonlocal ultimo
        if not pode_lancar(ultimo):
            raise _Recuar()
        r = ctx.cmd("cast '%s' %s" % (magia, alvo_magia), espera)
        ultimo = r[1] or ultimo
        return r

    try:
        return _ida(ctx, lance, alvo, tipo, magias, dorme, entrada, m0, log)
    except _Recuar:
        log('  vida abaixo de %d antes do lance: recall' % VIDA_PISO_LANCE)
        ctx.recall()
        return 'recall'


class _Recuar(Exception):
    """Vida abaixo do piso antes de um lance."""


def _ida(ctx, lance, alvo, tipo, magias, dorme, entrada, m0, log):
    if dorme:
        lance('sleep', '1.' + alvo if alvo == 'torre' else alvo, 2)
        if alvo == 'torre' and len(re.findall('castelo negro', normalizar(entrada))) >= 2:
            lance('sleep', '2.torre', 2)
    for m in magias:
        lance(m, alvo, 1.5)
    for i in range(1, 9):
        texto, vit, combate = lance('lightning bolt', '1.torre' if alvo == 'torre' else alvo, 1.5)
        h = vida(vit)
        log('  raio %d vida=%s mana=%s mortes=%d' % (i, h, mana(vit), mortes(tipo)))
        if mortes(tipo) > m0:
            return 'morto'
        if h and h <= LIMITE_VIDA:
            ctx.recall()
            return 'recall'
    return 'sem_morte'


def cumprir_etapa(nome, log=print):
    ctx = Ctx()
    alvos = ETAPAS[nome]
    tipo = alvos[0][2]
    padrao_morte = r'%s Negr[oa] est.{1,2} mort[oa]!' % tipo
    feitas = lambda: desde_marca(ORDEM[nome], padrao_morte)   # noqa: E731
    meta = len(alvos)
    log('etapa %s: mortes de %s desde a ordem=%d, meta=%d' % (nome, tipo, feitas(), meta))
    for tentativa in range(1, 31):
        if feitas() >= meta:
            log('etapa %s cumprida' % nome)
            return 0
        if not ctx.garantir_templo():
            raise Perdida('nao consegui confirmar o Templo')
        ctx.comer_beber()
        ctx.descansar()
        ctx.ir_h5()
        ctx.cmd("cast 'invisibility'", 3)
        tab = Tabuleiro('H5', ctx.run)
        for casa, alvo, tp, magias, dorme in alvos:
            if feitas() >= meta:
                break
            try:
                res = atacar_peca(ctx, tab, casa, alvo, tp, magias, dorme, meta, log, espera=(tentativa % 2 == 0))
            except Perdida as e:
                log('POSICAO INCERTA: %s -> recall' % e)
                ctx.recall()
                return 3
            log('ida %d %s: %s' % (tentativa, casa, res))
            if res == 'perigo':
                log('consider deu perigo duro em %s: etapa parada (diretiva §2)' % casa)
                return 4
            if res in ('recall', 'tarefa'):
                break
        ctx.recall()
    return 1


def varrer_peoes(meta_mortes=9, log=print):
    """Etapa 1: varre as fileiras 7 a 2 matando peoes negros ate' somar `meta_mortes` mortes no log."""
    ctx = Ctx()
    base = desde_aceite(r'Pe.{1,2}o Negro do Tabuleiro est.{1,2} morto!')
    log('peoes: %d mortes desde a aceitacao; meta %d' % (base, meta_mortes))
    if base >= meta_mortes:
        return 0
    if not ctx.garantir_templo():
        raise Perdida('nao consegui confirmar o Templo')
    ctx.comer_beber()
    ctx.descansar()
    ctx.ir_h5()
    ctx.cmd("cast 'invisibility'", 3)
    tab = Tabuleiro('H5', ctx.run)
    tab.ir('H7')
    sentido = -1
    for fil in (7, 6, 5, 4, 3, 2):
        cols = range(7, -1, -1) if sentido < 0 else range(0, 8)
        for col in cols:
            if nome_casa(col, fil) != tab.casa:
                tab.ir(nome_casa(col, fil))
            texto = ctx.cmd('look', 0.5)[0]
            if re.search(r'pe.{1,2}o negro aqui', normalizar(texto)) or 'peao negro aqui' in normalizar(texto):
                if ctx.considerar('peao negro', log):
                    ctx.recall()
                    return 1
                vit = None
                for _ in range(5):
                    if vit is not None and not pode_lancar(vit):
                        log('vida abaixo de %d antes do lance: recall' % VIDA_PISO_LANCE)
                        ctx.recall()
                        return 1
                    t2, vit, _c = ctx.cmd("cast 'lightning bolt' peao negro", 2)
                    if 'em que voce' in normalizar(t2):
                        break
                time.sleep(2)
            feitas = desde_aceite(r'Pe.{1,2}o Negro do Tabuleiro est.{1,2} morto!')
            if feitas >= meta_mortes:
                log('peoes: %d mortes desde o inicio' % feitas)
                ctx.recall()
                return 0
            _t, vit, _c = ctx.cmd('look', 0.2)
            if (vida(vit) and vida(vit) < 120) or (mana(vit) and mana(vit) < 100):
                log('recursos baixos (vida=%s mana=%s); recall' % (vida(vit), mana(vit)))
                ctx.recall()
                return 1
        sentido = -sentido
    log('peoes: fim da varredura com %d mortes; recall' % desde_aceite(r'Pe.{1,2}o Negro do Tabuleiro est.{1,2} morto!'))
    ctx.recall()
    return 1


def inspecionar_corpo_do_rei(ctx, log):
    """Logo apos a morte do Rei, SEM recall: sala, corpo e o cetro (Dia 159: o recall imediato me tirou de E8 e o corpo voltou vazio)."""
    # so' a CHAVE (e `look`): `get all corpo` trouxe 2 cetros, 2 armaduras de peao, espada e 160 kg (Dia 163), violava o §29 (item
    # sem identify) e o peso impedia pegar o tesouro. O cetro ja' foi entregue (Xeque-mate concluida).
    # `all.chave`: o Rei deixa 3 a 4 chaves e cada `unlock` gasta uma (Dia 163): pegar so' uma rendia 1 tomada por kill
    for c in ('look', 'look in corpo', 'get all.chave corpo', 'get all.chave', 'inventory'):
        t = ctx.cmd(c, 0.6)[0]
        log('  [%s] %s' % (c, ' | '.join(l.strip() for l in t.splitlines() if l.strip() and not re.match(r'^-?\d+hp', l.strip()))[:420]))


def kite_rei(idas=1, log=print, lado='negro'):
    """Etapa final, tatica do autor: chegar, sleep, curse, blind, 1 raio e recall (kite). Exige --rei."""
    L = LADOS[lado]
    nome_lower = L['nome'].lower()
    ctx = Ctx()
    base_mortes = mortes_do_lado(L)       # mortes anteriores do Rei no log nao contam: so' a desta execucao
    for n in range(1, idas + 1):
        if mortes_do_lado(L) > base_mortes:
            log('o Rei %s ja morreu' % L['nome'])
            return 0
        ctx.cmd('wake', 0.5)       # o descanso dorme; um laco interrompido deixa a personagem dormindo e o look falha
        ctx.cmd('stand', 0.5)
        if not ctx.garantir_templo():
            raise Perdida('nao consegui confirmar o Templo')
        ctx.comer_beber()
        if n == 1 or n % 10 == 0:
            ctx.armor()                    # diretiva §26: armor ligada antes de atacar (o auditor reprova CA < 140)
        ctx.descansar(mn_min=130)          # uma ida gasta ~35 mana (sleep + raio); descansar ate' 460 triplicava o ciclo
        ctx.ir_h5()
        if n == 1 or n % 12 == 0:           # invisibilidade dura horas; recastar a cada ida desperdicava mana
            ctx.cmd("cast 'invisibility'", 2)
            ctx.cmd("cast 'detect invisibility'", 2)   # os itens do Rei (cetro, chave) sao INVISIVEIS: sem isto o corpo parece vazio
        tab = Tabuleiro('H5', ctx.run)
        try:
            tab.ir(L['acesso'][0])
            texto, vit, _c = tab.passo(L['acesso'][1])
            log('%s: %s' % (L['casa'], titulo_sala(texto)))
            sala_dormindo = ('rei %s esta dormindo' % nome_lower) in normalizar(texto)   # ele volta a dormir sozinho entre as idas
            ctx.considerar('rei', log)        # antes do 1o sleep (diretiva §2/§22); so' registra: --rei e' a autorizacao do autor
            if sala_dormindo:
                log('  o Rei ja esta dormindo; sem sleep')
            else:
                texto, v_s, _c = ctx.cmd("cast 'sleep' rei", 1.5)
                vit = v_s or vit
            if 'em que voce deseja' in normalizar(texto):
                # sem alvo: o Rei morreu e ainda nao reapareceu. Insistir em `sleep` gera dezenas de recusas seguidas
                # (auditor repeticao-de-recusa, Dia 159); recolhe e espera o repop em vez disso.
                log('o Rei %s esta ausente (repop pendente); recall e espera 45 s' % L['nome'])
                ctx.recall()
                time.sleep(45)
                continue
            dormiu = sala_dormindo or 'dormindo' in normalizar(texto) or 'vai dormir' in normalizar(texto)
            for _t2 in range(1):                 # UMA nova tentativa: com o Rei acordado e me vendo, cada uma custa uma rodada (-76/-84 no Dia 158)
                if dormiu:
                    break
                t2, v2, c2 = ctx.cmd("cast 'sleep' rei", 1.5)
                if c2 or 'lutando contra voce' in normalizar(t2) or (vida(v2) and vida(v2) < 200):
                    break
                dormiu = 'vai dormir' in normalizar(t2) or 'dormindo' in normalizar(t2)
            if not dormiu:
                log('o Rei nao dormiu (3 tentativas); recall')
                ctx.recall()
                continue
            ctx.considerar('rei', log)   # so' registra: o --rei ja' e' a autorizacao explicita do autor
            saude = ctx.cmd('look rei', 0.5)[0]
            m_s = re.search(r'Rei %s est. com ([^\n.]+)' % L['nome'], saude)
            log('  saude do Rei ao chegar: %s' % (m_s.group(1).strip() if m_s else '?'))
            usa = [l.strip() for l in saude.splitlines() if '->' in l]
            log('  o Rei usa: %s' % (' | '.join(usa) if usa else 'NADA (sem equipamento visivel)'))
            # curse e blindness saem do kite de 1 raio (Dia 158): o Rei nunca revida antes do recall, entao nao ha' o que reduzir,
            # e cada um custava ~3 s e mana por ida (o ciclo caia de ~35 s para ~85 s).
            for i in (1,):   # tatica do autor: 1 raio por ida
                if not pode_lancar(vit):
                    raise Perdida('vida %s abaixo de %d antes do raio' % (vida(vit), VIDA_PISO_LANCE))
                _t, vit, _c = ctx.run("cast 'lightning bolt' rei")      # SEM espera: cada segundo aqui pode custar uma rodada do Rei
                if not re.search(r'mortalmente ferido|morrer. logo|esta morto|em pedacos', normalizar(_t)):
                    ctx.run('recall')           # imediato (Dia 158: 3 s de espera antes do recall = -62, -63 e morte)
                h = vida(vit)
                barras = re.findall(r'(\{[-<>]{10}\})\s+o Rei %s' % L['nome'], _t)
                dano = re.findall(r'impacto total! \[(\d+)\]', _t)
                log('  raio %d vida=%s mana=%s dano=%s barra_do_rei=%s' % (i, h, mana(vit), dano, barras[-1] if barras else '?'))
                # "mortalmente ferido" (barra vazia): o mob NAO luta mais e morre sozinho em instantes, SEM credito
                # se eu for embora (aconteceu no Dia 158: recall nessa hora = Rei morto sem EXP e sem cetro). Fica e remata.
                if re.search(r'mortalmente ferido|morrer. logo', normalizar(_t)):
                    log('  Rei MORTALMENTE FERIDO: ficando para rematar e pegar o cetro')
                    for _k in range(5):
                        tk, vit, _c = ctx.cmd("cast 'lightning bolt' rei", 2)
                        if 'esta morto' in normalizar(tk) or 'em pedacos' in normalizar(tk) or mortes_do_lado(L) > base_mortes:
                            break
                    inspecionar_corpo_do_rei(ctx, log)
                    log('REI %s MORTO; a personagem FICOU em %s: confira o corpo/chaves a mao e so entao recall' % (L['nome'].upper(), L['casa']))
                    return 0
                if mortes_do_lado(L) > base_mortes or re.search(r'esta morto|em pedacos', normalizar(_t)):
                    inspecionar_corpo_do_rei(ctx, log)
                    log('REI %s MORTO; a personagem FICOU em %s: confira o corpo/chaves a mao e so entao recall' % (L['nome'].upper(), L['casa']))
                    return 0
                if h and h <= LIMITE_VIDA + 10:
                    break
        except Perdida as e:
            log('POSICAO INCERTA: %s -> recall' % e)
        ctx.recall()
        log('ida %d ao Rei concluida' % n)
    return 1


def main(argv=None):
    ap = argparse.ArgumentParser(description='Cascata da Xeque-mate no tabuleiro (rastreio de posicao).')
    ap.add_argument('--etapa', required=True, choices=sorted(ETAPAS) + ['f1', 'peoes', 'rei'])
    ap.add_argument('--rei', action='store_true', help='confirma o kite no Rei (risco de morte)')
    ap.add_argument('--lado', choices=sorted(LADOS), default='negro', help='qual Rei (o branco exige --excecao-rei-branco)')
    ap.add_argument('--excecao-rei-branco', action='store_true', help='autorizacao do autor (DECISOES §17) para matar o Rei Branco UMA vez')
    ap.add_argument('--idas', type=int, default=1, help='idas do kite (so no Rei)')
    a = ap.parse_args(argv)
    try:
        if a.etapa == 'f1':
            ctx = Ctx()
            ctx.comer_beber()
            ctx.ir_h5()
            tab = Tabuleiro('H5', ctx.run)
            for d in ROTA_F1:          # ancora pela borda leste: H2, depois w w ate' F2 e s para F1
                tab.passo(d)
                time.sleep(0.4)
            assert tab.casa == 'F1'
            print('em F1')
            return 0
        if a.etapa == 'peoes':
            return varrer_peoes()
        if a.etapa == 'rei':
            if not a.rei:
                print('o kite no Rei exige --rei (risco de morte; a morte cancela a missao)')
                return 2
            if a.lado == 'branco' and not a.excecao_rei_branco:
                print('o Rei Branco e excecao de moralidade do autor (DECISOES §17): exige --excecao-rei-branco e so mata UMA vez')
                return 2
            return kite_rei(a.idas, lado=a.lado)
        return cumprir_etapa(a.etapa)
    except Perdida as e:
        print('PARADO: %s -> recall' % e)
        try:
            Ctx().recall()
        except Exception as e2:   # noqa: BLE001 - o recall e' o ultimo recurso
            print('recall falhou: %s' % e2)
        return 3


if __name__ == '__main__':
    sys.exit(main())
