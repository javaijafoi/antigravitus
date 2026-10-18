# -*- coding: utf-8 -*-
"""explorar_tabuleiro.py - Mapeia as peças e mobs presentes no Grande Tabuleiro.
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'nucleo'))

from base import *

def main():
    run('wake'); run('stand')
    for _ in range(4):
        andar('n')
    for _ in range(3):
        andar('w')
    
    # Agora estamos na entrada do Tabuleiro
    andar('w') # Casa Branca
    
    # Faz uma varredura pelas casas
    grid = ['w', 'n', 'e', 'n', 'w', 's', 'w', 'n', 'w', 's', 's', 'e', 's', 'w']
    mobs_encontrados = []
    
    for direcao in grid:
        andar(direcao)
        t, _, _ = run('look')
        linhas = t.splitlines()
        sala_nome = linhas[0] if linhas else '?'
        for l in linhas[1:]:
            if any(k in l.lower() for k in ['peão', 'peao', 'torre', 'cavaleiro', 'bispo', 'rainha', 'rei', 'armadura']):
                mobs_encontrados.append((sala_nome, l.strip()))
                print(f"[xadrez] {sala_nome}: {l.strip()}", flush=True)

    print(f"\n[xadrez] Total de alvos/itens detectados: {len(mobs_encontrados)}", flush=True)
    voltar_ao_templo()
    run('save')

if __name__ == '__main__':
    main()
