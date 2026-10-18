# -*- coding: utf-8 -*-
"""cacador_milharal.py - Executor contínuo e supervisionado do Milharal V2.

Ciclo por rodada:
1. Regenerar Mana no Templo (sleep até >= 340 mn).
2. Nutrição e Hidratação (pão da mochila + cantil).
3. Buffs ativos (armor + champions strength).
4. Executar milharal_v2.executar().
5. Retorno ao Templo, verificação de saldo e save.
6. Para quando atingir a meta de ouro (9.800) ou número de rodadas.
"""
import argparse
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'nucleo'))
sys.path.insert(0, str(ROOT / 'rotinas'))

from base import *
import milharal_v2


def descansar_ate_mana_cheia(min_mana=340, max_espera=120):
    print("[cacador] Descansando no Templo para recarga de mana...", flush=True)
    run('sleep')
    inicio = time.time()
    while time.time() - inicio < max_espera:
        time.sleep(10)
        t, v, _ = run('score')
        mn = v.get('mana')
        if mn is None:
            # Parse mana from prompt/text if needed
            for token in t.split():
                if token.endswith('mn'):
                    try:
                        mn = int(token[:-2])
                        break
                    except ValueError:
                        pass
        print(f"[cacador] Mana atual: {mn}/350", flush=True)
        if mn is not None and mn >= min_mana:
            break
    run('wake')
    run('stand')


def alimentar_e_hidratar(proativo=False):
    t, v, _ = run('score tudo')
    precisa_comer = 'fome' in t.lower() or proativo
    precisa_beber = 'sede' in t.lower() or proativo

    if precisa_comer:
        print("[cacador] Alimentando (pão da mochila)...", flush=True)
        run('get pao mochila')
        run('eat pao')
    if precisa_beber:
        print("[cacador] Hidratando (cantil)...", flush=True)
        r, _, _ = run('drink cantil')
        if 'vazio' in r.lower():
            print("[cacador] Cantil vazio! Enchendo na fonte da Praça do Templo...", flush=True)
            run('d')
            run('fill cantil fonte')
            run('drink cantil')
            run('u')


def ouro_atual():
    for _ in range(2):
        t, _, _ = run('score tudo')
        for line in t.splitlines():
            if 'Carregando:' in line:
                for p in line.split():
                    cleaned = p.replace('.', '').replace(',', '')
                    if cleaned.isdigit():
                        return int(cleaned)
        time.sleep(0.5)
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
    ap.add_argument('--rodadas', type=int, default=5, help='Número de rodadas')
    ap.add_argument('--meta-ouro', type=int, default=9800, help='Meta de ouro para parar')
    args = ap.parse_args()

    print(f"[cacador] Iniciando caçada: rodadas={args.rodadas}, meta_ouro={args.meta_ouro}", flush=True)
    run('recall')
    run('stand')

    ouro_ini = ouro_atual()
    exp_ini = exp_atual()
    total_abates = 0

    print(f"[cacador] Ouro inicial: {ouro_ini} | EXP inicial: {exp_ini}", flush=True)

    for r in range(1, args.rodadas + 1):
        print(f"\n=== [cacador] RODADA {r}/{args.rodadas} ===", flush=True)
        alimentar_e_hidratar(proativo=(r % 2 == 1))
        descansar_ate_mana_cheia()

        print("[cacador] Disparando milharal_v2...", flush=True)
        reiniciar_relogio()
        try:
            ok = milharal_v2.executar()
        except SystemExit as se:
            print(f"[cacador] Guarda de repeticao ativada ({se}); recuperando no Templo...", flush=True)
            run('recall')
            run('stand')
            ok = False
        except Exception as ex:
            print(f"[cacador] Excecao na rodada: {ex}; recuperando no Templo...", flush=True)
            run('recall')
            run('stand')
            ok = False
        print(f"[cacador] Rodada {r} concluída (ok={ok})", flush=True)

        ouro = ouro_atual()
        exp = exp_atual()
        print(f"[cacador] Progresso: Ouro={ouro}/{args.meta_ouro} (+{ouro - ouro_ini}) | EXP={exp} (+{exp - exp_ini})", flush=True)

        run('save')

        if ouro >= args.meta_ouro:
            print(f"[cacador] META DE OURO ATINGIDA! Saldo={ouro} moedas.", flush=True)
            break

    print(f"\n[cacador] Sessão finalizada. Saldo final: {ouro_atual()} moedas | EXP: {exp_atual()}", flush=True)
    return True


if __name__ == '__main__':
    main()
