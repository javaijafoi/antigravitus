# -*- coding: utf-8 -*-
"""testar_abate_peao_direto.py - Vai direto à sala com o peão negro e abate.
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
    
    # Caminho que achou o peão no explorador:
    caminho = ['w', 'n', 'e', 'n', 'w']
    for d in caminho:
        andar(d)
        
    t, _, _ = run('look')
    print(f"[abate_peao] Sala:\n{t.strip()}", flush=True)

    if 'peão' not in t.lower() and 'peao' not in t.lower():
        print("[abate_peao] Peão não está nesta sala, tentando mais um passo oeste...", flush=True)
        andar('w')
        t, _, _ = run('look')
        print(f"[abate_peao] Sala +1:\n{t.strip()}", flush=True)

    r_cons, _, _ = run('consider peao')
    print(f"[abate_peao] Consider: {r_cons.strip()}", flush=True)

    print("[abate_peao] Cast lightning bolt...", flush=True)
    t, v, em_combate = run("cast 'lightning bolt' peao")
    print(f"[abate_peao] Turno 1: {t.strip()}", flush=True)

    for i in range(5):
        time.sleep(1)
        t, v, em_combate = run("cast 'magic missile' peao")
        print(f"[abate_peao] Turno {i+2}: {t.strip()}", flush=True)
        if 'morreu' in t.lower() or 'morto' in t.lower() or 'cai sem vida' in t.lower() or 'transforma' in t.lower():
            break

    print("[abate_peao] Pegando loot...", flush=True)
    r_get, _, _ = run('get all corpo')
    print(f"[abate_peao] Loot: {r_get.strip()}", flush=True)

    inv, _, _ = run('inventory')
    print(f"[abate_peao] Inventário:\n{inv.strip()}", flush=True)

    # Guarda na mochila
    run('put all.armadura mochila')
    run('put all.escudo mochila')
    run('put all.espada mochila')

    voltar_ao_templo()
    run('save')
    print("[abate_peao] Concluído e salvo no Templo.", flush=True)

if __name__ == '__main__':
    main()
