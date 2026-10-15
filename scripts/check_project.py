#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Validador de Integridade Pré-Commit do Projeto Crônicas MUD.
Garante a consistência entre JSONs, ordenação de posts, sincronia de fichas e diretrizes de projeto.
"""

import sys
import os
import json
import re

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DATA_DIR = os.path.join(ROOT_DIR, "data")
HEROES_FILE = os.path.join(DATA_DIR, "heroes.json")

# Suporte robusto a UTF-8 no console Windows
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")

def print_header(title):
    print(f"\n{'=' * 60}\n🔍 {title}\n{'=' * 60}")

def check_json_file(file_path):
    rel_path = os.path.relpath(file_path, ROOT_DIR)
    if not os.path.exists(file_path):
        return None, [f"Arquivo não encontrado: {rel_path}"]
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data, []
    except json.JSONDecodeError as e:
        return None, [f"JSON inválido em {rel_path}: {e}"]
    except Exception as e:
        return None, [f"Erro lendo {rel_path}: {e}"]

def validate_posts(hero_id, posts):
    errors = []
    warnings = []
    required_keys = ["id", "day", "title", "date", "in_game_time", "excerpt", "tags", "content"]

    if not isinstance(posts, list):
        errors.append(f"posts.json de '{hero_id}' deve ser uma lista JSON.")
        return errors, warnings

    if not posts:
        warnings.append(f"posts.json de '{hero_id}' está vazio.")
        return errors, warnings

    # Determina a direção esperada da ordenação
    is_ascending = True
    if len(posts) >= 2 and posts[0].get("id", 0) > posts[1].get("id", 0):
        is_ascending = False
        if hero_id != "antigravitus":
            errors.append(f"posts.json de '{hero_id}' está em ordem decrescente; a norma do projeto é estritamente crescente (Dia 1, Dia 2, ...).")

    prev_id = None
    seen_ids = set()

    for idx, post in enumerate(posts):
        post_id = post.get("id")
        title = post.get("title", f"Post sem título #{idx}")

        # Checagem de chaves obrigatórias
        missing = [k for k in required_keys if k not in post]
        if missing:
            errors.append(f"Post #{post_id or idx} ({title}) de '{hero_id}' está sem campos obrigatórios: {missing}")

        # Checagem de conteúdo
        content = post.get("content")
        if not isinstance(content, list) or len(content) == 0:
            errors.append(f"Post #{post_id} ({title}) de '{hero_id}' possui 'content' vazio ou não é lista.")

        # Checagem de IDs e ordenação estrita
        if post_id is not None:
            if not isinstance(post_id, int):
                errors.append(f"Post na posição {idx} de '{hero_id}' possui id não-inteiro: {post_id}")
            else:
                if post_id in seen_ids:
                    errors.append(f"ID duplicado #{post_id} encontrado em '{hero_id}'.")
                if prev_id is not None:
                    if is_ascending and post_id <= prev_id:
                        errors.append(f"Ordenação incorreta em '{hero_id}': ID #{post_id} veio após #{prev_id} (esperado crescente).")
                    elif not is_ascending and post_id >= prev_id:
                        errors.append(f"Ordenação incorreta em '{hero_id}': ID #{post_id} veio após #{prev_id} (esperado decrescente).")
                seen_ids.add(post_id)
                prev_id = post_id

    # Alerta de metajogo em títulos dos últimos 3 posts
    for post in posts[-3:]:
        title = post.get("title", "")
        if re.search(r"\b\d+[\.,]?\d*\s*(EXP|XP)\b", title, re.IGNORECASE):
            warnings.append(f"Post #{post.get('id')} em '{hero_id}': Título '{title}' contém menção explícita de EXP (viola regra de zero metajogo em prosa).")

    return errors, warnings

def validate_hero_sync(hero_entry):
    errors = []
    warnings = []
    hero_id = hero_entry.get("id")
    hero_dir = os.path.join(DATA_DIR, "heroes", hero_id)
    hero_json_path = os.path.join(hero_dir, "hero.json")

    if not os.path.exists(hero_dir):
        errors.append(f"Diretório do herói não encontrado: data/heroes/{hero_id}")
        return errors, warnings

    hero_json, json_errs = check_json_file(hero_json_path)
    if json_errs:
        errors.extend(json_errs)
        return errors, warnings

    # Validar campos de quick_stats sincronizados
    qs_main = hero_entry.get("quick_stats", {})
    qs_local = hero_json.get("quick_stats", {})

    compare_keys = ["hp", "mana", "mv", "ac", "sanctuary", "level_badge", "weapon"]
    for key in compare_keys:
        val_main = qs_main.get(key)
        val_local = qs_local.get(key)
        if val_main != val_local:
            errors.append(f"Dessincronia em quick_stats.{key} para '{hero_id}': heroes.json='{val_main}' vs hero.json='{val_local}'")

    # Validar ficha.md se existir
    ficha_path = os.path.join(hero_dir, "ficha.md")
    if os.path.exists(ficha_path):
        try:
            with open(ficha_path, "r", encoding="utf-8") as f:
                ficha_text = f.read()

            # Extrair HP máximo
            hp_match = re.search(r"Pontos de Vida \(HP\)\s*\|\s*(\d+)\s*\|\s*(\d+)", ficha_text)
            wimpy_match = re.search(r"Configuração de Fuga \(Wimpy\):\*\*\s*(\d+)\s*HP", ficha_text)

            if hp_match and wimpy_match:
                hp_max = int(hp_match.group(2))
                wimpy_val = int(wimpy_match.group(1))
                expected_wimpy = int(hp_max * 0.25)
                # Aceita margem de +-1 devido a arredondamento
                if abs(wimpy_val - expected_wimpy) > 1:
                    warnings.append(f"Ficha de '{hero_id}': Wimpy configurado ({wimpy_val} HP) diverge de 25% do HP máximo ({hp_max} HP -> esperado ~{expected_wimpy} HP).")

            # Alerta de treinos pendentes
            train_match = re.search(r"(\d+)\s*sessões de treino acumuladas", ficha_text)
            if train_match:
                train_count = int(train_match.group(1))
                if train_count > 0:
                    warnings.append(f"Ficha de '{hero_id}': Há {train_count} sessões de treino acumuladas prontas para uso na guilda.")

        except Exception as e:
            warnings.append(f"Erro ao analisar ficha.md de '{hero_id}': {e}")

    # Validar missoes.md se existir
    missoes_path = os.path.join(hero_dir, "missoes.md")
    if os.path.exists(missoes_path):
        try:
            with open(missoes_path, "r", encoding="utf-8") as f:
                missoes_text = f.read()
            if "▶️" not in missoes_text and "✅" not in missoes_text and "🔎" not in missoes_text:
                warnings.append(f"Catálogo de missões de '{hero_id}' sem ícones canônicos de status (🔎, ▶️, ✅).")
        except Exception as e:
            warnings.append(f"Erro ao ler missoes.md de '{hero_id}': {e}")

    return errors, warnings

def main():
    print_header("Executando Verificação Pré-Commit do Projeto Crônicas MUD")
    all_errors = []
    all_warnings = []

    # 1. Validar heroes.json
    heroes_data, errs = check_json_file(HEROES_FILE)
    if errs:
        all_errors.extend(errs)
    else:
        if not isinstance(heroes_data, list):
            all_errors.append("data/heroes.json deve ser uma lista JSON.")
        else:
            print(f"✓ data/heroes.json válido ({len(heroes_data)} heróis configurados).")
            for hero in heroes_data:
                h_errs, h_warns = validate_hero_sync(hero)
                all_errors.extend(h_errs)
                all_warnings.extend(h_warns)

                hero_id = hero.get("id")
                # Validar posts.json do herói
                posts_path = os.path.join(DATA_DIR, "heroes", hero_id, "posts.json")
                posts_data, p_errs = check_json_file(posts_path)
                if p_errs:
                    all_errors.extend(p_errs)
                elif posts_data:
                    p_val_errs, p_val_warns = validate_posts(hero_id, posts_data)
                    all_errors.extend(p_val_errs)
                    all_warnings.extend(p_val_warns)
                    print(f"✓ posts.json de '{hero_id}' verificado ({len(posts_data)} crônicas).")

                # Validar ciclos.json se existir
                ciclos_path = os.path.join(DATA_DIR, "heroes", hero_id, "ciclos.json")
                if os.path.exists(ciclos_path):
                    _, c_errs = check_json_file(ciclos_path)
                    if c_errs:
                        all_errors.extend(c_errs)
                    else:
                        print(f"✓ ciclos.json de '{hero_id}' válido.")

                # Validar mapa.json se existir
                mapa_path = os.path.join(DATA_DIR, "heroes", hero_id, "mapa.json")
                if os.path.exists(mapa_path):
                    _, m_errs = check_json_file(mapa_path)
                    if m_errs:
                        all_errors.extend(m_errs)
                    else:
                        print(f"✓ mapa.json de '{hero_id}' válido.")

    # Relatório final
    if all_warnings:
        print("\n⚠️ AVISOS ENCONTRADOS:")
        for w in all_warnings:
            print(f"  [AVISO] {w}")

    if all_errors:
        print("\n❌ ERROS CRÍTICOS ENCONTRADOS:")
        for e in all_errors:
            print(f"  [ERRO] {e}")
        print("\n🚫 Validação FALHOU! Corrija os erros acima antes de efetuar commit.")
        sys.exit(1)

    print("\n✨ Todos os testes passaram com sucesso! Projeto íntegro para commit e deploy.")
    sys.exit(0)

if __name__ == "__main__":
    main()
