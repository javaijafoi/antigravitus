# -*- coding: utf-8 -*-
"""
Módulo de funções puras para parsing e análise de texto do CircleMUD / Devil's Bob MUD.
Totalmente desacoplado de rede ou estado de conexão (Zero-Network).
Permite testes unitários determinísticos contra amostras reais gravadas em log.
"""

import re
import unicodedata
from typing import Optional, Dict, Any

def strip_accents(text):
    """Remove acentos e marcas diacríticas para comparações insensíveis a caracteres especiais."""
    if not text:
        return ""
    # Tratar eventuais artefatos de decodificação mista (mojibake)
    text = text.replace("Ã­", "i").replace("Ã¡", "a").replace("Ã£", "a").replace("Ã©", "e").replace("Ã³", "o").replace("Ãº", "u").replace("Ã§", "c")
    text = text.replace("\xad", "i")
    return ''.join(c for c in unicodedata.normalize('NFD', text) if unicodedata.category(c) != 'Mn')

# Mapeamento de direções cardeais do CircleMUD (PT-BR e códigos rápidos)
DIRECTION_NORM = {
    "norte": "norte", "n": "norte", "north": "norte",
    "sul": "sul", "s": "sul", "south": "sul",
    "leste": "leste", "l": "leste", "e": "leste", "east": "leste",
    "oeste": "oeste", "o": "oeste", "w": "oeste", "west": "oeste",
    "cima": "cima", "c": "cima", "u": "cima", "up": "cima",
    "baixo": "baixo", "b": "baixo", "d": "baixo", "down": "baixo"
}

DIRECTION_CODES = {
    "norte": "n",
    "sul": "s",
    "leste": "e",  # padrão telnet aceito universalmente
    "oeste": "w",
    "cima": "u",
    "baixo": "d"
}

DIRECTION_OPPOSITES = {
    "norte": "sul", "sul": "norte",
    "leste": "oeste", "oeste": "leste",
    "cima": "baixo", "baixo": "cima",
    "n": "s", "s": "n",
    "e": "w", "w": "e",
    "u": "d", "d": "u",
    "l": "o", "o": "l",
    "c": "b", "b": "c"
}

# Padrões canônicos de recusa de comandos no CircleMUD
REJECTION_PATTERNS = [
    (r"voc[eê]\s+n[aã]o\s+pode\s+ir\s+por\s+a[ií]", "blocked_exit"),
    (r"o\s+seu\s+movimento\s+est[aá]\s+bloqueado", "blocked_exit"),
    (r"movimento\s+(?:est[aá]\s+)?bloqueado", "blocked_exit"),
    (r"est[aá]\s+bloquead[ao]", "blocked_exit"),
    (r"n[aã]o\s+h[aá]\s+sa[ií]da", "blocked_exit"),
    (r"n[aã]o\s+pode\s+passar", "blocked_exit"),
    (r"a\s+porta\s+est[aá]\s+fechada", "closed_door"),
    (r"a\s+porta\s+parece\s+estar\s+fechada", "closed_door"),
    (r"porta\s+fechada", "closed_door"),
    (r"est[aá]\s+fechad[ao]", "closed_door"),
    (r"voc[eê]\s+n[aã]o\s+pode\s+abrir\s+isso", "cannot_open"),
    (r"voc[eê]\s+n[aã]o\s+pode\s+fechar\s+isso", "cannot_close"),
    (r"est[aá]\s+trancad[ao]", "locked"),
    (r"voc[eê]\s+n[aã]o\s+tem\s+a\s+chave", "no_key"),
    (r"voc[eê]\s+n[aã]o\s+pode\s+encontrar\s+isto", "cannot_find"),
    (r"voc[eê]\s+n[aã]o\s+pode\s+encontrar", "cannot_find"),
    (r"n[aã]o\s+h[aá]\s+ningu[eé]m\s+com\s+esse\s+nome", "target_not_found"),
    (r"n[aã]o\s+h[aá]\s+ningu[eé]m\s+aqui", "target_not_found"),
    (r"voc[eê]\s+n[aã]o\s+v[eê]\s+nenhum", "target_not_found"),
    (r"voc[eê]\s+n[aã]o\s+pode\s+carregar\s+mais\s+itens", "inventory_full"),
    (r"voc[eê]\s+n[aã]o\s+tem\s+mana\s+suficiente", "insufficient_mana"),
    (r"voc[eê]\s+n[aã]o\s+tem\s+pontos\s+de\s+magia\s+suficientes", "insufficient_mana"),
    (r"voc[eê]\s+precisa\s+descansar\s+antes", "need_rest"),
    (r"voc[eê]\s+precisa\s+estar\s+em\s+p[eé]", "need_stand"),
    (r"voc[eê]\s+n[aã]o\s+pode\s+fazer\s+isso\s+sentado", "need_stand"),
    (r"voc[eê]\s+est[aá]\s+dormindo", "need_stand"),
    (r"voc[eê]\s+n[aã]o\s+pode\s+atacar\s+isso", "invalid_target"),
    (r"como\?!?", "syntax_error"),
    (r"^o\s+que\?", "syntax_error"),
    (r"comando\s+desconhecido", "unknown_command"),
]

