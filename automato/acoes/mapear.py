# -*- coding: utf-8 -*-
"""mapear.py - anda uma sequencia de passos imprimindo CADA sala.

E a ferramenta que a doutrina exige: antes de automatizar um trajeto, mapeie a mao.

Uso:
    python automato/acoes/mapear.py "n,n,e,e,s"            # a partir de onde esta
    python automato/acoes/mapear.py --floresta "n,n,e,e,s" # indo antes ate a floresta
"""
import argparse
import sys
from pathlib import Path

AQUI = Path(__file__).resolve()
sys.path.insert(0, str(AQUI.parents[1] / 'nucleo'))
sys.path.insert(0, str(AQUI.parents[1] / 'rotinas'))
import random        # noqa: E402
import base          # noqa: E402
import milharal      # noqa: E402

NOMES = {'n': 'norte', 's': 'sul', 'e': 'leste', 'w': 'oeste', 'd': 'baixo', 'u': 'cima'}


def relatar(rotulo):
    ex, t = base.sala()
    nome = next((l.strip() for l in t.split(chr(10)) if l.strip()), '?')
    saidas = ' '.join(f"{k}:{v}" for k, v in sorted(ex.items()))
    print(f"{rotulo:>10} | {nome[:38]:38s} | {saidas[:110]}", flush=True)
    return nome


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('passos', nargs='?', default='', help='sequencia separada por virgula')
    ap.add_argument('--floresta', action='store_true', help='ir antes ate a Entrada da Floresta')
    ap.add_argument('--buscar', help='andar pelo bosque ate uma saida/sala conter esta marca')
    args = ap.parse_args()
    if args.floresta:
        print('viajando ate a floresta...', flush=True)
        if not milharal.ir_ate_a_floresta():
            print('nao cheguei a floresta')
            return 2
    if args.buscar:
        marca = args.buscar.lower()
        caminho = []
        for passo in range(200):
            ex, t = base.sala()
            nome = next((l.strip() for l in t.split(chr(10)) if l.strip()), '?')
            if marca in t.lower() or any(marca in v.lower() for v in ex.values()):
                print(f"ACHADO na sala '{nome}' (passo {passo})", flush=True)
                relatar(nome)
                print('CAMINHO:', ','.join(caminho), flush=True)
                return 0
            bosque = [d for d, v in ex.items() if 'Bosque' in v]
            trans = [d for d, v in ex.items() if ('Densa' in v or 'Floresta' in v or 'Trilha' in v)]
            d = random.choice(bosque or trans or list(ex) or ['n'])
            caminho.append(d)
            base.andar(d)
        print('nao achei a marca')
        return 1
    relatar('inicio')
    for passo in [x.strip() for x in args.passos.split(',') if x.strip()]:
        r, _, _ = base.run(passo)
        if 'não pode ir' in r:
            print(f"{passo:>10} | (bloqueado)")
            continue
        relatar(NOMES.get(passo, passo))
    return 0


if __name__ == '__main__':
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    sys.exit(main())
