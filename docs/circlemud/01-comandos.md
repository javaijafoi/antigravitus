# 01 — Comandos do CircleMUD 3.x: afirmações verificáveis

Documento de **afirmações sobre o engine**, para validação posterior ao vivo no Devil's Bob MUD (DeBo, `debomud.org:4000`). Nada aqui prova o DeBo; prova o CircleMUD 3.x do mirror consultado.

## Fonte consultada

| Fonte | Como foi lida | Estado |
| --- | --- | --- |
| `https://raw.githubusercontent.com/Yuffster/CircleMUD/master/src/interpreter.c` | `web_fetch` (texto bruto) | **TRUNCADO**: o fetch omitiu 7.051 bytes do meio do arquivo (o trecho entre `command_interpreter()` e `search_block()`, que continha `find_alias`, `do_alias`, `perform_alias`). O conteúdo dessas funções foi recuperado por busca indexada (linhas completas). |
| `.../src/constants.c`, `.../src/act.other.c`, `.../src/alias.c`, `.../src/act.social.c`, `.../src/act.comm.c`, `.../lib/misc/socials` | `web_fetch` (texto bruto) | Completos, sem aviso de truncamento. |
| `.../src/act.informative.c`, `.../src/comm.c`, `.../src/db.c`, `.../src/db.h`, `.../src/structs.h`, `.../src/utils.h`, `.../src/utils.c`, `.../src/interpreter.h`, `.../src/config.c`, `.../src/fight.c`, `.../src/spell_parser.c` | **não lidos por inteiro** — consultados por busca indexada (linha + trecho) | Citações pontuais e verificáveis |
| **Números de linha** | [Sourcegraph](https://sourcegraph.com/) — API `/search/stream`, busca `regexp` `count:all` restrita ao repo `github.com/Yuffster/CircleMUD` | Os `arquivo:linha` abaixo vêm do **commit `12a0cedbb563465029c46de9537c96854bc11610`** indexado pelo Sourcegraph. Se o HEAD de `master` mudar, os números podem deslocar; o texto citado é a âncora confiável. |

Nenhum número de linha deste documento foi estimado. Onde só existia um intervalo, ele está escrito como **intervalo derivado de duas âncoras confirmadas** e marcado como tal.

## Níveis usados

| Nível | Significa |
| --- | --- |
| **Testado (código)** | O comportamento está no fonte com `arquivo:linha` citado. Prova o **engine** — e só ele. O DeBo pode ter alterado. |
| **Provável** | Decorre do código, mas depende de configuração, versão, mundo, tradução, ou de o DeBo não ter mexido. |
| **Dúvida** | Hipótese, conflito entre fontes, ou dado que não consegui confirmar. |

## Tabela principal

| # | Afirmação | Nível | Fonte (arquivo:linha) | Como validar no DeBo |
| --- | --- | --- | --- | --- |
| 1 | Existe **uma** tabela de comandos, `cmd_info[]`, aberta em `src/interpreter.c`; a primeira entrada é `{ "RESERVED", 0, 0, 0, 0 }` e as direções vêm logo depois. | Testado (código) | src/interpreter.c:201-210 | `commands` deve listar tudo; `north`/`east` movem. |
| 2 | O casamento de comando é por **prefixo** (`strncmp` com o tamanho do que foi digitado) e **a primeira entrada da tabela que casar e cujo nível permitir vence** — não há aviso de ambiguidade. | Testado (código) | src/interpreter.c:600-602 | Digitar `k` (deve virar `kill`, 339, antes de `kick` 340 e `kiss` 341) e `l` (deve virar `look`, 343). |
| 3 | A comparação é sensível a maiúsculas contra nomes em minúsculas, então a entrada sentinela `RESERVED` (maiúscula) nunca casa com o que o jogador digita. | Testado (código) | src/interpreter.c:202 + 601 | Digitar `reserved` e `RESERVED` — ambos devem dar `Huh?!?`. |
| 4 | Comando inexistente responde literalmente `Huh?!?`. | Testado (código) | src/interpreter.c:605-606 | `xyzzy` |
| 5 | Nível insuficiente **não** gera mensagem própria: se a única entrada que casaria é de nível superior, o resultado é o mesmo `Huh?!?`. | Testado (código) | src/interpreter.c:600-606 | Mortal digitar `goto`, `stat`, `wiznet` → `Huh?!?`, e não "você não pode". |
| 6 | Se a posição atual for menor que `minimum_position` da entrada, o comando **não executa** e uma mensagem por posição é enviada; morto recebe `Lie still; you are DEAD!!! :-(`. | Testado (código) | src/interpreter.c:613, 615-616 | Morrer (ou estar dormindo) e tentar um comando de posição maior, ex. `look` (POS_RESTING). |
| 7 | Comando existente mas sem função associada responde `Sorry, that command hasn't been implemented yet.` | Testado (código) | src/interpreter.c:609-610 | Nenhum caso conhecido no DeBo; observar `Huh?!?` vs. essa frase. |
| 8 | Personagem imortal "switched" em um NPC não pode usar comandos de imortal. | Testado (código) | src/interpreter.c:611-612 | Exige imortal; fora do escopo mortal. |
| 9 | Comandos de **um caractere não alfanumérico** existem como entradas próprias: `:` = emote, `;` = wiznet (imortal), `'` = say. | Testado (código) | src/interpreter.c:275, 429, 529 | `'oi` (fala), `:sorri` (emote), `;teste` (só imortal). |
| 10 | `qui` **não sai do jogo**: existe uma entrada própria (`qui`, subcmd 0) cuja única função é responder `You have to type quit--no less, to quit!`. | Testado (código) | src/interpreter.c:407-408 + src/act.other.c:75 | Digitar `qui` e depois `quit`. |
| 11 | `quit` em combate é recusado (`No way!  You're fighting for your life!`); abaixo de POS_STUNNED o personagem morre (`You die before your time...`). | Testado (código) | src/act.other.c:77, 79 | Tentar `quit` durante luta. |
| 12 | `save` é POS_SLEEPING e salva aliases junto; com *auto-save* ligado e nível ≤ LVL_IMMORT a saída é só `Saving aliases.`, senão `Saving <nome> and aliases.` | Provável (qual ramo depende de `auto_save`) | src/act.other.c:120, 124 (ver também 105) | `save` e registrar a frase literal. |
| 13 | `practice` com argumento é recusado: `You can only practice skills in your guild.`; sem argumento lista perícias. | Testado (código) | src/act.other.c:323 (comando em src/interpreter.c:397) | `practice` e `practice espada`. |
| 14 | `title` recusa parênteses (`Titles can't contain the ( or ) characters.`), limita a **80 caracteres** e é bloqueado por PLR_NOTITLE. | Testado (código) | src/act.other.c:354, 356, 357-358; src/structs.h:501 | `title Duque (o)` e `title` com 100 caracteres. |
| 15 | Qualquer comando digitado **apaga o AFF_HIDE** antes de rodar: esconder-se não sobrevive ao próximo comando. | Testado (código) | src/interpreter.c:580 | `hide`, depois `look`, depois `hide` de novo — comparar mensagens. |
| 16 | `hide` só funciona com a perícia: sem ela, `You have no idea how to do that.`; com ela, `You attempt to hide yourself.` | Testado (código) | src/act.other.c:172, 181 (comando em src/interpreter.c:320) | `hide` em personagem sem a perícia. |
| 17 | `visible` para mortal desfaz invisibilidade (`You break the spell of invisibility.`) ou responde `You are already visible.`; para imortal chama `perform_immort_vis`. | Testado (código) | src/act.other.c:330, 339, 341; src/interpreter.c:509 | `visible` sem estar invisível. |
| 18 | `wimpy` sem argumento mostra `Your current wimp level is %d hit points.` ou `At the moment, you're not a wimp.  (sure, sure...)`. | Testado (código) | src/act.other.c:702, 705; src/interpreter.c:525 | `wimpy` |
| 19 | O teto de `wimpy` é **metade dos HP máximos** (`You can't set your wimp level above half your hit points.`); `0` desativa; valor não numérico recebe instrução. | Testado (código) | src/act.other.c:715-716, 722-723, 726 | `wimpy 5000`, `wimpy 0`, `wimpy abc`. |
| 20 | O wimpy **realmente foge**: o combate testa `GET_WIMP_LEV` contra os HP atuais e dispara a fuga. | Testado (código) | src/fight.c:796-797 | Pôr `wimpy` alto, entrar em luta e observar a fuga automática. |
| 21 | `alias` é POS_DEAD (funciona morto/dormindo) e é implementado em `interpreter.c`, não em `act.other.c`. | Testado (código) | src/interpreter.c:215, 671 | `alias` |
| 22 | Sintaxe de alias: `alias` sem argumento lista (`Currently defined aliases:`); com um argumento remove (`Alias deleted.`) ou avisa `No such alias.`; com dois cria (`Alias added.`). | Testado (código) | src/interpreter.c:683, 688, 701, 703, 719 | `alias`, `alias x look`, `alias x`, `alias x de novo`. |
| 23 | `alias alias` é explicitamente proibido (`You can't alias 'alias'.`). | Testado (código) | src/interpreter.c:705-706 | `alias alias olhar` |
| 24 | Aliases "complexos" são detectados pelos caracteres `;` (separador), `$` (variável) e `*` (glob). | Testado (código) | src/interpreter.c:713-716; src/interpreter.h:71-73 | `alias sauda say oi;wave` e depois `sauda`. |
| 25 | **Não há limite de quantidade de aliases** no engine: nenhuma ocorrência de `MAX_ALIAS` no repositório. Persistência em `lib/plralias/`. | Testado (código) | src/alias.c:28; src/db.h:26, 37; src/utils.c:565 | Criar vários aliases e reentrar. |
| 26 | `socials`, `commands` e `wizhelp` chamam o mesmo `do_commands` e imprimem `The following %s%s are available to %s:`. | Testado (código) | src/interpreter.c:250, 463; src/act.informative.c:1643, 1669 | `socials`, `commands`, `wizhelp`. |
| 27 | **Não existe** o comando `social <nome>`: cada social é uma entrada própria da tabela apontando para `do_action`. | Testado (código) | src/interpreter.c:216-537 | `social sorriso` deve falhar; `smile` funciona. |
| 28 | O arquivo `lib/misc/socials` tem **104 entradas** (contagem exaustiva por busca indexada). | Testado (código) | lib/misc/socials (104 cabeçalhos de social) | `socials` e contar; comparar com 104. |
| 29 | A tabela de comandos tem **105** entradas apontando para `do_action` (106 ocorrências de `do_action` menos o protótipo). | Testado (código) | src/interpreter.c:64 vs. 216-537 | Contagem indireta; ver #30. |
| 30 | `hop` está na tabela de comandos mas **não existe no arquivo de socials** — deve responder `That action is not supported.` | Provável (a diferença de 1 comando é o `hop`, por exclusão) | src/interpreter.c:325; src/act.social.c:93 | Digitar `hop` no DeBo. |
| 31 | Cada social tem 8 mensagens + 2 parâmetros (`hide`, `min_victim_position`): sem-argumento, outros-sem-argumento, alvo/outros/vítima, alvo-inexistente, auto/outros-auto. | Testado (código) | src/act.social.c:36-56 | `smile`, `smile fulano`, `smile eu`, `smile ninguem`. |
| 32 | Sem argumento, o social usa `char_no_arg` + `others_no_arg`; se o alvo é você mesmo, usa `char_auto`/`others_auto`; com alvo válido, `char_found` (para você), `others_found` (sala) e `vict_found` (alvo). | Testado (código) | src/act.social.c:98, 112, 117-119 | `wave`, `wave eu`, `wave <alguém>`. |
| 33 | Se a vítima estiver em posição baixa demais, sai `$N is not in a proper position for that.` e nenhuma mensagem de social. | Testado (código) | src/act.social.c:115 | Social com alvo dormindo (varia por social; ver `min_victim_position`). |
| 34 | O segundo número da linha do social é a posição mínima da vítima; o primeiro é o "hide" (0 = aparece na sala). | Testado (código) | lib/misc/socials:0 (`accuse 0 5`), :140 (`dance 1 8`), :610 (`spank 0 8`) | `accuse` alguém deitado vs. `dance` com alguém deitado. |
| 35 | Um `#` no arquivo de socials encerra a leitura daquele social ("se não houver `char_found`, o resto é ignorado"), então social com `#` logo após a 2ª linha **não aceita alvo**. | Testado (código) | src/act.social.c:259-260; lib/misc/socials:10-13 (`applaud`) | `applaud fulano` deve usar a mensagem sem-alvo. |
| 36 | Os slots de social são contados a partir da **tabela de comandos**, não do arquivo; social desconhecido no arquivo gera erro no boot e o slot é reaproveitado. | Testado (código) | src/act.social.c:225-229, 240-241 | Não observável em jogo; depende do log do servidor. |
| 37 | `insult` é um comando **separado** (`do_insult`), não um social do arquivo, com frases aleatórias (3 casos). | Testado (código) | src/act.social.c:126, 149, 152, 157, 160 | `insult <alvo>` várias vezes; `insult` sem alvo. |
| 38 | Insultar-se a si mesmo responde `You feel insulted.` | Testado (código) | src/act.social.c:166 | `insult eu` / `insult <seu nome>`. |
| 39 | Socials "engraçados"/explícitos existem no arquivo padrão: `fart`, `burp`, `spank`, `grope`, `french`, `snowball`. | Testado (código) | lib/misc/socials:175, 55, 610, 270, 205, 590 | Digitar cada um; `snowball` exige imortal (ver #40). |
| 40 | `snowball` é o (único) social com nível mínimo: POS_STANDING e LVL_IMMORT. | Provável ("único" por inspeção da tabela) | src/interpreter.c:460 | Mortal digitar `snowball` → `Huh?!?`. |
| 41 | `say` sem argumento responde `Yes, but WHAT do you want to say?`; a sala ouve `$n says, '<texto>'`. | Testado (código) | src/act.comm.c:45, 49 (comando em src/interpreter.c:428) | `say` vazio e `say oi`. |
| 42 | `say` monta a terceira pessoa com o texto **cru** do jogador dentro de `act()` — a interpretação de `$`/`$n` no que a sala vê depende do mecanismo de `$$`; não confirmei o comportamento final. | Dúvida | src/act.comm.c:49; src/interpreter.c:897 (comentário sobre `$$`) | `say oi $n` e pedir a um segundo personagem o que ele viu. |
| 43 | `tell` exige alvo e texto (`Who do you wish to tell what??`); a checagem `is_tell_ok` recusa: a si mesmo, quem tem `notell`, sala `SOUNDPROOF` (`The walls seem to absorb your words.`), alvo linkless, alvo escrevendo (`PLR_WRITING`) e alvo com `notell` (`$E can't hear you.`). | Testado (código) | src/act.comm.c:121-143 (intervalo; `is_tell_ok` em 121, `The walls...` em 128); comando em src/interpreter.c:479 | `tell`, `tell ninguem oi`, `tell <alvo> oi` numa sala à prova de som. |
| 44 | `reply` usa o último ID que te falou; sem último tell → `You have nobody to reply to!`; se o interlocutor saiu → `They are no longer playing.` | Testado (código) | src/act.comm.c:104, 163 (`do_reply`) | `reply oi` sem nunca ter recebido tell. |
| 45 | Canais: `holler`, `shout`, `gossip`, `auction`, `grats` (do_gen_comm). Quem ouve precisa estar em `CON_PLAYING`, não ser o autor, não ter a flag do canal (`PRF_DEAF`/`NOGOSS`/`NOAUCT`/`NOGRATZ`), não estar escrevendo e não estar em sala `SOUNDPROOF`; **`shout` só alcança a mesma zona** e quem está acordado. | Testado (código) | src/act.comm.c:366-484 (função inteira), 373 (vetor de flags), 388 (matriz de mensagens) | Dois personagens em zonas diferentes → `shout` não chega; `gossip` chega. |
| 46 | Canal bloqueado por `PLR_NOSHOUT` responde `You cannot holler!!` / `You cannot shout!!` / `You cannot gossip!!` / `You cannot auction!!` / `You cannot congratulate!`; quem não está no canal recebe `You aren't even on the channel!`. | Testado (código) | src/act.comm.c:389-409, 420, 434 | `noshout` e depois `shout oi`. |
| 47 | Nível mínimo para falar em canais é `level_can_shout = 1`, com a mensagem `You must be at least level %d before you can %s.` | Testado (código) | src/config.c:60; src/act.comm.c:428-429 | Só verificável em personagem de nível 0. |
| 48 | `holler` custa 20 pontos de movimento (`holler_move_cost`) e pode falhar com `You're too exhausted to holler.` | Testado (código) | src/config.c:63; src/act.comm.c:446-450 | `score`, `holler oi`, `score` de novo. |
| 49 | `gossip`, `auction`, `grats` e `gsay` são POS_SLEEPING: funcionam dormindo. | Testado (código) | src/interpreter.c:303, 314 (POS_SLEEPING); 304, 428 (comparação POS_RESTING) | Dormir (`sleep`) e tentar `gossip oi` e `say oi`. |
| 50 | `gsay`/`gtell` fala só com o grupo (`AFF_GROUP`), alcançando o líder e os seguidores marcados; fora de grupo → `But you are not the member of a group!` | Testado (código) | src/act.comm.c:62-94 (do_gsay, 62) | `gtell oi` sem grupo. |
| 51 | `whisper` e `ask` são o mesmo `do_spec_comm` com verbos diferentes (`whisper to` / `asks`); alvo tem de estar na sala; falar consigo mesmo dá `You can't get your mouth close enough to your ear...` | Testado (código) | src/act.comm.c:200, 208, 215-216, 233 | `whisper eu oi`, `ask alguem algo`. |
| 52 | A preferência `norepeat` troca o eco da sua própria fala por `OK` em todos os canais e no say/tell. | Testado (código) | src/act.comm.c:52, 91, 108, 240, 456, 499 | `norepeat`, depois `say oi` e `gossip oi`. |
| 53 | **Não existe** comando `pagelength`, `pagelen` nem `pagesize` em lugar algum do repositório (busca exaustiva: 0 resultados). | Testado (código) | busca no repositório, 0 ocorrências | `pagelength 60` → esperado `Huh?!?`. Se o DeBo responder, é modificação. |
| 54 | **Não existem** comandos `columns` ou `rows` no engine; as ocorrências são internas (`autowiz.c:33`, `MAX_BAG_ROWS` em `objsave.c`). | Testado (código) | src/util/autowiz.c:33; src/objsave.c:27 | `columns 80`, `rows 40`. |
| 55 | `prompt` e `display` são o mesmo comando (`do_display`) e aceitam **apenas** `H`, `M`, `V`, `all`/`on`, `none`/`off`, `auto`; qualquer outro texto responde `Usage: prompt { { H | M | V } | all | auto | none }`. | Testado (código) | src/interpreter.c:266, 396; src/act.other.c:730, 741, 770 | `prompt %h` (deve sair a mensagem de uso), `prompt all`, `prompt hmv`. |
| 56 | O engine 3.x **não tem prompt com tokens** (`%h`, `%m`, `%v`): o prompt é montado por `make_prompt` sempre no formato `[iX ]<H H><M M><V V>> ` ou `<nome>> `, truncado em 96 caracteres. | Testado (código) | src/comm.c:985, 992, 1004, 1010, 1016, 1022, 1028, 1030; src/structs.h:488 | Comparar o prompt antes/depois de `prompt hmv` e de `prompt all`. |
| 57 | `prompt auto` liga `PRF_DISPAUTO` ("mostrar HP/MP/MV quando < 30%"), mas essa flag **não é consultada em nenhum outro ponto do código**. | Provável (conclusão de ausência de uso; 3 ocorrências no total) | src/structs.h:216; src/act.other.c:746-747; src/comm.c (nenhuma referência) | `prompt auto`, baixar HP abaixo de 30% e ver se o prompt muda. |
| 58 | O toggle `autoexit` controla mostrar saídas automaticamente no `look`. | Testado (código) | src/interpreter.c:221; src/act.informative.c:432; mensagens em src/act.other.c:881-882 | `autoexit` e comparar o `look` com/sem. |
| 59 | O toggle `brief` suprime a descrição da sala no `look`; mensagens `Brief mode on./off.` | Testado (código) | src/interpreter.c:233; src/act.informative.c:427; src/act.other.c:855-856 | `brief` e `look` na mesma sala. |
| 60 | O toggle `compact` remove o CRLF extra antes do prompt; mensagens `Compact mode on./off.` | Testado (código) | src/interpreter.c:251; src/comm.c:1411; src/act.other.c:857-858 | `compact` e observar a linha em branco antes do prompt. |
| 61 | `nohassle` é restrito a imortais; mensagens `Nohassle enabled./disabled.` | Testado (código) | src/interpreter.c:367; src/act.other.c:853-854 | Mortal digitar `nohassle` → `Huh?!?`. |
| 62 | A lista de toggles é indexada pelo `subcmd`, e o `toggle` mostra o estado de cada preferência. | Testado (código) | src/act.other.c:850, 892-940; src/act.informative.c:1596-1607 | `toggle` e comparar com `brief`/`compact`/`autoexit`. |
| 63 | `noshout` é flag de **jogador** (`player_bits`), não de preferência. | Testado (código) | src/constants.c:115 (lista `player_bits`) | `noshout` funciona, mas não aparece na lista de preferências do `toggle`. |
| 64 | `norepeat`, `nosummon`, `notell` são toggles de mortal; `roomflags`, `holylight`, `nowiz` são de imortal; `slowns` e `trackthru` são de implementador. | Testado (código) | src/interpreter.c:368, 370, 371, 373, 324, 450; src/act.other.c:928, 934, 940 | Testar com mortal e ver quais dão `Huh?!?`. |
| 65 | `credits`, `news`, `wizlist`, `immlist`, `policy`, `info`, `motd`, `version`, `whoami` imprimem arquivos de `lib/text/` (uma `page_string` cada). | Testado (código) | src/db.h:72-83; src/db.c:390-399; src/act.informative.c:1253-1286 | `credits`, `news`, `wizlist`, `info`, `version`, `whoami`. |
| 66 | `handbook` (LVL_IMMORT) e `imotd` (LVL_IMMORT) são restritos a imortais. | Testado (código) | src/interpreter.c:317, 331 | Mortal digitar `handbook` → `Huh?!?`. |
| 67 | `idea`, `typo` e `bug` **anexam** texto ao fim de `lib/misc/ideas`, `lib/misc/typos`, `lib/misc/bugs` e respondem `Okay.  Thanks!`; há checagem de tamanho máximo do arquivo. | Testado (código) | src/db.h:85-87; src/act.other.c:791, 794, 797, 836 (checagem de tamanho entre 820 e 828) | `bug teste`, `typo teste`, `idea teste`. |
| 68 | `clear` e `cls` são o mesmo comando; `murder` é `hit` com outro subcomando; `take` é `get`; `gtell` é `gsay`; `display` é `prompt`. | Testado (código) | src/interpreter.c:243, 245, 359, 481, 314, 266 | Digitar cada par e comparar saída. |
| 69 | `recall` **não é comando**: "word of recall" é magia registrada com nível 20, mana 10 e posição POS_FIGHTING. | Testado (código) | src/spell_parser.c:956 | `recall` → `Huh?!?`; `cast 'word of recall'`. |
| 70 | `who` lista jogadores (`do_who`) e `whoami` mostra só você; são comandos distintos. | Testado (código) | src/interpreter.c:517 (who), 518 (whoami); src/act.informative.c:958 | `who` e `whoami`. |

## Detalhes técnicos

### 1. Como o engine resolve o comando (prefixo, ambiguidade, "Huh?!?")

```c
for (length = strlen(arg), cmd = 0; *cmd_info[cmd].command != '\n'; cmd++)
  if (!strncmp(cmd_info[cmd].command, arg, length))
    if (GET_LEVEL(ch) >= cmd_info[cmd].minimum_level)
      break;
```
— src/interpreter.c:600-602

- Não há detecção de ambiguidade: **a ordem da tabela é a regra**. `src/interpreter.c:204` registra o motivo histórico de as direções virem antes.
- Falha de nível e nome inexistente terminam no mesmo lugar:
```c
send_to_char(ch, "Huh?!?\r\n");
```
— src/interpreter.c:606
- Comando bloqueado por posição: condição em `src/interpreter.c:613`, com o caso morto em `src/interpreter.c:615-616`. O intervalo entre 606 e 609 (frozen / nível) é **intervalo derivado** das duas âncoras confirmadas, por isso não é citado linha a linha.

### 2. Abreviação de uma letra: o que a ordem da tabela decide

| Digitar | Entrada que vence | Linha | Por quê |
| --- | --- | --- | --- |
| `k` | `kill` | src/interpreter.c:339 | `kill` (339) vem antes de `kick` (340) e `kiss` (341) na tabela. |
| `l` | `look` | src/interpreter.c:343 | primeira entrada com `l`. |
| `s` | `say` | src/interpreter.c:428 | `say` (428) vem antes de `save` (430) e `score` (431). |
| `q` | `quaff` | src/interpreter.c (bloco `quaff`/`qecho`/`quest`/`qui`/`quit`) | `quaff` precede `qui` (407) e `quit` (408); a conclusão é **Provável** (depende da ordem completa, lida no fonte bruto). |
| `qui` | `qui` (não `quit`) | src/interpreter.c:407 | existe justamente para responder a bronca de `do_quit` (src/act.other.c:75). |

### 3. Configuração de cliente e paginação

- Busca exaustiva no repositório por `pagelength|pagelen|pagesize`: **0 resultados**. Busca por `columns|rows`: só usos internos (`src/util/autowiz.c:33`, `src/objsave.c:27`) e textos de sala.
- O único comando de cliente relacionado a saída no 3.x é `prompt`, e ele **não** aceita string livre:
```c
send_to_char(ch, "Usage: prompt { { H | M | V } | all | auto | none }\r\n");
```
— src/act.other.c:741 (e repetido em 770)
- O prompt é montado peça por peça, sem interpretar tokens do jogador:
```c
strcpy(prompt, "] ");      /* comm.c:992 */
count = snprintf(prompt + len, sizeof(prompt) - len, "%dH ", GET_HIT(d->character));  /* 1010 */
```
— src/comm.c:992, 1010, e equivalentes em 1004/1016/1022/1028/1030; teto de `MAX_PROMPT_LENGTH 96` em src/structs.h:488.
- **Consequência prática:** `pagelength`, `term`, `columns`, `rows` e `prompt %h ...` são, no 3.x puro, ou inexistentes ou inválidos. Se o DeBo os aceitar, são modificações/port de outra base.

### 4. `prompt auto` e o vestígio sem uso

```c
TOGGLE_BIT(PRF_FLAGS(ch), PRF_DISPAUTO);
send_to_char(ch, "Auto prompt %sabled.\r\n", PRF_FLAGGED(ch, PRF_DISPAUTO) ? "en" : "dis");
```
— src/act.other.c:746-747; a flag é definida em src/structs.h:216 como `Show prompt HP, MP, MV when < 30%` e não aparece em nenhum consumidor no repositório.

### 5. Toques, ecos e quem ouve

- `say`:
```c
snprintf(buf, sizeof(buf), "$n says, '%s'", argument);   /* act.comm.c:49 */
send_to_char(ch, "Yes, but WHAT do you want to say?\r\n");  /* act.comm.c:45, caso vazio */
```
- Entrega de canais: o autor não recebe o próprio `$n ...`, e a lista de flags proibidas vem do vetor `channels[]` (`PRF_DEAF`, `PRF_NOGOSS`, `PRF_NOAUCT`, `PRF_NOGRATZ`) em `src/act.comm.c:373`; a matriz de mensagens está em `src/act.comm.c:388`.
- `shout` é o único canal com filtro geográfico (mesma zona) e de sono; `gossip`/`auction`/`grats` são POS_SLEEPING (`src/interpreter.c:303`).

### 6. Socials: contagem e o caso `hop`

- 104 entradas no arquivo (`lib/misc/socials`), 105 comandos `do_action` na tabela (`src/interpreter.c:216-537`, protótipo em 64).
- `hop` existe na tabela (`src/interpreter.c:325`) e **não** existe no arquivo (busca `^hop` no arquivo: 0 resultados).
```c
if ((act_nr = find_action(cmd)) < 0) {
  send_to_char(ch, "That action is not supported.\r\n");
```
— src/act.social.c:92-93

- Exemplos de mensagens citáveis (arquivo e linha): `burp` — "You burp loudly." (lib/misc/socials:55); `fart` — "Where are your manners?" (175); `spank 0 8` — "You spank WHO?  Eh?  How?  Naaah, you'd never." (610); `snowball` — "You throw a snowball in $N's face." (590).
- O arquivo termina com uma linha `$`; `#` corta a leitura do social (`src/act.social.c:259-260`).

### 7. Easter eggs e comandos "de ninguém"

| Comando | O que faz | Fonte |
| --- | --- | --- |
| `qui` | Não sai: dá bronca | src/interpreter.c:407; src/act.other.c:75 |
| `hop` | Deve dizer que a ação não é suportada (sem social) | src/interpreter.c:325; src/act.social.c:93 |
| `snowball` | Social de imortal (joga bola de neve) | src/interpreter.c:460 |
| `:` | Emote curto | src/interpreter.c:275 |
| `;` | Wiznet (imortal) | src/interpreter.c:529 |
| `murder` | `hit` com SCMD_MURDER | src/interpreter.c:359 |
| `clear` / `cls` | Limpar tela | src/interpreter.c:243, 245 |
| `insult` | Três frases aleatórias, incluindo `$n calls your mother a bitch!` | src/act.social.c:126, 157 |
| `idea`/`typo`/`bug` | Anexa em `lib/misc/*` e responde `Okay.  Thanks!` | src/act.other.c:791-797, 836; src/db.h:85-87 |
| `immlist`, `handbook`, `imotd`, `wizlist` | Arquivos de `lib/text/` (parte só para imortais) | src/db.h:72-83; src/act.informative.c:1253-1286 |
| `norepeat` | Eco vira `OK` em vez de repetir sua fala | src/act.comm.c:52, 91, 108, 240, 456, 499 |
| `wimpy` | Fuga automática real, com teto de metade dos HP | src/act.other.c:715-716; src/fight.c:796-797 |
| `hide` | Quebra no comando seguinte (AFF_HIDE é limpo) | src/interpreter.c:580 |

## Limites desta pesquisa

1. **`interpreter.c` foi truncado no fetch bruto** (7.051 bytes omitidos). Recuperei `do_alias`, `find_alias` e `perform_alias` por busca indexada, mas **não li o arquivo inteiro linha a linha**; pode haver detalhe fora dos pontos citados.
2. **`act.informative.c`, `comm.c`, `db.c` e outros só foram consultados por busca**, não lidos integralmente. Citações pontuais são confiáveis; a ausência de menção não é prova de ausência de comportamento.
3. A palavra **`term` não foi pesquisada** (é ambígua e apareceria em contextos não relacionados). O nível 00-afirmacoes-e-validacao.md prevê testá-la; do lado do engine **não posso afirmar se existe**. `pagelength`, `pagelen`, `pagesize` e `columns`/`rows` **foram** pesquisados e não existem.
4. Os números de linha vêm do **commit indexado pelo Sourcegraph** (`12a0ced…`), não necessariamente do HEAD de `master`.
5. Nada aqui foi observado **no DeBo**. Tradução PT-BR, mudanças de tabela de comandos, port de `term`/paginação e a mensagem `Huh?!?` traduzida (se for o caso) são exatamente o que os testes ao vivo devem checar.
6. Não confirmei se o DeBo mantém os mesmos **níveis mínimos** de comando, nem se ele tem `snowball`, `hop`, `insult` ou `qui`.
7. A contagem de 105 comandos `do_action` na tabela foi feita por inspeção das linhas retornadas na busca; um erro de contagem mudaria o caso `hop` (por isso ele está como **Provável**).
