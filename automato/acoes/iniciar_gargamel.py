# -*- coding: utf-8 -*-
"""iniciar_gargamel.py - Espera o minerador falar, responde 'say sim', confirma inicio da quest."""
import time
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'nucleo'))

from base import *

def main():
    print("[gargamel] Partindo para O Fim Do Túnel...", flush=True)
    run('recall')
    run('stand')

    passos = ['d', 's', 'e', 'e', 'e', 'e', 'e', 'e', 'e', 'e', 'n', 'n', 'n', 'n', 'd', 'e']
    for p in passos:
        r, v, c = run(p)

    t, _, _ = run('look')
    print("[gargamel] Na sala:\n", t, flush=True)

    # Aguarda o mob falar (até 15 segundos)
    print("[gargamel] Aguardando fala do minerador...", flush=True)
    for _ in range(5):
        time.sleep(3)
        t, _, _ = run('look')
        print(f"[gargamel] Look: {t[:200]}...", flush=True)
        if 'ajudar' in t or 'lampião' in t or 'lampiao' in t or 'óleo' in t:
            print("[gargamel] Minerador falou!", flush=True)
            break

    # Responde sim
    print("[gargamel] Enviando 'say sim'...", flush=True)
    r_sim, _, _ = run('say sim')
    print("[gargamel] Resposta say sim:\n", r_sim, flush=True)

    time.sleep(3)
    r_look, _, _ = run('look')
    print("[gargamel] Look final:\n", r_look, flush=True)

    r_score, _, _ = run('score tudo')
    print("[gargamel] Score tudo:\n", r_score, flush=True)

    run('recall')
    run('stand')
    run('save')

if __name__ == '__main__':
    main()
