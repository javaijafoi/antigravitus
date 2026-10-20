#!/usr/bin/env python3
"""Acha o plano mais recente de um herói e entrega ao agente a ordem de leitura.

O autor diz "mandabala": roda este script e o agente recebe, num bloco só,
**qual plano é o vigente** e o **conteúdo integral** dele. Não edita nada,
não joga, não publica — só lê e mostra.

Uso:
    python scripts/mandabala.py                    # herói com planos, plano mais alto
    python scripts/mandabala.py --hero grebolius
    python scripts/mandabala.py --listar           # todos os planos, dos dois heróis
    python scripts/mandabala.py --numero 3         # um plano específico
    python scripts/mandabala.py --so-caminho       # imprime só o caminho do plano
"""
import argparse
import re
import sys
from pathlib import Path

for _stream in (sys.stdout, sys.stderr):
    if hasattr(_stream, "reconfigure"):
        _stream.reconfigure(encoding="utf-8", errors="replace")

ROOT_DIR = Path(__file__).resolve().parents[1]
HEROES_DIR = ROOT_DIR / "data" / "heroes"
PADRAO = re.compile(r"^plano(\d{3,})\.md$", re.IGNORECASE)


def heroes_com_planos():
    """Heróis que têm pasta de planos, em ordem alfabética."""
    if not HEROES_DIR.is_dir():
        return []
    return sorted(
        d.name for d in HEROES_DIR.iterdir()
        if d.is_dir() and (d / "planos").is_dir()
    )


def planos_de(heroi):
    """[(numero, caminho)] do herói, ordenado por número."""
    pasta = HEROES_DIR / heroi / "planos"
    if not pasta.is_dir():
        return []
    achados = []
    for arq in pasta.iterdir():
        m = PADRAO.match(arq.name)
        if m and arq.is_file():
            achados.append((int(m.group(1)), arq))
    return sorted(achados)


def resolver_heroi(pedido):
    """Devolve o herói a usar; erro claro se houver ambiguidade."""
    disponiveis = heroes_com_planos()
    if not disponiveis:
        return None, "nenhum herói tem pasta 'planos/' ainda."
    if pedido:
        if pedido not in disponiveis:
            return None, (f"o herói '{pedido}' não tem planos. "
                          f"Com planos: {', '.join(disponiveis)}.")
        return pedido, None
    if len(disponiveis) == 1:
        return disponiveis[0], None
    # mais de um: prefere o que tem o plano mais alto
    return max(disponiveis, key=lambda h: max(n for n, _ in planos_de(h))), None


def cabecalho_do_plano(texto):
    """Extrai 'Por', 'Criado em' e 'Objetivo' da tabela do plano, se houver."""
    campos = {}
    for chave in ("Criado em", "Por", "Herói", "Objetivo", "Sessão encerrada?"):
        m = re.search(rf"\|\s*\*\*{re.escape(chave)}\*\*\s*\|\s*(.+?)\s*\|", texto)
        if m:
            campos[chave] = re.sub(r"[*`]", "", m.group(1)).strip()
    return campos


def lacunas(numeros):
    """Números faltantes entre 1 e o maior."""
    if not numeros:
        return []
    return [n for n in range(1, max(numeros) + 1) if n not in numeros]


DEVOLUTIVA = re.compile(r"^#{1,4}\s*\d*\.?\s*devolutiva\s+t[eé]cnica", re.IGNORECASE | re.MULTILINE)
PLACEHOLDER = re.compile(r"<[^>\n]{3,}>")


def devolutiva_tecnica(texto):
    """(tem_secao, tem_conteudo_real) da devolutiva técnica de um plano.

    O AGENTS.md §5 diz ONDE cada descoberta vai; o que faltava era alguém cobrar. O sintoma de
    devolutiva ignorada é a descoberta existir em prosa e não no artefato — aconteceu no Dia 156,
    quando a caminhada revelou os anéis do esgoto e o `mapa.json` não foi tocado.
    """
    m = DEVOLUTIVA.search(texto)
    if not m:
        return False, False

    corpo = []
    for linha in texto[m.end():].split("\n"):
        if re.match(r"^#{1,4}\s*\d+\.", linha):      # começou outra seção numerada
            break
        if linha.strip():
            corpo.append(linha.strip())

    # O cabeçalho e a régua da tabela do modelo NÃO contam como conteúdo: sem isso, um plano que
    # só copiou o modelo passaria no teste. (Foi o que a primeira versão fazia.)
    CABECALHO = re.compile(r"^(descobri|registrei em|o qu[êe])\b", re.IGNORECASE)

    def util(linha):
        if PLACEHOLDER.search(linha):
            return False
        if re.fullmatch(r"[|\-: ]+", linha):          # régua |---|---|
            return False
        celulas = [c.strip() for c in linha.strip("|").split("|")]
        if celulas and all(CABECALHO.match(c) for c in celulas if c):
            return False                              # cabeçalho do modelo
        return len(linha.strip(" |-")) > 12

    return True, any(util(l) for l in corpo)


