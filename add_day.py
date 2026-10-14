import json
import os
import sys
import argparse

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
HEROES_DIR = os.path.join(BASE_DIR, "data", "heroes")
DEFAULT_HERO = "antigravitus"

def get_posts_path(hero_id=DEFAULT_HERO):
    # Se existir a pasta específica do herói, usa ela
    hero_posts = os.path.join(HEROES_DIR, hero_id, "posts.json")
    if os.path.exists(hero_posts) or os.path.exists(os.path.join(HEROES_DIR, hero_id)):
        return hero_posts
    # Fallback legado
    return os.path.join(BASE_DIR, "data", "posts.json")

def add_chronicle(day_num, title, date_str, in_game_time, excerpt, tags, content_paragraphs, day_label=None, hero_id=DEFAULT_HERO):
    """
    Adiciona ou atualiza uma crônica em posts.json do herói selecionado (ordem crescente: Dia 1, Dia 2, ..., Dia N).
    """
    posts_path = get_posts_path(hero_id)
    os.makedirs(os.path.dirname(posts_path), exist_ok=True)

    if os.path.exists(posts_path):
        with open(posts_path, "r", encoding="utf-8") as f:
            posts = json.load(f)
    else:
        posts = []
        
    new_post = {
        "id": int(day_num),
        "day": day_label if day_label else f"Dia {day_num}",
        "title": title,
        "date": date_str,
        "in_game_time": in_game_time,
        "excerpt": excerpt,
        "tags": tags if isinstance(tags, list) else [t.strip() for t in tags.split(",")],
        "content": content_paragraphs if isinstance(content_paragraphs, list) else [content_paragraphs]
    }
    
    # Remove se já existia com o mesmo ID
    posts = [p for p in posts if p.get("id") != int(day_num)]
    
    # Insere e ordena sempre em ordem crescente (Dia 1, Dia 2, Dia 3...)
    posts.append(new_post)
    posts.sort(key=lambda x: x.get("id", 0), reverse=False)
    
    with open(posts_path, "w", encoding="utf-8") as f:
        json.dump(posts, f, ensure_ascii=False, indent=2)
        
    print(f"[{hero_id.upper()}] Crônica do Dia {day_num} ('{title}') gravada em {posts_path}!")
    if int(day_num) % 10 == 0:
        print(f"⏳ MARCO DECENAL ALCANÇADO (Dia {day_num})! Lembre-se de atualizar e sincronizar o mapa interativo: data/heroes/{hero_id}/mapa.json e mapa.md")

    # Se for antigravitus, mantém o data/posts.json legado sincronizado
    if hero_id == "antigravitus":
        legacy_path = os.path.join(BASE_DIR, "data", "posts.json")
        try:
            with open(legacy_path, "w", encoding="utf-8") as f:
                json.dump(posts, f, ensure_ascii=False, indent=2)
        except Exception:
            pass

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Adiciona nova crônica ao diário de um herói.")
    parser.add_argument("--hero", default=DEFAULT_HERO, help="Slug do herói (ex: antigravitus, novo_heroi)")
    parser.add_argument("--day", type=int, help="Número do dia/ciclo (ex: 9)")
    parser.add_argument("--title", help="Título da crônica")
    parser.add_argument("--date", help="Data real (ex: '14 de outubro de 2026')")
    parser.add_argument("--time", help="Tempo no jogo (ex: 'Midgaard — 9º Ciclo')")
    parser.add_argument("--excerpt", help="Resumo/Lead da crônica")
    parser.add_argument("--tags", help="Tags separadas por vírgula")
    args = parser.parse_args()

    if args.day and args.title:
        add_chronicle(
            day_num=args.day,
            title=args.title,
            date_str=args.date or "14 de outubro de 2026",
            in_game_time=args.time or f"Midgaard — {args.day}º Ciclo",
            excerpt=args.excerpt or args.title,
            tags=args.tags.split(",") if args.tags else ["Jornada"],
            content_paragraphs=["Conteúdo registrado via CLI."],
            hero_id=args.hero
        )
    else:
        print("Uso programmatico:")
        print("add_chronicle(day_num, title, date_str, in_game_time, excerpt, tags, content_paragraphs, hero_id='antigravitus')")
        print("Ou via CLI:")
        print("python add_day.py --hero novo_heroi --day 2 --title 'Título' --date '14/10/2026' --tags 'Tag1,Tag2'")
