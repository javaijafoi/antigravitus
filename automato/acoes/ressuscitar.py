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

# A morte devolve TODO o equipamento ao inventario desvestido (Dia 161: CA 37, Acerto 0 e 308 kg depois da
# 1a ressurreicao, 18 idas de kite assim e fome). Item a item, nunca `wear all`: a Lanca do Cavaleiro Negro
# e' amaldicoada. (comando, palavra que o item tem no `inventory`, sem acento e em minusculas)
REEQUIPAR = (
    ('wear coroa', 'coroa da rainha branca'), ('wear brinco', 'brinco de novato'),
    ('wear colar', 'colar com uma pedra'), ('wear cruz', 'cruz ansada'),
    ('wear mochila', 'mochila de pellinore'),    # vestida no lugar do manto: so' assim ela reduz o peso (§23)
    ('wear bracadeiras', 'bracadeiras de novato'), ('wear luvas', 'luvas de couro'),
    ('wear rosario', 'rosario'), ('wear bracelete', 'bracelete de prata'),
    ('wear escudo', 'escudo de aco'), ('wear cinturao', 'cinturao de rodeio'),
    ('wear calca', 'calca de couro'), ('wear dourado', 'anel dourado'), ('wear rubi', 'anel de rubi'),
    ('wear veste', 'veste de escamas'),   # slot `no corpo`: CA +8, vida maxima +20, FOR +2 (Dia 161); a tunica dourada, CA +18, disputa o mesmo slot
    ('wear botas', 'botas negras'),       # slot `nos pes`: CA +13
    ('wear coleira', 'coleira do dragao'),   # 2o slot do pescoco; a Cruz Ansada (ANTI-NEUTRO) da choque com alinhamento baixo
    ('wield ferro', 'lamina de ferro'), ('hold cajado', 'cajado retorcido'),
)


def _sem_acento(texto):
    import unicodedata
    return ''.join(c for c in unicodedata.normalize('NFD', texto or '') if unicodedata.category(c) != 'Mn').lower()


def comandos_pos_morte(inventario):
    """Pura: comer, beber e reequipar o que esta no `inventory` (so' a lista conhecida). Nada de `wear all`.

    A coroa so' veste se ha' UMA coroa no inventario (a da Rainha Negra e' ANTI-BOM e `wear coroa` pegaria a errada).
    """
    inv = _sem_acento(inventario)
    cmds = []
    if 'pao recheado' in inv:
        cmds.append('eat pao')
    if 'cantil' in inv:
        cmds.append('drink cantil')
    for cmd, chave in REEQUIPAR:
        if chave not in inv:
            continue
        if cmd == 'wear coroa' and inv.count('coroa') != 1:
            continue
        cmds.append(cmd)
    return cmds


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
    inv, _, _ = run('inventory')
    for cmd in comandos_pos_morte(inv):
        print('POS-MORTE:', cmd, flush=True)
        run(cmd)
    t, _, _ = run('score tudo')
    print('VIDA:', [l.strip() for l in t.split('\n') if 'Vida:' in l])
    return 0


if __name__ == '__main__':
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    sys.exit(main())
