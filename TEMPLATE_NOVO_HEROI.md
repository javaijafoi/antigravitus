# 📋 Boilerplate: Projeto Crônicas de Herói (MUD / RPG)

Guia e template limpo para clonar a arquitetura de **Antigravitus** e criar o compêndio/blog vivo de um novo personagem.

---

## 🧭 Fase 1: As Perguntas de Concepção do Novo Herói

Preencha este formulário para definir o DNA do novo herói antes de gerar os arquivos:

### 1. Ficha Básica
* **Nome do Herói:** `[Ex: Vaelen, Kaelen, Boris, Lyra]`
* **Raça e Classe:** `[Ex: Anão Guerreiro, Ladino Humano, Clériga Elfa]`
* **Título / Alcunha:** `[Ex: O Martelo de Ferro, O Olho das Sombras]`
* **Alinhamento Moral:** `[Ex: Leal e Bom, Neutro Puro, Caótico e Neutro]`
* **Runa / Emoji Símbolo:** `[Ex: ᛏ, ⚔️, 🛡️, 🌙, 🩸]`
* **Universo / Servidor:** `[Ex: Devil's Bob MUD (debomud.org:4000), D&D, Tormenta]`
* **Frase Lema (Quote de abertura):** `["..."]`

### 2. A Matriz das 5 Perguntas Capitais (Psicologia)
1. **Qual é o objetivo principal dele?** *(Desejo externo e grande busca)*
   * `-> Resposta:`
2. **O que ele mais teme?** *(Trauma primordial, insegurança que paralisa ou faz errar)*
   * `-> Resposta:`
3. **Qual é a maior falha de caráter dele?** *(Defeito moral a superar para amadurecer)*
   * `-> Resposta:`
4. **O que ele está disposto a sacrificar?** *(O que aceita perder vs. sua linha ética inegociável)*
   * `-> Resposta:`
5. **Que legado almeja deixar?** *(O que dirão sobre ele quando a jornada terminar)*
   * `-> Resposta:`

### 3. Cenário e Ponto de Partida
* **Local de nascimento/despertar:** `[Ex: Templo, Taverna decadente, Prisão]`
* **Primeiro contato / Mentor / Rival:** `[Nome e função]`
* **Tom narrativo:** `[Ex: Dark fantasy introspectivo, Épico militar, Sarcástico e urbano]`

---

## 📂 Fase 2: Estrutura de Arquivos do Projeto

Crie a seguinte pasta raiz:

```text
[nome-do-heroi]/
├── data/
│   ├── identidade.md      # A alma: 5 perguntas e matriz operacional
│   ├── evolucao.md        # O cinzel: log de mutações psicológicas ciclo a ciclo
│   ├── conhecimento.md    # O grimório: mapa, NPCs, facções e regras do mundo
│   ├── mapa.md            # Registro topográfico e saídas verificadas (a cada 10 ciclos)
│   ├── mapa.json          # Dados do mapa interativo do aventureiro (a cada 10 ciclos)
│   ├── ficha.md           # Ficha viva em tempo real
│   ├── ciclos.json        # Resumos emocionantes de cada ciclo com aviso de spoiler (a cada 10 ciclos)
│   └── posts.json         # Array de crônicas (mais recente no topo)
├── css/
│   └── style.css          # Estilo dark fantasy responsivo (copiar do original)
├── js/
│   └── main.js             # Engine de renderização de posts, mapas e filtros
├── index.html             # Feed principal das crônicas
├── mapa.html              # Mapa interativo do aventureiro
├── ficha.html             # Ficha viva do aventureiro
├── sobre.html             # Apresentação do herói e da matriz psicológica
├── add_day.py             # Script utilitário para injetar nova crônica
├── publish_daily.py       # (Opcional) Sincronização via GitHub API
├── vercel.json            # Deploy estático na Vercel
└── README.md              # Documentação e manifesto
```

---

## 📄 Fase 3: Templates Prontos dos Arquivos

### 1. `data/identidade.md`
```markdown
# ᛟ A Alma de [NOME] — Matriz de Identidade

> *"[INSIRA UMA FRASE DE IMPACTO DO HERÓI]"*

Esta matriz é o motor psicológico de [NOME]. Ela não é estática; ela é desafiada a cada ciclo.

---

## 1. Qual é o objetivo principal dele?
**[OBJETIVO PRINCIPAL]**  
[Detalhamento da busca central, desejos e motivações].

---

## 2. O que ele mais teme?
**[MAIOR TEMOR]**  
[Detalhamento da fobia psicológica, trauma ou fraqueza interna].

---

## 3. Qual é a maior falha de caráter dele?
**[MAIOR FALHA]**  
[Detalhamento do vício, arrogância, covardia, fúria ou desconfiança].

---

## 4. O que ele está disposto a sacrificar para vencer?
**[LIMITES DE SACRIFÍCIO]**  
Sacrifica: [o que ele aceita perder].  
Jamais sacrifica: [o limite ético inegociável].

---

## 5. Que marca ou legado ele quer deixar?
**[LEGADO ALMEJADO]**  
[Como deseja ser lembrado pelas próximas eras].

---

## ⚖️ Matriz de Decisão Operacional
$$\text{Ação Diária} = f(\text{Objetivo}, \text{Filtro de Temor}, \text{Desafio da Falha}) + \text{Saber Acumulado}$$

* **Diante do conflito:** [Como reage].
* **Diante do desconhecido/segredos:** [Como investiga].
* **Diante de outros viajantes/aliados:** [Postura social].
```

