#!/usr/bin/env python3
"""Verifica o PROTOCOLO DE FIM DE SESSÃO antes de deixar o próximo agente continuar.

**Rode isto antes de encerrar.** Ele não substitui o julgamento — ele pega o que passar despercebido:
a descoberta que existe em prosa e não no artefato, o plano sem devolutiva, a evidência sem autoria,
o capítulo fechado pela metade.

Existe porque duas sessões seguidas falharam do MESMO jeito (Dia 156): a de `deepseek-flash` publicou
uma crônica errada, e a de `Gemini 3.8 Flash` andou os esgotos, descobriu que quatro salas eram anéis
de mão dupla, escreveu isso no `conhecimento.md` **e não tocou no `mapa.json`**. Nos dois casos, nenhum
validador percebeu — o `check_project.py` confere estrutura, não cobertura.

Uso:
    python scripts/devolutiva.py                  # herói com planos, verificação completa
    python scripts/devolutiva.py --hero grebolius
    python scripts/devolutiva.py --desde HEAD~1   # compara o que mudou desde um commit
    python scripts/devolutiva.py --sem-git        # pula as checagens que dependem de git

Saída: código 0 se tudo passa; 1 se houver FALHA; 2 se houver só AVISO.
"""
import argparse
import json
import os
import re
import subprocess
import sys
from pathlib import Path

for _stream in (sys.stdout, sys.stderr):
    if hasattr(_stream, "reconfigure"):
        _stream.reconfigure(encoding="utf-8", errors="replace")

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

FALHAS, AVISOS, OKS = [], [], []


def ok(msg):
    OKS.append(msg)
    print(f"  [ok]    {msg}")


def falha(msg):
    FALHAS.append(msg)
    print(f"  [FALHA] {msg}")


def aviso(msg):
    AVISOS.append(msg)
    print(f"  [aviso] {msg}")


def git(*args, cwd=None):
    r = subprocess.run(["git", *args], capture_output=True, text=True,
                       encoding="utf-8", errors="replace", cwd=cwd or ROOT)
    return r.returncode, (r.stdout or "").strip()


def mudou(caminho, desde, sem_git=False):
    """O caminho foi tocado no diff? (arquivos versionados + não rastreados)"""
    if sem_git:
        return (ROOT / caminho).is_file()
    if desde:
        codigo, saida = git("diff", "--name-only", desde, "--", caminho)
        if codigo == 0 and saida:
            return True
    codigo, saida = git("status", "--porcelain", "--", caminho)
    return codigo == 0 and bool(saida)


# --------------------------------------------------------------------------- #
# 1. O plano
# --------------------------------------------------------------------------- #

def checar_plano(heroi, numero_esperado=None):
    import mandabala  # reaproveita a descoberta de planos

    planos = mandabala.planos_de(heroi)
    if not planos:
        falha(f"nenhum plano em data/heroes/{heroi}/planos/ — o AGENTS.md §6.1 exige criar o próximo")
        return None, None

    numero, caminho = planos[-1]
    texto = caminho.read_text(encoding="utf-8", errors="replace")
    rel = caminho.relative_to(ROOT).as_posix()

    if numero_esperado is not None and numero != numero_esperado:
        falha(f"o plano mais alto é o {numero:03d}, mas o esperado era {numero_esperado:03d} "
              "(o número seguinte ao da sessão anterior)")
    else:
        ok(f"plano vigente: {rel}")

    campos = mandabala.cabecalho_do_plano(texto)
    if not campos.get("Por"):
        falha(f"{rel} não declara autoria ('Por') — AGENTS.md §0 e §6.1")
    else:
        ok(f"autoria declarada: {campos['Por']}")

    tem, real = mandabala.devolutiva_tecnica(texto)
    if not tem:
        falha(f"{rel} não tem a seção 'Devolutiva técnica'")
    elif not real:
        falha(f"{rel}: a seção 'Devolutiva técnica' está só com o MODELO (placeholders)")
    else:
        ok("seção 'Devolutiva técnica' presente e preenchida")

    return numero, texto