# --------------------------------------------------------------------------- #
# Plano v2: autossuficiente e com próximo passo executável (catraca, AGENTS §14)
# --------------------------------------------------------------------------- #

# A partir deste número as regras do plano v2 são FALHA no devolutiva.py; antes, só aviso.
# Os planos antigos são append-only e não podem ser corrigidos.
PLANO_V2_DESDE = 34

# "Igual ao Plano 032", "o do Plano 032", "lê-lo inteiro": a seção manda o leitor a outro plano em
# vez de trazer o conteúdo. Foi o que os planos 029 e 033 fizeram; os do Gemini (ex.: 026) não.
REFERENCIA = re.compile(
    r"\b(igual\s+ao|(?:tudo\s+)?os?\s+do|sem\s+mudan[çc]a\s+desde\s+o|vale\s+o\s+do)\s+plano\s+\d+"
    r"|l[êe]-lo\s+inteiro",
    re.IGNORECASE)
# §5 que devolve a decisão ao autor ("decidir, com o autor, ...") em vez de dizer o que fazer.
DELEGA = re.compile(
    r"(decidir|combinar|definir|perguntar|consultar|aguardar)[^.\n]{0,40}\bautor\b"
    r"|\bcom\s+o\s+autor\b",
    re.IGNORECASE)
# Pedir ao autor é legítimo quando a regra manda: give/compra (#13), ética (#15), diretiva expressa.
DELEGA_LEGITIMA = re.compile(r"#\s*1[35]\b|invariante\s+1[35]|diretiva", re.IGNORECASE)


def delegacao_sem_motivo(passo):
    """Primeira frase do §5 que devolve a decisão ao autor sem citar #13/#15/diretiva NA MESMA FRASE.

    DELEGA_MESMA_FRASE: a citação vale só para a frase em que aparece. A brecha real (Plano 035):
    o §5 citava "AGENTS #13 e #14" ao falar do give e, em outra frase, mandava "perguntar ao autor a
    palavra de abertura", que estava no conhecimento.md. Citar #13 em qualquer lugar não pode
    liberar todas as delegações do parágrafo.
    """
    for frase in re.split(r"(?<=[.;:!?])\s+|\n+", passo):
        if DELEGA.search(frase) and not DELEGA_LEGITIMA.search(frase):
            return frase.strip()
    return None


def secao(texto, numero):
    """Corpo da seção '## <numero>. ...' do plano, sem o título. '' se não houver."""
    m = re.search(rf"^#{{1,4}}\s*{numero}\.[^\n]*\n(.*?)(?=^#{{1,4}}\s*\d+\.|\Z)",
                  texto, re.MULTILINE | re.DOTALL)
    return m.group(1).strip() if m else ""


def checar_plano_v2(texto):
    """[(id, mensagem)] do que o plano v2 exige e este plano não cumpre. Lista vazia = ok.

    IDs na catraca (docs/agentes/catraca.json): plano.autossuficiente, plano.estado_numerico,
    plano.proximo_passo_executavel.
    """
    achados = []
    for n, nome in ((1, "onde o objetivo está"), (2, "estado exato"), (3, "o que já foi descoberto"),
                    (4, "bloqueios"), (5, "próximo passo"), (6, "não repita"), (7, "ferramentas")):
        corpo = secao(texto, n)
        m = REFERENCIA.search(corpo)
        if m:
            achados.append(("plano.autossuficiente",
                            f"§{n} ({nome}) remete a outro plano (\"{m.group(0)}\") em vez de trazer o "
                            "conteúdo. Copie o que segue valendo: o próximo lê só este plano."))
    estado = secao(texto, 2)
    if len(re.findall(r"\d+", estado)) < 3:
        achados.append(("plano.estado_numerico",
                        "§2 (estado exato) sem números: vida/mana/MV, ouro, nível, local. "
                        "O encerrar.py gera essa seção a partir do state.json."))
    passo = secao(texto, 5)
    if not passo:
        achados.append(("plano.proximo_passo_executavel", "plano sem §5 (o próximo passo, e só ele)."))
    else:
        frase = delegacao_sem_motivo(passo)
        if frase:
            achados.append(("plano.proximo_passo_executavel",
                            f"§5 devolve a decisão ao autor (\"{frase[:90]}\"). Diga qual ação o próximo "
                            "executa por padrão. Perguntar ao autor só em AGENTS #13/#15 ou diretiva "
                            "expressa, citada na mesma frase. Antes, procure a resposta: "
                            "python scripts/mandabala.py --sobre <termo>."))
    return achados


