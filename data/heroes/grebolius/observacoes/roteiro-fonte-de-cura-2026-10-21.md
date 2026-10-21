# Roteiro — em busca de uma fonte de cura (subtrama do Capítulo 12)

> **Ordem do autor (2026-10-21):** esta subtrama vem **antes** das missões do capítulo 12.
> Registro canônico: `capitulos.json` → capítulo 12 → `subplots[]` (`id: fonte-de-cura`).
> É **sondagem**, não combate e não compra: quase tudo é `list`.

**Autoria:** roteiro escrito pelo autor e transcrito por DeepSeek deepseek-flash (dsh) em 2026-10-21.
**O que é hipótese, não fato:** "`list` é grátis", "não existem `listar`/`recitar`/`usar`/`zap`/`beber`",
saturação 24 e "tick" — nada disso está medido nos transcripts. Trate como ponto de partida e registre
a resposta literal. O que **está** medido: fome/sede custam ~3 hp/tick, o sono devolve ~5 hp/min,
e magia falha no Templo e na Loja de Magias ("Sua magia falha e desaparece").

## 0. Regras do teste (para não custar caro)

- **`list` é grátis.** Nenhum teste abaixo compra nada sem OK explícito do autor.
- **Teto de gasto:** 5% do ouro = **1.588** (na data: 31.769 no total). Autorizado **até 3.500** só para
  o cajado de Lyon (comprar → `identify` → revender) e **zero** no resto até saber o efeito.
- **Não testar magia no Templo nem em loja** (`NO_MAGIC`): pergaminho/poção/varinha falham. Teste na **Praça**.
- **Comandos que funcionam:** `list`, `recite`, `use`, `hold`, `curar`, `drink`, `cast 'identify'`.
  **Alegação de que não existem:** `listar`, `recitar`, `usar`, `zap`, `beber` — confirmar antes de usar.
- Se levar aggro: `recall` na hora. **Sem luta neste roteiro.**
- **Modo (§26):** é sondagem comercial dentro de `missão` — à mão, linha a linha, **sem compra**.
  Não é preciso inventar um sexto modo; a compra, se houver, é a exceção que pede o OK do autor.

## 1. Antes de sair (2 min)

- [ ] `score tudo` → anotar **HP atual/máx**, ouro na mão e no banco, peso.
- [ ] `withdraw 4000` (a loja compra com ouro **na mão**).
- [ ] Comer/beber até saciado; `fill cantil fonte`.
- [ ] `inventory` → espaço para 1 item novo (peso já está ~110/115).

## 2. Bloco A — Midgaard (10 min, risco zero)

**A1. Guilda dos Clérigos** — o candidato mais óbvio e nunca testado.
Rota: Praça do Templo → `o` → Entrada da Guilda → `look` → `exits`.
- [ ] `stand` / `curar`
- [ ] Se `Como?!?`, ir `n` e `s` (salas internas) e repetir `curar`.

**A2. Loja de Magias** (norte da Praça do Comércio)
- [ ] `list` → copiar a lista inteira.
- [ ] `list 1`, `list 2`… até o último → procurar `heal`, `cure critic`, `cure light`, `sanctuary`,
      `remove poison`.
- [ ] Anotar preço + nível de cada um.

**A3. Sala de Doações** (Templo → `l`)
- [ ] `look` → se houver poção/pergaminho/cajado, `look <item>` e anotar (é de graça).

**A4. Fonte da Praça do Templo** (só com sede)
- [ ] `drink fonte` → anotar HP/mana antes/depois. O texto promete sede e mana; **vida nunca foi medida**.

## 3. Bloco B — Jareth (15 min, no caminho da Torre)

**B1. As Misturas de Clariss** (Avenida Floris → `s`)
- [ ] `list` (deve dar os 2 já conhecidos) e `list 1` / `list 2` para ver os atributos.

