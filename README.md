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

## 🧠 Ciclo Diário & Protocolo de IA (`skills/mud-ciclo-diario/`)

Para manter a consistência narrativa e a evolução dos heróis via agentes de IA, todas as diretrizes de gameplay e pós-processamento estão versionadas localmente no projeto em:
👉 [`skills/mud-ciclo-diario/SKILL.md`](skills/mud-ciclo-diario/SKILL.md)

### O que essa skill dita para o agente:
1. **Ritmo Narrativo Rico:** Dias longos, foco em imersão sensorial e ausência total de metajogo.
2. **3 Ações Diárias Obrigatórias:** Ações estruturadas que geram consequências reais no mundo.
3. **Combate & Treino:** Rotina frequente de progressão de atributos, magias e sobrevivência.
4. **Reflexão Decenal (a cada 10 ciclos):** Ponto de virada na psique, consolidação de mapas topológicos e crônicas maiores.
5. **Ficha Viva Sincronizada:** Atualização imediata dos arquivos de ficha, identidade, evolução e conhecimento do personagem.
6. **Autonomia:** O agente deve executar alterações reversíveis diretamente, sem pedir confirmação a cada passo.

> **Dica para amigos/colaboradores:** Se estiver usando o Antigravity, Claude Code, Cursor ou qualquer outro assistente de IA, aponte o assistente para ler `skills/mud-ciclo-diario/SKILL.md` antes de jogar ou gerar crônicas. Assim a IA saberá exatamente como conduzir o herói e atualizar os arquivos.

---

## 🚀 Publicação & Deploy na Vercel

1. **Repositório GitHub:** [https://github.com/javaijafoi/antigravitus](https://github.com/javaijafoi/antigravitus)
2. **Vercel:** Conectado diretamente ao repositório para deploy estático automático.

---

## ⚔️ Conexão ao Mundo
* **MUD Web:** [https://www.debomud.org](https://www.debomud.org)
* **Telnet:** `debomud.org` porta `4000`

