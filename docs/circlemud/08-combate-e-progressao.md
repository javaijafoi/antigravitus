# 08 — COMBATE E PROGRESSÃO: a matemática do CircleMUD 3.1 (para validar no DeBo)

Documento de **afirmações verificáveis** sobre acerto, dano, HP/mana, magias ofensivas, XP, fuga e
`wimpy`, extraídas do **código-fonte** do engine — e cruzadas, onde possível, com **registros reais
do DeBo** que já existem neste repositório. O objetivo é responder com números: **"qual nível é bom
para limpar o esgoto?"**

---

## Fonte consultada

**Repositório:** <https://github.com/Yuffster/CircleMUD> (branch `master`)
**Commit:** `12a0cedbb563465029c46de9537c96854bc11610` — *"Initial commit of 3.1."*, 2012-03-22
(é o único commit do repo; o `release_notes.3.1.txt` na raiz confirma a versão 3.1).

**Método:** o tarball completo foi baixado
(`https://codeload.github.com/Yuffster/CircleMUD/tar.gz/refs/heads/master`) e extraído localmente,
de modo que **todos os números de linha** citados aqui foram lidos diretamente do arquivo, com
numeração 1-based verificada. Arquivos de código lidos:

| Arquivo | O que foi extraído |
|---|---|
| `src/fight.c` | `compute_armor_class`, `compute_thaco`, `hit`, `damage`, `die`, `solo_gain`, `group_gain`, `perform_violence` |
| `src/class.c` | `saving_throws`, `thaco`, `advance_level`, `do_start`, `level_exp`, `init_spell_levels` |
| `src/constants.c` | `str_app`, `dex_app`, `con_app` |
| `src/structs.h` | pulsos (`PULSE_VIOLENCE`), posições (`POS_*`), structs de `apply` |
| `src/spell_parser.c` | `mag_manacost`, `call_magic`, `do_cast` (custo e lag) |
| `src/magic.c` | `mag_savingthrow`, `mag_damage` (dados de dano) |
| `src/utils.c` | `rand_number`, `dice` |
| `src/db.c` | formato do arquivo `.mob`, `read_mobile`, `clear_char` (AC base) |
| `src/config.c` | `max_exp_gain`, `max_exp_loss` |
| `src/act.offensive.c` | `do_flee` |
| `src/act.other.c` | `do_wimpy` |
| `lib/world/mob/70.mob`, `72.mob` | mobs dos esgotos |
| `lib/world/zon/70.zon`…`73.zon` | o que nasce em cada sala dos esgotos |
| `lib/world/wld/70.wld` | nomes das salas |

**Registros do DeBo usados como contraprova** (dados já existentes no projeto, não inventados aqui):
`data/heroes/grebolius/ficha.md`, `hero.json`, `evolucao.md`, `monstros.md`,
`observacoes/manutencao-maquina-2026-10-15.json`, `evidence/dia91.json`, `dia92.json`, `dia93.json`,
`dia94.json`, `dia95.json`, `dia112.json`, `dia117.json`, `dia132.json`, `dia156b.json`.

> ⚠️ **AVISO (premissa do projeto):** este é o código do **CircleMUD 3.1**. O DeBo declara-se baseado
> em **3.0**. As fórmulas de `fight.c` / `magic.c` citadas aqui são idênticas no 3.0 naquilo que a
> literatura do engine documenta, mas **a correspondência 1:1 não foi verificada neste trabalho** —
> onde isso importar, a linha está marcada como **Dúvida** ou **Provável**.

---

## Limites desta pesquisa (resumo antecipado)

1. Tudo o que é **fórmula** vem do código com `arquivo:linha`. Tudo o que é **número de mundo**
   (HP, dano, XP, nível dos mobs) vem de `lib/world/mob/*.mob` — **o mundo padrão do 3.1**.
2. **O DeBo mudou o mundo.** Comparações diretas estão na §10 e mostram divergências **grandes** em
   XP de nível, em dano de cobra e em eficácia do `armor`. O veredito da §9 é sobre **o mundo padrão**.
3. Números que **não existem no código** (ex.: AC de uma maga vestida, dado da arma inicial, % de
   `GET_SKILL` por magia) **não foram estimados** — estão marcados como não encontrados.
4. Não foi medido em servidor. Nenhuma linha deste documento é "testado no DeBo".

---

## Níveis de confiança

- **Testado (código)** — está literalmente no código, com linha citada. Prova o *engine*.
- **Provável** — decorre do código somado a um dado de mundo ou a um registro do DeBo, sem margem
  de interpretação relevante.
- **Dúvida** — depende de configuração, de versão (3.0 vs 3.1), do mundo (DeBo) ou de hipótese.

---

## 1. Tabela de afirmações

