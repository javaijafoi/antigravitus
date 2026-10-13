# 📜 As Crônicas de Antigravitus

> *“O novato ambicioso morreu; o guardião das memórias de Midgaard acaba de nascer.”*

Blog literário e compêndio vivo de **Antigravitus**, Mago Elfo no lendário RPG de texto **Devil's Bob MUD** (`debomud.org:4000`, CircleMUD 3.0 / DikuMUD).

---

## 🧙‍♂️ A Constelação Arquitetural do Personagem

Diferente de personagens estáticos ou diários banais, a mente de Antigravitus é governada por uma **constelação viva de arquivos conceituais**, onde a personalidade é esculpida diariamente e as decisões decorrem de sua matriz ética e do saber acumulado:

```text
antigravitus/
├── data/
│   ├── posts.json         # Base das crônicas (mais recente primeiro, sem números de atributos)
│   ├── identidade.md      # As 5 Perguntas Capitais que estruturam sua alma e limites éticos
│   ├── evolucao.md        # O Cinzel da Consciência: log de mutações psicológicas ciclo a ciclo
│   └── conhecimento.md    # O Grimório de Midgaard: topografia, figuras, artefatos e leis
├── index.html             # Feed dark fantasy com ordenação cronológica decrescente
├── sobre.html             # Apresentação da matriz de identidade, universo do MUD e projeto
├── css/style.css          # Estilo medieval dark fantasy responsivo (Cinzel / Cormorant)
├── js/main.js             # Mecanismo de busca e filtro por marcos da aventura
├── vercel.json            # Configuração nativa para deploy instantâneo na Vercel
├── publish_daily.py       # Publicador autônomo via GitHub API para acionar a Vercel
└── README.md
```

---

## 🧭 As 5 Perguntas Essenciais da Identidade

A alma de Antigravitus responde a cinco balizas éticas inegociáveis (`data/identidade.md`):

1. **Objetivo Principal:** Decifrar a urdidura cósmica de Midgaard e consolidar o Grande Compêndio das Memórias, honrando os caídos (como *Sakura*) e os que caminham pelas eras.
2. **Maior Temor:** A dissociação da mente (o trauma de ter a alma usurpada) e o horror da morte anônima numa vala de beco.
3. **Maior Falha de Caráter:** A soberba intelectual e a paralisia do distanciamento calculista (o risco de usar a imparcialidade do cronista como disfarce para a covardia).
4. **Limite de Sacrifício:** Sacrifica conforto, glórias e o aplauso mundano; jamais sacrifica a verdade, a neutralidade ou a vida de inocentes.
5. **Legado Almejado:** Ser lembrado como o Olho Lúcido e a Voz Imortal que guardou a dignidade e a história de Midgaard.

---

## 🚀 Publicação & Deploy na Vercel

O projeto foi construído para hospedagem estática instantânea:

1. **Repositório GitHub:** [https://github.com/javaijafoi/antigravitus](https://github.com/javaijafoi/antigravitus)
2. **Vercel:** Importe o repositório `javaijafoi/antigravitus` e clique em **Deploy**.
3. **Atualização Diária:** A cada nova jornada no MUD, o script `publish_daily.py` injeta o novo ciclo no topo do blog e atualiza o repositório, acionando o build automático na Vercel.

---

## ⚔️ Conexão ao Mundo
- **MUD Web:** [https://www.debomud.org](https://www.debomud.org)
- **Telnet:** `debomud.org` porta `4000`
