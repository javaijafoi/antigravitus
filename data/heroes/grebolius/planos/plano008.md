# Plano 008 — Capítulo 07: `Problemas Agrícolas`, a que ficou por fazer

| | |
|---|---|
| **Criado em** | 2026-10-16 · Dia 156 |
| **Por** | **`deepseek-flash`** |
| **Herói** | `grebolius` |
| **Objetivo** | **Concluir `Problemas Agrícolas`** — a missão que ela começou no Dia 90 e nunca entregou |
| **Sessão encerrada?** | **Sim** — personagem no Templo, salva; daemon no ar |

> **Leia o [`LEIA.md`](LEIA.md) primeiro.** **Este arquivo não se edita** — quem vier cria o
> **`plano009.md`**.
>
> **Antes de encerrar, rode `python scripts/devolutiva.py`** — é obrigatório desde o Dia 156 e
> **reprova** quem promete no plano e não grava no artefato (§8).

---

## 1. A missão, e por que ela importa agora

**Esta é a missão que ela abandonou.** No Dia 90 o Pacificador pediu, ela foi, matou **onze monstros
contra uma cota de dez** — e **a entrega nunca foi confirmada**. Depois disso ela foi fazer outras
coisas, e a missão foi perdida.

**Na ficção, é o capítulo dela voltando atrás:** *ela não gosta de deixar coisa por fazer.* O Capítulo
05 foi sobre descobrir que ela estava perseguindo a coisa errada; **este é sobre terminar a que ela
deixou no meio.**

> **Diretriz do autor (Dia 156):** *"vamos dar a missão para o próximo agente e ver se ele consegue
> fazer a do Problemas Agrícolas. Na ficção ela fala que não gosta de deixar coisas por fazer, que vai
> tentar de novo."*

**⚠️ Isto REVOGA o veto anterior.** A missão estava marcada como *"vetada pelo autor"* desde o Dia 150;
**não está mais.** É o objetivo do Capítulo 07.

**⚠️ O `Problemas Agrícolas` NÃO está ativo.** O `score` não tem bloco de autoquests e o catálogo diz
`Não feita`. **Tem de ser reiniciada do zero** — e é isso que torna este plano necessário.

---

## 2. Estado exato

| | |
|---|---|
| Personagem | **Nível 21**, Mago Elfo, 1ª encarnação |
| Vida / mana / movimento | **131/135 · 264/270 · 127/131** *(levemente ferida — comer, beber e descansar antes)* |
| Experiência | **1.219.294** (próximo em 1.400.000) |
| Ouro | **300 na mão + 1.351 no banco** (1.651) |
| Mortes | **8** — **e a #5 foi ARMADILHA MORTAL dentro do milharal** |
| Classe de Armadura | **111** (81 + 30 de `armor`) |
| `wimpy` | **45** |
| Magias | `burning hands` 99% · `lightning bolt` 99% · `magic missile` 99% · `detect invisibility` 97% · `armor` 99% · `curse` 10% |
| Pontos de Aventura | **0** |
| Local | **O Templo de Midgaard** |
| Mapa | **381 salas / 793 arestas** |

---

## 3. O caminho — verificado no Dia 90 e usado nas sessões do milharal

### 3.1 Passo 1: achar O Pacificador e reiniciar a missão

**Ele NÃO fica parado.** É visto na **Praça do Templo**, no **Término da Rua** e no **Portão Oeste** —
**vigília rotativa de ~5 minutos em três praças.**

**Para localizar, use `where` — não ande procurando:**
```
where pacificador        # localiza dentro da área
where                    # sozinho, lista os JOGADORES da área
```
> **`onde` NÃO existe** — o `help where` documenta `onde <alvo>`, e o servidor responde `Como?!?`.
> Só `where` funciona. (`maquina/verificacoes.md`)

**O gatilho é `say sim`** — e ele **fala primeiro**. O padrão de toda autoquest do DeBo é **o NPC
pergunta, ela responde** (`automato/DECISOES.md` §9).

**O briefing dele, literal** (do transcript, Dia 90) — é o mapa da missão:

