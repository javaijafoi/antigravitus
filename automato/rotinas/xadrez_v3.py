# -*- coding: utf-8 -*-
"""xadrez_v3.py - Rotina de caça e colheita de alta eficiência no Grande Tabuleiro de Xadrez.

Melhorias em relação à V2:
1. Lote de Venda Expresso: usa 'sell 5 armadura', 'sell 5 escudo' e 'sell 5 espada' em comando único
   (conforme comprovado em conhecimento.md §19), reduzindo round-trips e latência.
2. Diretiva Atualizada de Armaduras:
   - Coisas da Torre Negra são PERMITIDAS se NÃO forem amaldiçoadas (diretiva explícita do autor, Dia 156).
   - Triagem estrita: descarta APENAS itens com flag 'amaldiçoada' ou 'amaldiçoado'.
   - Armaduras de peão, cavaleiro, torre negra (não amaldiçoadas) e escudos são guardados na mochila e liquidados no Armeiro.
3. Varredura Tática de Fileiras:
   - Percorre a fileira clássica de peões (n, n) e expande pelas colunas adjacentes (a, b, c, d),
     maximizando a coleta de armaduras caídas no chão e o encontro de peões vivos.
4. Duplo Lightning Bolt Arcana:
   - Abre com 'lightning bolt' (70-85 dano) e encerra rapidamente com segundo cast antes que o peão fuja da sala.
   - Saque automático e imediato de moedas de ouro do corpo ('get all.moedas corpo').
5. Modularidade e Relatório de Desempenho:
   - Contabiliza detalhadamente abates, peças coletadas e ouro gerado por rodada.
"""
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'nucleo'))

from base import *

NOME = 'xadrez_v3'
DESCRICAO = 'Caçada e colheita de alta eficiência no Tabuleiro com venda em lote e triagem de maldição.'


def ir_ao_tabuleiro():
    run('wake'); run('stand')
    for _ in range(9):
        ex, t = sala()
        if set(ex) >= {'n', 'e', 's', 'w'} and 'Campo' in t:
            break
        andar('n')
    for m in ['w', 'w', 'w', 'w']:
        andar(m)
    t, _, _ = run('look')
    return 'Casa' in t or 'Tabuleiro' in t



def triagem_e_guarda_espolios():
    """Garante que nenhum item amaldiçoado permaneça no inventário e guarda espólios na mochila."""
    # Saque unificado de moedas e equipamentos em 1 comando
    run('get all corpo')

    # Triagem de segurança: descarta APENAS itens com flag amaldiçoada (Diretiva do autor Dia 156)
    # Itens da Torre Negra são permitidos se não forem amaldiçoados
    inv, _, _ = run('inventory')
    inv_lower = inv.lower()

    if 'amaldiçoada' in inv_lower or 'amaldiçoado' in inv_lower:
        print("[xadrez_v3] ALERTA: Item com flag amaldiçoada detectado! Descartando imediatamente...", flush=True)
        run('drop all.amaldiçoada')
        run('drop all.amaldiçoado')

    # Guarda espólios limpos na mochila de Pellinore para alívio de peso
    run('put all.armadura mochila')
    run('put all.escudo mochila')
    run('put all.espada mochila')


def matar_peao():
    print("[xadrez_v3] Burst 1: Lightning Bolt no peão...", flush=True)
    t, v, em_combate = run("cast 'lightning bolt' peao")
    if 'morreu' in t.lower() or 'morto' in t.lower() or 'cai sem vida' in t.lower() or 'transforma' in t.lower() or not em_combate:
        triagem_e_guarda_espolios()
        return True

    rounds = 0
    while em_combate and rounds < 5:
        rounds += 1
        time.sleep(0.4)
        if 'tenta fugir' in t.lower() or 'fugiu' in t.lower() or 'não está aqui' in t.lower() or 'em que você deseja' in t.lower():
            print("[xadrez_v3] Peão fugiu da sala. Encerrando combate nesta sala.", flush=True)
            return 'fugiu'

        print(f"[xadrez_v3] Burst 2: Lightning Bolt finalizador (round {rounds})...", flush=True)
        t, v, em_combate = run("cast 'lightning bolt' peao")
        if 'morreu' in t.lower() or 'morto' in t.lower() or 'cai sem vida' in t.lower() or 'transforma' in t.lower() or not em_combate:
            break

    triagem_e_guarda_espolios()
    return True


