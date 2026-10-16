# 🧾 Tabela de Itens — quem vende o quê, por quanto

> **O que este arquivo é.** A tabela de itens do mundo conhecido, **referenciando o NPC que
> vende** — como pedido. Cada item tem **ID próprio**, e cada linha de oferta é uma loja.
>
> **Fonte:** comando `list`, lido ao vivo. É a **única** fonte autoritativa de "quem vende o quê":
> o estoque de uma loja **não pode ser examinado antes de comprar** (ver §4).

---

## 1. Como os IDs funcionam

| Prefixo | O que é | Exemplo |
|---|---|---|
| `it_` | **item** — o objeto em si, independente de quem vende | `it_espada_longa` |
| `of_` | **oferta** — um preço específico num NPC específico | `of_loja_armas_espada_longa` |

**Por que separar os dois:** o mesmo item pode estar em duas lojas por preços diferentes —
`Uma garrafa de cospefogo` custa **50** na Taverna Encardida e **55** no Bar do Javali. Se o ID
fosse do preço, a comparação desapareceria. Assim, o item é um só e as ofertas competem.

O ID é **slug do nome**, sem acento e em minúsculas. Nome repetido em lojas diferentes → mesmo
`it_`; preço diferente → `of_` diferente. Não é numérico de propósito: `it_espada_longa` se lê,
`it_0043` não.

---

## 2. Ofertas por loja

Nível = requisito mínimo para usar. **Ela é nível 20.**

### A Loja de Armas — *O Ferreiro Armeiro* (`loja_armas`)

| ID | Item | Preço | Nível | Enc. | Estoque |
|---|---|---|---|---|---|
| `it_adaga` | Uma adaga | 12 | 0 | 1 | Ilimitado |
| `it_clava_de_madeira` | Uma clava de madeira | 15 | 2 | 1 | Ilimitado |
| `it_espada_curta` | Uma espada curta | 77 | 1 | 1 | Ilimitado |
| `it_pequena_espada` | Uma pequena espada | 77 | 11 | 1 | 1 |
| `it_espada_do_peao_negro` | A Espada do Peão Negro | 129 | 11 | 1 | 1 |
| `it_espada_do_peao_branco` | A Espada do Peão Branco | 129 | 11 | 1 | 2 |
| `it_lamina_improvisada` | Uma lâmina improvisada | 389 | 4 | 1 | 1 |
| `it_picareta` | Uma picareta | 389 | 11 | 1 | 1 |
| `it_brilhante_maca_de_novato` | Uma brilhante maça de novato | 389 | 0 | 1 | 2 |
| `it_espada_longa` | Uma espada longa | 779 | 3 | 1 | Ilimitado |
| `it_mangual` | Um mangual | 812 | 7 | 1 | Ilimitado |

> **O `list` mostra o estoque entre colchetes** (`[1]`, `[2]`, `[Ilimitado]`). A Loja de Armas é a
> única com peças limitadas — as Espadas dos Peões são troféus do tabuleiro, não produção.

### O Armazém — *O Merceeiro* (`armazem`)

| ID | Item | Preço | Nível | Enc. | Estoque |
|---|---|---|---|---|---|
| `it_tocha` | Uma tocha | 15 | 0 | 1 | Ilimitado |
| `it_mochila` | Uma mochila | 30 | 0 | 1 | Ilimitado |
| `it_mala` | Uma mala | 75 | 0 | 1 | Ilimitado |
| `it_lanterna` | Uma lanterna | 75 | 0 | 1 | Ilimitado |
| `it_atadura` | Uma atadura | 300 | 0 | 1 | Ilimitado |

> ⚠️ A **mochila NÃO alivia peso** — testado e registrado no Dia 101. Compra-la por causa de carga
> é dinheiro perdido.

### A Taverna Encardida (`taverna_encardida`)

| ID | Item | Preço | Nível | Enc. | Estoque |
|---|---|---|---|---|---|
| `it_garrafa_especialidade_local` | Uma garrafa de especialidade local | 20 | 0 | 1 | Ilimitado |
| `it_garrafa_cospefogo` | Uma garrafa de cospefogo | 50 | 0 | 1 | Ilimitado |

### O Bar do Javali Roncador (`bar_javali`)

| ID | Item | Preço | Nível | Enc. | Estoque |
|---|---|---|---|---|---|
| `it_garrafa_cerveja_ale` | Uma garrafa de cerveja ale | 11 | 0 | 1 | Ilimitado |
| `it_garrafa_cerveja` | Uma garrafa de cerveja | 22 | 0 | 1 | Ilimitado |
| `it_garrafa_especialidade_local` | Uma garrafa de especialidade local | **22** | 0 | 1 | Ilimitado |
| `it_garrafa_cospefogo` | Uma garrafa de cospefogo | **55** | 0 | 1 | Ilimitado |
| `it_barril_de_cerveja` | Um barril de cerveja | 330 | 0 | 1 | Ilimitado |