```
O Pacificador diz: 'Ei, quer fazer uma boa ação hoje?'
O Pacificador diz: 'Vou ser bastante direto com você, pois a situação é grave.'
O Pacificador diz: 'Recebi uma carta de um fazendeiro que está com problemas em sua fazenda.'
O Pacificador diz: 'Ele, a esposa e o filho deles estão cercados por monstros horrendos.'
O Pacificador diz: 'Então o fazendeiro e sua família não conseguem sair de lá.'
O Pacificador diz: 'Preciso que vá ao encontro desse fazendeiro.'
O Pacificador diz: 'A fazenda fica para as bandas da floresta dos Kobolds, perto de Jareth.'
O Pacificador diz: 'Se não sabe, Jareth fica para o norte de Midgaard. Basta ir pela estrada.'
O Pacificador diz: 'Uma carroça sai da Praça do Comércio e segue para lá de tempos em tempos.'
O Pacificador diz: 'Quando chegar em Jareth, vá para leste até a Entrada da Floresta.'
O Pacificador diz: 'Você encontrará uma Divisão da Trilha ao norte.'
O Pacificador diz: 'Aí é só seguir para o leste e você chegará ao seu destino.'
O Pacificador diz: 'Mas cuidado! A floresta pode enganar quem é novo por aquelas bandas.'
```

### 3.2 Passo 2: ir até a fazenda

```
Templo -> 5 norte -> leste -> norte -> leste -> norte -> 9 norte   (rodovia e vila)
       -> leste até A Entrada da Floresta
       -> norte, norte            (Adentrando, Divisão da Trilha)
       -> leste pelo bosque, até uma sala cujo SUL abre A Entrada da Fazenda
       -> oeste, sul, oeste, oeste  ->  O Milharal Destruído
```

**Regras de trânsito que custaram rodada:**
- **O mapa acerta a topologia mas erra a contagem em 1-2 passos** no trecho de Midgaard e simplifica
  Jareth. **Use o mapa para planejar e o `exits` para confirmar.**
- **O bosque é de salas homônimas** (*"Num Bosque Iluminado"*). **Navegue pelas SAÍDAS, nunca pela
  memória nem pelo título.**
- **O milharal e as estradas também repetem título.** *"Nome igual não comprova sala igual."*

### 3.3 Ferramentas prontas — use antes de escrever código novo

| Ferramenta | O que faz |
|---|---|
| **`automato/rotinas/milharal.py`** | A rotina inteira: navega, conta mobs e mata. `MOBS = esfomeado, agressivo, invasor, bola…` |
| **`automato/acoes/encontrar_fazendeiro.py`** | Navega até a casa da fazenda |
| **`automato/acoes/falar_fazendeiro.py`** | Vai até a casa **e dialoga** com o fazendeiro |

```
python automato/rotinas/milharal.py                 # caça
python automato/acoes/falar_fazendeiro.py           # navega e fala
```

---

## 4. O bloqueio real: **A ENTREGA**

**Onze abates contra uma cota de dez — e o fazendeiro nunca confirmou.** É aqui que a missão mora.

**O que JÁ foi tentado** (nos transcripts), sem resultado:
```
ask fazendeiro invasores
ask fazendeiro missao
ask fazendeiro ajuda
ask Pacificador fazenda
ask Pacificador monstros
```

**O que NÃO foi tentado — e é onde eu apostaria, pela lição do Capítulo 05:**
1. **Ler o objetivo ANTES de agir.** `score tudo` **a cada passo** — a linha da missão diz o que ela
   quer, e **muda** conforme a etapa. *(No capítulo 05 eu falei/entreguei antes da hora e não contou.)*
2. **A palavra LITERAL do jogo.** O diálogo de missão é literal: `retornar` funcionou e `recall` não;
   `ajuda remortar` funcionou e `ajuda encarnação` não. **Não invente sinônimo** — use a palavra que o
   NPC usar.
3. **`give`** — entregar algo ao fazendeiro, se o `score` pedir objeto. *(Foi assim que a Novela
   fechou: entregar a veste à tagarela.)*