def parse_vitals(text):
    """
    Extrai pontos vitais instantâneos a partir de linhas de prompt ou score:
    Retorna dicionário com 'hp', 'mana', 'mv' (int ou None).
    Suporta inteiros com sinal (ex: -30hp) para detecção de estados críticos e morte.
    """
    if not text:
        return {"hp": None, "mana": None, "mv": None}

    # Busca no prompt (ex: 52hp 140mn 95mv > ou -30hp 140mn 95mv >)
    matches = re.findall(r'(-?\d+)\s*hp\s+(-?\d+)\s*mn\s+(-?\d+)\s*mv', text, re.IGNORECASE)
    if matches:
        last = matches[-1]
        return {
            "hp": int(last[0]),
            "mana": int(last[1]),
            "mv": int(last[2])
        }

    # Fallback para score textual (ex: Vida: {<<<<<>>>>>} 52 de 52 ou Vida: {---} -12 de 52)
    hp_match = re.search(r'Vida:\s*(?:\{.*?\})?\s*(-?\d+)(?:\s+de\s+(-?\d+))?', text, re.IGNORECASE)
    mn_match = re.search(r'Mana:\s*(?:\{.*?\})?\s*(-?\d+)(?:\s+de\s+(-?\d+))?', text, re.IGNORECASE)
    mv_match = re.search(r'Movimento:\s*(?:\{.*?\})?\s*(-?\d+)(?:\s+de\s+(-?\d+))?', text, re.IGNORECASE)

    hp = int(hp_match.group(1)) if hp_match else None
    mana = int(mn_match.group(1)) if mn_match else None
    mv = int(mv_match.group(1)) if mv_match else None

    return {"hp": hp, "mana": mana, "mv": mv}

def parse_supplies(text):
    """Fome e sede a partir do que o servidor mostra.

    Devolve {'fome': bool|None, 'sede': bool|None}; None significa "ainda nao
    observado". O bloco '[Situacao atual]' do score e a fonte autoritativa,
    porque ele reflete o AGORA. As rajadas 'morrendo de fome/sede' so valem
    como reserva, quando nao ha bloco nenhum: o servidor as repete com o dano
    junto ('-2hp, -3mn e -2mv'), mas elas envelhecem no buffer.
    """
    if not text:
        return {"fome": None, "sede": None}
    norm_txt = strip_accents(text.lower())
    corte = norm_txt.rfind('situacao atual')
    if corte != -1:
        corpo = norm_txt[corte:corte + 400]
        return {"fome": 'fome' in corpo, "sede": 'sede' in corpo}
    return {
        "fome": ('morrendo de fome' in norm_txt) or ('esta com fome' in norm_txt),
        "sede": ('morrendo de sede' in norm_txt) or ('esta com sede' in norm_txt),
    }

def parse_exits(text):
    """
    Analisa o bloco de saídas de uma sala no CircleMUD:
    Exemplo:
        Saídas:
        Norte - A Entrada da Guilda dos Magos
        Leste - O Laboratório dos Magos
        Baixo - A Junção no Esgoto
    Retorna:
        {
            "exits": {"norte": "A Entrada da Guilda dos Magos", ...},
            "exit_directions": ["norte", "leste", "baixo"],
            "exit_codes": ["n", "e", "d"]
        }
    """
    exits = {}
    directions = []
    codes = []

    if not text:
        return {"exits": exits, "exit_directions": directions, "exit_codes": codes}

    lines = [line.strip() for line in text.split('\n') if line.strip()]
    in_exits_block = False

    for line in lines:
        norm = strip_accents(line.lower())

        if "saidas:" in norm or "saidas :" in norm:
            in_exits_block = True
            # Checar se na mesma linha há "Nenhuma!"
            if "nenhuma" in norm:
                break
            continue

        if in_exits_block:
            # Uma saída é formatada como: <Direção> - <Destino>
            # Ex: "Oeste - O Bar dos Magos"
            m = re.match(r'^([a-zA-ZçÇ]+)\s*-\s*(.+)$', line)
            if m:
                raw_dir = m.group(1).strip().lower()
                dest = m.group(2).strip()
                norm_dir = strip_accents(raw_dir)
                canonical_dir = DIRECTION_NORM.get(norm_dir, norm_dir)
                exits[canonical_dir] = dest
                if canonical_dir not in directions:
                    directions.append(canonical_dir)
                    code = DIRECTION_CODES.get(canonical_dir, canonical_dir[0] if canonical_dir else "")
                    codes.append(code)
            else:
                # Fim do bloco de saídas se a linha não corresponder ao padrão de saída
                # (ex: prompt, linha de mob, ou texto livre)
                if line and not line.startswith("("):
                    in_exits_block = False

    return {
        "exits": exits,
        "exit_directions": directions,
        "exit_codes": codes
    }

