"""Navegacao por sala-marco para sessoes conduzidas por agente (nunca fala com NPC).

Cada passo envia UM comando ao driver (play.py), le o titulo da sala que veio na resposta e
compara com o nome esperado. Para na primeira divergencia, em combate ou recusa de movimento.
Falas de missao (say/ask/whisper) sao recusadas aqui: diretiva do jogo, secoes 19 e 20.

Uso: python automato/rotas/nav.py <rota> [--de N] [--ate N]
     python automato/rotas/nav.py --listar
Agente: Claude Sonnet 5.5 (claude-sonnet-5-5), Dia 157.
"""
import argparse, os, re, subprocess, sys, unicodedata

RAIZ = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
PLAY = os.path.join(RAIZ, 'automato', 'nucleo', 'driver', 'play.py')
PROIBIDOS = ('say ', 'ask ', 'whisper', 'tell ', 'give ', 'quit', 'kill ', 'hit ')

# (direcao, nome esperado da sala de chegada). Nomes sem acento, minusculos.
TEMPLO_A_PRACA_JARETH = (
    [('n', 'o altar do templo'), ('n', 'atras do altar')]
    + [('n', 'o grande campo de midgaard')] * 3
    + [('n', 'um caminho dentre os campos'), ('e', 'um caminho dentre os campos'),
       ('n', 'o comeco da estrada'), ('n', 'a estrada midgaard-jareth'), ('n', 'a estrada midgaard-jareth'),
       ('n', 'um posto de guarda na estrada'), ('n', 'numa pequena vila'), ('n', 'o centro do vilarejo'),
       ('n', 'numa pequena vila'), ('n', 'um posto de guarda na estrada'),
       ('n', 'a estrada midgaard-jareth'), ('n', 'a estrada midgaard-jareth')]
    + [('e', 'a estrada midgaard-jareth')] * 5
    + [('e', 'nas proximidades da cidade'), ('e', 'o portao oeste'), ('e', 'avenida floris'), ('e', 'uma praca')]
)

ROTAS = {
    'templo-praca-jareth': TEMPLO_A_PRACA_JARETH,
    'praca-floris1': [('e', 'avenida floris')],
}


def norm(s):
    s = s.strip()
    if 'Ã' in s or 'Â' in s:
        try:
            s = s.encode('latin-1').decode('utf-8')
        except UnicodeError:
            pass
    s = unicodedata.normalize('NFKD', s)
    return re.sub(r'\s+', ' ', ''.join(c for c in s if ord(c) < 128)).lower().strip()


def enviar(cmd):
    if cmd.lower().startswith(PROIBIDOS):
        raise SystemExit('recusado (fala/give/combate nao se automatiza): ' + cmd)
    r = subprocess.run([sys.executable, '-I', PLAY, cmd], capture_output=True, cwd=RAIZ, timeout=120)
    return r.stdout.decode('utf-8', errors='replace')


def titulo(saida):
    linhas = [l for l in saida.splitlines() if l.strip() and not l.startswith(('>>>', 'DICA', '['))]
    return norm(linhas[0]) if linhas else ''


def andar(passos, de=0, ate=None):
    for i, (d, esperado) in enumerate(passos[de:ate], start=de):
        saida = enviar(d)
        t = titulo(saida)
        if re.search(r'lutando|ocupado|nao pode ir|esta muito relaxado|dormindo', norm(saida)) and esperado not in t:
            print(f'PARADA no passo {i} ({d}): recusa/combate: {t}'); return False
        if esperado not in t:
            print(f'PARADA no passo {i} ({d}): esperava "{esperado}", veio "{t}"'); return False
        print(f'{i:02d} {d} -> {t}')
    return True


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('rota', nargs='?')
    ap.add_argument('--de', type=int, default=0)
    ap.add_argument('--ate', type=int)
    ap.add_argument('--listar', action='store_true')
    a = ap.parse_args()
    if a.listar or not a.rota:
        for k, v in ROTAS.items(): print(k, len(v), 'passos')
        sys.exit(0)
    sys.exit(0 if andar(ROTAS[a.rota], a.de, a.ate) else 3)
