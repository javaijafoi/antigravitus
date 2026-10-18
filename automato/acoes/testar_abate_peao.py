# -*- coding: utf-8 -*-
"""testar_abate_peao.py - Teste de abate de 1 peão negro, coleta de loot e retorno seguro.
"""
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'nucleo'))

from base import *

def main():
    print("[abate_peao] Saindo do Templo...", flush=True)
    run('wake'); run('stand')
    for _ in range(4):
        andar('n')
    for _ in range(3):
        andar('w')
    andar('w') # Casa Branca de entrada
    
    # Avança para achar um peão negro desocupado
    grid = ['w', 'n', 'w', 's', 'w', 'n', 'e']
    achou = False
    
    for d in grid:
        andar(d)
        t, _, _ = run('look')
        if 'peão negro' in t.lower() or 'peao negro' in t.lower():
            if 'lutando' in t.lower():
                print(f"[abate_peao] Peão em combate com outro jogador, passando...", flush=True)
                continue
            print(f"[abate_peao] Peão encontrado!", flush=True)
            achou = True
            break
            
    if not achou:
        print("[abate_peao] Nenhum peão livre encontrado.", flush=True)
        voltar_ao_templo()
        run('save')
        return False

    r_cons, _, _ = run('consider peao')
    print(f"[abate_peao] Consider: {r_cons.strip()}", flush=True)

    print("[abate_peao] Iniciando combate com Lightning Bolt...", flush=True)
    t, v, em_combate = run("cast 'lightning bolt' peao")
    print(f"[abate_peao] Turno 1: {t.strip()[:160]}", flush=True)

    rounds = 0
    while em_combate and rounds < 10:
        rounds += 1
        time.sleep(1)
        # Magia rápida de finalização
        t, v, em_combate = run("cast 'burning hands' peao")
        print(f"[abate_peao] Turno {rounds+1}: {t.strip()[:160]}", flush=True)
        if 'morreu' in t.lower() or 'morto' in t.lower() or 'cai sem vida' in t.lower() or not em_combate:
            break

    print("[abate_peao] Coletando espólio...", flush=True)
    r_get, _, _ = run('get all corpo')
    print(f"[abate_peao] Loot: {r_get.strip()}", flush=True)

    # Inspeciona inventário
    inv, _, _ = run('inventory')
    print(f"[abate_peao] Inventário após loot:\n{inv.strip()}", flush=True)

    # Guarda na mochila para não pesar
    run('put all.armadura mochila')
    run('put all.escudo mochila')
    run('put all.espada mochila')

    voltar_ao_templo()
    run('save')
    print("[abate_peao] Teste concluído com sucesso e salvo no Templo.", flush=True)
    return True

if __name__ == '__main__':
    main()
