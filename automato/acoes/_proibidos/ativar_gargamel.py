# -*- coding: utf-8 -*-
raise SystemExit('PROIBIDO: este script automatiza fala/entrega/compra de missao (AGENTS #13/#14). Veja automato/acoes/_proibidos/LEIA.md')  # trava: _proibidos
"""ativar_gargamel.py - Vai até O Fim Do Túnel na Vila dos Smurfs e ativa 'Uma Lição em Gargamel'.

Rota:
Templo -> s, s -> 8x e -> n (Entrada Para a Vila dos Smurfs) -> 3x n (O Poço Smurf) -> d -> e (O Fim Do Túnel)
NPC: o smurf minerador
Comando de ativação: 'say sim'
Retorno: 'recall', 'stand', 'save'
"""
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'nucleo'))

from base import *


def ir_ao_fim_do_tunel():
    run('recall')
    run('stand')

    print('[ativar_gargamel] Partindo do Templo...', flush=True)
    # Templo -> Praça do Comércio
    run('s')
    run('s')

    # Praça do Comércio -> Estrada do Rei até Entrada da Vila dos Smurfs
    # 8x leste
    for i in range(8):
        andar('e')
        t, _, _ = run('look')
        linha1 = t.split(chr(10))[0].strip()
        print(f'[ativar_gargamel] Leste passo {i+1}: {linha1}', flush=True)

    # Entra na Vila dos Smurfs (norte)
    andar('n')
    t, _, _ = run('look')
    print(f'[ativar_gargamel] Entrada: {t.split(chr(10))[0]}', flush=True)
    if 'Vila dos Smurfs' not in t:
        print('[ativar_gargamel] Falha ao entrar na Vila dos Smurfs.', flush=True)
        voltar_ao_templo()
        return False

    # Caminho pela Vila até o Poço Smurf (3x norte)
    for i in range(3):
        andar('n')
        t, _, _ = run('look')
        print(f'[ativar_gargamel] Norte passo {i+1}: {t.split(chr(10))[0]}', flush=True)

    t, _, _ = run('look')
    if 'Poço' not in t:
        print('[ativar_gargamel] Nao encontrou O Poço Smurf.', flush=True)
        voltar_ao_templo()
        return False

    # Desce no poço e vai a leste para O Fim Do Túnel
    andar('d')
    t, _, _ = run('look')
    print(f'[ativar_gargamel] Desceu: {t.split(chr(10))[0]}', flush=True)

    andar('e')
    t, _, _ = run('look')
    print(f'[ativar_gargamel] Fim do Túnel: {t.split(chr(10))[0]}', flush=True)

    if 'Fim Do Túnel' not in t and 'minerador' not in t.lower():
        print('[ativar_gargamel] Nao encontrou o Fim Do Túnel ou o minerador.', flush=True)
        voltar_ao_templo()
        return False

    return True


def dialogar_com_minerador():
    print('[ativar_gargamel] Dialogando com o Smurf Minerador...', flush=True)
    r1, _, _ = run('look')
    print(f'[ativar_gargamel] Ambiente: {r1}', flush=True)

    # Sequência canônica do conhecimento.md §41.1: say sim -> say Grebolius -> say sim
    time.sleep(2)
    print('[ativar_gargamel] 1. say sim...', flush=True)
    r_sim1, _, _ = run('say sim')
    print(f'[ativar_gargamel] R1: {r_sim1}', flush=True)
    time.sleep(2)

    print('[ativar_gargamel] 2. say Grebolius...', flush=True)
    r_nome, _, _ = run('say Grebolius')
    print(f'[ativar_gargamel] R2: {r_nome}', flush=True)
    time.sleep(2)

    print('[ativar_gargamel] 3. say sim...', flush=True)
    r_sim2, _, _ = run('say sim')
    print(f'[ativar_gargamel] R3: {r_sim2}', flush=True)
    time.sleep(3)

    r_look, _, _ = run('look')
    print(f'[ativar_gargamel] Olhar apos dialogo: {r_look}', flush=True)

    # Confere score tudo
    t_score, _, _ = run('score tudo')
    print(f'[ativar_gargamel] Score tudo:\n{t_score}', flush=True)

    voltar_ao_templo()
    run('save')

    ok = 'Uma Lição em Gargamel' in t_score or 'minerador' in r_look.lower()
    print(f'[ativar_gargamel] Ativacao confirmada={ok}', flush=True)
    return ok


def main():
    if not ir_ao_fim_do_tunel():
        return False
    return dialogar_com_minerador()


if __name__ == '__main__':
    ok = main()
    sys.exit(0 if ok else 1)
