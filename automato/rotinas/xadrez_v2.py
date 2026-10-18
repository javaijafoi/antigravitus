# -*- coding: utf-8 -*-
"""xadrez_v2.py - Rotina ativa e segura de caça a peões no Grande Tabuleiro de Xadrez.

Melhorias em relação à V1 (suspensa):
1. Combate ativo: não espera itens no chão; abate peões negros/brancos com burst de magia (lightning + burning).
2. Consider preventivo: nunca ataca Cavaleiro, Torre, Rei ou Rainha.
3. Tratamento de pânico/fuga: se o peão fugir da sala, não insiste em magias nulas.
4. Triagem estrita de maldição: descarta qualquer Armadura da Torre Negra se coletada por engano.
5. Mochila de Pellinore: guarda armaduras, escudos e espadas na mochila para alívio de peso.
6. Rota comercial completa: vende armaduras e escudos no Armeiro, e espadas no Ferreiro.
"""
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'nucleo'))

from base import *

NOME = 'xadrez_v2'
DESCRICAO = 'Caçada seletiva a peões no Tabuleiro com venda de armaduras, escudos e espadas.'


def ir_ao_tabuleiro():
    run('wake'); run('stand')
    for _ in range(4):
        andar('n')
    for _ in range(3):
        andar('w')
    andar('w') # Casa Branca de entrada
    t, _, _ = run('look')
    return 'Casa' in t or 'Tabuleiro' in t


def matar_peao():
    r_cons, _, _ = run('consider peao')
    if 'Muito fácil' not in r_cons and 'Fácil' not in r_cons and 'perda de tempo' not in r_cons:
        print(f"[xadrez_v2] Consider desfavorável ou alvo incorreto: {r_cons.strip()}", flush=True)
        return False

    print("[xadrez_v2] Abrindo com Lightning Bolt...", flush=True)
    t, v, em_combate = run("cast 'lightning bolt' peao")
    if 'morreu' in t.lower() or 'morto' in t.lower() or 'cai sem vida' in t.lower() or 'transforma' in t.lower() or not em_combate:
        run('get all corpo')
        run('put all.armadura mochila')
        run('put all.escudo mochila')
        run('put all.espada mochila')
        return True

    rounds = 0
    while em_combate and rounds < 6:
        rounds += 1
        time.sleep(0.5)
        if 'tenta fugir' in t.lower() or 'fugiu' in t.lower() or 'não está aqui' in t.lower() or 'em que você deseja' in t.lower():
            print("[xadrez_v2] Peão fugiu da sala. Encerrando combate nesta sala.", flush=True)
            return 'fugiu'
            
        t, v, em_combate = run("cast 'lightning bolt' peao")
        if 'morreu' in t.lower() or 'morto' in t.lower() or 'cai sem vida' in t.lower() or 'transforma' in t.lower() or not em_combate:
            break

    # Loot do corpo
    run('get all corpo')
    
    # Triagem de segurança: descarta APENAS itens com flag amaldiçoada (Diretiva do autor Dia 156)
    # Itens da Torre Negra são permitidos se não forem amaldiçoados
    inv, _, _ = run('inventory')
    if 'amaldiçoada' in inv.lower() or 'amaldiçoado' in inv.lower():
        print("[xadrez_v2] ALERTA: Item com flag amaldiçoada detectado! Descartando imediatamente...", flush=True)
        run('drop all.amaldiçoada')
        run('drop all.amaldiçoado')

    # Guarda espólios na mochila de Pellinore para aliviar carga
    run('put all.armadura mochila')
    run('put all.escudo mochila')
    run('put all.espada mochila')
    return True


def varrer_tabuleiro(max_abates=4):
    caminho = ['w', 'n', 'e', 'n', 'w', 's', 'w', 'n', 'w', 's', 's', 'e', 's', 'w']
    abates = 0

    for d in caminho:
        if abates >= max_abates:
            break
        andar(d)
        t, _, _ = run('look')
        # 1. Coleta armaduras de peão caídas no chão (venda de 150 moedas cada no Armeiro)
        if 'armadura de um peão' in t.lower() or 'armadura do peão' in t.lower():
            print("[xadrez_v2] Armadura de peão encontrada no chão! Coletando...", flush=True)
            run('get all.armadura')
            run('put all.armadura mochila')
            abates += 1

        # 2. Detecta mob vivo de peão de forma precisa
        if ('aguardando ordens' in t.lower() or 'peão negro aqui' in t.lower() or 'peão branco aqui' in t.lower()) and 'lutando' not in t.lower():
            print(f"[xadrez_v2] Peão vivo encontrado!", flush=True)
            res = matar_peao()
            if res is True:
                abates += 1
                print(f"[xadrez_v2] Abate confirmado! Total na rodada: {abates}", flush=True)

    return abates


def vender_espolios():
    print("[xadrez_v2] Retornando para venda de espólios...", flush=True)
    voltar_ao_templo()
    run('stand')

    # Tira itens da mochila para a mão antes de vender
    run('get all.escudo mochila')
    run('get all.armadura mochila')

    # Vai ao Armeiro: Templo -> s, s, w, s
    for m in ['s', 's', 'w', 's']:
        andar(m)
    t, _, _ = run('look')
    if 'Armaduras' in t or 'armaduras' in t:
        print("[xadrez_v2] No Armeiro: vendendo escudos e armaduras...", flush=True)
        for _ in range(6):
            r, _, _ = run('sell escudo')
            if 'não tem' in r.lower() or 'nao tem' in r.lower() or 'caro demais' in r.lower() or 'não parece' in r.lower() or 'nao parece' in r.lower():
                break
        for _ in range(6):
            r, _, _ = run('sell armadura')
            if 'não tem' in r.lower() or 'nao tem' in r.lower() or 'caro demais' in r.lower() or 'não parece' in r.lower() or 'nao parece' in r.lower():
                break
    else:
        print("[xadrez_v2] Falha ao chegar no Armeiro.", flush=True)

    # Vai à Ferraria (vender espadas)
    # Da Loja de Armaduras: n, e (Praça) -> n, n (Rua Leste) -> e (Loja de Armas)
    run('recall'); run('stand')
    for m in ['s', 's', 'e', 'e', 'n']:
        andar(m)
    t, _, _ = run('look')
    if 'Armas' in t or 'armas' in t:
        run('get all.espada mochila')
        print("[xadrez_v2] No Ferreiro: vendendo espadas...", flush=True)
        for _ in range(6):
            r, _, _ = run('sell espada')
            if 'não tem' in r.lower() or 'nao tem' in r.lower() or 'caro demais' in r.lower() or 'não parece' in r.lower() or 'nao parece' in r.lower():
                break

    voltar_ao_templo()
    run('save')
    return True


def executar(max_abates=4):
    run('wake'); run('stand')
    if not ir_ao_tabuleiro():
        print("[xadrez_v2] Falha ao entrar no Tabuleiro.", flush=True)
        voltar_ao_templo()
        return 0

    abates = varrer_tabuleiro(max_abates=max_abates)
    print(f"[xadrez_v2] Varrida concluída com {abates} abates.", flush=True)
    
    if abates > 0:
        vender_espolios()
    else:
        voltar_ao_templo()
        run('save')

    return abates


if __name__ == '__main__':
    executar()
