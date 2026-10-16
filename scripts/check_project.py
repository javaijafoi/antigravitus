#!/usr/bin/env python3
"""Confere registros documentais; não certifica mecânicas nem estado ao vivo do MUD."""
import argparse
import json
import re
import sys
from pathlib import Path

for _stream in (sys.stdout, sys.stderr):
    if hasattr(_stream, "reconfigure"):
        _stream.reconfigure(encoding="utf-8", errors="replace")

ROOT_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT_DIR / "data"
HEROES_FILE = DATA_DIR / "heroes.json"
SLUG = re.compile(r"[a-z0-9][a-z0-9_-]*\Z")
META = re.compile(r"\b(?:\d+[.,]?\d*\s*(?:XP|EXP|HP|MP|MV|%|pontos de (?:mana|dano|experiência))|(?:mana|armadura|dano|experiência)\s*[:=]\s*\d+|passos de (?:maturidade|experiência)|pontos de (?:mana|couraça|experiência)|pontos acumulados)", re.I)


def integer(value, minimum=0):
    return isinstance(value, int) and not isinstance(value, bool) and value >= minimum


def nonempty(value):
    return isinstance(value, str) and bool(value.strip())


def documented_day(value):
    if not isinstance(value, str):
        return None
    span = re.search(r"Dias\s+(\d+)\s*[-–—]\s*(\d+)", value, re.I)
    if span:
        return int(span.group(2))
    match = re.search(r"Dia\s+(\d+)", value, re.I)
    return int(match.group(1)) if match else None


def check_json_file(file_path):
    try:
        return json.loads(Path(file_path).read_text(encoding="utf-8-sig")), []
    except (OSError, UnicodeError, ValueError) as exc:
        return None, [f"Não foi possível ler {file_path}: {exc}"]


def validate_evidence(evidence, context, max_day, hero_dir=None, bound=True):
    errors = []
    if not isinstance(evidence, list) or not evidence:
        return [f"{context}: evidence deve ser uma lista não vazia de fontes."]
    for ref in evidence:
        if not isinstance(ref, dict) or not nonempty(ref.get("document")):
            errors.append(f"{context}: fonte precisa de document (arquivo ou registro da observação).")
            continue
        document = ref["document"]
        path = Path(document)
        if path.is_absolute() or ".." in path.parts or ":" in document or "\\" in document:
            errors.append(f"{context}: document deve ser um caminho relativo dentro da pasta do herói.")
        elif hero_dir is not None and not (Path(hero_dir) / path).is_file():
            errors.append(f"{context}: fonte documental não encontrada: {document}.")
        day = ref.get("day")
        if day is not None and (not integer(day, 1) or (bound and day > max_day)):
            errors.append(f"{context}: evidência aponta para dia inválido ou futuro: {day} (limite {max_day}).")
    return errors


