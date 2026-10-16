# Plano 001 — Capítulo 05, as duas autoquests

| | |
|---|---|
| **Criado em** | 2026-10-16 · Dia 156 |
| **Por** | **`deepseek-flash`** |
| **Herói** | `grebolius` |
| **Objetivo** | Fechar as **duas autoquests** do Capítulo 05 |
| **Sessão encerrada?** | **Sim** — nada rodando, personagem salva |

> **Leia o [`LEIA.md`](LEIA.md) desta pasta primeiro** se não sabe como os planos funcionam.
> **Este arquivo não se edita.** Quem vier depois cria o **`plano002.md`**.

---

## 1. Onde o objetivo está

**As duas missões já estão ATIVAS — não inicie de novo.**

```
[Autoquests em andamento]
Novela dos Novatos: Você deve dizer algo ao personagem.
Limpando Monstros: Você deve matar criatura.
```

| Missão | Iniciada | Fechada | Falta |
|---|---|---|---|
| **Limpando Monstros** | ✅ *Novato Alquimista*, `say sim` | ❌ | **abates** |
| **Novela dos Novatos** | ✅ *Smart Newbie*, `say sim` | ❌ | **disparar o `say`** |

**As duas valem.** *(Dicas Mágicas e Problemas Agrícolas foram vetadas pelo autor.)*

O capítulo é **"Amanhã Eu Começo por Elas"** — `capitulos.json` `id=5`, `kind=marco`, **`em_curso`**.
**Não é sobre as portas**: o autor re-escopou para as duas missões.

---

## 2. Estado exato

| | |
|---|---|
| Personagem | Nível **20**, Mago Elfo, 1ª encarnação |
| Vida / mana / movimento | **113/113 · 260/260 · 114/114** |
| Fome e sede | **nenhuma** |
| Ouro | **340 na mão + 1.142 no banco** (1.482) |
| Mortes | **7** (nenhuma nesta sessão) |
| `wimpy` | **45** *(o perfil pede 34; a diretiva §6 manda 45 por causa de armadilha mortal)* |
| Equipamento | Armadura da Torre Negra (**amaldiçoada**), espada curta, Acerto 3 / Dano 1 / CA 110 |
| Mochila | cantil, pães, Cruz Ansada, colar púrpura, pergaminho de sabedoria, mochila de Pellinore, **a coleira do dragão** *(pista falsa, §6)* |
| Local | **O Templo de Midgaard** |
| Mapa | **381 salas / 793 arestas** |
| Pontos de Aventura | **0** |

---

## 3. O que já foi descoberto (não redescubra)

### 3.1 O padrão de diálogo do DeBo — a lição mais cara

**Toda autoquest começa com o NPC falando primeiro, e a personagem respondendo.** Não é comando de
aceitar: é **diálogo**.

| Missão | O NPC perguntou | Resposta |
|---|---|---|
| Problemas Agrícolas | *"Ei, quer fazer uma boa ação hoje?"* | `say sim` |
| Dicas Mágicas | *"Começando suas aventuras?"* | `say sim` |
| Limpando Monstros | o Alquimista falou | `say oi` → `say sim` |
| Novela dos Novatos | o Smart Newbie falou | `say oi` → `say sim` |

➡️ **Para a Novela avançar, um novato tem que FALAR.** Nenhum falou em sessão alguma.

### 3.2 Onde cada novato nasce (dos `docs/circlemud`)

| Novato | Sala padrão | No mapa | Frase do jogo |
|---|---|---|---|
| **Smart Newbie** (18615) | 18645 | **A Sacada (sul)** | *"aparenta estar bem confiante"* |
| Annoying Newbie (18611) | 18646 | Caminho Iluminado (leste) | *"perturbando você"* |
| **Friendly Newbie** (18613) | 18640 | **A Sala da Estátua** | *"**falando muito**"* ← a *novata tagarela* |
| Clueless Newbie (18612) | 18642 | A Escadaria Norte | *"parecendo muito confuso"* |
| **Lost Newbie** (18614) | 18604 | **A Passagem Estreita** | *"está perdido aqui"* |

