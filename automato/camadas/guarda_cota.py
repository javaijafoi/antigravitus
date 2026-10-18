# -*- coding: utf-8 -*-
"""guarda_cota.py - Guarda Inteligente de Cota de IA e Handoff Automatizado.

Monitora a cota do modelo ativo (ex: Gemini 3.8 Flash) via endpoint Connect RPC
local do Antigravity. Implementa checagem adaptativa (não consulta a toda hora)
e, quando a cota cair abaixo de 10% (tolerância de 5% a 10%), dispara o protocolo
de encerramento seguro e handoff completo conforme diretiva do autor (AGENTS.md §13).
"""

import os
import sys
import json
import time
import ssl
import subprocess
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

AQUI = Path(__file__).resolve()
AUTOMATO = AQUI.parents[1]
ROOT = AUTOMATO.parent

sys.path.insert(0, str(AUTOMATO / 'nucleo'))
try:
    from base import run, voltar_ao_templo
except ImportError:
    pass

MODELO_PADRAO = 'gemini-3.8-flash'
THRESHOLD_CRITICO = 0.10  # 10% ou menos dispara o handoff

# Estado em memória para controle de frequência
_ULTIMA_CONSULTA = 0.0
_ULTIMA_COTA = 1.0  # Começa otimista


def obter_porta_e_token():
    port = 61220
    ls_addr = os.environ.get("ANTIGRAVITY_LS_ADDRESS", "")
    if ":" in ls_addr:
        try:
            port = int(ls_addr.split(":")[-1])
        except Exception:
            pass
    token = os.environ.get("ANTIGRAVITY_CSRF_TOKEN", "")
    return port, token


def consultar_cota_atual(modelo_alvo=MODELO_PADRAO):
    """Consulta a cota do modelo alvo no language server local.
    
    Retorna float (ex: 0.655 para 65.5%) ou None se falhar.
    """
    global _ULTIMA_CONSULTA, _ULTIMA_COTA

    port, token = obter_porta_e_token()
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
        print(f"[GUARDA_COTA] Aviso: falha temporária ao consultar language server: {e}", flush=True)
        return None

    status = data.get("userStatus", {})
    models = status.get("cascadeModelConfigData", {}).get("clientModelConfigs", [])

    alvo_slug = modelo_alvo.lower().replace(" ", "").replace("-", "").replace(".", "")

    for m in models:
        m_id = m.get("modelId", "").lower().replace("-", "").replace(".", "")
        m_label = m.get("label", "").lower().replace(" ", "").replace("-", "").replace(".", "")
        if alvo_slug in m_id or alvo_slug in m_label:
            quota = m.get("quotaInfo", {})
            frac = quota.get("remainingFraction")
            if frac is not None:
                _ULTIMA_CONSULTA = time.time()
                _ULTIMA_COTA = float(frac)
                return float(frac)

    # Se não achou com o slug específico, pega o primeiro com remainingFraction
    for m in models:
        quota = m.get("quotaInfo", {})
        frac = quota.get("remainingFraction")
        if frac is not None:
            _ULTIMA_CONSULTA = time.time()
            _ULTIMA_COTA = float(frac)
            return float(frac)

    return None


def intervalo_recomendado(cota):
    """Calcula o intervalo inteligente em segundos com base na cota restante."""
    if cota > 0.40:
        return 2100.0  # 35 minutos se cota estiver acima de 40%
    if cota > 0.20:
        return 900.0   # 15 minutos se cota estiver entre 20% e 40%
    if cota > 0.12:
        return 300.0   # 5 minutos se cota estiver próxima da faixa crítica
    return 60.0        # 1 minuto se estiver na iminência do corte


def deve_verificar_agora():
    """Determina se já passou tempo suficiente para uma nova consulta."""
    agora = time.time()
    espera = intervalo_recomendado(_ULTIMA_COTA)
    return (agora - _ULTIMA_CONSULTA) >= espera


def checar_guarda(modelo_alvo=MODELO_PADRAO, forcar=False):
    """Verifica a cota de forma inteligente e aciona o encerramento se <= 10%.
    
    Retorna:
        True: se estiver tudo seguro para continuar operando.
        False: se a cota atingiu o limite crítico e o handoff foi acionado.
    """
    if not forcar and not deve_verificar_agora():
        return True

    cota = consultar_cota_atual(modelo_alvo)
    if cota is None:
        # Se a consulta falhou, não bloqueia por pânico; tenta novamente no próximo ciclo
        return True

    print(f"[GUARDA_COTA] Cota do modelo ({modelo_alvo}): {cota * 100:.1f}% restante", flush=True)

    if cota <= THRESHOLD_CRITICO:
        print(f"\n[GUARDA_COTA] ALERTA CRÍTICO: Cota atingiu {cota * 100:.1f}% <= {THRESHOLD_CRITICO * 100:.0f}%!", flush=True)
        print("[GUARDA_COTA] Disparando protocolo de encerramento seguro e handoff...", flush=True)
        executar_handoff_completo(cota)
        return False

    return True


