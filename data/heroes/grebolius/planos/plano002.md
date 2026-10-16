# Plano 002 — Capítulo 05 fechado; escolher o 06

| | |
|---|---|
| **Criado em** | 2026-10-16 · Dia 156 |
| **Por** | **`deepseek-flash`** |
| **Herói** | `grebolius` |
| **Objetivo** | **O Capítulo 05 está CONCLUÍDO.** Falta escolher e abrir o próximo |
| **Sessão encerrada?** | **Sim** — driver finalizado depois de `save`, personagem no Templo |

> **Leia o [`LEIA.md`](LEIA.md) desta pasta primeiro** se não sabe como os planos funcionam.
> **Este arquivo não se edita.** Quem vier depois cria o **`plano003.md`**.
>
> **O plano 001 fica como está** — ele descreve o problema que este plano resolveu. Não o apague: é o
> registro de que as duas missões foram perseguidas e por quais caminhos.

---

## 1. ✅ O Capítulo 05 está FECHADO

**As duas autoquests foram concluídas** — não há mais nada a fazer nelas.

```
Novela dos Novatos             Concluída
Limpando Monstros              Concluída
```

`capitulos.json` → capítulo 5, `status: "concluido"`, `closed_on_day: 156`, 12 parágrafos de narrativa.
**Evidência:** `evidence/dia156d.json`.

### Como cada uma fechou — porque o "como" vale mais que o "que"

| Missão | O que a fechou |
|---|---|
| **Novela dos Novatos** | **Falar com a novata tagarela** na Escadaria Norte. Não foi a frase: foi ser **resposta** a quem falou primeiro |
| **Limpando Monstros** | **Fazer o mico fugir** de cima do Novato Alquimista. Ele agradeceu, deu o manto e a missão fechou — **sem precisar matar o bicho** |

**A lição que custou mais rodadas do que qualquer outra:** o objetivo dizia *"Você deve dizer algo ao
personagem"* e eu tratei isso como **comando** — procurar a palavra certa. Era **diálogo**. Em toda
autoquest do DeBo, **o NPC fala primeiro e a personagem responde**. O plano 001 registrou essa hipótese;
o Dia 156 a confirmou.

---

## 2. Estado exato

| | |
|---|---|
| Personagem | **Nível 21**, Mago Elfo, 1ª encarnação |
| Vida / mana / movimento | **135 / 135 · 270 / 270 · 131 / 131** |
| Experiência | **1.200.001** (próximo em 1.400.000) |
| Ouro | **300 na mão + 1.351 no banco** (1.651) |
| Mortes | **7** (nenhuma nesta sessão) |
| Alinhamento | **181 — um pouco bom** |
| Acerto / Dano / CA | **4 / 2 / 110** |
| `wimpy` | **45** |
| Sessões de treino | **40** |
| Pontos de Aventura | **0** |
| Local | **O Templo de Midgaard** |
| Mapa | **381 salas / 793 arestas** |

**Equipamento novo desta sessão — os dois importam:**
- **`um diminuto brinco de novato`** (orelha) — **ANTI-DT**; +15 vida máx, +15 movimento máx, +1 acerto,
  +1 dano. Flags: `BRILHO NÃO-DOAR NÃO-INVISÍVEL NÃO-VENDER ANTI-DT ENTALHADO`. **É a primeira defesa
  contra armadilha mortal** — a única coisa que o `wimpy` não segura.
- **`um manto de pano`** (sobre o corpo) — armadura **+30**, recompensa do Alquimista.
- E **aprendeu a magia `curse`** a 10% (subiu de nível).

---

## 3. O que já foi descoberto (não redescubra)

### 3.1 O padrão de diálogo do DeBo — **confirmado**

| Missão | O NPC falou primeiro | Resposta |
|---|---|---|
| Problemas Agrícolas | *"Ei, quer fazer uma boa ação hoje?"* | `say sim` |
| Dicas Mágicas | *"Começando suas aventuras?"* | `say sim` |
| Limpando Monstros | o Alquimista | `say sim` |
| **Novela dos Novatos** | a novata tagarela | **`say oi`** ← fechou |

### 3.2 Onde cada novato nasce (dos `docs/circlemud`)

| Novato | Sala | No mapa | Frase do jogo |
|---|---|---|---|
| Smart Newbie (18615) | 18645 | A Sacada (sul) | *"aparenta estar bem confiante"* |
| Annoying Newbie (18611) | 18646 | Caminho Iluminado (leste) | *"perturbando você"* |
| **Friendly Newbie (18613)** | 18640 | A Sala da Estátua | *"falando muito"* ← **a tagarela** |
| Clueless Newbie (18612) | 18642 | A Escadaria Norte | *"parecendo muito confuso"* |
| Lost Newbie (18614) | 18604 | A Passagem Estreita | *"está perdido aqui"* |