**A novata tagarela é a única descrita como "falando muito"**, e o objetivo é *"dizer algo ao
personagem"*. **Ela só foi vista CHEGANDO** (*"A novata tagarela chegou do norte"*), nunca falando.

### 3.3 Rotas verificadas (o mapa **erra** nestas áreas)

```
Zona dos Novatos:  Templo -> n,n,n,n,e,n   (O Começo Da Passagem)
                   e,e,s,s,n,n             (O Cruzamento)
                   open norte -> n -> Um Caminho Iluminado -> n -> A Sala da Estátua
                   e,e -> O Salão, A Escadaria Norte
                   u   -> A Sacada (norte)  ->  s  -> A Sacada (sul)

Jareth:            Templo -> n,n,n,n,n,n,e,n,n,n,e,e,e,e,e   (O Centro da Cidade)
Avenida Floris:    abre de O Portão Leste de Jareth (lv056) -> w
Distrito novo:     Templo -> n,n,n,n,n -> w -> A Entrada da Vila Residencial -> w -> Uma Rua Larga
```

**⚠️ Nunca use o título para saber onde está no Grande Campo** — ~10 salas com o mesmo nome. **A
identidade confiável é a impressão digital do `exits`** (o conjunto de destinos).

### 3.4 A vantagem que ninguém usou ainda

**`autoquest loja`** (dentro do Templo) teleporta para **"O Templo dos Aventureiros"** — 16 itens
divinos por **Pontos de Aventura**:

| Item | PA | Nível | Efeito |
|---|---|---|---|
| bracelete de Osiris | 15 | 2 | armadura **+30**, ANTI-DT |
| **franjas coloridas de careto** | **20** | 3 | **armadura +100**, ANTI-DT |
| **pequeno vortex em forma de argola** | **25** | 0 | **IMUNE-DT**, contêiner 1200 kg |

**A CA dela hoje é 110.** DT é a **armadilha mortal** que o `wimpy` **não segura** — o único risco que
o motor não sabe evitar. **Fechar as autoquests é o caminho para isso.** A sala não tem saída: sai com
`recall`. E **`list <número>` mostra a ficha completa do item** — a **única loja onde se inspeciona
antes de comprar**.

---

## 4. Os bloqueios, e o que já foi tentado

### Limpando Monstros — abates

**A zona 186 seca.** Uma passada boa **esvazia a masmorra**, e ela repovoa devagar: medido **1 a 4
abates por ciclo**, com ciclos inteiros sem nada, ao longo de dezenas de minutos.

**Já tentado:** patrulhas em 6+ ciclos; varredura das 53 salas; espera de 4 min; **ataque ao Grande
Minotauro** — que **existe e é abatível**, mas **não de adaga**.

### Novela dos Novatos — o `say` não dispara

**Já tentado, sem reação:** ~35 frases com `say` (saudações, `sim`, `yes`, `nao`, o nome dela, frases
temáticas), **9 tópicos** com `ask`, **3 itens** com `give`, `tell` com a chave `tagarela` — em **4 dos
5 novatos**, **com eles presentes**.

**O que resta sem testar:** o **Lost Newbie** (nunca visto) e **estar presente no instante em que um
deles falar**.

---

## 5. O próximo passo, e só ele

> **Vigiar os novatos até um deles FALAR, e responder.**

Não fale no vácuo — foi o que eu fiz por rodadas. **Os cinco endereços estão no §3.2.** A **novata
tagarela** é a candidata mais forte.

**Em paralelo, os abates.** A ronda barata é a que **não usa `recall`** por sala checada — o laço do
§3.3 cobre as salas dos novatos em **14 passos**.

**Ordem sugerida:** patrulhar a zona (abates) **enquanto** vigia as salas dos novatos. As duas missões
no mesmo passeio.

---

## 6. NÃO REPITA

1. **A coleira do dragão** — o **autor confirmou: a missão do dragão JÁ FOI FEITA.** Pista falsa. *(Eu
   estava com ela no inventário, prestes a entregá-la.)*
