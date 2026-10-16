# Afirmações sobre o CircleMUD — o que é certo, o que é provável, o que é dúvida

Pesquisa feita sobre o **código-fonte do CircleMUD 3.x** (mirror [Yuffster/CircleMUD](https://github.com/Yuffster/CircleMUD), branch `master`, último push 2021-07-19) e sobre **o que já observamos no Devil's Bob MUD** (DeBo, `debomud.org:4000`, banner do servidor: *"Baseado no CircleMUD 3.0 criado por Jeremy Elson"*).

O DeBo é um derivado **traduzido, configurado e modificado**. Por isso uma afirmação sobre o engine **não** é uma afirmação sobre o DeBo. Este documento separa as duas coisas e diz, em cada linha, **como testar**.

## Como ler os níveis

| Nível | Significa | Vale como |
| --- | --- | --- |
| **Testado (código)** | O comportamento está no fonte do CircleMUD, com `arquivo:linha` citado. | Prova o **engine**, e só ele. O DeBo pode ter alterado. |
| **Testado (servidor)** | Resposta real do DeBo registrada numa transcrição/evidência nossa, com `arquivo:linha`. | Prova o **DeBo**. Não diz se o engine concorda. |
| **Testado (código + servidor)** | As duas coisas ao mesmo tempo: o fonte explica e o nosso registro confirma. | É o grau mais forte que este projeto consegue produzir sem sessão nova. |
| **Provável** | Decorre do código (ou do mundo padrão), mas depende de configuração, versão, tradução ou do mundo do DeBo não ter mudado aquilo. | Hipótese de trabalho **forte**. Não escrever crônica em cima. |
| **Dúvida** | Fontes divergem, ou o dado depende de algo que não temos (ex.: `.zon`/`.obj` do DeBo, flags de sala do servidor), ou é palpite. | Pergunta a resolver em sessão autorizada. |

Regra da casa: **Provável não vira Testado sozinho**. Só uma resposta real do servidor, registrada, promove uma linha.

## Onde estão as afirmações

| Arquivo | Tema |
| --- | --- |
| [01-comandos.md](01-comandos.md) | Comandos, posições, abreviações, toggles, prompt, socials |
| [02-navegacao.md](02-navegacao.md) | Movimento, custo por setor, portas, `look`/`exits`, paginação, fuga |
| [03-magias.md](03-magias.md) | Magias: dano, mana, alvos, duração, resistência, `recall` |
| [04-especiais-easter-eggs.md](04-especiais-easter-eggs.md) | NPCs com rotina própria, banco, murais, xadrez, esgotos, segredos |
| [05-mundo-padrao-vs-mapa.md](05-mundo-padrao-vs-mapa.md) | Mundo padrão (Midgaard, tabuleiro, esgotos, novatos) contra o nosso `mapa.json` |
| [06-evidencias-debo.md](06-evidencias-debo.md) | O que já foi observado no DeBo, com transcrição e arquivo:linha |

## Protocolo de validação (uma sessão autorizada resolve quase tudo)

Cada teste abaixo é barato, cabe no teto de 3 conexões por dia e produz **evidência registrável**. Nada aqui autoriza jogar por si só: vale a autorização vigente do ciclo diário.

### Bloco A — apresentação e paginação (5 minutos)

1. `term` (sem argumento) — o servidor mostra o tamanho atual? Registrar a resposta literal.
2. `term 60 200` — o servidor aceita? Qual a resposta? Isso reduz paginação.
3. Procurar uma resposta longa (`help`, `list` de loja cheia, `score tudo`) e registrar **o texto exato da linha de paginação** e quantas páginas.
4. Depois de `term 60 200`, repetir o mesmo comando e comparar o número de páginas.
5. `prompt` e `prompt <formato>` — descobrir se o servidor aceita prompt customizado e quais tokens.

### Bloco B — comandos e visão da sala (10 minutos)

6. Numa sala com porta fechada/trancada: `open`, `unlock`, `enter`, `look <direção>` — registrar cada recusa literal.
7. `exits` numa sala conhecida de 4+ saídas, e comparar com a linha de saídas do `look`.
8. Gastar movimento até faltar: registrar a mensagem de exaustão e o custo por passo observado.
9. `consider` contra dois monstros de níveis bem diferentes: registrar a escala de mensagens.

### Bloco C — magias (15 minutos, o bloco mais valioso)

10. `lightning bolt` contra um tipo de monstro, 10 vezes: registrar cada dano. Comparar a faixa com a fórmula do [03-magias.md](03-magias.md).
11. O mesmo para `burning hands` e `magic missile` — três séries de dano viram a prova.
12. Registrar o custo de mana de cada conjuração (diferença de `score` antes/depois).
13. ~~`armor` no Templo e confirmar "área sem magia"~~ **já resolvido**: é `NO_MAGIC` na sala (Testado). Falta generalizar: `cast 'armor'` **dentro de uma loja**.
14. ~~`invisibility` + `list`~~ **já resolvido**: o engine checa via `CAN_SEE` (`shop.c:119`). Falta ver se `b`/`r` existem no pager traduzido.
15. Cronometrar a duração de `armor`/`invisibility` pelo relógio do jogo (`time`), não pelo relógio real.

### Bloco D — morte e retorno (só se acontecer)

16. Se houver morte: registrar o que o servidor disse, o que foi perdido, onde ficou o corpo.
17. `recall` a partir de uma sala comum: registrar destino e custo.

### Bloco E — mundo (comparação com o mundo padrão)

18. Percorrer 10 salas de Midgaard e confrontar nome/saídas com a tabela do [05-mundo-padrao-vs-mapa.md](05-mundo-padrao-vs-mapa.md).
19. No tabuleiro de xadrez (zona 36 do mundo padrão): contar as casas e as peças.
20. Nos esgotos (zonas 70-73): contar salas e conferir as ligações conhecidas.

## O que este documento **não** é

- Não é transcrição de sessão nem prova de que algo aconteceu com a personagem. Fatos de campanha continuam vindo de `events.json` e das evidências do dia.
- Não transfere conhecimento para a Grebolius: ela não sabe nada disto, e a **Regra de Ouro dos Números** continua valendo.
- Não substitui `maquina/`, que é onde vive o que o servidor **documenta** e o que já foi **verificado** (`maquina/verificacoes.md`).

## Snapshot e método desta consolidação

- **Engine:** `Yuffster/CircleMUD`, commit único `12a0ced…` cuja mensagem é *"Initial commit of 3.1"* (2012-03-22). As linhas citadas valem para o **3.1**; o DeBo se declara **3.0** (banner: *"Baseado no CircleMUD 3.0 criado por Jeremy Elson"*). Onde 3.0/3.1 diferem, o nível cai para Dúvida.
- **Servidor:** as citações marcadas **✓** foram reconferidas por mim nesta sessão, lendo o arquivo na linha indicada. As demais vêm da mineração de [06-evidencias-debo.md](06-evidencias-debo.md).
- **`mapa.json` é um alvo móvel:** ele foi reescrito **às 15:32:46 de hoje** por uma sessão que está **rodando agora** (o driver escuta em `127.0.0.1:14888`). No snapshot que usei: `total_rooms: 360`, `last_updated_day: 156`. Qualquer contagem de salas neste documento é uma foto, não um fato estável.
- **Contagens de mundo padrão verificadas por mim** (dois marcadores independentes — blocos `#` e terminadores `S` — concordam): zona 30 = **59**, zona 31 = **54**, tabuleiro = **67**, esgotos = 62+26+87 = **175**, novatos = **41**, Three of Swords = **76**.

## A. Apresentação, paginação e cliente

| # | Afirmação | Nível | Fonte | Como validar no DeBo |
| --- | --- | --- | --- | --- |
| A1 | O engine pagina com **22 linhas × 80 colunas** e o pager **captura todo o input antes do interpretador** — durante a paginação nenhum comando funciona | Testado (código) | `src/comm.h:40-41`, `src/modify.c:341-361`, `src/comm.c:740-745` | Provocar `help` longo e tentar mandar um comando no meio da paginação; ver se ele é engolido |
| A2 | O DeBo paginou com o texto `[ Aperte ENTER para continuar, S para sair ou número da página ( 1 de N ) ]`, colado ao prompt sem quebra de linha | Testado (servidor) | `9eb61a.jsonl:116` (1 de 3), `dia91.json:285` (1 de 5) | Repetir `help` e `list` de loja cheia; registrar quantas páginas |
| A3 | O prompt de paginação do engine é em inglês e oferece ENTER/q/r/b/número; **o DeBo traduziu e trocou por "S"** | Testado (código + servidor) | `src/comm.c:994-997` + A2 | Testar `b` e `r` no DeBo: se não funcionarem, a adaptação é só ENTER/S/número |
| A4 | **`term` não existe no engine** (nem `pagelength`, `pagelen`, `pagesize`, `columns`, `rows`); é acréscimo do DeBo | Testado (código) / Testado (servidor) | busca exaustiva em `src/`; `consulta_2026-10-15.json:411,415` ✓ | `term` sem argumento; `term 60 200`; ver se aceita |
| A5 | O único comando de cliente do engine é `prompt`, e ele aceita **só** `H,M,V,all,on,none,off,auto` — `prompt %h` cai no uso | Testado (código) | `src/act.other.c:730,741` | `prompt %h` e `prompt H` |
| A6 | `prompt auto` liga `PRF_DISPAUTO`, mas a flag não é lida em nenhum outro ponto do código — **vestígio sem efeito** | Testado (código) | `src/structs.h:216` + 3 ocorrências totais | `prompt auto` e olhar se o prompt muda abaixo de 30% |
| A7 | O DeBo **não negocia IAC GA/EOR**; o engine só manda WILL/WONT ECHO — logo detectar prompt por texto é a única via | Testado (código) | `src/comm.c` (handshake), busca por `GA`/`EOR` | Despejar bytes crus numa conexão de teste e procurar `0xFF 0xF9` |
| A8 | Hoje jogamos com o terminal em **22×80** — exatamente a configuração que mais pagina | Testado (servidor) | `consulta_2026-10-15.json:411` ✓ | `term 60 200` e comparar o número de páginas do mesmo `help` |

## B. Comandos

| # | Afirmação | Nível | Fonte | Como validar no DeBo |
| --- | --- | --- | --- | --- |
| B1 | Comando casa por **prefixo** (`strncmp`), **primeira entrada da tabela vence**, sem aviso de ambiguidade: `l`=look, `k`=kill, `s`=say | Testado (código) | `src/interpreter.c:600-602` | `l`, `k`, `s` e `sco` no DeBo (a ordem da tabela pode ter mudado na tradução) |
| B2 | `qui` **não sai do jogo**: a entrada existe só para responder *"You have to type quit--no less, to quit!"* | Testado (código) | `src/interpreter.c:407`, `src/act.other.c:75` | Digitar `qui` e `quitt` |
| B3 | Comando inexistente e nível insuficiente devolvem a **mesma** resposta ("Huh?!?") — mortal não recebe "você não pode" | Testado (código) | `src/interpreter.c:606` | Comando inventado vs comando de imortal |
| B4 | **Qualquer** comando cancela o efeito de esconder-se (`AFF_HIDE`) | Testado (código) | `src/interpreter.c:580` | `hide` e depois `score`: se aparecer, o engine está mantido |
| B5 | `hop` está na tabela de comandos mas **não tem social** correspondente → "That action is not supported." | Testado (código) | `src/interpreter.c:325`, `src/act.social.c:93`; `lib/misc/socials` sem `^hop` | Digitar `hop` |
| B6 | São **104 socials**, com 8 mensagens cada; `#` na 3ª linha marca social que **não aceita alvo** (ex.: `applaud`) | Testado (código) | `src/act.social.c:36-56,259-260`, `lib/misc/socials` | `socials` e contar; `applaud <alguém>` |
| B7 | `snowball` é social de **imortal**; `insult` é comando separado, com frases aleatórias | Testado (código) | `src/interpreter.c:460`, `src/act.social.c:126` | Digitar `snowball` e `insult` |
| B8 | `shout` só alcança a **mesma zona** e quem está acordado; `gossip`/`auction`/`grats` funcionam **dormindo** | Testado (código) | `src/act.comm.c:366-484`, `src/interpreter.c:303` | `shout` de uma sala periférica; `gossip` dormindo |
| B9 | `holler` custa **20 de movimento** | Testado (código) | `src/config.c:63` | Medir mv antes/depois |
| B10 | `save` salva também os **aliases**, e o engine **não tem limite** de aliases | Testado (código) | `src/act.other.c:120,124`, `src/db.h:26,37` | Criar alias, `save`, reconectar |
| B11 | `'texto` = say e `:emo` = emote | Testado (código) | `src/interpreter.c:275,429` | Testar os dois atalhos |
| B12 | O canal `norepeat` troca o eco da fala por `OK` | Testado (código) | `src/act.comm.c` | Ligar e falar |

## C. Movimento e navegação

| # | Afirmação | Nível | Fonte | Como validar no DeBo |
| --- | --- | --- | --- | --- |
| C1 | São **6 direções** (n/e/s/w/u/d); `enter`/`leave` são comandos separados, não direções | Testado (código) | `src/act.movement.c:480-531` | `enter` num portal e numa porta comum |
| C2 | O custo do passo é a **média inteira dos setores** de origem e destino; esgotado → *"You are too exhausted."* | Testado (código) | `src/constants.c:731-743`, `src/act.movement.c:120-131` | Medir mv em 5 passos de estrada e 5 de floresta; comparar |
| C3 | **O movimento é bloqueado em SILÊNCIO durante o combate** — só `flee` anda | Testado (código) | `src/act.movement.c:188-189` | Em combate, mandar `norte` e observar se **não vem mensagem nenhuma** |
| C4 | Só `SECT_WATER_NOSWIM` barra passagem; `SECT_FLYING` e `SECT_UNDERWATER` **nunca são checados** no código | Testado (código) | `src/act.movement.c` (checagens de setor) | Entrar em água funda sem barco; tentar voar/submergir |
| C5 | Ordem do `look`: nome → descrição → linha de saídas → objetos → mobs; `BRIEF` só suprime a descrição **ao andar** | Testado (código) | `src/act.informative.c:352-369` | `brief`, andar, depois `look` — a descrição deve voltar |
| C6 | `exits` mostra o **nome** da sala de destino, e **mortal nunca vê vnum** de sala | Testado (código) | `src/act.informative.c:372-401` | `exits` em qualquer sala |
| C7 | O DeBo imprime `Saídas:` com `Norte - <sala>` alinhado e marca porta fechada com `!` | Testado (servidor) | `1a4abb.jsonl:13`, `dia92.json:976` | `exits` numa sala com porta fechada |
| C8 | `consider` compara **só nível** e **não imprime nada** se a diferença passar de 100 | Testado (código) | `src/act.informative.c:1494-1496` | `consider` num monstro muito abaixo do nível |
| C9 | `flee` não tem teste de chance: sorteia até 6 direções; não foge para sala de morte nem por porta fechada | Testado (código) | `src/act.movement.c` (do_flee) | Fugir em beco sem saída e numa sala com porta fechada |
| C10 | `wimpy` dispara **dentro** do cálculo de dano, com teto de **metade dos HP** | Testado (código) | `src/fight.c:796-801`, `src/act.other.c:715-716` | `wimpy 999` — deve ser recusado/limitado |
| C11 | O DeBo responde `wimpy` com *"Certo, você irá se acovardar se você ficar abaixo de NN pontos de vida."* | Testado (servidor) | 06, seção comandos | `wimpy 13` |
| C12 | **Fugir custa XP** no DeBo (*"Você perdeu 1 ponto de experiência na sua fuga."*) — **isso não existe no engine** | Testado (servidor) / Dúvida na fórmula | `dia95.json:317`; engine sem penalidade em `fight.c`/`act.movement.c` | Fugir 3× e medir a XP perdida |
| C13 | `recall` não é comando: é a magia `word of recall`, que leva ao `mortal_start_room` (Templo por padrão) | Testado (código) | `src/spell_parser.c:956` | Digitar `recall` (deve falhar como comando) e `cast 'word of recall'` |
| C14 | A regra do DeBo *"retornar gratuitamente até o nível 70"* **não é do engine** | Testado (servidor) / Provável modificação | resposta citada em 06 | `cast 'word of recall'` acima do nível 70 |
| C15 | Templo de Midgaard tem `d → 3005` **igual ao `s`** no mundo padrão | Testado (código) | `lib/world/wld/30.wld`, sala `3001` | `d` e `s` no Templo: as duas levam à Praça |

## D. Magias

| # | Afirmação | Nível | Fonte | Como validar no DeBo |
| --- | --- | --- | --- | --- |
| D1 | **Dano de magia não escala com nível** (só `earthquake` = 2d8+nível): MM 1d8+1, burning hands 3d8+3, shocking grasp 5d8+5, **lightning bolt 7d8+7 (8–63)**, fireball 11d8+11 (22–99) | Testado (código) | `src/spells.c`, `src/magic.c` | 10 conjurações contra o mesmo tipo de monstro, anotando cada dano |
| D2 | Teto absoluto de **100 de dano por golpe** | Testado (código) | `src/fight.c:737` | Só verificável com alvo de vida alta |
| D3 | O teste de resistência corta o dano **pela metade** | Testado (código) | `src/magic.c` (mag_damage) | Comparar a distribuição: deve haver dois agrupamentos (cheio e metade) |
| D4 | **AC não reduz dano**: entra só na chance de acerto (`victim_ac = AC/10`, acerta se `thaco − d20 <= victim_ac`) | Testado (código) | `src/fight.c` | Anotar dano recebido com e sem `armor` — a média deve ficar parecida |
| D5 | `armor` = `APPLY_AC −20`, dura **24 h de jogo**; recaste **não soma** o valor, só a duração | Testado (código) | `src/spells.c`, `src/magic.c` | Conjurar `armor` 3× e ler `score` — AC não deve cair 60 |
| D6 | Duração em **horas de jogo** (1 hora = ~75 s reais): sanctuary 4 h, bless 6 h, invisibility 12+nível/4, poison = nível do conjurador | Testado (código) | `src/spells.c`, `src/magic.c` | Cronometrar `armor`/`invisibility` com `time` do jogo |
| D7 | Save = `MAX(1,save) < rand(0,99)`; para mago/`SAVING_SPELL`: 60 no nível 1, 44 no 10, 26 no 20, 8 no 30 | Testado (código) | `src/magic.c` | Estatística de resistência contra alvo de nível conhecido |
| D8 | **`sanctuary` não altera o save** | Testado (código) | `src/magic.c` | Conjurar ofensiva em alvo com e sem sanctuary |
| D9 | **Regra de posição:** `POS_FIGHTING`(7) < `POS_STANDING`(8) → `sanctuary`, `invisibility`, `bless`, `strength`, `sleep`, `poison`, `curse` **não podem ser lançadas em combate**; `armor`, MM, LB, fireball e word of recall podem | Testado (código) | `src/spell_parser.c` (min_position da tabela) | Em combate, tentar `cast 'sanctuary'` e `cast 'armor'` |
| D10 | Lag de **2 s** (PULSE_VIOLENCE) após conjurar, em sucesso e em falha; **falha custa metade da mana** | Testado (código) | `src/spell_parser.c` | Medir mana antes/depois de uma falha de concentração |
| D11 | Mana = `MAX(mana_max − mana_change×(nível − min_level), mana_min)`; **não há tabela por classe** | Testado (código) | `src/spell_parser.c`, `src/class.c` | Comparar custo de `magic missile` em dois níveis |
| D12 | Níveis mínimos do mago: MM 1, invisibility/armor 4, burning hands 5, strength 6, shocking grasp 7, sleep 8, **lightning bolt 9**, color spray 11, energy drain 13, curse/poison 14, fireball 15 | Testado (código) | `src/spell_parser.c` | Conferir contra `practice`/`spells` da personagem |
| D13 | `sanctuary`, `heal` e `word of recall` são **de clérigo** no 3.1 stock; se a maga as tem, é modificação do DeBo | Testado (código) / Provável | `src/spell_parser.c` | Ver de onde vem o `sanctuary` (item vs conjuração) |
| D14 | **`identify` não é conjurável** (`#201` > `MAX_SPELLS 130`, `min_level = LVL_IMMORT`): só por pergaminho/varinha/cajado | Testado (código) | `src/spell_parser.c`, `src/spells.h` | `cast 'identify'` deve falhar; usar o pergaminho |
| D15 | `identify` revela tipo, bits, peso/valor/aluguel, `Damage Dice XdY` (arma), `AC-apply N` (armadura), cargas e `Affects: X By N` | Testado (código) | `src/spells.c` (spell_identify) | Identificar um item conhecido |
| D16 | `invisibility` = −40 AC + `AFF_INVISIBLE`, 12+nível/4 h; é derrotada por `detect invisibility`; **acaba no primeiro dano causado** | Testado (código) | `src/spells.c`, `src/magic.c` | Atacar invisível: deve aparecer; e um terceiro com detect invis deve vê-la |
| D17 | Buracos do engine: `ventriloquate`, `group recall` e `control weather` não fazem nada; `protection from evil` não altera dano | Testado (código) | `src/spell_parser.c` (sem `spello()`), `src/magic.c` | Conjurar cada um e observar |

## E. Lojas, banco e morte

| # | Afirmação | Nível | Fonte | Como validar no DeBo |
| --- | --- | --- | --- | --- |
| E1 | **O engine recusa comércio com quem o lojista não vê**: `shop.c:119` usa `CAN_SEE`, e a string stock é *"I don't trade with someone I can't see!"* | Testado (código) | `src/shop.c:119`, `src/shop.h` (`MSG_NO_SEE_CHAR`) | `invisibility` + `list` |
| E2 | No DeBo isso sai como *"O balconista do bar exclama: 'Não negocio com quem não vejo!'"*, e `visible` restaura a loja | Testado (código + servidor) | `123921_2cb7a0.jsonl:5290` ✓ (e `:5292`) | `invisibility`, `list`, `visible`, `list` |
| E3 | O banco é um **objeto** (ATM 3034 / cashcard 3036); `balance`/`deposit`/`withdraw` são `do_not_here` — só funcionam **perto do objeto** — e **não há juros** | Testado (código) | `src/obj…`/`spec_procs.c` (ATM), `lib/world/zon/30.zon` | `balance` longe do Templo (deve recusar) e perto |
| E4 | O DeBo aceita `deposit`/`balance` com respostas *"Você deposita 232 moedas."* / *"Você possui 7.032 moedas no banco."* | Testado (servidor) | 06, seção lojas | `deposit 1` no Templo e `balance` |
| E5 | O dinheiro do lojista é **finito**, com conta bancária entre 5.000 e 15.000 | Testado (código) | `src/shop.h:134-135`, `src/shop.c:627-629,808-811` | Vender itens caros até o lojista recusar por falta de caixa |
| E6 | Lojista **tapa** quem tenta `steal` | Testado (código) | `src/shop.c:966-973` | `steal` numa loja (com risco — e a diretiva de não roubar continua valendo) |
| E7 | As margens de preço vêm do `.shp` de cada loja e são ajustadas pelo **CARISMA** em ~±21% | Testado (código) | `src/shop.c:474-514` | `buy`/`sell` com e sem itens de carisma |
| E8 | Morte: perde-se **metade do XP total** e **não se perde nível** | Testado (código) | `src/fight.c:380`, `src/limits.c:265-292` | Só na próxima morte; anotar XP antes e depois |
| E9 | No DeBo a morte imprimiu *"Você perdeu 1.435 pontos de experiência pela sua morte."* seguido de *"\*Você falhou em suas aventuras!\*"* e o Menu Principal | Testado (servidor) | `transcript_dia100_20261016_000913_acc661.jsonl:126` ✓ | Comparar com o XP total registrado antes da morte |
| E10 | A mesma frase *"Você falhou em suas aventuras!"* também aparece no `quit` — serve aos **dois** gatilhos | Testado (servidor) | `dia156.json:31` | `quit` e comparar |
| E11 | Inventário, equipamento e **ouro** vão para o cadáver; o corpo dura 5 ticks (NPC) / 10 (jogador) | Testado (código) | `src/fight.c:304-328`, `src/config.c:76-77` | Morrer e cronometrar o apodrecimento |
| E12 | No Templo do mundo padrão **não nasce mob nenhum** — só um ATM (3034); a Fonte (3035) é na Praça 3005 | Testado (código) | `lib/world/zon/30.zon` | `look` no Templo após um reset |

## F. Mundo padrão vs nosso mapa

| # | Afirmação | Nível | Fonte | Como validar no DeBo |
| --- | --- | --- | --- | --- |
| F1 | Zona 30 = **59 salas** e zona 31 = **54** (não 65/62) | Testado (código) | contagem própria em `30.wld`/`31.wld` (blocos e `S` coincidem) | — |
| F2 | Tabuleiro = **67** salas (entrada + 64 casas + 2 tesourarias); esgotos = **175**; novatos = **41**; Three of Swords = **76** | Testado (código) | contagem própria; `36.zon:86-97` | Contar as casas andando no DeBo (hoje temos 6) |
| F3 | `32.wld`/`32.zon` **não existem**; as salas de rio estão em `31.wld`; a zona 73 está dentro de `72.wld` | Testado (código) | árvore do repo + contagem própria | — |
| F4 | Topologia idêntica ao padrão nas ruas (3012-3016), altar (3054), templo (n/e/s/w), Praças, guildas dos magos/ladrões, Grubby Inn, ponte, junção dos esgotos (5/5) e ~20 salas dos novatos | Provável | 05, comparação direção-a-direção | Percorrer e conferir as saídas uma a uma |
| F5 | O `d` do Templo local duplicar o `s` **não é erro de dado**: o mundo padrão faz igual | Testado (código) | `30.wld` sala 3001 → `d → 3005` = `s` | — |
| F6 | A única saída local sem par no padrão é `u` do Templo → `panteao_centenarios` (conteúdo local) | Provável | 05 + `30.wld` | `u` no Templo |
| F7 | **NO_MAGIC** está em 17 salas da zona 30 — incluindo **todas as lojas** (Padaria, Armazém, Armaria, Loja de Armas, Loja de Magia, Loja de Animais, *Water Shoppe*, Grubby Inn) e o **Templo**; a **Praça do Templo (3005) não tem** | Testado (código) | `lib/world/wld/30.wld` (flags `h`), `src/constants.c:40-54` (índice 7) | Conjurar dentro de uma loja e na Praça |
| F8 | Templo = `NO_MAGIC + PEACEFUL + NO_MOB + INDOORS`; `PEACEFUL` só em 3000, 3001, 3062 (correio) e 3063 (doação) | Testado (código) | `30.wld` (flags `cdeh`/`e`) | Tentar `kill` no Templo |
| F9 | No DeBo, conjurar **no Templo** devolve *"Sua magia falha e desaparece."* e um passo abaixo, na Praça, funciona | Testado (código + servidor) | `30.wld` F7/F8 + `123921_2cb7a0.jsonl:96` ✓ (`armor` e `invisibility`) | `cast 'armor'` no Templo e na Praça |
| F10 | Ausências no nosso mapa (frente à zona 31): Prefeitura, Cemitério/Capela, Parque, *Emerald Avenue*, *Road Crossing*, Concourse | Dúvida | 05 | Sondar as direções do cruzamento sul da cidade |
| F11 | O Prefeito carrega a **Chave da Cidade** (obj 3112) na sala 3138 — sala que não temos mapeada | Provável | `30.wld`/`31.wld`, 05 | Encontrar o Prefeito; o DeBo **tem** um Prefeito (visto no log do cartógrafo) |

## G. Easter eggs e subsistemas (a fila divertida)

| # | Afirmação | Nível | Fonte | Como validar no DeBo |
| --- | --- | --- | --- | --- |
| G1 | O **prefeito** (mob 3105) tem rota horária às **6h e 20h** do jogo e 6 falas fixas | Testado (código) | `src/spec_procs.c:237-303` | Esperar a hora (75 s/hora) e seguir o Prefeito |
| G2 | O **guarda da cidade** cospe em quem tem **CARISMA < 6** | Testado (código) | `src/spec_procs.c:620-625` | Precisa de personagem de carisma baixo |
| G3 | A **recepcionista** executa social aleatório, incluindo `fart` | Testado (código) | `src/objsave.c:1066-1072` | Ficar na recepção |
| G4 | O **Rei Welmar** faz monólogo **em latim às 12h** do jogo | Testado (código) | `src/castle.c:448-453,472` | Zona 150 (Castelo do Rei Welmar) ao meio-dia |
| G5 | **Fido** devora cadáveres e solta o conteúdo no chão | Testado (código) | `src/spec_procs.c:527-549` | Largar um corpo e observar |
| G6 | No mundo padrão **não existe "sino" nem comando `castle`** de clã/guilda; `castle.c` é só comportamento de NPC do reino | Testado (código) | busca em `src/` e `interpreter.c` | Se o DeBo tiver sino/clã, é **acréscimo local** — segredo do DeBo |
| G7 | As tesourarias do tabuleiro (3665/3666) são abertas pelas **chaves dos dois reis** | Testado (código) | `lib/world/zon/36.zon:86-97` | Matar/roubar o rei certo — mas a diretiva de não roubar vale |

## H. Conflitos resolvidos nesta consolidação

1. **Invisibilidade × comércio.** O relatório 03 concluiu que o engine **não** checa invisibilidade na loja; o 06 tinha a resposta real dizendo que bloqueia. **Resolvido a favor do servidor:** a checagem existe, mas por macro — `shop.c:119` (`CAN_SEE`), com a string stock em `shop.h`. O 03 procurou `AFF_INVISIBLE` literal e não achou. → **Testado (código + servidor)**, e o `00` original (que tratava como hipótese) fica corrigido.
2. **Contagem de salas do mundo padrão.** O 05 reportou 65/62 (aritmética de faixa de vnum); o 04 reportou 59/54 (blocos). **Resolvido por medição própria:** 59 e 54, com blocos `#` e terminadores `S` coincidindo. As salas "faltantes" da faixa (3034-3039, 3056-3057, 3142-3199) são vnums de **objeto/mob** ou simplesmente não existem em `.wld`.
3. **`total_rooms`.** O 05 leu 359; eu li 361 no início desta sessão e 360 agora. Não é erro de ninguém: **o arquivo está sendo reescrito ao vivo** (sessão ativa, driver escutando em `127.0.0.1:14888`). Toda contagem precisa de carimbo de hora.

## I. Correções que devemos fazer nos nossos próprios documentos

| Onde | Diz | A evidência indica |
| --- | --- | --- |
| `conhecimento.md:569`, `ficha.md:110` | `armor`/`invisibility` custam "~25 de mana" | **15** de mana para `armor` (260→245; 239→224; 200→185) |
| `maquina/tips.md:5` | Dias 90–91 não tinham linhas `DICA:` | Os dias 91, 92 e 93 têm muitas |
| `automato/README.md:160`, `diretiva_de_jogo.md:67,88,110` | *"Nah... você está muito relaxado.."* | **Nenhuma transcrição** registra essa string — é prosa, não evidência |
| `00-afirmacoes-e-validacao.md` (Bloco C, item 13) | "confirmar a hipótese de área sem magia" | Já é **Testado (código + servidor)**; e vale para **toda loja**, não só o Templo |
| Decisões de rota | Portas recusadas saem da fronteira | Continua válido — o engine **não responde nada** ao tentar andar em combate (C3), o que pode estar gerando "porta recusada" onde era só combate |

## J. As 12 perguntas de maior valor para a próxima sessão

1. `term` sem argumento, e depois `term 60 200` — quantas páginas caem no mesmo `help`?
2. `prompt` aceita outra coisa além de H/M/V/all/auto/none? (`prompt %h` falha?)
3. `cast 'armor'` **dentro de uma loja** falha como no Templo? (generaliza o NO_MAGIC?)
4. Dez danos de `lightning bolt` no mesmo tipo de monstro: a faixa fica dentro de 8–63 ou passa (como os 80 já registrados)?
5. `armor` conjurado 3× muda a AC mais de uma vez?
6. Em combate, `norte` devolve **silêncio** ou uma recusa?
7. `qui` responde "tem que digitar quit inteiro"?
8. `hop` dá "ação não suportada"?
9. `consider` em monstro muito abaixo do nível: **fica mudo**?
10. `balance` longe do Templo recusa? Perto, soma sem juros?
11. Fugir 3×: quanto de XP se perde, e a perda é fixa (1) ou proporcional?
12. Quantas casas tem o tabuleiro **no DeBo** (o padrão tem 64 + entrada + 2 tesourarias)?

## K. O que é do DeBo e não do CircleMUD (verificado por ausência)

Método: varredura da **distribuição padrão inteira** (`src/` + `lib/`, incluindo os arquivos de ajuda) e leitura da tabela real de comandos, `command_info[]` em `src/interpreter.c`.

| Comando | Existe na distribuição padrão? | Evidência no DeBo | Consequência |
| --- | --- | --- | --- |
| **`autoquest`** | **Não.** Zero ocorrências em `src/`, `lib/`, ajuda — e zero para `autogold` também | `autoquest todas` → **"Autoquests do DeBo MUD"** (`transcript_dia101_…cd4a79.jsonl:88`, `dia104…:183`, `dia111…:301`, `dia141…:36`); `score` → `[Autoquests em andamento]` (`evidence/dia91.json:235`) | Sistema **local**: nada no engine explica regras, Pontos de Aventura, limites ou o "morrer falha as autoquests". Só a resposta do servidor é fonte. |
| `autogold` | Não (zero ocorrências) | Citado no `commands` do DeBo (`transcript_dia156_…2cb7a0.jsonl:5958`) | Local. |
| `tips` | Não | `tips` → *"Você verá as dicas do jogo."* (`maquina/verificacoes.md:13`) | Local. |
| `term` | Não (nem `pagelength`/`pagesize`) | `term 22 80` → *"Muito bem, agora seu terminal está configurado…"* (`consulta_2026-10-15.json:411`) | Local — e é a alavanca para reduzir a paginação. |
| `identify` (como comando) | Não na tabela de comandos (é **magia**, `cast 'identify'`) | Ajuda do DeBo documenta `IDENTIFICAR` com limite de nível 80 | Local como comando; a magia é do engine. |
| `recall` | Não na tabela de comandos (é `word of recall`, magia) | `cast 'word of recall'` funciona e diz "grátis até o nível 70" | Comando local/atalho; a regra do nível 70 é local. |
| `scan` | Não | Ajuda do DeBo exige ladrão nível 17 | Local. |
| `autoexit`, `prompt`, `balance`, `deposit`, `withdraw`, `practice`, `hide`, `auction`, `grats`, `visible`, `wimpy`, `consider` | **Sim**, estão em `command_info[]` | — | São do engine: aqui a pesquisa de fonte vale. |

**O que o CircleMUD chama de "quest" é outra coisa:** uma flag de jogador (`PRF_QUEST`, `src/structs.h:204`), um **toggle** `quest` (`src/interpreter.c:407` → `do_gen_tog`) que só responde *"Okay, you are part of the Quest!"* / *"You are no longer part of the Quest."* (`src/act.other.c:872-873`), um **canal** (`quest-say`, `src/act.comm.c:503-509`) e um filtro no `who` (`-quest`, "On Quest:"). **Não há objetivo, recompensa, catálogo nem NPC doador** — isso é invenção do DeBo.

Sinal indireto que confirma: no DeBo **`help autoquest` responde e `ajuda autoquest` é recusado** — a entrada de ajuda foi escrita no conjunto em inglês e não no traduzido, típico de acréscimo local.