# --------------------------------------------------------------------------- #
# Sessão deixada aberta (sessao.aberta)
# --------------------------------------------------------------------------- #

RUNTIME_DIR = ROOT_DIR / "automato" / "runtime"


def transcripts(desde_ts=0.0, pasta=None):
    """Transcripts com conteúdo modificados depois de desde_ts (epoch), do mais antigo ao mais novo."""
    pasta = pasta or RUNTIME_DIR
    if not pasta.is_dir():
        return []
    achados = [p for p in pasta.glob("transcript_*.jsonl")
               if p.stat().st_size > 0 and p.stat().st_mtime > desde_ts]
    return sorted(achados, key=lambda p: p.stat().st_mtime)


def sessao_aberta(caminho):
    """True se o transcript tem comando e não termina com close/shutdown. ID: sessao.aberta.

    Caso real (Dia 157): depois do commit do handoff, uma conexão nova levou a personagem a Lyon e
    ficou aberta, parada, sem `_CLOSE`. O driver grava 'close' e 'shutdown' ao fechar; sem eles, a
    personagem está no mundo, sem ninguém olhando.
    """
    import json
    tipos = []
    for linha in caminho.read_text(encoding="utf-8", errors="replace").splitlines():
        try:
            tipos.append(json.loads(linha).get("kind"))
        except ValueError:
            continue
    return "command" in tipos and not ({"close", "shutdown"} & set(tipos))


# --------------------------------------------------------------------------- #
# O que o repositório já sabe (abertura.conhecimento_do_npc, --sobre)
# --------------------------------------------------------------------------- #

# Palavras com maiúscula que não são nome de NPC, lugar ou missão (início de frase, rótulos).
_NAO_NOMES = {"Antes", "Depois", "Opção", "Se", "Só", "Não", "Nunca", "Ir", "Ler", "Abrir", "Voltar",
              "Parar", "Confirmar", "Testar", "Levar", "Registrar", "Seguir", "Usar", "Fazer",
              "Agents", "Plano", "Capítulo", "Templo", "Midgaard", "Sala", "Você", "Ajuda", "Mágica",
              "Entrada", "Centro", "Cidade", "Rua", "Python", "Ainda", "Quando", "Sempre"}
# Termo que aparece em mais linhas que isto é genérico demais para ajudar (ex.: Templo: 83).
_GENERICO = 25


def _fontes(heroi):
    pasta = HEROES_DIR / heroi
    return [pasta / "conhecimento.md", pasta / "missoes.json"]


# Linhas de missoes.json que só apontam arquivo não dizem nada sobre o NPC.
_LINHA_VAZIA = re.compile(r'^\s*"(document|evidence|source|day|agent)"\s*:')


def sobre(termo, heroi, maximo=6):
    """O que conhecimento.md e missoes.json dizem sobre o termo.

    Devolve (secoes, linhas, total): as seções '## ' do conhecimento.md que citam o termo, da mais
    nova para a mais antiga; as linhas, com as do conhecimento.md primeiro e as mais recentes antes;
    e o total de menções. Arquivo ausente = nada a mostrar.
    """
    secoes, do_conhecimento, das_missoes = [], [], []
    for arq in _fontes(heroi):
        if not arq.is_file():
            continue
        secao_atual = ""
        for n, linha in enumerate(arq.read_text(encoding="utf-8", errors="replace").splitlines(), 1):
            if linha.startswith("## "):
                secao_atual = linha[3:].strip()
            if termo.lower() not in linha.lower() or _LINHA_VAZIA.match(linha):
                continue
            item = f"{arq.name}:{n}  {linha.strip()[:220]}"
            if arq.name == "conhecimento.md":
                do_conhecimento.append(item)
                if secao_atual and secao_atual not in secoes:
                    secoes.append(secao_atual)
            else:
                das_missoes.append(item)
    linhas = list(reversed(do_conhecimento)) + list(reversed(das_missoes))
    return list(reversed(secoes)), linhas[:maximo], len(do_conhecimento) + len(das_missoes)


