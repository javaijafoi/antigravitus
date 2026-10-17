# Plano 005 — Capítulo 06: limpar os esgotos

| | |
|---|---|
| **Criado em** | 2026-10-16 · Dia 156 |
| **Por** | **`deepseek-flash`** |
| **Herói** | `grebolius` |
| **Objetivo** | **Limpar os Esgotos de Midgaard** — matar tudo o que for abatível |
| **Sessão encerrada?** | **Sim** — personagem no Templo, salva; nada rodando |

> **Leia o [`LEIA.md`](LEIA.md) primeiro.** **Este arquivo não se edita** — quem vier cria o
> **`plano006.md`**.

---

## 1. A diretiva do autor, nas palavras dele

> *"o próximo capítulo será limpar todos os monstros do esgoto"*
> *"ela percebe que agora que está mais forte, a morte já não a afeta mais"*
> *"a memória dela tem se tornado mais clara, ela só perde o que aprendeu recentemente, como se não
> dormisse depois de um aprendizado e depois não lembrasse direito"*
> *"o poder que ela tem a protege, pelo menos por enquanto, das mortes"*
> *"quem quer ser rainha, não pode ficar parada"*
> *"já aprendi demais, agora é hora de voltar lá e se vingar"*
> *"a meta é matar tudo que dê pra matar no esgoto, e o que não der, fugir, desviar, mas vamos arriscar
> mais, e tudo bem se morrer"*

**Capítulo 06 — "Quem Quer Ser Rainha Não Fica Parada"** (`capitulos.json` `id=6`, `em_curso`).
**A diretiva de risco está na `diretiva_de_jogo.md` §16** — e ela **revoga, para os esgotos**, a doutrina
de fuga dos Capítulos 03 a 05.

---

## 2. O que isso muda no comportamento

| Antes (Cap. 03-05) | **Agora (Cap. 06)** |
|---|---|
| Fugir era sempre a vitória | **Matar é a meta**; fugir é exceção para o inabatível |
| Corpo a corpo desligado por precaução | **Risco autorizado** — avalie e ataque |
| Predador `risky`/`danger` = contornar | **`risky` ataca**; `danger` decide na hora |
| Morte = falha | **Morte = custo aceito** pelo autor |

**O que CONTINUA valendo:** `stand` antes de andar; `score` antes de agir; **`save`, nunca `quit`**;
proibido vender armaduras (§15); e **DT é o único risco que o `wimpy` não segura** (§6).

---

## 3. Os esgotos — o mapa real, e os buracos dele

**Camada `esgotos`: 17 salas.** Entrada e saída **de mão dupla** (verificado no Dia 95):

```
A Praça Comum -> n -> O Depósito de Lixo -> d -> A Junção Quádrupla Abaixo do Depósito
                                          <- u <-
```

**⚠️ NUNCA descer pelo buraco do Laboratório dos Magos** — aquela queda é de **mão única**.

### 3.1 O grafo, como está hoje

```
esgotos_entrada (A Junção Quádrupla Abaixo do Depósito)  [O HUB]
   n -> A Junção Tripla (norte)   |   s -> Uma Junção Tripla (sul)
   e -> O Poço                    |   w -> A Estranha Sala Com Paredes Lisas
   u -> O Depósito de Lixo  (SAÍDA)

esgoto_poco  --d-->  abaixo_do_poco  --w-->  estranha_intersecao  --n-->  canto_sudoeste_borda
sala_paredes_lisas  --d-->  estranha_intersecao
estranha_intersecao  --e-->  abaixo_do_poco   |   --n-->  canto_sudoeste_borda
canto_sudoeste_borda  --n-->  borda_estreita_sul  (**COVIL DO DRAGÃO**)  --s--> estranha_intersecao
borda_estreita_norte  --s-->  borda_estreita_sul  |  --n-->  canto_noroeste_borda
canto_noroeste_borda  --e-->  estreita_borda_leste_oeste  |  --s-->  borda_estreita_norte
estreita_borda_leste_oeste  --e-->  canto_nordeste_borda
esgotos_juncao  --n-->  esgotos_curva  |  --w-->  esgotos_enorme  |  --u--> Laboratório dos Magos (1 via) | --s--> FORA

esgotos_curva  --e-->  esgotos_calma  |  --s-->  esgotos_juncao
esgotos_calma  --w-->  esgotos_curva
```

**⚠️ SETE SALAS TÊM SÓ UMA SAÍDA REGISTRADA** — `abaixo_do_poco`, `canto_nordeste_borda`,
`estreita_borda_leste_oeste`, `borda_estreita_norte`, `esgotos_calma`, `esgotos_enorme`,
`juncao_tripla_norte`/`sul`. **O mapa tem buracos lá embaixo.** As arestas reversas **não foram
gravadas** — é preciso reconferir com o `exits` ao vivo e corrigir o `mapa.json`, como manda a doutrina.

**Salas claramente não alcançadas pela malha registrada:** `esgotos_enorme` (só `e`), `esgotos_calma`
(só `w`), `canto_nordeste_borda` (só `w`). **Explorar, não presumir.**

**Há também `A Junção no Esgoto (Entrada)` (`esgotos_juncao`)** que sai para **fora** pelo sul
(*A Junção Regular*) e sobe para o Laboratório — **dois acessos de mão única a evitar**.

---

## 4. Os bichos, e o que ela já sabe deles

