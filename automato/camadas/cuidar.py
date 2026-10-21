# -*- coding: utf-8 -*-
"""cuidar.py - o cuidado consigo mesma, em campo.

Terceira camada, separada das outras duas de proposito:

    vigia.py    OBSERVA. Le o log e o driver, e reporta. Nunca manda comando.
    cuidar.py   CUIDA.  Come, bebe, veste armadura e invisibilidade, AQUI.
    prepara.py  RECARREGA. Vai a cidade comprar pao, encher cantil, guardar
                ouro e dormir - so' quando o estoque acaba.

O que estava errado antes: o `prepara.py` fazia as duas ultimas coisas e era
chamado a qualquer sinal de fome. Resultado: com seis paes na bolsa, no meio do
mato, a rotina parava e voltava para a padaria. Fome pede COMIDA; a cidade entra
quando a comida acaba.

Este arquivo NAO VAI A CIDADE. A unica coisa que ele move e' um passo, para sair
da area sem magia (o Templo de Midgaard recusa conjuracao), porque sem isso nao
ha como vestir armadura nem invisibilidade.

Codigos de saida (o `turno.py` usa):
    0  tudo em ordem
    2  precisa RECARREGAR -> e' a vez do prepara.py
    1  nao consegui resolver sozinha
"""
import re
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'nucleo'))
import base           # noqa: E402
import config         # noqa: E402
import inventario     # noqa: E402
from base import run, andar, vida_frac   # noqa: E402

LIMIAR_PAO = 2          # minimo para partir / abaixo disso, recarrega
LIMIAR_AGUA = 0.0       # cantil vazio e' o gatilho; meio cantil nao e'
AREA_SEM_MAGIA = 'templo de midgaard'
PRACA = 'praca do templo'

# A decisao de re-conjurar e' por DADO, nao por relogio: o `score` mostra as horas de
# JOGO que restam (`armor ( 24 horas )`), e `horas_restantes()` le dali. O cache por
# tempo que existia antes (25 min) era um chute sobre a duracao — e chute errado deixa
# a personagem sem armadura sem ninguem perceber. Ver `config.horas_de_jogo_para_segundos_reais()`.
_MAGIAS = {'armadura': None, 'invisibilidade': None, 'em': 0.0,
           'local': None, 'respostas': {}}

# Respostas medidas no servidor. A FALHA e' conferida ANTES do sucesso: o
# sucesso da invisibilidade ("Voce desaparece.") contem a palavra 'desaparece',
# que tambem aparece na falha ("Sua magia falha e desaparece.").
FALHA_MAGIA = ('falha', 'nao consegue', 'sem forcas', 'nao tem mana', 'desconhece',
               'como?!', 'nao sabe')
OK_ARMADURA = ('sente alguem te protegendo', 'sente-se protegid', 'esta protegid')
OK_INVISIBILIDADE = ('voce desaparece', 'desaparece da vista')
# Sem evidencia ainda. Se aparecer, entra aqui - e' assim que o texto entra.
JA_ATIVA = ('ja esta', 'ja se encontra', 'nada acontece')

IGNORAR_TITULO = ('saidas:', 'voce ', 'vida:', 'mana:', 'movimento:', 'banco:',
                  'carregando:', 'experiencia:', 'proximo nivel:', 'alinhamento:')


def sem_acento(texto):
    import unicodedata
    t = unicodedata.normalize('NFKD', (texto or '').lower())
    return ''.join(c for c in t if not unicodedata.combining(c))


def titulo(texto):
    for linha in (texto or '').split('\n'):
        limpa = re.sub(r'^-?\d+\s*hp\s+-?\d+\s*mn\s+-?\d+\s*mv\s*>\s*', '', linha.strip()).strip()
        if not limpa or limpa.startswith('['):
            continue
        b = sem_acento(limpa)
        if any(b.startswith(p) for p in IGNORAR_TITULO) or b.endswith(':'):
            continue
        return b
    return '?'


def sala_atual(tentativas=3):
    for _ in range(tentativas):
        t, _, _ = run('look')
        nome = titulo(t)
        if nome != '?':
            return nome
        time.sleep(0.4)
    return '?'


def score(tentativas=3):
    """Le o score de verdade. Sem isto o chamador conclui 'sem fome' e nao come."""
    for _ in range(tentativas):
        t, _, _ = run('score tudo')
        if 'situa' in sem_acento(t) or 'vida:' in sem_acento(t):
            break
        print('[CUIDAR] score nao chegou; tentando de novo', flush=True)
        time.sleep(0.5)
    return t


def conta_comida():
    """Unidades de comida na bolsa. None = nao consegui ler (NAO e' zero)."""
    return inventario.contar_comida()


def agua_no_cantil():
    """0.0 vazio .. 1.0 cheio. None = nao consegui ler."""
    return inventario.agua_no_cantil()