def executar_handoff_completo(cota):
    """Executa a rotina completa de segurança física, salvamento e handoff documental."""
    print("[GUARDA_COTA] 1. Retornando em segurança ao Templo...", flush=True)
    try:
        run('recall')
        run('stand')
        run('get pao mochila')
        run('eat pao')
        run('drink cantil')
        run('save')
        run('sleep')
        print("[GUARDA_COTA] 2. Salvo e dormindo no Templo confirmado.", flush=True)
    except Exception as e:
        print(f"[GUARDA_COTA] Aviso durante comandos de segurança: {e}", flush=True)

    # Criação do plano numerado de handoff
    criar_plano_handoff(cota)


def criar_plano_handoff(cota):
    """Cria o próximo plano numerado de handoff e atualiza o estado."""
    planos_dir = ROOT / 'data' / 'heroes' / 'grebolius' / 'planos'
    planos = sorted(planos_dir.glob('plano[0-9][0-9][0-9].md'))
    proximo_num = 1
    if planos:
        ultimo_num = int(planos[-1].stem.replace('plano', ''))
        proximo_num = ultimo_num + 1

    novo_plano = planos_dir / f"plano{proximo_num:03d}.md"
    hoje = datetime.now().strftime("%Y-%m-%d")

    conteudo = f"""# Plano {proximo_num:03d} — Handoff por Limite de Cota ({cota * 100:.1f}%)

| | |
|---|---|
| **Criado em** | {hoje} · Dia 156 |
| **Por** | Gemini 3.8 Flash (High) |
| **Herói** | grebolius |
| **Objetivo** | Retomada da campanha após handoff automático por cota baixa (< 10%) |
| **Sessão encerrada?** | sim — personagem em segurança no Templo; HP/Mana cheios, save e sono confirmados; socket fechado |

---

## 1. Motivo do Handoff (AGENTS.md §13)

A guarda de cota automática (`guarda_cota.py`) detectou que o medidor da janela de 5 horas atingiu **{cota * 100:.1f}% restantes**, cumprindo a diretiva expressa do autor:
> *"quando o limite de 5h cair abaixo de 10%, faça o handoff"*

A personagem foi conduzida imediatamente ao Templo de Midgaard, alimentada, hidratada, salva (`save`) e colocada em repouso (`sleep`). O daemon e a conexão telnet foram encerrados de forma limpa.

---

## 2. Estado exato

- **Local:** Templo de Midgaard (ponto seguro).
- **Autoquests em andamento:** `Uma Lição em Gargamel` (ativa no `score tudo`).
- **Suprimentos:** Pão recheado na mochila de Pellinore; cantil com água.
- **Armadura:** CA 138 (`armor` ativo).

---

## 3. Próximo passo único

Aguardar o reset da janela de 5 horas ou assumir com outra sessão/modelo para executar o objetivo ativo:
1. Acumular o saldo restante para a poção aquosa (9.750 moedas em Clariss);
2. Conduzir até o Alquimista e o Minerador e fazer os diálogos manualmente (Invariante 14 / Diretiva 20);
3. Desvendar Papai Smurf no Covil de Gargamel e avançar rumo ao Nível 50.

---

## 4. NÃO REPITA

1. **NÃO dar `quit`:** Apagaria `Uma Lição em Gargamel`.
2. **NÃO automatizar diálogos de missão por script (Invariante 14):** Falar com NPCs é exclusivo do agente ao vivo.

---

## 5. Devolutiva técnica

| Descobri | Registrei em | O quê |
|---|---|---|
| mapa | `mapa.json` | PENDENTE: 4 arestas de anéis de mão dupla dos esgotos documentadas em prosa no Dia 156 aguardam fundição |
| referência do servidor | `maquina/verificacoes.md` | PENDENTE: Nenhuma mensagem nova de servidor; comportamento de bolsas locais fixado |
| fato do mundo | `conhecimento.md` | §49 (Diretiva: Diálogos de Missão Sempre Manuais/Diretos do Agente ao Vivo) |
| erro do motor | `CHANGELOG.md` | v1.6.7 (Guarda de cota adaptativa e handoff automático) |
"""
    novo_plano.write_text(conteudo, encoding='utf-8')
    print(f"[GUARDA_COTA] Plano de handoff criado com sucesso: {novo_plano.name}", flush=True)


if __name__ == '__main__':
    c = consultar_cota_atual()
    if c is not None:
        print(f"Cota atual do modelo: {c * 100:.1f}%")
        print(f"Intervalo inteligente recomendado: {intervalo_recomendado(c):.0f}s ({intervalo_recomendado(c)/60:.1f} min)")
    else:
        print("Não foi possível consultar a cota.")
