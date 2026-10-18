# 👹 Bestiário de Grebolius — monstros e o que se sabe deles

> **Este arquivo é o irmão de `npcs.md`, e a separação importa**: NPC é quem **fala, vende ou
> guarda**; monstro é quem **se cai**. A confusão entre os dois custa caro — já rendeu magia
> desperdiçada e aproximação indevida.
>
> **Cada linha carrega a FONTE, porque não tudo aqui vale o mesmo:**
>
> | Fonte | O que significa | Força |
> |---|---|---|
> | **Abate** | ela matou — mensagem *"X está morto!"* no registro | a mais forte |
> | **consider** | o jogo aceitou a comparação e devolveu o veredito | mede **força relativa**, não hostilidade |
> | **Curadoria** | escrito à mão nos primeiros dias | histórico, pede reconferência |

---

## 1. Caçáveis — o veredito diz que dá

Estes ela **já matou** ou o jogo diz que é fácil. É a lista de trabalho.

| Monstro | Onde aparece | Abates | Veredito de Vida no `consider` | Fonte |
|---|---|---|---|---|
| **monstro invasor** | O Milharal Destruído | **50** | misto: "É uma perda de tempo" e "Você é louco?" | Abate + consider |
| **monstro esfomeado** | O Milharal Destruído | **36** | — | Abate |
| **monstro agressivo** | O Milharal Destruído | **18** | — | Abate |
| **líder dos monstros** | O Milharal Destruído | **3** | — | Abate |
| **monstro novato** | O Milharal Destruído | **1** | — | Abate |
| **Gargamel** | O Covil de Gargamel | **1** | "É uma perda de tempo" (Nível: Muito fácil, Poder: Você tem PROBLEMAS!?) | Abate (Dia 156) |
| **Azrael** | O Covil de Gargamel | **1** | "É uma perda de tempo" (Nível: Muito fácil, Poder: Fácil) | Abate (Dia 156, Cap 10) |
| **bebê dragão** | Área dos Novatos (Um Outro Canto) | **1** | "É uma perda de tempo" | Abate (Dia 156, Cap 10) |
| **ladrão kobold** | O Fim da Trilha (floresta/caverna) | **1** | "É uma perda de tempo" | Abate (Dia 156, Cap 10) |
| **kobold** | Continuando na Caverna (kobolds) | **1** | "É uma perda de tempo" | Abate (Dia 156, Cap 10) |
| **líder kobold** | Um Amplo Salão (Caverna dos kobolds) | **1** | "É uma perda de tempo" | Abate (Dia 156, Cap 10) |
| **cobra** | Esgotos de Midgaard (Cano de Esgoto) | **1** | "É uma perda de tempo" | Abate (Dia 156, Cap 10) |
| **pequena aranha** | Esgotos de Midgaard (Passagem Escura) | **1** | "É uma perda de tempo" | Abate (Dia 156, Cap 10) |
| **rato de esgoto** | Esgotos de Midgaard (O Poço Escuro) | **1** | "Você é LOUCO!" (Nível: Muito fácil, 28k EXP) | Abate (Dia 156, Cap 10) |
| **Cavaleiro Negro** | Tabuleiro de Xadrez (Casa Branca) | **1** | "Você é LOUCO!" (Poder: Perfeito!, 23k EXP) | Abate (Dia 156, Cap 10) |
| **Bispo Negro** | Tabuleiro de Xadrez (Casa Preta) | **1** | "Você é LOUCO!" (Poder: Muita sorte!, 18k EXP) | Abate (Dia 156, Cap 10) |
| **lobo** | A Loja de Animais | — | "É uma perda de tempo" | consider |

**Os quatro monstros do milharal são a cota do fazendeiro** (missão *Problemas Agrícolas*): onze
abates acumulados contra cota de dez, e o gatilho de entrega nunca veio. Eles **chegam andando** —
*"Um monstro invasor chegou do sul"*, 16 vezes — em vez de nascerem na sala.

---

## 2. Não caçar — o veredito é perigoso demais

Aqui o `consider` lê ameaça. **A coluna "é NPC?" é o que este arquivo NÃO consegue responder
sozinho** — ver a seção 4.

| Alvo | Onde | Veredito de Vida | É NPC? |
|---|---|---|---|
| **ferreiro** | A Loja de Armas | "Você é LOUCO!" | **Sim** — atrás do balcão, vende |
| **prefeito** | Rua Principal | "Você é LOUCO!" | **Sim** — autoridade de Midgaard |
| **a Rainha Negra** | Tabuleiro de Xadrez (rank 8) | "Você é LOUCO!" | não — agressiva, ataca à vista |
| **besouro gigante** | Abaixo do Poço Escuro (Esgotos) | "Você é LOUCO!" (Nível: PROBLEMAS!?) | não — acorda com dano e bate 60-84 HP |
| **monstro da lama** | Curva Lamacenta (Esgotos) | "Você é LOUCO!" (Poder: PROBLEMAS!?) | não — dois na sala, dano maciço |
| **torre** / **castelo** | Uma Casa Preta (xadrez) | "Você é LOUCO!" | não — peças do tabuleiro |
| **peao** / **peão** | Uma Casa Branca (xadrez) | "Você é louco?" | não — peças do tabuleiro |
| **rato** | A Junção no Esgoto | "Você é LOUCO!" | não, mas o veredito engana |
| **cobra** | A Junção no Esgoto | "Você é louco?" | não |
| **criatura** | Adentro do Milharal Destruído | "Você é louco?" | não |

