# -*- coding: utf-8 -*-
"""pegar_jarro.py - Vai até A Sala do Alquimista e pega o jarro brilhante (se estiver no chão ou com o alquimista).
"""
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'nucleo'))

from base import *


def main():
    run('recall')
    run('stand')

    print('[pegar_jarro] Partindo do Templo...', flush=True)
    # Templo -> Grande Campo
    run('n')
    run('n')
    run('n')
    for _ in range(6):
        ex, t = sala()
        if set(ex) >= {'n', 'e', 's', 'w'} and 'Campo' in t:
            break
        andar('n')

    # Entra na Área dos Novatos
    andar('e')
    t, _, _ = run('look')
    if 'Novatos' not in t:
        print('[pegar_jarro] Falha ao entrar na Área dos Novatos.', flush=True)
        voltar_ao_templo()
        return False

    # Caminho até Um Outro Canto: n, e, e, s, s
    for p in ['n', 'e', 'e', 's', 's']:
        andar(p)

    run('open leste')
    andar('e')
    t, _, _ = run('look')
    print(f'[pegar_jarro] Entrou em:\n{t}', flush=True)

    # Tenta pegar jarro do chão
    r_get, _, _ = run('get jarro')
    print(f'[pegar_jarro] Resposta get jarro: {r_get}', flush=True)

    # Se ainda estiver lutando contra mob (zumbi/etc), defende-se
    if 'lutando' in t.lower() or 'luta' in r_get.lower() or 'mortal' in r_get.lower():
        matar('monstro')

    inv, _, _ = run('inventory')
    print(f'[pegar_jarro] Inventario: {inv}', flush=True)

    voltar_ao_templo()
    run('save')

    ok = 'jarro' in inv.lower()
    print(f'[pegar_jarro] Jarro obtido={ok}', flush=True)
    return ok


if __name__ == '__main__':
    ok = main()
    sys.exit(0 if ok else 1)