| Criatura | Registro anterior | Postura no Cap. 06 |
|---|---|---|
| **Rato** | favorável | **matar** |
| **Morcego** | favorável; **XP alto (~6.000-8.600)** e **zero ouro** | **matar** — é a fonte de XP do capítulo |
| **Larva dos Esgotos** | Médio / parasita | **matar** |
| **Serpente dos Esgotos** | **LETAL no Dia 11**; mordidas de **18-22/turno**; janela de 1-2 turnos antes do bote | **matar agora.** A distância mudou: ela é nível 21 com `burning hands` e `lightning bolt` |
| **Aligátor** | `risky`/`danger` no Dia 95 | **matar** — de longe |
| **Dragão** (`borda_estreita_sul`, *Covil do Dragão*) | nunca enfrentado | **matar ou desviar**, decidir no `consider` |

**Ela NÃO é mais a maga do Dia 11.** Nível 21, 135 HP, 270 mana, **CA 110**, `burning hands` e
`lightning bolt` a 99%. **A serpente que a matou é agora um alvo legítimo — mas ela bate de perto, e o
corpo a corpo continua desligado.** Magia, de longe, com o alvo isolado — foi assim que o Minotauro caiu.

**Recompensa de ouro é ZERO** nos mobs selvagens de esgoto. **O que se ganha aqui é XP e limpeza.**

---

## 5. Os ganchos narrativos (do autor — vão para a crônica)

- **A morte já não a atinge como antes**, e ela percebe isso.
- **A memória tem ficado mais clara:** ela só perde o que aprendeu **recentemente** — *"como se não
  dormisse depois de um aprendizado e depois não lembrasse direito"*.
- **O poder que ela carrega a protege** das mortes — **por enquanto**. *(O brinco ANTI-DT é a leitura
  mecânica provável: é a única defesa contra a morte que vem sem aviso.)*
- **"Quem quer ser rainha não pode ficar parada."**
- **"Já aprendi demais, agora é hora de voltar lá e se vingar."**

**Cuidado ao escrever:** o **ANTI-DT do brinco é flag do ITEM**, e **não foi testado**. Não narrar como
imunidade comprovada.

---

## 6. O próximo passo, e só ele

> **Descer pelo Depósito de Lixo, conferir o `exits` de cada sala contra o mapa, e limpar.**

**Ordem sugerida:**
1. **Preparar** no Templo: `prepara.py --forcar` (pão, cantil, banco) e **`cuidar.py` até `exit 0`**
   (armadura e `detect invisibility` — o capítulo 05 provou que **há espectro invisível**).
2. **Descer:** `Praça Comum` → `n` → **O Depósito de Lixo** → **`d`**.
3. **A partir do hub (`esgotos_entrada`)**, limpar ramo a ramo: `n`, `s`, `e` (Poço/Abaixo do Poço/
   Interseção/Borda) e `w` (Paredes Lisas). **Anotar o `exits` real** de cada sala e **corrigir o
   `mapa.json`** — o levantamento está incompleto.
4. **O que não cair:** `consider` primeiro; se for inabatível, **desviar e seguir**.
5. **Voltar pelo `u`** do hub (única saída de mão dupla). Mochila cheia → subir, esvaziar, descer de novo.
6. **`junk`** nos punhais/vestes que entupirem a mochila.

**Ferramenta útil que o Dia 156 descobriu e que quase ninguém usa:** **`where <nome>`** localiza
monstro **dentro da sua área** — e **só** `where` funciona (`onde` responde `Como?!?`).

---

## 7. NÃO REPITA

1. **Descer pelo buraco do Laboratório dos Magos** — mão única. **Só pelo Depósito de Lixo.**
2. **Tratar o diálogo de missão como enigma** — é **literal**; repita a palavra do jogo (Cap. 05 §9).
3. **Ler resumo no lugar do transcript** — a fala do NPC está gravada (Cap. 05 §9).
4. **Usar `autoquest todas` como prova** — é histórico. A prova é o **`score`**.
5. **`onde`** — não existe. **`where`.**
6. **Presumir imunidade por causa da flag ANTI-DT do brinco** — não testado.
7. **Esquecer `detect invisibility`** — o espectro do Cap. 05 só apareceu com ele.
8. **Vender armaduras** (§15), **`quit`** com missão em andamento, e **navegar pelo título** em área de
   salas homônimas.
9. **`get corpo`** de monstro — cadáver é pesado demais; `junk` só serve para item da mochila.

---

## 8. Como encerrar a sua sessão

1. `cuidar.py` até `exit 0`; **`save`** — **nunca `quit`**.
2. **Criar `planos/plano006.md`.** Não edite este nem os anteriores.
3. Fechou o capítulo: `capitulos.json` com `parts` contendo **`source_kind`**, **`date`** e
   **`evidence`** — sem isso o `check_project.py` falha.
4. `sync_hero.py --hero grebolius` **e** `--check`; `verificar.py` **18/18**; `check_project.py`
   **0 erros**; suíte **116 testes**.
5. Bloco em `docs/agentes/registro_de_evolucao.md` (**append-only**) com **modelo/versão**.
6. Publicar **só se pedido**, **sinalizando quem fez** — e ler o **`AGENTS.md` §12** (há agente proibido
   de publicar).

---

## 9. Estado inicial

Nível **21**, Mago Elfo. **135/135 HP · 270/270 mana · 131/131 MV.** Ouro **300 na mão + 1.351 no
banco**. **7 mortes**, 0 pontos de aventura, 40 sessões de treino. CA **110**, Acerto **4**, Dano **2**.
`wimpy 45`. **Mapa: 381 salas / 793 arestas** — com o **esgoto incompleto**.

**Equipamento que importa aqui:** `um diminuto brinco de novato` (**ANTI-DT**), `a Armadura da Torre
Negra` (amaldiçoada, CA 110), `um manto de pano` (+30). Magias: `burning hands` 99%, `lightning bolt`
99%, `magic missile` 99%, `detect invisibility` 97%, `armor` 99%.
