# -*- coding: utf-8 -*-
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'nucleo'))

from base import *

def main():
    run('recall')
    run('stand')
    # Templo -> Portao Leste
    for p in ['d', 's', 'e', 'e', 'e']:
        run(p)

    for i in range(1, 15):
        run('e')
        e_txt, _, _ = run('exits')
        l_txt, _, _ = run('look')
        lines = [x.strip() for x in l_txt.splitlines() if x.strip()]
        title = lines[0] if lines else '??'
        ex = [x.strip() for x in e_txt.splitlines() if x.strip()]
        print(f"Passo {i} E: {title} | Saidas: {ex}", flush=True)
        if any('smurf' in x.lower() for x in ex) or 'smurf' in l_txt.lower():
            print(f"--> ENCONTRADO INDICIO SMURF EM PASSO {i}!", flush=True)
            break

    run('recall')
    run('stand')
    run('save')

if __name__ == '__main__':
    main()
