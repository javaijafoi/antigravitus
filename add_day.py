"""Registra crônicas reais, com fonte explícita e proteção contra substituição acidental."""
import argparse
import json
import os
from pathlib import Path
import re
import sys
from scripts.check_project import validate_cycles, validate_evidence, validate_posts

BASE_DIR = Path(__file__).resolve().parent
HEROES_DIR = BASE_DIR / "data" / "heroes"
DEFAULT_HERO = "antigravitus"


def hero_directory(hero_id):
    if not isinstance(hero_id, str) or not re.fullmatch(r"[a-z0-9][a-z0-9_-]*", hero_id):
        raise ValueError("Identificador de herói inválido.")
    directory = Path(HEROES_DIR) / hero_id
    if not directory.is_dir():
        raise ValueError(f"Herói '{hero_id}' não encontrado; crie o herói antes de registrar sua jornada.")
    return directory


def get_posts_path(hero_id=DEFAULT_HERO):
    return hero_directory(hero_id) / "posts.json"


def get_ciclos_path(hero_id=DEFAULT_HERO):
    return hero_directory(hero_id) / "ciclos.json"


def read_list(path):
    data = json.loads(path.read_text(encoding="utf-8-sig")) if path.is_file() else []
    if not isinstance(data, list) or any(not isinstance(item, dict) for item in data):
        raise ValueError(f"{path} deve ser lista de objetos; o arquivo existente foi preservado.")
    return data


def write_json(path, value):
    temporary = path.with_name(path.name + ".tmp")
    try:
        temporary.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        os.replace(temporary, path)
    finally:
        if temporary.exists():
            temporary.unlink()


def add_cycle_summary(cycle_num, summary, title=None, hero_id=DEFAULT_HERO, *, replace=False):
    path = get_ciclos_path(hero_id)
    cycles = read_list(path)
    if not isinstance(cycle_num, int) or isinstance(cycle_num, bool) or cycle_num < 1:
        raise ValueError("Número do ciclo deve ser inteiro positivo.")
    posts = read_list(get_posts_path(hero_id))
    days = [p.get("id") for p in posts if isinstance(p.get("id"), int) and not isinstance(p.get("id"), bool)]
    if any(cycle.get("cycle") == cycle_num for cycle in cycles) and not replace:
        raise ValueError(f"Ciclo {cycle_num} já existe. Use --replace somente para uma correção editorial deliberada.")
    item = {"cycle": cycle_num, "start_day": (cycle_num - 1) * 10 + 1, "end_day": cycle_num * 10,
            "title": title or f"Ciclo {cycle_num}", "summary": summary}
    errors, _ = validate_cycles(hero_id, [item], max(days, default=0))
    if errors:
        raise ValueError("\n".join(errors))
    cycles = [cycle for cycle in cycles if cycle.get("cycle") != cycle_num] + [item]
    if any(not isinstance(cycle.get("cycle"), int) for cycle in cycles):
        raise ValueError("Arquivo de ciclos contém IDs inválidos; confira antes de escrever.")
    cycles.sort(key=lambda cycle: cycle["cycle"])
    write_json(path, cycles)
    return item


