# -*- coding: utf-8 -*-
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'nucleo'))

from base import *

def main():
    print("Indo do Templo para o Laboratório dos Magos...", flush=True)
    run('recall')
    run('stand')
    # Templo -> praca templo -> praca comercio -> rua oeste 1 -> termino oeste -> guilda -> bar -> laboratorio
    run('d')
    run('s')
    run('w')
    run('w')
    run('s')
    run('s')
    run('e')

    t, v, c = run('look')
    print("SALA ATUAL:\n", t, flush=True)

    t_prac, _, _ = run('practice')
    print("PRACTICE NA MESTRE DOS FEITICEIROS:\n", t_prac, flush=True)

    print("\nVoltando ao Templo...", flush=True)
    run('recall')
    run('stand')
    run('save')

if __name__ == '__main__':
    main()
