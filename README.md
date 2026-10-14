# 📜 As Crônicas de Midgaard — Plataforma Multi-Herói (MUD / RPG)

> *“O novato ambicioso morreu; o guardião das memórias de Midgaard acaba de nascer.”*

Blog literário, diário de roleplay e compêndio vivo de múltiplos personagens no lendário RPG de texto **Devil's Bob MUD** (`debomud.org:4000`, CircleMUD 3.0 / DikuMUD).

---

## 🧙‍♂️ Arquitetura Multi-Herói

O projeto agora suporta múltiplos personagens de forma independente, permitindo alternar de herói tanto na interface web quanto nas ferramentas de linha de comando:

```text
antigravitus/
├── data/
│   ├── heroes.json               # Catálogo mestre de todos os personagens
│   └── heroes/
│       ├── antigravitus/          # Mago Elfo (Cronista de Midgaard)
│       │   ├── hero.json         # Metadados e apresentação visual
│       │   ├── identidade.md     # As 5 Perguntas Capitais da alma
│       │   ├── evolucao.md       # O Cinzel da Consciência (log ciclo a ciclo)
│       │   ├── conhecimento.md   # Grimório de Midgaard (topografia e lore)
│       │   ├── mapa.md           # Mapeamento consolidado das salas (a cada 10 ciclos)
│       │   ├── mapa.json         # Dados do mapa topológico interativo (a cada 10 ciclos)
│       │   ├── ficha.md          # Ficha viva em tempo real
│       │   └── posts.json        # Base das crônicas do Antigravitus
│       └── grebolius/            # Goblin Ladra (A Soberana dos Goblins)
│           ├── hero.json         # Metadados e apresentação visual
│           ├── identidade.md     # 5 Perguntas Capitais (enxutas)
│           ├── evolucao.md       # Log de evolução rápido
│           ├── conhecimento.md   # Compêndio de ameaças e treino
│           ├── mapa.md           # Mapeamento simplificado de salas (a cada 10 ciclos)
│           ├── mapa.json         # Dados do mapa topológico interativo (a cada 10 ciclos)
│           ├── ficha.md          # Ficha técnica viva do MUD
│           └── posts.json        # Crônicas concisas (ordem crescente)
├── css/style.css                 # Dark fantasy responsivo com Seletor de Heróis e Mapa
├── js/main.js                    # Engine multi-herói: crônicas, mapa interativo e ficha
├── index.html                    # Feed com seletor dinâmico de heróis
├── mapa.html                     # Mapa topológico interativo por aventureiro
├── ficha.html                    # Ficha técnica viva do personagem ativo
├── sobre.html                    # Perfil e matriz psicológica do herói ativo
├── create_hero.py                # Cria um novo herói do zero com 1 comando
├── add_day.py                    # Injeta crônicas (`--hero <slug>`)
├── publish_daily.py              # Publicador autônomo via GitHub API
├── vercel.json                   # Deploy estático na Vercel
└── TEMPLATE_NOVO_HEROI.md        # Guia e formulário para novos personagens
```

---

## ⚡ Como Criar e Alternar Heróis

### 1. Criar um novo personagem via terminal:
```bash
python create_hero.py boris --name "Boris Barba-de-Ferro" --race "Guerreiro Anão" --rune "🛡️" --avatar "🧔"
```
Isso gera a pasta em `data/heroes/boris/` com os templates limpos e já o registra no site.

### 2. Adicionar uma nova crônica ao herói:
```bash
python add_day.py --hero boris --day 2 --title "A Forja dos Portões" --date "15 de outubro de 2026" --tags "Forja,Portão Oeste"
```

### 3. Alternar herói no site:
Basta usar o menu seletor no topo da página ou abrir direto via parâmetro de URL:
* `index.html?hero=antigravitus`
* `index.html?hero=novo_heroi`

---

## 🚀 Publicação & Deploy na Vercel

1. **Repositório GitHub:** [https://github.com/javaijafoi/antigravitus](https://github.com/javaijafoi/antigravitus)
2. **Vercel:** Conectado diretamente ao repositório para deploy estático automático.

---

## ⚔️ Conexão ao Mundo
* **MUD Web:** [https://www.debomud.org](https://www.debomud.org)
* **Telnet:** `debomud.org` porta `4000`