def add_chronicle(day_num, title, date_str, in_game_time, excerpt, tags, content_paragraphs,
                  day_label=None, hero_id=DEFAULT_HERO, *, evidence=None, source_kind=None, replace=False):
    path = get_posts_path(hero_id)
    posts = read_list(path)
    if not isinstance(day_num, int) or isinstance(day_num, bool) or day_num < 1:
        raise ValueError("Dia deve ser inteiro positivo.")
    if any(post.get("id") == day_num for post in posts) and not replace:
        raise ValueError(f"Dia {day_num} já existe. Use --replace somente para uma correção editorial deliberada.")
    if source_kind not in ("documental", "live"):
        raise ValueError("Informe source_kind='documental' ou 'live'; a origem não deve ser presumida.")
    if isinstance(tags, str):
        tags = [tag.strip() for tag in tags.split(",") if tag.strip()]
    if isinstance(content_paragraphs, str):
        content_paragraphs = [part.strip() for part in re.split(r"\n\s*\n", content_paragraphs) if part.strip()]
    item = {"id": day_num, "day": day_label or f"Dia {day_num}", "title": title, "date": date_str,
            "in_game_time": in_game_time, "excerpt": excerpt, "tags": tags,
            "content": content_paragraphs, "source_kind": source_kind, "evidence": evidence}
    # Um post isolado não permite inferir ordem nem continuidade da coleção.
    errors, _ = validate_posts(hero_id, [item], hero_dir=path.parent)
    errors.extend(validate_evidence(evidence, f"Dia {day_num}", day_num, path.parent))
    if errors:
        raise ValueError("\n".join(dict.fromkeys(errors)))
    posts = [post for post in posts if post.get("id") != day_num] + [item]
    if any(not isinstance(post.get("id"), int) or isinstance(post.get("id"), bool) for post in posts):
        raise ValueError("posts.json contém IDs inválidos; o arquivo existente foi preservado.")
    # Antigravitus conserva sua ordem histórica decrescente; novos heróis usam crescente.
    descending = hero_id == "antigravitus" and len(posts) > 1 and posts[0]["id"] > posts[1]["id"]
    posts.sort(key=lambda post: post["id"], reverse=descending)
    write_json(path, posts)
    legacy = Path(BASE_DIR) / "data" / "posts.json"
    if hero_id == "antigravitus" and legacy.is_file():
        write_json(legacy, posts)
    # O primeiro fato real encerra o estado de template nos dois catálogos.
    local_path = path.parent / "hero.json"
    if local_path.is_file():
        local = json.loads(local_path.read_text(encoding="utf-8-sig"))
        if isinstance(local, dict) and local.get("record_status") == "draft":
            local["record_status"] = "documental"
            catalog_path = Path(BASE_DIR) / "data" / "heroes.json"
            catalog = read_list(catalog_path)
            catalog = [local if hero.get("id") == hero_id else hero for hero in catalog]
            write_json(local_path, local)
            write_json(catalog_path, catalog)
    print(f"[{hero_id}] Crônica do Dia {day_num} registrada com fonte {source_kind}.")
    if day_num % 10 == 0:
        print("Marco decenal: consolide mapa, missões, estado e resumo somente com fatos já observados.")
    return item


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--hero", default=DEFAULT_HERO)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--day", type=int)
    group.add_argument("--cycle", type=int)
    parser.add_argument("--title", required=True)
    parser.add_argument("--date", help="Data real da sessão; não é preenchida com uma data fixa.")
    parser.add_argument("--time", help="Referência temporal real dentro do jogo.")
    parser.add_argument("--excerpt")
    parser.add_argument("--tags", default="Jornada")
    parser.add_argument("--content-file", type=Path, help="UTF-8, com parágrafos separados por linha em branco.")
    parser.add_argument("--evidence-file", type=Path, help="JSON: [{document, day, note}], caminhos relativos à pasta do herói.")
    parser.add_argument("--source-kind", choices=("documental", "live"))
    parser.add_argument("--cycle-summary")
    parser.add_argument("--replace", action="store_true", help="Permite substituir explicitamente um dia ou ciclo existente.")
    args = parser.parse_args()
    try:
        if args.cycle is not None:
            if not args.cycle_summary:
                parser.error("--cycle requer --cycle-summary.")
            add_cycle_summary(args.cycle, args.cycle_summary, args.title, args.hero, replace=args.replace)
        else:
            if not all((args.date, args.time, args.content_file, args.evidence_file, args.source_kind)):
                parser.error("--day requer --date, --time, --content-file, --evidence-file e --source-kind.")
            add_chronicle(args.day, args.title, args.date, args.time, args.excerpt or args.title,
                          args.tags, args.content_file.read_text(encoding="utf-8-sig"), hero_id=args.hero,
                          evidence=json.loads(args.evidence_file.read_text(encoding="utf-8-sig")),
                          source_kind=args.source_kind, replace=args.replace)
    except (ValueError, OSError) as exc:
        parser.exit(1, f"Erro: {exc}\n")
    return 0


if __name__ == "__main__":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.exit(main())