def validate_posts(hero_id, posts, allow_empty=False, hero_dir=None, legacy_through_day=None):
    errors, warnings = [], []
    if not isinstance(posts, list):
        return [f"posts.json de '{hero_id}' deve ser uma lista."], warnings
    if not posts:
        if not allow_empty:
            errors.append(f"posts.json de '{hero_id}' está vazio; somente record_status='draft' permite uma jornada ainda não iniciada.")
        return errors, warnings
    ids, previous, historical, metagame = set(), None, [], []
    valid_ids = [p.get("id") for p in posts if isinstance(p, dict) and integer(p.get("id"), 1)]
    descending = len(valid_ids) >= 2 and valid_ids[0] > valid_ids[1]
    if descending and hero_id != "antigravitus":
        errors.append(f"posts.json de '{hero_id}' deve estar em ordem crescente.")
    for index, post in enumerate(posts):
        context = f"{hero_id}/posts.json, posição {index + 1}"
        if not isinstance(post, dict):
            errors.append(f"{context}: post deve ser objeto.")
            continue
        day = post.get("id")
        if not integer(day, 1):
            errors.append(f"{context}: id deve ser inteiro positivo.")
        else:
            if day in ids:
                errors.append(f"{context}: ID duplicado {day}.")
            if previous is not None and ((descending and day >= previous) or (not descending and day <= previous)):
                errors.append(f"{context}: ordem de IDs incorreta ({previous} → {day}).")
            ids.add(day)
            previous = day
            if post.get("day") != f"Dia {day}":
                errors.append(f"{context}: day deve ser 'Dia {day}'.")
        for key in ("day", "title", "date", "in_game_time", "excerpt"):
            if not nonempty(post.get(key)):
                errors.append(f"{context}: {key} precisa de texto não vazio.")
        content = post.get("content")
        if not isinstance(content, list) or not content or any(not nonempty(p) for p in content):
            errors.append(f"{context}: content precisa de parágrafos reais não vazios.")
        elif any(p.strip() == "Conteúdo registrado via CLI." for p in content):
            errors.append(f"{context}: conteúdo automático de preenchimento não é uma crônica.")
        tags = post.get("tags")
        if not isinstance(tags, list) or any(not nonempty(tag) for tag in tags):
            errors.append(f"{context}: tags deve ser lista de textos.")
        if "evidence" in post:
            errors.extend(validate_evidence(post["evidence"], context, day if integer(day, 1) else 0, hero_dir))
            if post.get("source_kind") not in ("documental", "live"):
                errors.append(f"{context}: source_kind deve ser 'documental' ou 'live'.")
        else:
            historical.append(day)
            if legacy_through_day is not None and integer(day, 1) and day > legacy_through_day:
                errors.append(f"{context}: Dia {day} posterior ao legado (Dia {legacy_through_day}) precisa de evidence e source_kind explícitos.")
        prose = [post.get("title"), post.get("excerpt")]
        if isinstance(content, list):
            prose += content
        if any(META.search(value) for value in prose if isinstance(value, str)):
            metagame.append(day)
    if ids and ids != set(range(1, max(ids) + 1)):
        warnings.append(f"'{hero_id}': há lacunas nos dias; conferir se são ausências documentais deliberadas.")
    if historical:
        warnings.append(f"'{hero_id}': {len(historical)} crônicas legadas sem evidence estruturada; preservadas como documentação histórica, sem certificação ao vivo.")
    if metagame:
        warnings.append(f"'{hero_id}': possível metajogo em {len(metagame)} crônicas (dias {', '.join(map(str, sorted(d for d in metagame if integer(d))))}); revisão editorial, sem reescrita automática.")
    return errors, warnings


def parse_ficha(text):
    """Aceita Markdown com e sem negrito; devolve também campos não interpretados."""
    plain = text.replace("**", "").replace("`", "")
    values = {}
    for key, label in (("hp", r"Pontos de Vida \(HP\)"), ("mana", r"Pontos de Mana \(MP\)"), ("mv", r"Estamina\s*/\s*Movimento \(MV\)")):
        match = re.search(label + r"\s*\|\s*(\d+)\s*\|\s*(\d+)", plain, re.I)
        values[key] = tuple(map(int, match.groups())) if match else None
    for key, pattern in {
        "wimpy": r"Configuração de Fuga \(Wimpy\):\s*(\d+)",
        "level": r"Grau\s*/\s*Nível Atual:\s*(\d+)",
        "gold": r"Ouro Líquido:\s*([\d.]+)",
        "experience": r"Experiência Acumulada:\s*([\d.]+)",
        "training_sessions": r"Sessões de Treino Disponíveis:\s*(\d+)",
    }.items():
        match = re.search(pattern, plain, re.I)
        values[key] = int(match.group(1).replace(".", "")) if match else None
    if values["training_sessions"] is None:
        match = re.search(r"(\d+)\s*sessões de treino acumuladas", plain, re.I)
        values["training_sessions"] = int(match.group(1)) if match else None
    return values


