# Plano 011 — Capítulo 08: `Uma Lição em Gargamel` (Grind dos ~5.750 Ouros Restantes, Reset Limpo de Quests e Resgate de Papai Smurf)

| | |
|---|---|
| **Criado em** | 2026-10-17 · Dia 156 |
| **Por** | **`Gemini 4 Argon (sessão de jogo) / Gemini 3.8 Flash (encerramento e handoff)`** |
| **Herói** | `grebolius` |
| **Objetivo** | **Concluir `Uma Lição em Gargamel`** — farmar os ~5.750 ouros restantes no milharal até atingir 9.800 moedas, fazer reset limpo via `quit` no Templo para desobstruir o Alquimista, comprar a `poção aquosa` em Clariss (Jareth), entregá-la ao Alquimista em troca do jarro, levar a luz ao Smurf Minerador e resgatar Papai Smurf no Covil de Gargamel |
| **Sessão encerrada?** | **Sim** — personagem no Templo de Midgaard, salva (`save`, sem `quit`); vitais plenos (172/172 HP, 330/330 mana, 139/139 mv); CA 136 com `armor` ativa por 31h; daemon desativado |

> **Leia o [`LEIA.md`](LEIA.md) primeiro.** **Este arquivo não se edita** — quem vier cria o
> **`plano012.md`**.
>
> **Antes de encerrar, rode `python scripts/devolutiva.py`** — é obrigatório desde o Dia 156 e
> **reprova** quem promete no plano e não grava no artefato (§8).

---

## 1. Onde o objetivo está

A autoquest **`Uma Lição em Gargamel`** está em andamento no Capítulo 08:
1. **Etapa 1 cumprida:** Falamos com `o smurf minerador` em `O Fim Do Túnel` (`Dentro do Poço` -> `e`). Ele precisa de iluminação para trabalhar e pediu para procurar um ferreiro ou alquimista, avisando enfaticamente: *'Mas por favor, não machuque ninguém!'*.
2. **Diagnóstico da Etapa 2 (Alquimista desvendado):** Localizamos `O Novato Alquimista` em `A Sala do Alquimista`. Descobrimos por que ele não entregava o jarro: **conflito de concorrência com `Limpando Monstros`**. Enquanto a missão de monstros estiver ativa, ele só fala do subsolo (*'Eles se encontram logo aqui embaixo...'*) e não ativa o diálogo de troca do `jarro brilhante`.
3. **Estratégia autorizada pelo autor:** O autor autorizou perder a missão concorrente e reiniciar quando tiver o ouro: *"Talvez tenha que matar bixos, perder a missão e reiniciar quando tiver 10k"*. Um `quit` limpo a partir do Templo reseta as autoquests ativas sem perder nível, equipamentos, itens ou ouro.
4. **Etapa financeira em andamento:** Temos **4.054 moedas de ouro** vivas na mão (saldo elevado de 881 para 4.054 durante o grind seguro no milharal). A `poção aquosa` em Clariss custa **9.750 moedas**. Faltam apenas **~5.700 moedas**.
5. **Avanço expressivo de poder:** Grebolius subiu do **Nível 22 para o Nível 27** (HP 172, Mana 330, MV 139, CA 136, 64 treinos acumulados).

---

## 2. Estado exato