**Ela ANDA:** foi vista na Escadaria Norte, na Passagem Estreita e na Sacada. **A missão fechou na
Escadaria Norte**, com ela presente.

### 3.3 Rotas verificadas (o mapa **erra** nestas áreas)

```
Zona dos Novatos:  Templo -> n,n,n,n,e,n   (O Começo Da Passagem)
                   e,e,s,s,n,n             (O Cruzamento)
                   open norte -> n -> Um Caminho Iluminado -> n -> A Sala da Estátua
                   e,e -> O Salão, A Escadaria Norte
                   u   -> A Sacada (norte)  ->  s  -> A Sacada (sul)

A Sala do Alquimista (o mico):  Templo -> n,n,n,e,n,e,e,s,s  ->  e  ->  u
A masmorra / Minotauro:         da Sala do Alquimista, `baixo` -> A Entrada -> ... -> Outra Curva

Jareth:            Templo -> n,n,n,n,n,n,e,n,n,n,e,e,e,e,e   (O Centro da Cidade)
Avenida Floris:    abre de O Portão Leste de Jareth (lv056) -> w
```

**⚠️ Nunca use o título para saber onde está no Grande Campo** — ~10 salas com o mesmo nome. **A
identidade confiável é a impressão digital do `exits`.**

### 3.4 O Grande Minotauro — **é abatível, e com magia**

Fica em **Outra Curva** (`18629` no padrão, *The Red Room* nas vizinhanças). **Já caiu**: `lightning
bolt` de longe, **1.600 + 1.944 de experiência, 95 moedas**. Ele **quase não sente** o corpo a corpo
(uma adaga mal arranha) — **a distância é a resposta**. Ele **repovoa**: os chifres e a pele estavam no
chão de novo na segunda passagem.

### 3.5 A vantagem que continua sem uso

**`autoquest loja`** (dentro do Templo) teleporta para **"O Templo dos Aventureiros"** — 16 itens
divinos por **Pontos de Aventura** (ela tem **0**):

| Item | PA | Nível | Efeito |
|---|---|---|---|
| bracelete de Osiris | 15 | 2 | armadura **+30**, ANTI-DT |
| franjas coloridas de careto | 20 | 3 | **armadura +100**, ANTI-DT |
| **pequeno vortex em forma de argola** | **25** | 0 | **IMUNE-DT**, contêiner 1200 kg |

A sala não tem saída: sai com `recall`. E **`list <número>` mostra a ficha completa** — a **única loja
onde se inspeciona antes de comprar**.

---

## 4. Os bloqueios — agora são de ESCOLHA, não de execução

**Não há missão travada.** O que falta é **decidir o próximo capítulo**. Os candidatos, em ordem de
valor aparente:

1. **As 33 portas nomeadas** do Capítulo 04 — nunca abertas. É a promessa que o capítulo 05 subverteu
   duas vezes.
2. **Jareth e a Avenida Floris** — rota conhecida, **nunca percorridas**. É mapa novo a custo baixo.
3. **Pontos de Aventura → IMUNE-DT** — as autoquests são a fonte; fechar mais é o caminho para a
   proteção que falta.
4. **As 18 regiões de `help mapas`** — só Midgaard, Jareth e a Zona dos Novatos foram tocadas.

**O que eu faria:** **Jareth**. É a única com rota verificada e sem risco conhecido, e destrava a
Avenida Floris de graça.

---

## 5. O próximo passo, e só ele

> **Escolher o objetivo do Capítulo 06 com o autor, e só então jogar.**

O 05 fechou. **Jogar sem alvo definido gasta rodada** — foi o que o 05 ensinou, e é o que o autor
cobrou. Se ele não decidir, o caminho de menor risco é **Jareth** (§4.2).

---

## 6. NÃO REPITA

1. **Tratar `say` como comando.** É **diálogo** — só funciona como resposta a quem falou. Custou
   **seis rodadas**.
2. **Falar no vácuo com os novatos.** ~35 frases, 9 tópicos de `ask`, 3 itens com `give`, em 4 dos 5
   novatos. **Nenhum respondeu a nada.** O que faltava era presença no momento certo, não a frase.
3. **A coleira do dragão** — **a missão do dragão já foi feita**. Pista falsa.
4. **O Andarilho Misterioso** (*"Energias obscuras… Uma Cela de Prisão"*) — **evento de mundo**
   (`help andarilho`), não pista de missão.
