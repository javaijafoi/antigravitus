# -*- coding: utf-8 -*-
"""falar_minerador.py - Vai até o smurf minerador na Vila dos Smurfs e inicia 'Uma Lição em Gargamel'."""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'nucleo'))

from base import *

def main():
    print("[minerador] Partindo do Templo para O Fim Do Túnel...", flush=True)
    run('recall')
    run('stand')

    # Templo (d, s), Midgaard leste (e, e, e), Estrada do Rei (e, e, e, e, e), Smurf (n, n, n, n, d, e)
    passos = ['d', 's', 'e', 'e', 'e', 'e', 'e', 'e', 'e', 'e', 'n', 'n', 'n', 'n', 'd', 'e']
    for p in passos:
        r, v, c = run(p)
        if c:
            print(f"[minerador] Combate inesperado em {p}!", flush=True)
            run('recall')
            run('stand')
            return False

    t, _, _ = run('look')
    print("[minerador] Sala atual:\n", t, flush=True)

    if 'Túnel' not in t and 'Tunel' not in t and 'minerador' not in t:
        print("[minerador] Não chegou na sala do minerador!", flush=True)
        run('recall')
        run('stand')
        return False

    print("[minerador] Falando com o minerador...", flush=True)
    r1, _, _ = run('say Grebolius')
    print("[minerador] Say Grebolius:\n", r1, flush=True)

    r2, _, _ = run('say sim')
    print("[minerador] Say sim:\n", r2, flush=True)

    r3, _, _ = run('look')
    print("[minerador] Look pós-fala:\n", r3, flush=True)

    r_score, _, _ = run('score tudo')
    print("[minerador] Score tudo:\n", r_score, flush=True)

    print("[minerador] Retornando ao Templo...", flush=True)
    run('recall')
    run('stand')
    run('save')
    return True

if __name__ == '__main__':
    main()
