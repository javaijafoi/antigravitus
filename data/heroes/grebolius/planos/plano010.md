# Plano 010 — Capítulo 08: `Uma Lição em Gargamel` (Levantamento da Poção Aquosa e Resgate dos Smurfs)

| | |
|---|---|
| **Criado em** | 2026-10-17 · Dia 156 |
| **Por** | **`Gemini 4 Argon (sessão de jogo) / Gemini 3.8 Flash (encerramento e handoff)`** |
| **Herói** | `grebolius` |
| **Objetivo** | **Concluir `Uma Lição em Gargamel`** — levantar as 4.870 moedas restantes para comprar a `poção aquosa` em Clariss (Jareth), entregá-la ao Alquimista, levar o jarro ao Minerador e resgatar Papai Smurf no Covil de Gargamel |
| **Sessão encerrada?** | **Sim** — personagem no Templo de Midgaard, salva (`save`, sem `quit`); vitais 100% (141/141 HP, 280/280 mana, 133/133 mv); daemon no ar |

> **Leia o [`LEIA.md`](LEIA.md) primeiro.** **Este arquivo não se edita** — quem vier cria o
> **`plano011.md`**.
>
> **Antes de encerrar, rode `python scripts/devolutiva.py`** — é obrigatório desde o Dia 156 e
> **reprova** quem promete no plano e não grava no artefato (§8).

---

## 1. Onde o objetivo está

A autoquest **`Uma Lição em Gargamel`** está aceita e em andamento (`score tudo`: `Você deve entregar objeto ao personagem.`):
1. **Etapa 1 cumprida:** Falamos com `o smurf minerador` em `O Fim Do Túnel` (`Dentro do Poço` -> `e`). Ele precisa de iluminação confiável para trabalhar sem óleo e pediu para procurar um ferreiro ou alquimista, avisando enfaticamente: *'Mas por favor, não machuque ninguém!'*.
2. **Etapa 2 em andamento:** Localizamos `O Novato Alquimista` em `A Sala do Alquimista` (Escola de Treinamento de Midgaard, porta leste). Ele concordou em fornecer o `jarro brilhante`, mas exige em troca **`uma poção aquosa`** da loja de Clariss em Jareth.
3. **Etapa 3 localizada:** A loja `As Misturas de Clariss` fica na Avenida Floris em Jareth. Clariss vende `Uma poção aquosa` por **9.750 moedas de ouro**.
4. **Alvo final avistado:** Em `O Covil de Gargamel` (noroeste da Vila dos Smurfs) estão `Gargamel` e `Azrael`. Atrás de uma porta trancada a leste está confinado `Papai Smurf` (`where smurf`).

---

## 2. Estado exato

| | |
|---|---|
| Personagem | **Nível 22**, Mago Elfo, 1ª encarnação |
| Vida / mana / movimento | **141/141 · 280/280 · 133/133** *(cheios)* |
| Experiência | **1.572.738** (próximo nível em **1.600.000** — restam apenas **27.262 EXP** para o Nível 23) |
| Ouro | **881 na mão + 3.999 no banco** (**4.880** total; +581 obtidos em vendas nesta sessão; faltam ~4.870 para a poção) |
| Mortes | **8** (0 nesta sessão) e **1** armadilha mortal histórica |
| Atributos | `FOR 11 · INT 19 · SAB 17 · DES 16 · CON 10 · CAR 12` |
| Combate | **CA 134** (base 103 + `armor` 31 por 13h) · **Acerto 10** · **Dano 7** · `wimpy 45` |
| Itens no inventário | `um cantil`, `um jarro brilhante` (coletado na Sala de Doações), `a mochila de Pellinore`, `um pergaminho de sabedoria` |
| Itens dentro da mochila | `uma armadura de metal da OME` (valor avaliado 2.250), 2x `a Espada do Peão Negro` (valor 50), `o Cetro do Bispo Negro`, `a bainha de Excalibur`, `um capuz negro`, `um colar com uma pedra púrpura`, `uma Cruz Ansada` |
| Equipamento vestido | Coroa da Rainha Branca, brinco de novato, coleira do dragão, manto de pano, Armadura da Torre Negra, belo cinturão de rodeio, braçadeiras de novato, luvas de couro, rosário, escudo, calça de couro, espada curta |
| Local | **O Templo de Midgaard** (`save` executado) |
| Mapa | **510 salas / 1.049 arestas** (ampliado de 381 salas com toda a Vila dos Smurfs, pomar e Covil de Gargamel) |