5. **Digerir corpus parcial** — levou o mapa de 360 para 224 salas. O `--glob` precisa cobrir tudo.
6. **Navegar pelo título no Grande Campo** — use o `exits`.
7. **Vender armaduras** — diretiva do autor.
8. **`quit` com missão em andamento** — zera o progresso. Use `save`.
9. **Trocar `next_objective` inteiro no `state.json`** sem manter **`missing_preparation`** — o
   `sync_hero.py` lê esse campo por nome e **quebra** (`'missing_preparation'`). Aconteceu comigo esta
   sessão.

---

## 7. Ferramentas e comandos

| Ferramenta | Para quê |
|---|---|
| **`docs/circlemud/`** | **A fonte que mais rendeu.** A Zona dos Novatos **é o `186.wld` padrão**: mob por mob, sala por sala, com o item que cada um carrega |
| `data/heroes/grebolius/andarilho_e_novatos.md` | Todos os textos literais das duas missões |
| `data/heroes/grebolius/diretiva_de_jogo.md` | **Leia antes de jogar** |
| `automato/rotinas/mercado.py` | Audita lojas |
| `automato/camadas/prepara.py` | Saca ouro (alvo 300) e revisa a Sala de Doações |

```
python automato/nucleo/driver/play.py "<comando>"     # comando avulso
python automato/camadas/cuidar.py                     # come, bebe, magias (exit 0/1/2)
python automato/camadas/prepara.py --forcar           # padaria, fonte, banco, doações
python automato/verificar.py                          # 18/18
python scripts/check_project.py                       # 0 erros
python scripts/sync_hero.py --hero grebolius          # regenera ficha.md / hero.json
```

**Combate:** `consider` antes; **`burning hands`** a 99% mata de primeira o monstro novato; **`lightning
bolt`** para o que é grande — **de longe**. **Corpo a corpo está DESLIGADO** (`allow_verified_melee =
False`): **nunca use a adaga**. Fugir é vitória.

### Armadilhas do motor que custam rodada

| Sintoma | Causa | O que fazer |
|---|---|---|
| `list` de loja não responde | **invisibilidade bloqueia comércio** | `visible` antes |
| `get corpo` recusado | cadáver é **pesadíssimo** | não insista; `junk` só serve para item da mochila |
| Mochila fecha sem avisar | entulho de punhais/vestes | `junk punhal` / `junk veste` por lote |
| Busca de NPC falhando | filtro casando com **"monstro novato"** | exclua `monstro` do filtro |
| Magia não pega | **Templo e Loja de Magias bloqueiam** | conjure na **Praça do Templo** |
| `sync_hero.py` com `missing_preparation` | campo faltando em `next_objective` | manter o campo (§6.9) |

---

## 8. Como encerrar a sua sessão (a mesma obrigação que gerou este plano)

1. `cuidar.py` até `exit 0`.
2. **`save`** — **nunca `quit`**.
3. **Criar `planos/plano003.md`** (o próximo número) com o modelo do `LEIA.md`. **Não edite este.**
4. Se fechou um capítulo: `capitulos.json` com `status`, `days`, `parts` (com **`source_kind`**,
   **`date`** e **`evidence`**), `content`, `tags`, `evidence`, `excerpt`, `closed_on_day`.
   **A `part` sem `source_kind` e sem `evidence` faz o `check_project.py` falhar.**
5. `python scripts/sync_hero.py --hero grebolius` **e** `--check`.
6. `python automato/verificar.py` (18/18), `python scripts/check_project.py` (**0 erros**),
   `python -B -m unittest discover -s scripts -p "test_*.py"` (**116 testes**).
7. Bloco em `docs/agentes/registro_de_evolucao.md` (**append-only**) com **modelo/versão**.
8. Se mexeu no motor: `automato/CHANGELOG.md` (+ `DECISOES.md` se houve decisão com custo).
9. `publish_daily.py --publish --push` — e **confira `git status` antes e depois**: a árvore é
   compartilhada com outras conversas do mesmo agente.

---

## 9. Fios soltos (não bloqueiam)

- **33 portas nomeadas** por abrir — a promessa não cumprida, agora duas vezes.
- **Jareth** e a **Avenida Floris** nunca visitados.
- **40 sessões de treino** sobrando.
- **`curse` a 10%** — aprendida agora, praticamente inútil até treinar.
- A **coleira do dragão** continua na mochila — pode ser descartada (`junk`); **não é de missão**.
- `data/heroes/grebolius/planos/plano001.md` **descreve o problema que este plano resolveu**. Fica.