def termos_do_passo(passo):
    """Nomes próprios do §5 (NPC, lugar, item), na ordem em que aparecem, sem repetição.

    Verbo no infinitivo com maiúscula ('Reabrir', 'Ir') é início de frase, não nome.
    """
    vistos = []
    for t in re.findall(r"\b[A-ZÀ-Ý][a-zà-ÿ]{3,}\b", passo or ""):
        if t in _NAO_NOMES or t in vistos or re.search(r"(ar|er|ir)$", t):
            continue
        vistos.append(t)
    return vistos


def conhecimento_para(texto, heroi, max_termos=4, por_termo=3):
    """Bloco 'O QUE O REPOSITÓRIO JÁ SABE' sobre os nomes do §5. ID: abertura.conhecimento_do_npc.

    Existe porque o Haiku (Plano 035) foi a Lemin, tentou `ask lemin ajuda` e mandou perguntar ao
    autor a palavra de abertura. A cadeia (olhar Lemin, aceitar, responder Merlin) estava no
    conhecimento.md §61. Ler 2.400 linhas não acontece; apontar as seções certas acontece.
    """
    linhas = []
    for termo in termos_do_passo(secao(texto, 5))[:max_termos]:
        secoes, achados, total = sobre(termo, heroi, por_termo)
        if not achados or total > _GENERICO:
            continue
        linhas.append(f"  • {termo} ({total} menções). Leia estas seções do conhecimento.md:")
        linhas += [f"      § {s[:90]}" for s in secoes[:6]]
        linhas += [f"      {a}" for a in achados]
    return linhas


def sequencia_abertura(texto, heroi):
    """Os passos fixos de abertura + a primeira ação, tirada do §5 do plano (PROTOCOLO §1)."""
    passo = secao(texto, 5) or "(o plano não tem §5 — leia o §1 e o §4 e registre isso no próximo plano)"
    if len(passo) > 900:
        passo = passo[:900].rstrip() + " […]"
    linhas = [
        "",
        "=" * 78,
        "SEQUÊNCIA DE ABERTURA — faça nesta ordem (docs/agentes/PROTOCOLO.md §1)",
        "=" * 78,
        "  1. git status --porcelain  e  git log --oneline -5   (há trabalho de outro agente?)",
        f"  2. leia data/heroes/{heroi}/diretiva_de_jogo.md §19 a §23   (give, fala, etapa, ética, ritual)",
        "  3. cota: python scripts/checar_cota.py (Antigravity) ou, no Claude Code, chame get_usage e rode",
        "     python scripts/cota_claude.py --registrar --5h <% usado> --semanal <% usado>   (cota.claude.abertura)",
        "     diária <= 10% ou semanal <= 5%  ->  não jogue: vá ao encerramento (PROTOCOLO §3)",
        "  4. se vai jogar: driver no ar e  python automato/verificar.py  sem FALHA",
        "  5. ao conectar: score tudo  -> confira com o §2 do plano; divergiu? registre antes de agir",
        "     e mantenha o state.json atualizado: jogou sem atualizar, o devolutiva.py reprova",
        "  6. SUA PRIMEIRA AÇÃO (§5 do plano):",
    ]
    linhas += ["       " + l for l in passo.split("\n")]
    saber = conhecimento_para(texto, heroi)
    if saber:
        linhas += ["", "  7. O QUE O REPOSITÓRIO JÁ SABE sobre os nomes do §5 (leia ANTES de falar com NPC):"]
        linhas += saber
        linhas.append("     Mais: python scripts/mandabala.py --sobre <nome>   (NPC, missão, lugar, item)")
    else:
        linhas += ["", "  7. Antes de falar com NPC de missão: python scripts/mandabala.py --sobre <nome>"]
    linhas += [
        "",
        "  Não pergunte ao autor o que o plano ou o conhecimento.md já respondem. Pergunte só em AGENTS #13/#15.",
        "  Para encerrar:  python scripts/encerrar.py --agente \"<modelo/versão>\"",
    ]
    return "\n".join(linhas)


