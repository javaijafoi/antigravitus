# -*- coding: utf-8 -*-
raise SystemExit('PROIBIDO: este script automatiza fala/entrega/compra de missao (AGENTS #13/#14). Veja automato/acoes/_proibidos/LEIA.md')  # trava: _proibidos
"""entregar_alquimista.py - Leva a poção aquosa ao Novato Alquimista na Área dos Novatos.

Passos:
1. Templo -> Grande Campo -> Entrada dos Novatos -> Um Outro Canto -> A Sala do Alquimista.
2. Diálogo com O Novato Alquimista: ouvir fala, 'say sim' se perguntado, 'give aquosa alquimista'.
3. Receber 'o jarro brilhante' no inventário.
4. Retornar ao Templo com 'recall' e salvar.
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'nucleo'))

from base import *


def ir_ao_alquimista():
    run('recall')
    run('stand')

    print('[alquimista] Partindo do Templo...', flush=True)
    # Templo -> Grande Campo
    run('n')
    run('n')
    run('n')
    for _ in range(6):
        ex, t = sala()
        if set(ex) >= {'n', 'e', 's', 'w'} and 'Campo' in t:
            break
        andar('n')

    ex, t = sala()
    print(f'[alquimista] Em: {t.split(chr(10))[0]} (saidas: {ex})', flush=True)

    # Entra na Área dos Novatos
    andar('e')
    t, _, _ = run('look')
    print(f'[alquimista] {t.split(chr(10))[0]}', flush=True)
    if 'Novatos' not in t:
        print('[alquimista] Falha ao entrar na Área dos Novatos.', flush=True)
        voltar_ao_templo()
        return False

    # Caminho pelos corredores até A Sala do Alquimista:
    # n (Começo da Passagem), e (Corredor Sujo), e (Cruzamento), s (Mais Corredor), s (Um Outro Canto)
    passos = ['n', 'e', 'e', 's', 's']
    for p in passos:
        andar(p)
        t, _, _ = run('look')
        print(f'[alquimista] -> {t.split(chr(10))[0]}', flush=True)

    t, _, _ = run('look')
    if 'Outro Canto' not in t:
        print('[alquimista] Nao chegou a Um Outro Canto.', flush=True)
        voltar_ao_templo()
        return False

    # Abre a porta leste e entra
    run('open leste')
    andar('e')
    t, _, _ = run('look')
    print(f'[alquimista] Entrou em: {t.split(chr(10))[0]}', flush=True)
    if 'Alquimista' not in t:
        print('[alquimista] Nao entrou na Sala do Alquimista.', flush=True)
        voltar_ao_templo()
        return False

    return True


def verificar_preparacao_entrega():
    print('[alquimista] Verificando pré-condições da entrega...', flush=True)
    t, _, _ = run('score tudo')
    if 'Gargamel' not in t:
        print('[alquimista] ERRO: Uma Lição em Gargamel NÃO está em andamento no score tudo! Abortando entrega.', flush=True)
        return False
    
    inv, _, _ = run('inventory')
    if 'aquosa' not in inv.lower() and 'poção' not in inv.lower():
        print('[alquimista] Tentando tirar poção da mochila...', flush=True)
        run('get aquosa mochila')
        inv, _, _ = run('inventory')
        if 'aquosa' not in inv.lower():
            print('[alquimista] ERRO: Poção aquosa não encontrada no inventário! Abortando entrega.', flush=True)
            return False

    print('[alquimista] Pré-condições OK: Uma Lição em Gargamel ativa e poção aquosa pronta.', flush=True)
    return True


def dialogar_e_entregar():
    if not verificar_preparacao_entrega():
        voltar_ao_templo()
        return False

    print('[alquimista] Analisando ambiente do Alquimista...', flush=True)
    time.sleep(2)
    r1, _, _ = run('look')
    print(f'[alquimista] Olhar: {r1}', flush=True)

    # 1. Se houver mob agressivo na sala (ex: zumbi), neutraliza antes de qualquer diálogo
    if 'lutando' in r1.lower() or 'zumbi' in r1.lower() or 'mico' in r1.lower():
        print('[alquimista] Detectado mob agressivo na sala; eliminando ameaça antes do diálogo...', flush=True)
        matar('monstro')
        time.sleep(1)
        r1, _, _ = run('look')

    # 2. Diálogo canônico obrigatório (§41.1):
    # say Grebolius -> Alquimista reconhece -> say sim -> Alquimista pede a poção aquosa
    print('[alquimista] Iniciando diálogo: say Grebolius...', flush=True)
    r_nome, _, _ = run('say Grebolius')
    print(f'[alquimista] Say Grebolius: {r_nome}', flush=True)
    time.sleep(2)

    r_talk, _, _ = run('look')
    print(f'[alquimista] Resposta Alquimista: {r_talk}', flush=True)

    print('[alquimista] Confirmando pedido do jarro: say sim...', flush=True)
    r_sim, _, _ = run('say sim')
    print(f'[alquimista] Say sim: {r_sim}', flush=True)
    time.sleep(2)

    # 3. Entregar a poção aquosa somente após o diálogo de troca estar ativo
    print('[alquimista] Entregando a poção aquosa...', flush=True)
    r_give, _, _ = run('give aquosa alquimista')
    print(f'[alquimista] Give aquosa: {r_give}', flush=True)

    # Aguardar 2s e conferir reações/diálogos
    time.sleep(2)
    r_wait, _, _ = run('look')
    print(f'[alquimista] Apos entrega: {r_wait}', flush=True)

    inv, _, _ = run('inventory')
    print(f'[alquimista] Inventario: {inv}', flush=True)

    voltar_ao_templo()
    run('save')

    ok = 'jarro' in inv.lower() or 'brilhante' in inv.lower() or 'jarro brilhante' in r_give.lower() or 'jarro brilhante' in r_wait.lower()
    print(f'[alquimista] Sucesso jarro={ok}', flush=True)
    return ok


def main():
    if not verificar_preparacao_entrega():
        return False
    if not ir_ao_alquimista():
        return False
    return dialogar_e_entregar()


if __name__ == '__main__':
    ok = main()
    sys.exit(0 if ok else 1)
