#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""cota_claude.py - vigia de cota para o Claude Code (AGENTS.md §13).

O `checar_cota.py` só lê o Antigravity. No Claude Code a cota vem do `get_usage` do harness, que o Python
não alcança. Por isso o vigia lê um SNAPSHOT em automato/runtime/cota_claude.json, que o agente registra
logo depois de chamar `get_usage`, e recusa dado velho (cota.claude.fresco).

Uso:
  python scripts/cota_claude.py --registrar --5h 93 --semanal 7 [--reset5h ISO] [--resetsemanal ISO]
  python scripts/cota_claude.py            # checa o snapshot

Códigos de saída: 0 ok · 1 CRÍTICO ou snapshot ausente/velho (parar e fazer o handoff) · 2 atenção.
Cortes (cota.claude.corte): janela de 5 h restando <= 10%, semanal restando <= 5%.
"""
import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SNAPSHOT = ROOT / "automato" / "runtime" / "cota_claude.json"

CORTE_5H_RESTANTE = 10.0       # cota.claude.corte
CORTE_SEMANAL_RESTANTE = 5.0   # cota.claude.corte
VALIDADE_MIN = 20.0            # cota.claude.fresco: snapshot mais velho que isto não vale


def _agora():
    return datetime.now(timezone.utc)


def avaliar(snap, agora=None):
    """(codigo, [mensagens]) a partir de um snapshot; função pura, testável."""
    agora = agora or _agora()
    if not snap:
        return 1, ["sem snapshot: chame get_usage e registre com --registrar (cota.claude.fresco)"]
    try:
        quando = datetime.fromisoformat(str(snap["registrado_em"]).replace("Z", "+00:00"))
        usado_5h = float(snap["usado_5h_pct"])
        usado_sem = float(snap["usado_semanal_pct"])
    except (KeyError, ValueError, TypeError):
        return 1, ["snapshot ilegível: registre de novo com --registrar"]
    idade = (agora - quando).total_seconds() / 60.0
    msgs, codigo = [], 0
    if idade > VALIDADE_MIN:
        return 1, ["snapshot com %.0f min (> %.0f): chame get_usage e registre de novo (cota.claude.fresco)"
                   % (idade, VALIDADE_MIN)]
    rest_5h, rest_sem = 100.0 - usado_5h, 100.0 - usado_sem
    for nome, rest, corte in (("janela de 5 h", rest_5h, CORTE_5H_RESTANTE),
                              ("semanal", rest_sem, CORTE_SEMANAL_RESTANTE)):
        if rest <= corte:
            msgs.append("CRÍTICO: %s restando %.0f%% (corte %.0f%%): parar e fazer o handoff (PROTOCOLO §3)"
                        % (nome, rest, corte))
            codigo = 1
        elif rest <= corte * 2:
            msgs.append("atenção: %s restando %.0f%% (corte %.0f%%)" % (nome, rest, corte))
            codigo = max(codigo, 2)
        else:
            msgs.append("ok: %s restando %.0f%%" % (nome, rest))
    return codigo, msgs


def carregar(caminho=SNAPSHOT):
    try:
        return json.loads(Path(caminho).read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None


def registrar(usado_5h, usado_sem, reset5h=None, resetsem=None, caminho=SNAPSHOT):
    snap = {"registrado_em": _agora().isoformat(), "usado_5h_pct": float(usado_5h),
            "usado_semanal_pct": float(usado_sem), "reset_5h": reset5h, "reset_semanal": resetsem}
    Path(caminho).parent.mkdir(parents=True, exist_ok=True)
    Path(caminho).write_text(json.dumps(snap, ensure_ascii=False, indent=2), encoding="utf-8")
    return snap


def main(argv=None):
    ap = argparse.ArgumentParser(description="vigia de cota do Claude Code")
    ap.add_argument("--registrar", action="store_true", help="grava o snapshot a partir do get_usage")
    ap.add_argument("--5h", dest="usado_5h", type=float, help="percentual USADO da janela de 5 h")
    ap.add_argument("--semanal", dest="usado_sem", type=float, help="percentual USADO da janela semanal")
    ap.add_argument("--reset5h")
    ap.add_argument("--resetsemanal")
    args = ap.parse_args(argv)
    if args.registrar:
        if args.usado_5h is None or args.usado_sem is None:
            ap.error("--registrar exige --5h e --semanal")
        registrar(args.usado_5h, args.usado_sem, args.reset5h, args.resetsemanal)
    codigo, msgs = avaliar(carregar())
    for m in msgs:
        print("[cota-claude] " + m)
    return codigo


if __name__ == "__main__":
    sys.exit(main())
