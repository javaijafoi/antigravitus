"""Cria um rascunho de campanha, sem atribuir acontecimentos ou números não observados."""
import argparse
import json
from pathlib import Path
import re
import shutil
import sys

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
HEROES_DIR = DATA_DIR / "heroes"
HEROES_JSON = DATA_DIR / "heroes.json"


def create_hero(slug, name, race_class="A definir", rune="⚔️", avatar="🛡️",
                title="Aventureiro de Midgaard", quote=None, server="debomud.org:4000"):
    slug = slug.lower().strip().replace(" ", "_")
    if not re.fullmatch(r"[a-z0-9][a-z0-9_-]*", slug) or slug.startswith("_"):
        raise ValueError("Slug deve conter letras minúsculas, números, hífen ou sublinhado, sem caminhos.")
    if not isinstance(name, str) or not name.strip():
        raise ValueError("Nome não pode ser vazio.")
    target = Path(HEROES_DIR) / slug
    catalog = json.loads(Path(HEROES_JSON).read_text(encoding="utf-8-sig")) if Path(HEROES_JSON).is_file() else []
    if not isinstance(catalog, list) or any(not isinstance(hero, dict) for hero in catalog):
        raise ValueError("Catálogo inválido; não foi sobrescrito.")
    if target.exists() or any(hero.get("id") == slug for hero in catalog):
        raise ValueError(f"Herói '{slug}' já existe; seus registros foram preservados.")
    meta = {
        "id": slug, "name": name, "title": title, "rune": rune, "avatar": avatar,
        "race_class": race_class, "role": "A definir", "alignment": "A definir",
        "quote": quote or "Identidade em preparação.",
        "subtitle": f"Campanha de {name} em preparação; nenhuma sessão registrada.",
        "vigilia": "Ponto de partida a observar", "server": server,
        "folder": f"data/heroes/{slug}", "record_status": "draft",
        "evidence_policy": {"legacy_through_day": 0},
        "questions": {f"q{n}": "A definir com o autor da personagem." for n in range(1, 6)},
        "quick_stats": {"level_badge": "(Grau a verificar)", "hp": "Não verificado",
                        "mana": "Não verificado", "mv": "Não verificado", "ac": "Não verificado",
                        "weapon": "Não verificado", "weapon_icon": rune,
                        "sanctuary": "Não verificado"},
        "voice": {"engine": "edge-tts", "voice_id": "pt-BR-AntonioNeural", "rate": "+0%",
                  "pitch": "+0Hz", "style": "default", "description": "Configuração inicial a escolher."},
    }
    staging = target.with_name(f"_creating_{slug}")
    expected_parent = Path(HEROES_DIR).resolve()
    if target.resolve().parent != expected_parent or staging.resolve().parent != expected_parent:
        raise ValueError("Pasta calculada está fora do diretório de heróis.")
    if staging.exists():
        raise ValueError(f"Rascunho de criação já existe em {staging}; confira antes de continuar.")
    staging.mkdir(parents=True)
    try:
        template = Path(HEROES_DIR) / "_template"
        for filename in ("identidade.md", "evolucao.md", "conhecimento.md", "mapa.md", "ficha.md", "mapa.json", "ciclos.json", "missoes.md", "missoes.json", "events.json", "posts.json"):
            src = template / filename
            if not src.is_file():
                continue
            text = src.read_text(encoding="utf-8-sig")
            for placeholder, value in {"NOME": name, "SLUG": slug, "RACA_CLASSE": race_class,
                                       "RUNA": rune, "AVATAR": avatar, "TITULO": title}.items():
                text = text.replace(f"[{placeholder}]", value)
            # Dados estruturados são construídos abaixo para nomes com aspas continuarem JSON válido.
            if src.suffix == ".md":
                (staging / filename).write_text(text, encoding="utf-8")
        files = {
            "hero.json": meta, "posts.json": [], "ciclos.json": [], "events.json": [],
            "missoes.json": {"hero_id": slug, "as_of_day": 0, "items": []},
            "mapa.json": {"hero_id": slug, "hero_name": name, "sanctuary_id": None,
                          "last_updated_day": 0, "last_updated_cycle": "Jornada ainda não iniciada (Dia 0)",
                          "verification": "template", "total_rooms": 0, "layers": [], "zones": [], "rooms": []},
        }
        for filename, value in files.items():
            (staging / filename).write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        staging.rename(target)
        # O catálogo só passa a apontar para a pasta depois que todos os arquivos estão prontos.
        temp_catalog = Path(HEROES_JSON).with_suffix(".json.tmp")
        temp_catalog.write_text(json.dumps(catalog + [meta], ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        temp_catalog.replace(HEROES_JSON)
    except Exception:
        if staging.exists() and staging.resolve().parent == expected_parent:
            shutil.rmtree(staging)
        raise
    print(f"Herói '{name}' criado como rascunho. Nenhum dia, item ou estado de jogo foi inventado.")
    return True


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("slug")
    parser.add_argument("--name", required=True)
    parser.add_argument("--race", default="A definir")
    parser.add_argument("--rune", default="⚔️")
    parser.add_argument("--avatar", default="🛡️")
    parser.add_argument("--title", default="Aventureiro de Midgaard")
    parser.add_argument("--quote")
    args = parser.parse_args()
    try:
        create_hero(args.slug, args.name, args.race, args.rune, args.avatar, args.title, args.quote)
    except (ValueError, OSError) as exc:
        parser.exit(1, f"Erro: {exc}\n")
    return 0


if __name__ == "__main__":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.exit(main())
