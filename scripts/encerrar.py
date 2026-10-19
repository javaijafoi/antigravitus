#!/usr/bin/env python3
"""Encerramento e handoff de sessão em um comando — o par do mandabala.py.

O mandabala.py diz por onde começar; este diz como terminar. Antes, o handoff estava em prosa em
quatro lugares (AGENTS §9 e §13, LEIA.md, §9 de cada plano) e cada modelo fazia de um jeito. Agora a
sequência está no PROTOCOLO.md §3, e este script faz a parte mecânica.

Duas etapas:

    python scripts/encerrar.py --agente "<modelo/versão>"
        1. confere no transcript mais recente se o fecho foi `_CLOSE sleep` com save e sleep confirmados;
        2. roda sync_hero --check, check_project e auditar_sessao, e resume tudo num quadro;
        3. se o plano mais alto já está commitado (é da sessão anterior), CRIA o esqueleto do próximo,
           com cabeçalho e §2 (estado exato) tirados do state.json. Nunca sobrescreve.

    python scripts/encerrar.py --agente "<modelo/versão>" --fechar --avanco sim|nao
        depois de preencher o plano: confere o modelo v2, roda o devolutiva.py e grava uma linha
        no docs/agentes/boletim.jsonl (para comparar modelos com dado, não com impressão).

    --simular   mostra o que faria, sem gravar nada.

Não joga, não faz commit, não publica. Saída: 0 ok | 1 há FALHA | 2 só avisos.
"""
import argparse
import json
import re
import subprocess
import sys
from datetime import date
from pathlib import Path

for _stream in (sys.stdout, sys.stderr):
    if hasattr(_stream, "reconfigure"):
        _stream.reconfigure(encoding="utf-8", errors="replace")

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import mandabala  # noqa: E402

RUNTIME = ROOT / "automato" / "runtime"
BOLETIM = ROOT / "docs" / "agentes" / "boletim.jsonl"


# --------------------------------------------------------------------------- #
# Funções puras (testadas em test_encerrar.py)
# --------------------------------------------------------------------------- #

def fecho_do_transcript(registros):
    """Resumo do fecho de um transcript: {'fechou', 'save', 'sleep'}. ID na catraca: encerrar.fecho."""
    fecho = next((r for r in reversed(registros) if r.get("kind") == "close"), None)
    if not fecho:
        return {"fechou": False, "save": False, "sleep": False}
    return {"fechou": True, "save": bool(fecho.get("save_confirmed")),
            "sleep": bool(fecho.get("sleep_confirmed"))}


def _num(v):
    return f"{v:,}".replace(",", ".") if isinstance(v, int) else str(v)


def estado_do_state(state):
    """§2 'Estado exato' do plano, em números, a partir do state.json."""
    vit = state.get("vitals") or {}

    def par(chave):
        v = vit.get(chave) or {}
        return f"{v.get('current', '?')}/{v.get('max', '?')}"

    exp = state.get("experience") or {}
    alin = state.get("alignment") or {}
    loc = state.get("location") or {}
    armor = state.get("armor") or {}
    asof = state.get("as_of") or {}
    linhas = [
        f"- **Local:** {loc.get('name', '?')} (`{loc.get('room_id', '?')}`)",
        f"- **Vida/mana/MV:** {par('hp')} · {par('mana')} · {par('mv')}",
        f"- **Nível:** {state.get('level', '?')} · EXP {_num(exp.get('current', '?'))} "
        f"(próximo nível em {_num(exp.get('next_level', '?'))})",
        f"- **Alinhamento:** {alin.get('value', '?')} ({alin.get('label', '?')}) · wimpy {state.get('wimpy', '?')}",
        f"- **Ouro:** {_num(state.get('gold', '?'))}",
        f"- **CA:** base {armor.get('base', '?')} / com magias {armor.get('with_armor', '?')}",
    ]
    for c in (state.get("conditions") or [])[:6]:
        linhas.append(f"- {c}")
    linhas.append(f"- **Fonte:** `state.json` (as_of dia {asof.get('day', '?')}, "
                  f"verificação {asof.get('verification', '?')}). Confira com `score tudo` ao conectar.")
    return "\n".join(linhas)