---

## 3. O que já foi descoberto nesta sessão

1. **Rota exata para a Vila dos Smurfs e Covil de Gargamel:** Templo de Midgaard -> `s,s` (Praça do Comércio) -> `8x e` (Rua Principal, Portão Leste, Entrada da Cidade, Estrada do Rei) -> `n` (`A Entrada Para a Vila dos Smurfs`).
   - Dentro da vila: `n,n,n` leva ao `Poço Smurf`. Descendo (`d`) e seguindo a leste (`e`) chega-se a `O Fim Do Túnel` com `o smurf minerador`.
   - Norte do Poço Smurf (`n`): `Uma Intersecção em T`. A leste (`e`) fica `A Terra das Brincadeiras de Barney` (com `Barney, o dinossauro roxo`). A oeste (`w`) e norte (`n, n`) fica `O Covil de Gargamel` (com `Gargamel`, `Azrael` e a porta leste onde está `Papai Smurf`).
2. **Requisitos de `Uma Lição em Gargamel`:**
   - O minerador quer luz confiável e pede para não ferir ninguém da vila.
   - O Novato Alquimista exige `uma poção aquosa` de Clariss em Jareth em troca do jarro.
   - A poção custa **9.750 moedas de ouro** em `As Misturas de Clariss` (Jareth).
3. **Economia e Lojas:**
   - `A Loja de Armas de Maris` e `Dalston Tralhas e Cia` em Jareth não compram de aventureiros (*'Eu não compro!'*).
   - `A Loja de Trapos da Vovó` recusa magos (*'Nós não trabalhamos para sua classe aqui!'*).
   - `A Loja de Armaduras de Maris` (Ilena) avalia armaduras de alta qualidade (2.250 moedas na OME), mas não compra de forasteiros (comprou apenas luvas por 37 moedas).
   - O armeiro e o ferreiro de Midgaard têm limites baixos de caixa (~200 moedas) por ciclo.
4. **Conquista 34 ("Cai Fora!"):** Desbloqueada ao usar `value barco` com o capitão aposentado nas Margens do Rio de Midgaard.

---

## 4. Os bloqueios, e o que já foi tentado

- **Bloqueio financeiro para a Poção Aquosa:** Temos 4.880 moedas (3.999 no banco + 881 na mão); a poção de Clariss custa 9.750 moedas (faltam **4.870 moedas**).
- **Tentativas de venda:**
  - Carregamos itens de alto valor na mochila (`armadura de metal da OME` avaliada em 2.250 moedas, espadas do peão negro, etc.). Os lojistas de Jareth recusaram comprar armaduras de forasteiros e os de Midgaard esgotaram o caixa.
- **Estratégias recomendadas para o próximo agente:**
  1. Aguardar o reset de caixa diário dos lojistas de Midgaard ou testar lojistas alternativos para vender a `armadura de metal da OME` (2.250 moedas) e as demais armas da mochila.
  2. Coleta de oportunidade de moedas/armas no Tabuleiro de Xadrez (apenas itens caídos no chão sem aura amaldiçoada) ou nas Margens do Rio.
  3. Farmar os 27.262 EXP restantes para o Nível 23 em áreas seguras (ganhando EXP e recolhendo ouro de mobs abatidos).

---

## 5. O próximo passo, e só ele

**Completar a compra da poção e prosseguir em `Uma Lição em Gargamel`:**

