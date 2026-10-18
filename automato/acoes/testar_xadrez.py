# -*- coding: utf-8 -*-
"""testar_xadrez.py - Teste seguro de reconhecimento do Tabuleiro de Xadrez.
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'nucleo'))

from base import *

def main():
    print("[xadrez_test] Saindo do Templo rumo ao Tabuleiro...", flush=True)
    run('wake')
    run('stand')
    
    # Rota Templo -> Grande Campo -> Tabuleiro
    # 4 norte
    for _ in range(4):
        andar('n')
    
    # 3 oeste
    for _ in range(3):
        andar('w')
        
    t, _, _ = run('look')
    print(f"[xadrez_test] Chegou em:\n{t}", flush=True)
    
    # Entra na Casa Branca
    andar('w')
    t, _, _ = run('look')
    print(f"[xadrez_test] Casa Branca:\n{t}", flush=True)
    
    # Considera mobs na sala ou arredores
    r_cons, _, _ = run('consider peao')
    print(f"[xadrez_test] Consider peao: {r_cons}", flush=True)
    
    r_cons_cav, _, _ = run('consider cavaleiro')
    print(f"[xadrez_test] Consider cavaleiro: {r_cons_cav}", flush=True)

    # Retorna ao templo
    voltar_ao_templo()
    run('save')
    print("[xadrez_test] Retornou ao Templo com segurança.", flush=True)

if __name__ == '__main__':
    main()