def esqueleto_plano(numero, agente, heroi, state, hoje):
    """Texto do plano NNN com o que é mecânico já preenchido e o julgamento em <...>."""
    dia = (state.get("as_of") or {}).get("day") or state.get("as_of_day") or "?"
    obj = (state.get("next_objective") or {}).get("title", "<uma frase>")
    return f"""# Plano {numero:03d} — <capítulo ou objetivo>

| | |
|---|---|
| **Criado em** | {hoje} · Dia {dia} |
| **Por** | {agente} |
| **Herói** | {heroi} |
| **Objetivo** | {obj} |
| **Sessão encerrada?** | <sim/não — onde ficou, save/sleep confirmados, driver fechado> |

> Plano v2: **autossuficiente** (não escreva "igual ao Plano N": copie o que segue valendo) e com
> **§5 executável** (uma ação; se houver bloqueio, diga qual opção o próximo executa por padrão).
> Apague este quadro ao preencher.

## 1. Onde o objetivo está
<o que está feito, o que falta, em duas ou três frases>

## 2. Estado exato
{estado_do_state(state)}

## 3. O que já foi descoberto
<rotas verificadas, endereços, padrões — tudo o que o próximo NÃO precisa redescobrir, inclusive o que veio de planos anteriores e continua valendo>

## 4. Os bloqueios, e o que já foi tentado
<cada bloqueio com o resultado de cada tentativa>

## 5. O próximo passo, e só ele
<uma ação concreta que o próximo executa sem perguntar. Se houver opções, liste em ordem e marque a padrão>

## 6. NÃO REPITA
<caminhos já provados errados>

## 7. Ferramentas e comandos
<o que existe e como se usa; ver a tabela "Ferramentas" do automato/README.md>

## 8. Devolutiva técnica
| Descobri | Registrei em | O quê |
|---|---|---|
| mapa | `mapa.json` | <salas/arestas, ou "nada"> |
| referência do servidor | `maquina/verificacoes.md` | <comando/mensagem nova, ou "nada"> |
| fato do mundo | `conhecimento.md` §NN | <NPC/item/perigo, ou "nada"> |
| erro do motor | `automato/CHANGELOG.md` | <o que travou, ou "nada"> |

## 9. Como encerrar a sua sessão
Siga `docs/agentes/PROTOCOLO.md` §3: `_CLOSE sleep` no Templo, evidência com `agent`,
`python scripts/encerrar.py --agente "<modelo/versão>"`, preencher o plano {numero + 1:03d},
`python scripts/encerrar.py --agente "<modelo/versão>" --fechar --avanco sim|nao`.
"""


def resumo_saida(texto, padrao):
    """(falhas, avisos) lidos da linha de resumo de um verificador; (None, None) se não achar."""
    m = re.search(padrao, texto or "")
    return (int(m.group(1)), int(m.group(2))) if m else (None, None)


RX_DEVOLUTIVA = r"RESULTADO:\s*(\d+)\s*falha\(s\),\s*(\d+)\s*aviso"
RX_AUDITOR = r"Resumo:\s*(\d+)\s*falha\(s\),\s*(\d+)\s*aviso"


def linha_boletim(hoje, agente, heroi, plano, fecho, devolutiva, auditor, avanco, v2):
    """Uma linha JSON do boletim. ID na catraca: encerrar.boletim."""
    return {
        "data": hoje, "agente": agente, "heroi": heroi, "plano": plano,
        "sessao_fechada": fecho, "devolutiva": {"falhas": devolutiva[0], "avisos": devolutiva[1]},
        "auditor": {"falhas": auditor[0], "avisos": auditor[1]},
        "plano_v2": [i for i, _ in v2], "avanco_declarado": avanco,
    }