def detect_rejection(text):
    """
    Inspeciona uma resposta textual do servidor e detecta se uma ação falhou ou foi rejeitada.
    Retorna:
        {
            "is_rejected": bool,
            "reason": str or None,
            "message": str or None
        }
    """
    if not text:
        return {"is_rejected": False, "reason": None, "message": None}

    lines = [line.strip() for line in text.split('\n') if line.strip()]
    for line in lines:
        # Pular linhas de prompt (suportando vitais com sinal, ex: -30hp)
        if re.search(r'-?\d+hp\s+-?\d+mn', line):
            # Mas se a linha do prompt contiver uma mensagem após o '>', verificar a mensagem
            prompt_tail = line.split('>')[-1].strip() if '>' in line else ""
            if prompt_tail:
                line_to_check = prompt_tail
            else:
                continue
        else:
            line_to_check = line

        norm = strip_accents(line_to_check.lower())
        for pattern, reason in REJECTION_PATTERNS:
            if re.search(pattern, norm):
                return {
                    "is_rejected": True,
                    "reason": reason,
                    "message": line_to_check
                }

    return {"is_rejected": False, "reason": None, "message": None}

def parse_room(text):
    """
    Analisa o texto retornado pelo comando look (ou entrada em nova sala) e separa:
    - title: Nome da sala
    - exits: Dicionário {direção_canônica: destino}
    - exit_directions: Lista de direções disponíveis ['norte', 'oeste', ...]
    - exit_codes: Códigos curtos ['n', 'w', ...]
    - live_mobs: Criaturas vivas (excluindo cadáveres e estátuas decorativas)
    - ground_items: Itens no chão
    - raw: Texto original
    """
    lines = [line.strip() for line in text.split('\n') if line.strip()]
    room_title = ""
    live_mobs = []
    ground_items = []

    ignore_prefixes = [
        "o corpo de", "o cadáver de", "o defunto de",
        "vermes consomem", "uma monumental estátua",
        "uma estátua", "uma caixa de madeira", "um grande quadro",
        "um discreto aviso", "uma fonte", "um brilhante portal"
    ]

    # Extrai saídas do bloco
    parsed_exits_data = parse_exits(text)
    exits = parsed_exits_data["exits"]
    exit_directions = parsed_exits_data["exit_directions"]
    exit_codes = parsed_exits_data["exit_codes"]

    # Procurar título da sala e entidades
    in_exits_section = False
    for line in lines:
        norm = strip_accents(line.lower())

        # Se for linha de prompt pura (ex: 36hp 116mn 91mv > ou -30hp 140mn 95mv >)
        if re.search(r'^\s*((-?\d+)hp\s+(-?\d+)mn\s+(-?\d+)mv\s*>\s*)+$', norm):
            continue

        # Se tiver prompt embutido, limpa o prefixo do prompt para avaliar o conteúdo
        if ">" in line and re.search(r'-?\d+hp\s+-?\d+mn', line):
            line = line.split('>')[-1].strip()
            norm = strip_accents(line.lower())
            if not line:
                continue

        # Se começar com SEND ou echo do comando
        if norm.startswith(">>>") or norm.startswith("olhar") or norm.startswith("look") or norm.startswith("saidas"):
            continue

        # Marcador de bloco de saídas
        if "saidas:" in norm or "saidas :" in norm:
            in_exits_section = True
            continue

        if in_exits_section:
            if re.match(r'^[a-zA-ZçÇ]+\s*-\s*.+$', line):
                continue
            else:
                in_exits_section = False

        # Título da sala: primeira linha substantiva
        if not room_title and len(line) < 60 and not norm.startswith("voce") and not norm.startswith("certo, voce") and not norm.startswith("como"):
            # Evitar capturar banners do jogo ou mensagens de status
            if not any(skip in norm for skip in ["devil's bob", "baseado no circlemud", "pressione enter", "conecte-se novamente"]):
                room_title = line
                continue

        # Criaturas vivas
        if any(k in norm for k in ["está aqui", "esta aqui", "zanza por aqui", "rastejando pelo chão"]):
            is_ignored = False
            for ig in ignore_prefixes:
                if strip_accents(ig) in norm:
                    is_ignored = True
                    break
            if not is_ignored:
                # Checar se não é item com descrição similar
                if any(item_kw in norm for item_kw in ["veste", "punhal", "elmo", "espada", "armadura", "coleira", "carroça"]):
                    ground_items.append(line)
                else:
                    live_mobs.append(line)
        elif "está jogad" in norm or "esta jogad" in norm or "foi deixad" in norm:
            ground_items.append(line)

    return {
        "title": room_title,
        "exits": exits,
        "exit_directions": exit_directions,
        "exit_codes": exit_codes,
        "live_mobs": live_mobs,
        "ground_items": ground_items,
        "raw": text
    }