| # | Afirmação | Nível | Fonte (arquivo:linha) | Como validar no DeBo |
|---|---|---|---|---|
| 1 | O ataque acerta quando `calc_thaco − d20 ≤ victim_ac`, onde `victim_ac = AC_display / 10`. | Testado (código) | `src/fight.c:909`; divisão: `src/fight.c:891` | `score` mostra a CA; somar as quedas de HP por rodada num mob conhecido e comparar com a tabela da §2. |
| 2 | `d20` é `rand_number(1,20)`: **1 = erro automático**, **20 = acerto automático**, e alvo dormindo é sempre acertado. | Testado (código) | `src/fight.c:894`, `src/fight.c:904-909` | Atacar dormindo → nunca erra. |
| 3 | O THAC0 do jogador vem de uma **tabela fixa por classe/nível** (maga: 20 no nível 1, 11 no nível 30); o do NPC é sempre **20** e o `.mob` só informa um `hitroll`. | Testado (código) | `src/class.c:1220-1262` (maga); `src/fight.c:853-855`; `src/db.c:1142` | `score` ("Acerto") e a tabela da §2. |
| 4 | `INT` e `WIS` **acertam mais**: cada uma subtrai `(atributo−13)/1.5` (truncado) do THAC0. | Testado (código) | `src/fight.c:858-859` | Comparar a CA efetiva com e sem equipamento de INT/WIS. |
| 5 | CA base de qualquer personagem novo é **100** ("Basic Armor"); a melhor CA possível é **−100**. | Testado (código) | `src/db.c:2685`; piso `src/fight.c:109` | `score` em personagem nu. |
| 6 | O dano por golpe é `str_app[STR].todam + damroll + dados(arma ou mão)`, multiplicado por posição do alvo, com mínimo de 1. | Testado (código) | `src/fight.c:918-931`, `:946-950` | Média de 20 golpes com e sem arma. |
| 7 | **Teto de dano: 100 por golpe**, aplicado depois de qualquer divisão. `sanctuary` divide o dano por 2. | Testado (código) | `src/fight.c:737`; `src/fight.c:726-727` | Nenhum golpe único passa de 100; com `sanctuary`, metade. |
| 8 | O dano das magias ofensivas de mago é **fixo por magia** e **não escala com o nível**. | Testado (código) | `src/magic.c:177-213` | Conjurar a mesma magia no nível 9 e no 25 e comparar a faixa. |
| 9 | O custo de mana **cai** com o nível: `MAX(mana_max − mana_chg×(nível−nível_min), mana_min)`. | Testado (código) | `src/spell_parser.c:88-92` | `cast` em vários níveis e ler o gasto no prompt. |
| 10 | O save do alvo **divide o dano da magia por 2**; a chance de save do mob segue a tabela **de guerreiro** (não a da classe dele). | Testado (código) | `src/magic.c:262-263`; `src/magic.c:55-62`; `src/class.c:1149-1201` | Medir a distribuição de dano de 50 `magic missile` no mesmo tipo de mob. |
| 11 | Magias **não têm rolagem de acerto**: `mag_damage` chama `damage()` direto. Só o save interfere. | Testado (código) | `src/magic.c:266`; `src/spell_parser.c:242-244` | Conjurar em alvo de CA altíssima: nunca "erra". |
| 12 | Conjurar custa **uma rodada de lag** depois da magia (`WAIT_STATE(ch, PULSE_VIOLENCE)`); a magia resolve no mesmo instante. | Testado (código) | `src/spell_parser.c:636`; `:627` (falha) | Cronometrar dois `cast` seguidos. |
| 13 | **1 rodada de combate = `PULSE_VIOLENCE` = 2 segundos reais.** | Testado (código) | `src/structs.h:474-476` (`OPT_USEC`, `PASSES_PER_SEC`, `RL_SEC`), `src/structs.h:480` | Contar segundos entre mensagens de combate. |
| 14 | Cada combatente ataca **uma vez por rodada** (`perform_violence` chama `hit` uma vez por entrada da `combat_list`). Não há múltiplos ataques em 3.1. | Testado (código) | `src/fight.c:962-996`; chamado em `src/comm.c:843-844` | Nº de linhas de ataque por rodada no log. |
| 15 | HP da maga por nível = `10 + Σ rand(3,8) + Σ con_app[CON].hitp`; a mana começa em **100 para todas as classes** e sobe no máximo **10 por nível**. | Testado (código) | `src/class.c:1473-1474`, `:1498`, `:1523`, `:1527-1532`, `:1554-1558`; `src/constants.c:620-647` | `score` nível a nível; comparar com a tabela da §4. |
| 16 | **Mana não sobe no nível 1** (só a partir do nível 2): a primeira mana extra vem no nível 2. | Testado (código) | `src/class.c:1557-1558` | Criar maga nova: 100 de mana no nível 1. |
| 17 | XP por abate (solo) = `mob_exp/3` + bônus de diferença de nível `exp × min(8, nível_mob−nível_maga)/8`. | Testado (código) | `src/fight.c:444-465` (bônus na `:454`) | Matar o mesmo mob com níveis diferentes e comparar a mensagem "You receive N experience". |
| 18 | **Bater também dá XP**: cada golpe que causa `dam` rende `nível_do_alvo × dam` de XP ao atacante. | Testado (código) | `src/fight.c:741-742` | Comparar o total de XP ganho com o dano total desferido. |
| 19 | O ganho de XP por chamada é limitado a `max_exp_gain = 100000`; a perda por morte a `max_exp_loss = 500000`. | Testado (código) | `src/config.c:72-73`; `src/limits.c:266`, `:288` | Abate de mob gigante. |
| 20 | **Morrer custa metade da XP acumulada** (`gain_exp(ch, −(GET_EXP(ch)/2))`). | Testado (código) | `src/fight.c:378-384` | `score` antes/depois de morrer. |
| 21 | `wimpy N` só aceita `N ≤ maxHP/2`; a fuga dispara quando `HP < wimpy` e `HP > 0`. | Testado (código) | `src/act.other.c:714-721`; `src/fight.c:797-801` | `wimpy 999` → recusa. |
| 22 | `flee` sorteia direções e **custa XP** (`(maxHP−HP)×nível` do oponente) quando bem-sucedido. | Testado (código) | `src/act.offensive.c:268-298` (perda em `:286-290`) | Log "You lost N experience" ao fugir. |
| 23 | Mob do arquivo `.mob`: `nível thac0 CA HPdados DANOdados` — o HP real é **`dados(HPnum, HPsize) + HPplus`**, calculado no carregamento. | Testado (código) | `src/db.c:1134-1156`; `src/db.c:1820-1824` | `consider`/medição de HP do mob. |
| 24 | A CA gravada no `.mob` é **multiplicada por 10** e o `thac0` vira `hitroll = 20 − thac0`. | Testado (código) | `src/db.c:1142-1143` | Comparar "CA" do score com a do arquivo. |
| 25 | Nos esgotos padrão os mobs vão do **nível 1** (morcego, aranha) ao **nível 19** (dragão vermelho). | Testado (código) | `lib/world/mob/70.mob:25,50,38`, `lib/world/mob/70.mob:151`; spawn em `lib/world/zon/70.zon:6-17`, `71.zon:6-15`, `72.zon:6-43`, `73.zon:6-13` | `consider` nos esgotos do DeBo. |
| 26 | O DeBo usa **outra tabela de XP de nível** e **outro dano de cobra** que o padrão 3.1 — ver §10. | Provável | `data/heroes/grebolius/evolucao.md:517`, `:912`; `evidence/dia95.json:317` vs `src/class.c:1728-1763`; `lib/world/mob/70.mob:89` | Comparar "Próximo nível" no `score` com a §7. |
| 27 | A fórmula de mana por nível reproduz **exatamente** o observado no DeBo (L11 = 170 ∈ [164,179]; L20 = 260 ∈ [254,269]). | Provável | `src/class.c:1529-1530` vs `data/heroes/grebolius/evidence/dia95.json:335` e `ficha.md:24` | Confirmar mana máxima em cada nível. |
| 28 | O `armor` do DeBo dá **±25 de CA**; o do padrão 3.1 dá **−20**. | Provável | DeBo: `evidence/dia91.json:135` ("+25 em ARMADURA") vs `src/magic.c:312-315` (`modifier = -20`) | Conjurar `armor` e ler a CA. |
| 29 | Não foi possível determinar no código a **CA de uma maga vestida** nem o **dado da arma inicial**: esses valores vêm dos arquivos `.obj`, que não foram objeto desta pesquisa. | Dúvida | não encontrado em `src/` | `score`, `equipment`. |
| 30 | O DeBo pode ter alterado `PULSE_VIOLENCE`, o teto de 100 de dano, a fórmula de XP por dano e as tabelas de save. Nada disso foi testado aqui. | Dúvida | — | Cronometrar uma rodada; medir dano > 100. |

---

## 2. Fórmula de acerto

### 2.1 A regra exata

```
diceroll  = rand_number(1, 20)                    // src/fight.c:894
victim_ac = compute_armor_class(vítima) / 10      // src/fight.c:891
calc_thaco = compute_thaco(atacante, vítima)      // src/fight.c:888

se diceroll == 20  -> ACERTO automático           // src/fight.c:904
se diceroll == 1   -> ERRO automático             // src/fight.c:906
se vítima dormindo -> ACERTO                      // src/fight.c:904
senão: ACERTO se (calc_thaco - diceroll <= victim_ac)   // src/fight.c:909
```

`compute_armor_class` (`src/fight.c:102-110`):

```
ac = GET_AC(ch)                                   // base 100 (src/db.c:2685)
se acordado: ac += dex_app[DEX].defensive * 10    // src/fight.c:107
ac = MAX(-100, ac)                                // src/fight.c:109
```

`compute_thaco` (`src/fight.c:848-862`):

```
se jogador: calc = thaco(classe, nível)           // src/fight.c:853 -> src/class.c:1220
se NPC    : calc = 20                             // src/fight.c:855
calc -= str_app[STR].tohit                        // src/fight.c:856
calc -= GET_HITROLL                               // src/fight.c:857  (arma/magia)
calc -= (int)((INT - 13) / 1.5)                   // src/fight.c:858
calc -= (int)((WIS - 13) / 1.5)                   // src/fight.c:859
```

### 2.2 O que entra no THAC0 da maga

| Componente | Onde | Valor |
|---|---|---|
| Tabela de classe/nível | `src/class.c:1220-1262` | 20 (nv 1–3); 19 (4–6); 18 (7–9); **17 (10–12)**; 16 (13–15); 15 (16–18); 14 (19–21); 13 (22–24); 12 (25–27); 11 (28–30) |
| Força | `src/constants.c:519-551` | `tohit` 0 com STR 8–15; +1 com STR 16–18; −1 com STR 6 |
| `hitroll` (arma + bênçãos) | `src/fight.c:857` | o que o equipamento somar |
| INT | `src/fight.c:858` | `−(INT−13)/1.5` truncado: INT 19 → −4 |
| WIS | `src/fight.c:859` | `−(WIS−13)/1.5` truncado: WIS 17 → −2 |

**Exemplo de Grebolius (nível 11, INT 18→19, WIS 16→17, STR 10–12, hitroll 1–3):**
`calc = 17 (tabela) − 0 (STR) − 1 (hitroll) − 4 (INT 19) − 2 (WIS 17) = 10`.

### 2.3 Probabilidade de acerto em função de `need = calc_thaco − victim_ac`

Como `diceroll ∈ [2,19]` é testado e 1/20 são automáticos, vale a forma fechada:

> **P(acerto) = min(19, max(1, 21 − need)) / 20**

| `need` | ≤2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 | 13 | 14 | 15 | 16 | 17 | 18 | 19 | ≥20 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| **P(acerto)** | 95% | 90% | 85% | 80% | 75% | 70% | 65% | 60% | 55% | 50% | 45% | 40% | 35% | 30% | 25% | 20% | 15% | 10% | **5%** |

### 2.4 A pergunta do enunciado: **atacante de nível 11 contra alvo de CA 0**

CA 0 no `score` → `victim_ac = 0/10 = 0`.

- **Maga "crua"** (sem bônus de INT/WIS/STR/hitroll): `calc = 17` (tabela, `src/class.c:1236`).
  `need = 17 − 0 = 17` → **P = 20% (4 em 20)**.
- **Maga com INT 19 e WIS 17** (`−4 −2 = −6`): `calc = 11`. `need = 11` → **P = 50% (10 em 20)**.

### 2.5 Chance de acerto da maga por nível (com INT 19 / WIS 17, sem hitroll)

`calc_thaco = thaco_tabela − 6`:

| Nível | 1–3 | 4–6 | 7–9 | **10–12** | 13–15 | 16–18 | 19–21 | 22–24 | 25–30 |
|---|---|---|---|---|---|---|---|---|---|
| `calc_thaco` | 14 | 13 | 12 | **11** | 10 | 9 | 8 | 7 | ≤6 |
| vs CA 100 (`victim_ac` 10) | 45% | 50% | 55% | **60%** | 65% | 70% | 75% | 80% | 95% |
| vs CA 50 (`victim_ac` 5) | 65% | 70% | 75% | **80%** | 85% | 90% | 95% | 95% | 95% |
| vs CA 0 (`victim_ac` 0) | 40% | 45% | 50% | **55%** | 60% | 65% | 70% | 75% | 95% |
| vs CA −50 (`victim_ac` −5) | 25% | 30% | 35% | **40%** | 45% | 50% | 55% | 60% | 80% |

*(Para a maga crua, some 6 a `need`: nível 11 vs CA 0 → 20%, não 55%.)*

### 2.6 Chance de acerto dos mobs dos esgotos

Mob NPC: `STR = 11` (`src/db.c:1122`) → `tohit = 0`; `GET_HITROLL = 20 − thac0_do_arquivo`
(`src/db.c:1142`); INT 11 e WIS 11 → cada um vale `+1`. **Logo `calc_thaco = thac0_do_arquivo + 2`.**

Sewer rat (`lib/world/mob/70.mob:38`, `thac0 16`): `calc = 18`.
Contra uma maga com `victim_ac = 5` (CA 50): `need = 13` → **40%**.

| Mob (arquivo:linha) | Nv | `thac0` | `calc` | Dano/golpe (dados) | % vs CA 100 | % vs CA 50 | % vs CA 20 |
|---|---|---|---|---|---|---|---|
| Morcego `70.mob:25` | 1 | 20 | 22 | 1d5 (1–5) | 45% | 20% | 10% |
| Aranha `70.mob:50` | 1 | 20 | 22 | 1d4 (1–4) | 45% | 20% | 10% |
| Rato do esgoto `70.mob:38` | 5 | 16 | 18 | 2d4 (2–8) | 65% | 40% | 30% |
| Larva gigante `70.mob:75` | 3 | 17 | 19 | 1d7 (1–7) | 60% | 35% | 25% |
| Cobra `70.mob:89` | 4 | 16 | 18 | 1d9 (1–9) | 65% | 40% | 30% |
| Besouro `70.mob:63` | 8 | 13 | 15 | 2d4+2 (4–10) | 80% | 55% | 45% |
| Ettin Herald `70.mob:231` | 6 | 14 | 16 | 1d8 (1–8) | 75% | 50% | 40% |
| Ettin Jones `70.mob:218` | 10 | 11 | 13 | 2d6+2 (4–14) | 90% | 65% | 55% |
| Monstro de lama `70.mob:12` | 12 | 9 | 11 | 2d5+3 (5–13) | 95% | 75% | 65% |
| Chr-eff'n `70.mob:138` | 12 | 9 | 11 | 2d7+1 (3–15) | 95% | 75% | 65% |
| Naga `70.mob:178` | 12 | 9 | 11 | 2d7+1 (3–15) | 95% | 75% | 65% |
| Rato gigante `72.mob:61` | 12 | 9 | 11 | 2d6+2 (4–14) | 95% | 75% | 65% |
| Basilisco `70.mob:191` | 13 | 11 | 13 | 2d7+2 (4–16) | 90% | 65% | 55% |
| Mindflayer mestre `72.mob:11` | 14 | 7 | 9 | 3d4+4 (7–16) | 95% | 85% | 75% |
| Bruxa do mar `70.mob:164` | 14 | 7 | 9 | 2d8+1 (3–17) | 95% | 85% | 75% |
| **Dragão vermelho** `70.mob:151` | **19** | **2** | **4** | 3d6+3 (6–21) | 95% | **95%** | 95% |

> Note o **achatamento**: contra CA ≤ 20 o dragão acerta 95% das vezes **mesmo em nível baixo** —
> a CA só compra sobrevida contra mobs de `thac0` alto (morcego, aranha, rato), não contra os bichos
> de `thac0` 2–9.

---

## 3. Fórmula de dano por golpe

### 3.1 `hit()` — quem bate com arma/mão

```
dam  = str_app[STR].todam                      // src/fight.c:918  (src/constants.c:519-551)
dam += GET_DAMROLL                             // src/fight.c:919
se arma empunhada:
    dam += dice(valor[1], valor[2])            // src/fight.c:924  (dados da arma)
senão se NPC:
    dam += dice(damnodice, damsizedice)        // src/fight.c:928  (dados do .mob)
senão (jogador desarmado):
    dam += rand_number(0, 2)                   // src/fight.c:930  (máx. 2 na mão)

se POS(vítima) < POS_FIGHTING:                 // src/fight.c:946
    dam *= 1 + (POS_FIGHTING - POS(vítima)) / 3   // sentado ×1,33; dormindo ×2; imóvel ×2,66
dam = MAX(1, dam)                              // src/fight.c:950
se backstab: dam *= backstab_mult(nível)       // src/fight.c:952-953
```

Multiplicadores por posição (o próprio código documenta em `src/fight.c:933-945`; `POS_FIGHTING = 7`,
`POS_STANDING = 8` em `src/structs.h:148-149`): sentado 1,33× · descansando 1,66× · dormindo 2,00× ·
atordoado 2,33× · incapacitado 2,66× · mortalmente ferido 3,00×.

### 3.2 `damage()` — onde o dano é **cortado**

```
se AFF_SANCTUARY e dam >= 2: dam /= 2          // src/fight.c:726-727   <<< o "/2"
se pk_allowed == NO e atacante é PK: dam = 0   // src/fight.c:730-734
dam = MAX(MIN(dam, 100), 0)                    // src/fight.c:737       <<< TETO = 100
GET_HIT(vítima) -= dam                         // src/fight.c:738
gain_exp(atacante, nível_da_vítima * dam)      // src/fight.c:741-742
```

E nas magias, **antes** de chegar em `damage()`:

```
se mag_savingthrow(vítima, tipo, 0): dam /= 2  // src/magic.c:262-263   <<< o save divide
```

> **Tetos e cortes, em ordem:** save da magia (÷2) → `sanctuary` (÷2) → **teto absoluto 100 por golpe**
> (`src/fight.c:737`) → nunca negativo.
> Consequência: mesmo uma magia de 99 de dano médio (fireball) **não passa de 100**, e um crítico de
> arma também não.

### 3.3 Dano da maga desarmada

`str_app[11].todam = 0` (`src/constants.c:531`) + `damroll` + `rand_number(0,2)` (`src/fight.c:930`).
Sem arma e sem `damroll`, a maga faz **1 a 2 de dano por golpe** — irrelevante em combate real.

---

## 4. Curva de HP e mana da classe MAGO (níveis 1..30)

### 4.1 A regra

```
do_start():  MAX_HIT = 10 ; MAX_MANA = 100 ; MAX_MOVE = 82      // src/class.c:1473-1475
             advance_level() é chamado AINDA no nível 1          // src/class.c:1498

advance_level() (chamado DEPOIS de GET_LEVEL += 1, src/limits.c:270-272):
   mago:  add_hp   = con_app[CON].hitp + rand_number(3, 8)       // src/class.c:1523,1528
          add_mana = rand_number(nível, (int)(1.5*nível))        // src/class.c:1529
          add_mana = MIN(add_mana, 10)                           // src/class.c:1530
   max_hit  += MAX(1, add_hp)                                    // src/class.c:1554
   se nível > 1:  max_mana += add_mana                           // src/class.c:1557-1558
```

`con_app[CON].hitp` (`src/constants.c:620-647`): CON ≤6 → −1/−2; CON 7–14 → **0**; CON 15 → +1;
CON 16–17 → +2; CON 18–19 → +3; CON 20 → +4; CON 21–23 → +5; CON 24–25 → +6.

`rand_number(a,b)` é uniforme em `[a,b]` (`src/utils.c:35-56`); `dice(n,s)` = n somas de
`rand_number(1,s)` (`src/utils.c:61-72`).

### 4.2 Tabela de HP da maga (CON 10 → `hitp = 0`) — min / média / máx

HP = `10 + Σ_{k=1..N} rand(3,8)` → mín `10+3N`, máx `10+8N`, média `10+5,5N`.