**B2. Pergaminhos e Afins** (Rua do Rio)
- [ ] `list` + `list <n>` → procurar pergaminho de cura. Já se sabe: retorno 6.209, remover maldições 4.369.

**B3. Templo de Todos e Ninguém** (Jareth — **rota não está no `mapa.json`**; visitado no Dia 157)
- [ ] `look`, `stand`, `curar`.
- [ ] **Anotar a rota** (sala anterior, direção) para o mapa.

**B4. Banco de Sangue** (Jareth — mesma situação: visitado, sem rota no mapa)
- [ ] `look`, `stand`, `curar`.
- [ ] Anotar a rota. **É o candidato nº 1 a serviço de cura** pelo nome.

**B5. Guilda dos Magos de Jareth** (Recepção/Sala de Leitura)
- [ ] Se houver loja: `list` + `list <n>`.

## 4. Bloco C — Lyon (só se a rota do tomo passar; **de dia**, as lojas fecham à noite)

**C1. Pierre — Loja de Magias da França.** Já catalogado: `cajado mágico` 3.150, `poção mágica` 9.835,
`poção cor de creme` 21.462, `poção marrom` 2.940.
- [ ] `list` + `list <n>` em **cada um** → é aqui que pode estar a cura.
- [ ] **`poção mágica` (9.835)** é o nome genérico mais suspeito.
- [ ] **`cajado mágico` (3.150)** é barato: se `list <n>` não revelar o efeito, comprar com OK,
      `cast 'identify' cajado`, revender.

**C2. Toulouse — Itens Variados.** `list` + `list <n>`.

## 5. Bloco D — teste de efeito (só quando HP < máximo)

Presença e preço se testam com vida cheia; **efeito precisa de déficit**. Fazer depois do primeiro
combate da sessão.

- [ ] `score` (HP antes)
- [ ] Pergaminho: `recite <pergaminho>`
- [ ] Varinha: `hold <varinha>` → `use <varinha> grebolius`
- [ ] Cajado: `hold <cajado>` → `use <cajado>` — **atinge todos menos você**; só serve em outro
- [ ] Poção: `quaff <poção>`
- [ ] `score` (HP depois) + anotar se consumiu carga/unidade

## 6. Bloco E — controle negativo

- [ ] `curar` no **Templo de Midgaard** → deve dar `Como?!?`. Serve de régua: qualquer resposta
      diferente nos outros lugares = tem curandeiro.

## 7. Tabela de registro (copiar para `maquina/verificacoes.md`)

| # | Local | Comando | Resposta literal | Preço | HP antes→depois | Veredito |
|---|---|---|---|---|---|---|
| A1 | Guilda dos Clérigos | `curar` | | | | |
| A2 | Loja de Magias | `list 3` | | | | |
| B4 | Banco de Sangue | `curar` | | | | |
| C1 | Pierre | `list 2` | | | | |

## 8. O que cada resultado decide

- **`curar` ≠ `Como?!?`** → achou o serviço. Próximo passo: com HP baixo, `curar` e medir
  **ouro gasto ÷ HP ganho**. Se der < ~10 ouro/HP, virou o método padrão.
- **`list <n>` mostra `heal`** → ouro/HP = preço ÷ ~100 (heal = 100+3d8, teto 100). Compare com dormir
  (grátis, ~5 hp/min). Só vale emergência/chefe.
- **`list <n>` não existe** → compre o item **mais barato**, `cast 'identify'` (é de graça), revenda.
  Anote a perda.
- **Tudo negativo** → registrar e fechar a via: sobra prevenção (`sanctuary`/`armor`/`invisibility`/
  `sleep`/`wimpy`) + sono em fatias.

## 9. O que NÃO fazer

- Não comprar o **cetro de 22.999** (já tem dois) nem a **poção de 9.835** no escuro.
- Não dar `give`, não `quit`, não `donate`/`junk`.
- Não testar magia dentro do Templo/lojas.
- Não repetir `curar` num lugar que já deu `Como?!?` (é comando desconhecido, não falta de vida).
