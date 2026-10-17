# Plano 013 — Capítulo 09: comprar a poção e iluminar a mina

| | |
|---|---|
| **Criado em** | 2026-10-17 · Dia 156 |
| **Por** | **`deepseek-flash`** |
| **Herói** | `grebolius` |
| **Capítulo** | **09 — "O Preço Não Se Mata com Raio"**, já **`em_curso`** em `capitulos.json` (`id=9`), `continues_chapter: 8` |
| **Objetivo** | **Concluir `Uma Lição em Gargamel`** — falta comprar a poção aquosa e entregar o jarro ao minerador |
| **Sessão encerrada?** | **Sim** — `save` + `sleep` confirmados no Templo; **driver encerrado, nenhum processo deixado rodando** |

> **Leia o [`LEIA.md`](LEIA.md) primeiro.** **Este arquivo não se edita** — quem vier cria o
> **`plano014.md`**.
>
> **Antes de encerrar, rode `python scripts/devolutiva.py`** — obrigatório desde o Dia 156 (§8).
>
> ## 🔴 A PRIMEIRA COISA A FAZER: comprar comida
>
> **Ela está com FOME e sem comida na bolsa** — o `cuidar.py` acusou *"fome sem comida na bolsa"*. Sem
> comida ela **não regenera vida nem mana** (`diretiva_de_jogo.md` §13) e emagrece até morrer.
> **Padaria de Midgaard, com 30 moedas:** compre pães antes de qualquer outra coisa. *(Ela tem 4.229.)*

---

## 0. O Capítulo 08 fechou **incompleto, e isso foi decidido**

> **Diretiva do autor:** *"FECHAR INCOMPLETO TUDO BEM, COMENTA QUE VAI FICAR PRO PROXIMO E CONTINUAMOS NO
> PROXIMO CAPITULO"*

**O Capítulo 08 (`Uma Lição em Gargamel`) está `concluido`** com 14 parágrafos, e **o último diz em voz
alta que a história continua.** O campo **`carried_over`** do capítulo registra a mesma coisa em dado. **O
Capítulo 09 (`O Preço Não Se Mata com Raio`) já está aberto** e é onde você continua.

**Fechar incompleto é permitido desde que declarado em três lugares:**
1. **`carried_over`** do capítulo fechado;
2. **o último parágrafo da narrativa** (na voz dela, sem metalinguagem);
3. **o plano numerado** do próximo agente — este.

**O capítulo anterior a este (o 08) fechou assim. O 09 pode fechar igual, se faltar ouro de novo.**

---

## 1. Onde a missão está — e ela está **ATIVA**

```
[Autoquests em andamento]
Uma Lição em Gargamel: Você deve entregar objeto ao personagem.
```

**O Capítulo 08 está fechado** (`capitulos.json` `id=8`, `concluido`, 13 parágrafos), **mas o capítulo
fechou a expedição, não a missão.** O handoff dela está no campo **`carried_over`** do capítulo.

**A cadeia, do começo ao ponto onde parou:**

| Etapa | Quem | O que quer |
|---|---|---|
| 1 ✅ | **o smurf minerador** (Vila dos Smurfs, túnel sob o Poço Smurf) | ficou **sem óleo no lampião**; quer algo confiável que ilumine — **`um jarro brilhante`**. E pediu: *"não machuque ninguém"* |
| 2 ✅ | **O Novato Alquimista** (A Sala do Alquimista, escola de Midgaard) | em troca do jarro, quer **`uma poção aquosa`** de **`As Misturas de Clariss`**, na **Avenida Floris em Jareth** |
| 3 ⛔ | **Clariss** | vende a poção por **9.750 moedas**. **Ela tem 4.229.** |
| 4 ⛔ | de volta ao Alquimista | entregar a poção → receber o **jarro brilhante** |
| 5 ⛔ | de volta ao **minerador** | entregar o jarro → fechar a missão |

**O bloqueio é OURO. Não é combate, não é caminho, não é enigma.** Faltam **5.521 moedas**.

---

## 2. Estado exato

| | |
|---|---|
| Personagem | **Nível 28**, Mago Elfo |
| Vida / mana / movimento | **178/178 · 340/340 · 141/141** |
| Experiência | **4.000.001** (próximo em 4.500.000) |
| **Ouro** | **4.229 na mão · 0 no banco** |
| Mortes | **8** (nenhuma nova) |
| Classe de Armadura | **112** (78 + 34 de `armor`) |
| `wimpy` | **45** |
| Treinos | **68 sessões** — **escolher o que treinar conforme o objetivo** |
| Pontos de Aventura | **0** |
| Local | **O Templo de Midgaard** |
| Mapa | **511 salas** |