| Nv | min | média | máx | | Nv | min | média | máx |
|---:|---:|---:|---:|---|---:|---:|---:|---:|
| 1 | 13 | 15,5 | 18 | | 16 | 58 | 98,0 | 138 |
| 2 | 16 | 21,0 | 26 | | 17 | 61 | 103,5 | 146 |
| 3 | 19 | 26,5 | 34 | | 18 | 64 | 109,0 | 154 |
| 4 | 22 | 32,0 | 42 | | 19 | 67 | 114,5 | 162 |
| 5 | 25 | 37,5 | 50 | | 20 | 70 | 120,0 | 170 |
| 6 | 28 | 43,0 | 58 | | 21 | 73 | 125,5 | 178 |
| 7 | 31 | 48,5 | 66 | | 22 | 76 | 131,0 | 186 |
| 8 | 34 | 54,0 | 74 | | 23 | 79 | 136,5 | 194 |
| 9 | 37 | 59,5 | 82 | | 24 | 82 | 142,0 | 202 |
| 10 | 40 | 65,0 | 90 | | 25 | 85 | 147,5 | 210 |
| 11 | 43 | 70,5 | 98 | | 26 | 88 | 153,0 | 218 |
| 12 | 46 | 76,0 | 106 | | 27 | 91 | 158,5 | 226 |
| 13 | 49 | 81,5 | 114 | | 28 | 94 | 164,0 | 234 |
| 14 | 52 | 87,0 | 122 | | 29 | 97 | 169,5 | 242 |
| 15 | 55 | 92,5 | 130 | | 30 | 100 | 175,0 | 250 |

### 4.3 Tabela de mana da maga — 100 no nível 1, +10/nível a partir do 10

Ganho por nível (nível em que o ganho ocorre → intervalo, `src/class.c:1529-1530`):

| Nv do ganho | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10+ |
|---|---|---|---|---|---|---|---|---|---|
| `rand_number(n, 1.5n)` | 2–3 | 3–4 | 4–6 | 5–7 | 6–9 | 7–10 | 8–12→10 | 9–13→10 | n–1,5n→**10** |
| ganho efetivo | 2–3 | 3–4 | 4–6 | 5–7 | 6–9 | 7–10 | 8–10 | 9–10 | **10** |

| Nv | min | máx | | Nv | min | máx | | Nv | min | máx |
|---:|---:|---:|---|---:|---:|---:|---|---:|---:|---:|
| 1 | 100 | 100 | | 11 | 164 | 179 | | 21 | 264 | 279 |
| 2 | 102 | 103 | | 12 | 174 | 189 | | 22 | 274 | 289 |
| 3 | 105 | 107 | | 13 | 184 | 199 | | 23 | 284 | 299 |
| 4 | 109 | 113 | | 14 | 194 | 209 | | 24 | 294 | 309 |
| 5 | 114 | 120 | | 15 | 204 | 219 | | 25 | 304 | 319 |
| 6 | 120 | 129 | | 16 | 214 | 229 | | 26 | 314 | 329 |
| 7 | 127 | 139 | | 17 | 224 | 239 | | 27 | 324 | 339 |
| 8 | 135 | 149 | | 18 | 234 | 249 | | 28 | 334 | 349 |
| 9 | 144 | 159 | | 19 | 244 | 259 | | 29 | 344 | 359 |
| 10 | 154 | 169 | | 20 | 254 | 269 | | 30 | 354 | 369 |

### 4.4 Contraprova no DeBo (registros reais de Grebolius)

| Medida no DeBo | Valor observado | Faixa do engine (§4.2/§4.3) | Veredito |
|---|---|---|---|
| Mana máx. nível 11 | **170** (`evidence/dia95.json:335`) | 164–179 | ✅ dentro |
| Mana máx. nível 20 | **260** (`ficha.md:24`, `evidence/dia156b.json:22`) | 254–269 | ✅ dentro |
| HP máx. nível 11 (CON 9) | **87** (`evidence/dia94.json:5024`) | 43–98 | ✅ dentro (alto) |
| HP máx. nível 16 (CON 10) | **87** (`evidence/dia112.json:18`) | 58–138 | ✅ dentro |
| HP máx. nível 17 | **92** (`evidence/dia117.json:7`) | 61–146 | ✅ dentro |
| HP máx. nível 19 | **108** (`evidence/dia132.json:9`) | 67–162 | ✅ dentro |
| HP máx. nível 20 (CON 10) | **113** (`ficha.md:23`) | 70–170 | ✅ dentro |
| Salto de HP no nível 4→5 | +6 | rand(3,8) + con hitp(0) | ✅ |
| Salto de mana no nível 3→4 | +5 (`evolucao.md:384`) | 4–6 no nível 4 | ✅ |
| Salto de mana no nível 7→8 | +10 (`evolucao.md:919`) | 8–10 no nível 8 | ✅ |

> Isto é a evidência **mais forte** deste documento a favor de que o DeBo mantém **as mesmas fórmulas
> de HP e mana** do 3.1. Nada disso prova o resto.

---

## 5. Magias ofensivas de mago: dano e mana

### 5.1 Dano (fixo, sem escala de nível) — `src/magic.c:177-213`

| Magia | Dado (mago) | Faixa | Média | Outros (clérigo/etc.) |
|---|---|---|---|---|
| `magic missile` | `dice(1,8)+1` | 2–9 | 5,5 | `dice(1,6)+1` = 2–7 |
| `burning hands` | `dice(3,8)+3` | 6–27 | 16,5 | `dice(3,6)+3` = 6–21 |
| `shocking grasp` | `dice(5,8)+5` | 10–45 | 27,5 | `dice(5,6)+5` = 10–35 |
| `lightning bolt` | `dice(7,8)+7` | 14–63 | 38,5 | `dice(7,6)+7` = 14–49 |
| `color spray` | `dice(9,8)+9` | 18–81 | 49,5 | `dice(9,6)+9` = 18–63 |
| `fireball` | `dice(11,8)+11` | 22–99 | 60,5 | `dice(11,6)+11` = 22–77 |
| `chill touch` | igual a `magic missile` | 2–9 | 5,5 | + efeito de STR |

`chill touch` compartilha o `case` de `magic missile` (`src/magic.c:177-183`).
`energy drain` (`src/magic.c:246-251`) faz **100 fixo** se o alvo tiver nível ≤ 2; senão `1d10`.

### 5.2 Nível mínimo e custo de mana

Nível mínimo do mago: `src/class.c:1631-1650`.
Parâmetros `spello(nome, mana_max, mana_min, mana_change, ...)`: `src/spell_parser.c:779, 799, 871, 895, 903, 933`.
Fórmula: **`custo(nível) = MAX(mana_max − mana_change × (nível − nível_min), mana_min)`** (`src/spell_parser.c:88-92`).

| Magia | nv mín | mana_max | mana_min | chg | custo: nível mín → estável |
|---|---|---|---|---|---|
| `magic missile` | 1 | 25 | 10 | 3 | 25 (nv1) … **10 no nv6+** |
| `burning hands` | 5 | 30 | 10 | 3 | 30 (nv5) … **10 no nv12+** |
| `shocking grasp` | 7 | 30 | 15 | 3 | 30 (nv7) … **15 no nv12+** |
| `lightning bolt` | 9 | 30 | 15 | 1 | 30 (nv9) … **15 no nv24+** |
| `color spray` | 11 | 30 | 15 | 3 | 30 (nv11) … **15 no nv16+** |
| `fireball` | 15 | 40 | 30 | 2 | 40 (nv15) … **30 no nv20+** |

### 5.3 Dano total de **uma barra de mana cheia**

Contas: `nº de conjurações = floor(mana / custo)`; `dano médio = nº × média do dado`.
Sem contar saves (que reduzem ~11–30% no total — §5.4), sem contar falha de concentração.

**Nível 11 (mana 164–179, uso 170 — valor real do DeBo):**

| Magia | custo | conjuras | dano médio total | mín | máx |
|---|---|---|---|---|---|
| `magic missile` | 10 | 17 | 93,5 | 34 | 153 |
| `burning hands` | 12 | 14 | 231,0 | 84 | 378 |
| `shocking grasp` | 18 | 9 | **247,5** | 90 | 405 |
| `lightning bolt` | 28 | 6 | 231,0 | 84 | 378 |
| `color spray` | 30 | 5 | **247,5** | 90 | 405 |
| `fireball` | — | — | indisponível (< nv 15) | — | — |

**Nível 15 (mana 204–219, uso 210):**

| Magia | custo | conjuras | dano médio total |
|---|---|---|---|
| `magic missile` | 10 | 21 | 115,5 |
| `burning hands` | 10 | 21 | 346,5 |
| `shocking grasp` | 15 | 14 | 385,0 |
| `lightning bolt` | 24 | 8 | 308,0 |
| `color spray` | 18 | 11 | **544,5** |
| `fireball` | 40 | 5 | 302,5 |

**Nível 20 (mana 254–269, uso 260):**

| Magia | custo | conjuras | dano médio total |
|---|---|---|---|
| `magic missile` | 10 | 26 | 143,0 |
| `burning hands` | 10 | 26 | 429,0 |
| `shocking grasp` | 15 | 17 | 467,5 |
| `lightning bolt` | 19 | 13 | 500,5 |
| `color spray` | 15 | 17 | **841,5** |
| `fireball` | 30 | 8 | 484,0 |

**Nível 25 (mana 304–319, uso 310) e nível 30 (mana 354–369, uso 360):**

