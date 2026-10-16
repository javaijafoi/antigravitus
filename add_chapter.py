"""Abre, salva partes e fecha capítulos (Season 02+). Fecha por objetivo, não por dia."""
import argparse
import json
import os
from pathlib import Path
import re
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
from scripts.check_project import validate_capitulos, validate_evidence

BASE_DIR = Path(__file__).resolve().parent
HEROES_DIR = BASE_DIR / "data" / "heroes"
KINDS = ("prologo", "missao", "intervalo", "reflexao", "marco")


def hero_dir(hero_id):
    if not isinstance(hero_id, str) or not re.fullmatch(r"[a-z0-9][a-z0-9_-]*", hero_id):
        raise ValueError("Identificador de herói inválido.")
    directory = HEROES_DIR / hero_id
    if not directory.is_dir():
        raise ValueError(f"Herói '{hero_id}' não encontrado.")
    return directory


def load(path, default):
    return json.loads(path.read_text(encoding="utf-8-sig")) if path.is_file() else default


def write(path, value):
    temporary = path.with_name(path.name + ".tmp")
    temporary.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    os.replace(temporary, path)


def chapters_path(hero_id):
    return hero_dir(hero_id) / "capitulos.json"


def read_chapters(hero_id):
    data = load(chapters_path(hero_id), {"schema_version": 1, "hero_id": hero_id, "season": "s02", "tomos": [], "chapters": []})
    if not isinstance(data.get("chapters"), list):
        raise ValueError("capitulos.json inválido; a lista de capítulos não foi encontrada.")
    return data


def max_day(hero_id):
    posts = load(hero_dir(hero_id) / "posts.json", [])
    return max((p["id"] for p in posts if isinstance(p, dict) and isinstance(p.get("id"), int)), default=0)


def next_day(hero_id):
    return max_day(hero_id) + 1


def save_validated(hero_id, data):
    errors, _ = validate_capitulos(hero_id, data, max_day(hero_id), hero_dir(hero_id))
    if errors:
        raise ValueError("\n".join(errors))
    write(chapters_path(hero_id), data)


def open_chapter(hero_id, chapter, title, goal, tomo=1, kind="missao"):
    data = read_chapters(hero_id)
    if kind not in KINDS:
        raise ValueError("kind inválido.")
    existing = next((c for c in data["chapters"] if c.get("id") == chapter), None)
    if existing and existing.get("status") == "concluido":
        raise ValueError(f"Capítulo {chapter} já está concluído; use uma revisão editorial explícita.")
    item = existing or {"id": chapter, "tomo": tomo, "title": title, "kind": kind, "status": "aberto",
                        "goal": goal, "days": [], "parts": [], "content": [], "tags": [],
                        "source_kind": "live", "evidence": []}
    item["tomo"] = tomo
    item["title"] = title or item["title"]
    item["goal"] = goal or item["goal"]
    item["kind"] = kind
    if item["status"] == "aberto":
        item["status"] = "em_curso"
    data["chapters"] = [c for c in data["chapters"] if c.get("id") != chapter] + [item]
    data["chapters"].sort(key=lambda c: c["id"])
    save_validated(hero_id, data)
    print(f"[{hero_id}] Capítulo {chapter} (Tomo {tomo}) em curso: {item['title']} — objetivo: {item['goal']}")
    return item


def add_part(hero_id, chapter, day, summary, evidence, source_kind="live", date=None):
    day = day if day is not None else next_day(hero_id)
    data = read_chapters(hero_id)
    item = next((c for c in data["chapters"] if c.get("id") == chapter), None)
    if not item:
        raise ValueError(f"Capítulo {chapter} não existe; abra-o antes de salvar partes.")
    part = {"day": day, "summary": summary, "source_kind": source_kind, "evidence": evidence}
    if date:
        part["date"] = date
    item.setdefault("parts", []).append(part)
    days = set(item.get("days", [])) | {day}
    item["days"] = sorted(days)
    item["status"] = "em_curso"
    save_validated(hero_id, data)
    print(f"[{hero_id}] Parte do Dia {day} salva no capítulo {chapter} (o capítulo segue aberto até o objetivo ser cumprido).")
    return item


def close_chapter(hero_id, chapter, content, excerpt, tags, evidence, source_kind="live", day=None, date=None, in_game_time=None):
    data = read_chapters(hero_id)
    item = next((c for c in data["chapters"] if c.get("id") == chapter), None)
    if not item:
        raise ValueError(f"Capítulo {chapter} não existe.")
    item["content"] = content
    if excerpt:
        item["excerpt"] = excerpt
    if tags:
        item["tags"] = tags
    if date:
        item["date"] = date
    if in_game_time:
        item["in_game_time"] = in_game_time
    item["source_kind"] = source_kind
    if evidence:
        item["evidence"] = evidence
    item["status"] = "concluido"
    item["closed_on_day"] = day if day is not None else next_day(hero_id) - 1
    save_validated(hero_id, data)
    print(f"[{hero_id}] Capítulo {chapter} CONCLUÍDO no Dia {item['closed_on_day']}: {item.get('title')}")
    return item


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--hero", default="grebolius")
    parser.add_argument("--chapter", type=int, required=True)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--part", action="store_true")
    mode.add_argument("--close", action="store_true")
    parser.add_argument("--tomo", type=int, default=1)
    parser.add_argument("--title")
    parser.add_argument("--goal")
    parser.add_argument("--kind", default="missao")
    parser.add_argument("--summary")
    parser.add_argument("--day", type=int)
    parser.add_argument("--date")
    parser.add_argument("--in-game-time", dest="in_game_time")
    parser.add_argument("--excerpt")
    parser.add_argument("--tags", default="")
    parser.add_argument("--content-file", type=Path)
    parser.add_argument("--evidence-file", type=Path)
    parser.add_argument("--source-kind", choices=("documental", "live"), default="live")
    args = parser.parse_args()
    try:
        if args.close:
            if not args.content_file:
                parser.error("--close exige --content-file (a crônica do capítulo).")
            if not args.evidence_file:
                parser.error("--close exige --evidence-file.")
            content = args.content_file.read_text(encoding="utf-8-sig")
            content = [p.strip() for p in re.split(r"\n\s*\n", content) if p.strip()]
            evidence = json.loads(args.evidence_file.read_text(encoding="utf-8-sig"))
            tags = [t.strip() for t in args.tags.split(",") if t.strip()]
            close_chapter(args.hero, args.chapter, content, args.excerpt, tags, evidence,
                          args.source_kind, args.day, args.date, args.in_game_time)
        elif args.part:
            if not args.summary or not args.evidence_file:
                parser.error("--part exige --summary e --evidence-file.")
            evidence = json.loads(args.evidence_file.read_text(encoding="utf-8-sig"))
            add_part(args.hero, args.chapter, args.day, args.summary, evidence, args.source_kind, args.date)
        else:
            if not args.title or not args.goal:
                parser.error("abrir um capítulo exige --title e --goal.")
            open_chapter(args.hero, args.chapter, args.title, args.goal, args.tomo, args.kind)
    except (ValueError, OSError) as exc:
        parser.exit(1, f"Erro: {exc}\n")
    return 0


if __name__ == "__main__":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.exit(main())
