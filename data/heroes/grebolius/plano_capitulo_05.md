# Plano do Capítulo 05 — "Amanhã Eu Começo por Elas"

> **Título escolhido pelo autor, e ele virou o eixo do capítulo.** É a última linha do fecho do
> Capítulo 04 — *"Amanhã eu começo por elas"* — dita sobre **as trinta portas**. O Capítulo 05 abre
> com a dúvida: ela senta, pensa, e **"elas" acaba sendo outra coisa**.

**Natureza:** `kind` **`marco`**. **`id` no `capitulos.json`: 5.**

---

## 1. A dúvida da abertura — e a decisão

O Capítulo 04 terminou com uma promessa: *amanhã eu começo por elas*, as trinta portas nomeadas e
nunca abertas. O Capítulo 05 **abre traindo essa promessa**, e é isso que o torna um capítulo e não
uma continuação.

Ela para, olha a lista das portas, e pensa. **As portas não vão levá-la a lugar nenhum útil por
enquanto.** Uma delegacia, um banco, uma sapataria, um clube — são lugares de cidade, e cidade ela
já sabe andar. O que as portas oferecem é **mapa**, e o mapa ela já provou que consegue fazer. O que
elas **não** oferecem é o que ela precisa agora: experiência, poder, e um motivo para os deuses
olharem para ela.

E existe outra lista, aquela que ela viu sem querer enquanto conferia outra coisa: **as missões**.

Então ela decide o contrário do que prometeu. Vai começar pelas **missões**, não pelas portas. As
portas ficam para quando houver motivo para atravessá-las — e "elas", no fim, era as missões.

> **É a primeira vez que ela muda de plano por conta própria.** Nos capítulos anteriores ela reagia:
> ao milharal, à torre, ao que pediam dela. Aqui ela escolhe, e a escolha contraria a própria
> promessa.

---

## 2. As duas missões do capítulo

O autor vetou duas das cinco disponíveis — **Dicas Mágicas** e **Problemas Agrícolas**. As duas
escolhidas são as do **tier de nível 30**, adequadas ao nível 20 dela:

### Missão A — Limpando Monstros

| | |
|---|---|
| **Teto** | até o nível 30 |
| **Inicia com** | **O Novato Alquimista** |
| **Onde** | **A Sala do Alquimista**, na Masmorra dos Novatos |
| **Rota do Templo** | **10 passos: `n,n,n,e,n,e,e,s,s,e`** |
| **Objetivo (o que a base sabe)** | *"Eliminação de pragas e entrega de materiais ao Alquimista"* |

**⚠️ Esta missão exige COMBATE.** É a diferença central em relação ao Capítulo 04, onde a regra era
*não lutar*. "Limpar monstros" é matar bichos e entregar o material. Ela vai para uma masmorra de
novatos (teto de nível 30) no nível 20, com 113 de vida, classe de armadura 110 e a experiência do
milharal — é um alvo adequado, não um suicídio. Mas **é luta**, e o capítulo tem de dizer isso.

**Inimigos já vistos na camada `novatos`:** Monstro Novato, Monstro Novato de Elite, Novato Zumbi
Descarnado, Diabinho, Guarda Novato em Apuros.

### Missão B — Novela dos Novatos

| | |
|---|---|
| **Teto** | até o nível 30 |
| **Inicia com** | **o novato esperto** |
| **Onde** | **não tem sala fixa.** A base o descreve como *"habitante das praças e encruzilhadas civis"* |
| **Objetivo** | *"Cadeia narrativa de suporte aos recém-chegados"* |

**Ele é andarilho**, como O Pacificador e O zelador — aparece andando. As praças candidatas são
**A Praça do Templo**, **A Praça do Comércio** e **A Praça Comum**. Encontrá-lo é parte da missão:
ela vai ter de **esperar em praça pública**, o que é o oposto de tudo que ela fez no Capítulo 04.

---

## 3. O método

O que continua valendo do Capítulo 04:

1. **Rota pelo mapa, a partir da sala onde ela ESTÁ** — nunca de onde se supõe.
2. **Conferir a chegada por marco de sala**, não por contagem de passos.
3. **Desviar das 20 salas de risco alto** (`RISCO_A_EVITAR`), e registrar quando não houver caminho
   limpo.
4. **`visible` antes de qualquer comércio** — invisibilidade bloqueia troca.
5. **`term 200 80` já é aplicado no login**; o paginador não existe mais.
6. **Voltar ao Templo e salvar** ao fim de cada rodada.

**O que muda:** o passo 5 do capítulo anterior era *não lutar*. Aqui **a luta é o objetivo da Missão
A** — mas continua valendo que ela não procura briga fora do escopo, e que **fugir é vitória quando a
vida cai**. `wimpy` fica em **48**.

**Ao entrar em cada lugar novo, anotar:** nome, saídas, NPC que atende, o que vende (`list`) e preço.

---

## 4. Diretivas que continuam valendo

- **PROIBIDO vender armaduras** da Torre Negra ou de peão.
- **Saque do prepara: 300** na mão (`config.SAQUE_PARA_COMPRAR`).
- **Teto de 10 conexões**, com 3 preferidas.
- **Nada de metajogo** nas descrições dos capítulos.
- **Nunca dar `quit` com missão em andamento.** Descoberto no Dia 156: `quit` responde
  ***"Você falhou em suas aventuras! Se quiser concluí-las deverá recomeçá-las!"*** e **zera todo o
  progresso** — foi o que apagou as missões em andamento desde o Dia 97. **Terminar as sessões com
  `save` e deixar a conexão cair**, não com `quit`.

---

## 5. Quando o capítulo fecha

Quando **as duas missões estiverem concluídas e confirmadas pelo servidor** — não por achismo. A
confirmação é o servidor dizendo, ou o status mudando no `autoquest`/`score`.

**E o que o capítulo deixa:** duas missões a menos, alguma experiência, e a lição de que ela pode
escolher.

---

## 6. Riscos conhecidos

| Risco | Estado |
|---|---|
| **A Masmorra dos Novatos tem monstros** | esperado — é o objeto da Missão A. Ir com vida e mana cheias. |
| **O novato esperto pode não aparecer** | é andarilho. Se não aparecer, a Missão B fica pendente e o capítulo fecha com uma. Registrar como resposta, não como falha. |
| **`quit` apaga o progresso** | proibido no meio do capítulo. Só `save`. |
| **As portas ficam para depois** | decisão do capítulo, não dívida. Elas continuam no mapa, nomeadas e esperando motivo. |

---

## 7. Anexo — por que não as outras

| Missão | Por quê não |
|---|---|
| **Dicas Mágicas** | vetada pelo autor |
| **Problemas Agrícolas** | vetada pelo autor |
| **Uma Lição em Gargamel** | o conteúdo mais novo do jogo (não catalogado, teto 80), mas o **smurf minerador não está no mapa** — viraria exploração antes de virar missão. Guardada para um capítulo próprio. |
