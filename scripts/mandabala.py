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
    linhas.append("  1. AGENTS.md                                    (como trabalhar aqui)")
    linhas.append(f"  2. {plano_rel}")
    linhas.append("  3. docs/agentes/registro_de_evolucao.md         (o que mudou na ferramenta)")
    linhas.append(f"  4. data/heroes/{heroi}/diretiva_de_jogo.md      (regras de jogo — ANTES de jogar)")
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
    args = p.parse_args(argv)

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
    return 0


if __name__ == "__main__":
    sys.exit(main())