def bloco_ordem(heroi, numero, caminho, campos, proximo):
    plano_rel = caminho.relative_to(ROOT_DIR).as_posix()
    linhas = []
    linhas.append("=" * 78)
    titulo = f"MANDABALA · {heroi} · PLANO {numero:03d}"
    if campos.get("Por"):
        titulo += f" · por {campos['Por']}"
    linhas.append(titulo)
    linhas.append("=" * 78)
    if campos.get("Objetivo"):
        linhas.append(f"Objetivo: {campos['Objetivo']}")
    if campos.get("Criado em"):
        linhas.append(f"Criado em: {campos['Criado em']}")
    if campos.get("Sessão encerrada?"):
        linhas.append(f"Sessão encerrada? {campos['Sessão encerrada?']}")
    linhas.append("")
    linhas.append(f"VOCÊ CONTINUA DE ONDE O PLANO {numero:03d} PAROU — como se fosse quem o escreveu.")
    linhas.append("")
    linhas.append("Leia, nesta ordem:")
    linhas.append("  1. docs/agentes/PROTOCOLO.md                    (a sessão inteira em comandos)")
    linhas.append(f"  2. {plano_rel}   (abaixo, na íntegra)")
    linhas.append("  3. AGENTS.md §4                                 (as invariantes; o resto é consulta)")
    linhas.append(f"  4. data/heroes/{heroi}/diretiva_de_jogo.md §19-§23  (regras de jogo — ANTES de jogar)")
    linhas.append("  O registro_de_evolucao.md é consulta: leia os 3 últimos blocos, não o arquivo todo.")
    linhas.append("")
    linhas.append("Regras que não se negociam:")
    linhas.append(f"  - NÃO edite o plano {numero:03d}. Para encerrar, CRIE o plano {proximo:03d}.")
    linhas.append("  - 'save', nunca 'quit', com missão em andamento — quit apaga o progresso.")
    linhas.append("  - Diga seu modelo/versão no relatório, na evidência e no commit [agente: ...].")
    linhas.append("")
    linhas.append(f"---------- CONTEÚDO INTEGRAL DO PLANO {numero:03d} ----------")
    linhas.append("")
    return "\n".join(linhas)


