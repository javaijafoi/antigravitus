# -*- coding: utf-8 -*-
"""trabalhar.py - despachante de ROTINAS.

Uso:
    python scripts/local/trabalhar.py --rotina milharal
    python scripts/local/trabalhar.py --listar

Cada rotina sabe partir do Templo, trabalhar e voltar. Elas sao protegidas:
  - pela guarda de repeticao (dentro de base.py);
  - pelo vigia.py, que o turno.py consulta de minuto em minuto.
"""
import argparse
import sys
from pathlib import Path

LOCAL = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(LOCAL / 'nucleo'))
sys.path.insert(0, str(LOCAL / 'rotinas'))


def rotinas_disponiveis():
    return sorted(p.stem for p in (LOCAL / 'rotinas').glob('*.py')
                  if p.stem not in ('base', '__init__'))


def carregar(nome):
    return __import__(nome)


def main():
    ap = argparse.ArgumentParser(description='Despachante de rotinas do heroi.')
    ap.add_argument('--rotina', help='nome da rotina a executar')
    ap.add_argument('--listar', action='store_true', help='lista as rotinas disponiveis')
    args = ap.parse_args()
    if args.listar or not args.rotina:
        for nome in rotinas_disponiveis():
            try:
                mod = carregar(nome)
                print(f'  {nome:10s} {getattr(mod, chr(68)+chr(69)+chr(83)+chr(67)+chr(82)+chr(73)+chr(67)+chr(65)+chr(79), chr(63))}')
            except Exception as e:
                print(f'  {nome:10s} (nao carregou: {e})')
        return 0
    mod = carregar(args.rotina)
    print(f'[trabalhar] rotina={args.rotina}', flush=True)
    ok = mod.executar()
    print(f'[trabalhar] rotina={args.rotina} resultado={ok}', flush=True)
    return 0 if ok else 1


if __name__ == '__main__':
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    sys.exit(main())