# --------------------------------------------------------------------------- #
# Efeitos (git, subprocessos, arquivos)
# --------------------------------------------------------------------------- #

def transcript_recente():
    if not RUNTIME.is_dir():
        return None
    todos = [p for p in RUNTIME.glob("transcript_*.jsonl") if p.stat().st_size > 0]
    return max(todos, key=lambda p: p.stat().st_mtime) if todos else None


def ler_jsonl(caminho):
    regs = []
    for linha in caminho.read_text(encoding="utf-8", errors="replace").splitlines():
        try:
            regs.append(json.loads(linha))
        except ValueError:
            continue
    return regs


def plano_e_desta_sessao(caminho):
    """True se o plano está novo ou alterado no git (logo, foi criado nesta sessão)."""
    r = subprocess.run(["git", "status", "--porcelain", "--", str(caminho)], capture_output=True,
                       text=True, encoding="utf-8", errors="replace", cwd=ROOT)
    return r.returncode == 0 and bool(r.stdout.strip())


def rodar(args, rotulo):
    print(f"  ... {rotulo}")
    r = subprocess.run([sys.executable, "-X", "utf8", *args], capture_output=True, text=True,
                       encoding="utf-8", errors="replace", cwd=ROOT, timeout=900)
    return r.returncode, (r.stdout or "") + (r.stderr or "")