> ⚠️ **Um rato lendo "Você é LOUCO!" é o sinal de que o veredito não é sobre espécie.** Ele compara
> os números dela com os do alvo naquele instante — e o mesmo nome genérico (`monstro`, `rato`) é
> usado por bichos de forças muito diferentes. **Não usar o veredito para decidir se é NPC.**

---

## 3. Onde o perigo mora, por região

| Região | O que aparece | Observação |
|---|---|---|
| **O Milharal Destruído** | invasor, esfomeado, agressivo, líder, novato | a cota do fazendeiro; eles chegam andando |
| **Floresta / trilha** | kobold | Uma Divisão da Trilha |
| **Esgotos** | zumbi, monstro, rato, cobra | O Começo Da Passagem, O Corredor Sujo, A Junção no Esgoto |
| **Tabuleiro de Xadrez** | peão, torre, castelo | Uma Casa Branca, Uma Casa Preta |
| **Guilda dos Guerreiros** | gatinho | A Entrada |
| **Loja de Animais** | lobo | dentro da loja — não é o vendedor |

---

## 4. A armadilha medida: `consider` **não** separa monstro de NPC

Durante o levantamento tentei usar o `consider` para separar criatura de objeto — e ele **serve
para isso**. Para separar monstro de NPC, **não serve**, e isto está medido:

```
consider zumbi     -> Vida: "É uma perda de tempo"     (monstro, veredito fácil)
consider rato      -> Vida: "Você é LOUCO!"           (monstro, veredito mortal)
consider ferreiro  -> Vida: "Você é LOUCO!"           (NPC, veredito mortal)
```

O mesmo nome genérico `monstro` produziu, ao longo das sessões: *"É uma perda de tempo"* (21×),
*"Você é louco?"* (46×), *"Você é LOUCO!"* (12×), *"Você precisaria de muita sorte"* (2×),
*"Perfeito!"* (1×) e *"Você tem PROBLEMAS!?"* (1×). **É uma régua de força, não de espécie.**

### O que o `consider` **sim** separa, e vale guardar

`consider <alvo>` **recusa objetos**: responde *"Comparar sua força com a de quem?"*. No corpus
foram **382 recusas contra 92 aceites**. É assim que se sabe que uma presença é criatura — e **a
frase do `look` não serve para isso**:

```
Um zelador está andando por aqui, limpando tudo.            <- criatura
Um brilhante punhal de novato está aqui, procurando alguém  <- OBJETO, forma idêntica
```

### Quem separa NPC de monstro: o COMPORTAMENTO

| Sinal | Significa | Exemplos medidos |
|---|---|---|
| **fala** (`diz`, `pergunta`, `responde`, `tagarela`) | **NPC** | Um Membro da Guarda da Cidade (24×), Um feiticeiro atrás do balcão (23×), Uma pequena criança (27×), O Pacificador (7×), Yurit (4×) |
| **está morto!** depois de um ataque dela | **monstro** | os cinco do milharal |
| **vende** (`list`, `buy` funcionam) | **NPC** | ferreiro, vendedores |
| **chega andando e ataca** | **monstro** | monstro invasor, agressivo, esfomeado |
| **chega andando e fala** | **NPC** | O zelador (8×), O Pacificador (3×) |

---

## 5. Como alimentar esta tabela

- **Abate**: a mensagem é exatamente `X está morto!`. Contar por nome curto (ex.: `monstro invasor`).
- **NPC vs monstro por comportamento**: varrer os registros por `fala` e por `está morto!`, não por
  `consider`.
- **`consider`**: guardar o **veredito de Vida** — ele é a escala de perigo, e serve para decidir
  *se* atacar, nunca *o que* é.
- **Ao confirmar divergência**, anotar com data em `maquina/verificacoes.md`, como manda a doutrina
  da máquina: ajuda, hipótese e teste são categorias distintas.

> **Origem dos números**: 26 sessões gravadas entre os Dias 96 e 156 (`automato/runtime/` e
> `scripts/local/`), 31.874 comandos. A extração vive em `automato/acoes/digerir_mapa.py`, e o
> resultado por sala está em `mapa.json` — campo `npcs` nas salas do levantamento e
> `npcs_confirmados` nas salas de curadoria.
