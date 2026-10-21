#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""quality_run.py — o radar de USO das ferramentas (pedido do autor, Dia 158).

O problema que ele resolve: 4 dias passaram sem rotina supervisionada com o
`vigia.py` respondendo OK o tempo todo. O vigia olha o ESTADO da personagem (fome,
vida, combate); ele não sabe se você está andando à mão uma rota que o
`navegar.py` conhece, ou caçando à mão o que o `turno.py` faria.

A cada verificação, este radar pergunta ao `vigia.uso_do_transcript()`: nos
últimos N minutos, quem mandou os comandos? Se a maioria veio do `play.py` e é
passo ou ataque, o modo da diretiva §26 não está sendo seguido.

Não pergunta ao modelo se ele leu a diretiva — auto-relato não vale. **Afirma a
contradição e mostra a resolução**: rodar o script, ou mudar o modo com motivo.

O que ele NÃO pega: tática ruim com o script certo rodando. Para isso continua
valendo o `mandabala.py --sobre <alvo>` e o número no `conhecimento.md`.

Uso:
    python scripts/quality_run.py                    # uma verificação e sai
    python scripts/quality_run.py --loop             # a cada 30 min (job em segundo plano)
    python scripts/quality_run.py --loop --intervalo 15
    python scripts/quality_run.py --sem-registro     # não grava o histórico

Saída: 0 tudo em ordem | 1 USO_ANOMALO | 2 sem sessão (nada a medir).
"""
import argparse
import json
import sys
import time
from datetime import datetime
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ / "automato" / "nucleo"))
sys.path.insert(0, str(RAIZ / "automato" / "camadas"))

import config  # noqa: E402
import vigia  # noqa: E402

REGISTRO = Path(config.DIR_LOGS) / "qualidade.jsonl"


def verificar(janela=vigia.JANELA_USO_MIN):
    """Uma leitura: uso + diagnóstico. Devolve (dict, codigo)."""
    uso = vigia.uso_do_transcript(janela_min=janela)
    d = vigia.diagnostico_de_uso(uso, supervisionado=vigia.rotina_recente())
    codigo = {"OK": 0, "SEM_SESSAO": 2, "USO_ANOMALO": 1}.get(d["estado"], 1)
    return d, codigo


def linha_do_registro(d):
    u = d.get("uso") or {}
    return {
        "at": datetime.now().astimezone().isoformat(timespec="seconds"),
        "estado": d["estado"],
        "janela_min": u.get("janela_min"),
        "comandos": u.get("comandos"),
        "passos_mao": u.get("passos_mao"),
        "ataques_mao": u.get("ataques_mao"),
        "origens": u.get("por_origem"),
        "motivos": d.get("motivos"),
    }


def relatar(d):
    u = d.get("uso") or {}
    origens = ", ".join("%s=%d" % kv for kv in sorted((u.get("por_origem") or {}).items(),
                                                     key=lambda kv: -kv[1])) or "—"
    print("[QUALIDADE] %s · %s min · %s comandos · %s" % (
        d["estado"], u.get("janela_min"), u.get("comandos"), origens))
    for m in d.get("motivos") or []:
        print("  - %s" % m)
    if d["estado"] == "USO_ANOMALO":
        print("  Resolva AGORA, de um dos dois jeitos:")
        print("    a) rode a ferramenta do modo (navegar.py / turno.py --rotina <x>);")
        print("    b) mude o modo e registre o motivo no plano (§1) — mudar sem motivo é a falha.")


def main(argv=None):
    p = argparse.ArgumentParser(description="Radar de uso das ferramentas (diretiva §26).")
    p.add_argument("--janela", type=int, default=vigia.JANELA_USO_MIN,
                   help="minutos olhados para trás (padrão: %(default)s)")
    p.add_argument("--loop", action="store_true", help="repete a cada --intervalo minutos")
    p.add_argument("--intervalo", type=int, default=30, help="minutos entre verificações no --loop")
    p.add_argument("--sem-registro", action="store_true", help="não grava em runtime/qualidade.jsonl")
    p.add_argument("--json", action="store_true")
    a = p.parse_args(argv)

    codigo = 0
    while True:
        d, codigo = verificar(a.janela)
        if a.json:
            print(json.dumps(d, ensure_ascii=False))
        else:
            relatar(d)
        if not a.sem_registro and d["estado"] != "SEM_SESSAO":
            try:
                with REGISTRO.open("a", encoding="utf-8") as fh:
                    fh.write(json.dumps(linha_do_registro(d), ensure_ascii=False) + "\n")
            except OSError as e:
                print("[QUALIDADE] não consegui registrar: %s" % e, file=sys.stderr)
        if not a.loop:
            return codigo
        time.sleep(max(1, a.intervalo) * 60)


if __name__ == "__main__":
    for _s in (sys.stdout, sys.stderr):
        if hasattr(_s, "reconfigure"):
            _s.reconfigure(encoding="utf-8", errors="replace")
    sys.exit(main())