> 🔍 **Comparação que só existe porque o ID é do item**: a mesma `garrafa de especialidade local`
> custa **20 na Taverna Encardida** e **22 no Bar do Javali**. E o `cospefogo`: **50 contra 55**.
> A Taverna Encardida é a mais barata nos dois. Sem o ID separado do preço, isso ficaria invisível.

---

## 3. Catálogo histórico (auditorias anteriores, ainda não reconferido ao vivo)

Estes preços vêm do `npcs.md`, auditados nos Dias 42, 51, 60 e 80–81. **São históricos**: o `list`
ao vivo ainda não passou por estas lojas nesta rodada.

| Loja | Item | Preço | Fonte |
|---|---|---|---|
| Padaria (`padaria`) | Pão Recheado | 6 | Dia 81 |
| Padaria | Broa de Milho | 13 | Dia 81 |
| Padaria | Rosquinha Malhada | 151 | Dia 81 |
| Loja de Magias (`loja_magias`) | Pergaminho de Identificação | 4.601 | Dia 42/80 |
| Loja de Magias | Poção Amarela de Detectar Invisibilidade | 5.370 | Dia 42/80 |
| Loja de Magias | Pergaminho de Remover Maldições | 8.509 | Dia 42/80 |
| Loja de Magias | Pergaminho de Retorno | 9.202 | Dia 42/80 |
| Loja de Magias | Cajado Retorcido | 14.570 | Dia 42/80 |
| Loja de Magias | Bastão Cinza de Invisibilidade | 92.233 | Dia 42/80 |
| Loja de Magias | Pergaminho Portador de Tempestades | 574.999 | Dia 42/80 |
| Loja de Armaduras (`loja_armaduras`) | Braçadeiras de bronze | 1.750 | Dia 80 |
| Loja de Armaduras | Manoplas de bronze | 1.750 | Dia 80 |
| Loja de Armaduras | Cota de malha de bronze | 2.500 | Dia 80 |
| Loja de Armaduras | Perneiras de bronze | 3.500 | Dia 80 |
| Loja de Armaduras | Elmo de bronze | 3.500 | Dia 80 |
| Loja de Armaduras | Peitoral de bronze | 7.000 | Dia 80 |
| Loja de Armaduras | Peitoral reforçado de bronze | 18.000 | Dia 80 |
| Loja de Armas | Espada Longa Militar (venda) | 240 | até Dia 60 |
| Loja de Armas | Picareta Pesada (venda) | 120 | até Dia 60 |
| Loja de Armas | Lâmina Improvisada (venda) | 120 | até Dia 60 |
| Loja de Armas | Adaga / Punhal de Novato (venda) | 4 a 10 | até Dia 60 |

**Dívida registrada:** as cinco lojas da Rua Principal ainda não tiveram `list` ao vivo nesta
rodada — a rota falhou (§5).

---

## 4. Como avaliar um item — e o que NÃO dá

Pergunta feita e testada ao vivo no Dia 156, por **duas vias independentes**: o `help` do próprio
servidor e um **bruteforce de 19 verbos** contra um item à venda.

### 4.1 O veredito, e é o `help` que dá

> **`help listar`** — *"Se você gostaria de ver quais itens de uma loja estão à venda, dê uma olhada
> na lista. A lista contém todos os itens à venda no momento, assim como a quantidade em estoque. O
> preço para cada item também será listado. Caso você tenha interesse num tipo particular de item,
> você pode especificar quais itens listar."*

**A lista é tudo o que a loja revela: nome, estoque e preço.** Não há verbo de inspeção — e o `help`
deixa isso implícito ao listar só `COMPRAR`, `VENDER`, `LOJAS` e `VALOR` como assuntos relacionados.

> ### ⚠️ A EXCEÇÃO, descoberta depois (Dia 156) — e ela delimita este veredito
>
> **Na loja dos deuses** (`autoquest loja` — ver §32 do compêndio), **`list <número>` devolve a ficha
> completa do item**: tipo, peso, valor, nível, encarnação, onde se veste e o efeito.
>
> ```
> list 1 -> Objeto: 'um livro imaterial' Tipo: LIVRO-MAGIAS
>           O item é: BRILHO ENTALHADO
>           Peso: 1, Valor: 10, Nível: 75, Encarnação: 1
>           Este livro faz seu counter shield melhorar em 5%.
> ```
>
> **É a única loja onde se inspeciona antes de comprar.**
>
> **Testado para achar o limite:** na loja comum, `list 1` é lido como **filtro de palavra** e responde
> *"Por enquanto, nada disto está sendo vendido"*. **O número só é índice na loja divina.**
>
> **Ou seja: o veredito abaixo vale para MERCADOR COMUM. Não generalizar.** A conclusão anterior,
> escrita antes desta descoberta, está corrigida aqui e não apagada — o erro era generalizar.
>
> *(Bônus do mesmo teste: o armeiro oferece **`repair <item>`** para consertar equipamento.)*