# --------------------------------------------------------------------------- #
# 2. Coerência: o que a devolutiva PROMETE está no artefato?
# --------------------------------------------------------------------------- #

# A chave é o CAMINHO do artefato, não uma palavra-chave: é assim que o modelo do LEIA.md escreve a
# coluna "Registrei em". Casar por sinônimo (`referencia`) falhava porque a célula traz o caminho.
ARTEFATOS = {
    "mapa.json": ("data/heroes/{heroi}/mapa.json",
                  "a devolutiva promete o mapa, mas o mapa.json NÃO foi tocado nesta sessão"),
    "verificacoes.md": ("maquina/verificacoes.md",
                        "a devolutiva promete referência de servidor, mas maquina/verificacoes.md "
                        "NÃO foi tocado"),
    "conhecimento.md": ("data/heroes/{heroi}/conhecimento.md",
                        "a devolutiva promete fato do mundo, mas conhecimento.md NÃO foi tocado"),
    "CHANGELOG.md": ("automato/CHANGELOG.md",
                     "a devolutiva promete erro do motor, mas o CHANGELOG.md NÃO foi tocado"),
}

# "ainda não fiz" declarado no plano é honestidade, não falha. Vira aviso.
PENDENTE = re.compile(r"\b(pendente|a fazer|nada|não fiz|nao fiz|falta)\b", re.IGNORECASE)


def desde_da_sessao(heroi, explicito):
    """O commit anterior ao início desta sessão.

    O plano ANTERIOR foi criado no FIM da sessão passada — então o commit que o adicionou é a
    fronteira. Tudo depois dele é esta sessão. É mais preciso que `HEAD~1`, que erra quando a
    sessão já publicou (foi o que aconteceu: o `conhecimento.md` já estava commitado).
    """
    if explicito:
        return explicito
    import mandabala
    planos = mandabala.planos_de(heroi)
    for _, caminho in reversed(planos[:-1]):          # o penúltimo plano, do mais novo para trás
        rel = caminho.relative_to(ROOT).as_posix()
        codigo, saida = git("log", "--diff-filter=A", "--format=%H", "-1", "--", rel)
        if codigo == 0 and saida:
            return saida.split("\n")[0]
    return "HEAD"


def checar_coerencia_da_devolutiva(heroi, texto, desde, sem_git=False):
    """O coração da verificação: prometer no plano e não gravar no artefato.

    Só olha as LINHAS DE TABELA da seção (a segunda coluna, "Registrei em") — a prosa explicativa
    ao redor fala dos mesmos arquivos e não é promessa nenhuma. E uma linha marcada PENDENTE vira
    aviso: declarar o que não se fez é o comportamento certo, não o errado.
    """
    if not texto:
        return
    secao = re.search(r"^#{1,4}\s*\d*\.?\s*devolutiva\s+t[eé]cnica(.*?)(?=^#{1,4}\s*\d+\.|\Z)",
                      texto, re.IGNORECASE | re.MULTILINE | re.DOTALL)
    if not secao:
        return

    linhas = [l.strip() for l in secao.group(1).split("\n") if l.strip().startswith("|")]
    if not linhas:
        aviso("a devolutiva não tem tabela — não há o que conferir contra o git")
        return

    for linha in linhas:
        if re.fullmatch(r"[|\-: ]+", linha):
            continue
        celulas = [c.strip() for c in linha.strip("|").split("|")]
        if len(celulas) < 3 or celulas[0].lower().startswith(("descobri", "sintoma")):
            continue                                   # cabeçalho ou linha fora do modelo
        destino = celulas[1]
        if not destino or destino.startswith("<"):
            continue                                   # modelo não preenchido
        for chave, (caminho_tpl, msg) in ARTEFATOS.items():
            if chave not in destino:
                continue
            if PENDENTE.search(linha):
                aviso(f"devolutiva declara PENDENTE em '{chave}' — o próximo tem de fazer: "
                      f"{' '.join(celulas[2:])[:80]}")
                continue
            caminho = caminho_tpl.format(heroi=heroi)
            if mudou(caminho, desde, sem_git=sem_git):
                ok(f"coerência: '{chave}' prometido e {caminho} alterado")
            else:
                falha(msg + f"  (destino declarado: {destino[:60]})")


