# -*- coding: utf-8 -*-
raise SystemExit('PROIBIDO: este script automatiza fala/entrega/compra de missao (AGENTS #13/#14). Veja automato/acoes/_proibidos/LEIA.md')  # trava: _proibidos
"""comprar_pocao.py - Viaja até Jareth (As Misturas de Clariss) e compra 'uma poção aquosa'.

Preço: 9.750 moedas de ouro.
Comando obrigatório: 'buy aquosa' (nunca 'buy pocao', que compra a poção amarela errada).
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'nucleo'))
sys.path.insert(0, str(ROOT / 'rotinas'))

from base import *
from milharal import ir_ate_a_floresta


def comprar_pocao_aquosa():
    run('wake')
    run('stand')
    run('recall')
    run('stand')

    print('[comprar_pocao] Indo ate A Entrada da Floresta...', flush=True)
    if not ir_ate_a_floresta():
        print('[comprar_pocao] Falha ao chegar na floresta.', flush=True)
        voltar_ao_templo()
        return False

    print('[comprar_pocao] Na Entrada da Floresta. Entrando em Jareth pelo Portão Leste...', flush=True)
    # De A Entrada da Floresta para oeste chega em O Portão Leste
    andar('w')
    t, _, _ = run('look')
    print(f'[comprar_pocao] Sala inicial: {t.split(chr(10))[0]}', flush=True)

    # Anda para oeste pela Avenida Floris até encontrar 'As Misturas de Clariss' ao sul
    achou = False
    for i in range(18):
        t, _, _ = run('look')
        linha1 = t.split('\n')[0].strip()
        e_txt, _, _ = run('exits')
        print(f'[comprar_pocao] Passo {i}: {linha1}', flush=True)
        if 'Clariss' in t or 'Clariss' in e_txt:
            achou = True
            break
        r, _, _ = run('w')
        if 'não pode ir' in r.lower():
            print('[comprar_pocao] Bloqueio a oeste.', flush=True)
            break

    if not achou:
        print('[comprar_pocao] Nao encontrou As Misturas de Clariss.', flush=True)
        voltar_ao_templo()
        return False

    # Entra na loja ao sul
    andar('s')

    t, _, _ = run('look')
    print(f'[comprar_pocao] Entrou em: {t.split(chr(10))[0]}', flush=True)
    if 'Clariss' not in t:
        print('[comprar_pocao] Erro: nao esta na loja da Clariss.', flush=True)
        voltar_ao_templo()
        return False

    # Compra a poção aquosa
    res, _, _ = run('buy aquosa')
    print(f'[comprar_pocao] Resposta buy aquosa: {res}', flush=True)

    # Confere inventário
    inv, _, _ = run('inventory')
    print(f'[comprar_pocao] Inventario: {inv}', flush=True)

    voltar_ao_templo()
    run('save')

    ok = 'aquosa' in inv.lower() or 'poção aquosa' in res.lower()
    print(f'[comprar_pocao] Sucesso={ok}', flush=True)
    return ok


if __name__ == '__main__':
    ok = comprar_pocao_aquosa()
    sys.exit(0 if ok else 1)