| | |
|---|---|
| Personagem | **Nível 27**, Mago Elfo, 1ª encarnação |
| Vida / mana / movimento | **172/172 · 330/330 · 139/139** *(cheios)* |
| Experiência | **3.892.670** (próximo nível em **4.000.000** — restam **107.330 EXP** para o Nível 28) |
| Ouro | **4.054 na mão + 0 no banco** (**4.054** total; faltam ~5.696 para os 9.750 da poção) |
| Treinos disponíveis | **64 sessões** preservadas |
| Mortes | **8** (0 nesta sessão) e **1** armadilha mortal histórica |
| Atributos | `FOR 11 · INT 19 · SAB 17 · DES 16 · CON 10 · CAR 12` |
| Combate | **CA 136** (base 103 + `armor` 33 por 31h) · **Acerto 10** · **Dano 7** · `wimpy 45` |
| Itens no inventário | `um cantil` (cheio de água cristalina da Praça do Templo), `a mochila de Pellinore`, `um pergaminho de sabedoria` |
| Itens dentro da mochila | 5x `um pão recheado`, `uma armadura de metal da OME` (valor avaliado 2.250), 2x `a Espada do Peão Negro` (valor 50), `o Cetro do Bispo Negro`, `a bainha de Excalibur`, `um capuz negro`, `um colar com uma pedra púrpura`, `uma Cruz Ansada` |
| Equipamento vestido | Coroa da Rainha Branca, brinco de novato, coleira do dragão, manto de pano, Armadura da Torre Negra, belo cinturão de rodeio, braçadeiras de novato, luvas de couro, rosário, escudo, calça de couro, espada curta |
| Local | **O Templo de Midgaard** (`save` executado) |
| Mapa | **510 salas / 1.049 arestas** |

---

## 3. O que já foi descoberto