# --------------------------------------------------------------------------- #
# 3. Capítulo, evidência, livro-razão
# --------------------------------------------------------------------------- #

def checar_capitulos(heroi):
    arq = ROOT / "data" / "heroes" / heroi / "capitulos.json"
    if not arq.is_file():
        aviso("capitulos.json ausente — herói legado? pulando")
        return
    capitulos = json.loads(arq.read_text(encoding="utf-8")).get("chapters", [])
    if not capitulos:
        aviso("capitulos.json sem capítulos")
        return

    em_curso = [c for c in capitulos if c.get("status") == "em_curso"]
    fechados = [c for c in capitulos if c.get("status") == "concluido"]
    print(f"  [info]  capítulos: {len(fechados)} concluído(s), {len(em_curso)} em curso")

    for cap in capitulos:
        if cap.get("status") != "concluido":
            continue
        for i, parte in enumerate(cap.get("parts") or [], 1):
            etiqueta = f"capítulo {cap.get('id')} parte {i}"
            for campo in ("source_kind", "date", "evidence"):
                if not parte.get(campo):
                    falha(f"{etiqueta} sem '{campo}' — o check_project.py reprova isso")
            if parte.get("evidence") and not isinstance(parte["evidence"], list):
                falha(f"{etiqueta}: 'evidence' precisa ser lista")
        if cap.get("parts"):
            ok(f"capítulo {cap.get('id')} com parts completas")


def checar_evidencias(heroi, desde):
    pasta = ROOT / "data" / "heroes" / heroi / "evidence"
    if not pasta.is_dir():
        aviso("pasta evidence/ ausente")
        return
    novas = [p for p in sorted(pasta.glob("*.json"), key=lambda p: p.stat().st_mtime)
             if mudou(p.relative_to(ROOT).as_posix(), desde)]
    if not novas:
        aviso("nenhuma evidência nova/alterada nesta sessão — se jogou, grave uma")
        return
    for arq in novas[-5:]:
        try:
            dados = json.loads(arq.read_text(encoding="utf-8"))
        except Exception as e:
            falha(f"{arq.name}: JSON inválido ({e})")
            continue
        if isinstance(dados, dict) and not dados.get("agent"):
            falha(f"{arq.name} sem o campo 'agent' — AGENTS.md §0")
        elif isinstance(dados, list):
            ok(f"{arq.name}: lista de fontes ({len(dados)} item(ns))")
        else:
            ok(f"{arq.name}: com autoria ({dados.get('agent')})")


def checar_livro_razao(desde):
    arq = ROOT / "docs" / "agentes" / "registro_de_evolucao.md"
    if not arq.is_file():
        aviso("registro de evolução ausente")
        return
    if not mudou("docs/agentes/registro_de_evolucao.md", desde):
        aviso("o livro-razão não foi tocado nesta sessão — AGENTS.md §6 pede um bloco novo")
        return
    texto = arq.read_text(encoding="utf-8", errors="replace")
    if not re.search(r"^### .*·.*·\s*\S", texto, re.MULTILINE):
        aviso("livro-razão alterado, mas não achei bloco no formato '### data · dia · modelo'")
    else:
        ok("livro-razão com bloco no formato do §2")


# --------------------------------------------------------------------------- #
# 4. Validações e git
# --------------------------------------------------------------------------- #

