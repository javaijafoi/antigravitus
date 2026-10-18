# -*- coding: utf-8 -*-
"""atingir_meta_pocao.py - Roda rodadas focadas no Milharal V2 até atingir 9.750 moedas."""
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'nucleo'))
sys.path.insert(0, str(ROOT / 'rotinas'))
sys.path.insert(0, str(ROOT / 'camadas'))

from base import *
import milharal_v2
import xadrez_v3
import guarda_cota


def ouro_atual():
    t, _, _ = run('score tudo')
    for line in t.splitlines():
        if 'Carregando:' in line:
            parts = line.split('-')
            if len(parts) >= 2 and 'Total:' in parts[1]:
                tot = parts[1].replace('Total:', '').strip().replace('.', '').replace(',', '')
                if tot.isdigit():
                    return int(tot)
            for part in line.split():
                clean = part.replace('.', '').replace(',', '')
                if clean.isdigit():
                    return int(clean)
    return 0


def alimentar_e_hidratar():
    t, _, _ = run('score tudo')
    if 'fome' in t.lower():
        print("[meta_pocao] Alimentando com pão da mochila...", flush=True)
        run('get pao mochila')
        run('eat pao')
    if 'sede' in t.lower():
        print("[meta_pocao] Bebendo do cantil...", flush=True)
        r, _, _ = run('drink cantil')
        if 'vazio' in r.lower():
            run('d')
            run('fill cantil fonte')
            run('drink cantil')
            run('u')


def descansar(min_mana=360, max_espera=120):
    print("[meta_pocao] Descansando no Templo para recarga de mana...", flush=True)
    run('recall')
    run('sleep')
    inicio = time.time()
    while time.time() - inicio < max_espera:
        time.sleep(4)
        t, v, _ = run('score')
        mn = v.get('mana')
        if mn is None:
            for token in t.split():
                if token.endswith('mn'):
                    try:
                        mn = int(token[:-2])
                        break
                    except ValueError:
                        pass
        print(f"[meta_pocao] Mana atual: {mn}/395", flush=True)
        if mn and mn >= min_mana:
            break
    run('wake')
    run('stand')


def main(rodada_inicial=3):
    meta = 9750
    run('recall'); run('stand')
    o = ouro_atual()
    print(f"[meta_pocao] Saldo inicial: {o} moedas. Meta: {meta} moedas (Faltam {meta - o}).", flush=True)
    rodada = rodada_inicial

    while o < meta:
        if not guarda_cota.checar_guarda():
            print("[meta_pocao] Parada preventiva por cota de IA baixa.", flush=True)
            break

        print(f"\n==========================================", flush=True)
        print(f"[meta_pocao] === RODADA {rodada} (Saldo: {o}/{meta} moedas) ===", flush=True)
        print(f"==========================================", flush=True)

        alimentar_e_hidratar()
        descansar()
        try:
            milharal_v2.executar()
        except Exception as ex:
            print(f"[meta_pocao] Exceção na rodada: {ex}; recuperando no Templo...", flush=True)
            run('recall'); run('stand')

        run('recall')
        run('stand')
        run('save')
        o = ouro_atual()
        print(f"[meta_pocao] Pós-Rodada {rodada}: Ouro = {o} moedas (Faltam {max(0, meta - o)}).", flush=True)

        # A cada 3 ciclos, passa no Xadrez para colheita/venda de espólios extras
        if rodada % 3 == 0:
            print(f"\n[meta_pocao] === CICLO {rodada}: PASSANDO NO TABULEIRO DE XADREZ ===", flush=True)
            try:
                descansar(min_mana=300)
                abates_xadrez = xadrez_v3.executar(max_abates=4)
                print(f"[meta_pocao] Xadrez concluído: {abates_xadrez} abates/coletas.", flush=True)
            except Exception as ex:
                print(f"[meta_pocao] Exceção no Xadrez: {ex}; recuperando no Templo...", flush=True)
                run('recall'); run('stand')
            run('recall')
            run('stand')
            run('save')
            o = ouro_atual()
            print(f"[meta_pocao] Pós-Xadrez (Ciclo {rodada}): Ouro = {o} moedas (Faltam {max(0, meta - o)}).", flush=True)

        rodada += 1

    print(f"\n[meta_pocao] FINALIZADO! Saldo alcançado: {o} moedas.", flush=True)
    return o >= meta


if __name__ == '__main__':
    main()