| Magia | custo | nv25 conjuras → dano | nv30 conjuras → dano |
|---|---|---|---|
| `burning hands` | 10 | 31 → 511,5 | 36 → 594,0 |
| `shocking grasp` | 15 | 20 → 550,0 | 24 → 660,0 |
| `lightning bolt` | 15 | 20 → 770,0 | 24 → 924,0 |
| `color spray` | 15 | 20 → **990,0** | 24 → **1.188,0** |
| `fireball` | 30 | 10 → 605,0 | 12 → 726,0 |

> **Eficiência (dano por ponto de mana), valores estáveis:**
> `lightning bolt` 38,5/15 = **2,57** · `color spray` 49,5/15 = **3,30** · `burning hands` 1,65 ·
> `shocking grasp` 1,83 · `fireball` 2,02 · `magic missile` 0,55.
> Ou seja: **`color spray` é a melhor magia de dano por mana do jogo** a partir do nível 16, e o
> `fireball` — a magia de nível 15 — fica **atrás** dela e do `lightning bolt` em eficiência.

### 5.4 Save do mob (divide o dano por 2)

`mag_savingthrow` (`src/magic.c:53-72`): NPCs usam a tabela **de guerreiro**
(`src/class.c:1149-1201`), e **save acontece se `MAX(1,save) < rand_number(0,99)`**, isto é:

> **P(save) = (99 − save)/100**

| Mob | Nv | `save` | P(save) | Fator de dano esperado `(1 − P/2)` |
|---|---|---|---|---|
| Rato do esgoto | 5 | 77 (`class.c:1156`) | 22% | 0,89 |
| Besouro | 8 | 68 (`class.c:1159`) | 31% | 0,845 |
| Monstro de lama | 12 | 58 (`class.c:1163`) | 41% | 0,795 |
| Rato gigante | 12 | 58 | 41% | 0,795 |
| Basilisco | 13 | 55 (`class.c:1164`) | 44% | 0,78 |
| Mindflayer mestre | 14 | 53 (`class.c:1165`) | 46% | 0,77 |
| Bruxa do mar | 14 | 53 | 46% | 0,77 |
| Dragão vermelho | 19 | 40 (`class.c:1170`) | 59% | 0,705 |

**Logo o dano real por barra de mana contra o dragão é ≈ 0,705 × o da tabela da §5.3.**

### 5.5 O que **não** foi encontrado

- **A % de `GET_SKILL` de cada magia** não vem do código: é ganha por prática/treino. O `do_cast`
  só testa `rand_number(0,101) > GET_SKILL` (`src/spell_parser.c:626`); falhar custa **metade da mana**
  e uma rodada de lag (`:627-631`). **Não achei no código um valor base por magia** — não estimado.
  (No DeBo, `evolucao.md:261` registra `Projétil Mágico (95%)`.)

---

## 6. Quantos golpes um mob do esgoto precisa para matar a maga

### 6.1 Modelo

```
dano_por_rodada = média(dano_do_mob) × P(acerto_do_mob)
rodadas_para_matar = HP_da_maga / dano_por_rodada
segundos = rodadas × 2        (PULSE_VIOLENCE = 2 s — src/structs.h:480)
```

Só a **maga** e **um** mob. Com K mobs na sala, **multiplique o dano por K**: cada mob age uma vez por
rodada (`src/fight.c:962-996`), e a maga também age só uma vez — a assimetria é o que mata.

### 6.2 Rodadas para o mob **matar a maga** (maga com CA 50 → `victim_ac` 5)

HP da maga = média da §4.2 (CON 10).

| Mob | dano médio | P(acerto) | dano/rodada | L5 (37,5 HP) | L11 (70,5 HP) | L20 (120 HP) |
|---|---|---|---|---|---|---|
| Morcego | 3,0 | 20% | 0,60 | 63 rd / **125 s** | 118 rd / 235 s | 200 rd / 400 s |
| Aranha | 2,5 | 20% | 0,50 | 75 rd / 150 s | 141 rd / 282 s | 240 rd / 480 s |
| Rato do esgoto | 5,0 | 40% | 2,00 | 19 rd / **38 s** | 35 rd / 71 s | 60 rd / 120 s |
| Larva gigante | 4,0 | 35% | 1,40 | 27 rd / 54 s | 50 rd / 101 s | 86 rd / 171 s |
| Cobra (padrão 3.1) | 5,0 | 40% | 2,00 | 19 rd / 38 s | 35 rd / 71 s | 60 rd / 120 s |
| Besouro | 7,0 | 55% | 3,85 | 10 rd / 19 s | 18 rd / **37 s** | 31 rd / 62 s |
| Ettin Herald | 4,5 | 50% | 2,25 | 17 rd / 33 s | 31 rd / 63 s | 53 rd / 107 s |
| Ettin Jones | 9,0 | 65% | 5,85 | 6 rd / 13 s | 12 rd / **24 s** | 21 rd / 41 s |
| Monstro de lama | 9,0 | 75% | 6,75 | 6 rd / 11 s | 10 rd / **21 s** | 18 rd / 36 s |
| Chr-eff'n / Naga | 9,0 | 75% | 6,75 | 6 rd / 11 s | 10 rd / 21 s | 18 rd / 36 s |
| Rato gigante | 9,0 | 75% | 6,75 | 6 rd / 11 s | 10 rd / 21 s | 18 rd / 36 s |
| Basilisco | 10,0 | 65% | 6,50 | 6 rd / 12 s | 11 rd / 22 s | 18 rd / 37 s |
| Mindflayer mestre | 11,5 | 85% | 9,78 | 4 rd / **8 s** | 7 rd / **14 s** | 12 rd / 25 s |
| Bruxa do mar | 10,0 | 85% | 8,50 | 4 rd / 9 s | 8 rd / 17 s | 14 rd / 28 s |
| **Dragão vermelho** | 13,5 | 95% | 12,83 | 3 rd / **6 s** | 5 rd / 11 s | 9 rd / **19 s** |

### 6.3 A conta inversa — quantas rodadas a maga precisa

Todas as linhas usam **`color spray` no nível 11** (dano médio 49,5, custo 30, mana 170 do DeBo)
contra **uma maga de CA 50 de nível 11 (70,5 HP)**, com o save do alvo já descontado:

`dano_por_conjuração = 49,5 × (1 − P(save)/2)` · `rodadas = HP_do_mob / dano_por_conjuração`

| Alvo | HP (arquivo) | HP médio | P(save) | dano/conj. | **Rodadas p/ matar** | Rodadas p/ morrer (§6.2) | Veredito |
|---|---|---|---|---|---|---|---|
| Rato do esgoto | 1d12+48 `70.mob:38` | 54,5 | 22% | 44,1 | **2** | 35 | sobra |
| Besouro | 2d10+98 `70.mob:63` | 109 | 31% | 41,8 | **3** | 18 | sobra |
| Monstro de lama | 4d6+140 `70.mob:12` | 154 | 41% | 39,4 | **4** | 10 | ok |
| Rato gigante | 1d10+150 `72.mob:61` | 155,5 | 41% | 39,4 | **4** | 10 | ok |
| Basilisco | 1d12+160 `70.mob:191` | 166,5 | 44% | 38,6 | **5** | 11 | ok |
| Chr-eff'n | 2d26+148 `70.mob:138` | 175 | 41% | 39,4 | **5** | 10 | **apertado** |
| Mindflayer mestre | 1d10+170 `72.mob:11` | 175,5 | 46% | 38,1 | **5** | 7 | **apertado** |
| Bruxa do mar | 1d8+172 `70.mob:164` | 176,5 | 46% | 38,1 | **5** | 8 | **apertado** |
| **Dragão vermelho** (L11) | 5d4+230 `70.mob:151` | 242,5 | 59% | 34,9 | **7** | **5** | **suicida** |
| **Dragão vermelho** (L15, `color spray` custo 18, 210 de mana) | idem | 242,5 | 59% | 34,9 | **7** | 7,2 (92,5 HP ÷ 12,83) | **no fio da navalha** |

> **A leitura correta desta tabela:** as "5 conjurações" cabem **exatamente** numa barra de mana de
> nível 11 (`floor(170/30) = 5`) — quem precisa de 6 ou 7 rodadas já não cabe. E o número que decide
> não é o dano, é **rodadas × K mobs na sala**: com K = 2, todas as linhas "apertado" viram derrota.

---

## 7. XP e progressão

### 7.1 XP ganha por abate

**Solo** (`solo_gain`, `src/fight.c:444-465`):

```
exp  = MIN(max_exp_gain, GET_EXP(mob) / 3)                            // :448
exp += MAX(0, exp * MIN(8, GET_LEVEL(mob) - GET_LEVEL(maga)) / 8)     // :454
exp  = MAX(exp, 1)                                                    // :456
```

**Em grupo** (`group_gain`, `src/fight.c:405-441`):

