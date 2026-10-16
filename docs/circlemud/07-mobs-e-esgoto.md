# 07 — Mobs dos esgotos do CircleMUD 3.1: nível, HP, dano e "para que nível é o esgoto?"

Pesquisa sobre o **MUNDO PADRÃO** do CircleMUD 3.1 (mirror
[Yuffster/CircleMUD](https://github.com/Yuffster/CircleMUD), branch `master`, commit único
`12a0cedb` — *"Initial commit of 3.1."*, 2012-03-22), lendo os arquivos de mob
(`lib/world/mob/*.mob`), os resets das zonas (`lib/world/zon/*.zon`) e o **código que lê esses
arquivos** (`src/db.c`), para responder duas perguntas:

1. **"Os mobs dos esgotos têm força parecida?"**
2. **"Qual nível é bom para limpar o esgoto?"**

> **Aviso de idioma e de origem.** Todo nome aqui é o **nome em inglês do mundo padrão**
> (`the sewer rat`, `the red dragon`…). O **DeBo é traduzido e modificado** (o banner do
> servidor diz *"Baseado no CircleMUD 3.0"*), e **nenhum vnum ou nome deste documento prova o
> que existe no DeBo**. Ver §8.

---

## Fonte consultada

Método: o repositório foi baixado inteiro como tarball
(`https://codeload.github.com/Yuffster/CircleMUD/tar.gz/refs/heads/master`, HTTP 200,
1.382.751 bytes) e lido localmente; as URLs cruas foram conferidas por HTTP para os arquivos de
mob (para pegar os 404 de verdade).

| Arquivo | URL crua (base `https://raw.githubusercontent.com/Yuffster/CircleMUD/master/`) | Resultado |
|---|---|---|
| `lib/world/mob/index` | [mob/index](https://raw.githubusercontent.com/Yuffster/CircleMUD/master/lib/world/mob/index) | 200 — lista **27** `.mob`; **não** lista `71.mob` nem `73.mob` |
| `lib/world/mob/70.mob` | [mob/70.mob](https://raw.githubusercontent.com/Yuffster/CircleMUD/master/lib/world/mob/70.mob) | 200 — 5.862 bytes, 234 linhas, mobs **#7000–#7046** |
| `lib/world/mob/72.mob` | [mob/72.mob](https://raw.githubusercontent.com/Yuffster/CircleMUD/master/lib/world/mob/72.mob) | 200 — 1.660 bytes, 64 linhas, mobs **#7200–#7204** |
| `lib/world/mob/71.mob` | [mob/71.mob](https://raw.githubusercontent.com/Yuffster/CircleMUD/master/lib/world/mob/71.mob) | **404 — NÃO EXISTE** (a zona 71 não define mobs próprios) |
| `lib/world/mob/73.mob` | [mob/73.mob](https://raw.githubusercontent.com/Yuffster/CircleMUD/master/lib/world/mob/73.mob) | **404 — NÃO EXISTE** (a zona 73 usa mobs `70xx`) |
| `lib/world/zon/70.zon` … `73.zon` | [zon/70.zon](https://raw.githubusercontent.com/Yuffster/CircleMUD/master/lib/world/zon/70.zon) | 200 — os quatro existem e terminam em `$`; 12 / 10 / 23 / 8 comandos `M` |
| `lib/world/mob/30.mob`, `31.mob`, `36.mob`, `186.mob` | idem | 200 — usados só para comparação (§6) |
| `lib/world/zon/30.zon`, `31.zon`, `36.zon`, `186.zon` | idem | 200 — usados só para comparação (§6) |
| `src/db.c` | [src/db.c](https://raw.githubusercontent.com/Yuffster/CircleMUD/master/src/db.c) | `parse_mobile` (`:1316`), `parse_simple_mob` (`:1117`), `read_mobile` (`:1801`), `reset_zone` (`:1982`) |
| `src/utils.c` | [src/utils.c](https://raw.githubusercontent.com/Yuffster/CircleMUD/master/src/utils.c) | `dice()` em `:61` |
| `src/constants.c` | [src/constants.c](https://raw.githubusercontent.com/Yuffster/CircleMUD/master/src/constants.c) | `action_bits[]` em `:139`, `affected_bits[]` em `:192` |
| `src/fight.c` | [src/fight.c](https://raw.githubusercontent.com/Yuffster/CircleMUD/master/src/fight.c) | teste de acerto em `:891` e `:909` |
| `src/spec_assign.c` | [src/spec_assign.c](https://raw.githubusercontent.com/Yuffster/CircleMUD/master/src/spec_assign.c) | `:191-195` — as *procedures* dos mobs `70xx`/`72xx` |
| `src/spec_procs.c` | [src/spec_procs.c](https://raw.githubusercontent.com/Yuffster/CircleMUD/master/src/spec_procs.c) | `snake` `:360-371`, `magic_user` `:392-461` |

Contagem medida: **23 mobs** definidos nos intervalos de vnum das quatro zonas de esgoto
(18 em `70.mob` + 5 em `72.mob`) e **20 deles são realmente colocados no mundo** por
**53 comandos `M`** somados nas quatro zonas.

---

## Limites desta pesquisa

1. **Só o mundo padrão.** Li o `.mob`/`.zon` do repositório e o código do engine. Não tenho
   acesso a nenhum arquivo do DeBo. O DeBo é CircleMUD 3.0 **traduzido e modificado**; vnum,
   nome, nível e distribuição podem ser outros.
2. **"Quantos nascem" = quantos comandos `M`.** Cada linha `M` carrega **1** mob se o total
   vivo daquele vnum for menor que o campo `max` (`src/db.c:1982-1989`). Ou seja: os números de
   §2 são o **teto do reset**; se parte já estiver viva, nasce menos.
3. **`71.mob` e `73.mob` não existem** (HTTP 404 confirmado). As zonas 71 e 73 existem como
   `.zon` e colocam mobs de vnum `70xx`. Isso é o mesmo padrão já visto nas salas
   (`wld/73.wld` também não existe — ver [05-mundo-padrao-vs-mapa.md](05-mundo-padrao-vs-mapa.md)).
4. **Não joguei.** Os números de HP e dano são **faixas calculadas pelos dados** (§4, §5), não
   dano observado. Nenhuma validação em servidor foi feita nesta pesquisa.
5. **Não verifiquei** as *procedures* de todos os 20 mobs linha a linha; citei as quatro que
   existem para os esgotos (`snake`, `magic_user` ×3).
6. **`consider` do jogo compara só nível** (`src/act.informative.c:1452-1496`, já citado em
   [02-navegacao.md](02-navegacao.md)), então ele **não** vê AC, HP nem *spec proc* — daí a
   diferença entre "nível parecido" e "perigo parecido" em §7.

---

## 0. Como o engine lê um mob (ordem exata dos campos — não adivinhada)

`parse_mobile()` (`src/db.c:1316-1394`) lê, nesta ordem:

| # | Campo | Onde é lido | Observação |
|---|---|---|---|
| 1 | `name` (aliases) até `~` | `db.c:1338` | é o campo usado por `look`/ataque por nome |
| 2 | `short_descr` até `~` | `db.c:1339` | o "nome" mostrado |
| 3 | `long_descr` até `~` | `db.c:1344` | a linha da sala |
| 4 | `description` até `~` | `db.c:1345` | texto de `look <mob>` (multi-linha) |
| 5 | `<action flags> <affect flags> <alignment> <S\|E>` | `db.c:1358-1377` | `action_bits` = `constants.c:139`; `affected_bits` = `constants.c:192`; letra `S` = *simple*, `E` = *enhanced* |
| 6 | `<level> <hitroll> <AC> <Hd>d<Hs>+<Hp> <Dd>d<Ds>+<Dp>` | `db.c:1134-1156` | **esta é a linha mais importante** |
| 7 | `<gold> <exp>` | `db.c:1164-1171` | |
| 8 | `<pos> <default pos> <sex>` | `db.c:1179-1187` | |

Consequências da linha 6 (`parse_simple_mob`, `src/db.c:1141-1156`):

| Campo do arquivo | Vira no engine | Linha |
|---|---|---|
| 1º número | `GET_LEVEL` — **o nível** | `db.c:1141` |
| 2º número | `GET_HITROLL = 20 − valor` | `db.c:1142` |
| 3º número | `GET_AC = 10 × valor` | `db.c:1143` |
| 4º (`Hd`), 5º (`Hs`), 6º (`Hp`) | dados de HP: `hit`, `mana`, `move` | `db.c:1147-1149` |
| 7º (`Dd`), 8º (`Ds`), 9º (`Dp`) | dados de dano: `damnodice`, `damsizedice`, `damroll` | `db.c:1154-1156` |

A flag `MOB_ISNPC` é forçada em todo mob (`db.c:1366`). Todas as letras de flag seguem
`'a' = bit 0, 'b' = bit 1, …` (`asciiflag_conv`, `src/db.c:877-897`), portanto
`f`=`AGGR`, `g`=`STAY-ZONE`, `b`=`SENTINEL`, `c`=`SCAVENGER`, `m`=`HELPER`, `h`=`WIMPY`,
`k` (2ª letra) = `INFRA`, etc.

**Todos os 23 mobs definidos nos intervalos das zonas de esgoto são do tipo `S` (simple)** —
verificado: nenhum mob de `70.mob`/`72.mob` usa a seção `E`. Isso importa para o HP (§4).

---

## 1. Tabela de afirmações

Níveis: **Testado (código/mundo padrão)** = número lido do arquivo padrão ou do fonte, com
`arquivo:linha`/`#vnum` citado — prova **o mundo padrão**, não o DeBo.
**Provável** = decorre do padrão e é o esperado no DeBo, mas depende da tradução/modificação.
**Dúvida** = depende de dado que não temos (`.mob`/`.zon` do DeBo) ou há divergência de fontes.

| # | Afirmação | Nível | Fonte (arquivo:linha/#vnum) | Como validar no DeBo |
|---|---|---|---|---|
| 1 | Os esgotos são as zonas **70, 71, 72 e 73** ("The Sewer, First Level", "The Second Sewer", "The Sewer Maze", "The Tunnels In The Sewer") | Testado | `zon/70.zon:1-2`, `zon/71.zon:1-2`, `zon/72.zon:1-2`, `zon/73.zon:1-2` | descer pelo Depósito de Lixo e ler o nome que o jogo dá a cada área |
| 2 | **`71.mob` e `73.mob` não existem** (404); os mobs do esgoto estão em **`70.mob` e `72.mob`** | Testado | HTTP 404 nos dois; `mob/index` (27 `.mob`) **não** lista nem `71.mob` nem `73.mob` | — (é organização de arquivo; não é observável no jogo) |
| 3 | Nos intervalos de vnum das 4 zonas existem **23 mobs**: 18 em `70.mob` (#7000–#7010, #7040–#7046) e 5 em `72.mob` (#7200–#7204) | Testado | `70.mob` (blocos `#7000`…`#7046`), `72.mob` (blocos `#7200`…`#7204`) | listar `#vnum` no DeBo é impossível para mortal: contar mobs distintos encontrados |
| 4 | Nascem **53 mobs** por reset nas 4 zonas: **12** (70) + **10** (71) + **23** (72) + **8** (73), de **20 tipos distintos** | Testado | comandos `M` em `70.zon:6-17`, `71.zon:6-15`, `72.zon:6-43`, `73.zon:6-13`; regra em `db.c:1982-1989` | limpar uma área e contar os mobs que voltam no repovoamento |
| 5 | **3 mobs definidos nunca nascem em lugar nenhum do mundo**: o wanderer (#7007), o homunculus (#7008) e o morkoth (#7009) | Testado | definidos em `70.mob:92`, `:104`, `:117`; **nenhum** comando `M` em **nenhum** `.zon` do mundo cita 7007/7008/7009 (varredura dos 30 `.zon` listados em `zon/index`) | não procurar: eles não são postos no mundo pelo reset padrão |
| 6 | Nível dos mobs do esgoto: **mínimo 1, máximo 19, mediana 10** (por tipo); **mediana 6** se ponderado pelas 53 cópias que nascem | Testado | §3; níveis na 1ª linha de dados de cada bloco `#vnum` de `70.mob`/`72.mob` (a que segue as quatro strings `~`) | `consider` nos mobs e comparar com a escala de `act.informative.c:1452-1496` |
| 7 | Faixas: **1-5: 6 tipos**, **6-10: 8**, **11-15: 8**, **16-20: 1**, 21+: 0 | Testado | §3 | idem |
| 8 | O único mob acima de 15 é o **dragon vermelho #7040 (nível 19)** | Testado | `70.mob:141` (nível na linha 150); nasce em `73.zon:6` (sala 7328) | `consider` nele: com um personagem de nível 9 ou menos, a resposta deve ser "Are you mad!?" ou pior |
| 9 | Os "chefes" do esgoto são **#7040 dragon (19)**, **#7041 sea hag (14)**, **#7200 master mindflayer (14)** e **#7043 basilisk (13)** | Testado | `70.mob:141`, `:154`, `:181`; `72.mob:1` | `consider` nos quatro, na ordem, e comparar as frases |
| 10 | O HP **não** é o 4º número da linha: o engine sorteia `dice(Hd, Hs) + Hp` | Testado | `db.c:1820-1822` (`mob->points.max_hit = dice(hit, mana) + move`) usando `hit/mana/move` gravados em `db.c:1147-1149` | `diagnose`/`consider` não bastam: medir o HP batendo (a faixa de §4 dá o intervalo esperado) |
| 11 | `dice(n, s)` = soma de `n` sorteios uniformes de 1..`s` (`utils.c:61-72`); logo `XdY+Z` vai de **X+Z** a **X·Y+Z**, média **X·(Y+1)/2 + Z** | Testado | `src/utils.c:61-72` | — |
| 12 | HP dos mobs do esgoto vai de **9** (spider #7003) a **250** (dragon #7040); o mais "gordo" fora dos chefes é o chr-eff'n #7010 (150-200) | Testado | §4 | matar cronometrando os golpes, ou `diagnose` |
| 13 | Dano por golpe vai de **1** (bat #7001, spider #7003) a **21** (dragon #7040); fora dele o máximo é 17 (sea hag) e 16 (basilisk, master mindflayer) | Testado | §5; `db.c:1154-1156` | anotar o dano recebido por golpe de cada mob |
| 14 | O 3º número é **AC÷10**: `GET_AC = 10 × valor`; no acerto o engine compara com `AC/10`, e **AC menor = mais difícil de acertar** | Testado | `db.c:1143`; `fight.c:891` e `:909` | comparar quantos golpes erram contra o maggot (AC 90) e contra o dragon (AC 0) |
| 15 | O 2º número é o hitroll **invertido**: `GET_HITROLL = 20 − valor` | Testado | `db.c:1142` | indireto: mobs com hitroll alto acertam mais; ver o dano recebido por rodada |
| 16 | Os mobs do esgoto têm AC **0, 10, 20, 30, 40, 50, 60, 70 ou 90**; AC 0 é do dragon, do basilisk e do master mindflayer | Testado | §2 (coluna AC; valor cru ×10 em `db.c:1143`) | idem #14 |
| 17 | Das ~53 cópias que nascem, **23 são de nível 1-5** e **16 de nível 6-10** — o esgoto é majoritariamente fraco | Testado | §3 (histograma ponderado) | contagem de mobs ao limpar |
| 18 | O esgoto tem **10 wererats nível 6** — o maior bloco de um só tipo | Testado | `72.zon:18-31` (10 comandos `M` de #7203, `max 10`) | sala 7214 e vizinhas do labirinto: contar os ratos |
| 19 | Os três **mindflayers** (#7200/#7201/#7202) têm a *spec proc* `magic_user`; ela conjura **por nível**: 6-7 `chill touch`, 8-9 `burning hands`, 12-13 `lightning bolt`, 14-17 `color spray` (+ cegueira se nível > 7, veneno se > 13, `energy drain` se maligno e nível > 12) | Testado | `spec_assign.c:193-195`; `spec_procs.c:392-461` (tabela `:428-457`, extras `:412-423`) | enfrentá-los e registrar qual magia sai (nomes traduzidos) |
| 20 | A **cobra #7006** tem a *spec proc* `snake`: a cada rodada, chance `1/(nível+1)` de morder e conjurar `SPELL_POISON` — o autor comenta *"Quite lethal to low-level characters"* | Testado | `spec_assign.c:191`; `spec_procs.c:357-371` (comentário `:358`, poison `:370`) | lutar contra a cobra e olhar `affects`/`score` depois |
| 21 | O **dragon #7040** é `MOB_SENTINEL + MOB_AWARE + MOB_AGGR + MOB_NO_CHARM + MOB_NO_SUMMN + MOB_NO_BASH` e tem `SANCT` (afeto) — não vagueia, ataca quem entra, não pode ser encantado nem derrubado; **não** é imune a sono (não tem `NO_SLEEP`) | Testado | `70.mob:150` (`befnoq dhkp -1000 S`) vs `constants.c:139`/`:192` | entrar na sala 7328 sem atacar; ele deve atacar. Tentar `sleep` nele se a magia existir |
| 22 | Os **wererats** têm `AGGR_GOOD` e `AGGR_NEUTRAL` — atacam quem é bom ou neutro, e não atacam quem é mau | Testado | `72.mob:48` (`cgjlk k -700 S`); semântica em `db.c:1379-1381`, `mobact.c:96-114` | entrar com alinhamento neutro e com alinhamento mau e comparar |
| 23 | Midgaard (zonas 30+31) tem mediana de nível **24/3**, tabuleiro (36) **25,5**, Zona dos Novatos (186) **4** — contra **10** do esgoto por tipo | Testado | §6 (contagem própria sobre `30.mob`, `31.mob`, `36.mob`, `186.mob`) | `consider` em amostras de cada zona |
| 24 | Em Midgaard o **nível não mede perigo**: os lojistas de **nível 33** (ex. #3000 the wizard, #3001 the baker) são `SENTINEL` sem `AGGR` e têm **30.001 HP** (`1d1+30000`); os guildmasters de nível **34** (#3020-3023) têm 646-800 HP | Testado | `30.mob:23` (`33 0 -10 1d1+30000 2d8+18`), `30.mob:143` (`34 0 -10 6d10+640 1d8+24`); flags em `30.mob:1`, `:133` | atacar um lojista é decisão de sessão autorizada — não fazer sem autorização |
| 25 | A afirmação #101 de [04-especiais-easter-eggs.md](04-especiais-easter-eggs.md) atribui "nível 1" ao bat/rat/spider e "nível 2" ao beetle/maggot/mudmonster/snake. **O `.mob` diz outra coisa**: bat 1, spider 1, maggot 3, snake 4, rat 5, beetle 8, mudmonster 12 | Testado | `70.mob:15` (bat 1), `:41` (spider 1), `:66` (maggot 3), `:78` (snake 4), `:28` (rat 5), `:53` (beetle 8), `:1` (mudmonster 12) | `consider` em cada um: a ordem das frases deve seguir estes níveis |

---

## 2. Tabela completa dos mobs dos esgotos (zonas 70, 71, 72, 73)

Colunas: `#vnum (arquivo:linha do bloco)` · nome (`short_descr`) · nível · dados de HP · faixa de
HP · dados de dano · faixa de dano por golpe · AC (já ×10) · hitroll/damroll · flags de ação
(`MOB_*`) · quantas cópias nascem (nº de comandos `M`) · salas de origem (vnum) · onde nasce.
Os três mobs que **nunca nascem** estão marcados com ⃰ na sub-tabela §2.1.

| #vnum (fonte) | nome | lvl | HP (dados) | HP mín-máx | dano (dados) | dano mín-máx | AC | hit/dam | flags (`MOB_*`) | nasce | salas (`zon`) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| **#7000** (`70.mob:1`) | the horrifying Mudmonster | 12 | `4d6+140` | 144-164 | `2d5+3` | 5-13 | 20 | 11 / 3 | `STAY-ZONE`,`NO_BASH`,`NO_BLIND` | **7** | 7103×2, 7286×2, 7281×2, 7280 (`71.zon:11-12`, `72.zon:39-43`) |
| **#7001** (`70.mob:15`) | the small bat | 1 | `5d2+6` | 11-16 | `1d5+0` | 1-5 | 50 | 0 / 0 | `AGGR`,`STAY-ZONE`,`NO_BLIND` | **4** | 7041, 7025, 7004×2 (`70.zon:6-9`) |
| **#7002** (`70.mob:28`) | the sewer rat | 5 | `1d12+48` | 49-60 | `2d4+0` | 2-8 | 50 | 4 / 0 | `AGGR` | **6** | 7049, 7031 (`70.zon:10-11`); 7104 (`71.zon:10`); 7285×3 (`72.zon:33,34,38`) |
| **#7003** (`70.mob:41`) | the small Spider | 1 | `1d12+8` | 9-20 | `1d4+0` | 1-4 | 30 | 0 / 0 | `AGGR` | **6** | 7039×3, 7037×2, 7050 (`70.zon:12-17`) |
| **#7004** (`70.mob:53`) | the giant earth beetle | 8 | `2d10+98` | 100-118 | `2d4+2` | 4-10 | 30 | 7 / 2 | *(nenhuma)* | **1** | 7102 (`71.zon:6`) |
| **#7005** (`70.mob:66`) | the maggot | 3 | `2d5+35` | 37-45 | `1d7+0` | 1-7 | 90 | 3 / 0 | `NO_BASH`,`NO_BLIND` | **3** | 7112×2, 7122 (`71.zon:7-9`) |
| **#7006** (`70.mob:78`) | the snake | 4 | `2d5+40` | 42-50 | `1d9+0` | 1-9 | 70 | 4 / 0 | `SPEC`,`AGGR` | **3** | 7113, 7122×2 (`71.zon:13-15`) |
| **#7010** (`70.mob:129`) | the evil chr-eff'n | 12 | `2d26+148` | 150-200 | `2d7+1` | 3-15 | 20 | 11 / 1 | `SCAVENGER`,`WIMPY` | **1** | 7329 (`73.zon:13`) |
| **#7040** (`70.mob:141`) | the red dragon | **19** | `5d4+230` | 235-250 | `3d6+3` | 6-21 | **0** | 18 / 3 | `SENTINEL`,`AWARE`,`AGGR`,`NO_CHARM`,`NO_SUMMN`,`NO_BASH` | **1** | 7328 (`73.zon:6`) |
| **#7041** (`70.mob:154`) | the sea hag | **14** | `1d8+172` | 173-180 | `2d8+1` | 3-17 | 10 | 13 / 1 | `AGGR` | **1** | 7344 (`73.zon:7`, `max 2`) |
| **#7042** (`70.mob:167`) | the guardian naga | 12 | `1d18+148` | 149-166 | `2d7+1` | 3-15 | 20 | 11 / 1 | `SENTINEL` | **1** | 7335 (`73.zon:8`, `max 2`) |
| **#7043** (`70.mob:181`) | the scaled basilisk | **13** | `1d12+160` | 161-172 | `2d7+2` | 4-16 | **0** | 9 / 2 | `SCAVENGER` | **1** | 7339 (`73.zon:9`, `max 3`) |
| **#7044** (`70.mob:194`) | the lemure | 5 | `3d5+57` | 60-72 | `2d4+0` | 2-8 | 60 | 4 / 0 | `AGGR`,`NO_CHARM`,`NO_BASH` | **1** | 7306 (`73.zon:10`, `max 6`) |
| **#7045** (`70.mob:208`) | Jones 'cruncher' ettin | 10 | `1d5+130` | 131-135 | `2d6+2` | 4-14 | 20 | 9 / 2 | `SCAVENGER` | **1** | 7319 (`73.zon:11`) |
| **#7046** (`70.mob:221`) | Herald 'the mouse-killer' ettin | 6 | `3d5+70` | 73-85 | `1d8+0` | 1-8 | 40 | 6 / 0 | `SCAVENGER` | **1** | 7324 (`73.zon:12`) |
| **#7200** (`72.mob:1`) | the master mindflayer | **14** | `1d10+170` | 171-180 | `3d4+4` | 7-16 | **0** | 13 / 4 | `SPEC`,`SCAVENGER`,`AWARE`,`AGGR`,`MEMORY`,`HELPER` | **1** | 7201 (`72.zon:6`) |
| **#7201** (`72.mob:14`) | the senior mindflayer | 8 | `1d10+100` | 101-110 | `2d4+3` | 5-11 | 20 | 7 / 3 | `SPEC`,`SCAVENGER`,`AWARE`,`AGGR_GOOD`,`AGGR_NEUTRAL`,`MEMORY`,`HELPER` | **1** | 7203 (`72.zon:12`) |
| **#7202** (`72.mob:27`) | the junior mindflayer | 6 | `1d10+75` | 76-85 | `1d4+2` | 3-6 | 40 | 5 / 2 | `SPEC`,`SCAVENGER`,`AWARE`,`WIMPY`,`MEMORY`,`HELPER` | **2** | 7205, 7207 (`72.zon:14,16`) |
| **#7203** (`72.mob:40`) | the ugly wererat | 6 | `4d6+69` | 73-93 | `2d4+2` | 4-10 | 30 | 5 / 2 | `SCAVENGER`,`STAY-ZONE`,`AGGR_GOOD`,`AGGR_NEUTRAL`,`MEMORY` | **10** | 7214, 7213, 7215, 7217, 7219, 7221, 7223, 7225, 7233×2 (`72.zon:18-31`) |
| **#7204** (`72.mob:52`) | the gigantic rat | 12 | `1d10+150` | 151-160 | `2d6+2` | 4-14 | 20 | 11 / 2 | `SENTINEL`,`AGGR` | **1** | 7234 (`72.zon:32`) |

Flags de **afeto** (2ª coluna da linha de flags), para completar: #7000 `INFRA,SNEAK`;
#7001 `INFRA,SNEAK`; #7002 `INFRA`; #7003 `INFRA,SNEAK`; #7004 `INFRA`; #7005 `INFRA`;
#7006 `INFRA`; #7010 `DET-INVIS,INFRA,SNEAK`; #7040 `DET-INVIS,SANCT,INFRA,NO-TRACK`;
#7041 `INFRA`; #7042 `INFRA`; #7043 `DET-INVIS,SENSE-LIFE,INFRA`; #7044 `INFRA`;
#7045 `INFRA`; #7046 `INFRA`; #7200/7201/7202 `DET-INVIS,SENSE-LIFE,INFRA`;
#7203 `INFRA`; #7204 `INFRA`. (Nomes de `src/constants.c:192-217`.)

Alinhamento (3º campo da linha de flags): o extremo maligno é `-1000`, em **#7002 (rat)** e
**#7040 (dragon)**; o extremo bondoso é `+700`, em **#7042 (guardian naga)**. Também são
positivos o **#7005 maggot** (`+300`) e o **#7046 Herald** (`+200`); os outros **17** que nascem
são negativos (de `-250` a `-1000`), assim como os três que não nascem (#7007 `-1000`,
#7008 `-780`, #7009 `-900`).

### 2.1 Os três definidos e nunca usados ⃰

| #vnum (fonte) | nome | lvl | HP | dano | AC | hit/dam | flags | nasce |
|---|---|---|---|---|---|---|---|---|
| ⃰ **#7007** (`70.mob:92`) | the evil wanderer | 10 | `4d10+100` (104-140) | `2d6+1` (3-13) | 20 | 9 / 1 | `SCAVENGER`,`WIMPY` | **0** — nenhum `M` no mundo |
| ⃰ **#7008** (`70.mob:104`) | the creature homunculus | 11 | `6d3+130` (136-148) | `2d6+2` (4-14) | 10 | 10 / 2 | `NO_CHARM`,`NO_SUMMN`,`NO_SLEEP` | **0** — nenhum `M` no mundo |
| ⃰ **#7009** (`70.mob:117`) | the shadowy morkoth | 10 | `1d20+120` (121-140) | `2d6+0` (2-12) | 30 | 8 / 0 | `SPEC`,`AGGR`,`WIMPY` | **0** — nenhum `M` no mundo |

O #7009 ainda tem `magic_user` atribuído (`spec_assign.c:192`), mas sem reset ele só aparece se
um imortal o carregar.

---

## 3. Distribuição de níveis — "os mobs têm força parecida?"

### 3.1 Por **tipo** de mob (23 mobs definidos nas zonas 70-73)

* **mínimo 1 · máximo 19 · mediana 10 · média 8,78 · desvio-padrão 4,56**
* Lista ordenada: `1, 1, 3, 4, 5, 5, 6, 6, 6, 8, 8, 10, 10, 10, 11, 12, 12, 12, 12, 13, 14, 14, 19`

| nível | quantos tipos | quem |
|---|---|---|
| 1 | 2 | bat #7001, spider #7003 |
| 3 | 1 | maggot #7005 |
| 4 | 1 | snake #7006 |
| 5 | 2 | sewer rat #7002, lemure #7044 |
| 6 | 3 | Herald #7046, junior mindflayer #7202, wererat #7203 |
| 8 | 2 | earth beetle #7004, senior mindflayer #7201 |
| 10 | 3 | wanderer #7007 ⃰, morkoth #7009 ⃰, Jones #7045 |
| 11 | 1 | homunculus #7008 ⃰ |
| 12 | 4 | Mudmonster #7000, chr-eff'n #7010, naga #7042, gigantic rat #7204 |
| 13 | 1 | basilisk #7043 |
| 14 | 2 | sea hag #7041, master mindflayer #7200 |
| 19 | 1 | **red dragon #7040** |

⃰ nunca nasce (§2.1).

* Faixas: **1-5 → 6** · **6-10 → 8** · **11-15 → 8** · **16-20 → 1** · **21-30 → 0** · **31+ → 0**

```
  1- 5 | ██████            6
  6-10 | ████████          8
 11-15 | ████████          8
 16-20 | █                 1
 21-30 |                   0
  31+  |                   0
```

### 3.2 Por **cópia que nasce** (53 comandos `M` — o que o jogador realmente encontra)

Pesando cada tipo pelo número de vezes que nasce (#7203 vale 10, #7000 vale 7, #7003 vale 6…):

* **mediana 6 · média 6,58 · mínimo 1 · máximo 19**

```
  1- 5 | ███████████████████████  23
  6-10 | ████████████████         16
 11-15 | █████████████            13
 16-20 | █                         1
```

### 3.3 Resposta direta

**Não, não têm força parecida — mas a assimetria não está onde o nível sugere.**

* O **nível** se concentra em duas faixas: 6-10 e 11-15 (8 tipos cada). A **mediana por cópia é
  6**, porque os dois maiores blocos do jogo (10 wererats nível 6 e 7 mudmonsters nível 12) e os
  mobs do primeiro nível do esgoto são fracos.
* **A variação bruta é grande**: nível 1 → 19 é um fator de 19; HP 9 → 250 é um fator de ~28;
  dano por golpe 1 → 21 é um fator de 21.
* **Fora da curva (chefes):** o **dragon #7040 (19)** está sozinho numa faixa que mais ninguém
  ocupa (só ele tem nível > 15). Depois dele, um degrau com **sea hag #7041 (14)**,
  **master mindflayer #7200 (14)** e **basilisk #7043 (13)**, e um degrau intermediário de
  nível 12 (mudmonster, chr-eff'n, naga, gigantic rat) que já tem 150-200 HP.
* **Empate de nível ≠ empate de força** (ver §7): o `maggot` (nível 3, AC 90, 37-45 HP) e o
  `snake` (nível 4, mas com *spec proc* de veneno) e o `junior mindflayer` (nível 6, mas
  conjurador) não se comparam.

---

## 4. HP efetivo

**Fórmula do engine** (`lib/world/mob/*.mob` → HP): o 4º bloco da linha de dados **não é** o HP
— é `XdY+Z`, e o HP é sorteado a cada carga do mob:

```c
// src/db.c:1820-1822 (read_mobile)
if (!mob->points.max_hit) {
  mob->points.max_hit = dice(mob->points.hit, mob->points.mana) + mob->points.move;
}
// src/utils.c:61-72 — dice(n, s) = soma de n sorteios de 1..s
```

Como todos os mobs dos esgotos são do tipo `S`, `hit/mana/move` vêm exatamente dos números
`Hd/Hs/Hp` da linha de dados (`src/db.c:1147-1149`). Logo:

> **HP = dice(Hd, Hs) + Hp**, isto é, faixa **[Hd + Hp .. Hd·Hs + Hp]** e média
> **Hd·(Hs+1)/2 + Hp**.

| #vnum | mob | dados | faixa de HP | média |
|---|---|---|---|---|
| #7003 | small Spider | `1d12+8` | **9-20** | 14,5 |
| #7001 | small bat | `5d2+6` | **11-16** | 13,5 |
| #7005 | maggot | `2d5+35` | **37-45** | 41 |
| #7006 | snake | `2d5+40` | **42-50** | 46 |
| #7002 | sewer rat | `1d12+48` | **49-60** | 54,5 |
| #7044 | lemure | `3d5+57` | **60-72** | 66 |
| #7046 | Herald ettin | `3d5+70` | **73-85** | 79 |
| #7203 | wererat | `4d6+69` | **73-93** | 83 |
| #7202 | junior mindflayer | `1d10+75` | **76-85** | 80,5 |
| #7004 | giant earth beetle | `2d10+98` | **100-118** | 109 |
| #7201 | senior mindflayer | `1d10+100` | **101-110** | 105,5 |
| #7045 | Jones ettin | `1d5+130` | **131-135** | 133 |
| #7000 | horrifying Mudmonster | `4d6+140` | **144-164** | 154 |
| #7042 | guardian naga | `1d18+148` | **149-166** | 158 |
| #7010 | evil chr-eff'n | `2d26+148` | **150-200** | 175 |
| #7204 | gigantic rat | `1d10+150` | **151-160** | 155,5 |
| #7043 | scaled basilisk | `1d12+160` | **161-172** | 166,5 |
| #7041 | sea hag | `1d8+172` | **173-180** | 176,5 |
| #7200 | master mindflayer | `1d10+170` | **171-180** | 175,5 |
| #7040 | **red dragon** | `5d4+230` | **235-250** | 242,5 |

Adicionais, para contexto: #7007 wanderer 104-140; #7008 homunculus 136-148;
#7009 morkoth 121-140 (os três não nascem).

**Resumo:** o mob mais fraco do esgoto (spider, 9-20 HP) morre em poucos golpes de um
personagem de nível 5; o mais forte (dragon, 235-250 HP, média 242,5) tem **quase 3 vezes** o HP
médio de um wererat (83) e **~28 vezes** o mínimo da aranha (9).

---

## 5. Dano por golpe

Mesma função `dice()`. O 3º bloco da linha de dados (`Dd d Ds + Dp`) vira
`damnodice/damsizedice/damroll` (`src/db.c:1154-1156`) e o dano do golpe é
`dice(damnodice, damsizedice) + damroll`:

> **dano = dice(Dd, Ds) + Dp** → faixa **[Dd + Dp .. Dd·Ds + Dp]**, média **Dd·(Ds+1)/2 + Dp**.

| #vnum | mob | dados | dano mín-máx (por golpe) | média |
|---|---|---|---|---|
| #7001 | small bat | `1d5+0` | **1-5** | 3,0 |
| #7003 | small Spider | `1d4+0` | **1-4** | 2,5 |
| #7005 | maggot | `1d7+0` | **1-7** | 4,0 |
| #7046 | Herald ettin | `1d8+0` | **1-8** | 4,5 |
| #7002 | sewer rat | `2d4+0` | **2-8** | 5,0 |
| #7044 | lemure | `2d4+0` | **2-8** | 5,0 |
| #7006 | snake | `1d9+0` | **1-9** | 5,0 |
| #7202 | junior mindflayer | `1d4+2` | **3-6** | 4,5 |
| #7203 | wererat | `2d4+2` | **4-10** | 7,0 |
| #7004 | giant earth beetle | `2d4+2` | **4-10** | 7,0 |
| #7201 | senior mindflayer | `2d4+3` | **5-11** | 8,0 |
| #7000 | Mudmonster | `2d5+3` | **5-13** | 9,0 |
| #7045 | Jones ettin | `2d6+2` | **4-14** | 9,0 |
| #7010 | chr-eff'n | `2d7+1` | **3-15** | 9,0 |
| #7042 | guardian naga | `2d7+1` | **3-15** | 9,0 |
| #7204 | gigantic rat | `2d6+2` | **4-14** | 9,0 |
| #7041 | sea hag | `2d8+1` | **3-17** | 10,0 |
| #7043 | basilisk | `2d7+2` | **4-16** | 10,0 |
| #7200 | master mindflayer | `3d4+4` | **7-16** | 11,5 |
| #7040 | **red dragon** | `3d6+3` | **6-21** | 13,5 |

(Os três que não nascem: #7007 `2d6+1` = 3-13; #7008 `2d6+2` = 4-14; #7009 `2d6+0` = 2-12.)

**Leitura:** o **dano por golpe no esgoto é baixo e comprimido** — **19 dos 20** mobs têm dano
máximo ≤ 17 (só o dragon chega a 21), e as **médias** ficam em 2,5-13,5, com 16 das 20 entre 4 e
10. Quem mata personagem no esgoto não é o dano do golpe: é
**(a)** volume (10 wererats batendo juntos), **(b)** AC baixa dos chefes que faz o jogador
**errar** muito, e **(c)** as *spec procs* (veneno da cobra, magias dos mindflayers) — §7.

---

## 6. Para comparar: Midgaard (30/31), Zona dos Novatos (186) e Tabuleiro (36)

Mesma medição, sobre `30.mob`+`31.mob`, `186.mob` e `36.mob` (todos os mobs definidos no
intervalo de vnum de cada zona — inclusive NPCs pacíficos):

| Zona | mobs | mín | máx | mediana | média | 1-5 | 6-10 | 11-15 | 16-20 | 21-30 | 31+ |
|---|---|---|---|---|---|---|---|---|---|---|---|
| **Esgoto 70-73** | 23 | 1 | 19 | **10** | 8,8 | 6 | 8 | 8 | 1 | 0 | 0 |
| 30 — Northern Midgaard Main City | 43 | 0 | 34 | **24** | 21,5 | 9 | 3 | 0 | 2 | 6 | 21 |
| 31 — Southern part of Midgaard | 11 | 0 | 33 | **3** | 9,3 | 4 | 1 | 1 | 1 | 1 | 1 |
| 36 — The Chessboard of Midgaard | 12 | 6 | 36 | **25,5** | 23,8 | 0 | 2 | 0 | 2 | 4 | 4 |
| 186 — Newbie Zone | 15 | 1 | 7 | **4** | 3,7 | 13 | 2 | 0 | 0 | 0 | 0 |

**Chefes de cada zona:**

| Zona | chefes (maiores níveis) |
|---|---|
| Esgoto 70-73 | **#7040 red dragon (19)**; depois **#7041 sea hag (14)**, **#7200 master mindflayer (14)**, **#7043 basilisk (13)**, grupo de nível 12 |
| 30 Midgaard | #3020-3023 guildmasters (**34**), #3000-#3010 e #3046/#3095 lojistas (33), #3024-3027 NPCs de guilda (33), #3059 Peacekeeper (17) |
| 31 Midgaard Sul | #3100 the Maid (**33**), #3105 the Mayor (24), #3102 Chief Guard (17), #3104 Secretary (12) |
| 36 Tabuleiro | #3610/#3611 Black/White **King (36)**, #3608/#3609 Queen (32), #3602/#3603 Rook (27), #3606/#3607 Bishop (24), #3604/#3605 Knight (18), #3600/#3601 Pawn (6) |
| 186 Novatos | #18609 massive Minotaur (**7**), #18610 dark spectre (6), #18601/#18605/#18615 nível 5 |

**Três ressalvas que o número cru esconde:**

1. **Midgaard 30/31 não é comparável por nível.** O grosso dos níveis 33-34 é lojista e
   guildmaster `SENTINEL` **sem** `AGGR`: os de nível 33 têm **30.001 HP** (`1d1+30000`, ex.:
   `30.mob:23`) e os guildmasters de nível 34 têm 646-800 HP (`30.mob:143`) — são parede, não
   combate. Se filtrarmos só os mobs com alguma flag de agressão, a
   zona 30 tem níveis **0, 0 e 20** (`#3062`/`#3066` Fido, `#3068` green gelatinous blob), e a
   zona 31 tem **10 e 17** (`#3103` upset cityguard, `#3102` Chief Guard). Ou seja: **a parte
   agressiva de Midgaard (10-20) e o esgoto (1-19) se sobrepõem** — o esgoto é uma área de
   nível médio, não uma área de iniciante.
2. **A Zona dos Novatos (186) é o único lugar realmente mais fraco que o esgoto**: 13 dos 15
   mobs são nível 1-5 e o teto é 7 (Minotauro). Comparar com o esgoto: **6 tipos** de nível 1-5.
3. **O Tabuleiro (36) é muito mais duro**: nada abaixo de nível 6, mediana 25,5 e dois reis
   nível 36 com 2.010-2.100 HP. O esgoto é, no mapa de dificuldade, um **degrau entre a Zona dos
   Novatos e o Tabuleiro/Midgaard hostil**.

---

## 7. Leitura prática

### 7.1 Triviais ou quase (resolvidos entre o nível ~5 e ~8)

| Mob | Por quê |
|---|---|
| **#7001 small bat (1)** e **#7003 small Spider (1)** | 9-20 HP, dano 1-5 e **hitroll 0 / damroll 0**. Aparecem em bando (4 bats, 6 aranhas), mas qualquer um morre em poucos golpes de um personagem de nível ~5. |
| **#7005 maggot (3)** | 37-45 HP, mas **AC 90** (o mais fácil de acertar do esgoto) e dano 1-7. É o mob de "treino" do segundo nível. |
| **#7002 sewer rat (5)** e **#7044 lemure (5)** | 49-72 HP, dano 2-8. O lemure tem `NO_CHARM`/`NO_BASH`, então não dá para encantá-lo nem derrubá-lo — mas o dano dele é baixo. |
| **#7046 Herald ettin (6)**, **#7202 junior mindflayer (6)**, **#7203 wererat (6)** | 73-93 HP e dano baixo (Herald 1-8, wererat 4-10; o junior mindflayer faz 3-6, mas é conjurador). Sozinhos são fáceis. **O wererat só é problema porque nascem 10.** |

### 7.2 Perigosos, e por quê (a partir de nível ~10-12)

| Mob | Perigo |
|---|---|
| **#7040 red dragon (19)** | O chefe. **AC 0** (difícil de acertar), 235-250 HP, dano 6-21 e **hitroll 18**. É `AGGR` + `SENTINEL`: ataca quem entra na sala 7328 e não pode ser encantado/adormecido/derrubado (`NO_CHARM`,`NO_SUMMN`,`NO_BASH`) nem tem rastro (`NO_TRACK`). É o único mob do esgoto acima do nível 15. |
| **#7041 sea hag (14)** | 173-180 HP e o **maior dano não-dragão** (3-17). `AGGR`: ataca na entrada. |
| **#7200 master mindflayer (14)** | 171-180 HP, **AC 0**, dano 7-16 **e** `magic_user` (`spec_assign.c:193`): conjura **`color spray`** (tabela por nível 14-17, `spec_procs.c:449-453`) e, por ser maligno de nível > 13, ainda pode aplicar **veneno** (1/11), **cegueira** (1/9) e **`energy drain`** (1/13) — `spec_procs.c:412-423`. |
| **#7043 basilisk (13)** | 161-172 HP **com AC 0**, dano 4-16. Tem `DET-INVIS`+`SENSE-LIFE`: invisibilidade não resolve. |
| **#7000 Mudmonster (12)**, **#7010 chr-eff'n (12)**, **#7042 naga (12)**, **#7204 gigantic rat (12)** | Todos 144-200 HP com dano médio. O **gigantic rat #7204 é `SENTINEL`+`AGGR`** e o **chr-eff'n** tem `DET-INVIS`. A **naga #7042** é de alinhamento bom (`+700`) e só `SENTINEL` — o texto dela (`70.mob:173-175`) *avisa* o jogador sobre os mobs maus adiante. |
| **#7006 snake (4) — perigo desproporcional ao nível** | Só 42-50 HP, mas tem a *spec proc* `snake` (`spec_assign.c:191`, `spec_procs.c:360-371`): a cada rodada, chance `1/(nível+1)` = **1/5** de morder e conjurar **`SPELL_POISON`**. O próprio autor deixou escrito: *"Quite lethal to low-level characters"* (`spec_procs.c:358`). **É o mob mais "mentiroso" do esgoto em relação ao nível.** |
| **#7201 senior mindflayer (8)** e **#7202 junior mindflayer (6)** | Nível baixo, mas **conjuradores** (`magic_user`): senior → `burning hands` + **cegueira**; junior → `chill touch`. Dois juniores juntos, num corredor, são bem piores que os wererats de mesmo nível. |
| **#7203 wererat ×10 (6)** | Individualmente fraco (73-93 HP), mas **dez cópias** e `AGGR_GOOD`+`AGGR_NEUTRAL`: quem é bom ou neutro é atacado. São o maior bloco de XP/vida do labirinto (`72.zon:18-31`). |
| **#7004 giant earth beetle (8)** | 100-118 HP com dano 4-10, **sem nenhuma flag de agressão** — só ataca se atacado. É o "mob comum gordo" do segundo nível. |

### 7.3 Qual nível é "bom" para limpar o esgoto?

A resposta sai dos números, não de opinião:

* A esmagadora maioria (**23 das 53 cópias**, níveis 1-5; mais 16 em 6-10) é **trivial para um
  personagem de nível ~8-10**. O primeiro nível do esgoto (zona 70) tem **só nível 1 e 5**.
* O bloco de **nível 11-15** (13 cópias, incluindo mudmonsters, gigantic rat, chr-eff'n,
  naga, basilisk, sea hag e master mindflayer) é o **degrau real** da área. Um personagem de
  nível 10 com equipamento fraco vai errar muito (AC 0 e 10) e apanhar 3-17 por golpe.
* **O único teto duro é o dragon (19)**. Ele está sozinho numa faixa própria.
* **Conclusão numérica:** o esgoto é uma área de **nível 5 a 15** que se limpa com folga a
  partir do **nível ~12-14**; para fazer a área inteira *incluindo* o dragon, o nível
  recomendado é **~15-19** (mesma faixa do próprio dragão), porque `consider` só compara nível
  e ele é nível 19. **Abaixo do nível 10**, o esgoto "raso" (zonas 70 e 71) ainda é fazível, mas
  o labirinto (72) e os túneis (73) não.
* **Ordem de dificuldade sugerida pelos dados:** zona 70 (níveis 1 e 5) → zona 71 (3-12) →
  zona 72 (6-14, com 10 wererats) → zona 73 (5-19, com os chefes).

---

## 8. O que é mundo padrão e pode **não** valer no DeBo

1. **Tudo neste documento é o mundo padrão em inglês.** Nomes como `the sewer rat`,
   `the ugly wererat`, `the scaled basilisk` e `the red dragon` são do `.mob` padrão; no DeBo
   eles estarão traduzidos (e podem ter sido renomeados ou removidos).
2. **Os vnums são do padrão.** `#7040`, `#7200`… só provam a estrutura do mundo padrão. O DeBo
   pode ter renumerado, acrescentado ou apagado zonas. Vnum padrão **não** é prova de existência
   no DeBo — a mesma ressalva já registrada em
   [00-afirmacoes-e-validacao.md](00-afirmacoes-e-validacao.md) e
   [05-mundo-padrao-vs-mapa.md](05-mundo-padrao-vs-mapa.md).
3. **A versão diverge.** Este mirror é rotulado **3.1** (commit `12a0cedb`, *"Initial commit of
   3.1."*), mas o DeBo se declara **CircleMUD 3.0**; os próprios textos do `lib/` misturam
   rótulos 3.0/3.1. A **ordem dos campos** do `.mob` e a fórmula de HP (`db.c:1820-1822`) são as
   mesmas em 3.0/3.1, mas detalhes finos podem diferir.
4. **Números de HP/dano podem ter sido retocados no DeBo.** As faixas de §4/§5 são
   *calculadas* (`dice`), não medidas em servidor. Basta o DeBo ter trocado um `1d8+172` para
   mudar tudo — e é exatamente o tipo de ajuste que MUDs traduzidos fazem.
5. **A contagem de "quantos nascem" é do reset padrão.** O DeBo tem o próprio `.zon`; o número
   de cópias (10 wererats, 7 mudmonsters, 4 bats) pode ser outro.
6. **Se o DeBo cortou o esgoto**, nada disso se aplica: o que temos do lado local é o mapa em
   `data/heroes/grebolius/mapa.json` (ver §8/§10 de
   [05-mundo-padrao-vs-mapa.md](05-mundo-padrao-vs-mapa.md)), que só levantou parte das salas.
7. **Correção de registro:** a linha #101 de
   [04-especiais-easter-eggs.md](04-especiais-easter-eggs.md) dá "nível 1"/"nível 2" a mobs do
   esgoto. Os níveis corretos, lidos do `.mob`, estão na afirmação #25 de §1 — **a linha do 04
   não foi alterada**, apenas anotada aqui (regra: não mexer em arquivo alheio).