def varrer_tabuleiro(max_abates=4):
    """Varre as fileiras de peões do tabuleiro priorizando acúmulos no chão e abates rápidos."""
    # Rota tática cobrindo as fileiras 2 e 3 das colunas a, b, c, d
    caminho = [
        'n',        # Casa Preta (coluna a, fila 2)
        'n',        # Uma Casa Branca (coluna a, fila 3 - ponto clássico de acúmulo de peões/armaduras)
        's', 'w',   # Coluna b, fila 2
        'n',        # Coluna b, fila 3
        's', 'w',   # Coluna c, fila 2
        'n',        # Coluna c, fila 3
        's', 'w',   # Coluna d, fila 2
        'n',        # Coluna d, fila 3
        's', 'e', 'e', 'e' # Retorno para coluna a
    ]
    abates = 0

    for d in caminho:
        if abates >= max_abates:
            break
        andar(d)
        t, _, _ = run('look')

        # 1. Coleta armaduras e escudos caídos no chão com dupla checagem prévia de maldição
        if 'armadura' in t.lower():
            t_low = t.lower()
            if 'torre' in t_low or ('negra' in t_low and 'peão' not in t_low and 'peao' not in t_low):
                print("[xadrez_v3] Armadura da Torre/Negra no chão! Dupla checagem com identify antes de pegar...", flush=True)
                ident_out, _, _ = run('identify armadura')
                ident_low = ident_out.lower()
                if 'amaldiço' in ident_low or 'no-drop' in ident_low or 'nodrop' in ident_low:
                    print("[xadrez_v3] BLOQUEIO: Armadura da Torre é AMALDIÇOADA (NODROP)! Não pegar do chão.", flush=True)
                else:
                    print("[xadrez_v3] Armadura da Torre LIMPA (não amaldiçoada). Coletando...", flush=True)
                    run('get 1.armadura')
                    triagem_e_guarda_espolios()
                    abates += 1
            else:
                print("[xadrez_v3] Armadura de peão encontrada no chão! Coletando...", flush=True)
                run('get all.armadura')
                triagem_e_guarda_espolios()
                abates += 1

        if 'escudo' in t.lower():
            print("[xadrez_v3] Escudo encontrado no chão! Coletando...", flush=True)
            run('get all.escudo')
            triagem_e_guarda_espolios()
            abates += 1

        # 2. Detecta mob vivo de peão de forma precisa
        if ('aguardando ordens' in t.lower() or 'peão negro aqui' in t.lower() or 'peão branco aqui' in t.lower()) and 'lutando' not in t.lower():
            print("[xadrez_v3] Peão vivo encontrado!", flush=True)
            res = matar_peao()
            if res is True:
                abates += 1
                print(f"[xadrez_v3] Abate confirmado! Total na rodada: {abates}", flush=True)

    return abates


def vender_espolios():
    """Liquida armaduras, escudos e espadas usando venda em lote no Armeiro e Ferreiro."""
    print("[xadrez_v3] Retornando ao Templo para iniciar rota de vendas...", flush=True)
    voltar_ao_templo()
    run('stand')

    # 1. Venda no Armeiro (escudos por 200 moedas, armaduras por 150 moedas)
    run('get all.escudo mochila')
    run('get all.armadura mochila')

    # Templo -> s, s, w, s (Loja de Armaduras)
    for m in ['s', 's', 'w', 's']:
        andar(m)
    t, _, _ = run('look')
    if 'Armaduras' in t or 'armaduras' in t or 'Armeiro' in t:
        print("[xadrez_v3] No Armeiro: vendendo em lote...", flush=True)
        # Venda expressa em lote
        run('sell 5 escudo')
        run('sell 5 armadura')
        run('sell 5 armadura')
        # Limpeza residual unitária
        for _ in range(2):
            run('sell escudo')
            run('sell armadura')
    else:
        print("[xadrez_v3] AVISO: Não alcançou a Loja de Armaduras.", flush=True)

    # 2. Venda no Ferreiro (espadas por 40 moedas)
    voltar_ao_templo()
    run('stand')
    run('get all.espada mochila')

    # Templo -> s, s, e, e, n (Loja de Armas)
    for m in ['s', 's', 'e', 'e', 'n']:
        andar(m)
    t, _, _ = run('look')
    if 'Armas' in t or 'armas' in t or 'Ferreiro' in t:
        print("[xadrez_v3] No Ferreiro: vendendo espadas em lote...", flush=True)
        run('sell 5 espada')
        run('sell espada')
    else:
        print("[xadrez_v3] AVISO: Não alcançou a Loja de Armas.", flush=True)

    # Retorno seguro ao Templo
    voltar_ao_templo()
    run('save')
    return True


def executar(max_abates=4):
    run('wake'); run('stand')
    if not ir_ao_tabuleiro():
        print("[xadrez_v3] Falha ao entrar no Tabuleiro.", flush=True)
        voltar_ao_templo()
        return 0

    abates = varrer_tabuleiro(max_abates=max_abates)
    print(f"[xadrez_v3] Varrida concluída com {abates} abates/coletas.", flush=True)

    if abates > 0:
        vender_espolios()
    else:
        voltar_ao_templo()
        run('save')

    return abates


if __name__ == '__main__':
    executar()
