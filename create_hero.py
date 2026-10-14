import json
import os
import sys
import argparse
import shutil

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

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

    # 1. Cria hero.json com quick_stats e perguntas base
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
        "folder": f"data/heroes/{slug}",
        "questions": {
            "q1": f"Decifrar os segredos de Midgaard e honrar o caminho de {race_class}.",
            "q2": "A morte anônima e esquecida em sarjetas hostis.",
            "q3": "Impulsividade e excesso de confiança diante de ameaças desconhecidas.",
            "q4": "Sacrifica o conforto e as honras fáceis; jamais sua honra ou verdade.",
            "q5": f"Que o nome de {name} ecoe nas lendas e memórias de Midgaard."
        },
        "quick_stats": {
            "level_badge": f"(Grau 1 • {race_class})",
            "hp": "20 / 20",
            "mana": "50 / 50",
            "mv": "80 / 80",
            "ac": "AC 20",
            "weapon": "Arma de Novato",
            "weapon_icon": rune or "🗡️",
            "sanctuary": "Templo de Midgaard"
        },
        "voice": {
            "engine": "edge-tts",
            "voice_id": "pt-BR-AntonioNeural",
            "rate": "+0%",
            "pitch": "+0Hz",
            "style": "default",
            "description": f"Voz narrativa de {name} ({race_class})"
        }
    }

    with open(os.path.join(target_dir, "hero.json"), "w", encoding="utf-8") as f:
        json.dump(hero_meta, f, ensure_ascii=False, indent=2)

    # 2. Copia e hidrata os templates canônicos de _template
    template_dir = os.path.join(HEROES_DIR, "_template")
    files_to_copy = ["identidade.md", "evolucao.md", "conhecimento.md", "mapa.md", "mapa.json", "ficha.md"]
    for fname in files_to_copy:
        src = os.path.join(template_dir, fname)
        dst = os.path.join(target_dir, fname)
        if os.path.exists(src):
            with open(src, "r", encoding="utf-8") as f_in:
                content = (
                    f_in.read()
                    .replace("[NOME]", name)
                    .replace("[SLUG]", slug)
                    .replace("[RACA_CLASSE]", race_class)
                    .replace("[RUNA]", rune)
                    .replace("[AVATAR]", avatar)
                    .replace("[TITULO]", title)
                )
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

    print(f"[SUCESSO] Herói '{name}' ({slug}) criado com sucesso em: {target_dir}")
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