---

### 2. `data/evolucao.md`
```markdown
# 📜 O Cinzel da Consciência — Log de Metamorfose de [NOME]

> *"A alma não nasce pronta; ela é desbastada golpe a golpe pelas pedras do mundo."*

Este documento registra as mutações psicológicas, quebras de crença e refinamento das 5 perguntas essenciais.

---

### ⏳ Ciclo 1 (Dia 1): O Ponto de Partida
* **Estado Inicial:** [Ilusão ou motivação com a qual iniciou a jornada].
* **Impacto Chave:** [O primeiro grande acontecimento].
  * *Mutação na Pergunta [X]:* [Como a percepção foi alterada].
```

---

### 3. `data/conhecimento.md`
```markdown
# 🗺️ O Grimório do Mundo — Saber Acumulado de [NOME]

> *"Caminhar sem conhecer o chão é cortejar a sepultura."*

## 🏛️ 1. Topografia e Locais Notáveis

| Localidade | Posição Relativa | Nível de Perigo | Utilidade Prática & Saber Estratégico |
| :--- | :--- | :--- | :--- |
| **Ponto Seguro** | Centro | **Zero (Santuário)** | Descanso e recuperação. |
| **Zona de Risco** | Arredores | **Médio / Alto** | Fontes de recursos e perigos. |

---

## 👥 2. Figuras Notáveis e Facções

* **[Nome do NPC]:**
  * *Posto/Papel:* [Função no mundo].
  * *Relação com [NOME]:* [Aliado, neutro, mentor ou hostil].
```

---

### 4. `data/posts.json`
```json
[
  {
    "id": 1,
    "day": "Dia 1",
    "title": "O Despertar e o Primeiro Passo",
    "date": "14 de outubro de 2026",
    "in_game_time": "Ciclo 1 — O Despertar",
    "excerpt": "O momento em que meus olhos se abriram para este mundo e o primeiro sopro de desafio atingiu meu peito.",
    "tags": [
      "Início da Jornada",
      "Primeiro Ciclo",
      "Despertar"
    ],
    "content": [
      "Parágrafo 1 da crônica contando o início da aventura...",
      "Parágrafo 2 detalhando a primeira decisão tomada...",
      "Parágrafo 3 com a reflexão moral e encerramento do dia."
    ]
  }
]
```

---

### 5. `add_day.py`
```python
import json
import os

POSTS_PATH = os.path.join(os.path.dirname(__file__), "data", "posts.json")

def add_chronicle(day_num, title, date_str, in_game_time, excerpt, tags, content_paragraphs, day_label=None):
    """
    Adiciona nova crônica no topo de data/posts.json mantendo ordenação decrescente.
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

    # Remove duplicata caso já exista
    posts = [p for p in posts if p.get("id") != day_num]
    posts.insert(0, new_post)
    posts.sort(key=lambda x: x.get("id", 0), reverse=True)

    with open(POSTS_PATH, "w", encoding="utf-8") as f:
        json.dump(posts, f, ensure_ascii=False, indent=2)

    print(f"Crônica do Dia {day_num} ('{title}') adicionada com sucesso!")

if __name__ == "__main__":
    print("Script de adição de crônicas diárias.")
```

---

### 6. `vercel.json`
```json
{
  "cleanUrls": true,
  "headers": [
    {
      "source": "/(.*)",
      "headers": [
        {
          "key": "Cache-Control",
          "value": "public, max-age=0, must-revalidate"
        }
      ]
    }
  ]
}
```

---

## ⚡ Passo a Passo para Subir um Novo Herói

1. **Copiar arquivos base de front-end:**
   * Copie `css/style.css` e `js/main.js` deste projeto (eles já cuidam da busca, badges de tag, modal e layout responsivo).
   * Em `index.html` e `sobre.html`, faça a substituição das menções de `Antigravitus` pelo nome, runa e biografia do novo herói.
2. **Definir o herói:** Responda as perguntas da Fase 1 e preencha `data/identidade.md`.
3. **Inicializar crônicas:** Limpe `data/posts.json` deixando apenas o post inaugural (Dia 1).
4. **Deploy:** Suba no GitHub e conecte à Vercel com 1 clique (deploy estático automático).