```
tot_gain = GET_EXP(mob)/3 + tot_membros - 1                           // :424
base     = MAX(1, tot_gain / tot_membros)                             // :431
```

**Por dano desferido** (`src/fight.c:741-742`): cada golpe rende `GET_LEVEL(mob) × dano`.
Somando todos os golpes até a morte, isso equivale a **`nível_do_mob × HP_total_do_mob`** de XP extra.

**Caps:** `max_exp_gain = 100000` por chamada (`src/config.c:72`, aplicado em `src/limits.c:266`);
`max_exp_loss = 500000` (`src/config.c:73`, `src/limits.c:288`).

### 7.2 XP total por abate nos esgotos (mundo padrão)

`total ≈ (exp/3 com bônus) + nível × HP_médio`

| Mob (arquivo:linha) | Nv | `EXP` | Solo (`exp/3`) | XP por dano | **Total aprox.** |
|---|---|---|---|---|---|
| Aranha `70.mob:51` | 1 | 100 | 33 | 1 × 14,5 = 15 | **48** |
| Morcego `70.mob:26` | 1 | 150 | 50 | 1 × 13,5 = 14 | **64** |
| Larva gigante `70.mob:76` | 3 | 350 | 117 | 3 × 41 = 123 | **240** |
| Rato do esgoto `70.mob:39` | 5 | 1000 | 333 | 5 × 54,5 = 273 | **606** |
| Cobra `70.mob:90` | 4 | 1000 | 333 | 4 × 46 = 184 | **517** |
| Lemure `70.mob:206` | 5 | 1000 | 333 | 5 × 66 = 330 | **663** |
| Wererat `72.mob:50` | 6 | 1500 | 500 | 6 × 83 = 498 | **998** |
| Mindflayer júnior `72.mob:38` | 6 | 1500 | 500 | 6 × 80,5 = 483 | **983** |
| Ettin Herald `70.mob:232` | 6 | 1500 | 500 | 6 × 79 = 474 | **974** |
| Besouro `70.mob:64` | 8 | 3750 | 1250 | 8 × 109 = 872 | **2122** |
| Mindflayer sênior `72.mob:25` | 8 | 4500 | 1500 | 8 × 105,5 = 844 | **2344** |
| Ettin Jones `70.mob:219` | 10 | 11000 | 3666 | 10 × 133 = 1330 | **4996** |
| Monstro de lama `70.mob:13` | 12 | 13000 | 4333 | 12 × 154 = 1848 | **6181** |
| Rato gigante `72.mob:62` | 12 | 13000 | 4333 | 12 × 155,5 = 1866 | **6199** |
| Chr-eff'n `70.mob:139` | 12 | 13000 | 4333 | 12 × 175 = 2100 | **6433** |
| Naga `70.mob:179` | 12 | 13500 | 4500 | 12 × 157,5 = 1890 | **6390** |
| Basilisco `70.mob:192` | 13 | 16000 | 5333 | 13 × 166,5 = 2165 | **7498** |
| Bruxa do mar `70.mob:165` | 14 | 18000 | 6000 | 14 × 176,5 = 2471 | **8471** |
| Mindflayer mestre `72.mob:12` | 14 | 20000 | 6666 | 14 × 175,5 = 2457 | **9123** |
| **Dragão vermelho** `70.mob:152` | 19 | 40000 | 13333 | 19 × 242,5 = 4608 | **17941** |

### 7.3 XP necessária por nível — tabela `level_exp` (MAGO, `src/class.c:1728-1763`)

| Nv | XP acumulada | Δ desde o nível anterior | Nv | XP acumulada | Δ |
|---:|---:|---:|---:|---:|---:|
| 1 | 1 | — | 16 | 2.250.000 | 375.000 |
| 2 | 2.500 | 2.499 | 17 | 2.625.000 | 375.000 |
| 3 | 5.000 | 2.500 | 18 | 3.000.000 | 375.000 |
| 4 | 10.000 | 5.000 | 19 | 3.375.000 | 375.000 |
| 5 | 20.000 | 10.000 | 20 | 3.750.000 | 375.000 |
| 6 | 40.000 | 20.000 | 21 | 4.000.000 | 250.000 |
| 7 | 60.000 | 20.000 | 22 | 4.300.000 | 300.000 |
| 8 | 90.000 | 30.000 | 23 | 4.600.000 | 300.000 |
| 9 | 135.000 | 45.000 | 24 | 4.900.000 | 300.000 |
| 10 | 250.000 | 115.000 | 25 | 5.200.000 | 300.000 |
| 11 | 375.000 | 125.000 | 26 | 5.500.000 | 300.000 |
| 12 | 750.000 | 375.000 | 27 | 5.950.000 | 450.000 |
| 13 | 1.125.000 | 375.000 | 28 | 6.400.000 | 450.000 |
| 14 | 1.500.000 | 375.000 | 29 | 6.850.000 | 450.000 |
| 15 | 1.875.000 | 375.000 | 30 | 7.400.000 | 550.000 |
| | | | 31 (immortal) | 8.000.000 | 600.000 |

A função só devolve valor para os níveis enumerados; fora da tabela, `log("SYSERR: Requesting exp for
invalid level")` e retorno 0 (`src/class.c:1711-1714`). **A tabela de mago é a mais cara das quatro.**

### 7.4 "Quantos mobs do esgoto para subir de N para N+1"

Usando o **rato do esgoto** (606 XP, §7.2) e a **larva/morcebo/aranha** para os primeiros níveis:

| Transição | Δ XP (mago, §7.3) | Ratos do esgoto (606 XP) | Monstros de lama (6181 XP) |
|---|---:|---:|---:|
| 1 → 2 | 2.499 | **5** (ou 4 com bônus de nível) | — |
| 2 → 3 | 2.500 | **5** | — |
| 3 → 4 | 5.000 | **9** | — |
| 4 → 5 | 10.000 | **17** | — |
| 5 → 6 | 20.000 | **33** | **4** |
| 6 → 7 | 20.000 | **33** | **4** |
| 7 → 8 | 30.000 | **50** | **5** |
| 8 → 9 | 45.000 | **75** | **8** |
| 9 → 10 | 115.000 | **190** | **19** |
| 10 → 11 | 125.000 | **207** | **21** |
| 11 → 12 | 375.000 | **619** | **61** |
| 12 → 13 | 375.000 | 619 (o rato ainda dá o mesmo) | 61 |
| 15 → 16 | 375.000 | 619 | 61 |
| 20 → 21 | 250.000 | 413 | 41 |

> Com o **dragão vermelho** (17.941 XP), a transição 11 → 12 cai de 619 ratos para **21 dragões**.
> Nota importante: **o rato do esgoto vale sempre os mesmos 606 XP**, independentemente do nível da
> maga — o bônus de diferença de nível só existe quando o mob é **mais alto** que a maga
> (`src/fight.c:452-454`), e uma vez que a maga passa do nível 5 o rato não dá mais bônus nenhum.
> O que muda de verdade é a **tabela**: o custo por nível salta de 30.000 (8→9) para 45.000 (9→10),
> 115.000 (10→11) e 375.000 (11→12) — e é aí que o esgoto deixa de ser fonte de XP.

---

## 8. Fuga (`flee`) e `wimpy`

### 8.1 `wimpy` — `src/act.other.c:690-728`

- `wimpy N` aceita `N` entre 1 e `MAX_HIT/2`; acima disso recusa
  (`"You can't set your wimp level above half your hit points."`, `src/act.other.c:716-717`).
- `wimpy 0` desliga.
- Gatilho, dentro de `damage()`:

```
se !NPC e GET_WIMP_LEV > 0 e vítima != atacante
   e GET_HIT < GET_WIMP_LEV e GET_HIT > 0:
       "You wimp out, and attempt to flee!"      // src/fight.c:797-801
       do_flee(...)
```

### 8.2 `flee` — `src/act.offensive.c:268-298`

- Se a posição for pior que `POS_FIGHTING` (7), **não consegue fugir**: "You are in pretty bad shape,
  unable to flee!" (`:273-276`). Isto é o **furo do wimpy**: quando o HP já caiu abaixo de
  `POS_FIGHTING`, a fuga está bloqueada — e é exatamente a situação em que o wimpy dispara.
- Sorteia até 6 direções aleatórias (`:278-296`); se nenhuma servir → `"PANIC! You couldn't escape!"`
  (`:297`) — **e a rodada é perdida**.
- Fugir com sucesso **custa XP**:

```
loss  = GET_MAX_HIT(oponente) - GET_HIT(oponente)     // src/act.offensive.c:287
loss *= GET_LEVEL(oponente)                           // :288
gain_exp(ch, -loss)                                   // :289
```

### 8.3 O comportamento perto do limiar