def situacao():
    """Fome, sede, comida e agua - confirmados pelo servidor."""
    score()
    s = base.suprimentos()
    return {'fome': bool(s.get('fome')), 'sede': bool(s.get('sede')),
            'comida': conta_comida(), 'agua': agua_no_cantil()}


def comer(limite=6):
    for _ in range(limite):
        score()
        if not base.suprimentos().get('fome'):
            return True
        if conta_comida() == 0:      # so' o ZERO CONFIRMADO impede
            return False
        run('eat pao')
    score()
    return not base.suprimentos().get('fome')


def beber(limite=6):
    """Bebe do cantil. A fonte so' entra quando o cantil esta' vazio."""
    for _ in range(limite):
        score()
        if not base.suprimentos().get('sede'):
            return True
        if agua_no_cantil() == 0.0:  # so' o VAZIO CONFIRMADO impede
            return False
        run('drink cantil')
    score()
    return not base.suprimentos().get('sede')


def _conjurar(magia, marcas, ja_ativa=()):
    """Conjura e devolve (ok, resposta_normalizada).

    Nunca presume duracao: so' vale o que o servidor responder. A resposta crua
    e' devolvida para o chamador registrar - e' assim que o texto da expiracao
    entra no conhecimento, em vez de ser adivinhado.
    """
    t, _, _ = run("cast '%s'" % magia)
    b = sem_acento(t)
    if any(f in b for f in FALHA_MAGIA):
        return False, b
    if any(m in b for m in marcas):
        return True, b
    if any(j in b for j in ja_ativa):
        return True, b
    return False, b


def sair_da_area_sem_magia():
    """O Templo de Midgaard recusa magia. Um passo abaixo resolve.

    Isto e' reposicionamento de autocuidado, NAO viagem: nao sai da cidade, nao
    compra nada, nao dorme. A viagem de recarga e' do prepara.py.
    """
    nome = sala_atual()
    if AREA_SEM_MAGIA in nome and PRACA not in nome:
        run('d')
        nome = sala_atual()
    if PRACA not in nome and AREA_SEM_MAGIA in nome:
        return False, nome
    return True, nome


RX_BUFF = re.compile(r"(armor|invisibility|invisibilidade)\s*\(\s*(\d+)\s*horas?\s*\)", re.I)
# Abaixo disto, re-conjura. 4 horas de JOGO ~ 5 min reais (1 h de jogo ~ 75 s).
HORAS_MINIMAS_MAGIA = 4


def horas_restantes(texto, magia):
    """Horas de JOGO que restam da magia, lidas do `score`. ID: horas_restantes.

    `None` = a magia nao aparece no score, ou seja, nao esta' ativa. Antes a decisao de
    re-conjurar era um cache de 25 min: um chute sobre a duracao. O `score` diz a
    duracao de verdade (`armor ( 24 horas )`), e ela e' em horas de JOGO.
    """
    alvo = sem_acento(magia)[:5]
    for m in RX_BUFF.finditer(texto or ''):
        if sem_acento(m.group(1))[:5] == alvo:
            return int(m.group(2))
    return None