def classify_game_state(vitals: Optional[dict], text: str = "", is_connected: bool = True) -> str:
    """
    Classifica o estado operacional da personagem no MUD com base na conectividade, vitais e texto retornado.
    Retorna uma das seguintes constantes:
    - "disconnected": conexão caída, fechada ou EOF
    - "dead_or_menu": personagem morta (HP <= -10 ou mensagem de morte) ou em menu/login/pager
    - "unknown": vitais ausentes/corrompidos (impede progressão automática)
    - "incapacitated": HP <= 0 e HP > -10 (atordoada / sangrando / incapacitada)
    - "in_combat": combate ativo detectado via medidor de combate ({...>>}) ou mensagens de agressão
    - "in_game": conectada, viva (HP > 0) e sem ameaça ativa
    """
    if not is_connected:
        return "disconnected"

    raw_text = text or ""
    norm = strip_accents(raw_text.lower())

    # 1. Checagem de Morte ou Menu (dead_or_menu)
    # 1a. HP em nível de morte (CircleMUD: <= -10 HP)
    if vitals and vitals.get("hp") is not None and vitals["hp"] <= -10:
        return "dead_or_menu"

    # 1b. Mensagens explícitas de morte da personagem do jogador
    # Cuidado com o historico do score: "Voce morreu 7 vezes" e contagem, nao
    # obito. Sem o lookahead, todo 'score' era lido como morte.
    # "sua alma" solto casava com lore; agora exige o verbo ou as reticencias.
    death_patterns = [
        r"voc[eê]\s+est[aá]\s+morto",
        r"sua\s+alma(?:\s+(?:flutua|abandona|deixa)|\.\.\.)",
        r"voc[eê]\s+morreu(?!\s+(?:\d|vezes))",
        r"o\s+ceifador\s+ceifa\s+sua\s+vida",
        r"\br\.i\.p\.\b",
        r"seu\s+corpo\s+cai\s+sem\s+vida",
    ]
    for pat in death_patterns:
        if re.search(pat, norm):
            return "dead_or_menu"

    # 1c. Telas de menu, seleção, login ou pager
    menu_patterns = [
        r"menu\s+principal",
        r"fa[cç]a\s+a\s+sua\s+escolha",
        r"escolha\s+uma\s+das\s+seguintes\s+op[cç][oõ]es",
        r"escolha\s*:",
        r"pressione\s+(?:enter|<enter>)",
        r"aperte\s+enter\s+para\s+continuar",
        r"qual\s+o\s+seu\s+nome",
        r"digite\s+seu\s+nome",
        r"qual\s+a\s+sua\s+senha",
        r"voc[eê]\s+deseja\s+entrar\s+como",
        r"conecte-se\s+novamente\s+mais\s+tarde",
    ]
    for pat in menu_patterns:
        if re.search(pat, norm):
            return "dead_or_menu"

    # 2. Dados ausentes: vitais nulos ou sem HP impedem progressão automática (unknown)
    if vitals is None or vitals.get("hp") is None:
        return "unknown"

    hp = vitals["hp"]

    # 3. Incapacitada: HP <= 0 e HP > -10 (atordoada / mortalmente ferida)
    if hp <= 0 and hp > -10:
        return "incapacitated"

    # 4. Combate ativo (in_combat)
    # 4a. Barra / medidor de combate do CircleMUD ({...>>} ou medidores duplos de combate)
    # Um medidor de combate nao vem rotulado. As barras do score vem com rotulo
    # antes da chave ('Banco: {<<<<<>>>>>}', 'Proximo nivel: {----<>>>>>}') e tem
    # exatamente a mesma forma. Sem separar as duas, rodar 'score' ligava o flag
    # de combate e ele nunca mais desligava.
    in_combat_meter = False
    for line in raw_text.splitlines():
        if ':' in line.split('{', 1)[0]:
            continue
        if re.search(r'\{[^\}]*>>\}', line) or re.search(r'\{[^\}]*<<[^\}]*\}', line) or re.search(r'\{[<\->=]{5,}\}.*?\{[<\->=]{5,}\}', line):
            in_combat_meter = True
            break

    if in_combat_meter:
        return "in_combat"

    # 4b. Mensagens de agressão ou ação em combate
    combat_action_patterns = [
        r"ataca\s+voc[eê]",
        r"acerta\s+voc[eê]",
        r"arrebenta\s+voc[eê]",
        r"massacra\s+voc[eê]",
        r"golpeia\s+(?:voc[eê]|seu\s+|sua\s+)",
        r"tenta\s+acertar\s+voc[eê]",
        r"desvia\s+do\s+ataque",
        r"bloquear\s+o\s+ataque",
        r"erra\s+voc[eê]",
        r"n[aã]o\s+d[aá]!\s+voc[eê]\s+est[aá]\s+muito\s+ocupado,\s+lutando",
        r"voc[eê]\s+entra\s+em\s+p[aâ]nico\s+e\s+tenta\s+fugir",
        r"voc[eê]\s+arrebenta",
        r"voc[eê]\s+massacra",
        r"voc[eê]\s+acerta",
        r"voc[eê]\s+golpeia",
        r"voc[eê]\s+desfere",
        r"voc[eê]\s+tenta\s+furar",
        r"voc[eê]\s+tenta\s+cravar\s+sua\s+arma",
        r"seu\s+m[ií]ssil\s+m[aá]gico",
    ]
    for pat in combat_action_patterns:
        if re.search(pat, norm):
            return "in_combat"

    # 5. Normal: HP > 0 e sem ameaça ativa
    if hp > 0:
        return "in_game"

    return "unknown"

