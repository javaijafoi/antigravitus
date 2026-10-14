import json
import os
import sys
import argparse
import shutil

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
HEROES_DIR = os.path.join(DATA_DIR, "heroes")
HEROES_JSON = os.path.join(DATA_DIR, "heroes.json")

def create_hero(slug, name, race_class="Guerreiro", rune="⚔️", avatar="🛡️", title="Aventureiro de Midgaard", quote=None, server="debomud.org:4000"):
    slug = slug.lower().strip().replace(" ", "_")
    target_dir = os.path.join(HEROES_DIR, slug)

    if os.path.exists(target_dir):
        print(f"Aviso: O herói '{slug}' já existe em {target_dir}")
        return False

    os.makedirs(target_dir, exist_ok=True)

    # 1. Cria hero.json
    hero_meta = {
        "id": slug,
        "name": name,
        "title": title,
        "rune": rune,
        "avatar": avatar,
        "race_class": race_class,
        "role": f"Desbravador em {title}",
        "alignment": "Neutro",
        "quote": quote or f"“O destino é forjado a cada escolha de {name}.”",
        "subtitle": f"Crônicas diárias de {name} ({race_class}) pelas terras de {server}.",
        "vigilia": "Vigília Ativa: Praça de Midgaard",
        "server": server,
        "folder": f"data/heroes/{slug}"
    }

    with open(os.path.join(target_dir, "hero.json"), "w", encoding="utf-8") as f:
        json.dump(hero_meta, f, ensure_ascii=False, indent=2)

    # 2. Copia ou gera templates base
    template_dir = os.path.join(HEROES_DIR, "novo_heroi")
    for fname in ["identidade.md", "evolucao.md", "conhecimento.md"]:
        src = os.path.join(template_dir, fname)
        dst = os.path.join(target_dir, fname)
        if os.path.exists(src):
            with open(src, "r", encoding="utf-8") as f_in:
                content = f_in.read().replace("Novo Herói", name).replace("[NOME]", name)
            with open(dst, "w", encoding="utf-8") as f_out:
                f_out.write(content)

    # 3. Post inaugural (Dia 1)
    initial_posts = [
        {
            "id": 1,
            "day": "Dia 1",
            "title": f"O Despertar de {name}",
            "date": "14 de outubro de 2026",
            "in_game_time": "Midgaard — 1º Ciclo da Jornada",
            "excerpt": f"Os primeiros passos de {name} sob o céu de Midgaard.",
            "tags": ["O Despertar", "Primeiro Ciclo", race_class],
            "content": [
                f"Meus olhos se abriram para a vastidão de Midgaard. O eco das muralhas e o rumor dos passos na pedra marcaram o início da minha história como {race_class}.",
                "Não há glória sem sacrifício; o primeiro dia é apenas o alicerce de tudo o que ainda está por vir."
            ]
        }
    ]
    with open(os.path.join(target_dir, "posts.json"), "w", encoding="utf-8") as f:
        json.dump(initial_posts, f, ensure_ascii=False, indent=2)

    # 4. Atualiza o catálogo geral heroes.json
    heroes_list = []
    if os.path.exists(HEROES_JSON):
        with open(HEROES_JSON, "r", encoding="utf-8") as f:
            heroes_list = json.load(f)

    # Se já estiver na lista, atualiza; senão, adiciona
    heroes_list = [h for h in heroes_list if h.get("id") != slug]
    heroes_list.append(hero_meta)

    with open(HEROES_JSON, "w", encoding="utf-8") as f:
        json.dump(heroes_list, f, ensure_ascii=False, indent=2)

    print(f"🎉 Herói '{name}' ({slug}) criado com sucesso em: {target_dir}")
    print(f"Catálogo atualizado em: {HEROES_JSON}")
    return True

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Cria a estrutura completa de um novo herói no projeto.")
    parser.add_argument("slug", help="Identificador único (ex: boris, lyra, kaelen)")
    parser.add_argument("--name", required=True, help="Nome de exibição (ex: 'Boris Barba-de-Ferro')")
    parser.add_argument("--race", default="Guerreiro Anão", help="Raça e classe (ex: 'Ladino Humano')")
    parser.add_argument("--rune", default="⚔️", help="Runa/Emoji símbolo")
    parser.add_argument("--avatar", default="🛡️", help="Avatar/Emoji")
    parser.add_argument("--title", default="Aventureiro de Midgaard", help="Título/Alcunha")
    parser.add_argument("--quote", help="Frase de impacto")

    args = parser.parse_args()
    create_hero(
        slug=args.slug,
        name=args.name,
        race_class=args.race,
        rune=args.rune,
        avatar=args.avatar,
        title=args.title,
        quote=args.quote
    )
