#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""checar_cota.py - Consulta em tempo real o saldo de cota e a janela de 5 horas do Antigravity.

Endpoint interno descoberto:
http://127.0.0.1:61220/exa.language_server_pb.LanguageServerService/GetUserStatus
com header 'x-codeium-csrf-token' obtido da variavel de ambiente ANTIGRAVITY_CSRF_TOKEN.
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
        if reset_str:
            try:
                dt = datetime.fromisoformat(reset_str.replace("Z", "+00:00"))
                diff = dt - now
                if diff.total_seconds() > 0:
                    horas = int(diff.total_seconds() // 3600)
                    minutos = int((diff.total_seconds() % 3600) // 60)
                    tempo_restante = f"{horas}h {minutos:02d}m"
                else:
                    tempo_restante = "reseta agora"
            except Exception:
                tempo_restante = reset_str

        pct = f"{frac * 100:.1f}%" if frac is not None else "100.0% (sem limite fracionado)"

        # Agrupar por família para não poluir
        familia = label.split("(")[0].strip()
        if familia not in agrupados:
            agrupados[familia] = {
                "frac": frac,
                "pct": pct,
                "reset": tempo_restante,
                "reset_iso": reset_str,
            }

    print("==========================================================================")
    print(f"ANTIGRAVITY · COTA E JANELA DE LIMITES · Plano: {plan_name}")
    print("==========================================================================")
    print(f"{'Modelo / Família':<32} | {'Saldo Restante':<15} | {'Reseta Em':<15}")
    print("-" * 74)
    for fam, info in agrupados.items():
        print(f"{fam:<32} | {info['pct']:<15} | {info['reset']:<15}")
    print("==========================================================================")
    return agrupados


if __name__ == "__main__":
    consultar_cota()