**Equipamento:** a Armadura da Torre Negra (amaldiçoada), a Coroa da Rainha Branca, **o brinco de novato
ANTI-DT**, o manto de pano, braçadeiras, luvas, calça de couro, escudo, espada curta, e o **cinto de
rodeio (CA 134** conforme o registro do Capítulo 07 — **conferir no `equipment`**).

---

## 3. 🎯 A descoberta que resolve o "círculos" do agente anterior

**O `O Novato Alquimista` tem DUAS missões na cabeça ao mesmo tempo** — a dele (limpar os monstros do
porão) e a do jarro. **E ele escolhe.**

> **Com `Limpando Monstros` ativa ao mesmo tempo, ele prioriza a própria missão e NÃO dispara o diálogo
> do jarro.** Pior: **se receber a poção nesse estado, ele ENG OLE o item e não entrega o jarro.**

**Isto foi documentado no `conhecimento.md` §42.1** — e é a explicação de por que o agente anterior
girava em círculos.

**✅ A concorrência já foi RESOLVIDA:** o `Limpando Monstros` foi entregue de novo (7 abates, manto,
**94.227 de experiência**, nível 28). **Ele não tem mais nada para pedir além da poção.**

**Portanto, na próxima sessão:** **NÃO reinicie `Limpando Monstros`.** A janela está limpa.

---

## 4. Como levantar as 5.521 moedas

**Opção A — o milharal (a mais segura, e a mais lenta).**
Os invasores deixam **~50 moedas por abate** (medido, abate a abate). **São ~110 abates.** A rota está no
`conhecimento.md` §16, e a rotina `automato/rotinas/milharal.py` funciona.

**Opção B — vender o que não se usa.** `state.json → inventory` e `equipment` listam tudo. **Em Jareth:**
- `A Loja de Armas de Maris` e `Dalston Tralhas e Cia` → *"Eu não compro!"* (**não perca tempo**)
- `A Loja de Trapos da Vovó` (Granny) → *"Nós não trabalhamos para sua classe aqui!"* (**recusa magos**)
- `A Loja de Armaduras de Maris` (Ilena) → avalia armaduras boas, mas *"não compro de forasteiros"*
  (**comprou luvas de couro por 37**)

**Em Midgaard:** o Ferreiro compra armas até zerar o caixa (~200); o Armeiro comprou um peitoral por 200.

**Opção C — `farm_ouro_xadrez` / armaduras de peão: ❌ PROIBIDO.** Diretiva do autor (`diretiva_de_jogo.md`
§15): **não vender armaduras**, nem da Torre Negra nem de peão. **Um agente anterior escreveu
`farm_ouro_xadrez.py` — está no entulho, e a rotina `xadrez` está suspensa. Não reative.**

**Opção D — as missões vizinhas.** Há **`Cuidado Com o Chacal`** (nível 22+, ela é 28 → **liberada**) e
**`QuizBo!`** (25+). **Missão paga em XP e às vezes em ouro, e o capítulo 05 provou que uma entrega vale
horas de grind** (67.068 e 94.227 de experiência em duas ocasiões).

---

## 5. As rotas (verificadas)

```
Vila dos Smurfs:  Templo -> s, s (Praça do Comércio) -> 8x leste (Rua Principal, Portão Leste,
                  Entrada da Cidade, Estrada do Rei) -> n -> A Entrada Para a Vila dos Smurfs

Minerador:        da vila, `d` em `O Poço Smurf` -> `e` -> O Fim Do Túnel

Alquimista:       escola de Midgaard -> corredor nordeste -> `open leste` -> A Sala do Alquimista

Clariss:          Jareth, Avenida Floris (sul da praça central oeste) -> As Misturas de Clariss

Castelo:          norte de O Poço Smurf -> Uma Intersecção em T -> oeste -> A Estrada para o Castelo
                  -> A Entrada do Castelo -> `n` -> O Covil de Gargamel
```

**⚠️ A `Avenida Floris` e Jareth nunca foram percorridas por mim** — a rota veio do `conhecimento.md`
§41.3 e do `help mapa 2`. **Confirme com o `exits` ao vivo.**

---

## 6. 🎁 O tesouro que ficou para o Capítulo 09

**No `O Covil de Gargamel`** estão **Gargamel** e **Azrael** (o gato, que usa `o colar de Azrael`).
**E a leste há uma porta TRANCADA — atrás dela, `Papai Smurf`, preso.**

**Confirmado via `where smurf`** (`conhecimento.md` §41.2). **Isto é a continuação natural da missão
`Uma Lição em Gargamel`:** o nome do capítulo não é sobre comprar poção — **é sobre o vilão.**