def rodar(cmd, rotulo):
    # GUARDA DE RECURSÃO: este script roda a suíte de testes, e pode ser chamado DE DENTRO dela.
    # Sem esta guarda, `devolutiva.py` -> suíte -> test_devolutiva.py -> devolutiva.py -> ... trava.
    if os.environ.get("DSH_DEVOLUTIVA_RODANDO"):
        aviso(f"{rotulo}: pulado (já estamos dentro de uma execução da devolutiva)")
        return
    ambiente = dict(os.environ, DSH_DEVOLUTIVA_RODANDO="1")
    r = subprocess.run([sys.executable, *cmd], capture_output=True, text=True,
                       encoding="utf-8", errors="replace", cwd=ROOT, env=ambiente,
                       timeout=600)
    saida = ((r.stdout or "") + (r.stderr or "")).strip()
    if r.returncode == 0:
        ultima = [l for l in saida.split("\n") if l.strip()][-1] if saida else ""
        ok(f"{rotulo}: {ultima[:90]}")
    else:
        falha(f"{rotulo} retornou {r.returncode}: {saida[-300:]}")


def checar_git():
    codigo, saida = git("status", "--porcelain")
    if codigo != 0:
        aviso("não é um repositório git? pulando")
        return
    linhas = [l for l in saida.split("\n") if l.strip()]
    alheios = [l for l in linhas if "test_local.js" not in l]
    if alheios:
        aviso(f"{len(alheios)} arquivo(s) pendente(s) no git — publique ou explique:\n"
              + "\n".join("           " + l for l in alheios[:8]))
    else:
        ok("árvore git limpa")

    # segredos: nada de runtime/ ou credencial entrando no git
    codigo, saida = git("ls-files", "--cached", "automato/runtime")
    if saida:
        falha("há arquivos de automato/runtime/ RASTREADOS no git — segredos! (AGENTS.md §4.9)")
    else:
        ok("nenhum arquivo de automato/runtime/ rastreado")


# --------------------------------------------------------------------------- #

def main(argv=None):
    p = argparse.ArgumentParser(
        description="Verifica o protocolo de fim de sessão antes de deixar o próximo continuar.")
    p.add_argument("--hero", dest="heroi", help="id do herói (padrão: detecta)")
    p.add_argument("--desde", default=None,
                   help="commit base para o diff (padrão: HEAD; use HEAD~1 para a sessão inteira)")
    p.add_argument("--sem-git", action="store_true", help="pula as checagens de git")
    args = p.parse_args(argv)

    import mandabala
    heroi, erro = mandabala.resolver_heroi(args.heroi)
    if erro:
        print(f"[DEVOLUTIVA] {erro}", file=sys.stderr)
        return 1

    desde = None if args.sem_git else desde_da_sessao(heroi, args.desde)

    print("=" * 74)
    print(f"DEVOLUTIVA · fechamento de sessão · {heroi}")
    print("=" * 74)

    print("\n1. Plano numerado")
    numero, texto = checar_plano(heroi)

    print("\n2. Coerência da devolutiva técnica (o prometido está no artefato?)")
    if texto:
        checar_coerencia_da_devolutiva(heroi, texto, desde, sem_git=args.sem_git)
    else:
        aviso("sem plano, sem devolutiva a conferir")

    print("\n3. Capítulo, evidências e livro-razão")
    checar_capitulos(heroi)
    if not args.sem_git:
        checar_evidencias(heroi, desde)
        checar_livro_razao(desde)

    print("\n4. Validações")
    rodar(["scripts/check_project.py"], "check_project.py")
    rodar(["automato/verificar.py"], "verificar.py")
    rodar(["-B", "-m", "unittest", "discover", "-s", "scripts", "-p", "test_*.py"], "suíte offline")

    if not args.sem_git:
        print("\n5. Git")
        checar_git()

    print("\n" + "=" * 74)
    print(f"RESULTADO: {len(FALHAS)} falha(s), {len(AVISOS)} aviso(s), {len(OKS)} verificação(ões) ok")
    print("=" * 74)
    if FALHAS:
        print("\nFALHAS — resolva antes de encerrar:")
        for f in FALHAS:
            print(f"  * {f}")
        return 1
    if AVISOS:
        print("\nAvisos (leia, não silencie):")
        for a in AVISOS:
            print(f"  - {a}")
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
