# -*- coding: utf-8 -*-
"""novatos.py - Rotina de caça e colheita na Masmorra dos Novatos de Midgaard.

Alvos:
- Monstro Novato (moedas + punhal)
- Novato Zumbi (moedas)
- Coisa Assustadora / Inseto Rastejante
- Grande Minotauro (95 ouros + chifres + pele para venda no armeiro a 50 cada)

Coleta itens leves de revenda (punhal, chifre, pele, armadura) e guarda na mochila de Pellinore.
"""
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'nucleo'))

from base import *

NOME = 'novatos'
DESCRICAO = 'Caçada rápida na Masmorra dos Novatos com coleta e revenda de espólios leves.'

MOBS_NOVATOS = [
    ('minotauro', 'minotauro'),
    ('novato zumbi', 'zumbi'),
    ('zumbi', 'zumbi'),
    ('monstro novato', 'monstro'),
    ('monstro', 'monstro'),
    ('coisa assustadora', 'coisa'),
    ('inseto rastejante', 'inseto'),
]


def ir_aos_novatos():
    run('wake'); run('stand')
    for _ in range(4):
        andar('n')
    andar('e') # A Entrada da Área dos Novatos
    andar('n') # O Começo Da Passagem
    t, _, _ = run('look')
    return 'Passagem' in t or 'Novatos' in t or 'Corredor' in t


def matar_alvo(alvo):
    perigo = considerar(alvo)   # diretiva §2: consider antes do primeiro ataque a cada alvo
    if perigo:
        print(f'[novatos] consider {alvo}: "{perigo}" -> nao ataco', flush=True)
        return False
    print(f"[novatos] Atacando {alvo} com Lightning Bolt...", flush=True)
    t, v, em_combate = run(f"cast 'lightning bolt' {alvo}")
    if 'morreu' in t.lower() or 'morto' in t.lower() or 'cai sem vida' in t.lower() or not em_combate:
        coletar_espolios(alvo)
        return True

    rounds = 0
    while em_combate and rounds < 5:
        rounds += 1
        time.sleep(0.4)
        t, v, em_combate = run(f"cast 'lightning bolt' {alvo}")
        if 'morreu' in t.lower() or 'morto' in t.lower() or 'cai sem vida' in t.lower() or not em_combate:
            break

    coletar_espolios(alvo)
    return True


def coletar_espolios(alvo):
    """Saque direto de alta eficiência: 1 único comando por corpo."""
    if alvo == 'minotauro':
        run('get all.chifre corpo')
        run('get all.pele corpo')
        run('get all.moedas corpo')
    else:
        run('get all corpo')


def organizar_espolios():
    """Empacotamento em lote no fim da masmorra: 1 única triagem e guarda."""
    inv, _, _ = run('inventory')
    inv_lower = inv.lower()

    if 'torre negra' in inv_lower:
        run('drop armadura torre')
    if 'amaldiçoada' in inv_lower or 'amaldiçoado' in inv_lower:
        run('drop all.amaldiçoada')
        run('drop all.amaldiçoado')

    tem_armeiro = any(x in inv_lower for x in ['chifre', 'pele', 'armadura'])
    tem_ferreiro = 'espada' in inv_lower

    if tem_armeiro:
        run('put all.chifre mochila')
        run('put all.pele mochila')
        run('put all.armadura mochila')
    if tem_ferreiro:
        run('put all.espada mochila')

    return tem_armeiro, tem_ferreiro


def varrer_novatos(max_abates=6):
    reiniciar_relogio()
    caminho = [
        'e',       # O Corredor Sujo
        'e',       # O Cruzamento
        's',       # Mais Corredor (zumbis)
        's',       # Fim do Corredor (monstros novatos)
        'n', 'n',  # Retorna ao Cruzamento
        'n',       # Um Caminho Iluminado
        'e',       # Entrada do Alquimista / Sacada
        'w', 's',  # Retorna ao Cruzamento
        'w',       # O Corredor Sujo
        's',       # Pequena Sala do Guarda
        'n', 'w'   # Retorna ao Começo da Passagem
    ]
    abates = 0

    for d in caminho:
        if abates >= max_abates or estourou(180):
            break
        andar(d)
        t, _, _ = run('look')

        # Detecta mobs da lista
        for marca, kw in MOBS_NOVATOS:
            if marca in t.lower() and 'corpo de' not in t.lower() and 'lutando' not in t.lower():
                print(f"[novatos] Mob encontrado: {marca} ({kw})", flush=True)
                if matar_alvo(kw):
                    abates += 1
                    print(f"[novatos] Abate confirmado! Total: {abates}", flush=True)
                break

    return abates


def vender_espolios(tem_armeiro, tem_ferreiro):
    voltar_ao_templo()
    run('stand')

    # 1. Armeiro: vende chifres, peles e armaduras SE existirem
    if tem_armeiro:
        run('get all.chifre mochila')
        run('get all.pele mochila')
        run('get all.armadura mochila')

        inv, _, _ = run('inventory')
        inv_lower = inv.lower()

        for m in ['s', 's', 'w', 's']:
            andar(m)
        t, _, _ = run('look')
        if 'Armaduras' in t or 'Armeiro' in t or 'armaduras' in t:
            print("[novatos] Vendendo no Armeiro...", flush=True)
            if 'chifre' in inv_lower:
                run('sell 5 chifre')
                run('sell chifre')
            if 'pele' in inv_lower:
                run('sell 5 pele')
                run('sell pele')
            if 'armadura' in inv_lower:
                run('sell 5 armadura')
                run('sell armadura')
            run('put all.chifre mochila')
            run('put all.pele mochila')
            run('put all.armadura mochila')
        voltar_ao_templo()
        run('stand')

    # 2. Ferreiro: vende espadas SE existirem
    if tem_ferreiro:
        run('get all.espada mochila')
        for m in ['s', 's', 'e', 'e', 'n']:
            andar(m)
        t, _, _ = run('look')
        if 'Armas' in t or 'Ferreiro' in t or 'armas' in t:
            print("[novatos] Vendendo no Ferreiro...", flush=True)
            run('sell 5 espada')
            run('sell espada')
            run('put all.espada mochila')
        voltar_ao_templo()
        run('stand')

    run('save')


def executar(max_abates=6):
    reiniciar_relogio()
    if not ir_aos_novatos():
        print("[novatos] Falha ao entrar na Área dos Novatos.", flush=True)
        voltar_ao_templo()
        return 0

    abates = varrer_novatos(max_abates=max_abates)
    print(f"[novatos] Varrida concluída com {abates} abates.", flush=True)

    tem_armeiro, tem_ferreiro = False, False
    if abates > 0:
        tem_armeiro, tem_ferreiro = organizar_espolios()

    voltar_ao_templo()

    if tem_armeiro or tem_ferreiro:
        vender_espolios(tem_armeiro, tem_ferreiro)
    else:
        run('save')

    return abates


if __name__ == '__main__':
    executar()