**Não abra a porta sem saber o que tem atrás.** Gargamel está lá. **Ela tem nível 28 e 8 mortes; o
Dragão do esgoto a matou em um turno.**

---

## 7. NÃO REPITA

1. **Reiniciar `Limpando Monstros` enquanto a poção não estiver entregue** — **é o que faz o Alquimista
   engolir o item.** (§3, e `conhecimento.md` §42.1)
2. **Entregar a poção antes de conferir o `score`** — a etapa muda, e ação antes da hora não conta.
3. **Inventar frase para o NPC.** O diálogo é **literal**: o minerador aceita `say sim` → `say Grebolius`
   → `say sim`; o Alquimista, `say Grebolius` → `say sim`. **Nada de sinônimo.**
4. **Escrever um script por tentativa de fala.** *(O Dia 156 deixou **18** desses em `scripts/`; foram
   movidos para `scripts/local/entulho_dia156/`, que é gitignored. Se precisar testar fala, use
   `automato/nucleo/driver/play.py "say <frase>"` direto — não crie arquivo.)*
5. **Vender armaduras** — §15, proibido.
6. **`quit` com missão em andamento** — **zera.** Use `save`.
7. **`onde`** — não existe. **`where`.**
8. **`autoquest todas` como prova** — é histórico; a prova é o `score`.
9. **Presumir que o brinco ANTI-DT imuniza** — não testado.
10. **Comprar em Jareth contando com vender** — os três lojistas recusam (ver §4, Opção B).

---

## 8. Devolutiva técnica

| Descobri | Registrei em | O quê |
|---|---|---|
| **mapa** | *nada nesta sessão* | **A pendência do esgoto continua aberta** (as 4 arestas dos anéis) — **não a mexi nesta sessão, e o `devolutiva.py` avisa em toda execução.** O mapa já foi de 381 para 511 salas nas sessões anteriores. |
| **referência do servidor** | *nada nesta sessão* | Nada novo. Os achados do Dia 156 (aviso de DT, `Você é LOUCO!`, a mordida do Dragão) já estão no `maquina/verificacoes.md`. |
| **fato do mundo** | **`capitulos.json` id=8** ✅ | **O capítulo 08 fechado com 13 parágrafos**, o campo **`carried_over`** dizendo que a missão segue ativa, 4 evidências e 10 tags. **Nota de honestidade:** o `conhecimento.md` **não foi tocado por mim** nesta sessão — as seções §41-43 que entraram no mesmo commit são de **Gemini 4 Argon** e **GPT-6 / Codex**. **A explicação da concorrência de autoquests, que destravou o diagnóstico dos "círculos", já estava no §42.1 escrito por eles.** |
| **erro do motor** | *nada nesta sessão* | O motor não falhou. **O problema do "círculos" era regra do jogo, não bug** — e agora está escrito. |

### O entulho que eu limpei

**18 scripts soltos em `scripts/`**, um por tentativa de fala (`dizer_nome_minerador.py`,
`testar_entrega_tocha.py`, `comprar_pocao_clariss.py`, `farm_ouro_xadrez.py`…), escritos entre 08:01 e
09:02. **Movidos para `scripts/local/entulho_dia156/`** — preservados, gitignored, fora do caminho.
**`scripts/` está limpo.**

---

## 9. Como encerrar a sua sessão

1. `cuidar.py` até `exit 0`; **`save`** — **nunca `quit`**.
2. **Criar `planos/plano014.md`** com o modelo do `LEIA.md`, **incluindo a §8 Devolutiva técnica**.
3. **Rodar `python scripts/devolutiva.py` e resolver as FALHAS.** Só encerre com **0 falhas**.
4. Se fechou capítulo: `parts` com **`source_kind`**, **`date`** e **`evidence`**.
5. `sync_hero.py --hero grebolius` **e** `--check`; `verificar.py` **18/18**; `check_project.py` **0 erros**.
6. Bloco em `docs/agentes/registro_de_evolucao.md` (**append-only**) com **modelo/versão**.
7. **Se `scripts/` ganhar arquivo novo de teste de fala, ele está errado** — use `play.py` direto.
8. Publicar **só se pedido**, **sinalizando quem fez** — e ler o **`AGENTS.md` §12** (há agente proibido de
   publicar) e o **§13** (handoff com 10% da janela).

---

## 10. O placar

**Capítulos 0 a 8 concluídos.** Nove no total. **O Capítulo 09 é continuação direta do 08:** a poção, o
jarro, o minerador — e, atrás da porta trancada, o Papai Smurf.