def main(argv=None):
    p = argparse.ArgumentParser(description="Encerramento e handoff de sessão (PROTOCOLO §3).")
    p.add_argument("--agente", required=True, help='modelo/versão, ex.: "Gemini 3.8 Flash (High)"')
    p.add_argument("--hero", dest="heroi")
    p.add_argument("--fechar", action="store_true", help="etapa final: devolutiva + boletim")
    p.add_argument("--avanco", choices=("sim", "nao"),
                   help="com --fechar: a sessão avançou o objetivo do plano?")
    p.add_argument("--simular", action="store_true", help="não grava nada")
    a = p.parse_args(argv)

    if "<" in a.agente or len(a.agente.strip()) < 3:
        print("[ENCERRAR] --agente precisa do seu modelo/versão real (AGENTS §0).", file=sys.stderr)
        return 1
    if a.fechar and not a.avanco:
        print("[ENCERRAR] --fechar exige --avanco sim|nao (a sessão avançou o objetivo?).", file=sys.stderr)
        return 1

    heroi, erro = mandabala.resolver_heroi(a.heroi)
    if erro:
        print(f"[ENCERRAR] {erro}", file=sys.stderr)
        return 1
    hoje = date.today().isoformat()
    falhas, avisos = [], []

    print("=" * 74)
    print(f"ENCERRAR · {heroi} · {a.agente} · {'fechar' if a.fechar else 'preparar'}"
          f"{' · SIMULAÇÃO' if a.simular else ''}")
    print("=" * 74)

    # 1. fecho no jogo
    tr = transcript_recente()
    fecho = fecho_do_transcript(ler_jsonl(tr)) if tr else None
    if not tr:
        avisos.append("[encerrar.fecho] nenhum transcript em automato/runtime/ — se não jogou, ok")
    elif not fecho["fechou"]:
        falhas.append(f"[encerrar.fecho] {tr.name} sem registro de close: faça `_CLOSE sleep` no Templo")
    elif not (fecho["save"] and fecho["sleep"]):
        falhas.append(f"[encerrar.fecho] {tr.name}: close sem save/sleep confirmados ({fecho})")
    else:
        print(f"  [ok]    fecho confirmado em {tr.name} (save e sleep)")

    planos = mandabala.planos_de(heroi)
    numero, caminho = planos[-1] if planos else (0, None)
    auditor = (None, None)
    if tr:
        _, saida = rodar(["scripts/auditar_sessao.py", str(tr)], "auditar_sessao.py")
        auditor = resumo_saida(saida, RX_AUDITOR)
        if auditor[0]:
            avisos.append(f"[encerrar.auditor] auditor: {auditor[0]} FALHA(s) — corrija ou justifique no §4/§6 do plano")

    if not a.fechar:
        # 2. verificações de derivados e estrutura
        for args, rot in ((["scripts/sync_hero.py", "--hero", heroi, "--check"], "sync_hero --check"),
                          (["scripts/check_project.py"], "check_project.py")):
            codigo, saida = rodar(args, rot)
            ultima = [l for l in saida.splitlines() if l.strip()][-1:] or [""]
            if codigo:
                falhas.append(f"{rot} retornou {codigo}: {ultima[0][:120]}")
            else:
                print(f"  [ok]    {rot}: {ultima[0][:90]}")

        # 3. esqueleto do próximo plano
        if caminho is not None and plano_e_desta_sessao(caminho):
            print(f"  [info]  o plano {numero:03d} já é desta sessão (novo/alterado no git): preencha-o")
        else:
            novo = numero + 1
            destino = ROOT / "data" / "heroes" / heroi / "planos" / f"plano{novo:03d}.md"
            state_arq = ROOT / "data" / "heroes" / heroi / "state.json"
            state = json.loads(state_arq.read_text(encoding="utf-8")) if state_arq.is_file() else {}
            texto = esqueleto_plano(novo, a.agente, heroi, state, hoje)
            if destino.exists():
                falhas.append(f"{destino.name} já existe — não sobrescrevo")
            elif a.simular:
                print(f"  [sim]   criaria {destino.relative_to(ROOT).as_posix()}:\n")
                print(texto)
            else:
                destino.write_text(texto, encoding="utf-8")
                print(f"  [ok]    esqueleto criado: {destino.relative_to(ROOT).as_posix()}")
        print("\nPróximo: preencha o plano (§1, §3–§6, §8) e rode de novo com --fechar --avanco sim|nao.")
    else:
        # 4. etapa final: plano v2 + devolutiva + boletim
        texto = caminho.read_text(encoding="utf-8", errors="replace") if caminho else ""
        v2 = mandabala.checar_plano_v2(texto)
        if "<" in mandabala.secao(texto, 5) or "<" in mandabala.secao(texto, 1):
            falhas.append(f"[encerrar.plano_preenchido] plano {numero:03d} ainda tem <placeholders> no §1/§5")
        for ident, msg in v2:
            (falhas if numero >= mandabala.PLANO_V2_DESDE else avisos).append(f"[{ident}] {msg}")
        codigo, saida = rodar(["scripts/devolutiva.py", "--hero", heroi], "devolutiva.py")
        devol = resumo_saida(saida, RX_DEVOLUTIVA)
        print("\n".join("  | " + l for l in saida.splitlines() if "[FALHA]" in l or "RESULTADO" in l))
        if codigo == 1:
            falhas.append(f"devolutiva.py: {devol[0]} falha(s) — veja a saída acima")
        linha = linha_boletim(hoje, a.agente, heroi, f"plano{numero:03d}", fecho, devol, auditor,
                              a.avanco, v2)
        if a.simular:
            print(f"  [sim]   gravaria no boletim: {json.dumps(linha, ensure_ascii=False)}")
        else:
            with BOLETIM.open("a", encoding="utf-8") as f:
                f.write(json.dumps(linha, ensure_ascii=False) + "\n")
            print(f"  [ok]    boletim gravado em {BOLETIM.relative_to(ROOT).as_posix()}")

    print("\n" + "=" * 74)
    print(f"RESULTADO: {len(falhas)} falha(s), {len(avisos)} aviso(s)")
    for f in falhas:
        print(f"  [FALHA] {f}")
    for w in avisos:
        print(f"  [aviso] {w}")
    return 1 if falhas else (2 if avisos else 0)


if __name__ == "__main__":
    sys.exit(main())
