"""CLI de Narração: Transforma os dias da aventura em capítulos de áudio-livro."""

import os
import sys
import json
import argparse
from pathlib import Path

# Adiciona o diretório raiz ao sys.path para imports limpos
BASE_DIR = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(BASE_DIR))

from scripts.tts.preprocessor import prepare_speech_payload
from scripts.tts.engine import get_engine

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

def load_hero_config(hero_id: str) -> dict:
    hero_json_path = BASE_DIR / "data" / "heroes" / hero_id / "hero.json"
    if hero_json_path.exists():
        with open(hero_json_path, "r", encoding="utf-8") as f:
            return json.load(f)
    
    # Fallback para heroes.json geral
    heroes_file = BASE_DIR / "data" / "heroes.json"
    if heroes_file.exists():
        with open(heroes_file, "r", encoding="utf-8") as f:
            heroes = json.load(f)
            for h in heroes:
                if h.get("id") == hero_id:
                    return h
    raise FileNotFoundError(f"Herói '{hero_id}' não encontrado em data/heroes/ ou heroes.json")

def load_hero_posts(hero_id: str) -> list:
    posts_path = BASE_DIR / "data" / "heroes" / hero_id / "posts.json"
    if not posts_path.exists() and hero_id == "antigravitus":
        posts_path = BASE_DIR / "data" / "posts.json"

    if not posts_path.exists():
        raise FileNotFoundError(f"Arquivo de posts não encontrado para o herói '{hero_id}': {posts_path}")

    with open(posts_path, "r", encoding="utf-8") as f:
        return json.load(f)

def main():
    parser = argparse.ArgumentParser(description="Gerador de Narração em Áudio (TTS) para Devil's Bob MUD")
    parser.add_argument("--hero", default="antigravitus", help="ID do herói (ex: antigravitus, grebolius)")
    parser.add_argument("--day", type=int, help="Número do dia/capítulo específico para narrar")
    parser.add_argument("--all", action="store_true", help="Gera todos os capítulos pendentes")
    parser.add_argument("--force", action="store_true", help="Sobrescreve arquivos de áudio já existentes")
    parser.add_argument("--preview", action="store_true", help="Apenas exibe o roteiro prosódico sem gerar áudio")
    parser.add_argument("--list-heroes", action="store_true", help="Lista os heróis configurados e suas vozes")

    args = parser.parse_args()

    if args.list_heroes:
        heroes_dir = BASE_DIR / "data" / "heroes"
        print("\n=== HERÓIS E CONFIGURAÇÕES DE VOZ ===")
        for d in os.listdir(heroes_dir):
            h_path = heroes_dir / d / "hero.json"
            if h_path.exists():
                with open(h_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    voice = data.get("voice", {})
                    print(f"- [{data.get('id')}] {data.get('name')} ({data.get('race_class')})")
                    print(f"  Voz: {voice.get('voice_id', 'Não configurada')} (Rate: {voice.get('rate', '0%')}, Pitch: {voice.get('pitch', '0Hz')})")
                    print(f"  Perfil: {voice.get('description', '')}\n")
        return

    hero = load_hero_config(args.hero)
    voice_config = hero.get("voice", {})
    posts = load_hero_posts(args.hero)

    # Filtra os posts selecionados
    if args.day is not None:
        selected_posts = [p for p in posts if p.get("id") == args.day]
        if not selected_posts:
            print(f"❌ Dia {args.day} não encontrado nas crônicas de {hero.get('name')}.")
            return
    elif args.all:
        selected_posts = posts
    else:
        # Padrão: narra o último capítulo registrado
        selected_posts = [posts[0]] if posts else []

    if not selected_posts:
        print("Nenhum capítulo para processar.")
        return

    output_dir = BASE_DIR / "audio" / args.hero
    output_dir.mkdir(parents=True, exist_ok=True)

    engine_name = voice_config.get("engine", "edge-tts")
    engine = get_engine(engine_name)

    print(f"\n🎙️ Herói: {hero.get('name')} | Voz: {voice_config.get('voice_id')} | Engine: {engine_name}")
    print(f"📁 Diretório de saída: audio/{args.hero}/")

    for post in selected_posts:
        day_id = post.get("id")
        out_file = output_dir / f"dia_{day_id:02d}.mp3"

        payload = prepare_speech_payload(post, voice_config)

        if args.preview:
            print(f"\n--- [PREVIEW: {post.get('day')} - {post.get('title')}] ---")
            print(f"Voice ID: {payload['voice_id']} | Rate: {payload['rate']} | Pitch: {payload['pitch']}")
            print("\nTexto Prosódico para Narração:")
            print(payload["speech_text"])
            continue

        if out_file.exists() and not args.force:
            print(f"⏭️  [PULADO] {out_file.name} já existe (use --force para regravar).")
            continue

        print(f"⏳ Narrando {post.get('day')}: \"{post.get('title')}\"...", end="", flush=True)
        try:
            engine.synthesize(payload, str(out_file))
            size_kb = out_file.stat().st_size / 1024
            print(f" ✅ Pronto! ({size_kb:.1f} KB -> {out_file.name})")
        except Exception as e:
            print(f" ❌ Erro: {e}")

if __name__ == "__main__":
    main()