def manter_magias(forcar=False):
    """Armadura e invisibilidade decididas pelo DADO: as horas que o `score` mostra.

    Sem `forcar`, so' re-conjura o que caiu abaixo de HORAS_MINIMAS_MAGIA. O cache por
    tempo saiu: ele era um chute sobre a duracao, e um chute errado deixa a personagem
    sem armadura sem ninguem perceber.
    """
    texto = situacao()['texto']
    arm_h = horas_restantes(texto, 'armor')
    inv_h = horas_restantes(texto, 'invisibility')
    falta_arm = forcar or arm_h is None or arm_h < HORAS_MINIMAS_MAGIA
    falta_inv = forcar or (config.USAR_INVISIBILIDADE
                           and (inv_h is None or inv_h < HORAS_MINIMAS_MAGIA))
    if not falta_arm and not falta_inv:
        if not config.USAR_INVISIBILIDADE:
            # Comercio exige personagem visivel; `visible` e' inofensivo quando ja' esta'.
            run('visible')
        return {'armadura': True, 'invisibilidade': True, 'local': _MAGIAS['local'],
                'motivo': '', 'cache': True,
                'horas': {'armor': arm_h, 'invisibility': inv_h}}

    onde = sala_atual()
    if AREA_SEM_MAGIA in onde and PRACA not in onde:
        ok, onde = sair_da_area_sem_magia()
        if not ok:
            return {'armadura': False, 'invisibilidade': False, 'local': onde,
                    'motivo': 'area sem magia (o Templo recusa conjuracao)', 'cache': False}
    if vida_frac() < 0.35:
        return {'armadura': False, 'invisibilidade': False, 'local': onde,
                'motivo': 'vida baixa demais para gastar mana', 'cache': False}

    if falta_arm:
        arm, resp_a = _conjurar('armor', OK_ARMADURA, JA_ATIVA)
    else:
        arm, resp_a = True, 'ainda ativa (%s horas no score)' % arm_h
    if config.USAR_INVISIBILIDADE:
        if falta_inv:
            inv, resp_i = _conjurar('invisibility', OK_INVISIBILIDADE, JA_ATIVA)
        else:
            inv, resp_i = True, 'ainda ativa (%s horas no score)' % inv_h
    else:
        # Visibilidade e' requisito de comercio: "Nao negocio com quem nao vejo!".
        # Sem a magia, a protecao vem da ROTA - evitar as salas de risco alto.
        # `visible` e' inofensivo quando ja' esta' visivel, entao roda sempre.
        t, _, _ = run('visible')
        inv, resp_i = True, ' '.join(sem_acento(t).split())[:90]
    _MAGIAS.update({'armadura': arm, 'invisibilidade': inv, 'em': time.time(), 'local': onde,
                    'respostas': {'armor': ' '.join(resp_a.split())[:160],
                                  'invisibility': ' '.join(resp_i.split())[:160]}})
    print('[CUIDAR] armor=%s (%s) | invisibility=%s (%s)'
          % ('ok' if arm else 'nao', ' '.join(resp_a.split())[:60],
             'ok' if inv else 'nao', ' '.join(resp_i.split())[:60]), flush=True)
    return {'armadura': arm, 'invisibilidade': inv, 'local': onde, 'cache': False,
            'horas': {'armor': arm_h, 'invisibility': inv_h},
            'resposta_armor': _MAGIAS['respostas']['armor'],
            'resposta_invisibility': _MAGIAS['respostas']['invisibility'],
            'motivo': '' if (arm and inv) else 'conjuracao nao confirmada'}


def cuidar(forcar_magias=False):
    """Passa o cuidado completo. NUNCA viaja a cidade.

    devolve {
        'ok': tudo resolvido em campo,
        'precisa_repor': a bolsa/o cantil acabaram - e' a vez do prepara.py,
        'motivos': [...], 'acoes': [...],
    }
    """
    acoes, motivos = [], []
    s = situacao()
    precisa = False

    if s['fome']:
        comeu = comer()
        acoes.append('comeu' if comeu else 'sem comida')
        if not comeu:
            precisa = True
            motivos.append('fome sem comida na bolsa')
    if s['sede']:
        bebeu = beber()
        acoes.append('bebeu' if bebeu else 'sem agua')
        if not bebeu:
            precisa = True
            motivos.append('sede sem agua no cantil')

    magias = manter_magias(forcar=forcar_magias)
    acoes.append('magias:' + ('ok' if (magias['armadura'] and magias['invisibilidade'])
                              else 'incompletas'))
    if not (magias['armadura'] and magias['invisibilidade']):
        motivos.append(magias['motivo'] or 'magias incompletas')

    fim = situacao()
    # None = nao consegui ler. Nao sei NAO e' "acabou": disparar viagem a cidade
    # por uma leitura corrompida e' o mesmo defeito de parar por fome com a
    # mochila cheia. So' o numero CONFIRMADO e baixo justifica recarga.
    if fim['comida'] is not None and fim['comida'] < LIMIAR_PAO:
        precisa = True
        motivos.append('estoque de comida %d < %d' % (fim['comida'], LIMIAR_PAO))
    elif fim['comida'] is None:
        motivos.append('nao consegui ler a bolsa (nao conto isso como falta)')
    if fim['agua'] is not None and fim['agua'] <= LIMIAR_AGUA:
        precisa = True
        motivos.append('cantil vazio')

    return {'ok': not precisa and not motivos, 'precisa_repor': precisa,
            'motivos': motivos, 'acoes': acoes, 'situacao': fim, 'magias': magias}


def main():
    import argparse
    ap = argparse.ArgumentParser(description='Cuidado em campo: comer, beber, armadura e invisibilidade.')
    ap.add_argument('--forcar-magias', action='store_true')
    ap.add_argument('--json', action='store_true')
    args = ap.parse_args()

    r = cuidar(forcar_magias=args.forcar_magias)
    if args.json:
        import json
        print(json.dumps(r, ensure_ascii=False))
    else:
        print('[CUIDAR] ok=%s precisa_repor=%s' % (r['ok'], r['precisa_repor']), flush=True)
        for m in r['motivos']:
            print('[CUIDAR]   -', m, flush=True)
        print('[CUIDAR] acoes: %s' % ', '.join(r['acoes']), flush=True)
    if r['precisa_repor']:
        return 2
    return 0 if r['ok'] else 1


if __name__ == '__main__':
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    sys.exit(main())
