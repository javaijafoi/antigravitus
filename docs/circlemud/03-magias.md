# 03 — MAGIAS: números do motor CircleMUD (para validar no DeBo)

Documento de **afirmações verificáveis** sobre o subsistema de magia do engine CircleMUD, extraídas
do código-fonte, para depois serem conferidas num servidor real (Devil's Bob MUD, `debomud.org:4000`).

---

## Fonte consultada

**Repositório:** <https://github.com/Yuffster/CircleMUD> (branch `master`)
**Commit exato consultado (único commit do repo):** `12a0cedbb563465029c46de9537c96854bc11610`
— mensagem: *"Initial commit of 3.1."*, autor Michelle Steigerwalt, data **2012-03-22T02:26:26Z**
(verificado em <https://api.github.com/repos/Yuffster/CircleMUD/commits/master>).

> ⚠️ **AVISO IMPORTANTE (premissa do projeto):** este mirror chama-se CircleMUD, mas o commit diz
> literalmente **"Initial commit of 3.1"** — ou seja, é o código do **CircleMUD 3.1**, não do 3.0.
> O DeBo declara-se baseado em **3.0**. As fórmulas de magia do 3.0 e do 3.1 são, até onde este
> documento verifica, as mesmas nestes arquivos (o 3.1 mexeu sobretudo em portabilidade/OLC), mas
> **a correspondência 1:1 entre 3.1 e o 3.0 do DeBo não foi verificada aqui** e está marcada como
> *Provável* onde relevante. Todo número deste documento é do **3.1**.

**Arquivos lidos (raw, no commit acima):**

| Arquivo | URL crua | Linhas (aprox.) | Status do fetch |
|---|---|---|---|
| `src/spells.h` | `.../master/src/spells.h` | ~300 | completo |
| `src/spell_parser.c` | `.../master/src/spell_parser.c` | ~1000 | completo |
| `src/magic.c` | `.../master/src/magic.c` | ~1000 | completo |
| `src/spells.c` | `.../master/src/spells.c` | ~410 | completo |
| `src/fight.c` | `.../master/src/fight.c` | ~1010 | completo |
| `src/class.c` | `.../master/src/class.c` | 2183 | **truncado no fetch inline** (ver nota) |

**Nota sobre truncamento:** o fetch de `src/class.c` teve o corpo truncado no meio; o resultado
completo ficou salvo em arquivo de rascunho local e foi lido a partir dele. Os demais arquivos
vieram inteiros. `src/constants.c` **não** contém nada essencial de magia/afeto (afetos, posições,
`MAG_*`, `TAR_*` estão em `spells.h`, `structs.h` e `utils.h`) e por isso não é citado.

**Como os números de linha foram obtidos (importante para auditoria):**
o usuário não consegue ler o arquivo linha a linha via raw. Foi usada a API pública de busca de
código do Sourcegraph, que devolve `{line, lineNumber}` por correspondência, indexada no mesmo
commit `12a0cedbb…`:

`https://sourcegraph.com/.api/search/stream?q=repo:^github\.com/Yuffster/CircleMUD$ file:src/magic\.c count:all <padrão>&v=V3&t=literal`

O campo `lineNumber` dessa API é **0-based** (verificado: em `src/Makefile`, a 1ª linha `all:`
retorna `lineNumber: 0`). Todos os números citados neste documento já estão **convertidos para
1-based**. Validação cruzada: para 7 trechos distintos de `src/class.c`, o número obtido pelo
Sourcegraph +1 coincidiu **exatamente** com o número de linha medido na cópia crua salva
localmente do arquivo. Para reproduzir qualquer citação:

`https://raw.githubusercontent.com/Yuffster/CircleMUD/12a0cedbb563465029c46de9537c96854bc11610/src/<arquivo>`

**Níveis usados na tabela de afirmações**
- **Testado (código)** — está no código, com linha citada. Prova o *engine*, não o DeBo.
- **Provável** — decorre do código, mas depende de configuração, versão (3.0 vs 3.1) ou do mundo.
- **Dúvida** — hipótese/não confirmado.

---

## 1. Tabela de afirmações

| # | Afirmação | Nível | Fonte (arquivo:linha) | Como validar no DeBo |
|---|---|---|---|---|
| 1 | O dano das magias ofensivas **não escala com o nível do conjurador**: cada magia tem um número fixo de dados (única exceção: `earthquake` = `2d8 + nível`). | Testado (código) | `src/magic.c:177-255` (linha do `2d8+level`: `src/magic.c:255`) | Conjurar `lightning bolt` 10× no mesmo tipo de monstro, no nível 10 e no nível 20; a faixa de dano deve ser idêntica (8–63). |
| 2 | `magic missile` = `1d8+1` para Magic-User e `1d6+1` para qualquer outra classe. | Testado (código) | `src/magic.c:180` e `src/magic.c:182` | Conjurar 20× e conferir mínimo/máximo observados (2–9). Repetir com um clérigo lançando por pergaminho: a faixa cai para 2–7. |
| 3 | `burning hands` = `3d8+3` (mago) / `3d6+3` (outros) → 6–27 / 6–21. | Testado (código) | `src/magic.c:186`, `src/magic.c:188` | 10 conjurações: nenhum valor fora de 6–27. |
| 4 | `chill touch` = `1d8+1` / `1d6+1` **mais** `-1` em STR, com duração 4 h se o alvo **falhar** o save e 1 h se ele **passar**. | Testado (código) | `src/magic.c:180,182,302,304,306,307` | Conjurar em monstro e olhar `score`/`consider` antes e depois; cronometrar o retorno do STR (1 ou 4 horas de jogo). |
| 5 | `shocking grasp` = `5d8+5` / `5d6+5` → 10–45 / 10–35. | Testado (código) | `src/magic.c:192`, `src/magic.c:194` | 10 conjurações, conferir faixa. |
| 6 | `lightning bolt` = `7d8+7` (mago) / `7d6+7` → 8–63 / 8–49. **Exige posição de luta (`POS_FIGHTING`), não pode ser lançada parada.** | Testado (código) | `src/magic.c:198,200`; `src/spell_parser.c:895` | Em pé, sem alvo, tentar `cast 'lightning bolt' <alvo>` → mensagem `Impossible!  You can't concentrate enough!`. |
| 7 | `color spray` = `9d8+9` / `9d6+9` → 18–81 / 18–63. | Testado (código) | `src/magic.c:204`, `src/magic.c:206` | 10 conjurações, conferir faixa. |
| 8 | `fireball` = `11d8+11` / `11d6+11` → 22–99 / 22–77. | Testado (código) | `src/magic.c:210`, `src/magic.c:212` | 10 conjurações, conferir faixa. |
| 9 | `call lightning` = `7d8+7`; `harm` = `8d8+8`; `dispel evil`/`dispel good` = `6d8+6`; `energy drain` = 100 fixo se o alvo tiver nível ≤ 2, senão `1d10`; `earthquake` = `2d8+nível` do conjurador. | Testado (código) | `src/magic.c:217,227,239,243,250,255` | Medir o dano de `energy drain` em rato (nível baixo) e em monstro de nível alto: 100 vs 1–10. |
| 10 | Se o alvo **passa no save**, o dano é dividido por 2 (`dam /= 2`). Não existe "dano zero por resistir" em magia de dano. | Testado (código) | `src/magic.c:262-263` | Comparar a distribuição de dano: deve aparecer uma moda em ~metade do valor, nunca 0 vindo de save. |
| 11 | O dano de **um golpe** é limitado a **100** (`dam = MAX(MIN(dam, 100), 0)`), teto aplicado em `damage()`. | Testado (código) | `src/fight.c:737` | Nenhuma conjuração deve arrancar mais de 100 HP de uma vez. |
| 12 | `sanctuary` no alvo divide o dano recebido por 2 (só quando o dano é ≥ 2). | Testado (código) | `src/fight.c:726-727` | Bater no mesmo monstro 10× sem e 10× com sanctuary e comparar as médias. |
| 13 | A **AC do alvo não reduz dano**: entra só na chance de acerto — `victim_ac = compute_armor_class(vítima) / 10` e acerta se `(thaco - d20) <= victim_ac`. | Testado (código) | `src/fight.c:891`, `src/fight.c:904-909` | Verificar que aumentar a AC (via `armor`) não muda o valor dos danos, só a frequência dos "miss". |
| 14 | `compute_armor_class()` = `GET_AC` + `dex_app[DEX].defensive * 10` (se acordado), com mínimo −100. | Testado (código) | `src/fight.c:104-109` | `identify` em si mesma mostra "AC: N"; comparar com `GET_AC` antes/depois de aplicar `armor` e de ficar inconsciente. |
| 15 | `armor` aplica **`APPLY_AC = -20`**, duração **24**, e é acumulativo **só na duração**: recasting estende o tempo, mas o modificador **não** soma (o valor continua −20). | Testado (código) | `src/magic.c:313-316`; `src/handler.c:344-351` | Lançar `armor` 3× seguidas e conferir em `score`/`identify` que a AC cai uma única vez (20 pontos), mas o efeito demora mais para cair. |
| 16 | `invisibility` aplica `APPLY_AC = -40` + `AFF_INVISIBLE`, duração `12 + nível/4` horas de jogo. | Testado (código) | `src/magic.c:408-412` | Cronometrar a duração (contar horas de jogo) e conferir a AC. |
| 17 | `sanctuary` duração **4** horas de jogo, só a flag `AFF_SANCTUARY` (não muda AC nem save). | Testado (código) | `src/magic.c:438-442` | Contar 4 horas de jogo até a mensagem `The white aura around your body fades.` |
| 18 | `bless` = `+2` hitroll **e** `-1` em saving throw de magia, duração **6**; `accum_duration` (recasting acumula tempo). | Testado (código) | `src/magic.c:321-329` | Ver no `identify`/`score` o bônus de hitroll e medir a duração. |
| 19 | `strength` = `+1` em STR (`+2` se nível > 18), duração `(nível do conjurador / 2) + 4`; falha se o alvo já tem `ADD` 100. | Testado (código) | `src/magic.c:465-473` | Lançar em nível 6 (duração 7 h) e nível 20 (duração 14 h) e cronometrar. |
| 20 | `poison` = `-2` STR + flag `AFF_POISON`, duração = **nível do conjurador** (em horas de jogo). | Testado (código) | `src/magic.c:423-425` | Lançar em nível 10 e verificar se o afeto dura ~10 horas de jogo. |
| 21 | `sleep`: só funciona se o alvo **falhar** o save; ignora monstros com `MOB_NOSLEEP`; em MUD sem PK não afeta PC contra PC. Duração `4 + nível/4`. | Testado (código) | `src/magic.c:447-456` | Tentar dormir outro jogador num MUD sem PK (nada acontece) e um NPC comum (dorme). |
| 22 | Cada unidade de duração = **1 hora de jogo**, e `affect_update()` roda **1× por hora de jogo** (bloco de `SECS_PER_MUD_HOUR * PASSES_PER_SEC` no heartbeat). `SECS_PER_MUD_HOUR` = 75 s reais. | Testado (código) | `src/magic.c:76-95`; `src/comm.c:846-848`; `src/utils.h:120`; `src/structs.h:476` | Ativar um afeto de duração 4 e cronometrar ~5 minutos reais (4 × 75 s) até a mensagem de fim. |
| 23 | O afeto expira quando a duração chega a 0: é enviada a `wear_off_msg` da magia e o afeto é removido. Duração `-1` = permanente (só imortais). | Testado (código) | `src/magic.c:84-95`; textos em `src/spell_parser.c:768,772,776,788,792,926,938,942,954` | Ver as strings exatas de fim (ex.: `You feel less protected.` para `armor`). |
| 24 | Save = `saving_throws(classe, tipo, nível do alvo)` + `GET_SAVE(alvo,tipo)` + modificador; **passa** se `MAX(1, save) < rand_number(0, 99)`; rolagem 0 nunca salva. | Testado (código) | `src/magic.c:53-68` | Estatístico: em nível baixo o alvo quase nunca resiste; em nível alto quase sempre (ver #25). |
| 25 | Tabela de save **Magic-User / SAVING_SPELL**: nível 1 → 60; 10 → 44; 20 → 26; 30 → 8 (nível 0 → 90). | Testado (código) | `src/class.c:383-425` (linhas 386, 395, 405, 415) | Comparar a taxa de resistência de um mago nível 1 vs nível 20 contra a mesma magia. |
| 26 | Magia conjurada com `cast` usa `SAVING_SPELL`; magias por **item** (wand/staff/scroll/potion) usam `SAVING_ROD`. | Testado (código) | `src/spell_parser.c:231,234,237` | Comparar a taxa de resistência do mesmo feitiço lançado por `cast` e por varinha. |
| 27 | **`sanctuary` NÃO altera o save** — só o dano é reduzido (#12). | Testado (código) | busca por `AFF_SANCTUARY` no repo: `src/magic.c:439`, `src/fight.c:726`, `src/spells.c:207` | Medir taxa de "resistiu" com e sem sanctuary: não deve mudar. |
| 28 | Efeito de "o alvo resistiu" por magia: dano → metade (#10); `blindness`, `curse`, `poison` → **nada acontece** (`NOEFFECT` / `You fail.`); `sleep` → nada; `chill touch` → só duração 1 h. | Testado (código) | `src/magic.c:334,354,418,452,304-306` | Lançar `blindness`/`poison` repetidamente e observar as mensagens de falha. |
| 29 | Custo de mana = `MAX(mana_max - mana_change * (nível - min_level_da_classe), mana_min)`. | Testado (código) | `src/spell_parser.c:88-93` | Medir a mana gasta com `score` antes/depois no nível mínimo e em nível alto. |
| 30 | **Não existe tabela de custo de mana por classe.** O custo é por magia (`spello`) e o que muda por classe é só o **nível mínimo** (que desloca o desconto). | Testado (código) | `src/spell_parser.c:679-681`; `src/class.c:1628-1699` | Comparar o custo de `armor` para mago (nível mín. 4) e clérigo (nível mín. 1) no mesmo nível de personagem. |
| 31 | Mana máxima inicial = **100**; por nível, mago/clérigo ganham `rand_number(nível, 1.5*nível)` limitado a **10**; ladrão/guerreiro ganham 0. | Testado (código) | `src/class.c:1474`; `src/class.c:1529-1530` e `1536-1537`; `src/class.c:1543,1549,1558` | Subir do nível 1 para o 2 e conferir o ganho de mana (1 a 3 no mago nível 1→2… teto 10). |
| 32 | Níveis mínimos (mago): `magic missile` 1, `detect invis/magic` 2, `chill touch`/`infravision` 3, `invisibility`/`armor` 4, `burning hands` 5, `locate object`/`strength` 6, `shocking grasp` 7, `sleep` 8, `lightning bolt`/`blindness` 9, `detect poison` 10, `color spray` 11, `energy drain` 13, `curse`/`poison` 14, `fireball` 15, `charm` 16, `enchant weapon` 26, `clone` 30. | Testado (código) | `src/class.c:1631-1653` | No DeBo, pedir `practice`/`spells` em cada nível e comparar a lista. |
| 33 | Magias que **não** são de mago (só clérigo): `cure light` 1, `create food/water` 2, `bless` 5, `protection from evil` 8, `group armor` 9, `cure critic` 9, `summon` 10, `remove poison` 10, `word of recall` 12, `earthquake` 12, `dispel evil/good` 14, **`sanctuary` 15**, `call lightning` 15, **`heal` 16**, `sense life` 18, `harm` 19, `group heal` 22, `remove curse` 26. | Testado (código) | `src/class.c:1656-1684` | Se a maga do DeBo conjura `sanctuary`/`heal`, o DeBo **não** é 3.1 stock nesse ponto (classe extra ou magia liberada) — registrar a exceção. |
| 34 | Lag depois de conjurar = `WAIT_STATE(ch, PULSE_VIOLENCE)` = **2 s reais** (tanto no sucesso quanto na falha por concentração). | Testado (código) | `src/spell_parser.c:627,636`; `src/structs.h:480` (`PULSE_VIOLENCE = 2 RL_SEC`), `src/structs.h:476` | Cronometrar: após `cast`, o próximo comando deve ser recusado por ~2 s. |
| 35 | **Não existe a regra "não pode conjurar enquanto luta"** como texto. O que existe é a **posição mínima por magia**: `POS_FIGHTING` = 7 e `POS_STANDING` = 8, e o teste é `GET_POS(ch) < SINFO.min_position`. Logo, magias de posição `POS_STANDING` (ex.: `sanctuary`, `invisibility`, `bless`, `strength`, `sleep`, `poison`, `curse`) **não podem** ser lançadas em combate — mas `armor`, `magic missile` e `lightning bolt` são `POS_FIGHTING` e podem. | Testado (código) | `src/spell_parser.c:461-476`; `src/structs.h:148-149`; `min_position` de cada magia em `src/spell_parser.c:763-965` | Em combate, tentar `cast 'sanctuary' self` (POS_STANDING) → `Impossible!  You can't concentrate enough!`; tentar `cast 'armor' self` (POS_FIGHTING) → funciona. |
| 36 | Mensagens exatas de bloqueio por posição: dormindo `You dream about great magical powers.`; descansando `You cannot concentrate while resting.`; sentado `You can't do this sitting!`; **lutando** `Impossible!  You can't concentrate enough!`; outro `You can't do much of anything like this!` | Testado (código) | `src/spell_parser.c:461-476` | Reproduzir cada mensagem mudando de posição antes do `cast`. |
| 37 | Falha de concentração: `rand_number(0, 101) > GET_SKILL(ch, spellnum)` → lag de 2 s, mensagem `You lost your concentration!` e perda de **metade** da mana. | Testado (código) | `src/spell_parser.c:626-631` | Com a perícia baixa (recém-aprendida), contar falhas e conferir que a mana cai pela metade. |
| 38 | O nome da magia precisa vir entre apóstrofos; senão `Spell names must be enclosed in the Holy Magic Symbols: '`. Conjuração só para PCs (`if (IS_NPC(ch)) return;`). | Testado (código) | `src/spell_parser.c:510,517,529` | Digitar `cast magic missile` sem apóstrofos. |
| 39 | Sala com `ROOM_NOMAGIC`: `Your magic fizzles out and dies.`. Sala com `ROOM_PEACEFUL` + magia violenta: `A flash of white light fills the room, dispelling your violent magic!` | Testado (código) | `src/spell_parser.c:214-215`, `src/spell_parser.c:219-220` | Achar uma sala "no magic" (ex.: algumas salas de templo/guild) e tentar conjurar. |
| 40 | `word of recall` (#42): leva ao `mortal_start_room`; só afeta alvo **não-NPC**; mana 20→10 (change 2); nível mín. clérigo **12**; posição mínima **`POS_FIGHTING`** (funciona em combate); alvo `TAR_CHAR_ROOM` (pode ser lançada em outro). | Testado / Provável (destino) | `src/spells.c:71-81`; `src/spell_parser.c:957`; `src/class.c:1673`; `src/config.c:171` (`mortal_start_room = 3001`) | Conjurar em si e em outro jogador da sala e ver para onde vão; conferir se funciona em combate. O número **3001** é config do mundo = *Provável*. |
| 41 | `identify` (#201) **não é conjurável**: `do_cast` rejeita `spellnum > MAX_SPELLS` (130) e o `spello` dele usa mana 0 e `min_level = LVL_IMMORT` para todas as classes. Só existe via pergaminho/varinha/cajado/poção. | Testado (código) | `src/spell_parser.c:537-538`; `src/spell_parser.c:677-678` e `964`; `src/spells.h:91` e `115` | `cast 'identify' item` → `Cast what?!?`. Usar um pergaminho/varinha de identify → funciona. |
| 42 | `identify` revela: tipo do item, "Item is: <extra bits>", peso/valor/rent, as abilities (`GET_OBJ_AFFECT` como bitvector), e **por tipo**: magias de scroll/potion; magia + cargas máximas/restantes de wand/staff; `Damage Dice is 'XdY'` + média por rodada (arma); `AC-apply is N` (armadura); e a lista `Affects: <APPLY_x> By N`. Em criatura, mostra nome/idade/altura/peso/nível/HP/mana/AC/hitroll/damroll/atributos. | Testado (código) | `src/spells.c:256,264,266,291,295,300,304,312,316,320-328` | Usar pergaminho de identify numa arma, numa armadura e em si mesma; comparar com as linhas do texto. |
| 43 | `invisibility` é derrotada por `AFF_DETECT_INVIS` (magia `detect invisibility`); `hide` é derrotado por `AFF_SENSE_LIFE`; imortais com holylight veem tudo. | Testado (código) | `src/utils.h:427-429,431,433,439-441` | Ficar invisível e pedir para outro conjurar `detect invisibility`; conferir que ele passa a ver/te mirar. |
| 44 | Quem não vê a personagem invisível vê `someone` no lugar do nome (`PERS`), e ela desaparece do `who` (`!CAN_SEE(ch, tch)`). | Testado (código) | `src/utils.h:468`; `src/act.informative.c:1040` | `look` na sala com outra pessoa invisível sem detect; rodar `who` com alguém invisível. |
| 45 | A invisibilidade **acaba no primeiro dano causado**: `damage()` chama `appear()`, que remove `AFF_INVISIBLE` e o afeto de `SPELL_INVISIBLE`. | Testado (código) | `src/fight.c:722`; `src/fight.c:87-92` | Ficar invisível, bater uma vez e rodar `affects`/`score`. |
| 46 | Não há nenhuma checagem de `AFF_INVISIBLE` em `shop.c` nem em comandos de comércio: a invisibilidade só bloqueia **mira por nome** (comandos que usam `get_char_vis`/`CAN_SEE`, ex. `give`, `cast`). | Testado (código) | busca global por `AFF_INVISIBLE`: só em `fight.c:92,722`, `magic.c:411`, `utils.h:428`, `structs.h:222`, `act.other.c:338`, `act.wizard.c:1325`, `act.informative.c:273,297,783,1068` | `list`/`buy`/`sell` funcionam normalmente invisível; `give` para outra pessoa falha enquanto invisível. |
| 47 | `earthquake` é a **única** magia de área implementada (`MAG_AREAS`); `mag_masses()` não tem nenhuma magia. Área pula: conjurador, imortais, PCs (se não há PK) e pets charmed. | Testado (código) | `src/magic.c:616-661` (função) e skips em `src/magic.c:650-657`; `src/magic.c:593`; `src/spell_parser.c:856` | `cast 'earthquake'` num grupo com pet e com outro jogador: o pet e o outro PC não tomam dano. |
| 48 | No enum existem magias **sem `spello()`**, logo sem nome real (viram `!UNUSED!`) e impossíveis de conjurar: `SPELL_VENTRILOQUATE` (41) e `SPELL_GROUP_RECALL` (49). `SPELL_CONTROL_WEATHER` (11) existe no `spello` mas o `switch` de `MAG_MANUAL` de `call_magic` não tem `case` para ela → não faz nada. | Testado (código) | `src/spells.h:79,87`; `src/spell_parser.c:692-702`; `src/spell_parser.c:803-804`; `src/spell_parser.c:273-283` | `cast 'group recall'` e `cast 'ventriloquate'` → `Cast what?!?`; `cast 'control weather'` → consome mana e não faz nada. |
| 49 | `enchant weapon`: só em arma **não mágica** e sem nenhuma afinidade; dá `+1` hitroll (`+2` se nível ≥ 18) e `+1` damroll (`+2` se nível ≥ 20); marca `ITEM_MAGIC` e `ANTI_EVIL`/`ANTI_GOOD` conforme alinhamento. Mana 150→100, change 10, nível mín. mago 26. | Testado (código) | `src/spells.c:340-371`; `src/spell_parser.c:859`; `src/class.c:1652` | Encantar a mesma arma duas vezes: a segunda deve falhar silenciosamente. |
| 50 | `charm person`: duração = `24 * 2 * CHA(conjurador) / INT(vítima)`; bloqueado por `AFF_SANCTUARY` no alvo, `MOB_NOCHARM`, save `SAVING_PARA` e summon-protection. | Testado (código) | `src/spells.c:196-243` (sanctuary em `207`; save em `220`; `af.duration` em `229-233`) | Enfeitiçar o mesmo NPC com CHA alta e CHA baixa e comparar a duração. |
| 51 | Cura: `cure light` = `1d8+1+nível/4`; `cure critic` = `3d8+3+nível/4`; `heal` = `100 + 3d8`. Cura é limitada ao HP máximo do alvo. | Testado (código) | `src/magic.c:805,809,813`; `src/magic.c:817` | Medir HP antes/depois das três curas em níveis diferentes. |
| 52 | `group armor` e `group heal` reusam exatamente `spell_armor` e `SPELL_HEAL`; exigem estar em grupo. `group recall` está implementado em `perform_mag_groups` mas a magia não existe no `spello` (#48). | Testado (código) | `src/magic.c:528-540`; `src/spell_parser.c:493` | `cast 'group heal'` fora de grupo → `You can't cast this spell if you're not in a group!`. |
| 53 | `bless` também pode ser lançado em **objeto** (`MAG_ALTER_OBJS`): marca `ITEM_BLESS` se o peso ≤ `5 × nível`; `curse` em objeto marca `ITEM_NODROP` e **reduz em 1 o dado de dano** da arma. | Testado (código) | `src/magic.c:883-895`; `src/spell_parser.c:772,828` | Encantar/amaldiçoar uma arma e conferir com `identify`. |
| 54 | `protection from evil` só põe a flag `AFF_PROTECT_EVIL` por 24 h — **nenhum cálculo de dano no `fight.c` consulta essa flag**. | Testado (código) | `src/magic.c:431-434`; busca por `AFF_PROTECT_EVIL` (só `magic.c`) | Bater com um monstro maligno com e sem a magia: o dano deve ser idêntico (a magia é, no engine, inócua). |

---

## 2. Magias ofensivas — números completos

Colunas: **#** = número do enum (`spells.h`); **mana** = `max→min` e `change` do `spello`
(`spell_parser.c`); **nível** = nível mínimo por classe (`class.c`); **posição** = `min_position`;
**alvos/violenta** = linha seguinte ao `spello`. Dano: `MdN+K` = M dados de N faces + K.

| Magia | # | Dano (mago / outras classes) | mana (max→min /change) | nível mín. | posição mín. | alvos | violenta? | Fonte |
|---|---|---|---|---|---|---|---|---|
| `magic missile` | 32 | `1d8+1` / `1d6+1` (2–9 / 2–7) | 25→10 / 3 | mago 1 | FIGHTING | CHAR_ROOM \| FIGHT_VICT | sim | `magic.c:180,182`; `spell_parser.c:903-904`; `class.c:1631` |
| `burning hands` | 5 | `3d8+3` / `3d6+3` (6–27 / 6–21) | 30→10 / 3 | mago 5 | FIGHTING | CHAR_ROOM \| FIGHT_VICT | sim | `magic.c:186,188`; `spell_parser.c:779-780`; `class.c:1638` |
| `chill touch` | 8 | `1d8+1` / `1d6+1` **+ −1 STR** | 30→10 / 3 | mago 3 | FIGHTING | CHAR_ROOM \| FIGHT_VICT | sim | `magic.c:180,182,302-307`; `spell_parser.c:791-792`; `class.c:1634` |
| `shocking grasp` | 37 | `5d8+5` / `5d6+5` (10–45 / 10–35) | 30→15 / 3 | mago 7 | FIGHTING | CHAR_ROOM \| FIGHT_VICT | sim | `magic.c:192,194`; `spell_parser.c:933-934`; `class.c:1641` |
| `lightning bolt` | 30 | `7d8+7` / `7d6+7` (8–63 / 8–49) | 30→15 / 1 | mago 9 | FIGHTING | CHAR_ROOM \| FIGHT_VICT | sim | `magic.c:198,200`; `spell_parser.c:895-896`; `class.c:1643` |
| `color spray` | 10 | `9d8+9` / `9d6+9` (18–81 / 18–63) | 30→15 / 3 | mago 11 | FIGHTING | CHAR_ROOM \| FIGHT_VICT | sim | `magic.c:204,206`; `spell_parser.c:799-800`; `class.c:1646` |
| `fireball` | 26 | `11d8+11` / `11d6+11` (22–99 / 22–77) | 40→30 / 2 | mago 15 | FIGHTING | CHAR_ROOM \| FIGHT_VICT | sim | `magic.c:210,212`; `spell_parser.c:871-872`; `class.c:1650` |
| `call lightning` | 6 | `7d8+7` (8–63, sempre) | 40→25 / 3 | clérigo 15 | FIGHTING | CHAR_ROOM \| FIGHT_VICT | sim | `magic.c:239`; `spell_parser.c:783-784`; `class.c:1678` |
| `harm` | 27 | `8d8+8` (16–72) | 75→45 / 3 | clérigo 19 | FIGHTING | CHAR_ROOM \| FIGHT_VICT | sim | `magic.c:243`; `spell_parser.c:879-880`; `class.c:1682` |
| `dispel evil` | 22 | `6d8+6` (12–54) | 40→25 / 3 | clérigo 14 | FIGHTING | CHAR_ROOM \| FIGHT_VICT | sim | `magic.c:216-224`; `spell_parser.c:847-848`; `class.c:1675` |
| `dispel good` | 46 | `6d8+6` (12–54) | 40→25 / 3 | clérigo 14 | FIGHTING | CHAR_ROOM \| FIGHT_VICT | sim | `magic.c:226-232`; `spell_parser.c:851-852`; `class.c:1676` |
| `energy drain` | 25 | **100 fixo** se nível do alvo ≤ 2; senão `1d10` | 40→25 / 1 | mago 13 | FIGHTING | CHAR_ROOM \| FIGHT_VICT | sim | `magic.c:246-250`; `spell_parser.c:863-864`; `class.c:1647` |
| `earthquake` **(área)** | 23 | `2d8 + nível` (única magia que escala!) | 40→25 / 3 | clérigo 12 | FIGHTING | IGNORE (sala toda) | sim | `magic.c:255`; `magic.c:616-661`; `spell_parser.c:855-856`; `class.c:1674` |

**Regras comuns a todas** (linhas citadas acima): após o cálculo, `if (mag_savingthrow(...)) dam /= 2;`
(`magic.c:262-263`) e depois `damage()` aplica o teto de 100 (`fight.c:737`) e o corte de sanctuary
(`fight.c:726-727`). Nenhuma delas é `MAG_AREAS` exceto `earthquake`.

**Observações de "dano especial"** (`magic.c:216-232`): `dispel evil` lançado por conjurador
**maligno** volta contra ele (`victim = ch; dam = GET_HIT(ch) - 1`) e é anulado se o alvo for bom
(`The gods protect $N.`); `dispel good` é o espelho disso.

---

## 3. Magias de afeto / suporte — efeito e duração

Duração em **horas de jogo** (1 hora = 1 chamada de `affect_update`, ~75 s reais — #22).

| Magia | # | Efeito exato | Duração (horas) | Acumula? | mana (max→min/chg) | nível mín. | posição | Fonte |
|---|---|---|---|---|---|---|---|---|
| `armor` | 1 | `APPLY_AC -20` | 24 | duração sim, modificador **não** | 30→15 / 3 | mago 4 / clérigo 1 | **FIGHTING** | `magic.c:312-316`; `handler.c:344-351`; `spell_parser.c:767`; `class.c:1637,1657` |
| `bless` | 3 | `APPLY_HITROLL +2`, `APPLY_SAVING_SPELL -1` | 6 | duração sim | 35→5 / 3 | clérigo 5 | STANDING | `magic.c:320-329`; `spell_parser.c:771`; `class.c:1663` |
| `blindness` | 4 | `HITROLL -4`, `AC +40`, flag `AFF_BLIND`; save anula | 2 | não (`NOEFFECT` se repetida) | 35→25 / 1 | mago 9 / clérigo 6 | STANDING | `magic.c:333-347`; `spell_parser.c:775`; `class.c:1644,1665` |
| `curse` | 17 | `HITROLL -1`, `DAMROLL -1`, flag `AFF_CURSE`; save anula | `1 + nível/2` | duração e valor sim | 80→50 / 2 | mago 14 | STANDING | `magic.c:353-370`; `spell_parser.c:827`; `class.c:1648` |
| `detect invisibility` | 19 | flag `AFF_DETECT_INVIS` | `12 + nível` | duração sim | 20→10 / 2 | mago 2 / clérigo 6 | STANDING | `magic.c:382-385`; `spell_parser.c:835`; `class.c:1632,1664` |
| `detect magic` | 20 | flag `AFF_DETECT_MAGIC` | `12 + nível` | duração sim | 20→10 / 2 | mago 2 | STANDING | `magic.c:389-392`; `spell_parser.c:839`; `class.c:1633` |
| `detect alignment` | 18 | flag `AFF_DETECT_ALIGN` | `12 + nível` | duração sim | 20→10 / 2 | clérigo 4 | STANDING | `magic.c:375-378`; `spell_parser.c:831`; `class.c:1661` |
| `infravision` | 50 | flag `AFF_INFRAVISION` | `12 + nível` | duração sim | 25→10 / 1 | mago 3 / clérigo 7 | STANDING | `magic.c:396-399`; `spell_parser.c:887`; `class.c:1635,1666` |
| `invisibility` | 29 | flag `AFF_INVISIBLE` + `APPLY_AC -40` | `12 + nível/4` | duração sim | 35→25 / 1 | mago 4 | STANDING | `magic.c:407-412`; `spell_parser.c:891`; `class.c:1636` |
| `poison` | 33 | `APPLY_STR -2`, flag `AFF_POISON`; save anula | **= nível do conjurador** | não | 50→20 / 3 | mago 14 / clérigo 8 | STANDING | `magic.c:417-426`; `spell_parser.c:907-909`; `class.c:1649,1668` |
| `protection from evil` | 34 | flag `AFF_PROTECT_EVIL` (sem efeito mecânico no `fight.c`) | 24 | duração sim | 40→10 / 3 | clérigo 8 | STANDING | `magic.c:431-434`; `spell_parser.c:912`; `class.c:1667` |
| `sanctuary` | 36 | flag `AFF_SANCTUARY` (÷2 no dano recebido) | **4** | duração sim | 110→85 / 5 | clérigo 15 | STANDING | `magic.c:438-442`; `fight.c:726-727`; `spell_parser.c:925`; `class.c:1677` |
| `sense life` | 44 | flag `AFF_SENSE_LIFE` | `= nível do conjurador` | duração sim | 20→10 / 2 | clérigo 18 | STANDING | `magic.c:478-481`; `spell_parser.c:929`; `class.c:1681` |
| `sleep` | 38 | flag `AFF_SLEEP` + posição → dormindo; save anula | `4 + nível/4` | não | 40→25 / 5 | mago 8 | STANDING | `magic.c:447-456`; `spell_parser.c:937`; `class.c:1642` |
| `strength` | 39 | `APPLY_STR +1` (`+2` se nível > 18) | `nível/2 + 4` | duração e valor sim | 35→30 / 1 | mago 6 | STANDING | `magic.c:465-473`; `spell_parser.c:941`; `class.c:1640` |
| `waterwalk` | 51 | flag `AFF_WATERWALK` | 24 | duração sim | 40→20 / 2 | (sem classe no 3.1) | STANDING | `magic.c:484-487`; `spell_parser.c:953` |

**Magias de afeto que NÃO são conjuráveis por PC mago/clérigo no 3.1 stock:**
`waterwalk` (51) não aparece em `init_spell_levels` (`class.c:1628-1699`) → só via item.

**Curas** (`magic.c:798-819`, `spell_parser.c:815-824,883-884`):

| Magia | # | Cura | mana | nível mín. | posição |
|---|---|---|---|---|---|
| `cure light` | 16 | `1d8+1 + nível/4` | 30→10 / 2 | clérigo 1 | FIGHTING |
| `cure critic` | 15 | `3d8+3 + nível/4` | 30→10 / 2 | clérigo 9 | FIGHTING |
| `heal` | 28 | `100 + 3d8` (103–124) | 60→40 / 3 | clérigo 16 | FIGHTING |

(`heal` também remove `blindness`: `magic.c:833-841`. O total é limitado ao HP máximo —
`GET_HIT(victim) = MIN(GET_MAX_HIT(victim), ...)`, `magic.c:817`.)

---

## 4. Lista completa das magias do engine (`spells.h`, enum 1–51 + 201–206)

`spells.h` define `SPELL_*` de 1 a 51 (`MAX_SPELLS = 130`, `spells.h:91`) e as magias
"não-jogador/objeto" de 201 a 206. Número do enum e linha em `src/spells.h`:

`armor` **1** @39 · `teleport` **2** @40 · `bless` **3** @41 · `blindness` **4** @42 ·
`burning hands` **5** @43 · `call lightning` **6** @44 · `charm` **7** @45 · `chill touch` **8** @46 ·
`clone` **9** @47 · `color spray` **10** @48 · `control weather` **11** @49 · `create food` **12** @50 ·
`create water` **13** @51 · `cure blind` **14** @52 · `cure critic` **15** @53 · `cure light` **16** @54 ·
`curse` **17** @55 · `detect alignment` **18** @56 · `detect invisibility` **19** @57 ·
`detect magic` **20** @58 · `detect poison` **21** @59 · `dispel evil` **22** @60 · `earthquake` **23** @61 ·
`enchant weapon` **24** @62 · `energy drain` **25** @63 · `fireball` **26** @64 · `harm` **27** @65 ·
`heal` **28** @66 · `invisibility` **29** @67 · `lightning bolt` **30** @68 · `locate object` **31** @69 ·
`magic missile` **32** @70 · `poison` **33** @71 · `protection from evil` **34** @72 ·
`remove curse` **35** @73 · `sanctuary` **36** @74 · `shocking grasp` **37** @75 · `sleep` **38** @76 ·
`strength` **39** @77 · `summon` **40** @78 · `ventriloquate` **41** @79 (sem `spello` → `!UNUSED!`) ·
`word of recall` **42** @80 · `remove poison` **43** @81 · `sense life` **44** @82 ·
`animate dead` **45** @83 · `dispel good` **46** @84 · `group armor` **47** @85 · `group heal` **48** @86 ·
`group recall` **49** @87 (sem `spello` → `!UNUSED!`) · `infravision` **50** @88 · `waterwalk` **51** @89.

Não-jogador/objeto: `identify` **201** @115, `fire breath` **202** @116, `gas breath` **203** @117,
`frost breath` **204** @118, `acid breath` **205** @119, `lightning breath` **206** @120.
As cinco "breath" têm `spello` com mana 0 e rotinas 0 (`spell_parser.c:973-990`) → existem no nome,
não fazem nada.

Habilidades (não-magias) começam em 131: `backstab` 131 @94, `bash` 132 @95, `hide` 133 @96,
`kick` 134 @97, `pick lock` 135 @98, `rescue` 137 @100, `sneak` 138 @101, `steal` 139 @102,
`track` 140 @103.

**Magias que o DeBo "poderia ter" e que existem no engine:** `blindness` (4), `curse` (17),
`dispel evil` (22), `earthquake` (23), `energy drain` (25), `fireball` (26), `harm` (27),
`chill touch` (8), `shocking grasp` (37), `color spray` (10), `sleep` (38), `poison` (33),
`call lightning` (6), `protection from evil` (34), `detect magic/alignment/invisibility` (20/18/19),
`sense life` (44), `charm` (7), `clone` (9), `animate dead` (45), `summon` (40), `teleport` (2),
`locate object` (31), `create food/water` (12/13), `enchant weapon` (24), `remove curse/poison` (35/43),
`group armor/heal` (47/48), `infravision` (50), `waterwalk` (51).

---

## 5. Detalhes técnicos (trechos citados)

### 5.1 Dano (`mag_damage`)
```c
case SPELL_LIGHTNING_BOLT:
    if (IS_MAGIC_USER(ch)) dam = dice(7, 8) + 7; else dam = dice(7, 6) + 7;
```
(`src/magic.c:196-200` — nenhuma menção a `level` exceto em `earthquake`, `src/magic.c:254-255`.)

### 5.2 Save
```c
save = saving_throws(class_sav, type, GET_LEVEL(ch));
save += GET_SAVE(ch, type); save += modifier;
if (MAX(1, save) < rand_number(0, 99)) return (TRUE);
```
(`src/magic.c:62-68`; `modifier` = 0 em toda conjuração de magia, `src/magic.c:262`.)

### 5.3 Duração e expiração
```c
if (af->duration >= 1) af->duration--;
else { ... send_to_char(i, "%s\r\n", spell_info[af->type].wear_off_msg); affect_remove(i, af); }
```
(`src/magic.c:84-95`.) Chamado em `src/comm.c:846-848`, no bloco
`if (!(pulse % (SECS_PER_MUD_HOUR * PASSES_PER_SEC)))` → **1 tick = 1 hora de jogo**
(`SECS_PER_MUD_HOUR 75`, `src/utils.h:120`).

### 5.4 Acumulação de afeto
```c
if (add_dur) af->duration += hjp->duration;
if (avg_dur) af->duration /= 2;
if (add_mod) af->modifier += hjp->modifier;
```
(`src/handler.c:344-351`.) `mag_affects` chama `affect_join(victim, af+i, accum_duration, FALSE, accum_affect, FALSE)`
(`src/magic.c:515`), ou seja: **duração soma; valor só soma se `accum_affect`** (apenas `curse` e `strength`).

### 5.5 AC e combate
```c
int armorclass = GET_AC(ch);
if (AWAKE(ch)) armorclass += dex_app[GET_DEX(ch)].defensive * 10;
return (MAX(-100, armorclass));
```
(`src/fight.c:102-109`.)
```c
victim_ac = compute_armor_class(victim) / 10;
... dam = (calc_thaco - diceroll <= victim_ac);
```
(`src/fight.c:891` e `src/fight.c:909`.) `diceroll == 20` ou alvo dormindo = acerto automático;
`diceroll == 1` = erro automático (`src/fight.c:904-907`). **AC não entra no dano.**

### 5.6 Invisibilidade (quem vê quem)
```c
#define INVIS_OK(sub, obj) \
 ((!AFF_FLAGGED((obj),AFF_INVISIBLE) || AFF_FLAGGED(sub,AFF_DETECT_INVIS)) && \
 (!AFF_FLAGGED((obj), AFF_HIDE) || AFF_FLAGGED(sub, AFF_SENSE_LIFE)))
#define MORT_CAN_SEE(sub, obj) (LIGHT_OK(sub) && INVIS_OK(sub, obj))
#define IMM_CAN_SEE(sub, obj) \
   (MORT_CAN_SEE(sub, obj) || (!IS_NPC(sub) && PRF_FLAGGED(sub, PRF_HOLYLIGHT)))
#define CAN_SEE(sub, obj) (SELF(sub, obj) || \
   IMM_CAN_SEE(sub, obj)))
```
(`src/utils.h:427-429`, `431`, `433-434`, `439` e `441`; a linha intermediária do `CAN_SEE` não foi
capturada pela busca e encadeia `MORT_CAN_SEE`.) `PERS()` mostra `someone` para quem não vê
(`src/utils.h:468`); `who` pula (`src/act.informative.c:1040`); dano causado chama `appear()`
(`src/fight.c:722`).

### 5.7 Palavra de recall
```c
ASPELL(spell_recall) { if (victim == NULL || IS_NPC(victim)) return;
  char_to_room(victim, r_mortal_start_room); ... }
```
(`src/spells.c:71-81`.) Destino = `mortal_start_room`, default **3001** (`src/config.c:171`),
resolvido em `src/db.c:1019`. Não há checagem de sala/nível **dentro** da função: os limites são
`min_level` (clérigo 12, `src/class.c:1673`), mana (`src/spell_parser.c:957`) e `ROOM_NOMAGIC`.

### 5.8 Conjuração: lag e restrições
```c
if (rand_number(0, 101) > GET_SKILL(ch, spellnum)) { WAIT_STATE(ch, PULSE_VIOLENCE);
  ... GET_MANA(ch) - (mana / 2); }
else if (cast_spell(ch, tch, tobj, spellnum)) { WAIT_STATE(ch, PULSE_VIOLENCE); ... - mana; }
```
(`src/spell_parser.c:626-638`.) `PULSE_VIOLENCE = 2 RL_SEC` = **2 s reais** (`src/structs.h:480`).

```c
if (GET_POS(ch) < SINFO.min_position) {
  ... case POS_FIGHTING: "Impossible!  You can't concentrate enough!\r\n"
```
(`src/spell_parser.c:461-476`.) Com `POS_FIGHTING = 7` e `POS_STANDING = 8` (`src/structs.h:148-149`),
magias de posição `POS_STANDING` (ex.: `sanctuary`, `invisibility`, `bless`, `strength`, `sleep`,
`poison`, `curse`) **não podem** ser conjuradas em combate; as de `POS_FIGHTING`
(`armor`, `magic missile`, `lightning bolt`, `fireball`, `word of recall`…) podem.

### 5.9 identify
```c
send_to_char(ch, "You feel informed:\r\nObject '%s', Item type: %s\r\n", obj->short_description, bitbuf);
send_to_char(ch, "Damage Dice is '%dD%d' for an average per-round damage of %.1f.\r\n", ...);
send_to_char(ch, "AC-apply is %d\r\n", GET_OBJ_VAL(obj, 0));
```
(`src/spells.c:256`, `src/spells.c:300`, `src/spells.c:304`.)

### 5.10 Onde ficam os custos de mana
```c
return MAX(SINFO.mana_max - (SINFO.mana_change * (GET_LEVEL(ch) - SINFO.min_level[(int) GET_CLASS(ch)])), SINFO.mana_min);
```
(`src/spell_parser.c:89-91`.) Os três parâmetros vêm do `spello()` de cada magia
(`src/spell_parser.c:679-681`); `min_level[classe]` vem de `init_spell_levels()` em
`src/class.c:1628-1699` (o `spello` antes preenche todos com `LVL_IMMORT` = 31, `src/spell_parser.c:677-678`,
`src/structs.h:458`).

---

## 6. Limites desta pesquisa

1. **Versão:** o código analisado é o commit único identificado como *"Initial commit of 3.1"*.
   Não foi feita comparação com um tarball 3.0. Onde o comportamento pode ter mudado entre 3.0 e 3.1
   (tabelas de save em `class.c`, `MAG_*`/`TAR_*` em `spells.h`, ganho de mana), a afirmação está
   marcada como **Provável**.
2. **Fonte dos números de linha:** as linhas vêm da API de busca do Sourcegraph (índice no mesmo
   commit) e foram convertidas de 0-based para 1-based; foram conferidas por amostragem contra a
   cópia crua local de `src/class.c` (7 âncoras). Os demais arquivos foram validados apenas por
   consistência estrutural, não por contagem manual integral. Recomenda-se, na auditoria, abrir a
   URL crua do commit e conferir a linha citada.
3. **`class.c` truncado no fetch:** o corpo completo só estava disponível no arquivo de rascunho
   local; as citações de `class.c` foram verificadas nesse arquivo (offset de 4 linhas de cabeçalho
   do rascunho, confirmado contra o Sourcegraph).
4. **Isto prova o engine, não o DeBo.** O DeBo é declaradamente muito modificado: classes extras,
   magias de clérigo para a maga, custos/durações próprios e possivelmente `MAX_SPELLS` diferente
   são esperados. Nada aqui descreve o DeBo até ser medido lá.
5. **Configuração do mundo não é código:** `mortal_start_room` (3001), quais salas são `NO_MAGIC`
   ou `PEACEFUL`, a existência de PCs com `pk_allowed`, e a tabela de XP/mana efetiva dependem dos
   arquivos de mundo e do `config.c` do servidor — são **Provável/Dúvida** por natureza.
6. **Não foram analisados:** `src/constants.c` (nada de magia/afeto), `src/shop.c` (só foi
   verificado, por busca global, que não há `AFF_INVISIBLE` ali), `src/act.wizard.c` (comandos de
   imortal, `src/act.wizard.c:1325`), e as mensagens de combate em `lib/misc/messages`
   (`src/fight.c:139-195`) que definem os textos de acerto/erro exibidos.

---

## 7. Conflitos com hipóteses do plano de validação (`00-afirmacoes-e-validacao.md`)

Três expectativas do Bloco C do plano **não** encontram apoio no código do engine — testá-las ainda
vale, mas o resultado deve ser interpretado com cuidado:

1. **"`invisibility` e depois `list` numa loja: confirmar a recusa de comércio."**
   No engine **não há** nenhuma consulta a `AFF_INVISIBLE` em `src/shop.c` nem em comando de compra.
   A flag aparece apenas em `fight.c`, `magic.c`, `utils.h`, `structs.h`, `act.other.c`,
   `act.wizard.c` e `act.informative.c` (busca global, #46). Portanto `list` deve funcionar
   normalmente para alguém invisível; o que deve falhar é **mira por nome** (`give`, `cast`,
   `group`). Se o DeBo recusar `list` para invisíveis, isso é **modificação local do DeBo** — e é
   um achado interessante, não o contrário.
2. **"`armor` no Templo de Midgaard e tentar conjurar de novo: confirmar a hipótese de área sem
   magia."** A existência de sala sem magia depende da flag `ROOM_NOMAGIC` nos arquivos de mundo
   (`src/spell_parser.c:214-215` é só o efeito), **não** do código. Conjurar normalmente no Templo
   não contradiz o engine: apenas indica que aquela sala não está marcada no DeBo.
3. **"`recall` a partir de uma sala comum: registrar destino e custo."** No engine, `word of recall`
   é **magia de clérigo nível 12** e leva ao `mortal_start_room` (`3001` por padrão); se o DeBo
   tiver um comando `recall` de jogador (gratuito, sempre disponível), isso é implementação própria
   e a comparação de mana da tabela não se aplica.

Também vale notar: o `00` cita "último push 2021-07-19"; a API de commits mostra **um único commit**
(`parents: []`) com data de autoria **2012-03-22** e mensagem *"Initial commit of 3.1"*. As duas datas
são compatíveis (data do commit ≠ data do push ao GitHub), mas a versão do código é **3.1**, como
destacado no topo deste documento.