1. **Grind seguro e confinamento no Milharal (v1.6.2):**
   - Rota Templo -> Milharal: `s, s, 3w, 3s, w, s, w`. Rota de retorno: `e, n, e, 3n, 3e, n, n`.
   - A rotina `automato/rotinas/milharal.py` foi restrita para caçar apenas em salas com `'Milharal'`, evitando saídas para `O Gramado` e mantendo distância absoluta do DT `Adentro do Milharal Destruído` (Morte #5).
   - Abates rendem de 50 a 120 moedas por mob e alta EXP.
2. **Diagnóstico do Novato Alquimista:**
   - Com `Limpando Monstros` ativa, ele não oferece a troca do jarro brilhante por poção aquosa.
   - O comando `quit` no Templo reseta autoquests ativas sem afetar ouro, itens ou atributos.
3. **Catálogo de Clariss em Jareth:**
   - `As Misturas de Clariss` na Avenida Floris vende `Uma poção aquosa` por **9.750 moedas de ouro**.
4. **Cativeiro no Covil de Gargamel:**
   - `Papai Smurf` está trancado atrás da porta leste no covil de Gargamel e Azrael.

---

## 4. Os bloqueios, e o que já foi tentado

- **Bloqueio financeiro parcial:** Temos 4.054 moedas; a poção custa 9.750 (faltam ~5.700 moedas).
  - *Tentado:* Tentar vender itens em lojas de Jareth (recusaram forasteiros) e Midgaard (caixas esgotados).
  - *Solução validada:* O grind direto no milharal é rápido, seguro e altamente lucrativo com Grebolius no Nível 27.
- **Bloqueio de diálogo do Alquimista:** O Alquimista não reagia ao pedido de jarro porque priorizava a quest dos monstros do subsolo.
  - *Solução autorizada:* Efetuar `quit` no Templo assim que atingir 9.800 moedas para limpar a concorrência.

---

## 5. O próximo passo, e só ele

**Completar o saldo, limpar o Alquimista e resgatar Papai Smurf:**

1. **Subir o daemon:** Iniciar o daemon local escutando em `127.0.0.1:14888`.
2. **Farmar até 9.800–10.000 moedas:** Executar `python scripts/farm_ouro_milharal.py`. O script caça, gerencia fome/sede e dorme no Templo até o saldo atingir o valor necessário.
3. **Reset limpo no Templo:** No Templo de Midgaard, com vitais cheios e >= 9.800 moedas, executar `save` e em seguida `quit` para resetar as autoquests concorrentes.
4. **Reconectar:** Subir a sessão imediatamente.
5. **Comprar a poção aquosa:** Ir a `As Misturas de Clariss` em Jareth (Avenida Floris) e comprar a poção: `buy aquosa` (9.750 moedas).
6. **Falar com o Smurf Minerador:** Ir a `O Fim Do Túnel` na Vila dos Smurfs (`s, s, 8e, n, 3n, d, e`), dizer `say sim` e escutar toda a fala do minerador até o fim (*"Mas por favor, não machuque ninguém!"*).
7. **Obter o jarro com o Alquimista:** Ir a `A Sala do Alquimista` (Escola de Treinamento de Midgaard: `4n, e, n, e, e, s, s, open leste, e`). Agora desimpedido, dizer `say sim`, entregar a poção (`give aquosa alquimista`) e receber `um jarro brilhante`.
8. **Entregar o jarro ao Minerador:** Voltar a `O Fim Do Túnel` e entregar o jarro: `give jarro minerador`.
9. **Libertar Papai Smurf:** Ir a `O Covil de Gargamel` (`w, u, n, w, n, n`), abrir a porta leste e libertar Papai Smurf, concluindo o Capítulo 08.

---

## 6. NÃO REPITA

1. **Não machucar mobs da Vila dos Smurfs** (*"não machuque ninguém"*).
2. **Não falar com o Alquimista enquanto `Limpando Monstros` estiver ativa** — use o reset via `quit` no Templo.
3. **Não usar `quit` fora do Templo ou em combate/perigo**.
4. **Não vender armaduras vetadas** pelo autor (§15).
5. **Não entrar em `Adentro do Milharal Destruído`** (DT Morte #5).
6. **Não sair da sala de NPC de quest antes do término da fala**.

---

## 7. Ferramentas e comandos

```bash
python scripts/mandabala.py                         # lê o plano vigente (este plano)
python scripts/farm_ouro_milharal.py                # grind automatizado com salvaguardas até atingir a meta
python automato/camadas/prepara.py --forcar         # banco, pão, água e revisão de doações
python automato/camadas/cuidar.py                   # fome, sede, armor e detect invisibility
python scripts/devolutiva.py                        # auditoria de fim de sessão (obrigatória)
```

---

## 8. Devolutiva técnica

> **Obrigatória** (LEIA.md §8), e **cobrada** por `python scripts/devolutiva.py`.

| Descobri | Registrei em | O quê |
|---|---|---|
| **mapa** | **PENDENTE** | Nenhuma nova sala percorrida além das 510 já consolidadas; caça restrita às salas conhecidas do milharal. |
| **referência do servidor** | **PENDENTE** | Nenhuma alteração nova de comandos do servidor; o MUD respondeu conforme a referência conhecida. |
| **fato do mundo** | **`conhecimento.md` §42** ✅ | Diagnosticado o conflito de concorrência de autoquests do Novato Alquimista, mecânica de reset limpo de autoquest via quit, otimização de caça no milharal e avanço para Nível 27. |
| **erro do motor** | **`CHANGELOG.md` v1.6.2** ✅ | Correção de confinamento espacial em milharal.py (impedindo dispersão e contornando DT), expansão de direções cima/baixo em base.py e salvaguarda completa de fome/sede durante o sono. |

---

## 9. Como encerrar a sua sessão

1. `cuidar.py` até `exit 0`; **`save`** no Templo — **nunca `quit`** com missão ativa (a menos do reset planejado no passo 3).
2. **Criar `planos/plano012.md`** com o modelo do `LEIA.md`, **incluindo a §8 Devolutiva técnica**.
3. **Rodar `python scripts/devolutiva.py` e resolver as FALHAS.** Só encerre com **0 falhas**.
4. Se fechar capítulo: `capitulos.json` com `parts` contendo **`source_kind`**, **`date`** e **`evidence`**.
5. `sync_hero.py --hero grebolius` **e** `--check`; `verificar.py` **18/18**; `check_project.py` **0 erros**.
6. Bloco em `docs/agentes/registro_de_evolucao.md` (**append-only**) com **modelo/versão**.
7. Publicar **só se pedido**, **sinalizando quem fez** — e respeitando o **`AGENTS.md` §12**.
