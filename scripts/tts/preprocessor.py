"""Roteirizador Prosódico: Prepara textos de capítulos para narração com ritmo e cadência natural."""

import re
import html
from typing import Dict, Any, List

def clean_markdown(text: str) -> str:
    """Remove marcações Markdown e formata pontuações para fala."""
    # Remove negrito e itálico
    text = re.sub(r'[*_]{1,3}([^*_]+)[*_]{1,3}', r'\1', text)
    # Remove links [texto](url)
    text = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', text)
    # Remove cabeçalhos
    text = re.sub(r'^#+\s*', '', text, flags=re.MULTILINE)
    # Normaliza aspas e travessões
    text = text.replace('“', '"').replace('”', '"')
    text = text.replace('—', ' - ')
    return text.strip()

def prepare_speech_payload(post: Dict[str, Any], voice_config: Dict[str, Any]) -> Dict[str, Any]:
    """
    Gera o roteiro narrado nos formatos Texto Puro, Texto com Breaks (Edge-TTS) e SSML Completo.
    """
    day = post.get("day", f"Dia {post.get('id', '')}").strip()
    title = clean_markdown(post.get("title", "")).strip()
    paragraphs = post.get("content", [])

    voice_id = voice_config.get("voice_id", "pt-BR-AntonioNeural")
    rate = voice_config.get("rate", "+0%")
    pitch = voice_config.get("pitch", "+0Hz")
    volume = voice_config.get("volume", "+0%")
    style = voice_config.get("style", "default")

    # 1. Plain Text para exibição e debug
    plain_lines = [f"{day}: {title}."]
    for p in paragraphs:
        cleaned_p = clean_markdown(p)
        if cleaned_p:
            plain_lines.append(cleaned_p)
    plain_text = "\n\n".join(plain_lines)

    # 2. Texto modulado com pausas (<break time="..." />)
    speech_parts = []
    # Abertura do capítulo
    speech_parts.append(f"{day}. {title}. <break time='900ms'/>")

    for p in paragraphs:
        cleaned = clean_markdown(p)
        if not cleaned:
            continue

        # Evita quebrar caracteres que conflitem com tags XML
        # Substitui & solto por 'e'
        cleaned = re.sub(r'&(?!amp;|lt;|gt;|quot;|apos;)', ' e ', cleaned)

        # Modulação prosódica
        mod_p = cleaned.replace('...', '... <break time="450ms"/>')
        mod_p = mod_p.replace(' - ', ' <break time="300ms"/> ')
        
        speech_parts.append(f"{mod_p} <break time='750ms'/>")

    speech_parts.append("<break time='1000ms'/>")
    speech_text = "\n".join(speech_parts)

    return {
        "day": day,
        "title": title,
        "voice_id": voice_id,
        "rate": rate,
        "pitch": pitch,
        "volume": volume,
        "style": style,
        "plain_text": plain_text,
        "speech_text": speech_text
    }
