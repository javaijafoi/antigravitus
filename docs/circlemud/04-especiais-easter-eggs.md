# 04 — Comportamentos especiais de NPCs, subsistemas e easter eggs do CircleMUD

Catálogo do **engine** (special procedures, banco, correio, murais, casa/aluguel, morte, lojas) e do **mundo padrão** (Zona dos Novatos, tabuleiro de xadrez, esgotos, Midgaard), com `arquivo:linha` em toda afirmação, para validação posterior numa sessão autorizada no Devil's Bob MUD (DeBo, `debomud.org:4000`, PT-BR, declaradamente baseado em **CircleMUD 3.0**).

Este arquivo é o **04** da série descrita em [00-afirmacoes-e-validacao.md](00-afirmacoes-e-validacao.md). Ele cobre comportamento/segredos; a topologia de salas do mundo padrão contra o nosso `mapa.json` está em [05-mundo-padrao-vs-mapa.md](05-mundo-padrao-vs-mapa.md) e não é repetida aqui.

## Fonte consultada

| O quê | Onde |
| --- | --- |
| Repositório | [github.com/Yuffster/CircleMUD](https://github.com/Yuffster/CircleMUD), branch `master` |
| URL crua base | `https://raw.githubusercontent.com/Yuffster/CircleMUD/master/<caminho>` |
| Commit exato usado | `12a0cedbb563465029c46de9537c96854bc11610` — committer date **2012-03-22**, mensagem `Initial commit of 3.1` (consultado via `api.github.com/repos/Yuffster/CircleMUD/commits/master` em 2026-10-16) |
| Como os arquivos foram obtidos | tarball completo `https://codeload.github.com/Yuffster/CircleMUD/tar.gz/refs/heads/master` (1.382.751 bytes), extraído localmente; **todos os números de linha deste documento saem de `grep -n`/leitura paginada desses arquivos reais**, não de um `web_fetch` sem numeração |
| Arquivos do mundo padrão | `lib/world/wld/*.wld`, `lib/world/zon/*.zon`, `lib/world/obj/*.obj`, `lib/world/shp/*.shp`, `lib/world/mob/*.mob` |

**Truncamento:** nenhum. A ausência de truncamento foi verificada de dois modos: (a) cada arquivo baixado termina no seu marcador real (`}` final de `src/spec_procs.c` na linha 755; `$` final nos `.zon`; `$~` final nos `.shp`); (b) o `web_fetch` inicial de `src/spec_procs.c`, feito antes do tarball, produziu exatamente o mesmo conteúdo do arquivo do tarball (755 linhas).

**Aviso de versão (importante).** O DeBo se declara **3.0**, mas a árvore deste mirror está rotulada como **3.1** no commit (`Initial commit of 3.1`) e mistura rótulos dentro de `lib/`: `lib/text/motd:5` diz `C I R C L E M U D 3 . 0` e `lib/text/credits:3` diz `C I R C L E M U D 3 . 0`, enquanto `lib/text/greetings:4` diz `Based on CircleMUD 3.1` e `lib/text/imotd:3` diz `CircleMUD 3.1`. Consequência prática: **a estrutura dos subsistemas é a mesma, mas detalhes finos de 3.1 podem não existir no DeBo** (exemplos de código claramente 3.1: extração adiada com `PLR_NOTDEADYET` em `handler.c:961-969` e `fight.c:681`; `aggressive_mob_on_a_leash` em `mobact.c:253`).

**Estrutura de arquivos diferente do que se costuma supor.** Neste mirror **não existem** `spec_procs2.c`, `spec_procs3.c` nem `spec_procs4.c` (verificado por listagem do diretório `src/`). Cada família de procedures mora em outro arquivo, e isso muda onde procurar as coisas:

| Procedure | Arquivo real nesta árvore |
| --- | --- |
| `guild`, `dump`, `mayor`, `snake`, `thief`, `magic_user`, `guild_guard`, `puff`, `fido`, `janitor`, `cityguard`, `pet_shops`, `bank` | `src/spec_procs.c:39-52` (declarações) e `src/spec_procs.c:154-754` |
| `postmaster` | **`src/mail.c:500`** (não em `spec_procs*.c`) |
| `gen_board` | `src/boards.c:154` |
| `shop_keeper` | `src/shop.c:939` |
| `receptionist`, `cryogenicist` | `src/objsave.c:1142` e `src/objsave.c:1148` |
| `CastleGuard`, `king_welmar`, `peter`, `training_master`, `James`, `cleaning`, `tim`, `tom`, `DicknDavid`, `jerry` | `src/castle.c:444-925` |
| Tabela que liga vnum → procedure | `src/spec_assign.c:90-307` |

## Como ler os níveis

Conforme pedido, este arquivo usa **apenas três** níveis:

| Nível | Significa |
| --- | --- |
| **Testado (código)** | O comportamento está no fonte, com `arquivo:linha`. Prova o **engine**, e só o engine: o DeBo pode ter alterado ou traduzido. |
| **Provável** | Decorre do código, mas depende de configuração, do mundo do DeBo, de tradução, ou de o arquivo `.zon`/`.obj` do DeBo ser o mesmo. |
| **Dúvida** | Hipótese a resolver em sessão autorizada. |

Nenhuma linha aqui é "Testado (servidor)": **nada foi verificado ao vivo no DeBo**.

## 1. Tabela de afirmações

| # | Afirmação | Nível | Fonte (arquivo:linha) | Como validar no DeBo |
| --- | --- | --- | --- | --- |
| 1 | O mob de vnum **1** é o dragão **Puff** ("Puff the Fractal Dragon is here, contemplating a higher reality.") e é o único mob do jogo com a procedure `puff`. | Testado (código) | `lib/world/mob/0.mob:1-4`; `src/spec_assign.c:94` | Se o DeBo tem uma zona imortal com um dragão que fala sozinho, é este. Não testável por mortal em sessão normal. |
| 2 | `puff` fala sozinho com chance de **1 em 61** por tick, sorteando entre **4** falas fixas. | Testado (código) | `src/spec_procs.c:507` (sorteio `0..60`); falas em `:509`, `:512`, `:515`, `:518` | Ficar na mesma sala do dragão por vários minutos e contar as falas; registrar as 4 literalmente. |
| 3 | As falas do Puff são piadas: `"My god!  It's full of stars!"`, `"How'd all those fish get up here?"`, `"I'm a very female dragon."`, `"I've got a peaceful, easy feeling."` | Testado (código) | `src/spec_procs.c:509`, `:512`, `:515`, `:518` | Idem acima; comparar com a tradução PT-BR do DeBo. |
| 4 | O **prefeito** (`mayor`) é o único NPC com **rotina horária de caminhada** no mundo padrão: acorda às **6h** e às **20h** do relógio do jogo e percorre um caminho fixo codificado em string. | Testado (código) | `src/spec_procs.c:237-240` (caminhos), `:247` e `:251` (horas 6 e 20), `:261-320` (execução) | Ficar na rota do prefeito perto das 6h/20h do jogo (`time` para ver a hora) e seguir as falas dele. |
| 5 | O caminho do prefeito contém falas: `"Hello Honey!"` + `smirks`, `"What a view!  I must get something done about that dump!"`, `"Vandals!  Youngsters nowadays have no respect for anything!"`, `"Good day, citizens!"`, `"I hereby declare the bazaar open!"`, `"I hereby declare Midgaard closed!"`. | Testado (código) | `src/spec_procs.c:280-281`, `:285`, `:290`, `:295`, `:299`, `:303` | Idem; as falas aparecem sozinhas na sala, sem comando do jogador. |
| 6 | O prefeito **abre/destranca** e **fecha/tranca** um objeto chamado `gate` ao passar. | Testado (código) | `src/spec_procs.c:307-308` (unlock+open), `:312-313` (close+lock) | Observar o portão do bazar em Midgaard nos horários de passagem. |
| 7 | O prefeito é o mob **3105**, na zona 31 (sul de Midgaard); o prefeito do mundo padrão carrega a `City Key`. | Testado (código) | `src/spec_assign.c:120`; `lib/world/zon/31.zon:30-31` | Ver o prefeito na sala "The Mayor's Office" (sala 3138 no mundo padrão) e tentar `give`/`look`. |
| 8 | O `cityguard` **ataca** quem tem a flag de Player Killer ou de ladrão, gritando `"HEY!!!  You're one of those PLAYER KILLERS!!!!!!"` / `"...PLAYER THIEVES!!!!!!"`. | Testado (código) | `src/spec_procs.c:591-593` e `:597-599` | Só é testável com personagem marcada; **não** provocar para virar PK. Alternativa: observar guarda atacar outro jogador marcado. |
| 9 | O `cityguard` tem uma rotina de piada: se houver na sala alguém com **CARISMA < 6**, com 10% de chance ele **cospe** nessa pessoa usando o social `spit`. | Testado (código) | `src/spec_procs.c:584` (`min_cha = 6`), `:608-611`, `:620-625` (comentário `/* Reward the socially inept. */`) | Personagem feia (CHA baixo) parada perto de um guarda de Midgaard; esperar e registrar a mensagem de cuspida. |
| 10 | O `cityguard` também "protege os inocentes" com o grito `"PROTECT THE INNOCENT!  BANZAI!  CHARGE!  ARARARAGGGHH!"`. | Testado (código) | `src/spec_procs.c:614-616` | Observar combate entre NPCs perto de guarda. |
| 11 | Os vnums de guarda de cidade no mundo padrão incluem 3059, 3060, 3067 (Midgaard), 7900 (zona de Redferne) e ainda 5434, 5461-5463, 5482, 12018, 12021, 6500. | Testado (código) | `src/spec_assign.c:112-113`, `:117`, `:131`, `:240`, `:243-246`, `:260`, `:262`, `:273` | `consider`/observação por zona; vnums são do mundo padrão e podem não existir no DeBo. |
| 12 | O **Fido** é um cachorro que **devora cadáveres**: consome o corpo e **joga no chão** todo o conteúdo dele. | Testado (código) | `src/spec_procs.c:527-549`; `:535` (`IS_CORPSE`), `:538` (mensagem `"$n savagely devours a corpse."`), `:539-543` (solta o conteúdo) | Morrer perto de um Fido (ou observar um cadáver de NPC perto dele) e checar se o corpo some e os itens ficam no chão. |
| 13 | O **Fido** existe em 4 cópias em Midgaard (mob 3062) e uma quinta é o mob **3066** (chamado `Odif` no `.zon`). | Testado (código) | `src/spec_assign.c:115-116`; `lib/world/zon/30.zon:117-124` (Fido) e `:131` (`Odif`) | Procurar o cachorro nas ruas de Midgaard; `look` no mob. |
| 14 | O **janitor** (faxineiro) recolhe do chão só o que é pegável e que seja **bebida** ou tenha **custo < 15** moedas — ou seja, ele **ignora itens caros**. | Testado (código) | `src/spec_procs.c:561-563` (`CAN_WEAR`/`ITEM_WEAR_TAKE`, `ITEM_DRINKCON`, `GET_OBJ_COST >= 15`), `:565` (`"$n picks up some trash."`) | Largar um item barato no chão perto do faxineiro e ver sumir; largar um item caro e ver que fica. |
| 15 | Existem **3 janitors** no mundo padrão: mobs 1202 (zona imortal), 3061 e 3068 (Midgaard). | Testado (código) | `src/spec_assign.c:99`, `:114`, `:118`; `lib/world/zon/30.zon:116`, `:137` | Observar em Midgaard; vnum pode não existir no DeBo. |
| 16 | Existe um procedimento `dump` que **destrói tudo** que está no chão da sala e, se o jogador usar `drop` ali, paga por isso: valor = `MAX(1, MIN(50, custo/10))` por objeto; **nível < 3 ganha XP**, nível ≥ 3 ganha **ouro**. | Testado (código) | `src/spec_procs.c:199-230`; `:216` (fórmula), `:221` (`"You are awarded for outstanding performance."`), `:224-227` (regra de nível) | Ir ao lixão/dump de Midgaard (sala 3030 no mundo padrão) e `drop` um item barato; registrar o valor recebido. |
| 17 | O `dump` também é aplicado automaticamente a **toda sala com flag de death trap**, se a opção `dts_are_dumps` estiver ligada — e ela vem **ligada** (`YES`) por padrão. | Testado (código) | `src/spec_assign.c:303-306`; `src/config.c:86-87` (`int dts_are_dumps = YES;`) | Em death trap de Midgaard, largar um item e ver se some com `"$p vanishes in a puff of smoke!"`. |
| 18 | O `thief` rouba **1% a 10% do ouro** do alvo por tentativa, e o alvo pode flagrar: `"You discover that $n has $s hands in your wallet."` | Testado (código) | `src/spec_procs.c:332-354`; `:348` (fórmula `GET_GOLD * rand(1,10) / 100`), `:344-345` (mensagens) | Deixar ouro no bolso perto de um ladrão NPC e comparar `gold` antes/depois; registrar se apareceu a mensagem de flagrante. |
| 19 | Imortais e NPCs são **imunes** ao roubo do `thief`. | Testado (código) | `src/spec_procs.c:336-339`, `:383` | Não testável por mortal; serve para não confundir ausência de roubo em personagem imortal. |
| 20 | O `snake` só age **em combate** e, quando acerta, além da mordida conjura `SPELL_POISON` no alvo — "Quite lethal to low-level characters" (comentário do autor). | Testado (código) | `src/spec_procs.c:357-358` (comentário), `:362-370` | Enfrentar um dos mobs com `snake` e registrar envenenamento (`score`/`diagnose`). |
| 21 | `magic_user` só age em combate; escolhe alvo aleatório entre quem o está atacando, e usa uma **tabela de magias por nível do mob**: 4-5 `magic missile`, 6-7 `chill touch`, 8-9 `burning hands`, 10-11 `shocking grasp`, 12-13 `lightning bolt`, 14-17 `color spray`, acima disso `fireball`. | Testado (código) | `src/spec_procs.c:428-457` | Enfrentar mobs mágicos de níveis diferentes e registrar qual magia sai; os nomes das magias no DeBo serão PT-BR. |
| 22 | Além da magia de nível, o `magic_user` aplica efeitos extras: veneno (nível > 13), cegueira (nível > 7) e, para mobs malignos/bondosos, `energy drain`/`dispel evil`. | Testado (código) | `src/spec_procs.c:412-423` | Registrar `affects`/`score` depois de lutar contra mob mágico de nível alto. |
| 23 | São **dezenas** de mobs `magic_user` no mundo padrão (a lista ocupa ~40 linhas da tabela), inclusive na High Tower of Sorcery (zona 25), Pirâmide (53), Floresta (61), Arachnos (63), New Thalos (54), Roma (120) e Dwarven Kingdom (65). | Testado (código) | `src/spec_assign.c:126`, `:138-144`, `:147-188`, `:192-195`, `:198-203`, `:206-210`, `:213-216`, `:219-227`, `:232-242`, `:259-266`, `:274-276` | Não é preciso validar tudo; amostrar 3 zonas. Vnums são do mundo padrão. |
| 24 | Piada/leftover da tabela: o mob **5005** (um dragão de bronze no Deserto) recebe `guild_guard`, ou seja, age como **guarda de guilda**. | Testado (código) | `src/spec_assign.c:214` (`ASSIGNMOB(5005, guild_guard); /* brass dragon */`) | Se o DeBo tem dragão de bronze no deserto, ele bloqueia entrada de guilda. |
| 25 | `guild_guard` **bloqueia o movimento** de quem não é da classe daquela guilda, dizendo `"The guard humiliates you, and blocks your way."` | Testado (código) | `src/spec_procs.c:472` (mensagem), `:481-491` (checagem de sala/direção/classe) | Numa entrada de guilda de outra classe, tentar entrar e registrar a recusa literal. |
| 26 | Guards de guilda são imunes a cegueira e **deixam passar imortais**. | Testado (código) | `src/spec_procs.c:475` (`AFF_BLIND`), `:478-479` (`LVL_IMMORT`) | Guarda cego ou imortal é caso de teste de imortal; anotar como não testável por mortal. |
| 27 | Os guards de guilda do mundo padrão são exatamente os mobs **3024, 3025, 3026, 3027**. | Testado (código) | `src/spec_assign.c:108-111` | Confirmar nas 4 guildas de Midgaard. |
| 28 | Os **guildmasters** de Midgaard (mobs 3020-3023) usam a procedure `guild`, que só responde ao comando `practice` e calcula o ganho como `MIN(MAXGAIN, MAX(MINGAIN, int_app[INT].learn))`. | Testado (código) | `src/spec_assign.c:104-107`; `src/spec_procs.c:158` (`CMD_IS("practice")`), `:186-189` (fórmula), `:183` (`"You practice for a while..."`) | `practice` sem argumento deve listar as skills; com INT alta, o ganho por prática deve ser maior. |
| 29 | `practice` sem argumento lista as perícias com adjetivos graduados: `(not learned)`, `(awful)`, `(bad)`, `(poor)`, `(average)`, `(fair)`, `(good)`, `(very good)`, `(superb)`. | Testado (código) | `src/spec_procs.c:80-101` | `practice` no guildmaster e registrar os rótulos (traduzidos no DeBo, provavelmente). |
| 30 | O **banco** é um procedimento de **objeto**, não de mob: responde a `balance`, `deposit <n>` e `withdraw <n>`. | Testado (código) | `src/spec_procs.c:714-754`; `:718`, `:724`, `:738`; `src/spec_assign.c:289-290` | Ficar na sala do ATM e usar os três comandos. |
| 31 | Os objetos com banco no mundo padrão são o **ATM (vnum 3034)** e o **cashcard (vnum 3036)**; o ATM está instalado em 6 salas, e o cashcard é vendido/entregue pelo Grocer. | Testado (código) | `src/spec_assign.c:289-290`; `lib/world/obj/30.obj:209-224` (ATM); `lib/world/obj/30.obj:240-255` (cashcard); `lib/world/zon/30.zon:148-161` (6 salas com ATM); `lib/world/zon/30.zon:22` (cashcard dado pelo Grocer) | Na sala do Templo (3005) ou nas salas com ATM, testar `balance`. |
| 32 | O ATM **ensina o próprio comando** no `look`: `"To use, type 'BALANCE', 'WITHDRAW <amount>', or 'DEPOSIT <amount>'. Please report any strange occurrences to the bank manager."` | Testado (código) | `lib/world/obj/30.obj:221-222`; o mesmo texto no cashcard em `lib/world/obj/30.obj:252-253` | `look atm` e registrar o texto (tradução do DeBo pode diferir). |
| 33 | O banco **não paga juros, não cobra taxa e não tem limite**: quem trata dos três subcomandos é só o objeto, e não há nenhuma linha de juros/taxa em `spec_procs.c` (a procedure termina na linha 754). | Testado (código) | `src/spec_procs.c:714-754` (função inteira; nenhuma menção a juros/taxa); `:735`, `:749` (mensagens de depósito/saque) | Depositar 1 moeda, esperar dias de jogo e ver `balance`: se continuar 1, não há juros. |
| 34 | `balance`, `deposit`, `withdraw`, `mail`, `check`, `receive`, `rent` e `offer` **não são comandos reais**: na tabela de comandos todos apontam para `do_not_here`, cuja resposta é `"Sorry, but you cannot do that here!"`. Só funcionam onde um objeto/NPC com a procedure intercepta. | Testado (código) | `src/interpreter.c:227`, `:241`, `:265`, `:357`, `:417`, `:419`, `:380`, `:528`; `src/act.other.c:138-141` | Usar `balance` longe de um ATM: deve dar a recusa; perto do ATM, deve funcionar. É o teste mais limpo de todos. |
| 35 | O **correio** é a procedure `postmaster` e aceita exatamente três comandos: `mail`, `check`, `receive`. | Testado (código) | `src/mail.c:500-524`; `:505` | Na agência dos correios (sala 3062 no mundo padrão), testar os três. |
| 36 | Enviar carta custa **150 moedas** e exige **nível ≥ 2**; a carta é escrita e terminada com `@` numa linha nova. | Testado (código) | `src/mail.h:23` (`#define STAMP_PRICE 150`), `src/mail.h:20` (`#define MIN_MAIL_LEVEL 2`); `src/mail.c:533-537`, `:545-563`, `:558-560` (`"I'll take %d coins for the stamp."` / `"Write your message, use @ on a new line when done."`) | Com nível ≥ 2 e 150+ moedas, `mail <nome>` e registrar o custo real; com menos ouro, registrar a recusa. |
| 37 | `check` responde `"You have mail waiting."` ou `"Sorry, you don't have any mail waiting."`; `receive` cria um objeto do tipo **note** ("a piece of mail"). | Testado (código) | `src/mail.c:572-579`; `src/mail.c:588-598` (`obj->name = strdup("mail paper letter")`, `GET_OBJ_TYPE(obj) = ITEM_NOTE`); tipo note = `ITEM_NOTE 16` em `src/structs.h:309` | `check` e `receive` na agência; registrar o nome do item recebido. |
| 38 | O **postmaster** do mundo padrão é o mob **3010**, na sala "The Post Office" (3062); também há um na zona imortal (mob 1201). | Testado (código) | `src/spec_assign.c:98`, `:103`; `lib/world/zon/30.zon:60`; `lib/world/wld/30.wld:1303` (sala "The Post Office") | Localizar a agência e conferir. |
| 39 | Se o correio estiver desabilitado no boot, o postmaster responde `"Sorry, the mail system is having technical difficulties."` | Testado (código) | `src/mail.c:508-511`; `src/db.c:55` (`int no_mail = 0;`) e `src/db.c:445` | Se o DeBo tiver desligado o correio, é esta a mensagem. |
| 40 | Os **murais** são objetos com a procedure `gen_board`, e existem **4**: 3099 (mortal), 3098 (imortal), 3097 (frozen), 3096 (social). | Testado (código) | `src/boards.c:66-71` (tabela); `src/boards.h:11` (`NUM_OF_BOARDS 4`); `src/spec_assign.c:284-287` | `look board` nos 4 murais do mundo padrão (salas 3000, 3003, 3018, 3022, 3028 conforme `lib/world/zon/30.zon:163-172`). |
| 41 | Cada mural tem **nível mínimo de leitura, escrita e remoção**: o mortal (3099) todos leem e escrevem, mas só `LVL_GOD` remove; o social (3096) todos leem/escrevem e `LVL_IMMORT` remove. | Testado (código) | `src/boards.c:67`, `:70`; macros `READ_LVL`/`WRITE_LVL`/`REMOVE_LVL` em `src/boards.h:37-39`; checagem em `src/boards.c:194` | Tentar `write` e depois `remove` no mural de leitura livre; registrar a recusa. |
| 42 | O mural comporta **60 mensagens** de até **4096 caracteres**, e o título é cortado em **80** caracteres. | Testado (código) | `src/boards.h:12` (`MAX_BOARD_MESSAGES 60`), `src/boards.h:13` (`MAX_MESSAGE_LENGTH 4096`); `src/boards.c:198` (`"The board is full."`); `src/boards.c:211-212` (corte em 80) | `look board` num mural cheio; tentar título gigante e ver o corte. |
| 43 | As mensagens dos murais são gravadas em arquivo: `board.mort`, `board.immort`, `board.freeze`, `board.social` (caminho `lib/etc/...`). | Testado (código) | `src/boards.c:67-70`; `src/db.h:24` (`LIB_ETC ":etc:"`) e `src/db.h:35` (`LIB_ETC "etc/"`); gravação em `src/boards.c:433-443` | Só testável por imortal (olhar o arquivo). Para mortal: escrever, sair, relogar e ver se a mensagem persistiu. |
| 44 | Escrever num mural mostra `"Write your message.  Terminate with a @ on a new line."` e a sala vê `"$n starts to write a message."` | Testado (código) | `src/boards.c:227-228` | `write <título> board` e registrar a instrução de terminação. |
| 45 | O comando `remove` num mural **apaga mensagem**, embora `remove` seja normalmente o comando de tirar equipamento: o mesmo verbo é interceptado pela procedure. | Testado (código) | `src/boards.c:181-182`, `:356` (`Board_remove_msg`); `src/interpreter.c:418` (`remove` → `do_remove`) | `remove <n> board` num mural e ver a confirmação `"$n just removed message %d."` (`src/boards.c:425`). |
| 46 | O sistema de **casa** usa um arquivo de controle (`lib/etc/hcontrol`) e arquivos por casa (`lib/house/<vnum>.house`); há limite de **100 casas** e **10 convidados** por casa. | Testado (código) | `src/db.h:96` (`HCONTROL_FILE LIB_ETC"hcontrol"`); `src/house.c:55` (`LIB_HOUSE"%d.house"`); `src/db.h:39` (`LIB_HOUSE "house/"`); `src/house.h:1-2` (`MAX_HOUSES 100`, `MAX_GUESTS 10`); `src/house.c:225`, `:246` | Só imortal constrói casa; para mortal, ver se existe a sala "casa" e testar `house`. |
| 47 | A entrada numa casa é restrita ao **dono** e à lista de convidados; `LVL_GRGOD` entra sempre. | Testado (código) | `src/house.c:570-587` (usa `GET_IDNUM` contra `house_control[i].owner` e `guests[]`) | Se houver casa de outro jogador, tentar entrar e registrar a recusa. |
| 48 | O comando **de mortal** da casa é `house`, em posição `POS_RESTING`, e serve para **adicionar/remover convidados** (`Guest added.` / `Guest deleted.`) estando dentro da própria casa. | Testado (código) | `src/interpreter.c:327` (`house`, `do_house`, lvl 0); `src/house.c:511-548`; `:519` (`"You must be in your house to set guests."`), `:523` (`"Only the primary owner can set guests."`), `:547`, `:537` | Com casa própria (se houver no DeBo), `house <nome>` e registrar as mensagens. |
| 49 | O comando de administração é `hcontrol` (requer `LVL_GRGOD`) com subcomandos `build`, `destroy`, `pay`, `show`. | Testado (código) | `src/interpreter.c:319` (`hcontrol`, `do_hcontrol`, `LVL_GRGOD`); `src/house.c:491-507` (`:497` build, `:499` destroy, `:501` pay, `:503` show) | Não testável por mortal. |
| 50 | Curiosidade de texto do sistema de casa: ao construir, o imortal vê `"House built.  Mazel tov!"`; ao listar convidados mortos, o jogo escreve literalmente **`all dead`**. | Testado (código) | `src/house.c:422`; `src/house.c:611-612` | Pedir a um imortal para rodar `hcontrol show` e registrar. |
| 51 | O **aluguel** (`rent`) e a **criogenia** (`cryo`) são a mesma procedure com fator diferente: `RENT_FACTOR 1` e `CRYO_FACTOR 4`. | Testado (código) | `src/objsave.c:24-25`; `src/objsave.c:1142-1151` | `rent` na recepcionista e `rent` no criogenicista: o preço do cryo deve ser ~4x. |
| 52 | O custo do aluguel é `min_rent_cost * fator` **mais** `GET_OBJ_RENT` de cada item (× fator); `min_rent_cost` vem como **100**. | Testado (código) | `src/objsave.c:1023` (`totalcost = min_rent_cost * factor;`), `:995` (`GET_OBJ_RENT(obj) * factor`); `src/config.c:139` (`int min_rent_cost = 100;`), `src/config.c:138` (comentário "receptionist's surcharge") | `offer` na recepcionista com inventário vazio vs. cheio e comparar o total. |
| 53 | O aluguel é **por dia real** e a recepcionista informa quantos dias o jogador pode pagar com o ouro que tem (mão + banco). | Testado (código) | `src/objsave.c:1102` (`"Rent will cost you %d gold coins per day."`), `:962-964` (`"You can rent for %ld day%s with the gold you have on hand and in the bank."`) | `rent` na recepcionista e registrar a cotação e o prazo. |
| 54 | Se o item alugado não for retirado no prazo, ele é **apagado**: `rent_file_timeout` = 30 dias, `crash_file_timeout` = 10 dias. | Testado (código) | `src/config.c:158` (`crash_file_timeout = 10`), `src/config.c:161` (`rent_file_timeout = 30`); `src/objsave.c:300`, `:321-325` | Não testável de forma barata; anotar como limite. |
| 55 | Na árvore padrão o aluguel vem **de graça** (`free_rent = YES`), e a recepcionista diz `"Rent is free here.  Just quit, and your objects will be saved!"` | Testado (código) | `src/config.c:133` (`int free_rent = YES;`); `src/objsave.c:1090-1094` | `rent` na recepcionista: se aparecer a mensagem de graça, o DeBo manteve o padrão. |
| 56 | A **recepcionista** tem rotina própria de social aleatório: com 1 em 6 de chance ela executa um de `smile, dance, sigh, blush, burp, cough, fart, twiddle, yawn`. | Testado (código) | `src/objsave.c:1066-1067` (tabela), `:1069-1072` (sorteio e `do_action`) | Ficar parado ao lado da recepcionista por alguns minutos e registrar quais emotes ela faz sozinha. É um dos testes mais baratos e mais divertidos. |
| 57 | O **criogenicista** (mob 3095) é o "freeze" do jogo e também usa a lista de sociais acima. | Testado (código) | `src/spec_assign.c:119`; `src/objsave.c:1148-1151`; `lib/world/zon/30.zon:145` | Visitar o "Cryogenic Center" (sala 3064) e conversar/observar. |
| 58 | A **loja de animais** é uma **sala** (room proc), não um mob: a sala 3031 recebe `pet_shops`, e os animais são lidos da sala seguinte (`IN_ROOM(ch) + 1`), com o comentário `/* Gross. */` no código. | Testado (código) | `src/spec_assign.c:301`; `src/spec_procs.c:644-651`; `:650-651`; `lib/world/wld/30.wld:745` (The Pet Shop) e `:777` (Pet Shop Store) | Na loja de animais, `list` e `buy <animal>`; conferir que os bichos vêm da sala dos fundos. |
| 59 | Preço de animal = **nível do mob × 300** moedas; o bicho comprado vira seguidor com `AFF_CHARM` e **não pode carregar nada** (`IS_CARRYING_W = 1000`, `IS_CARRYING_N = 100`). | Testado (código) | `src/spec_procs.c:642` (`#define PET_PRICE(pet) (GET_LEVEL(pet) * 300)`); `:676-678`; `:693-695`; `:697` (`"May you enjoy your pet."`) | `list` na loja e comparar preço com o `consider` do bicho; comprar o mais barato e testar `give` nele. |
| 60 | Se o jogador nomear o bicho, ele ganha uma placa: `"A small sign on a chain around the neck says 'My name is %s'"`; e existe a piada no código: `/* No, you can't have the Implementor as a pet if he's in there. */` | Testado (código) | `src/spec_procs.c:685-686`; `src/spec_procs.c:656-658` | `buy <bicho> <nome>` e depois `look <nome>`; registrar a placa. |
| 61 | Os animais à venda no mundo padrão são `Kitten`, `Puppy`, `Beagle`, `Rottweiler` e `Wolf`, com um `Pet Shop Boy` (mob 3089) na loja. | Testado (código) | `lib/world/zon/30.zon:139-144` | `list` na loja de animais; registrar os nomes reais (PT-BR). |
| 62 | O **castelo/reino** desta árvore é o castelo do **Rei Welmar**, na zona **150**, e as procedures são atribuídas por **deslocamento dentro da zona**, não por vnum literal (`castle_virtual` = base da zona + offset). | Testado (código) | `src/castle.c:31` (`#define Z_KINGS_C 150`), `:98-106` (`castle_virtual`), `:126-153` (`assign_kings_castle`), `:76-81` (comentário do autor) | Se o DeBo mantiver a zona 150 e o castelo, o rei se move às 8h/21h/12h do jogo (ver #64). |
| 63 | Os mobs do castelo, por offset: 1 = Rei Welmar; 12 = Peter (capitão); 13 = training master; 16 = James (mordomo); 17 = Ze Cleaning Fomen; 20 = Tim; 21 = Tom; 24/25 = Dick e David (tesouro); 26 = Jerry (jogador); 0, 3-11, 27-29 = guardas (com nomes no comentário: Gwydion, Jim, Brian, Mick, Matt, Jochem, Anne, Andrew, Bertram, Jeanette, Michael, Hans, Boris). | Testado (código) | `src/castle.c:128-152` | `look` nos mobs do castelo e comparar os nomes com a lista. |
| 64 | O **Rei Welmar** tem agenda: às **12h** faz um **monólogo em latim** na sala do trono (`"Primus in regnis Geticis coronam."`, `"regiam gessi, subiique regis."`, `"munus et mores colui sereno."`, `"principe dignos."`), às **8h** vai para o trono e às **21h** volta para o quarto. | Testado (código) | `src/castle.c:448-453` (monólogo), `:455-457` (caminhos), `:464`, `:468`, `:472` (horários 8/21/12); falas do caminho em `:532`, `:536`, `:523`, `:518`; abre/fecha `door` em `:539-546` | Esperar as 12h do jogo na sala do trono e registrar o monólogo (4 falas, uma por tick). É o "segredo" mais teatral do castelo. |
| 65 | O Rei tem comportamento mágico em combate: `fry_victim` gasta 10 de mana para conjurar `color spray`, `harm`, `fireball` — ou **curar a si mesmo**. | Testado (código) | `src/castle.c:394-435`; `:405-429` (sorteio e magias), `:427-428` (auto-cura), `:432` (custo de mana) | Se algum jogador atacar o rei (não recomendado), registrar; caso contrário, só leitura. |
| 66 | Todo o staff do castelo (guardas, Tim, Tom, Dick, David, Peter, mestre, rei) usa `banzaii`: o grito `"Protect the Kingdom of Great King Welmar!  BANZAIIII!!!"` e ataque a quem estiver brigando com o staff. | Testado (código) | `src/castle.c:300-311`; `:307-308` (grito) | Observar (ou provocar com muito cuidado) uma briga no castelo e registrar o grito. |
| 67 | **Tim e Tom são gêmeos**: cada um socorre o outro e o Rei se o outro estiver com menos da metade dos HP; protegidos por `block_way`, empurram quem tenta entrar no quarto do Rei. | Testado (código) | `src/castle.c:652-660`; `:665-692`; `:684-686` (resgate do gêmeo); `:673` (`block_way`) ; `:352-369` (`block_way`, `"The guard roars: 'Entrance is Prohibited!', and pushes you back."`) | Tentar entrar no quarto do Rei (offset 48/49) e registrar o empurrão. |
| 68 | O **mordomo James** reclama do lixo: `"My oh my!  I ought to fire that lazy cleaning woman!"` e recolhe qualquer item de custo ≤ 10 ou bebida que esteja no chão. | Testado (código) | `src/castle.c:701-704`, `:709-731`; `:721-723`; `:376-385` (`is_trash`: `ITEM_DRINKCON` ou custo ≤ 10) | Largar um item barato no castelo e ver o mordomo pegar. |
| 69 | A **mulher da limpeza** ("Ze Cleaning Fomen") faz o mesmo, mas **sem** reclamar (a diferença é o argumento `gripe`). | Testado (código) | `src/castle.c:738-741`; `:709-731`; `:720` (`if (gripe)`) | Observar. |
| 70 | O capitão **Peter** inspeciona os guardas ao acaso com falas fixas, incluindo `"Those boots need polishing!"`, `"Straighten that collar!"` e `"That chain mail looks rusty!  CLEAN IT !!!"` | Testado (código) | `src/castle.c:779-839`; `:789` (sorteio), `:818`, `:825`, `:832` | Ficar na presença do capitão e de um guarda e registrar as broncas. |
| 71 | **Jerry, o jogador**, joga dados com **Michael** (um guarda) e tem 6 resultados distintos de fala, incluindo `"Well, my luck has to change soon"`. | Testado (código) | `src/castle.c:846-925`; `:874-923` | Observar Jerry e Michael na sala offset 8. |
| 72 | `DicknDavid` bloqueiam a direção para o **tesouro** (offset 36) e também `banzaii`. | Testado (código) | `src/castle.c:763-772`; `:771` | Tentar passar por eles. |
| 73 | O **mestre de treino** faz demonstrações com seus alunos fixos **"Brian"** e **"Mick"** (por nome, não por vnum), com golpes, quedas de arma e reverências. | Testado (código) | `src/castle.c:566-649`; `:579` e `:582` (busca por nome); `:596`, `:602`, `:608`, `:617-621`, `:625`, `:631`, `:637`, `:643` | Ficar na sala de treino do castelo e observar. |
| 74 | **Não existe** comando `castle` (de clã/guilda) nesta árvore: nenhuma entrada `castle` na tabela de comandos de `interpreter.c`; `castle.c` implementa apenas comportamento de NPCs. | Testado (código) | `src/interpreter.c` (busca por `castle` sem resultado); `src/castle.c:1-10` (cabeçalho: "Special procedures for King's Castle area") | Se o DeBo tem `castle`/clã com aluguel e guardas, é acréscimo posterior ao 3.x padrão — perguntar no jogo. |
| 75 | Leftover: `src/castle.c:72` **declara** `SPECIAL(guild)` mas o arquivo não define nem usa essa procedure; a atribuição real está em `spec_assign.c` (mobs 3020-3023). | Testado (código) | `src/castle.c:72`; ausência de definição em `castle.c` (definição real em `src/spec_procs.c:154`); `src/spec_assign.c:104-107` | Nada a testar no jogo; é nota de auditoria. |
| 76 | **Morte custa metade do XP total acumulado** (`gain_exp(ch, -(GET_EXP(ch) / 2))`) — não é uma fração do XP do nível. | Testado (código) | `src/fight.c:378-384`, em especial `:380` | Registrar `score` (XP) antes e depois de morrer: deve cair ~50%. |
| 77 | **Não se perde nível ao morrer**: o laço que rebaixa nível só existe no ramo de ganho de XP; a perda apenas subtrai XP e o piso é 0. | Testado (código) | `src/limits.c:265-274` (rebaixa/sobe nível só com ganho), `:287-292` (perda: `GET_EXP += gain`, `if (GET_EXP(ch) < 0) GET_EXP(ch) = 0;`) | Matar-se de propósito uma vez e conferir que o nível não caiu. |
| 78 | Ao morrer, **todo** o inventário, **todo** o equipamento e **todo** o ouro vão para o cadáver; o corpo é um container sem uso (`GET_OBJ_VAL(corpse, 0) = 0  /* You can't store stuff in a corpse */`), com marca de cadáver, peso do dono e aluguel artificial de 100000. | Testado (código) | `src/fight.c:272-334`; `:291-297`; `:294` (comentário), `:297` (`GET_OBJ_RENT(corpse) = 100000`); inventário `:304-307`; equipamento `:310-312`; ouro `:314-328` | Morrer com um item marcado e conferir, ao voltar, que tudo está no corpo no chão. |
| 79 | O cadáver some sozinho: **5 ticks** para corpos de NPC e **10 ticks** para corpos de jogador (padrão). | Testado (código) | `src/fight.c:298-301`; `src/config.c:76-77` (`max_npc_corpse_time = 5`, `max_pc_corpse_time = 10`) | Após morrer, contar quanto tempo o corpo fica no chão. |
| 80 | A morte é anunciada com grito ouvido nas salas vizinhas: `"Your blood freezes as you hear $n's death cry."` e a mesma mensagem (sem nome) nas salas adjacentes. | Testado (código) | `src/fight.c:349-358`; `:353`, `:357` | Observar a morte de outro jogador/NPC e registrar. |
| 81 | Morrer **limpa as flags de PK e de ladrão**: `REMOVE_BIT(PLR_FLAGS(ch), PLR_KILLER | PLR_THIEF)`. | Testado (código) | `src/fight.c:381-382` | Só testável com personagem marcada; anotar como não recomendado. |
| 82 | Morto por outro, o jogador volta a jogar sem perder comando: a extração é **adiada** para o fim do tick (`PLR_NOTDEADYET`), então o servidor não "trava" o personagem. | Testado (código) | `src/handler.c:961-969`; `src/handler.c:982-1015`; `src/fight.c:681`, `:686` | Perceber que, ao morrer, ainda se recebe uma última resposta/posição antes de sair. |
| 83 | A mensagem que o morto vê é `"You are dead!  Sorry..."` e a sala vê `"$n is dead!  R.I.P."` | Testado (código) | `src/fight.c:782-785` | Registrar a mensagem exata ao morrer. |
| 84 | Quem mata ganha XP: solo = `MIN(max_exp_gain, EXP(vítima)/3)` **mais bônus de diferença de nível**; em grupo há divisão e arredondamento (`tot_gain = EXP/3 + membros - 1`). | Testado (código) | `src/fight.c:444-465`; `:424` (grupo), `:431` (base), `:448` (solo), `:452`/`:454` (bônus), `:463`; `src/config.c:72` (`max_exp_gain = 100000`) | Matar o mesmo mob sozinho e em dupla e comparar XP recebido. |
| 85 | Curiosidade: **bater** também dá XP, na fórmula `GET_LEVEL(vítima) * dano` por golpe. | Testado (código) | `src/fight.c:741-742` | Comparar XP ganho em luta longa sem matar contra luta curta. |
| 86 | O dano por rodada é **limitado a 100** (`dam = MAX(MIN(dam, 100), 0)`) e santuário corta o dano pela metade. | Testado (código) | `src/fight.c:737`; `:726-727` | Medir dano máximo recebido em vários golpes; nenhum deve passar de 100 por golpe. |
| 87 | O `consider` (em `act.informative.c`, não em `fight.c`) compara **níveis** e tem 11 respostas fixas, de `"Now where did that chicken go?"` a `"You ARE mad!"`, além de `"Easy!  Very easy indeed!"` para si mesmo e `"Would you like to borrow a cross and a shovel?"` para outro jogador. | Testado (código) | `src/act.informative.c:1452-1496`; `:1465`, `:1469`, `:1475`, `:1477`, `:1483`, `:1491`, `:1495` | `consider` contra 3 mobs de níveis bem diferentes e contra si mesmo; registrar as frases (traduzidas no DeBo). |
| 88 | O `wimpy` é configurável por número de HP, **não pode passar da metade dos HP máximos**, e 0 desliga. | Testado (código) | `src/act.other.c:690-728`; `:716-717` (limite de metade), `:719`, `:723`; `src/interpreter.c:526` (`wimpy`, qualquer nível) | `wimpy` (sem argumento), depois `wimpy <n>` acima da metade dos HP e registrar a recusa. |
| 89 | Com `wimpy` ativo, ao cair abaixo do limiar o personagem **foge sozinho** e vê `"You wimp out, and attempt to flee!"`; mobs com `MOB_WIMPY` também fogem. | Testado (código) | `src/fight.c:797-801`; `:794-795` (mob wimpy) | Ativar `wimpy 1` e entrar num combate perdido; registrar a fuga automática. |
| 90 | Curiosidades do `wimpy`: `"At the moment, you're not a wimp.  (sure, sure...)"` e `"Heh, heh, heh.. we are jolly funny today, eh?"` (valor negativo). | Testado (código) | `src/act.other.c:706`, `:713` | `wimpy` e `wimpy -5`; registrar as duas respostas. |
| 91 | Mobs agressivos atacam por flag `MOB_AGGRESSIVE`/`MOB_AGGR_TO_ALIGN`, com tratamento especial para mobs "na coleira" (charmados/seguidores). | Testado (código) | `src/mobact.c:96`, `:105`, `:111`, `:132`, `:152`, `:248-253`; `src/db.c:1379-1380` | Entrar em sala com mob agressivo e registrar o ataque; em mob agressivo por alinhamento, testar com alinhamento oposto. |
| 92 | Ajuste de alinhamento ao matar: move 1/16 do caminho rumo ao alinhamento oposto ao da vítima. | Testado (código) | `src/fight.c:338-345`; `:344` (fórmula), `:340-343` (comentário do autor) | Matar mob muito bom e ver o alinhamento cair em `score`. |
| 93 | O **tabuleiro de xadrez** é a zona **36** e tem **67 salas**, das quais **64 são casas** ("A White Square"/"A Black Square" alternando) mais **1 sala de entrada** ("The Great Chessboard Of Midgaard", 3600) e **2 tesouros** ("The Black Treasury" 3665 e "The White Treasury" 3666). | Testado (código) | `lib/world/zon/36.zon:1-5`; `lib/world/wld/36.wld:1` (3600), `:1573` (3665), `:1585` (3666); contagem de blocos `#` = 67 e de terminadores `S` = 67 (medidos nos dois métodos sobre `36.wld`) | Contar as casas andando pelo tabuleiro e registrar os nomes; comparar com [05-mundo-padrao-vs-mapa.md](05-mundo-padrao-vs-mapa.md). |
| 94 | O tabuleiro nasce com **32 peças** (16 de cada lado): 8 peões pretos + 8 brancos, 2 torres, 2 cavalos, 2 bispos, 1 rainha e 1 rei por lado. | Testado (código) | `lib/world/zon/36.zon:8-55` (16 peões), `:56-63` (4 torres), `:64-71` (4 cavalos), `:72-79` (4 bispos), `:80-83` (2 rainhas), `:84-89` (2 reis) | Contar as peças no tabuleiro (cuidado: peões têm `max 8` e são reposicionados). |
| 95 | Os mobs-peça do tabuleiro são 3600-3611: 3600 Black Pawn, 3601 White Pawn, 3602 Black Rook, 3603 White Rook, 3604 Black Knight, 3605 White Knight, 3606 Black Bishop, 3607 White Bishop, 3608 Black Queen, 3609 White Queen, 3610 Black King, 3611 White King. | Testado (código) | `lib/world/zon/36.zon:8`, `:32`, `:56`, `:60`, `:64`, `:68`, `:72`, `:76`, `:80`, `:82`, `:84`, `:87` | `look`/`consider` nas peças e comparar nomes (PT-BR). |
| 96 | O tabuleiro tem **2 tesouros guardados** com **chaves**: os reis carregam a `Black Treasury Key`/`White Treasury Key` e há pilhas de ouro (`Black Treasury Gold` 3616, `White Treasury Gold` 3617) dentro de salas trancadas (portas `D` em `:94-97`). | Testado (código) | `lib/world/zon/36.zon:86`, `:89` (chaves), `:91-92` (ouro), `:94-97` (portas); salas 3665/3666 em `lib/world/wld/36.wld:1573`, `:1585` | Matar o rei, pegar a chave e abrir o tesouro — o "segredo" público mais conhecido do tabuleiro. |
| 97 | Cada peça nasce **equipada** com seu item temático (armadura de peão, lança de cavalo, cajado de bispo, coroa de rainha, cetro de rei). | Testado (código) | `lib/world/zon/36.zon:9-10`, `:33-34`, `:57`, `:61`, `:65`, `:69`, `:73`, `:77`, `:81`, `:83`, `:85`, `:88` | Matar uma peça e ver o que ela deixa cair. |
| 98 | Os **esgotos** são as zonas 70, 71, 72 e 73, somando **175 salas** nos arquivos de mundo: 62 + 26 + 87, sendo que **não existe `73.wld`** — as salas da zona 73 estão dentro de `72.wld` (que cobre 7200-7345). | Testado (código) | `70.wld`: 62 blocos/62 `S`; `71.wld`: 26/26; `72.wld`: 87/87 (contagem dupla medida); ausência de `lib/world/wld/73.wld` (verificado por listagem) | Contar salas ao andar; a ligação entre as zonas aparece nas portas citadas abaixo. |
| 99 | Os esgotos têm **quatro níveis nomeados**: "The Sewer, First Level" (70), "The Second Sewer" (71), "The Sewer Maze" (72), "The Tunnels In The Sewer" (73). | Testado (código) | `lib/world/zon/70.zon:2`, `71.zon:2`, `72.zon:2`, `73.zon:2` | Comparar os nomes vistos no jogo. |
| 100 | Os primeiros dois níveis têm reset a cada **15** e **20** minutos de jogo e 2 de "lifespan"; as zonas 72 e 73 a cada **25**. | Testado (código) | `lib/world/zon/70.zon:3` (`7000 7099 15 2`), `71.zon:3` (`7100 7199 20 2`), `72.zon:3` (`7200 7299 25 2`), `73.zon:3` (`7300 7399 25 2`) | Matar mobs e cronometrar o repovoamento. |
| 101 | Os mobs dos esgotos incluem `The Mean Bat`, `The Sewer Rat`, `The Small Hairy Spider` (nível 1), `The Earth Beetle`, `The Giant Maggot`, `The Horrifying Mudmonster`, `The Slithering Snake` (nível 2), `Wererat`, `Gigantic Rat` e os **Mindflayers** (Master/Senior/Junior) na zona 72. | Testado (código) | `lib/world/zon/70.zon:6-17`; `71.zon:6-15`; `72.zon:6-43` (`:6` Master Mindflayer, `:12` Senior, `:14`/`:16` Junior, `:18`+ Wererat, `:32` Gigantic Rat) | Registrar os mobs reais (nomes traduzidos) por nível. |
| 102 | A zona 73 (túneis) tem os chefes: **The Red Dragon**, **The Sea Hag**, **The Good Guardian Naga**, **The Basilisk**, **The Lemure Blob**, os ettins **Jones** e **Herald** e o `Chr-eff'n`. | Testado (código) | `lib/world/zon/73.zon:6-13` | Se o DeBo mantiver os esgotos, esses nomes devem aparecer; conferir `consider` antes. |
| 103 | Duas portas dos esgotos são chamadas **`False Door`** e existem `The Secret Room Door`, `Secret Tunnel Entrance` e `Secret Way Down` nas zonas 71-73. | Testado (código) | `lib/world/zon/73.zon:23-24` (False Door), `:15` (Secret Room Door), `:25` (Secret Tunnel Entrance); `71.zon:21` (`D 0 7116 5 1  Secret Way Down`) | Procurar saídas secretas nos túneis: `exits`/`look` nas salas citadas. |
| 104 | Há um **poço** no mundo padrão como sala, não como objeto: sala **7015 "The Old Well"** (zona 70) e sala **7105 "Down The Old Well"** (zona 71). | Testado (código) | `lib/world/wld/70.wld:385`; `lib/world/wld/71.wld:114` | Se o DeBo tem "poço", testar `enter well`/`look well` nas duas salas. |
| 105 | Há **fontes** como objeto tipo `ITEM_FOUNTAIN` (valor 23): a `fountain` 3035 na praça do Templo e a `fountain` 3113 no parque, ambas com valores `9999 9999 15 0` (reserva praticamente infinita). | Testado (código) | `src/structs.h:316` (`#define ITEM_FOUNTAIN 23`); `lib/world/obj/30.obj:225-232` (vnum 3035, tipo 23 em `:230`, valores em `:231`); `lib/world/obj/31.obj:172-179` (vnum 3113, tipo 23 em `:177`); reset em `lib/world/zon/30.zon:148-149` e `lib/world/zon/31.zon:49-50` | `drink fountain` e `fill <recipiente> fountain` nas duas fontes; registrar se a água acaba. |
| 106 | O comando `drink` funciona em `ITEM_DRINKCON` **e** `ITEM_FOUNTAIN`; encher recipiente na fonte é permitido, mas encher de/para certos tipos é bloqueado. | Testado (código) | `src/act.item.c:762`, `:802`, `:840-845`, `:1013`, `:1039` (`if (GET_OBJ_TYPE(from_obj) != ITEM_FOUNTAIN)`) | `fill cantil fountain` e depois `drink cantil`; testar também `drink fountain`. |
| 107 | Curiosidade: junto à fonte do parque há uma pilha de **`20 Coins`** (objeto 3114) que nasce no chão a cada reset. | Testado (código) | `lib/world/zon/31.zon:49-51` (`O 0 3113 1 3141 Fountain` e `O 0 3114 1 3141 20 Coins`); objeto em `lib/world/obj/31.obj:184-191` (tipo 20 = `ITEM_MONEY`, `src/structs.h:313`) | Ir ao parque no reset e pegar as moedas; mede o tempo do reset. |
| 108 | **Não existe "sino" (bell) em nenhum lugar desta árvore** — busca por `bell` em `src/*.c` só encontra "Aaron Campbell" (`bsd-snprintf.c:13`) e "Charmed Mob Rebellion" (`mobact.c:143`); não há objeto nem NPC de sino. | Testado (código) | `src/bsd-snprintf.c:13`; `src/mobact.c:143`; `lib/world/obj/*.obj` (sem `^bell$`) | Se no DeBo existe sino, é **acréscimo do DeBo** — bom candidato a "segredo local". |
| 109 | A **Zona dos Novatos** (zona 186, "Newbie Zone", criada por *Maynard of StrangeMUD*) tem **41 salas** (18600-18612 e 18620-18647) e **101 registros de saída**. | Testado (código) | `lib/world/zon/186.zon:1-5`; contagem dupla sobre `lib/world/wld/186.wld`: 41 blocos `#` e 41 linhas `S`; 101 linhas começando com `D` | Andar pela zona e contar; conferir com [05-mundo-padrao-vs-mapa.md](05-mundo-padrao-vs-mapa.md). |
| 110 | A zona de novatos tem salas com nomes sugestivos: "The Entrance To The Newbie Zone" (18600), "A Nexus" (18603), "The Dark Pit" (18605), "The Alchemist's Room" (18612), "The Red Room" (18629), "The Statue's Room" (18640), "The Balcony" (18643/18645). | Testado (código) | `lib/world/wld/186.wld:1`, `:64`, `:110`, `:249`, `:440`, `:668`, `:745`, `:792` | Conferir nomes no jogo. |
| 111 | Na sala da estátua (18640) o texto do mundo cita o autor: `"Maynard, Death Jester of the Harlequins"`. | Testado (código) | `lib/world/wld/186.wld:693` | `look statue`/`read` na sala 18640 e registrar a dedicatória. |
| 112 | A zona de novatos tem um **dragão** (`Dragon`, mob 18603) que carrega um `Collar`, além do `Pit Beast` (18601), `Newbie Monster` (18602), `Annoying Newbie` (18611), `Clueless Newbie` (18612), `Friendly Newbie` (18613), `Lost Newbie` (18614), `Smart Newbie` (18615), `Alchemist` (18605), `Crawler`, `Zombie`, `Quasit`, `Minotaur` e `Spectre`. | Testado (código) | `lib/world/zon/186.zon:8-47`; `:25-26` (Dragon + Collar) | `consider`/`look` nos mobs da zona de novatos. |
| 113 | Os "novatos" NPC da zona 186 (18611-18615) são mobs **com arma e armadura equipadas** no reset (Dagger, Vest, Sleeves, Leggings, Mace) — ou seja, matar "novato" dá equipamento. | Testado (código) | `lib/world/zon/186.zon:14-24`; `:29` (Key), `:32` (Light) | Matar um "Annoying Newbie" e ver o que cai. |
| 114 | Midgaard Norte (zona 30) tem **59 salas** (3000-3066) e Midgaard Sul (zona 31) tem **54 salas** (3100-3205), medidas nos `.wld`. (O arquivo irmão 05 reporta 65 e 62 salas para as mesmas zonas — divergência de método a reconciliar.) | Testado (código) | contagem dupla (blocos `#` e linhas `S`) sobre `lib/world/wld/30.wld` (59/59) e `lib/world/wld/31.wld` (54/54) | Andar e contar; é exatamente o tipo de número que [05](05-mundo-padrao-vs-mapa.md) já discute. |
| 115 | A zona 30 repõe **55 mobs, 12 objetos, 62 gives, 24 equipamentos e 12 "rooms"**, terminando o reset em `30.zon:174` (`S`). | Testado (código) | contagem medida sobre `lib/world/zon/30.zon`; terminator em `lib/world/zon/30.zon:174` | Observar o repovoamento de Midgaard depois de limpar uma área. |
| 116 | A zona 31 repõe **20 mobs, 9 objetos, 6 gives, 5 equipamentos, 2 `P` (item dentro de container) e 6 portas**, terminando em `31.zon:62`. | Testado (código) | contagem medida sobre `lib/world/zon/31.zon`; terminator em `lib/world/zon/31.zon:62` | Idem. |
| 117 | As lojas de Midgaard Norte são: **Wizard Shop Keeper** (3000, loja de magia), **Baker** (3001, padaria), **Grocer** (3002, mercearia — que vende o **Cashcard**), **Weaponsmith** (3003), **Armourer** (3004), **Pet Shop Boy** (3089), **Wally The Watermaster** (3009, água), **Bartender** (3040, Grunting Boar) e os garçons de guilda (3042-3045) e "Filthy" (3046). | Testado (código) | `lib/world/zon/30.zon:6`, `:12`, `:17`, `:24`, `:32`, `:139`, `:55`, `:73`, `:80-100`; cashcard em `:22` | `list` em cada loja e registrar o que é vendido (nomes PT-BR). |
| 118 | As margens de lucro são **por loja** (vêm do `.shp`), não do código: padaria 1.4/1.0; mercearia 1.5/0.4; armeiro 1.0/0.5; loja de magia 1.15/0.15; armas 1.3/0.4; barcos 1.2/0.9; bebidas 1.1/1.0; água 1.0/1.0; garçons 1.0-1.7. | Testado (código) | `lib/world/shp/30.shp:38-39` (padaria), `:65-66` (mercearia), `:134-135` (armadura), `:9-10` (magia), `:96-97` (armas), `:159-160` (barcos), `:234-235` (bebidas), `:207-208` (água), `:306` (1.7 no `#3044`) | `list` mostra o preço de venda; `value <item>` na mesma loja mostra o de compra. Comparar as razões entre lojas. |
| 119 | Fórmulas de preço: **compra** = `custo_do_objeto × profit_buy × (1 + (CHA_lojista − CHA_jogador)/70)`; **venda** = `custo × min(profit_sell × (1 − (CHA_lojista − CHA_jogador)/70), profit_buy × (1 + ...))`, com trava para não comprar mais caro do que vende. | Testado (código) | `src/shop.c:495-499`; `src/shop.c:505-514`; tabela comentada de carisma em `src/shop.c:474-493` (ex.: +10 → 1.1428; −10 → 0.8572) | Com dois personagens de CARISMA bem diferente, `list`/`value` na mesma loja e comparar os preços. |
| 120 | O lojista tem **dinheiro finito, mas com conta bancária**: se passa de `MAX_OUTSIDE_BANK` (15000) o excedente vai para o banco da loja; se cai abaixo de `MIN_OUTSIDE_BANK` (5000) ele saca do banco. Se nem banco + bolso bastam, ele recusa a compra. | Testado (código) | `src/shop.h:134-135` (`MIN_OUTSIDE_BANK 5000`, `MAX_OUTSIDE_BANK 15000`); `src/shop.c:627-629` (depósito), `:766-773` (recusa), `:808-811` (saque); bit `WILL_BANK_MONEY` em `src/shop.h:128`, `:131` | Vender itens caros repetidamente ao mesmo lojista até ele dizer que não pode pagar; registrar a mensagem `missing_cash1` (`src/shop.c:769`). |
| 121 | Vários lojistas de Midgaard têm o bit de banco ligado no `.shp` (segundo valor da linha final = `2` → `WILL_BANK_MONEY`), por exemplo a loja de magia e a loja dos barcos. | Testado (código) | `lib/world/shp/30.shp:23-24` (loja 3000: `0` e `2`), `:170-171` (loja 3006), `:192-193` (loja 3007); ordem dos campos em `src/shop.c:1209-1210`; bits em `src/shop.h:127-128` | Vender muito para a mesma loja e ver se ela continua comprando (se sim, tem banco). |
| 122 | Roubar numa loja é **impossível**: o lojista grita `"$n is a bloody thief!"` e **te dá um tapa** (executa o social `slap` em você). | Testado (código) | `src/shop.c:966-973`; `:969` (`MSG_NO_STEAL_HERE`); `src/shop.h:140` (`"$n is a bloody thief!"`); `:972` (`do_action(keeper, GET_NAME(ch), cmd_slap, 0)`) | `steal` de um lojista e registrar o grito + o tapa. |
| 123 | Lojista é **protegido**: atacá-lo faz o lojista te xingar (`MSG_CANT_KILL_KEEPER = "Get out of here before I call the guards!"`) e te dar um tapa, e o dano não acontece — a menos que a loja tenha o bit `WILL_START_FIGHT`. | Testado (código) | `src/shop.c:993-1015`; `:1005`, `:1008`, `:1011`; `src/shop.h:127` (`WILL_START_FIGHT (1 << 0)`), `:130`, `:145` | Bater (de leve) num lojista e registrar a recusa; **não** insistir. |
| 124 | As mensagens de erro das lojas são por loja e algumas são piadas: `"Are you drunk or what?? - NO CREDIT!"` (bebidas), `"Oh, bugger off, NO CREDIT!"` (bebidas 3046), `"I only buy armors.. Go away!"`, `"That is too expensive for me - Try a wizard!"`, `"You don't sound like a sailor - go away."` (barcos: na verdade `"I only trade ships."`). | Testado (código) | `lib/world/shp/30.shp:241`; `:362`; `:140`; `:141`; `:165` | `buy` um item inexistente e `sell` um item errado em cada loja; registrar as respostas. |
| 125 | Existe uma loja que **não vende para estranhos**: as mensagens são `"Sorry, you aren't on my list of people I can sell to."` / `"Sorry, I don't buy from outsiders."` (loja 3007, do barco). | Testado (código) | `lib/world/shp/30.shp:185-188` | `list`/`buy` nessa loja e registrar a recusa. |
| 126 | O `messages` de `lib/misc` **não** é mensagem de login: é o arquivo de **mensagens de dano de magias/habilidades** (12 linhas por registro: morte, erro, acerto e mensagem "god"), com exemplos literais como `"You burn $N with your hot little hands!"`. | Testado (código) | `lib/misc/messages:1-22` (cabeçalho explicativo), `:28-42` (Burning Hands), `:37` (exemplo); macros `MESS_FILE LIB_MISC"messages"` em `src/db.h:89` | Conjurar uma magia e comparar a mensagem com este arquivo (traduzido no DeBo). |
| 127 | As mensagens de login/MOTD ficam em **`lib/text/`**: `greetings`, `motd`, `imotd`, `news`, `info`, `credits`, `background`, `wizlist`, `immlist`, `policies`, `handbook` — mapeadas em `db.h`. | Testado (código) | `src/db.h:73-84`; `src/db.h:21` (`LIB_TEXT ":text:"`) e `:32` (`LIB_TEXT "text/"`) | No login, registrar o texto exibido e comparar com `lib/text/greetings`/`motd`. |
| 128 | O `motd` padrão diz `C I R C L E M U D 3 . 0` e traz a frase `"We addict players for their own enjoyment."` | Testado (código) | `lib/text/motd:5-6` | No login do DeBo, ver se esse texto foi traduzido ou substituído. |
| 129 | O `greetings` (tela de abertura) mostra a linha `"By what name do you wish to be known?"` e ainda o texto de "Based on CircleMUD 3.1". | Testado (código) | `lib/text/greetings:4`, `:11` | Registrar a tela de abertura do DeBo. |
| 130 | O `background` padrão é um **limerick**: `"There once was a guy who played MUDs / But the MUDs that he played were all duds / 'I'll write one,' said he. / And he brushed off his C. / And soon played his game with his buds."` | Testado (código) | `lib/text/background:3-7` | `background` no DeBo e registrar o texto (provavelmente traduzido ou trocado). |
| 131 | `policies` e `handbook` no mundo padrão são **placeholders** com piada: `"Bug the higher-ups to make some policies and write them in this file, lest a political disaster ensue..."` | Testado (código) | `lib/text/policies:3-7`; `lib/text/handbook:5-6` | Se o DeBo não traduziu/reescreveu, `policies`/`handbook` ainda dizem isso. Testável só por imortal. |
| 132 | Há **104 socials** no arquivo padrão, e o formato é `nome <min_victim_pos> <min_char_pos>` seguido das mensagens terminadas por `#`. | Testado (código) | `lib/misc/socials` (796 linhas; contagem de 104 registros medida sobre o arquivo; primeiro em `:1` `accuse 0 5`, exemplo completo em `:1-9`; terminator `#` em `:3`, `:24`, `:34`) | `socials`/`commands` no DeBo deve listar os socials disponíveis — comparar a contagem (traduzidos, mas provavelmente os mesmos nomes). |
| 133 | Socials engraçados/estranhos com mensagens literalmente citáveis: `beg` (`"You beg the gods for mercy.  (No way you're gonna get it! :-))"`), `fart` (`"$n lets off a real rip-roarer!"`), `burp`, `hiccup` (`*HIC*`), `purr` (`MMMMEEEEEEEEOOOOOOOOOWWWWWWWWWWWW.`), `snore` (`Zzzzzzzzzzzzzzzzz.`), `puke`, `spank` (`"You spank $M vigorously, long and hard.  Your hand hurts."`), `tango` (`$n puts a rose between $s teeth...`), `yodel`, `wiggle`. | Testado (código) | `lib/misc/socials:16-24` (beg), `:176-179` (fart), `:56-59` (burp), `:296-299` (hiccup), `:471-474` (purr), `:586-589` (snore), `:451-460` (puke), `:611-619` (spank), `:686-695` (tango), `:791-794` (yodel), `:761-764` (wiggle) | Rodar `fart`, `burp`, `hiccup`, `purr`, `spank <alvo>`, `tango`, `yodel` numa sessão autorizada e registrar as mensagens (traduzidas, se o DeBo traduziu). |
| 134 | Socials com **restrição de posição** (só funcionam de pé, nível de posição ≥ 5, ou exigem alvo "presente"): `accuse`, `bow`, `comfort`, `cry`, `cuddle`, `dance` (char ≥ 8), `drool`, `flirt`, `fondle`, `fume`, `glare`, `grope`, `hug`, `nuzzle`, `spank` (char ≥ 8), `stare`, `tackle`, `tango` (char ≥ 8), `thank`, `wink`, `worship`. | Testado (código) | `lib/misc/socials:1`, `:41`, `:86`, `:111`, `:121`, `:141`, `:156`, `:186`, `:196`, `:221`, `:241`, `:271`, `:301`, `:386`, `:611`, `:641`, `:676`, `:686`, `:706`, `:766`, `:776` | Sentado, tentar `spank <alvo>` e `dance`: devem exigir levantar. |
| 135 | Socials **sem** alvo dizem literalmente "quem?" de forma cômica: `sword`-like, `french` (`"French whom??"`), `fondle` (`"Who needs to be fondled?"`), `nibble` (`"Nibble on who?"`), `grope` (`"Whom do you wish to grope??"`), `nuzzle` (`"Nuzzle who??"`), `snowball` (`"Who do you want to throw a snowball at??"`). | Testado (código) | `lib/misc/socials:206-208` (french), `:196-198` (fondle), `:361-363` (nibble), `:271-273` (grope), `:386-388` (nuzzle), `:591-593` (snowball) | Rodar os socials sem argumento e registrar as respostas. |
| 136 | Comandos de mortal que quase ninguém usa, todos já no mundo padrão: `levels` (`src/interpreter.c:348`), `diagnose` (`:266`), `insult` (`:335`), `title` (`:490`), `toggle` (`:493`), `display` (`:267`), `color` (`:248`), `report` (`:420`), `split` (`:465`), `use` (`:505`), `where` (`:520`), `whoami` (`:519`). | Testado (código) | `src/interpreter.c:248`, `:266`, `:267`, `:335`, `:348`, `:420`, `:465`, `:490`, `:493`, `:505`, `:519`, `:520` | Rodar `levels`, `insult <alvo>`, `title <texto>`, `where`, `whoami`, `report`, `split`, `use` e registrar quais existem no DeBo. |
| 137 | Piada escondida no `do_where`: quando não encontra ninguém, o texto é `"You ain't nothin' but a hound-dog."` | Testado (código) | `src/act.informative.c:1416` | `where` numa sala vazia e registrar a frase. |
| 138 | `insult` é um comando separado dos socials, com mensagens próprias em `act.social.c` (linha 127). | Testado (código) | `src/act.social.c:127`; `src/interpreter.c:335` (`insult`, POS_RESTING, lvl 0) | `insult <alvo>` e registrar. |
| 139 | O `do_gen_ps`/`whoami` e o `do_commands` mostram informação de personagem/comandos; `users` e `syslog` são de imortal. | Testado (código) | `src/interpreter.c:519` (`whoami`), `:251` (`commands`), `:506` (`users`, `LVL_IMMORT`), `:478` (`syslog`, `LVL_IMMORT`) | `commands` e `socials`; os de imortal não são testáveis. |
| 140 | Skill barata de "segredo": em `do_gen_tog`/`do_display`/`do_toggle` o jogador muda flags de exibição pessoais (por exemplo esconder/diminuir saída espontânea); vale testar quais toggles o DeBo mantém. | Provável | `src/interpreter.c:267` (`display`), `:493` (`toggle`); `src/act.other.c:731-733` (`do_display`) | `toggle` sem argumento e registrar a lista exata (é a lista de flags do DeBo). |

## 2. Catálogo das special procedures

### 2.1 Tabela mestra (procedure → vnum → zona → gatilho → efeito)

Vnums são do **mundo padrão** e podem não existir no DeBo (traduzido e modificado). "Zona" vem do comentário da própria tabela ou do intervalo do vnum.

| Procedure (`src/spec_procs.c` etc.) | Mob/objeto/sala | Zona | Gatilho | Efeito | Easter egg? |
| --- | --- | --- | --- | --- | --- |
| `puff` `:500-523` | mob **1** (`spec_assign.c:94`) | 0 (imortal) | automático, a cada tick, 1/61 | 4 falas aleatórias (`:509`, `:512`, `:515`, `:518`) | **Sim** |
| `mayor` `:233-324` | mob **3105** (`spec_assign.c:120`) | 31 | relógio do jogo (6h/20h) | caminha, fala, tranca/destranca `gate` (`:237-240`, `:307-313`) | **Sim** |
| `dump` `:199-230` | **sala 3030** (`spec_assign.c:300`) + salas `ROOM_DEATH` (`:303-306`) | 30 | `drop` | destrói itens e paga XP (nv<3) ou ouro (`:216`, `:224-227`) | Não (mas é piada de "bom cidadão", `:221-222`) |
| `snake` `:360-372` | mobs 4000, 4001, 4053, 4102, 5300, 5301, 6113, 7006 (`spec_assign.c:123-125`, `:127`, `:134-135`, `:199`, `:191`) | 40, 53, 61, 70 | em combate, 1/(nível+1) | morde + `SPELL_POISON` (`:368-370`) | Não |
| `thief` `:375-389` | mobs 4103, 5304, 5305, 2511, 15015 (`spec_assign.c:128`, `:136-137`, `:152`, `:269`) | 41, 53, 25, 150 | automático com jogador na sala | rouba 1-10% do ouro (`npc_steal` `:332-354`) | Não |
| `magic_user` `:392-461` | dezenas de mobs (`spec_assign.c:126`, `:138-144`, `:147-188`, `:192-195`, `:198-210`, `:213-227`, `:232-242`, `:259-266`, `:270`, `:274-276`) | 25, 41, 50-54, 61, 63, 65, 70-72, 120, 150 | em combate | magia por nível (`:428-457`) + veneno/cegueira/drain (`:412-423`) | Não |
| `guild_guard` `:468-496` | mobs 3024-3027, **5005 (dragão de bronze)**, 5456-5459 (comentados) (`spec_assign.c:108-111`, `:214`, `:252-255`) | 30, 50, 54 | tentar mover para dentro da guilda | bloqueia (`:472`, `:490-491`) | Piada no dragão |
| `guild` `:154-195` | mobs 3020-3023 (`spec_assign.c:104-107`) | 30 | `practice` | ganho por INT (`:186-189`) | Não |
| `cityguard` `:575-639` | mobs 3059, 3060, 3067, 7900, 12018, 12021, 5434, 5461-5463, 5482, 6500 (`spec_assign.c:112-113`, `:117`, `:131`, `:240`, `:243-246`, `:260`, `:262`, `:273`) | 30, 31, 79, 54, 120, 65 | automático | ataca PK/ladrão; cospe em CHA baixo (`:591-601`, `:620-625`) | **Sim** (cuspida) |
| `fido` `:527-549` | mobs 3062, 3066 (`spec_assign.c:115-116`) | 30 | automático | devora cadáver, solta o conteúdo (`:535-544`) | Não |
| `janitor` `:553-572` | mobs 1202, 3061, 3068 (`spec_assign.c:99`, `:114`, `:118`) | 0, 30 | automático | pega lixo barato (`:561-567`) | Não |
| `pet_shops` `:644-705` | **sala 3031** (`spec_assign.c:301`), lê a sala 3032 | 30 | `list`, `buy` | vende mobs da sala dos fundos (`:651`, `:676`), preço nível×300 (`:642`) | **Sim** (comentário "Gross.", placa no bicho) |
| `bank` `:714-754` | **objetos 3034 (ATM) e 3036 (cashcard)** (`spec_assign.c:289-290`) | 30 | `balance`, `deposit`, `withdraw` | move ouro para o banco (`:733-734`, `:747-748`); sem juros | Não |
| `postmaster` (`src/mail.c:500-524`) | mobs 1201, 3010 (`spec_assign.c:98`, `:103`) | 0, 30 | `mail`, `check`, `receive` | custa 150 (`mail.h:23`), exige nível 2 (`mail.h:20`) | Não |
| `gen_board` (`src/boards.c:154-185`) | objetos 3096-3099 (`spec_assign.c:284-287`) | 30 | `look`/`read`/`write`/`remove` | mural com níveis por placa (`boards.c:66-71`) | Não |
| `shop_keeper` (`src/shop.c:939-990`) | atribuído dinamicamente pelo `.shp` (`shop.c:1211-1213`, `:1255-1258`) | 30, 31, 25, 120, 150, 33, 54, 65 | `list`, `buy`, `sell`, `value`, `steal` | preços e tapa (`:966-988`) | Piadas nas mensagens (`30.shp:241`, `:362`) |
| `receptionist` (`src/objsave.c:1142-1145`) | mobs 1200, 3005, 5404 (`spec_assign.c:97`, `:102`, `:231`) | 0, 30, 54 | `rent`, `offer` | aluguel + sociais aleatórios (`objsave.c:1066-1072`) | **Sim** (fart/burp aleatórios) |
| `cryogenicist` (`src/objsave.c:1148-1151`) | mob 3095 (`spec_assign.c:119`) | 30 | `rent`, `offer` | congela o personagem (fator 4) | Não |
| `CastleGuard` (`src/castle.c:749-755`) | offsets 0, 3-11, 27-29 da zona 150 (`castle.c:128-152`) | 150 | combate no castelo | `banzaii` (`:307-308`) | **Sim** (grito BANZAII) |
| `king_welmar` (`src/castle.c:444-556`) | offset 1 da zona 150 (`castle.c:130`) | 150 | 8h/12h/21h do jogo | anda, senta no trono, **monólogo em latim**, `fry_victim` | **Sim** |
| `peter` (`:779-839`) | offset 12 (`:140`) | 150 | automático | inspeciona guardas, broncas (`:818`, `:825`, `:832`) | **Sim** |
| `training_master` (`:566-649`) | offset 13 (`:141`) | 150 | automático | treina Brian e Mick (`:579`, `:582`) | **Sim** |
| `James` (`:701-704`) | offset 16 (`:142`) | 150 | automático | reclama do lixo (`:721-723`) | **Sim** |
| `cleaning` (`:738-741`) | offset 17 (`:143`) | 150 | automático | limpa sem reclamar | Não |
| `tim` (`:657-660`) / `tom` (`:652-655`) | offsets 20/21 (`:144-145`) | 150 | automático | gêmeos que se socorrem; bloqueiam a porta do rei (`:665-692`) | **Sim** |
| `DicknDavid` (`:763-772`) | offsets 24/25 (`:146-148`) | 150 | tentar ir ao tesouro | bloqueia (`:771`) | Não |
| `jerry` (`:846-925`) | offset 26 (`:149`) | 150 | automático | joga dados com Michael (`:862`, `:874-923`) | **Sim** |

### 2.2 Fichas com as strings literais

Estas são as strings exatas do engine padrão (o DeBo é PT-BR, então a **tradução provavelmente difere**; o que se valida no jogo é o *comportamento*, a *probabilidade* e a *ordem*).

**Puff (mob 1) — `spec_procs.c:500-523`**

| Fala | Linha |
| --- | --- |
| `My god!  It's full of stars!` | `spec_procs.c:509` |
| `How'd all those fish get up here?` | `spec_procs.c:512` |
| `I'm a very female dragon.` | `spec_procs.c:515` |
| `I've got a peaceful, easy feeling.` | `spec_procs.c:518` |

Chance: `rand_number(0, 60)` → só os casos 0-3 falam (`:507-519`). Descrição do mob: "contemplating a higher reality" (`lib/world/mob/0.mob:4`).

**Prefeito (mob 3105) — `spec_procs.c:233-324`**

| Evento | String | Linha |
| --- | --- | --- |
| acorda | `$n awakens and groans loudly.` | `:271` |
| dorme | `$n lies down and instantly falls asleep.` | `:276` |
| `a` | `$n says 'Hello Honey!'` + `$n smirks.` | `:280-281` |
| `b` | `$n says 'What a view!  I must get something done about that dump!'` | `:285` |
| `c` | `$n says 'Vandals!  Youngsters nowadays have no respect for anything!'` | `:290` |
| `d` | `$n says 'Good day, citizens!'` | `:295` |
| `e` | `$n says 'I hereby declare the bazaar open!'` | `:299` |
| `E` | `$n says 'I hereby declare Midgaard closed!'` | `:303` |

**Banco — `spec_procs.c:714-754`**

| Ação | String | Linha |
| --- | --- | --- |
| saldo > 0 | `Your current balance is %d coins.` | `:720` |
| saldo 0 | `You currently have no money deposited.` | `:722` |
| depósito ok | `You deposit %d coins.` | `:735` |
| depósito sem ouro | `You don't have that many coins!` | `:730` |
| saque ok | `You withdraw %d coins.` | `:749` |
| saque sem saldo | `You don't have that many coins deposited!` | `:744` |
| terceiros veem | `$n makes a bank transaction.` | `:736`, `:750` |

**Correio — `src/mail.c:500-598`** (`mail.h:20`, `mail.h:23`)

| Situação | String | Linha |
| --- | --- | --- |
| nível baixo | `$n tells you, 'Sorry, you have to be level %d to send mail!'` | `mail.c:534` |
| sem destinatário | `$n tells you, 'You need to specify an addressee!'` | `mail.c:541` |
| sem ouro | `$n tells you, 'A stamp costs %d coin%s.'` + `'...which I see you can't afford.'` | `mail.c:546-547` |
| nome desconhecido | `$n tells you, 'No one by that name is registered here!'` | `mail.c:553` |
| cobrança | `$n tells you, 'I'll take %d coins for the stamp.'` + `'Write your message, use @ on a new line when done.'` | `mail.c:558-559` |
| tem carta | `$n tells you, 'You have mail waiting.'` | `mail.c:576` |
| não tem | `$n tells you, 'Sorry, you don't have any mail waiting.'` | `mail.c:578` |
| correio off | `Sorry, the mail system is having technical difficulties.` | `mail.c:509` |

**Murais — `src/boards.c`**

| Situação | String | Linha |
| --- | --- | --- |
| nível insuficiente | `You are not holy enough to write on this board.` | `:195` |
| cheio | `The board is full.` | `:199` |
| avaria | `The board is malfunctioning - sorry.` | `:203` |
| sem título | `We must have a headline!` | `:215` |
| instrução | `Write your message.  Terminate with a @ on a new line.` | `:227` |
| terceiros | `$n starts to write a message.` | `:228` |
| remoção | `$n just removed message %d.` | `:425` |
| cabeçalho | `(%s)` com o nome do autor + data (`%6.10s %-12s :: %s`) | `:222-223` |
| lore do objeto | `Use 'look board' to read the board.` | `lib/world/obj/30.obj:545` |

**Loja — `src/shop.c`**

| Situação | String | Linha |
| --- | --- | --- |
| roubo | `MSG_NO_STEAL_HERE` = `$n is a bloody thief!` | `shop.h:140`; uso `shop.c:969` |
| atacar lojista | `MSG_CANT_KILL_KEEPER` = `Get out of here before I call the guards!` | `shop.h:145`; uso `shop.c:1008` |
| sem poder pagar | `missing_cash1` (por loja, ex. `"That is too expensive for me!"`) | `shop.c:769`; `30.shp:19` |
| fora do horário | `MSG_NOT_OPEN_YET`, `MSG_NOT_REOPEN_YET`, `MSG_CLOSED_FOR_DAY` | `shop.h:137-139` |
| classe/alinhamento errado | `MSG_NO_SELL_CLASS`, `MSG_NO_SELL_ALIGN` | `shop.h:142-143` |
| varinha gasta | `MSG_NO_USED_WANDSTAFF` | `shop.h:144` |
| invisível | `MSG_NO_SEE_CHAR` | `shop.h:141` |

**Recepcionista / criogenicista — `src/objsave.c:1062-1151`**

| Situação | String | Linha |
| --- | --- | --- |
| aluguel grátis | `Rent is free here.  Just quit, and your objects will be saved!` | `:1091` |
| preço do aluguel | `Rent will cost you %d gold coins per day.` | `:1102` |
| preço do cryo | `It will cost you %d gold coins to be frozen.` | `:1104` |
| prazo | `You can rent for %ld day%s with the gold you have on hand and in the bank.` | `:963-964` |
| sem dinheiro | `...which I see you can't afford.` | `:1108` |
| guarda-roupa | `$n stores your belongings and helps you into your private chamber.` | `:1116` |
| cryo | `A white mist appears in the room, chilling you to the bone...` / `You begin to lose consciousness...` | `:1122-1123` |

**Cirurgia de preço — `src/shop.c:474-514`.** Tabela de ajuste por diferença de CARISMA documentada no próprio código: com o lojista 10 pontos mais carismático, multiplicador 1.1428; com o jogador 10 pontos acima, 0.8572 (`shop.c:483`, `:486`). Ou seja: **CARISMA compra desconto real** (até ~21% de diferença entre extremos).

## 3. Subsistemas jogáveis

### 3.1 Banco / ATM

- O "banco" é um **objeto**, não um NPC: `bank` é atribuído a `ASSIGNOBJ(3034, bank)` e `ASSIGNOBJ(3036, bank)` (`src/spec_assign.c:289-290`).
- Objeto 3034 = `atm teller bank machine~` / "an automatic teller machine" (`lib/world/obj/30.obj:209-212`), tipo `ITEM_OTHER` 12 (`:214`; `src/structs.h:305`), com lore ensinando os comandos (`lib/world/obj/30.obj:221-222`). Objeto 3036 = `cashcard` (`lib/world/obj/30.obj:240-243`), dado pelo Grocer a cada reset (`lib/world/zon/30.zon:22`) — um **cartão de banco portátil**, que é a parte mais "secreta" e interessante: se o DeBo mantiver, dá para usar `balance`/`deposit`/`withdraw` carregando o cartão, longe do ATM.
- ATM instalado em 6 salas no reset: `O 0 3034 10 3001` (Templo), e mais 3008, 3004, 3017, 3021, 3027 (`lib/world/zon/30.zon:150-161`).
- **Sem juros e sem taxa** (não há nenhuma ocorrência em `src/spec_procs.c:714-754`).
- Fora de um ATM, os três comandos respondem `"Sorry, but you cannot do that here!"` (`src/act.other.c:138-141`), porque na tabela eles apontam para `do_not_here` (`src/interpreter.c:227`, `:265`, `:528`).

### 3.2 Correio

- `postmaster` intercepta `mail`, `check`, `receive` (`src/mail.c:505-523`); custa **150 moedas** (`src/mail.h:23`), nível mínimo **2** (`src/mail.h:20`), carta até 4096 chars (`src/mail.h:26`), terminada com `@` (`src/mail.c:559`).
- O correio do mundo padrão é o mob **3010** na sala 3062 "The Post Office" (`src/spec_assign.c:103`; `lib/world/zon/30.zon:60`; `lib/world/wld/30.wld:1303`), com um segundo na zona imortal (mob 1201, `src/spec_assign.c:98`).
- A carta recebida é um objeto do tipo note (`src/mail.c:596-600`).

### 3.3 Murais

- 4 murais (`src/boards.c:66-71`), 60 mensagens cada, 4096 chars (`src/boards.h:12-13`), título truncado em 80 (`src/boards.c:211-212`).
- Persistência em `lib/etc/board.mort|immort|freeze|social` (`src/boards.c:67-70`; `src/db.h:24`, `:35`).
- Níveis por placa (`src/boards.c:67`, `:70`); o **social board** (3096) aparece 5 vezes em Midgaard (`lib/world/zon/30.zon:165-172`) e o **mortal board** (3099) na Reading Room (`lib/world/zon/30.zon:164`).
- Peculiaridade útil: o verbo é sempre `read`/`look`/`write`/`remove` — o mesmo `remove` de equipamento (`src/interpreter.c:414`, `:418`, `:535`).

### 3.4 Casa e aluguel

- **Casa** (house): 100 casas, 10 convidados (`src/house.h:1-2`), controle em `lib/etc/hcontrol` (`src/db.h:96`), objetos em `lib/house/<vnum>.house` (`src/house.c:55`; `src/db.h:39`). Entrada só para dono/convidados/GRGOD (`src/house.c:570-587`).
- Comando de mortal: `house` (POS_RESTING) para gerir convidados (`src/interpreter.c:327`; `src/house.c:511-548`).
- Comando de imortal: `hcontrol build|destroy|pay|show` (`src/interpreter.c:319`; `src/house.c:497-503`), com `"House built.  Mazel tov!"` (`src/house.c:422`).
- **Aluguel** (rent) e **criogenia** (cryo): recepcionista = fator 1, criogenicista = fator 4 (`src/objsave.c:24-25`); custo = `min_rent_cost` (100, `src/config.c:139`) × fator + soma de `GET_OBJ_RENT` dos itens (`src/objsave.c:995`, `:1023`); cobrado por dia real (`src/objsave.c:1102`); sem retirada no prazo, os itens são apagados (10 e 30 dias: `src/config.c:158`, `:161`).
- Padrão vem com **aluguel grátis** (`src/config.c:133`), e nesse caso a resposta é `"Rent is free here..."` (`src/objsave.c:1090-1094`).

### 3.5 Castelo e reino

- Nesta árvore, o "reino" é o **King's Castle** (zona 150, `src/castle.c:31`), com ~20 NPCs com procedures (ver §2.1). **Não existe** comando `castle` de clã/guilda: `castle.c` é só comportamento de NPC (cabeçalho em `src/castle.c:1-10`) e a tabela de comandos não tem `castle`.
- Mecânicas "de reino" efetivamente presentes: guardas que bloqueiam direções (`block_way`, `src/castle.c:352-369`), tesouro guardado por Dick e David (`:771`), o rei que dorme/acorda/senta no trono e faz monólogo (`:444-556`), `banzaii` coletivo (`:300-311`), e o mordomo/limpeza recolhendo lixo (`:701-741`).
- Se o DeBo tiver "castelo" de jogadores (claim/aluguel/guarda), é acréscimo posterior ao 3.x padrão.

## 4. Morte — o que se perde, o que fica, o que acontece ao voltar

Resumo do fluxo, tudo citado: `damage()` reduz HP com teto de 100 por golpe (`src/fight.c:737`), `update_pos` decide o estado (`:198-212`), ao chegar a `POS_DEAD` o matador recebe XP (`:821-827`) e chama `die()` (`:834`), que **subtrai metade do XP total** (`:380`), limpa flags de PK/ladrão (`:382`) e chama `raw_kill()` (`:383`); `raw_kill` para o combate, remove todos os affects, grita o death cry, cria o cadáver e extrai o personagem (`:362-374`).

| Pergunta | Resposta no código | Fonte |
| --- | --- | --- |
| Quanto de XP se perde? | **50% do XP total acumulado** | `src/fight.c:378-380` |
| Perde nível? | **Não** — a perda só subtrai XP; o laço que rebaixa nível não existe no ramo negativo | `src/limits.c:265-274`, `:287-292` |
| Pode ficar com XP negativo? | Não, o piso é 0 | `src/limits.c:290-291` |
| O que vai para o corpo? | **Inventário inteiro**, **todo o equipamento** e **todo o ouro** | `src/fight.c:304-312`, `:314-328` |
| Pode guardar coisas no corpo? | Não: `GET_OBJ_VAL(corpse, 0) = 0` com o comentário `/* You can't store stuff in a corpse */` | `src/fight.c:294` |
| Peso e aluguel do corpo | peso = peso do dono + carga; `GET_OBJ_RENT(corpse) = 100000` | `src/fight.c:296-297` |
| Quanto tempo o corpo fica? | 5 ticks (NPC) / 10 ticks (jogador) | `src/fight.c:298-301`; `src/config.c:76-77` |
| Alguém é avisado? | Sim, a sala e as salas vizinhas ouvem o grito de morte | `src/fight.c:349-358` |
| O que o morto vê? | `You are dead!  Sorry...`; a sala vê `$n is dead!  R.I.P.` | `src/fight.c:782-785` |
| Perde comando/trava? | A extração é adiada (`PLR_NOTDEADYET`), processada no fim do tick | `src/handler.c:961-969`, `:982-1015`; `src/fight.c:681` |
| Onde volta? | A árvore não muda a sala de retorno na morte; o retorno usa o loadroom normal do personagem (`GET_LOADROOM`), definido no aluguel (`src/objsave.c:1132`) | `src/objsave.c:1132`; `src/db.c:2788` |

**Ouro do matador:** se o matador não tem grupo, `solo_gain` (`src/fight.c:444-465`); se tem, `group_gain` divide (`:405-441`). Golpes também rendem XP: `GET_LEVEL(vítima) * dano` (`:741-742`).

## 5. Zonas — números medidos

Todos os números abaixo foram medidos **nos arquivos deste mirror**, por dois métodos independentes (contagem de blocos `#<vnum>` e de linhas `S` terminadoras) quando aplicável. **Vnums e contagens são do mundo padrão e podem não existir no DeBo.**

| Zona | Arquivo de reset | Faixa de vnums | Salas (`.wld`) | Resets M | O | G | E | P | D | Resets no `.zon` | Terminator |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 30 — Northern Midgaard Main City | `lib/world/zon/30.zon:1-3` | 3000-3099 | **59** (`30.wld`) | 55 | 12 | 62 | 24 | 0 | 0 | R=12 | `30.zon:174` |
| 31 — Southern part of Midgaard | `lib/world/zon/31.zon:1-3` | 3100-3299 | **54** (`31.wld`) | 20 | 9 | 6 | 5 | 2 | 6 | R=4 | `31.zon:62` |
| 36 — The Chessboard of Midgaard | `lib/world/zon/36.zon:1-3` | 3600-3699 | **67** (`36.wld`) | 32 | 2 | 2 | 48 | 0 | 4 | — | `36.zon:99` |
| 70 — The Sewer, First Level | `lib/world/zon/70.zon:1-3` | 7000-7099 | **62** (`70.wld`) | 12 | 0 | 0 | 0 | 0 | 2 | — | `70.zon:22` |
| 71 — The Second Sewer | `lib/world/zon/71.zon:1-3` | 7100-7199 | **26** (`71.wld`) | 10 | 0 | 0 | 0 | 0 | 6 | — | `71.zon:24` |
| 72 — The Sewer Maze | `lib/world/zon/72.zon:1-3` | 7200-7299 | **87** (`72.wld`, que também contém as salas 7300-7345 da zona 73) | 23 | 4 | 2 | 11 | 0 | 10 | R=2 | `72.zon:61` |
| 73 — The Tunnels In The Sewer | `lib/world/zon/73.zon:1-3` | 7300-7399 | (não há `73.wld`) | 8 | 0 | 0 | 0 | 0 | 13 | — | `73.zon:29` |
| 186 — Newbie Zone ("Created by Maynard of StrangeMUD") | `lib/world/zon/186.zon:1-5` | 18600-18699 | **41** (`186.wld`) | 24 | 0 | 2 | 14 | 0 | 14 | — | `186.zon:64` |

Notas:

- **Frequência de reset** (linha 3 de cada `.zon`, formato `<bot> <top> <freq> <lifespan>`): 15 min para zona 30; 40 para 31; 10 para 36; 15 para 70; 20 para 71; 25 para 72 e 73; 10 para 186 — com lifespan 2 (2 exceto a 36, que tem 1).
- A **Zona dos Novatos** tem 41 salas em dois blocos: 18600-18612 (13) e 18620-18647 (28), com 101 registros de saída (`D`) nos resets (`186.zon:48-62`).
- O **tabuleiro** tem 67 salas = 64 casas + entrada (3600) + 2 tesouros (3665, 3666) e **32 peças** (ver tabela de afirmações #93-#97).
- Os **esgotos** somam 175 salas em três arquivos; a zona 73 compartilha o `72.wld`.

## 6. Lojas de Midgaard — o que vendem

As lojas são definidas em `lib/world/shp/*.shp` (formato carregado em `src/shop.c:1190-1228`), com **margens por loja** e **estoque por lista de objetos**. O que o mob carrega no reset está em `30.zon`/`31.zon`.

| Loja (`#vnum` no `.shp`) | Dono (mob) | Sala | Estoque/produção | profit_buy / profit_sell | Fonte |
| --- | --- | --- | --- | --- | --- |
| 3000 — loja de magia | Wizard Shop Keeper (3000) | 3033 (The Magic Shop) | 3050-3054: Scroll of Identify, Yellow Potion, Scroll of Recall, Grey Wand, Gnarled Staff; aceita SCROLL/WAND/STAFF/POTION | 1.15 / 0.15 | `30.shp:2-32`; `30.zon:6-11` |
| 3001 — padaria | Baker (3001) | 3009 (The Bakery) | Waybread, Loaf of Bread, Danish Pastry | 1.4 / 1.0 | `30.shp:33-57`; `30.zon:12-16` |
| 3002 — mercearia | Grocer (3002) | 3010 (The General Store) | 3030-3033, 3036: Torch, Lantern, Bag, Box, **Cashcard**; compra LIGHT/TREASURE/CONTAINER | 1.5 / 0.4 | `30.shp:58-87`; `30.zon:17-22` |
| 3003 — armaria | Weaponsmith (3003) | 3011 (The Weapon Shop) | 3020-3025: Dagger, Small/Long Sword, Wooden Club, Warhammer, Flail; só compra WEAPON | 1.3 / 0.4 | `30.shp:88-116`; `30.zon:24-31` |
| 3004 — armaduras | Armourer (3004) | 3020 (The Armory) | 3040-3046, 3070-3086: peitorais, escudo, jaquetas, manoplas, capacetes, leggings, sleeves | 1.0 / 0.5 | `30.shp:117-154`; `30.zon:32-48` |
| 3006 — barcos | Captain (3006) / Sailor (3007) | 3049 (The Levee) | Raft, Canoe (tipos BOAT) | 1.2 / 0.9 | `30.shp:155-179`; `30.zon:51-54` |
| 3007 — barracão do cais | (dono 3007) | 3050 (The Deserted Warehouse) | não vende a estranhos | 1.0 / 1.0 | `30.shp:180-201` |
| 3009 — água | Wally The Watermaster (3009) | 3058 (Ye Olde Water Shoppe) | Water Cup, Bottle, Canteen, Barrel | 1.0 / 1.0 | `30.shp:202-226`; `30.zon:55-59` |
| 3040 — bar (Grunting Boar) | Bartender (3040) | 3007 | Beer Barrel/Bottle, Dark Ale, Firebreather, Local Bottle | 1.1 / 1.0 | `30.shp:227-253`; `30.zon:73-79` |
| 3042-3046 — bares de guilda/tavernas | Waiters (3042-3045) e Filthy (3046) | 3018, 3044, 3045, 3046... | cervejas de guilda | 1.0 a 1.7 / 1.0 | `30.shp:254-374`; `30.zon:80-100` |
| 3100 — casa de chá | Maid (3100) | 3106 (Park Cafe) | Cup of Tea, Cup of Coffee, Cup of Water | 1.1 / 0.9 | `31.shp:2-26`; `31.zon:17-20` |

Extras de Midgaard que valem teste:

- **Fonte** no Templo: objeto 3035 em 3005, tipo `ITEM_FOUNTAIN` 23, com 9999 unidades (`lib/world/obj/30.obj:225-232`; `lib/world/zon/30.zon:148-149`).
- **Fonte** no parque: objeto 3113 em 3141, mais uma pilha de **20 Coins** (3114) ao lado (`lib/world/obj/31.obj:172-191`; `lib/world/zon/31.zon:49-51`).
- Cofre e mesa do prefeito: `Desk` (3109) com `Key To Safe` dentro, `Safe` (3110) com `Money` dentro (`lib/world/zon/31.zon:39-42`) — o "segredo" do ouro da prefeitura, protegido pelo `Chief Guard` e `Mad Guards` (`31.zon:23-28`).
- Banco dos guardas: `Key To HQ` é dado no reset dos cityguards (`lib/world/zon/31.zon:8`) e o `Chief Guard` carrega `Key To The Desk` (`:24`).
- O `Sexton` carrega a `Key To Graveyard` (`lib/world/zon/31.zon:22`), e há portas de cemitério/capela (`:57-60`).
- O `Beggar` carrega a `Sewer Key` (`lib/world/zon/30.zon:129`) — a chave que liga Midgaard aos esgotos.

## 7. Curiosidades e coisas que quase ninguém vê

1. **`lib/misc/messages` não é login/MOTD.** É o arquivo de mensagens de **dano** (`db.h:89`), com 887 linhas e piadas como `"You burn $N with your hot little hands!"` (`messages:37`). MOTD/login estão em `lib/text/` (`db.h:75-84`).
2. **Todos os textos padrão de `lib/text` são placeholders de desenvolvedor** — `policies:6-7` e `handbook:5-6` mandam "importunar os superiores" para escrever as regras. Num MUD em produção, isso quase sempre foi substituído.
3. **O `background` padrão é um limerick** (`lib/text/background:3-7`).
4. **`greetings` e `imotd` dizem 3.1, `motd` e `credits` dizem 3.0** (`greetings:4`, `imotd:3`, `motd:5`, `credits:3`) — sinal de que a árvore foi montada misturando versões.
5. **104 socials**, incluindo `yodel`, `tango`, `spank`, `purr`, `snowball`, `french`, `grope`, `puke`, `bleed`, `daydream`, `worship` (lista completa com linhas em §8 e na tabela #132-#135).
6. **Bichos de estimação podem ser renomeados** e ganham placa no pescoço (`spec_procs.c:685-686`); não podem carregar nada (`:694-695`).
7. **O prefeito xinga o lixão** ("What a view! I must get something done about that dump!") ao passar, e o lixão de Midgaard **paga** por itens jogados (`spec_procs.c:216`, `:285`).
8. **O guarda cospe em quem é feio** (`spec_procs.c:620-625`).
9. **A recepcionista peida sozinha** (`objsave.c:1066-1072` contém `fart` na lista de emotes aleatórios).
10. **O mordomo do castelo reclama da faxineira** que deveria estar fazendo o trabalho (`castle.c:721-722`).
11. **O rei do castelo faz um monólogo em latim** todos os dias ao meio-dia do jogo (`castle.c:448-453`, `:472`).
12. **Dois irmãos gêmeos (Tim e Tom) se socorrem** e empurram quem tenta entrar no quarto do rei (`castle.c:665-692`).
13. **Loja que tapa o ladrão** (`shop.c:966-973`).
14. **Loja que se recusa a vender para "estranhos"** (`30.shp:185-188`).
15. **`where` responde com letra de Elvis**: `"You ain't nothin' but a hound-dog."` (`act.informative.c:1416`).
16. **`consider` em outro jogador** responde `"Would you like to borrow a cross and a shovel?"` (`act.informative.c:1469`).
17. **`wimpy` tem piadas embutidas**: `"Heh, heh, heh.. we are jolly funny today, eh?"` (`act.other.c:713`) e `"(sure, sure...)"` (`:706`).
18. **Leftover de código**: `SPECIAL(guild)` declarado e nunca usado em `castle.c:72`.
19. **Duas portas "False Door"** nos túneis dos esgotos (`73.zon:23-24`) e três passagens secretas nomeadas (`71.zon:21`, `73.zon:15`, `73.zon:25`).
20. **Não existe sino** no mundo padrão (tabela #108) — se o DeBo tem um, é criação local e ótimo alvo de "segredo".

## 8. Lista completa de socials por linha

Contagem: **104** (`lib/misc/socials`, 796 linhas). Nome @ linha:

`accuse`@1, `applaud`@11, `beg`@16, `bleed`@26, `blush`@31, `bounce`@36, `bow`@41, `brb`@51, `burp`@56, `cackle`@61, `chuckle`@66, `clap`@71, `comb`@76, `comfort`@86, `cough`@96, `cringe`@101, `cry`@111, `cuddle`@121, `curse`@131, `curtsey`@136, `dance`@141, `daydream`@151, `drool`@156, `embrace`@166, `fart`@176, `flip`@181, `flirt`@186, `fondle`@196, `french`@206, `frown`@216, `fume`@221, `gasp`@231, `giggle`@236, `glare`@241, `greet`@251, `grin`@261, `groan`@266, `grope`@271, `grovel`@281, `growl`@291, `hiccup`@296, `hug`@301, `kiss`@311, `laugh`@321, `lick`@326, `love`@336, `massage`@346, `moan`@356, `nibble`@361, `nod`@371, `nudge`@376, `nuzzle`@386, `pat`@396, `peer`@406, `point`@411, `poke`@421, `ponder`@431, `pout`@436, `pray`@441, `puke`@451, `punch`@461, `purr`@471, `roll`@476, `ruffle`@486, `scream`@496, `shake`@501, `shiver`@511, `shrug`@516, `sigh`@521, `sing`@526, `slap`@531, `smile`@541, `smirk`@551, `snap`@556, `snarl`@561, `sneeze`@571, `snicker`@576, `sniff`@581, `snore`@586, `snowball`@591, `snuggle`@601, `spank`@611, `spit`@621, `squeeze`@631, `stare`@641, `steam`@651, `stroke`@656, `strut`@666, `sulk`@671, `tackle`@676, `tango`@686, `taunt`@696, `thank`@706, `think`@716, `tickle`@726, `twiddle`@736, `wave`@741, `whine`@751, `whistle`@756, `wiggle`@761, `wink`@766, `worship`@776, `yawn`@786, `yodel`@791.

## 9. Testes baratos para sessão autorizada

Ordenados por custo/benefício. Todos cabem numa sessão curta, dentro do teto de conexões do ciclo. Registre **a resposta literal** e a hora/período do jogo (`time`) quando o comportamento for agendado.

1. **Comando-sonda (30 s).** `balance` longe de um ATM → esperado `"Sorry, but you cannot do that here!"` (ou tradução). Prova que o comando é `do_not_here` (#34).
2. **Banco (2 min).** No Templo/ATM: `balance`, `deposit 1`, `balance`, `withdraw 1`. Registrar se há taxa/juros (esperado: nenhum, #33). Repetir com o **cashcard** no inventário, em outra sala, para confirmar se o cartão funciona como banco portátil (§3.1).
3. **Correio (2 min).** `check` na agência; `mail <nome>` com 150+ moedas; registrar o preço cobrado e a instrução de `@` (#36). Sem ouro, registrar a recusa.
4. **Mural (2 min).** `look board` no mural da Reading Room; `write` um título curto e terminar com `@`; relogar e confirmar persistência (#40, #43). Tentar `remove 1 board`.
5. **Loja — preço e margem (5 min).** Em 3 lojas (padaria, armeria, magia): `list` e `value` de um item do próprio inventário. Calcular as razões e comparar com `30.shp` (#118-#119). Registrar mensagens de recusa (`buy` inexistente, `sell` errado) para capturar as piadas traduzidas (#124).
6. **Loja — lojista sem dinheiro (5 min).** Vender itens de valor crescente ao mesmo lojista até ele recusar; registrar a mensagem e quantas vendas aguentou (testa `MIN/MAX_OUTSIDE_BANK`, #120-#121).
7. **Loja — roubo e agressão (1 min).** `steal` um lojista → esperado grito + tapa (#122). **Não** atacar lojista.
8. **Fido (3 min).** Matar um NPC barato perto de um cachorro em Midgaard e ver o corpo ser devorado e os itens caírem no chão (#12).
9. **Janitor (2 min).** Largar um item barato e um caro no chão perto do faxineiro; ver qual ele pega (#14).
10. **Dump (2 min).** Ir ao lixão (`The Dump`) e `drop` um item barato; registrar o pagamento em ouro ou XP (#16).
11. **Guarda e CARISMA (5 min).** Com personagem de CARISMA baixo, ficar perto de um cityguard e esperar a cuspida (#9). Registrar a mensagem.
12. **Prefeito (agendado).** Antes das 6h e das 20h do jogo, ficar na rota; registrar as falas e a abertura/fechamento do portão (#4-#6).
13. **`consider` (3 min).** Contra mob de nível muito abaixo, igual, e muito acima; e contra outro jogador (#87). Registrar a escala completa.
14. **`wimpy` (2 min).** `wimpy` (sem arg), `wimpy <metade+1>` (recusa), `wimpy 1`, entrar em combate perdido e ver a fuga automática (#88-#90).
15. **Socials baratos (5 min).** `fart`, `burp`, `hiccup`, `purr`, `snore`, `yodel`, `wiggle`, `bounce`; depois `spank <alvo>`, `tango <alvo>`, `grope <alvo>` e os mesmos sem alvo (para capturar as respostas "quem?" — #133-#135).
16. **Comandos raros (3 min).** `levels`, `insult <alvo>`, `title <texto>`, `where` numa sala vazia (esperado: hound-dog), `whoami`, `report`, `split`, `use`, `toggle` (listar flags), `color` (#136-#140).
17. **Tabuleiro de xadrez (15 min).** Contar casas (64) e peças (32); conferir nome das peças e equipamentos; se possível matar um peão e ver a armadura; a chave/tesouro dos reis (#93-#97). **Alto risco de morte** — `consider` antes.
18. **Esgotos (15 min).** Contar salas por nível e conferir as 4 zonas; procurar as portas "falsas"/secretas (#98-#103). Registrar a porta do poço (`The Old Well`/`Down The Old Well`, #104).
19. **Fontes (2 min).** `drink fountain` e `fill <recipiente> fountain` nas duas fontes; ver a pilha de 20 moedas no parque após um reset (#105-#107).
20. **Zona dos Novatos (10 min).** Contar salas (41) e conferir nomes; ler a dedicatória a Maynard na sala da estátua; matar um "novato" e ver o equipamento (#109-#113).
21. **Recepcionista/Criogenicista (5 min).** Ficar parado ao lado da recepcionista e anotar os emotes aleatórios (esperado: inclui peido); `offer` para ver a cotação; `rent` para ver se é grátis (#51-#56).
22. **Castelo (se alcançável, 20 min).** Assistir ao monólogo do rei às 12h; ver o mordomo e a limpeza recolhendo lixo; ver Peter inspecionando guardas; ver Jerry e Michael jogando dados; tentar entrar no quarto do rei e no tesouro (#62-#73).

## 10. Limites desta pesquisa

1. **Nenhuma verificação ao vivo.** Todas as linhas são **Testado (código)** ou **Provável**. Nada foi confirmado no DeBo. Nenhuma linha deste arquivo pode ser promovida a "Testado (servidor)" sem sessão registrada.
2. **Versão.** O DeBo se declara CircleMUD **3.0**; este mirror é o commit `12a0ced` rotulado **3.1** (2012-03-22) e mistura rótulos 3.0/3.1 dentro de `lib/text`. Estrutura de subsistemas é compatível, mas detalhes de código 3.1 (extração adiada `PLR_NOTDEADYET`, `aggressive_mob_on_a_leash`) podem não existir num 3.0 puro — e vice-versa.
3. **Tradução.** O DeBo é PT-BR: **todas as strings literais citadas aqui provavelmente aparecem traduzidas**. O que se valida no jogo é a *mecânica* (probabilidade, fórmula, ordem, quem faz o quê), não o texto inglês.
4. **Mundo modificado.** Todos os vnums (mobs, objetos, salas) e todas as contagens de zona são do **mundo padrão** deste mirror. O DeBo pode ter renumerado, removido ou acrescentado conteúdo. Vnum padrão **não** é prova de existência no DeBo.
5. **Divergência interna.** A contagem de salas de Midgaard neste arquivo (zona 30 = 59, zona 31 = 54, por dois métodos) difere do que o arquivo irmão [05-mundo-padrao-vs-mapa.md](05-mundo-padrao-vs-mapa.md) reporta (65 e 62). Não resolvi a divergência; tratei como questão aberta (linha #114).
6. **`spec_procs2/3/4.c` não existem** neste mirror; quem procurar `postmaster` em `spec_procs.c` não acha. Pode haver diferença de organização de arquivos em outras distribuições 3.0.
7. **O que não li linha a linha.** Não inspecionei `src/spells.c`, `src/limits.c` (além de `gain_exp`), `src/db.c` (além de pontos citados), `lib/text/news`, `lib/text/wizlist`, `lib/text/immlist`, os arquivos `.mob`/`.obj` fora dos vnums citados, nem as zonas fora de 0/25/30/31/36/50-73/120/150/186. Também não cataloguei **todas** as ~500 entradas de `spec_assign.c` linha a linha: citei as famílias e os vnums que importam para o roteiro (Fido, janitor, guarda, prefeito, banco, correio, mural, recepcionista, cryo, lojas, castelo, xadrez, esgotos, novatos). Para uma varredura exaustiva, `src/spec_assign.c:90-277` é o arquivo a percorrer.
8. **Risco nos testes.** Vários testes propostos envolvem morrer, virar PK, atacar lojista ou entrar nos esgotos/tabuleiro em nível baixo. A lista de testes marca os perigosos, mas **a decisão de risco é da sessão autorizada**, não deste documento.
9. **Sem valor de crônica.** Nada aqui é fato de campanha, nada aqui a Grebolius sabe. Vale a Regra de Ouro dos Números e o que o arquivo 00 estabelece.