4. **Falar com a FAMÍLIA.** A esposa e o filho estão na casa (o briefing do Pacificador os cita), e
   **nenhum plano meu tentou falar com eles.** Eles podem ser o gatilho da entrega.

---

## 5. Os perigos — e um deles já matou

### ⚠️ ARMADILHA MORTAL dentro do milharal (Morte #5)

**Ela morreu em *"Adentro do Milharal Destruído"*, por DT, durante a caçada.** O `wimpy` **não segura
armadilha mortal** — é o único risco que o motor não evita.

**O que ajuda:** ela carrega `um diminuto brinco de novato` com a flag **ANTI-DT**.
**⚠️ MAS ISSO NUNCA FOI TESTADO.** Não trate como certeza — e **não vá testar de propósito**.

**A defesa real é a memória:** o `Passo-Em-Falso` (nos esgotos) **avisa antes**
(*"Você percebe que há algo perigoso por perto!"*). **Se o milharal avisar, PARE.**

### Os monstros

| Bicho | XP medido | Ouro medido |
|---|---|---|
| **monstro agressivo** | **2.484** | **50** |
| **monstro esfomeado** | **2.268** | **50** |
| monstro invasor | 846 | 50 |
| "estranha criatura" / "bola de pêlos" | não medido | ? |

**As salas têm de 1 a 4 monstros. A caçada rende ~2.400 XP + 50 de ouro por abate** — é o melhor
grind do jogo em ouro, e empata com o esgoto em XP.

**Combate:** `consider` antes; **`lightning bolt`** de longe, com o alvo isolado; **`burning hands`** no
que chegar perto. **Corpo a corpo está DESLIGADO** — nunca a adaga.

### Fome e sede

**A viagem é longa e a fome mata devagar.** `prepara.py --forcar` antes de sair, e `cuidar.py` no
caminho. **Regra do Dia 147:** sem comida, **não regenera** — e emagrece até morrer.

---

## 6. O plano de execução, em ordem

1. **Preparar no Templo:** `prepara.py --forcar` (pão, cantil, banco) e **`cuidar.py` até `exit 0`**
   (armadura + `detect invisibility`). Ela está com 131/135 — **descansar até encher**.
2. **Achar O Pacificador com `where pacificador`** (ele anda); `say sim` no briefing.
3. **Ler o `score` e ANOTAR a linha da missão** — é o objetivo, e ele muda.
4. **Ir à fazenda** (§3.2). No caminho, **conferir o `exits`** em cada sala-marco.
5. **Falar com o fazendeiro** (`falar_fazendeiro.py`) e **ler a resposta inteira** — os diálogos levam
   dezenas de segundos.
6. **Caçar** (`milharal.py`) até o `score` dizer que a cota fechou. **`score` entre cada abate.**
7. **Voltar ao fazendeiro e ENTREGAR** — `give` ou a palavra literal que ele usar.
8. **Se travar:** tentar **a esposa e o filho**; conferir se o `score` pede **objeto** em vez de abate.
9. **Fechar o capítulo** com narrativa e evidência (`parts` com `source_kind`, `date`, `evidence`).

---

## 7. NÃO REPITA

1. **`ask` como entrega** — foi tentado três vezes e não fechou. **A entrega é `give` ou palavra literal.**
2. **Falar/entregar antes de o `score` pedir** — não conta. **(Lição do Cap. 05.)**
3. **Inventar sinônimo** para a palavra do jogo. **Use a palavra do NPC.**
4. **Entrar no milharal sem preparo** — **lá tem armadilha mortal que já matou uma vez.**
5. **Navegar pelo título** no bosque, nas estradas ou no milharal — **salas homônimas.**
6. **Presumir que o brinco ANTI-DT imuniza** — **não foi testado.**
7. **`onde`** — não existe. **`where`.**
8. **`autoquest todas` como prova** — é histórico; a prova é o `score`.
9. **`quit` com missão em andamento** — **zera o progresso. É o que provavelmente perdeu esta missão.**
10. **Vender armaduras** (§15), e **digerir corpus parcial** de mapa.

---

## 8. Devolutiva técnica