def main(argv=None):
    if argv is not None:
        # tolera chamada programática com int (ex.: --numero 99 em vez de "99"):
        # o argparse só normaliza strings, e quebra antes de converter.
        argv = [str(a) for a in argv]
    p = argparse.ArgumentParser(
        description="Mostra o plano mais recente do herói e a ordem de leitura para o agente.")
    p.add_argument("--hero", dest="heroi", help="id do herói (padrão: detecta)")
    p.add_argument("--numero", type=int, help="mostra um plano específico em vez do mais alto")
    p.add_argument("--listar", action="store_true", help="lista os planos de todos os heróis")
    p.add_argument("--so-caminho", action="store_true",
                   help="imprime apenas o caminho do plano, para usar em script")
    p.add_argument("--sobre", metavar="TERMO",
                   help="o que conhecimento.md e missoes.json já dizem sobre um NPC, missão ou lugar")
    args = p.parse_args(argv)

    if args.sobre:
        heroi, erro = resolver_heroi(args.heroi)
        if erro:
            print(f"[MANDABALA] {erro}", file=sys.stderr)
            return 1
        secoes, achados, total = sobre(args.sobre, heroi, maximo=20)
        print(f"O que o repositório sabe sobre '{args.sobre}' ({total} menção(ões); mais recentes primeiro):")
        for s in secoes:
            print(f"  § {s}")
        for a in achados:
            print(f"  {a}")
        if not achados:
            print("  nada registrado. Se descobrir algo, grave no conhecimento.md (devolutiva técnica).")
        return 0

    if args.listar:
        disponiveis = heroes_com_planos()
        if not disponiveis:
            print("Nenhum herói tem pasta 'planos/' ainda.", file=sys.stderr)
            return 1
        for heroi in disponiveis:
            achados = planos_de(heroi)
            numeros = [n for n, _ in achados]
            print(f"\n{heroi}  ({len(achados)} plano(s))")
            for numero, caminho in achados:
                campos = cabecalho_do_plano(caminho.read_text(encoding="utf-8", errors="replace"))
                resumo = campos.get("Objetivo", "")
                autor = campos.get("Por", "?")
                print(f"  plano{numero:03d}  {autor:<22} {resumo[:58]}")
            faltando = lacunas(numeros)
            if faltando:
                print(f"  [AVISO] numeração com lacuna: {faltando}")
        print()
        return 0

    heroi, erro = resolver_heroi(args.heroi)
    if erro:
        print(f"[MANDABALA] {erro}", file=sys.stderr)
        return 1

    achados = planos_de(heroi)
    if not achados:
        print(f"[MANDABALA] {heroi} não tem planos em "
              f"{(HEROES_DIR / heroi / 'planos').relative_to(ROOT_DIR).as_posix()}/",
              file=sys.stderr)
        return 1

    numeros = [n for n, _ in achados]
    if args.numero is not None:
        escolhido = next(((n, c) for n, c in achados if n == args.numero), None)
        if not escolhido:
            print(f"[MANDABALA] não existe plano{args.numero:03d} para '{heroi}'. "
                  f"Existem: {', '.join(f'{n:03d}' for n in numeros)}.", file=sys.stderr)
            return 1
        numero, caminho = escolhido
    else:
        numero, caminho = achados[-1]

    if args.so_caminho:
        print(caminho.relative_to(ROOT_DIR).as_posix())
        return 0

    texto = caminho.read_text(encoding="utf-8", errors="replace")
    campos = cabecalho_do_plano(texto)
    proximo = max(numeros) + 1

    print(bloco_ordem(heroi, numero, caminho, campos, proximo))
    print(texto.rstrip())

    faltando = lacunas(numeros)
    if faltando:
        print()
        print(f"[AVISO] a numeração de '{heroi}' tem lacuna: "
              f"{', '.join(f'{n:03d}' for n in faltando)}. "
              "Planos são append-only — lacuna indica arquivo removido ou renomeado.")
    if numero != max(numeros):
        print()
        print(f"[AVISO] este NÃO é o plano mais recente de '{heroi}' "
              f"(o mais alto é {max(numeros):03d}).")
    if not campos.get("Por"):
        print()
        print("[AVISO] o plano não declara autoria ('Por'). O AGENTS.md §6.1 exige modelo/versão.")

    tem_secao, tem_conteudo = devolutiva_tecnica(texto)
    if not tem_secao:
        print()
        print("[AVISO] o plano NÃO tem a seção 'Devolutiva técnica', que é obrigatória no modelo do")
        print("        LEIA.md. O AGENTS.md §5 diz onde cada descoberta vai (mapa.json,")
        print("        maquina/verificacoes.md, conhecimento.md, automato/DECISOES.md). Sem essa seção,")
        print("        a descoberta fica em prosa e não no artefato — foi o que aconteceu no Dia 156,")
        print("        quando a caminhada revelou os anéis do esgoto e o mapa.json não foi tocado.")
    elif not tem_conteudo:
        print()
        print("[AVISO] a seção 'Devolutiva técnica' existe mas está só com o MODELO (placeholders).")
        print("        Preencha, ou escreva 'nada' em cada linha que não se aplica.")

    recentes = transcripts()
    if recentes and sessao_aberta(recentes[-1]):
        print()
        print(f"[AVISO] [sessao.aberta] a última conexão ({recentes[-1].name}) NÃO foi fechada: a")
        print("        personagem pode estar parada no mundo, sem ninguém olhando. ANTES de tudo:")
        print("        se o driver estiver no ar, `play.py \"recall\"` e `play.py \"_CLOSE sleep\"`;")
        print("        se não estiver, conecte, `score tudo`, `recall`, `_CLOSE sleep`. Registre no plano.")

    v2 = checar_plano_v2(texto)
    if v2:
        print()
        print(f"[AVISO] o plano {numero:03d} não cumpre o modelo v2 (LEIA.md). Compense na leitura e")
        print("        NÃO repita isso no seu plano (a partir do "
              f"{PLANO_V2_DESDE:03d} o devolutiva.py reprova):")
        for ident, msg in v2:
            print(f"        - [{ident}] {msg}")

    print(sequencia_abertura(texto, heroi))
    return 0


if __name__ == "__main__":
    sys.exit(main())