> **`help valor`** — *"Antes de vender um item para uma loja, você pode perguntar ao lojista quanto
> ele está inclinado a pagar por isso."* — **é para VENDER, não para inspecionar estoque.**

### 4.2 O bruteforce: 19 verbos contra *Uma espada longa* (779 ouros)

| Verbo | Resposta | Serve? |
|---|---|---|
| `look`, `examine`, `read` | *"Você não está vendo nada parecido com isso."* | não |
| `value` | *"Você não parece ter essa arma!"* | não — só o que ela carrega |
| `identify` | *"Você não tem nenhuma espada."* | não — só o que ela carrega |
| `study` | idem `identify` | não |
| `consider` | *"Comparar sua força com a de quem?"* | não — só criaturas |
| `diagnose` | *"Não há ninguém com esse nome aqui."* | não — só criaturas |
| `check` | *(vazio)* | não — `help check` mostra que é **correio** |
| `display` | *"Uso: display \<número\>"* | não — é **seletor de prompt de vitais** |
| `itemgroup` | *(texto de toggle)* | não — agrupa itens ao andar |
| `appraise`, `inspect`, `probe`, `analyze`, `compare`, `assess`, `evaluate`, `measure`, `weigh` | *"Como?!?"* | **não existem** |

**Nenhum verbo revela propriedades.** O balcão e a prateleira também não são examináveis
(*"Você não está vendo nada parecido com isso"*).

### 4.3 A conveniência que o bruteforce achou

> **`help comprar`** — *"comprar \<nome do item\>"* **ou** *"comprar **#\<número\>**"*

**Dá para comprar pelo número da lista** — `comprar #12` pega a espada longa. Sem digitar o nome
inteiro e sem risco de casar com o item errado.

### 4.4 O `list` aceita filtro por palavra do item

```
list espada  ->  só as espadas, com os MESMOS números da lista completa
list adaga   ->  só as adagas
list armas   ->  "Por enquanto, nada disto está sendo vendido."
```

O `help` chama de "tipo do objeto" e dá o exemplo `listar espada`. Na prática casa a **palavra do
nome do item**: `armas`, `arma`, `armadura`, `todas` e inglês **não** funcionam.

### 4.5 A heurística que isso sugere

**Para item barato, comprar É a avaliação.** A adaga custa **12**, a clava de madeira **15**, a tocha
**15**. Descobrir o que fazem custa quase nada — e o que não servir vai para a **Sala de Doações**.

**Para item caro, não.** A espada longa custa 779 e não há como saber o que ela faz antes de pagar.
Aí a decisão sai do único dado duro disponível: o **nível mínimo** — e, dos 11 itens da Loja de
Armas, todos os 11 são usáveis por ela (nível ≤ 11 contra o nível 20 dela). O que decide é preço
contra utilidade, não requisito.

**Depois de comprar**, aí sim: `identify` descreve o alvo (a magia é de mago nível 22, mas o comando
funciona grátis abaixo do nível 80) e `value` diz quanto o mercador paga.

---

## 5. Defeito de mapa que a auditoria revelou

A varredura das 17 lojas **falhou em 11**, e a falha é informação: a rota levava ao lugar certo, mas
o **nome** não batia — porque curadoria e levantamento batizaram o mesmo lugar de formas diferentes.

| ID no mapa (curadoria) | Nome esperado | Nome que o jogo mostra |
|---|---|---|
| `correio_midgaard` | O Correio de Midgaard | **O Escritório dos Correios** |
| `bar_javali` | O Bar do Javali Roncador | **O Bar da Estalagem Javali Roncador** |
| `recepcao_javali` | A Recepção da Estalagem | A Entrada da Estalagem Javali Roncador |

**São o mesmo lugar com dois nomes — e o mapa tem os dois como salas separadas.** Variantes de nome
como essas o pareamento tolerante não pega (são nomes genuinamente diferentes), mas **a caminhada
prova a identidade**: se a rota até `correio_midgaard` termina em "O Escritório dos Correios", os
dois ids são a mesma sala.

Outras 8 falhas não são duplicata, são **rota/graph**:
- `bar_necromantes`: o guarda barra — *"só necromantes entram aqui"*
- `guilda_magos`, `laboratorio_magos`, `bar_magos`: a rota parou em Rua Principal ou na Guilda dos Paladinos
- `padaria`, `loja_magias`, `loja_armaduras`: ela não saiu do lugar na primeira tentativa

**Próximo passo:** casar os ids duplicados por **prova de caminhada** (a rota chegou lá = é o mesmo
lugar), e melhorar as rotas para as lojas que falharam por graph incompleto.

---

> **Origem**: `automato/rotinas/mercado.py` (a auditoria), lida em 2026-10-16. O `list` roda em
> cada loja e a tabela sai do próprio jogo. **Invisibilidade bloqueia comércio** — o balconista
> responde *"Não negocio com quem não vejo!"* — e a rotina resolve com o comando `visible`.