> **Obrigatória** (LEIA.md §8), e **cobrada** por `python scripts/devolutiva.py`.

| Descobri | Registrei em | O quê |
|---|---|---|
| **mapa** | **`mapa.json` — PENDENTE** | **Quatro arestas dos anéis do esgoto continuam registradas como becos**, apesar de o `Gemini 3.8 Flash` ter andado e provado que são de mão dupla: `esgotos_entrada --w--> sala_paredes_lisas`, `esgoto_poco --d--> abaixo_do_poco`, `sala_paredes_lisas --d--> estranha_intersecao`, `canto_noroeste_borda --e--> estreita_borda_leste_oeste`. **Não gravei porque não andei — gravar sem verificar seria inventar.** **E este plano leva ao milharal, não ao esgoto: a pendência continua aberta.** |
| **referência do servidor** | *nada nesta sessão* | Os achados de servidor (o aviso prévio de DT, o rótulo `Você é LOUCO!`, a mordida de 135 HP do Dragão) foram registrados na sessão anterior, **não nesta**. Nada novo a acrescentar. |
| **fato do mundo** | **`conhecimento.md` §39** ✅ | **O veto do autor caiu** e **`Problemas Agrícolas` está PERDIDA** — não ativa: o `score` não tem bloco de autoquests e o catálogo diz `Não feita`. Mais o bloqueio histórico (a entrega nunca confirmada), o que já foi tentado com `ask`, o que **não** foi (o `give`, a palavra literal, **a esposa e o filho**), e os valores medidos dos três bichos da fazenda. **Também atualizei o `state.json` e o `automato/DECISOES.md`**, que ainda diziam "vetada". |
| **erro do motor** | *nada nesta sessão* | O motor não atrapalhou. **Mas a limitação conhecida continua e é a razão de eu ter corrigido este plano duas vezes:** o `check_project.py` confere **estrutura**, não **cobertura** — foi o `devolutiva.py` que pegou esta devolutiva declarando trabalho da sessão **anterior**. |

### O que esta sessão descobriu e vale para o próximo

- **A missão `Problemas Agrícolas` está PERDIDA**, não ativa — o `score` não tem bloco de autoquests e o
  catálogo diz `Não feita`. **Registrado aqui; é a informação que faltava para planejar.**
- **O veto caiu.** Ela voltou a ser o objetivo — se algo no repositório ainda diz *"vetada"*,
  **está desatualizado**.
- **Os valores medidos dos bichos da fazenda** (~2.400 XP + 50 de ouro por abate) estão no §5, medidos
  abate a abate nos transcripts.
- **O briefing literal do Pacificador** está no §3.1 — é o mapa da missão, e estava só em transcript.

---

## 9. Como encerrar a sua sessão

1. `cuidar.py` até `exit 0`; **`save`** — **nunca `quit`** (é o que perdeu esta missão).
2. **Criar `planos/plano009.md`** com o modelo do `LEIA.md`, **incluindo a §8 Devolutiva técnica**.
3. **Rodar `python scripts/devolutiva.py` e resolver as FALHAS.** Só encerre com **0 falhas**.
4. Se fechou o capítulo: `capitulos.json` com `parts` contendo **`source_kind`**, **`date`** e
   **`evidence`**.
5. `sync_hero.py --hero grebolius` **e** `--check`; `verificar.py` **18/18**; `check_project.py` **0 erros**.
6. Bloco em `docs/agentes/registro_de_evolucao.md` (**append-only**) com **modelo/versão**.
7. Publicar **só se pedido**, **sinalizando quem fez** — e ler o **`AGENTS.md` §12**.

---

## 10. Os capítulos

**Os sete primeiros estão `concluido`.** Este plano **abre o Capítulo 07**, que ainda **não existe em
`capitulos.json`** — quem for jogar deve criá-lo com `status: em_curso`, `kind: marco` e o objetivo
`Problemas Agrícolas`.

**Sugestão de título, para o autor decidir:** *"O Que Eu Deixei no Meio"* — porque é o que ela diz
neste capítulo: que não gosta de deixar coisa por fazer, e que vai tentar de novo.