2. **O Andarilho Misterioso** — *"Energias obscuras… Uma Cela de Prisão"* é **evento de mundo**
   (`help andarilho`), **não** pista da missão.
3. **Tratar `say` como comando** — é **diálogo**; só funciona como **resposta a quem falou**.
4. **Digerir corpus parcial** — levou o mapa de **360 para 224 salas**. O `--glob` precisa cobrir
   **todo** o corpus. Sintoma: o `TOTAL` do `fundir_mapa.py` **diminuir**.
5. **Navegar pelo título no Grande Campo** — use o **`exits`**.
6. **Vender armaduras** (Torre Negra ou peão) — **diretiva do autor**.
7. **`quit` com missão em andamento** — **zera o progresso**. Use **`save`**. Queda **não** zera.

---

## 7. Ferramentas e comandos

| Ferramenta | Para quê |
|---|---|
| **`docs/circlemud/`** | **A fonte que resolveu seis rodadas.** A Zona dos Novatos **é o `186.wld` padrão**: mob por mob, sala por sala, com o item que cada um carrega |
| `automato/rotinas/mercado.py` | Audita lojas (`visible` + `list`) |
| `camadas/prepara.py` | Saca ouro (alvo 300) e **revisa a Sala de Doações** |
| `acoes/fundir_mapa.py` | Mescla o levantamento |
| `data/heroes/grebolius/andarilho_e_novatos.md` | **Todos os textos literais** das duas missões |
| `data/heroes/grebolius/diretiva_de_jogo.md` | **Leia antes de jogar** |

```
python automato/nucleo/driver/play.py "<comando>"     # comando avulso
python automato/camadas/cuidar.py                     # come, bebe, magias (exit 0/1/2)
python automato/camadas/prepara.py --forcar           # padaria, fonte, banco, doações
python automato/camadas/turno.py --rotina <n> --turnos N --socorrer
python automato/verificar.py                          # 18/18
python scripts/check_project.py                       # 0 erros
```

**Combate:** `consider` antes de atacar; **`cast 'burning hands'`** é o dano principal (mata de primeira
o monstro novato); **corpo a corpo está DESLIGADO** — **nunca use a adaga**. Fugir é vitória.

### Armadilhas do motor que custam rodada

| Sintoma | Causa | O que fazer |
|---|---|---|
| `list` de loja não responde | **invisibilidade bloqueia comércio** | **`visible`** antes |
| `get corpo` recusado | cadáver é **pesadíssimo** | não insista |
| Mochila fecha sem avisar | entulho de punhais/vestes | **`junk punhal` / `junk veste`** por lote |
| Busca de NPC falhando | filtro casando com **"monstro novato"** | exclua `monstro` do filtro |
| Magia não pega | **Templo e Loja de Magias bloqueiam** | conjure na **Praça do Templo** |

---

## 8. Como encerrar a sua sessão (a mesma obrigação que gerou este plano)

1. `cuidar.py` até `exit 0`.
2. **`save`** — **nunca `quit`**.
3. **Criar `planos/plano002.md`** (o próximo número) com o modelo do `LEIA.md`. **Não edite este.**
4. `python scripts/sync_hero.py --hero grebolius` e `--check`.
5. `python automato/verificar.py` (18/18) e `python scripts/check_project.py` (0 erros).
6. Bloco em `docs/agentes/registro_de_evolucao.md` (**append-only**) com **modelo/versão**.
7. Se mexeu no motor: `automato/CHANGELOG.md` (+ `DECISOES.md` se houve decisão com custo).
8. `publish_daily.py --publish --push` — e **confira `git status` antes e depois**: a árvore é
   compartilhada com outras conversas do mesmo agente.

---

## 9. Fios soltos (não bloqueiam)

- **33 portas nomeadas** por abrir — placar do Capítulo 04, adiado por decisão do autor.
- **Jareth** e a **Avenida Floris** nunca foram visitados (rotas no §3.3).
- A **coleira do dragão** está na mochila — pode ser descartada (`junk`); **não é da missão**.