def verify_save_confirmation(text: str) -> bool:
    """
    Verifica se a resposta do servidor confirma estritamente o salvamento do jogo.
    Retorna True APENAS se houver confirmação canônica explícita ("Salvando os seus atalhos.", "Salvo.", "Jogo salvo").
    Retorna False para erros, recusas, mensagens ambíguas ou falsos positivos como 'ok'.
    """
    if not text:
        return False

    norm = strip_accents(text.lower())

    # Rejeição imediata se houver mensagens de erro, recusa ou impedimento do servidor
    rejection_keywords = [
        "nao da!", "nao da !", "muito ocupado", "lutando",
        "precisa estar em pe", "esta dormindo", "esta descansando",
        "esta incapacitado", "bloqueado", "impossivel",
        "voce nao pode", "comando desconhecido"
    ]
    for kw in rejection_keywords:
        if kw in norm:
            return False

    # Confirmação estrita de padrões canônicos do CircleMUD
    canonical_patterns = [
        r"salvando\s+os\s+seus\s+atalhos",
        r"\bjogo\s+salvo\b",
        r"\bsalvo\.",
        r"^\s*salvo\b",
        r"\bsalvando\.\.\.",
        r"\bsalvando\s+seu\s+jogo\b",
    ]
    for pattern in canonical_patterns:
        if re.search(pattern, norm):
            return True

    return False

def detect_combat_target_absence(text: str) -> bool:
    """
    Detecta se o servidor indicou que o alvo de combate ou comando não está presente na sala.
    Retorna True para respostas como "não vê nenhuma", "não pode encontrar", "não há ninguém aqui".
    Garante que alvos ausentes nunca sejam contabilizados como vitórias em combate.
    """
    if not text:
        return False
    norm = strip_accents(text.lower())
    absence_patterns = [
        r"n[aã]o\s+v[eê]\s+nenhum",
        r"n[aã]o\s+pode\s+encontrar",
        r"n[aã]o\s+h[aá]\s+ningu[eé]m",
        r"em\s+que\s+voc[eê]\s+deseja\s+lan[cç]ar",
        r"atacar\s+quem\?",
    ]
    for pat in absence_patterns:
        if re.search(pat, norm):
            return True
    return False