| Fator | Efeito |
|---|---|
| `wimpy` limitado a `maxHP/2` | nunca dá para "wimpar" antes de estar na metade — não protege contra golpe que tira > 50% |
| Ordem dentro da rodada | o wimpy dispara **depois** que o dano já foi aplicado (`src/fight.c:738` antes de `:797`) |
| 1 tentativa por rodada, 6 direções | em sala com poucas saídas (becos dos esgotos) a chance de "PANIC" é alta |
| Custo de XP da fuga | cresce com o **dano já sofrido** pelo oponente — fugir de um mob quase morto custa caro |
| `flee` bloqueado se `POS < POS_FIGHTING` | abaixo de atordoado (3) não há fuga |

**Tradução para o DeBo:** Grebolius usa `wimpy 48` com 113 de HP (`ficha.md:44`) — 42% do máximo, dentro
do limite de `maxHP/2 = 56`. A cobra registrada em `evidence/dia95.json:317` tirou **12, 17, 19 e 25**
de uma vez com a maga em 87 HP: com `wimpy` em 48, **um único golpe de 25 não dispara a fuga**, e a
fuga só tenta sair na rodada seguinte — depois de 5 cobras terem agido.

---

## 9. Veredito de nível

> **Isto é o MUNDO PADRÃO do CircleMUD 3.1** (`lib/world/mob/*.mob`, `lib/world/zon/70-73.zon`).
> **O DeBo pode ter mudado qualquer número** — e a §10 mostra que mudou vários. Leia o veredito como
> *linha de base a comparar*, nunca como promessa.

### Faixas de mob, por profundidade do esgoto

| Faixa | Zona | Mobs | Nv | HP médio | Dano médio/golpe |
|---|---|---|---|---|---|
| **A — nível 1–5** | 70 (1º nível) | morcego (7001), aranha (7003), rato (7002) | 1–5 | 14–55 | 2,5–5 |
| **B — nível 6–10** | 71 (2º esgoto) | larva (7005), cobra (7006), besouro (7004), rato, lama | 3–12 | 41–154 | 4–9 |
| **C — nível 11–15** | 72 (labirinto) | wererat (7203), mindflayers 7200/01/02, rato gigante (7204), lama | 6–14 | 80–180 | 4,5–11,5 |
| **D — nível 16+** | 73 (túneis) | Jones/Herald ettin, lemure, chr-eff'n, naga, basilisco, bruxa, **dragão** | 5–19 | 66–250 | 4,5–13,5 |

> **Faixa "21+" não existe nos esgotos padrão.** O mob mais alto de `70.mob`/`72.mob` é o **dragão
> vermelho, nível 19** (`lib/world/mob/70.mob:151`). Os tetos de `thac0` 2 e HP 250 são o máximo que o
> esgoto oferece — qualquer maga de nível 21+ só enfrenta risco ali por **quantidade**, armadilha ou
> queda.

### Veredito por faixa

**Faixa A (mobs de nível 1–10) — zona 70 e parte da 71**

- **Trivial: nível 7+.** `burning hands` no nível 7 custa 24 e a maga tem ~133 de mana
  → `floor(133/24) = 5` conjurações; com save do rato (22%) cada uma vale 14,7 → **73,5 de dano**,
  acima do **máximo** de HP de um rato (60, `70.mob:38`) e com folga para morcego (16) e aranha (20).
  Nenhum mob da faixa tira mais de 5 por golpe, e nenhum acerta mais de 55%.
- **Morcego e aranha são trivial desde o nível 1:** mana 100, `magic missile` custa 25 → 4 conjurações
  × 5,5 = 22 de dano, e o morcego tem no máximo 16 de HP, a aranha 20.
- **Apertado: nível 5–6 (contra o rato).** Conta explícita no **nível 5**: mana 114–120,
  `magic missile` custa 13 → `floor(117/13) = 9` conjurações; descontado o save (22%), o dano é
  `9 × 4,9 = 44` — **abaixo do mínimo de 49** de HP do rato. Com `burning hands` (custo 30) são 3
  conjurações → 44 também. Sem o save seriam 49,5: **empate técnico**. Enquanto isso o rato tira
  2,0/rodada de 37,5 de HP médio (19 rodadas). É jogável, é apertado, e depende do dado.
- **Suicida: níveis 1–2.** Mana 100, `magic missile` custa 25 → **4 conjurações × 5,5 = 22 de dano**.
  O rato tem no mínimo 49. A maga **não consegue** matar um rato com uma barra inteira, e no corpo a
  corpo faz 1–2 por golpe com 60–65% de acerto. Enquanto isso o rato tira 2,0/rodada de uma maga com
  15,5 de HP médio → **~8 rodadas (16 s) para morrer**.

**Faixa B (mobs de nível 11–15) — zona 71 e o miolo da 72**

- **Trivial: nível 13+.** `color spray` no nível 13 custa 24; com ~190 de mana são
  `floor(190/24) = 7` conjurações × `49,5 × 0,795 = 39,4` (save do monstro de lama, 41%) =
  **~275 de dano efetivo por barra**, contra 154 de HP. Ela o mata em **4 rodadas**, e o monstro de
  lama só tira 6,75/rodada de 81,5 de HP → **12 rodadas**. Margem de 3×.
- **Apertado: nível 11–12.** No nível 11 (170 de mana real do DeBo): `color spray` custa 30
  → 5 conjurações × 39,4 = **197** de dano efetivo, contra os **154** de HP do monstro de lama — mata,
  mas gasta 4 das 10 rodadas antes de morrer (6,75/rodada × 70,5 HP). Com **dois** mobs na sala, o dano
  recebido dobra para 13,5/rodada e a maga morre em 5 rodadas, contra 8 necessárias: **derrota**. Era
  exatamente o cenário registrado no DeBo (nível 11, 6 cobras — `evidence/dia95.json:317`).
- **Suicida: abaixo do nível 9.** Sem `lightning bolt`, o teto de dano efetivo por barra no nível 8 é
  `floor(142/18) = 7` conjurações de `burning hands` × `16,5 × 0,845 = 13,9` ≈ **98**. O besouro
  (100–118 HP) e o monstro de lama (144–164) **não caem** com uma barra inteira de um mago de nível ≤ 8.

**Faixa C (mobs de nível 16–20) — zona 72 (covil dos mindflayers) e 73**

- **Trivial (zona 72 / mindflayers): nível 17+.** Com `color spray` a 15 de mana (nível 16+) e ~231 de
  mana no nível 17, são `floor(231/15) = 15` conjurações; com o save do mestre (46%) cada uma vale
  `49,5 × 0,77 = 38,1` → **~572 de dano efetivo por barra** contra os 175,5 de HP do mindflayer mestre.
  A maga o mata em **5 rodadas** e ele a mata em `103,5 ÷ 9,78 = 10,6` rodadas. **Margem de 2×.**
  O risco deixa de ser a barra de mana e passa a ser **quantos mobs estão na sala ao mesmo tempo** —
  cada mob age 1×/rodada (`src/fight.c:962-996`), e o covil `7200`–`7208` põe mindflayers **com
  escolta** (`lib/world/zon/72.zon:6-31`).
- **Apertado: nível 15–16 (contra o covil, não contra um mob isolado).** No nível 15 a maga tem ~210 de
  mana e 92,5 de HP; `color spray` (custo 18) dá `floor(210/18) = 11` conjurações, mas o mestre cai em
  **5 rodadas**. Se **dois** mindflayers estiverem na sala, o dano recebido dobra para 19,6/rodada e ela
  morre em **4,7 rodadas** — antes de matar o segundo. **Contra dois, é derrota.**
- **Suicida: abaixo do nível 13.** Sem `color spray`, o melhor é `lightning bolt` (nível 9+).
  No nível 12: custo 21, mana ~180 → `floor(180/21) = 8` conjurações; com o save do dragão (59%)
  cada uma vale `38,5 × 0,705 = 27,1` → **217 por barra**, contra os **242,5** de HP médio do dragão.
  **Não mata.** Seriam precisas **9 rodadas** (242,5 ÷ 27,1), e o dragão tira 12,83/rodada de uma
  maga com 76 de HP médio → **6 rodadas até morrer**. **Derrota por 3 rodadas de margem.**

**O caso especial do dragão vermelho (zona 73, sala `7328`)**

O dragão tem `thac0 = 2` (`70.mob:151`), o que dá `calc_thaco = 4` — **CA virou irrelevante**: ele
acerta 95% das vezes contra qualquer CA ≤ 20 (§2.6). A conta vira puramente `HP` contra `rodadas`:

| Nv da maga | HP médio | Mana | Rodadas p/ matar (`color spray`) | Rodadas p/ morrer (12,83/rd) | Margem |
|---|---|---|---|---|---|
| 11 | 70,5 | 170 | 7 — mas só **5** conjurações cabem na barra → **não mata** | 5,5 | **negativa** |
| 13 | 81,5 | 190 | 7 — cabem 6 (`6×34,9 = 209 < 242,5`) → **não mata** | 6,4 | **negativa** |
| 15 | 92,5 | 210 | 7 (cabem 11) | 7,2 | +0,2 rodada |
| 16 | 98,0 | 219 | 7 | 7,6 | +0,6 |
| 17 | 103,5 | 231 | 7 | 8,1 | +1,1 |
| 20 | 120,0 | 260 | 7 | 9,4 | +2,4 |
| 25 | 147,5 | 310 | 7 | 11,5 | +4,5 |

