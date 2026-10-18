# -*- coding: utf-8 -*-
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'nucleo'))

from base import *

def main():
    print("Enviando 'say sim'...", flush=True)
    t, v, c = run('say sim')
    print("RESPOSTA SAY SIM:\n", t, flush=True)

    print("\nEnviando 'give aquosa alquimista'...", flush=True)
    t, v, c = run('give aquosa alquimista')
    print("RESPOSTA GIVE AQUOSA:\n", t, flush=True)

    print("\nVerificando inventário...", flush=True)
    t, v, c = run('inventory')
    print("INVENTARIO:\n", t, flush=True)

    print("\nOlhando sala...", flush=True)
    t, v, c = run('look')
    print("LOOK:\n", t, flush=True)

    print("\nVoltando ao Templo...", flush=True)
    run('recall')
    run('stand')
    run('save')
    t, v, c = run('look')
    print("NO TEMPLO:\n", t, flush=True)

if __name__ == '__main__':
    main()
