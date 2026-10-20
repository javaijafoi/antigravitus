# -*- coding: utf-8 -*-
"""ressuscitar.py - volta da morte: do Paraiso/Inferno ate' a Fonte da Vida.

Depois de morrer a personagem cai no Paraiso (ou no Inferno). O caminho de volta e' achar o portal
escondido: a sala certa traz a dica "uma curiosa energia magica... chama sua atencao para o <direcao>";
segue-se a direcao, `enter portal`, e ao norte pelo Vazio/Purgatorio ate' a Fonte da Vida, onde
`drink fonte` ressuscita (diretiva de jogo par.6). O driver pode ficar parado no menu de morte
("Escolha uma das opcoes do menu!"): ai' manda `_RAW 1` antes (conhecimento par.73).

Fala com o driver por `base.run` (token de automato/runtime/.controller, origem `ressuscitar` no
transcript e guarda de repeticao). Antes usava um cliente proprio, com o token num caminho antigo e
sem origem.

Uso: python automato/acoes/ressuscitar.py        (live_daemon.py no ar)
"""
import re
import sys
from pathlib import Path

# O turno chama este arquivo como `automato/acoes/ressuscitar.py`, e nesse
# caminho o `nucleo/` nao esta' no sys.path - o import estourava com
# ModuleNotFoundError e a resurreicao simplesmente NAO acontecia.
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'nucleo'))

DIR = {'norte': 'n', 'sul': 's', 'leste': 'e', 'oeste': 'w', 'cima': 'u', 'baixo': 'd'}
# "Uma curiosa energia magica, muito viva e tenaz, chama sua atencao para o leste." e
# "Uma curiosa saida, para cima, chama sua atencao." (as duas formas estao nos logs do Dia 156)
_DICA = re.compile(r'aten.{1,2}o para o (norte|sul|leste|oeste)|curiosa sa.{1,2}da, para (cima|baixo)')
_MENU = re.compile(r'Escolha uma das op.{1,4}es do menu|^\s*Menu Principal\s*$', re.M)


def proximo_comando(texto):
    """O que mandar a partir do texto da sala (pura). 'drink fonte' = chegou; None nunca."""
    t = texto or ''
    if _MENU.search(t):
        return '_RAW 1'
    if 'Fonte da Vida' in t:
        return 'drink fonte'
    if 'Portal Escondido' in t:
        return 'enter portal'
    if 'Vazio' in t:
        return 'n'
    m = _DICA.search(' '.join(t.split()))       # a dica pode quebrar de linha
    if m:
        return DIR[m.group(1) or m.group(2)]
    return 'n'


def main(max_passos=40):
    from base import run
    for passo in range(max_passos):
        t, _, _ = run('look')
        cmd = proximo_comando(t)
        print(f'{passo}: {cmd}', flush=True)
        if cmd == 'drink fonte':
            print('DRINK:', ' '.join(run(cmd)[0].split())[:120], flush=True)
            break
        run(cmd)
    t, _, _ = run('score tudo')
    print('VIDA:', [l.strip() for l in t.split('\n') if 'Vida:' in l])
    return 0


if __name__ == '__main__':
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    sys.exit(main())