> **Leitura:** o dragão é matável por uma maga sozinha **a partir do nível 15**, e só fica confortável
> por volta do **nível 20**. Entre 11 e 14 a barra de mana **não fecha a conta**. Isto assume a maga
> começando com a barra cheia, sozinha, sem veneno, sem pressa e sem fuga interrompida.
> Com o `wimpy` em ~metade do HP, ela **abandona a luta nas rodadas 4–5** — ou seja, entre 15 e 19 o
> resultado prático é *"fugir com vida"*, não *"matar o dragão"*.

**Faixa D / conclusão operacional**

> **Resposta curta:** com o mundo padrão, **nível 11–12 é o primeiro nível em que limpar as zonas 70 e
> 71 é uma atividade e não um teste de sobrevivência**; **nível 15+** é o primeiro nível em que dá para
> *tentar* a zona 73 (e matar o dragão exige barra cheia e margem de uma ou duas rodadas); **nível
> 17–20** é o nível em que as zonas 72 e 73 deixam de ser perigosas *por magia* e passam a ser
> perigosas apenas *por número de mobs por sala*. Armadilhas, quedas e salas de morte — `7190`
> "Mid-Air", `7284` "The Firedeath", a borda do abismo `7106`–`7121` (ver
> [05-mundo-padrao-vs-mapa.md](05-mundo-padrao-vs-mapa.md)) — **não são cobertas pela matemática de
> combate** e continuam letais em qualquer nível.

### Contas explícitas (nível 11, Grebolius real)

```
MANA      = 170                       (evidence/dia95.json:335)  ∈ [164,179] ✅ (§4.3)
HP        = 87                        (evidence/dia94.json:5024) ∈ [43,98]   ✅ (§4.2)
THAC0     = 17 (tabela, class.c:1236)
          - 1 (hitroll, ficha.md:42)
          - 4 ((19-13)/1.5 truncado, fight.c:858)
          - 2 ((17-13)/1.5 truncado, fight.c:859)
          = 10
CA        = 50 (com armor) -> victim_ac = 50/10 = 5    (fight.c:891)

MAGA -> RATO DO ESGOTO (CA do arquivo 5 -> victim_ac 5):
   need  = 10 - 5 = 5        -> P = min(19, 21-5)/20 = 80%
   dano  = 0 (STR 11 tohit) + damroll + dados da arma  [arma nao levantada]
   dano de magia (nao rola acerto): color spray 49,5 medio, save do rato 22% -> 49,5 x 0,89 = 44,1
   barra = floor(170/30) = 5 conjuracoes  -> 5 x 44,1 = 220 de dano
   rato  = 1d12+48 -> 49..60 HP (media 54,5)  => 1,5 conjuracoes por rato

RATO -> MAGA:
   calc_thaco = thac0_do_arquivo(16) + 2 = 18                (db.c:1142 + fight.c:855-859)
   need  = 18 - 5 = 13   -> P = 40%
   dano  = 0 (STR do mob) + 0 (damroll) + dice(2,4) = 2..8, media 5,0
   dano/rodada = 5,0 x 0,40 = 2,0
   rodadas ate matar = 87 / 2,0 = 43,5 rodadas = 87 s       (PULSE_VIOLENCE = 2 s, structs.h:480)
   => 1 rato: irrelevante.  6 ratos: 12/rodada -> 7,25 rodadas = 15 s.  <<< e assim que se morre.
```

---

## 10. Divergências já medidas entre o padrão 3.1 e o DeBo

Estas são medições feitas **no servidor real** e registradas neste repositório. Todas mostram que o
DeBo **não** é o mundo padrão para efeito de combate/progressão.

| # | Item | Padrão 3.1 (arquivo:linha) | DeBo (registro) | Impacto |
|---|---|---|---|---|
| D1 | XP para o **nível 12** (mago) | **750.000** (`src/class.c:1742`) | **200.000** (`evidence/dia94.json:5024` → 195.202 + 4.798; `dia95.json:335` → 195.201 + 4.799) | DeBo ≈ **3,75× mais barato** |
| D2 | XP para o **nível 21** | **4.000.000** (`src/class.c:1751`) | **1.200.000** (`ficha.md:28`) | DeBo ≈ **3,33× mais barato** |
| D3 | XP para o **nível 8** | **90.000** (`src/class.c:1738`) | **40.000** (`evolucao.md:690`) | — |
| D4 | XP para o **nível 6** | **40.000** (`src/class.c:1736`) | **15.000** (`evolucao.md:494`) | — |
| D5 | XP para o **nível 4** | **10.000** (`src/class.c:1734`) | **5.000** (`evolucao.md:253`, 3.084+1.916) | exatamente metade |
| D6 | XP para o **nível 2** | **2.500** (`src/class.c:1732`) | **1.000** (`evolucao.md:178`, 396+604) | — |
| D7 | Dano da **cobra dos esgotos** | `1d9` = **1–9** (`lib/world/mob/70.mob:89`) | **12, 17, 19, 25** por mordida (`evidence/dia95.json:317`) | DeBo ≥ 2,7× o máximo padrão |
| D8 | **`armor`** | `modifier = -20` (`src/magic.c:314`) | **+25** (`evidence/dia91.json:135`) | mais forte no DeBo |
| D9 | Nível do **rato dos esgotos** | 5 (`lib/world/mob/70.mob:38`) | `consider rato` → **"Você é LOUCO!"** para uma maga de nível 20 (`monstros.md:50,80`) | DeBo tem outro bicho/outra força |
| D10 | XP por **abate simples** | fórmula `exp/3` (`src/fight.c:448`) | **1.178–3.664** por abate nas galerias (`evolucao.md:900,912`) | fora da escala do `exp/3` padrão |

> **Consequência para o veredito:** as **fórmulas** (§2–§6, §8) provavelmente valem no DeBo — a mana
> por nível comprova isso em dois pontos (nível 11 = 170 e nível 20 = 260, ambos dentro da faixa
> prevista). O que **não** vale é a **calibragem do mundo**: o DeBo dá muito mais XP por abate e cobra
> muito menos XP por nível, então "quantos mobs para subir" (§7.4) é **drasticamente menor** no DeBo —
> e os bichos dos esgotos do DeBo são **mais letais** que os do arquivo padrão.

---

## Limites desta pesquisa

1. **Nada foi medido no servidor.** Cada linha marcada "Testado (código)" prova o engine do
   repositório, **não** o comportamento do DeBo em `debomud.org:4000`.
2. **3.0 vs 3.1.** O DeBo declara-se 3.0; este código é 3.1. As diferenças conhecidas entre as duas
   versões estão em portabilidade/OLC, e as fórmulas de `fight.c`/`magic.c` conferem com a literatura
   do 3.0 — mas **não foi feita comparação linha a linha com um fonte 3.0**, o que mantém as
   afirmações de fórmula como *Provável* para o DeBo.
3. **Valores que vêm de arquivos de mundo, não de `src/`:** HP, dano, `thac0`, CA e XP de mob saem de
   `lib/world/mob/*.mob`. Tirei-os do **mundo padrão que acompanha este repositório**.
4. **Não encontrado no código (e portanto não estimado):**
   - o dado de dano da **arma inicial** da maga (está no `.obj`, que não foi objeto desta pesquisa);
   - a **CA real de uma maga vestida** (depende do equipamento; DeBo registra 64/80, padrão não;
     `ficha.md:40`);
   - o **`GET_SKILL` base de cada magia** (depende de prática — `src/spell_parser.c:626` só testa);
   - o **teto de dano do DeBo** (se for ≠ 100, toda a §5.3 muda);
   - o valor de `PULSE_VIOLENCE` no DeBo (assumi 2 s, `src/structs.h:480`);
   - **se o DeBo usa a mesma tabela `level_exp`** — §10 mostra que não usa.
5. **Aritmética:** todas as médias usam o valor esperado uniforme (`dice(n,s)` → `n(s+1)/2`). As
   divisões inteiras em C (**truncamento para zero**) foram respeitadas onde importam — em especial
   `compute_armor_class/10` (`src/fight.c:891`) e `(INT-13)/1.5` (`src/fight.c:858`).
6. **Não coberto:** combate a cavalo/montaria, `bash`/`backstab`/`rescue` e outras habilidades,
   regeneração (`hit_gain`/`mana_gain` em `src/limits.c:79-160`), morte por armadilha/sala, e o
   efeito de `AFF_SANCTUARY` no lado do mob.