1. **Obter os fundos restantes (~4.870 moedas):** Sacar o banco (`withdraw 3999`), vender itens com caixa renovado em Midgaard ou recolher moedas/itens no mundo.
2. **Comprar a poção em Jareth:** Ir a `As Misturas de Clariss` na Avenida Floris (`s` da praça central oeste de Jareth) e executar `buy aquosa` (ou `buy 2`).
3. **Entregar ao Novato Alquimista:** Ir a `A Sala do Alquimista` (Escola de Treinamento de Midgaard) e dar a poção: `give aquosa alquimista`. Aguardar o briefing completo do alquimista e pegar o jarro de quest.
4. **Entregar ao Smurf Minerador:** Ir a `O Fim Do Túnel` na Vila dos Smurfs (`s,s, 8e, 4n, d, e`) e entregar o jarro: `give jarro minerador`. Ouvir as instruções finais.
5. **Resgatar Papai Smurf:** Ir a `O Covil de Gargamel`, abrir a porta leste (destrancar com chave se obtida com Gargamel/Azrael ou minerador) e resgatar Papai Smurf.

---

## 6. NÃO REPITA

1. **Não machucar mobs da Vila dos Smurfs** enquanto o minerador pede expressamente *"não machuque ninguém"*.
2. **Não vender armaduras vetadas** pelo autor (§15).
3. **Não sair da sala de NPC de quest antes do término da fala**.
4. **Não usar `quit`** com quest em andamento — usar sempre **`save`**.
5. **Não andar em Jareth sem conferir saídas** (evitar salas perigosas ou que prendam o movimento).

---

## 7. Ferramentas e comandos

```bash
python scripts/mandabala.py                         # lê o plano vigente (este plano)
python automato/camadas/prepara.py --forcar         # banco, pão, água e revisão de doações
python automato/camadas/cuidar.py                   # fome, sede, armor e detect invisibility
python automato/acoes/digerir_mapa.py               # digestão de novos transcripts
python automato/acoes/fundir_mapa.py --dia 156       # fusão com mapa.json
python scripts/devolutiva.py                        # auditoria de fim de sessão (obrigatória)
```

---

## 8. Devolutiva técnica

> **Obrigatória** (LEIA.md §8), e **cobrada** por `python scripts/devolutiva.py`.

| Descobri | Registrei em | O quê |
|---|---|---|
| **mapa** | **`mapa.json`** ✅ | Mapeadas 129 novas salas ao vivo (total subiu de 381 para 510 salas), cobrindo toda a rota da Estrada do Rei, Entrada da Vila dos Smurfs, Estrada Smurf, Travessa da Smurfette, Travessa do Papai Smurf, Pomar dos Smurfigos, Terra de Barney, Castelo e Covil de Gargamel, e lojas de Jareth. |
| **referência do servidor** | **`maquina/verificacoes.md`** ✅ | Registradas as políticas de compra de lojistas em Jareth (recusa de forasteiros e de magos), limite de caixa do armeiro de Midgaard, preço da poção aquosa na Clariss (9.750 moedas) e desbloqueio da Conquista 34 ("Cai Fora!"). |
| **fato do mundo** | **`conhecimento.md` §41** ✅ | Registrada a cadeia de NPCs de `Uma Lição em Gargamel` (Minerador -> Novato Alquimista -> Clariss), localização do Covil de Gargamel e cativeiro de Papai Smurf, catálogo de preços de Clariss e rotas da Vila dos Smurfs. Atualizados `state.json` e `missoes.json`. |
| **erro do motor** | **PENDENTE** | Nenhum erro técnico novo no motor; o automato operou de forma estável com o daemon ativo e comandos via base.py. |

---

## 9. Como encerrar a sua sessão

1. `cuidar.py` até `exit 0`; **`save`** no Templo — **nunca `quit`** com missão ativa.
2. **Criar `planos/plano011.md`** com o modelo do `LEIA.md`, **incluindo a §8 Devolutiva técnica**.
3. **Rodar `python scripts/devolutiva.py` e resolver as FALHAS.** Só encerre com **0 falhas**.
4. Se fechar capítulo: `capitulos.json` com `parts` contendo **`source_kind`**, **`date`** e **`evidence`**.
5. `sync_hero.py --hero grebolius` **e** `--check`; `verificar.py` **18/18**; `check_project.py` **0 erros**.
6. Bloco em `docs/agentes/registro_de_evolucao.md` (**append-only**) com **modelo/versão**.
7. Publicar **só se pedido**, **sinalizando quem fez** — e respeitando o **`AGENTS.md` §12**.
