# -*- coding: utf-8 -*-
"""cacador_hibrido.py - Ciclo Híbrido Contínuo: Milharal -> Novatos -> Descanso & Venda.

Atende à demanda do autor:
Alterna entre duas zonas com respawn independente para zerar o tempo ocioso:
1. Milharal V2: caça monstros de colheita rápida (50 moedas/mob direto no corpo).
2. Masmorra dos Novatos: caça zumbis, monstros novatos e minotauro, vendendo espólios leves.
3. Descanso & Logística: hidratação na fonte, pão da mochila e sono restaurador no Templo.
Para automaticamente ao atingir a meta de ouro (9.800 moedas).
"""
import argparse
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
import novatos
import guarda_cota


def descansar_ate_mana_cheia(min_mana=340, max_espera=120):
    print("[cacador_hibrido] Descansando no Templo para recarga de mana...", flush=True)
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
        print(f"[cacador_hibrido] Mana atual: {mn}/360", flush=True)
        if mn is not None and mn >= min_mana:
            break
    run('wake')
    run('stand')


def alimentar_e_hidratar(proativo=False):
    t, _, _ = run('score tudo')
    precisa_comer = 'fome' in t.lower() or proativo
    precisa_beber = 'sede' in t.lower() or proativo

    if precisa_comer:
        print("[cacador_hibrido] Alimentando (pão da mochila)...", flush=True)
        run('get pao mochila')
        run('eat pao')
    if precisa_beber:
        print("[cacador_hibrido] Hidratando...", flush=True)
        r, _, _ = run('drink cantil')
        if 'vazio' in r.lower():
            print("[cacador_hibrido] Cantil vazio! Enchendo na fonte da Praça do Templo...", flush=True)
            run('d')
            run('fill cantil fonte')
            run('drink cantil')
            run('u')


def ouro_atual():
    t, _, _ = run('score tudo')
    for line in t.splitlines():
        if 'Carregando:' in line:
            for p in line.split():
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
    ap.add_argument('--ciclos', type=int, default=5, help='Número de ciclos (Milharal + Novatos)')
    ap.add_argument('--meta-ouro', type=int, default=9800, help='Meta de ouro para parar')
    args = ap.parse_args()

    print(f"[cacador_hibrido] Iniciando ciclo híbrido: ciclos={args.ciclos}, meta_ouro={args.meta_ouro}", flush=True)
    run('recall'); run('stand')

    ouro_ini = ouro_atual()
    exp_ini = exp_atual()

    print(f"[cacador_hibrido] Ouro inicial: {ouro_ini} | EXP inicial: {exp_ini}", flush=True)

    for c in range(1, args.ciclos + 1):
        print(f"\n==========================================", flush=True)
        print(f"=== [cacador_hibrido] CICLO {c}/{args.ciclos} ===", flush=True)
        print(f"==========================================", flush=True)

        # Guarda Inteligente de Cota de IA
        if not guarda_cota.checar_guarda():
            print("[cacador_hibrido] Interrompendo caçada híbrida devido a cota baixa (handoff executado).", flush=True)
            return False

        # FASE 1: Milharal V2
        print(f"[cacador_hibrido] [Ciclo {c}] >> FASE 1: Milharal V2...", flush=True)
        alimentar_e_hidratar(proativo=(c % 2 == 1))
        descansar_ate_mana_cheia()
        try:
            milharal_v2.executar()
        except Exception as ex:
            print(f"[cacador_hibrido] Exceção no Milharal: {ex}; recuperando no Templo...", flush=True)
            run('recall'); run('stand')

        voltar_ao_templo()
        run('stand')
        ouro_meio = ouro_atual()
        print(f"[cacador_hibrido] Pós-Milharal: Ouro={ouro_meio} (+{ouro_meio - ouro_ini})", flush=True)

        if ouro_meio >= args.meta_ouro:
            print(f"[cacador_hibrido] META DE OURO ATINGIDA: {ouro_meio} >= {args.meta_ouro}!", flush=True)
            break

        # FASE 2: Tabuleiro de Xadrez V3
        print(f"[cacador_hibrido] [Ciclo {c}] >> FASE 2: Tabuleiro de Xadrez V3...", flush=True)
        descansar_ate_mana_cheia(min_mana=320)
        try:
            xadrez_v3.executar(max_abates=4)
        except Exception as ex:
            print(f"[cacador_hibrido] Exceção no Xadrez: {ex}; recuperando no Templo...", flush=True)
            run('recall'); run('stand')

        voltar_ao_templo()
        run('stand')
        run('save')

        ouro_xadrez = ouro_atual()
        print(f"[cacador_hibrido] Pós-Xadrez: Ouro={ouro_xadrez} (+{ouro_xadrez - ouro_ini})", flush=True)
        if ouro_xadrez >= args.meta_ouro:
            print(f"[cacador_hibrido] META DE OURO ATINGIDA: {ouro_xadrez} >= {args.meta_ouro}!", flush=True)
            break

        # FASE 3: Masmorra dos Novatos
        print(f"[cacador_hibrido] [Ciclo {c}] >> FASE 3: Masmorra dos Novatos...", flush=True)
        descansar_ate_mana_cheia(min_mana=300)
        try:
            novatos.executar(max_abates=6)
        except Exception as ex:
            print(f"[cacador_hibrido] Exceção nos Novatos: {ex}; recuperando no Templo...", flush=True)
            run('recall'); run('stand')

        voltar_ao_templo()
        run('stand')
        run('save')

        ouro = ouro_atual()
        exp = exp_atual()
        print(f"[cacador_hibrido] Pós-Novatos (Fim do Ciclo {c}): Ouro={ouro} (+{ouro - ouro_ini}) | EXP={exp} (+{exp - exp_ini})", flush=True)

        if ouro >= args.meta_ouro:
            print(f"[cacador_hibrido] META DE OURO ATINGIDA: {ouro} >= {args.meta_ouro}!", flush=True)
            break

    ouro_fim = ouro_atual()
    exp_fim = exp_atual()

    print(f"\n==========================================", flush=True)
    print(f"[cacador_hibrido] CAÇADA HÍBRIDA FINALIZADA", flush=True)
    print(f"Ouro Ganho: {ouro_fim - ouro_ini} moedas (Saldo final: {ouro_fim})", flush=True)
    print(f"EXP Ganha: {exp_fim - exp_ini} EXP (Total final: {exp_fim})", flush=True)
    print(f"==========================================", flush=True)
    return True


if __name__ == '__main__':
    main()