def validate_state(hero_id, state, max_day, hero_dir=None):
    errors, warnings = [], []
    context = f"'{hero_id}'/state.json"
    if not isinstance(state, dict):
        return [f"{context}: deve ser objeto."], warnings
    if state.get("schema_version") != 1 or state.get("hero_id") != hero_id:
        errors.append(f"{context}: schema_version=1 e hero_id correspondente são obrigatórios.")
    as_of = state.get("as_of")
    if not isinstance(as_of, dict):
        errors.append(f"{context}: as_of deve informar day, source, verification e live_verified.")
    else:
        if not integer(as_of.get("day")) or as_of["day"] > max_day:
            errors.append(f"{context}: as_of.day inválido ou futuro (limite {max_day}).")
        if not nonempty(as_of.get("source")) or as_of.get("verification") not in ("documental", "live") or not isinstance(as_of.get("live_verified"), bool):
            errors.append(f"{context}: origem e tipo de verificação devem ser explícitos.")
        if as_of.get("verification") == "documental" and as_of.get("live_verified") is not False:
            errors.append(f"{context}: revisão documental não pode afirmar live_verified=true.")
        if as_of.get("live_verified") is False:
            warnings.append(f"'{hero_id}': estado documental do Dia {as_of.get('day')}; confirmar em jogo antes da próxima expedição.")
    for key in ("level", "gold", "wimpy", "training_sessions"):
        if not integer(state.get(key), 1 if key == "level" else 0):
            errors.append(f"{context}: {key} deve ser inteiro válido.")
    if not nonempty(state.get("mechanical_class")):
        errors.append(f"{context}: mechanical_class deve distinguir mecânica de estilo narrativo.")
    vitals = state.get("vitals")
    if not isinstance(vitals, dict):
        errors.append(f"{context}: vitals deve ser objeto.")
    else:
        for key in ("hp", "mana", "mv"):
            value = vitals.get(key)
            if not isinstance(value, dict) or not integer(value.get("current")) or not integer(value.get("max"), 1) or value["current"] > value["max"]:
                errors.append(f"{context}: vitals.{key} deve ter 0 <= current <= max, max positivo.")
    experience = state.get("experience")
    if not isinstance(experience, dict) or not integer(experience.get("current")) or not integer(experience.get("next_level")):
        errors.append(f"{context}: experience.current e next_level devem ser inteiros não negativos.")
    armor = state.get("armor")
    if not isinstance(armor, dict) or any(not isinstance(armor.get(key), int) or isinstance(armor.get(key), bool) for key in ("base", "with_armor")) or not isinstance(armor.get("effect_verified"), bool):
        errors.append(f"{context}: armor precisa de base, with_armor e effect_verified booleano.")
    for key in ("skills", "equipment"):
        items = state.get(key)
        if not isinstance(items, list) or any(not isinstance(item, dict) or not nonempty(item.get("name")) for item in items):
            errors.append(f"{context}: {key} deve ser lista de objetos nomeados.")
        elif key == "skills":
            for item in items:
                if not nonempty(item.get("id")) or not integer(item.get("proficiency")) or item["proficiency"] > 100:
                    errors.append(f"{context}: habilidade precisa de id e proficiency entre 0 e 100.")
                if isinstance(item.get("source"), dict):
                    errors.extend(validate_evidence([item["source"]], context, max_day, hero_dir))
    inventory = state.get("inventory")
    if not isinstance(inventory, dict) or any(not isinstance(inventory.get(key), list) for key in ("recorded", "pending_verification")):
        errors.append(f"{context}: inventory deve separar recorded de pending_verification.")
    elif any(not isinstance(item, dict) or not nonempty(item.get("name")) for key in ("recorded", "pending_verification") for item in inventory[key]):
        errors.append(f"{context}: itens do inventário precisam de nome.")
    else:
        for item in inventory["pending_verification"]:
            day = item.get("last_seen_day")
            if day is not None and (not integer(day, 1) or day > max_day):
                errors.append(f"{context}: last_seen_day inválido ou futuro.")
    for key in ("location", "camp", "sanctuary"):
        value = state.get(key)
        if not isinstance(value, dict) or not nonempty(value.get("name")) or (value.get("room_id") is not None and not nonempty(value["room_id"])):
            errors.append(f"{context}: {key} deve ter name e room_id textual ou nulo.")
    return errors, warnings


