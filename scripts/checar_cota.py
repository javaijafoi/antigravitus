#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""checar_cota.py - Consulta em tempo real o saldo de cota e a janela de limites do Antigravity.

Monitora:
- Limite Diário / Janela Curta (reset <= 24h): corte crítico em <= 10%
- Limite Semanal / Weekly (reset > 24h): corte crítico em <= 5%

Endpoint interno:
http://127.0.0.1:<port>/exa.language_server_pb.LanguageServerService/GetUserStatus
com header 'x-codeium-csrf-token' obtido da variável ANTIGRAVITY_CSRF_TOKEN.
"""

import os
import sys
import json
import ssl
import urllib.request
from datetime import datetime, timezone


def consultar_cota():
    port = 61220
    ls_addr = os.environ.get("ANTIGRAVITY_LS_ADDRESS", "")
    if ":" in ls_addr:
        try:
            port = int(ls_addr.split(":")[-1])
        except Exception:
            pass

    token = os.environ.get("ANTIGRAVITY_CSRF_TOKEN", "")

    url = f"http://127.0.0.1:{port}/exa.language_server_pb.LanguageServerService/GetUserStatus"
    headers = {
        "Content-Type": "application/json",
        "Connect-Protocol-Version": "1",
        "User-Agent": "antigravity",
    }
    if token:
        headers["x-codeium-csrf-token"] = token
        headers["X-Csrf-Token"] = token

    payload = json.dumps({
        "metadata": {
            "ideName": "antigravity",
            "extensionName": "antigravity",
            "locale": "en",
        }
    }).encode("utf-8")

    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    req = urllib.request.Request(url, data=payload, headers=headers, method="POST")
    try:
        with urllib.request.urlopen(req, context=ctx, timeout=3.0) as resp:
            data = json.loads(resp.read().decode("utf-8"))
    except Exception as e:
        print(f"[ERRO] Falha ao consultar language server local ({url}): {e}")
        return None

    status = data.get("userStatus", {})
    plan_name = status.get("planStatus", {}).get("planInfo", {}).get("planName", "Desconhecido")
    models = status.get("cascadeModelConfigData", {}).get("clientModelConfigs", [])

    agrupados = {}
    now = datetime.now(timezone.utc)

    for m in models:
        label = m.get("label", "")
        quota = m.get("quotaInfo", {})
        frac = quota.get("remainingFraction")
        reset_str = quota.get("resetTime")

        tempo_restante = "—"
        is_weekly = False
        horas_restantes = 0.0

        if reset_str:
            try:
                dt = datetime.fromisoformat(reset_str.replace("Z", "+00:00"))
                diff = dt - now
                if diff.total_seconds() > 0:
                    horas_restantes = diff.total_seconds() / 3600.0
                    horas = int(diff.total_seconds() // 3600)
                    minutos = int((diff.total_seconds() % 3600) // 60)
                    tempo_restante = f"{horas}h {minutos:02d}m"
                    is_weekly = (horas_restantes > 24.0)
                else:
                    tempo_restante = "reseta agora"
            except Exception:
                tempo_restante = reset_str

        tipo = "Semanal" if is_weekly else "Diário"
        threshold = 0.05 if is_weekly else 0.10
        pct = f"{frac * 100:.1f}%" if frac is not None else "100.0%"

        if frac is not None:
            if frac <= threshold:
                estado = "CRÍTICO (<= corte)"
            elif frac <= threshold * 2:
                estado = "ATENÇÃO"
            else:
                estado = "OK"
        else:
            estado = "OK (sem limite)"

        familia = label.split("(")[0].strip()
        if familia not in agrupados:
            agrupados[familia] = {
                "frac": frac,
                "pct": pct,
                "tipo": tipo,
                "threshold_pct": f"{threshold * 100:.0f}%",
                "reset": tempo_restante,
                "reset_iso": reset_str,
                "estado": estado,
            }

    print("==========================================================================================")
    print(f"ANTIGRAVITY · COTA E JANELA DE LIMITES · Plano: {plan_name}")
    print("==========================================================================================")
    print(f"{'Modelo / Família':<22} | {'Saldo':<8} | {'Tipo':<9} | {'Corte':<6} | {'Reseta Em':<12} | {'Status'}")
    print("-" * 90)
    for fam, info in agrupados.items():
        print(f"{fam:<22} | {info['pct']:<8} | {info['tipo']:<9} | {info['threshold_pct']:<6} | {info['reset']:<12} | {info['estado']}")
    print("==========================================================================================")
    return agrupados


if __name__ == "__main__":
    consultar_cota()
