import json
import os
import sys
from datetime import datetime

POSTS_PATH = os.path.join(os.path.dirname(__file__), "data", "posts.json")

def add_chronicle(day_num, title, date_str, in_game_time, excerpt, tags, content_paragraphs, day_label=None):
    """
    Adiciona uma nova crônica ao topo de posts.json (a mais recente primeiro).
    """
    if os.path.exists(POSTS_PATH):
        with open(POSTS_PATH, "r", encoding="utf-8") as f:
            posts = json.load(f)
    else:
        posts = []
        
    new_post = {
        "id": day_num,
        "day": day_label if day_label else f"Dia {day_num}",
        "title": title,
        "date": date_str,
        "in_game_time": in_game_time,
        "excerpt": excerpt,
        "tags": tags,
        "content": content_paragraphs
    }
    
    # Remove se já existia com o mesmo ID
    posts = [p for p in posts if p.get("id") != day_num]
    
    # Insere no topo
    posts.insert(0, new_post)
    
    # Ordena pelo ID decrescente
    posts.sort(key=lambda x: x.get("id", 0), reverse=True)
    
    with open(POSTS_PATH, "w", encoding="utf-8") as f:
        json.dump(posts, f, ensure_ascii=False, indent=2)
        
    print(f"Crônica do Dia {day_num} ('{title}') adicionada com sucesso ao blog!")

if __name__ == "__main__":
    print("Script de adição de crônicas diárias ao blog de Antigravitus.")
    print("Use: add_chronicle(day_num, title, date, in_game_time, excerpt, tags, content_paragraphs)")
