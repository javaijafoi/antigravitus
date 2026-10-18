# -*- coding: utf-8 -*-
"""cacador_xadrez_v3.py - Executor contínuo e supervisionado do Xadrez V3 (3 rodadas de benchmark).

Executa 3 rodadas consecutivas de xadrez_v3 medindo:
- Tempo de execução
- Abates e coletas de peças
- Ouro obtido com vendas em lote (armaduras, escudos e espadas)
- EXP acumulada
"""
import argparse
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'nucleo'))
sys.path.insert(0, str(ROOT / 'rotinas'))

from base import *
import xadrez_v3


def descansar_ate_mana_cheia(min_mana=340, max_espera=120):
    print("[cacador_xadrez_v3] Descansando no Templo para recarga de mana...", flush=True)
    run('sleep')
    inicio = time.time()
    while time.time() - inicio < max_espera:
        time.sleep(8)
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
        print(f"[cacador_xadrez_v3] Mana atual: {mn}/360", flush=True)
        if mn is not None and mn >= min_mana:
            break
    run('wake')
    run('stand')


def alimentar_e_hidratar():
    t, _, _ = run('score tudo')
    precisa_comer = 'fome' in t.lower()
    precisa_beber = 'sede' in t.lower()

    if precisa_comer:
        print("[cacador_xadrez_v3] Alimentando (pão da mochila)...", flush=True)
        run('get pao mochila')
        run('eat pao')
    if precisa_beber:
        print("[cacador_xadrez_v3] Hidratando...", flush=True)
        r, _, _ = run('drink cantil')
        if 'vazio' in r.lower():
            print("[cacador_xadrez_v3] Cantil vazio! Enchendo na fonte da Praça do Templo...", flush=True)
            run('d')
            run('fill cantil fonte')
            run('drink cantil')
            run('u')


def ouro_atual():
    t, _, _ = run('score tudo')
    for line in t.splitlines():
        if 'Carregando:' in line:
            parts = line.split()
            for p in parts:
                cleaned = p.replace('.', '').replace(',', '')
                if cleaned.isdigit():
                    return int(cleaned)
    return 0


def exp_atual():
    t, _, _ = run('score')
    for line in t.splitlines():
        if 'Experiência:' in line:
            parts = line.split()
            for p in parts:
                cleaned = p.replace('.', '').replace(',', '')
                if cleaned.isdigit():
                    return int(cleaned)
    return 0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--rodadas', type=int, default=3, help='Número de rodadas')
    args = ap.parse_args()

    print(f"[cacador_xadrez_v3] Iniciando benchmark do Xadrez V3: {args.rodadas} rodadas", flush=True)
    run('recall'); run('stand')

    ouro_ini = ouro_atual()
    exp_ini = exp_atual()
    total_abates = 0
    t0 = time.time()

    print(f"[cacador_xadrez_v3] Ouro inicial: {ouro_ini} | EXP inicial: {exp_ini}", flush=True)

    for r in range(1, args.rodadas + 1):
        print(f"\n=== [cacador_xadrez_v3] RODADA {r}/{args.rodadas} ===", flush=True)
        alimentar_e_hidratar()
        descansar_ate_mana_cheia()

        print("[cacador_xadrez_v3] Disparando xadrez_v3...", flush=True)
        r_ini_ouro = ouro_atual()
        r_ini_exp = exp_atual()
        r_t0 = time.time()

        abates = 0
        try:
            abates = xadrez_v3.executar(max_abates=4)
        except SystemExit as se:
            print(f"[cacador_xadrez_v3] Guarda de repetição ({se}); recuperando no Templo...", flush=True)
            run('recall'); run('stand')
        except Exception as ex:
            print(f"[cacador_xadrez_v3] Exceção na rodada: {ex}; recuperando no Templo...", flush=True)
            run('recall'); run('stand')

        duracao = time.time() - r_t0
        total_abates += abates
        ouro = ouro_atual()
        exp = exp_atual()
        delta_ouro = ouro - r_ini_ouro
        delta_exp = exp - r_ini_exp

        print(f"[cacador_xadrez_v3] Rodada {r} finalizada em {duracao:.1f}s: {abates} abates/peças | Ouro={delta_ouro:+d} | EXP={delta_exp:+d}", flush=True)
        print(f"[cacador_xadrez_v3] Acumulado: Ouro={ouro} (+{ouro - ouro_ini}) | EXP={exp} (+{exp - exp_ini})", flush=True)
        run('save')

    tempo_total = time.time() - t0
    ouro_fim = ouro_atual()
    exp_fim = exp_atual()

    print(f"\n==========================================", flush=True)
    print(f"[cacador_xadrez_v3] BENCHMARK XADREZ V3 FINALIZADO ({args.rodadas} rodadas em {tempo_total:.1f}s)", flush=True)
    print(f"Total Abates/Peças: {total_abates}", flush=True)
    print(f"Ouro Ganho: {ouro_fim - ouro_ini} moedas (Saldo final: {ouro_fim})", flush=True)
    print(f"EXP Ganha: {exp_fim - exp_ini} EXP (Total final: {exp_fim})", flush=True)
    print(f"==========================================", flush=True)
    return True


if __name__ == '__main__':
    main()