def validate_map(hero_id, data, max_day, state=None):
    errors, warnings = [], []
    context = f"'{hero_id}'/mapa.json"
    if not isinstance(data, dict) or not isinstance(data.get("rooms"), list):
        return [f"{context}: objeto com lista rooms obrigatório."], warnings
    rooms = data["rooms"]
    if data.get("hero_id") != hero_id:
        errors.append(f"{context}: hero_id incorreto.")
    if not integer(data.get("total_rooms")) or data["total_rooms"] != len(rooms):
        errors.append(f"{context}: total_rooms diverge da lista de salas.")
    layers = data.get("layers")
    if not isinstance(layers, list) or any(not isinstance(layer, dict) or not nonempty(layer.get("id")) for layer in layers):
        errors.append(f"{context}: layers deve conter objetos com id.")
        layer_ids = set()
    else:
        layer_ids = {layer["id"] for layer in layers}
        if len(layer_ids) != len(layers):
            errors.append(f"{context}: ID de camada duplicado.")
    ids = set()
    for room in rooms:
        if not isinstance(room, dict) or not nonempty(room.get("id")):
            errors.append(f"{context}: sala precisa de id textual.")
            continue
        if room["id"] in ids:
            errors.append(f"{context}: ID de sala duplicado: {room['id']}.")
        ids.add(room["id"])
    for room in rooms:
        if not isinstance(room, dict):
            continue
        room_id = room.get("id", "?")
        layer = room.get("layer")
        if not isinstance(layer, str) or layer not in layer_ids:
            errors.append(f"{context}: sala {room_id} em camada inexistente.")
        exits = room.get("exits")
        if not isinstance(exits, dict):
            errors.append(f"{context}: exits de {room_id} deve ser objeto.")
        else:
            for direction, target in exits.items():
                if not nonempty(target) or target not in ids:
                    errors.append(f"{context}: saída {room_id}/{direction} aponta para sala inexistente: {target}.")
        discovery = room.get("discovered_in", "")
        day_match = re.search(r"Dia\s+(\d+)", discovery, re.I) if isinstance(discovery, str) else None
        if day_match and int(day_match.group(1)) > max_day:
            errors.append(f"{context}: descoberta de {room_id} está no futuro.")
    for field in ("sanctuary_id", "current_location_id", "camp_id"):
        target = data.get(field)
        if target is not None and (not isinstance(target, str) or target not in ids):
            errors.append(f"{context}: {field} aponta para sala inexistente.")
    if isinstance(state, dict):
        for state_key, map_key in (("sanctuary", "sanctuary_id"), ("location", "current_location_id"), ("camp", "camp_id")):
            value = state.get(state_key)
            if isinstance(value, dict) and nonempty(value.get("room_id")):
                if value["room_id"] not in ids:
                    errors.append(f"{context}: state.{state_key}.room_id não existe no mapa.")
                if data.get(map_key) != value["room_id"]:
                    errors.append(f"{context}: {map_key} diverge de state.{state_key}.room_id.")
    day = data.get("last_updated_day")
    if day is None:
        text = data.get("last_updated_cycle", "")
        day = documented_day(text)
    if not integer(day) or day > max_day:
        errors.append(f"{context}: atualização sem dia interpretável ou no futuro (limite {max_day}).")
    elif day < (max_day // 10) * 10:
        warnings.append(f"{context}: consolidado no Dia {day}; último marco documental é Dia {(max_day // 10) * 10}.")
    return errors, warnings


def validate_cycles(hero_id, cycles, max_day):
    errors, warnings, seen = [], [], set()
    if not isinstance(cycles, list):
        return [f"'{hero_id}'/ciclos.json deve ser lista."], warnings
    for cycle in cycles:
        if not isinstance(cycle, dict):
            errors.append(f"'{hero_id}': resumo de ciclo deve ser objeto.")
            continue
        num, start, end = (cycle.get(key) for key in ("cycle", "start_day", "end_day"))
        if not all(integer(value, 1) for value in (num, start, end)):
            errors.append(f"'{hero_id}': ciclo e limites devem ser inteiros positivos.")
            continue
        if num in seen:
            errors.append(f"'{hero_id}': ciclo {num} duplicado.")
        seen.add(num)
        if start != (num - 1) * 10 + 1 or end != num * 10:
            errors.append(f"'{hero_id}': limites incorretos do ciclo {num}.")
        if end > max_day:
            errors.append(f"'{hero_id}': ciclo {num} resume dias futuros ({end} > {max_day}); planos pertencem ao plano de aventura.")
        for key in ("title", "summary"):
            if not nonempty(cycle.get(key)):
                errors.append(f"'{hero_id}': ciclo {num} sem {key}.")
    return errors, warnings


def validate_missions(hero_id, missions, max_day, hero_dir=None):
    errors, warnings = [], []
    if not isinstance(missions, dict) or not isinstance(missions.get("items"), list):
        return [f"'{hero_id}'/missoes.json deve conter lista items."], warnings
    if missions.get("hero_id") != hero_id or not integer(missions.get("as_of_day")) or missions["as_of_day"] > max_day:
        errors.append(f"'{hero_id}'/missoes.json: hero_id ou as_of_day inválido.")
    ids = set()
    for item in missions["items"]:
        if not isinstance(item, dict) or not nonempty(item.get("id")):
            errors.append(f"'{hero_id}': missão sem id textual.")
            continue
        if item["id"] in ids:
            errors.append(f"'{hero_id}': missão duplicada {item['id']}.")
        ids.add(item["id"])
        if item.get("type") not in ("official", "investigation", "personal") or item.get("status") not in ("discovered", "active", "completed", "blocked", "deferred", "abandoned"):
            errors.append(f"'{hero_id}': tipo ou status inválido em {item['id']}.")
        for key in ("title", "objective", "next_step"):
            if not nonempty(item.get(key)):
                errors.append(f"'{hero_id}': missão {item['id']} precisa de {key}.")
        for key in ("accepted_day", "last_progress_day"):
            day = item.get(key)
            if day is not None and (not integer(day, 1) or day > max_day):
                errors.append(f"'{hero_id}': {item['id']}.{key} inválido ou futuro.")
        if integer(item.get("accepted_day"), 1) and integer(item.get("last_progress_day"), 1) and item["last_progress_day"] < item["accepted_day"]:
            errors.append(f"'{hero_id}': progresso de {item['id']} anterior ao aceite.")
        errors.extend(validate_evidence(item.get("evidence"), f"{hero_id}/missão {item['id']}", max_day, hero_dir))
    return errors, warnings


CHAPTER_KINDS = ("prologo", "missao", "intervalo", "reflexao", "marco")
CHAPTER_STATUS = ("aberto", "em_curso", "concluido")


def validate_temporadas(hero_id, data, max_day, hero_dir=None):
    errors, warnings = [], []
    context = f"'{hero_id}'/temporadas.json"
    if not isinstance(data, dict) or not isinstance(data.get("seasons"), list) or not data["seasons"]:
        return [f"{context}: objeto com lista seasons não vazia é obrigatório."], warnings
    if data.get("hero_id") != hero_id or data.get("schema_version") != 1:
        errors.append(f"{context}: schema_version=1 e hero_id correspondente são obrigatórios.")
    ids = set()
    for season in data["seasons"]:
        if not isinstance(season, dict) or not nonempty(season.get("id")):
            errors.append(f"{context}: temporada precisa de id textual.")
            continue
        if season["id"] in ids:
            errors.append(f"{context}: temporada duplicada {season['id']}.")
        ids.add(season["id"])
        if not nonempty(season.get("title")) or season.get("model") not in ("dias", "capitulos"):
            errors.append(f"{context}: {season['id']} precisa de title e model 'dias' ou 'capitulos'.")
        if not nonempty(season.get("source")):
            errors.append(f"{context}: {season['id']} precisa de source.")
        elif hero_dir is not None and not (Path(hero_dir) / season["source"]).is_file():
            errors.append(f"{context}: fonte da temporada {season['id']} não encontrada: {season['source']}.")
        rng = season.get("range")
        if rng is not None and (not isinstance(rng, list) or len(rng) != 2 or not all(integer(v, 1) for v in rng)
                                or rng[0] > rng[1] or rng[1] > max_day):
            errors.append(f"{context}: range inválido em {season['id']}.")
        if season.get("model") == "capitulos" and not integer(season.get("started_day"), 1):
            errors.append(f"{context}: temporada por capítulos precisa de started_day.")
    if data.get("current") is not None and data["current"] not in ids:
        errors.append(f"{context}: current aponta para temporada inexistente.")
    return errors, warnings


def validate_capitulos(hero_id, data, max_day, hero_dir=None):
    errors, warnings = [], []
    context = f"'{hero_id}'/capitulos.json"
    if not isinstance(data, dict) or not isinstance(data.get("chapters"), list):
        return [f"{context}: objeto com lista chapters é obrigatório."], warnings
    if data.get("hero_id") != hero_id or data.get("schema_version") != 1 or not nonempty(data.get("season")):
        errors.append(f"{context}: schema_version=1, hero_id e season são obrigatórios.")
    tomos = data.get("tomos")
    if not isinstance(tomos, list) or not tomos:
        errors.append(f"{context}: tomos deve ser lista não vazia.")
        tomos = []
    ranges = {}
    for tomo in tomos:
        if not isinstance(tomo, dict) or not nonempty(tomo.get("id")) or not integer(tomo.get("number"), 1):
            errors.append(f"{context}: tomo precisa de id e number.")
            continue
        start, end = tomo.get("chapter_start"), tomo.get("chapter_end")
        if not integer(start, 0) or not integer(end, 0) or end < start:
            errors.append(f"{context}: limites inválidos no tomo {tomo['id']}.")
            continue
        ranges[tomo.get("number")] = (start, end, tomo["id"])
    ids = set()
    for chapter in data["chapters"]:
        if not isinstance(chapter, dict) or not isinstance(chapter.get("id"), int) or isinstance(chapter.get("id"), bool) or chapter["id"] < 0:
            errors.append(f"{context}: capítulo precisa de id inteiro >= 0.")
            continue
        cid = chapter["id"]
        if cid in ids:
            errors.append(f"{context}: capítulo duplicado {cid}.")
        ids.add(cid)
        if not nonempty(chapter.get("title")) or not nonempty(chapter.get("goal")):
            errors.append(f"{context}: capítulo {cid} precisa de title e goal.")
        if chapter.get("kind") not in CHAPTER_KINDS or chapter.get("status") not in CHAPTER_STATUS:
            errors.append(f"{context}: capítulo {cid} com kind/status inválido.")
        tomo = chapter.get("tomo")
        if not integer(tomo, 1) or tomo not in ranges:
            errors.append(f"{context}: capítulo {cid} aponta para tomo inexistente.")
        elif not (ranges[tomo][0] <= cid <= ranges[tomo][1]):
            errors.append(f"{context}: capítulo {cid} fora da faixa do Tomo {tomo} ({ranges[tomo][0]}-{ranges[tomo][1]}).")
        days = chapter.get("days", [])
        if not isinstance(days, list) or any(not integer(d, 1) for d in days):
            errors.append(f"{context}: days inválido no capítulo {cid}.")
        parts = chapter.get("parts", [])
        if not isinstance(parts, list):
            errors.append(f"{context}: parts deve ser lista no capítulo {cid}.")
        else:
            for part in parts:
                if not isinstance(part, dict) or not integer(part.get("day"), 1) or not nonempty(part.get("summary")):
                    errors.append(f"{context}: parte inválida no capítulo {cid}.")
                    continue
                if part.get("source_kind") not in ("documental", "live"):
                    errors.append(f"{context}: parte do capítulo {cid} precisa de source_kind.")
                errors.extend(validate_evidence(part.get("evidence"), f"{context} capítulo {cid} parte Dia {part.get('day')}", max_day, hero_dir, bound=False))
        evidence = chapter.get("evidence")
        if evidence:
            errors.extend(validate_evidence(evidence, f"{context} capítulo {cid}", max_day, hero_dir, bound=False))
        elif chapter.get("status") == "concluido":
            errors.append(f"{context}: capítulo {cid} concluído precisa de evidence.")
        if chapter.get("source_kind") not in ("documental", "live"):
            errors.append(f"{context}: capítulo {cid} precisa de source_kind.")
        if chapter.get("status") == "concluido":
            content = chapter.get("content")
            if not isinstance(content, list) or not content or any(not nonempty(p) for p in content):
                errors.append(f"{context}: capítulo {cid} concluído precisa de content com parágrafos reais.")
            if not integer(chapter.get("closed_on_day"), 1) or chapter["closed_on_day"] > max_day:
                errors.append(f"{context}: capítulo {cid} concluído precisa de closed_on_day válido.")
        else:
            warnings.append(f"'{hero_id}': capítulo {cid} em produção ({chapter.get('status')}); não publicado por inteiro.")
    return errors, warnings


def validate_hero_sync(hero_entry, root_dir=ROOT_DIR, max_day=None):
    errors, warnings = [], []
    if not isinstance(hero_entry, dict) or not isinstance(hero_entry.get("id"), str) or not SLUG.fullmatch(hero_entry["id"]):
        return ["Entrada inválida no catálogo: id deve ser slug seguro."], warnings
    hero_id = hero_entry["id"]
    hero_dir = Path(root_dir) / "data" / "heroes" / hero_id
    local, errs = check_json_file(hero_dir / "hero.json")
    errors.extend(errs)
    if not isinstance(local, dict):
        return errors + [f"'{hero_id}': hero.json deve ser objeto."], warnings
    if local != hero_entry:
        differing = sorted(key for key in set(local) | set(hero_entry) if local.get(key) != hero_entry.get(key))
        errors.append(f"'{hero_id}': catálogo e hero.json divergem em {', '.join(differing)}; sincronizar metadados completos.")
    if max_day is None:
        posts, errs = check_json_file(hero_dir / "posts.json")
        errors.extend(errs)
        max_day = max((post.get("id", 0) for post in posts if isinstance(post, dict) and integer(post.get("id"), 1)), default=0) if isinstance(posts, list) else 0
    draft = local.get("record_status") == "draft"
    if draft and max_day:
        errors.append(f"'{hero_id}': record_status=draft é incompatível com crônicas já iniciadas.")
    state = None
    effective_max = max_day
    chapters_file = hero_dir / "capitulos.json"
    if chapters_file.is_file():
        try:
            chapters_data = json.loads(chapters_file.read_text(encoding="utf-8-sig"))
            dias = [p["day"] for c in chapters_data.get("chapters", []) for p in c.get("parts", [])
                    if isinstance(p, dict) and integer(p.get("day"), 1)]
            if dias:
                effective_max = max(effective_max, max(dias))
        except Exception:
            pass
    if (hero_dir / "state.json").is_file():
        state, errs = check_json_file(hero_dir / "state.json")
        errors.extend(errs)
        se, sw = validate_state(hero_id, state, effective_max, hero_dir)
        errors.extend(se)
        warnings.extend(sw)
        # O mesmo renderizador cobre classe, habilidades e equipamento, além dos números.
        if not errs and not se:
            try:
                try:
                    from scripts.sync_hero import expected_outputs
                except ImportError:
                    from sync_hero import expected_outputs
                for relative, expected in expected_outputs(root_dir, hero_id).items():
                    target = Path(root_dir) / relative
                    actual = target.read_text(encoding="utf-8-sig") if target.is_file() else None
                    same = actual is not None and (json.loads(actual) == json.loads(expected) if target.suffix == ".json" else actual == expected)
                    if not same:
                        errors.append(f"'{hero_id}': derivado desatualizado: {relative}; executar sync_hero.py após conferir as fontes.")
            except (ValueError, KeyError, TypeError, AttributeError, IndexError, ZeroDivisionError, OSError) as exc:
                errors.append(f"'{hero_id}': não foi possível gerar/conferir derivados: {exc}.")
    elif not draft:
        warnings.append(f"'{hero_id}': estado estruturado ainda ausente no legado; ficha não certificada ao vivo.")
    ficha_path = hero_dir / "ficha.md"
    if not ficha_path.is_file():
        errors.append(f"'{hero_id}': ficha.md ausente.")
    elif not draft:
        ficha = parse_ficha(ficha_path.read_text(encoding="utf-8-sig"))
        quick = local.get("quick_stats")
        if not isinstance(quick, dict):
            errors.append(f"'{hero_id}': quick_stats deve ser objeto.")
            quick = {}
        for key in ("hp", "mana", "mv"):
            if ficha[key] is None:
                errors.append(f"'{hero_id}': não foi possível interpretar {key} em ficha.md; conferência não pode ser pulada.")
                continue
            match = re.fullmatch(r"\s*(\d+)\s*/\s*(\d+)\s*", str(quick.get(key, "")))
            if not match or tuple(map(int, match.groups())) != ficha[key]:
                errors.append(f"'{hero_id}': {key} de quick_stats diverge da ficha.")
            vital = state.get("vitals", {}).get(key) if isinstance(state, dict) and isinstance(state.get("vitals"), dict) else None
            if isinstance(vital, dict) and ficha[key] != (vital.get("current"), vital.get("max")):
                errors.append(f"'{hero_id}': {key} de ficha/quick_stats diverge de state.json.")
        if ficha["wimpy"] is None:
            (errors if state is not None else warnings).append(f"'{hero_id}': Wimpy ausente ou não interpretável na ficha.")
        elif ficha["hp"] and abs(ficha["wimpy"] - int(ficha["hp"][1] * .25)) > 1:
            warnings.append(f"'{hero_id}': Wimpy {ficha['wimpy']} difere de ~25% do HP máximo; isso não garante uma retirada segura.")
        if isinstance(state, dict):
            for key in ("level", "gold", "wimpy", "training_sessions", "experience"):
                expected = state.get("experience", {}).get("current") if key == "experience" and isinstance(state.get("experience"), dict) else state.get(key)
                if ficha[key] is None or ficha[key] != expected:
                    errors.append(f"'{hero_id}': ficha.{key} ausente, não interpretável ou diferente de state.json.")
        if ficha["training_sessions"]:
            warnings.append(f"'{hero_id}': {ficha['training_sessions']} sessões de treino documentadas; escolher conforme objetivo antes de gastar.")
    for filename, validator in (("mapa.json", validate_map), ("ciclos.json", validate_cycles), ("missoes.json", validate_missions)):
        path = hero_dir / filename
        if path.is_file():
            data, errs = check_json_file(path)
            errors.extend(errs)
            if errs:
                continue
            extra = {"state": state} if filename == "mapa.json" else {"hero_dir": hero_dir} if filename == "missoes.json" else {}
            ve, vw = validator(hero_id, data, effective_max, **extra)
            errors.extend(ve)
            warnings.extend(vw)
    events_path = hero_dir / "events.json"
    if events_path.is_file():
        events, errs = check_json_file(events_path)
        errors.extend(errs)
        if not isinstance(events, list):
            errors.append(f"'{hero_id}': events.json deve ser lista.")
        else:
            event_ids = set()
            for event in events:
                if not isinstance(event, dict) or not nonempty(event.get("id")):
                    errors.append(f"'{hero_id}': evento precisa de id textual.")
                    continue
                if event["id"] in event_ids:
                    errors.append(f"'{hero_id}': evento duplicado: {event['id']}.")
                event_ids.add(event["id"])
                if not integer(event.get("day"), 1) or event["day"] > max_day:
                    errors.append(f"'{hero_id}': evento {event['id']} está fora do histórico publicado.")
                if not nonempty(event.get("type")) or not nonempty(event.get("summary")) or event.get("source_kind") not in ("document", "documental", "live"):
                    errors.append(f"'{hero_id}': evento {event['id']} precisa de type, summary e source_kind explícito.")
                errors.extend(validate_evidence(event.get("evidence"), f"{hero_id}/evento {event['id']}", max_day, hero_dir))
    for filename, validator in (("temporadas.json", validate_temporadas), ("capitulos.json", validate_capitulos)):
        path = hero_dir / filename
        if path.is_file():
            data, errs = check_json_file(path)
            errors.extend(errs)
            if not errs:
                ve, vw = validator(hero_id, data, effective_max, hero_dir)
                errors.extend(ve)
                warnings.extend(vw)
    return errors, warnings


def validate_project(root_dir=ROOT_DIR):
    errors, warnings = [], []
    root_dir = Path(root_dir)
    heroes, errs = check_json_file(root_dir / "data" / "heroes.json")
    errors.extend(errs)
    if not isinstance(heroes, list):
        return errors + ["data/heroes.json deve ser lista."], warnings
    if not heroes:
        errors.append("data/heroes.json está vazio; nenhum herói pode ser conferido.")
    seen = set()
    for hero in heroes:
        if not isinstance(hero, dict) or not isinstance(hero.get("id"), str) or not SLUG.fullmatch(hero["id"]):
            errors.append("Entrada inválida no catálogo de heróis.")
            continue
        hero_id = hero["id"]
        if hero_id in seen:
            errors.append(f"Herói duplicado no catálogo: {hero_id}.")
        seen.add(hero_id)
        hero_dir = root_dir / "data" / "heroes" / hero_id
        posts, errs = check_json_file(hero_dir / "posts.json")
        errors.extend(errs)
        policy = hero.get("evidence_policy")
        legacy_limit = None
        if not isinstance(policy, dict) or not integer(policy.get("legacy_through_day")):
            errors.append(f"'{hero_id}': evidence_policy.legacy_through_day precisa de um limite documental explícito, sem presumir que novos dias sejam legado.")
        else:
            legacy_limit = policy["legacy_through_day"]
        pe, pw = validate_posts(hero_id, posts, allow_empty=hero.get("record_status") == "draft", hero_dir=hero_dir, legacy_through_day=legacy_limit)
        errors.extend(pe)
        warnings.extend(pw)
        max_day = max((p["id"] for p in posts if isinstance(p, dict) and integer(p.get("id"), 1)), default=0) if isinstance(posts, list) else 0
        he, hw = validate_hero_sync(hero, root_dir, max_day)
        errors.extend(he)
        warnings.extend(hw)
    return errors, warnings


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT_DIR, help="Raiz a conferir (padrão: este projeto).")
    args = parser.parse_args()
    errors, warnings = validate_project(args.root)
    for warning in warnings:
        print(f"[AVISO] {warning}")
    for error in errors:
        print(f"[ERRO] {error}")
    print(f"Conferência documental: {len(errors)} erro(s), {len(warnings)} aviso(s).")
    return 1 if errors else 0


if __name__ == "__main__":
    for _stream in (sys.stdout, sys.stderr):
        if hasattr(_stream, "reconfigure"):
            _stream.reconfigure(encoding="utf-8", errors="replace")
    sys.exit(main())
