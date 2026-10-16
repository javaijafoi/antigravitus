# 05 — O mundo padrão do CircleMUD vs. o mapa do DeBo

Comparação entre o **MUNDO PADRÃO** do CircleMUD (arquivos `.wld`/`.zon` do
`Yuffster/CircleMUD`, branch `master`) e o mapa levantado ao vivo no
**Devil's Bob MUD (DeBo)** — um CircleMUD 3.0 fortemente modificado e traduzido
para português — registrado em `data/heroes/grebolius/mapa.json` e
`data/heroes/grebolius/mapa_vivo.json`.

> **Aviso de idioma.** O mundo padrão é **em inglês**; o DeBo é **em português**.
> Toda equivalência de nome abaixo é uma *tradução mental* minha e vale como
> indício, nunca como prova. Toda afirmação marcada **Testado** prova apenas o
> **mundo padrão** (ou, quando diz "mapa local", prova apenas o `.json` local) —
> **nada nesta pesquisa prova o que existe no DeBo.**

---

## Fonte consultada

URL crua base: `https://raw.githubusercontent.com/Yuffster/CircleMUD/master/`

| Arquivo | URL | Resultado |
|---|---|---|
| `lib/world/wld/index` | [.../lib/world/wld/index](https://raw.githubusercontent.com/Yuffster/CircleMUD/master/lib/world/wld/index) | 200 — completo (29 zonas listadas) |
| `lib/world/zone.lst` | [.../lib/world/zone.lst](https://raw.githubusercontent.com/Yuffster/CircleMUD/master/lib/world/zone.lst) | 200 — completo |
| `lib/world/wld/30.wld` | [.../lib/world/wld/30.wld](https://raw.githubusercontent.com/Yuffster/CircleMUD/master/lib/world/wld/30.wld) | 200 — completo (termina em `$`), vnums 3000–3066 |
| `lib/world/wld/31.wld` | [.../lib/world/wld/31.wld](https://raw.githubusercontent.com/Yuffster/CircleMUD/master/lib/world/wld/31.wld) | 200 — completo (`$`), vnums 3100–3155 e 3200–3205 |
| `lib/world/wld/32.wld` | [.../lib/world/wld/32.wld](https://raw.githubusercontent.com/Yuffster/CircleMUD/master/lib/world/wld/32.wld) | **404 — NÃO EXISTE neste repositório** |
| `lib/world/wld/33.wld` | [.../lib/world/wld/33.wld](https://raw.githubusercontent.com/Yuffster/CircleMUD/master/lib/world/wld/33.wld) | 200 — completo (`$`), vnums 3300–3375 |
| `lib/world/wld/36.wld` | [.../lib/world/wld/36.wld](https://raw.githubusercontent.com/Yuffster/CircleMUD/master/lib/world/wld/36.wld) | 200 — completo (`$`), vnums 3600–3666 |
| `lib/world/wld/70.wld` | [.../lib/world/wld/70.wld](https://raw.githubusercontent.com/Yuffster/CircleMUD/master/lib/world/wld/70.wld) | 200 — completo (`$`), vnums 7000–7070 |
| `lib/world/wld/71.wld` | [.../lib/world/wld/71.wld](https://raw.githubusercontent.com/Yuffster/CircleMUD/master/lib/world/wld/71.wld) | 200 — completo (`$`), vnums 7100–7129 e 7190 |
| `lib/world/wld/72.wld` | [.../lib/world/wld/72.wld](https://raw.githubusercontent.com/Yuffster/CircleMUD/master/lib/world/wld/72.wld) | 200 — completo (`$`), vnums 7200–7299 **e 7300–7345** |
| `lib/world/wld/73.wld` | [.../lib/world/wld/73.wld](https://raw.githubusercontent.com/Yuffster/CircleMUD/master/lib/world/wld/73.wld) | **404 — NÃO EXISTE**; o conteúdo da zona 73 está dentro de `72.wld` |
| `lib/world/wld/186.wld` | [.../lib/world/wld/186.wld](https://raw.githubusercontent.com/Yuffster/CircleMUD/master/lib/world/wld/186.wld) | 200 — completo (`$`), vnums 18600–18612 e 18620–18647 |
| `lib/world/zon/30.zon` … `33.zon` | [.../lib/world/zon/](https://raw.githubusercontent.com/Yuffster/CircleMUD/master/lib/world/zon/30.zon) | 30, 31, 33 = 200 completos; **32.zon = 404** |
| `lib/world/zon/36.zon`, `70.zon`…`73.zon`, `186.zon` | idem | todos 200 e completos (terminam em `$`) |

**Truncamento:** nenhum dos arquivos que retornaram 200 veio truncado — todos
terminam com o marcador `$` de fim de arquivo do CircleMUD. **O que faltou de
fato foram dois arquivos inexistentes no repositório: `wld/32.wld` (404) e
`wld/73.wld` (404), e por consequência `zon/32.zon` (404).** Consequências:
1. **Midgaard River (zona 32)** não pode ser lida como arquivo próprio; as salas
   de rio que sobrevivem (`3200`–`3205`, "On The River") estão **dentro de
   `31.wld`**, cuja zona (`zon/31.zon`) declara o intervalo `3100 3299`.
2. **Sewer nível 3 (zona 73)** também não tem arquivo próprio: `72.wld` contém
   os vnums `7200`–`7299` (zona 72) **e** `7300`–`7345` (zona 73), apesar de
   `wld/index` listar apenas `70.wld 71.wld 72.wld`. O `zon/73.zon` existe
   normalmente.

---

## 1. Tabela de afirmações

Níveis: **Testado** = verificado no arquivo padrão/local com vnum citado (prova
o mundo padrão ou o `.json` local, **não** o DeBo). **Provável** = corresponde ao
DeBo por indício de nome/topologia. **Dúvida** = divergência ou não verificável.

| # | Afirmação (topologia/nome) | Nível | Fonte (arquivo / vnum) | Como validar no DeBo |
|---|---|---|---|---|
| 1 | Midgaard zona 30 tem **65 salas**, vnums 3000–3066; **3056 e 3057 não existem** | Testado | `wld/30.wld` — salas `#3000`…`#3066` | andar de 3000 a 3066 não é possível; procurar as salas por nome |
| 2 | Midgaard zona 31 tem **62 salas**: 3100–3155 (56) + 3200–3205 (6) | Testado | `wld/31.wld` | — |
| 3 | **Nenhuma** sala de Midgaard tem 6 saídas; o grau máximo é **5** | Testado | `wld/30.wld#3001` (n,e,s,w,d), `wld/31.wld#3120` (n,e,s,w,u) | `olhar`/comandos de saída no Templo e no cruzamento de estradas |
| 4 | O Templo de Midgaard (vnum **3001**) tem **5** saídas no padrão: n→3054 altar, e→3063 doações, s→3005 praça, w→3000 leitura, d→3005 praça | Testado | `wld/30.wld#3001` (blocos D0,D1,D2,D3,D5) | a sala local equivalente tem **6** saídas (n,e,s,w,u,d) — ver §8 |
| 5 | `wld/32.wld` e `zon/32.zon` **não existem** neste repo; as salas de rio (3200–3205) estão em `31.wld` | Testado | HTTP 404 em ambos | confirmar se o DeBo tem zona de rio própria ("No Rio"/"As Margens do Rio") |
| 6 | `wld/73.wld` **não existe**; as salas 7300–7345 estão dentro de `72.wld` | Testado | `wld/72.wld` contém `#7300`…`#7345`; `wld/73.wld` = 404 | — |
| 7 | O tabuleiro tem **67 salas**: portão `3600` + **64 casas** (`3601`–`3664`) + 2 tesourarias (`3665`, `3666`) | Testado | `wld/36.wld` | o mapa local só levantou **6 casas** — §8 |
| 8 | Cada casa do tabuleiro tem 2–4 saídas (bordas 2–3, interior 4); as casas das rainhas (`3604`, `3660`) têm um `D5` secreto para a tesouraria | Testado | `wld/36.wld#3604`, `#3660`, `#3665`, `#3666` | descer (`d`) na casa da rainha preta/branca |
| 9 | No tabuleiro nascem **32 peões** (8 pretos, 8 brancos) e **16 oficiais** + 2 reis + 2 rainhas = 32 peças | Testado | `zon/36.zon` (mobs 3600–3611) | matar/contar peões; `zon/36.zon` lista os vnums exatos |
| 10 | Esgotos = **175 salas** em 4 zonas: 70→62, 71→26, 72→41, 73→46 | Testado | `wld/70.wld`, `71.wld`, `72.wld` (zona 73 inclusa) | — |
| 11 | Newbie Zone (186) tem **41 salas**: 18600–18612 (13) + 18620–18647 (28); **18613–18619 não existem** | Testado | `wld/186.wld` | — |
| 12 | Three of Swords (33) tem **76 salas**, vnums 3300–3375, sem lacunas | Testado | `wld/33.wld`; nome confirmado em `zon/33.zon` ("The Three Of Swords") | — |
| 13 | `mapa.json` tem **359 salas**, não 361; 141 fora da camada "Levantamento" e 218 dentro dela (`lv001`–…) | Testado | `data/heroes/grebolius/mapa.json` (`total_rooms: 359`, `rooms.length = 359`) | recontar com `jq '.rooms|length'` |
| 14 | `mapa_vivo.json` tem **308 salas** e **640 arestas verificadas** (26 sessões, dias 96–156) | Testado | `data/heroes/grebolius/mapa_vivo.json` → `resumo` | recontar com `jq` |
| 15 | A **única** sala de 6 saídas nos dois mapas locais é o Templo de Midgaard | Testado | `mapa.json` → `templo_midgaard`; `mapa_vivo.json` → `r0001` | `olhar` no Templo |
| 16 | A Praça do Templo local reproduz 3005: n=?/u=Templo, e=Estalagem Javali, s=Praça do Comércio, w=Guilda dos Clérigos | Provável | `mapa.json` → `praca_templo`; padrão `wld/30.wld#3005` | sair nas 5 direções e comparar com §2.1 |
| 17 | As quatro salas da Rua Principal (3012, 3013, 3014, 3015, 3016) batem **exatamente**, direção por direção, com as salas locais | Provável | `mapa.json` → `termino_rua_oeste`, `rua_oeste_1`, `praca_comercio`, `rua_leste_1`, `rua_leste_2` | conferir lojas norte/sul de cada trecho |
| 18 | A Guilda dos Magos local (entrada→bar→laboratório) reproduz 3017→3018→3019 **exatamente** | Provável | `mapa.json` → `guilda_magos`, `bar_magos`, `laboratorio_magos` | — |
| 19 | A "Entrada da Guilda dos Clérigos" local tem **4** saídas (e,n,s,w) onde o padrão (3004) tem 2 (n→bar, e→praça) | Dúvida | `mapa.json` → `guilda_clerigos_entrada` vs `wld/30.wld#3004` | entrar na guilda e mapear de novo; a Sala Interna dos Clérigos (3002) não existe no mapa local |
| 20 | A "Entrada da Guilda dos Guerreiros" local aponta `s=bar_magos` (bar dos **magos**) | Dúvida | `mapa.json` → `guilda_guerreiros`; padrão `wld/30.wld#3021` aponta e→3022 (bar dos espadachins) | entrar na guilda dos guerreiros e verificar para onde vai o sul |
| 21 | O padrão não tem **Panteão dos Centenários**, **Guilda dos Necromantes**, **Bar dos Necromantes**, **Agência Lotérica**, **Jareth**, **Fazenda**, **Vila Residencial**, **Avenida Floris**, **Moinho de Vento** | Testado (ausência nas zonas baixadas) | não há vnum correspondente em `wld/30,31,33,36,70,71,72,186` | é modificação do DeBo (ou zona não baixada) — ver §10 |
| 22 | O padrão tem **64 casas** de tabuleiro; o mapa local tem **6** (`casa_branca_xadrez`, `casa_preta_xadrez` + 4 em `mapa_vivo` r0117–r0122) | Testado (padrão e local) | `wld/36.wld` vs `mapa.json`/`mapa_vivo.json` | andar em linha reta para fora das 6 casas conhecidas |
| 23 | O padrão repete nomes de sala; p.ex. **"A Turn In The Passage"** existe em 18620 **e** 18635, e "A Large Room" em 18625, 18638, 18639 | Testado | `wld/186.wld#18620`, `#18635`, `#18625`, `#18638`, `#18639` | o mapa local usa **1** nó (`curva_passagem`) para os dois homônimos |
| 24 | Nada no mundo padrão (zonas baixadas) se chama "Floris", "Jareth" ou "Necromante" | Testado | busca negativa em todos os `.wld`/`.zon` baixados | se o DeBo tem, é conteúdo próprio (ou de zona não baixada) |
| 25 | A **Chave da Cidade** (obj 3112) que abre os portões de Midgaard está com o **Prefeito** (mob 3105, sala 3138) | Testado | `zon/31.zon` ("M 0 3105 1 3138 Mayor" + "E 1 3112 1 17 City Key") | matar/comprar do prefeito na prefeitura — sala que **não existe** no mapa local |

---

## 2. Midgaard (zonas 30 e 31)

Formato: `vnum Nome — saídas (dir→vnum)`. `d`=down, `u`=up. Portas indicadas
com `[porta]` e a chave entre parênteses quando houver.

### 2.1 Zona 30 — Norte de Midgaard (65 salas)

| vnum | Nome (EN) | Saídas |
|---|---|---|
| 3000 | The Reading Room | e→3001 |
| 3001 | **The Temple Of Midgaard** | n→3054, e→3063, s→3005, w→3000, d→3005 |
| 3002 | The Clerics' Inner Sanctum | e→3003, d→7026 |
| 3003 | The Bar Of Divination | s→3004, w→3002 |
| 3004 | The Entrance To The Clerics' Guild | n→3003, e→3005 |
| 3005 | **The Temple Square** | n→3001, e→3006, s→3014, w→3004 |
| 3006 | The Entrance Hall Of The Grunting Boar Inn | n→3062, e→3007, w→3005, u→3008 |
| 3007 | The Grunting Boar (bar) | s→3006 |
| 3008 | The Reception | n→3064, d→3006 |
| 3009 | The Bakery | s→3013 |
| 3010 | The General Store | s→3015 |
| 3011 | The Weapon Shop | s→3016 |
| 3012 | **Main Street** (ponta oeste) | n→3033, e→3013, s→3017, w→3040 |
| 3013 | **Main Street** | n→3009, e→3014, s→3020, w→3012 |
| 3014 | **Market Square** | n→3005, e→3015, s→3025, w→3013 |
| 3015 | **Main Street** | n→3010, e→3016, s→3031, w→3014 |
| 3016 | **Main Street** (ponta leste) | n→3011, e→3041, s→3021, w→3015 |
| 3017 | The Entrance To The Mages' Guild | n→3012, s→3018 |
| 3018 | The Mages' Bar | n→3017, e→3019 |
| 3019 | The Mages' Laboratory | w→3018, d→7017 |
| 3020 | The Armory | n→3013 |
| 3021 | The Entrance Hall To The Guild Of Swordsmen | n→3016, e→3022 |
| 3022 | The Bar Of Swordsmen | s→3023, w→3021 |
| 3023 | The Tournament And Practice Yard | n→3022, d→7048 |
| 3024 | The Eastern End Of Poor Alley | e→3025, s→3048, w→3044 |
| 3025 | **The Common Square** | n→3014, e→3026, s→3030, w→3024 |
| 3026 | The Dark Alley | e→3045, s→3027, w→3025 |
| 3027 | The Entrance Hall To The Guild Of Thieves | n→3026, e→3028 |
| 3028 | The Thieves' Bar | s→3029, w→3027 |
| 3029 | The Secret Yard | n→3028, d→7043 |
| 3030 | The Dump | n→3025, d→7030 [porta, chave 3005] |
| 3031 | The Pet Shop | n→3015 |
| 3032 | Pet Shop Store | **(nenhuma saída)** |
| 3033 | The Magic Shop | s→3012 |
| 3040 | Inside The West Gate Of Midgaard | e→3012, s→3042, w→3052 [porta, chave 3112] |
| 3041 | Inside The East Gate Of Midgaard | e→3053 [porta, chave 3112], s→3058, w→3016 |
| 3042 | Wall Road | n→3040, s→3043 |
| 3043 | Wall Road | n→3042, e→3044, s→3047 |
| 3044 | Poor Alley | e→3024, w→3043 |
| 3045 | The Dark Alley At The Levee | e→3046, s→3049, w→3026 |
| 3046 | The Eastern End Of The Alley | s→3050, w→3045 |
| 3047 | Wall Road | n→3043, s→3051 |
| 3048 | Grubby Inn | n→3024 |
| 3049 | The Levee | n→3045, s→3203 |
| 3050 | The Deserted Warehouse | n→3046 |
| 3051 | On The Bridge | n→3047, s→3100 |
| 3052 | Outside The West Gate Of Midgaard | e→3040 [porta, chave 3112], w→6092 |
| 3053 | Outside The East Gate Of Midgaard | e→3503, w→3041 [porta, chave 3112] |
| 3054 | **By The Temple Altar** | n→3059, s→3001 |
| 3055 | Odin's Store | **(nenhuma saída)** |
| 3058 | Ye Olde Water Shoppe | n→3041 |
| 3059 | **Behind The Temple Altar** | n→3060, s→3054 |
| 3060 | The Great Field Of Midgaard | n→3061, s→3059 |
| 3061 | **The Great Field Of Midgaard** | n→3065, e→18600, s→3060, w→3066 |
| 3062 | The Post Office | s→3006 |
| 3063 | The Midgaard Donation Room | w→3001 |
| 3064 | The Cryogenic Center | s→3008 |
| 3065 | The Great Field Of Midgaard | n→**-1 (bloqueada, "plot device")**, s→3061 |
| 3066 | The Dirt Path | e→3061, w→3600 |

### 2.2 Zona 31 — Sul de Midgaard + rio (62 salas)

| vnum | Nome (EN) | Saídas |
|---|---|---|
| 3100 | The Northwest End Of The **Concourse** | n→3051, e→3101, s→3127 |
| 3101 | The Promenade | e→3102, s→3131, w→3100 |
| 3102 | The Promenade | e→3103, s→3105, w→3101 |
| 3103 | The Promenade | e→3104, s→3132, w→3102 |
| 3104 | The Northeast End Of The Concourse | s→3130, w→3103 |
| 3105 | The Park Entrance | n→3102, e→3106, s→3108 |
| 3106 | Park Cafe | w→3105 |
| 3107 | A Small Path In The Park | e→3108, s→3113 |
| 3108 | A Small Path In The Park | n→3105, e→3109, w→3107 |
| 3109 | A Small Path In The Park | s→3115, w→3108 |
| 3110 | Cityguard HeadQuarters | e→3111 [porta, chave 3105] |
| 3111 | Park Road | n→3131, e→3112, s→3118, w→3110 [porta, chave 3105] |
| 3112 | The Western Park Entrance | e→3113, w→3111 |
| 3113 | A Path In The Park | n→3107, e→3114, w→3112 |
| 3114 | The Pond (setor aquático) | e→3115, w→3113 |
| 3115 | A Path In The Park | n→3109, e→3116, w→3114 |
| 3116 | The Eastern Park Entrance | e→3117, w→3115 |
| 3117 | Emerald Avenue | n→3132, e→3137, s→3119, w→3116 |
| 3118 | Park Road | n→3111, s→3135 |
| 3119 | Emerald Avenue | n→3117, w→3133 |
| 3120 | **The Road Crossing** | n→3133, e→3136, s→3134, w→3135, u→7914 |
| 3121 | Emerald Avenue | e→3134, s→3125 |
| 3122 | Park Road | n→3136, e→3123, s→3126 |
| 3123 | Elm Street | e→3124, w→3122 |
| 3124 | The End Of Elm Street | w→3123 |
| 3125 | Emerald Avenue | n→3121, s→3128 |
| 3126 | Park Road | n→3122, s→3129 |
| 3127 | On The Concourse | n→3100, e→3128, s→3504 |
| 3128 | On The Concourse | n→3125, e→3129, w→3127 |
| 3129 | On The Concourse | n→3126, e→3130, s→3150 [grade, chave 3106], w→3128 |
| 3130 | On The Concourse | n→3104, w→3129 |
| 3131 | Park Road | n→3101, s→3111 |
| 3132 | Emerald Avenue | n→3103, e→3139, s→3117 |
| 3133 | Emerald Avenue | e→3119, s→3120 |
| 3134 | Emerald Avenue | n→3120, w→3121 |
| 3135 | Park Road | n→3118, e→3120 |
| 3136 | Park Road | s→3122, w→3120 |
| 3137 | The Waiting Room (Town Hall) | e→3138, w→3117 |
| 3138 | The Mayor's Office | w→3137 |
| 3139 | Penny Lane | e→3140, w→3132 |
| 3140 | Penny Lane | n→3141, w→3139 |
| 3141 | The End Of Penny Lane | s→3140 |
| 3150 | A Gravel Road In The Graveyard | n→3129 [grade, chave 3106], s→3151 |
| 3151–3153 | A Gravel Road In The Graveyard (3 salas em cadeia) | n↔s entre si (3151: n→3150, s→3152 …) |
| 3154 | In Front Of The Chapel | n→3153, s→3155 [porta] |
| 3155 | Inside The Chapel | n→3154 [porta] |
| 3200 | Under The Bridge | e→3201, w→900 |
| 3201 | On The River | e→3202, w→3200 |
| 3202 | On The River | e→3203, w→3201 |
| 3203 | On The River | n→3049, e→3204, w→3202 |
| 3204 | On The River | e→3205, w→3203 |
| 3205 | On The River | e→5001, w→3204 |

> Observação de dado: as salas **3137 e 3138** (Waiting Room / Mayor's Office)
> têm o campo de zona gravado como `30` em `31.wld`, não `31` — provável erro de
> digitação do arquivo original. As salas de rio **3200–3205** também estão em
> `31.wld` apesar de `zone.lst` atribuir "Midgaard River" à zona 32.

### 2.3 Perfil de topologia de Midgaard (padrão)

- **Nenhuma sala com 6 saídas.** Máximo = **5** (3001 Templo; 3120 Road Crossing).
- **Salas com 4 saídas:** 3005, 3006, 3012, 3013, 3014, 3015, 3016, 3025, 3061,
  3111, 3117, 3129.
- **Becos sem saída (1 saída):** 3000, 3007, 3009, 3010, 3011, 3020, 3031,
  3033, 3048, 3050, 3058, 3062, 3063, 3064, 3106, 3110, 3124, 3141, 3155.
- **Salas sem nenhuma saída (armadilha/armazém de objetos):** **3032** (Pet Shop
  Store) e **3055** (Odin's Store) — o próprio texto diz "é vital que o vnum
  desta sala seja exatamente um a mais que a sala X", é o padrão de *storage
  room* de loja do CircleMUD.
- **Escadas / cima / baixo:** 3001 `d`→praça (degraus do templo); 3002 `d`→7026;
  3006 `u`→3008 (recepção); 3008 `d`→3006; 3019 `d`→7017 (poço do laboratório
  dos magos); 3023 `d`→7048; 3029 `d`→7043; 3030 `d`→7030 (lixo→esgoto);
  3120 `u`→7914 (corrente para a Cidadela Voadora de Redferne).
- **Portas com chave:** 3040/3041/3052/3053 exigem a chave **3112** (City Key);
  3030 e 3129 exigem a **3005** (Sewer Key) e a **3106** (Key To Graveyard)
  respectivamente; 3110/3111 exigem a **3105** (Key To HQ).

---

## 3. Zona 32 — Midgaard River

**Não existe arquivo.** `wld/32.wld` = 404 e `zon/32.zon` = 404. O que se pode
dizer é só: `zone.lst` lista `32 - Midgaard River`, e as salas de rio que
restaram (`3200`–`3205`) vivem em `31.wld`, ligando a doca (`3049`, The Levee /
"A Doca") ao rio, à ponte (`3051`) e a um vnum externo `900` (zona 9, "The River
Island") e `5001` (barras de ferro na muralha leste). **Qualquer comparação da
zona 32 é impossível** — declarado explicitamente em §10.

---

## 4. Zona 33 — Three of Swords ("The Three Of Swords", `zon/33.zon`)

76 salas, `3300`–`3375`, sem lacunas. Estrutura em cinco blocos:

1. **3300–3307 — Encosta / Ferreiro Gabadiel (queimado).** 3300 Scraggly Trail
   (e→3301, w→3500); 3301 (w→3300, d→3302); 3302 (e→3303, u→3301);
   3303 Outside A House (e→3304 [porta], w→3302); 3304 The Smithery
   (e→3305, w→3303 [porta]); 3305 A Small Garden (e→3306, w→3304); 3306 Mountain
   Ridge (s→3307, w→3305); 3307 (n→3306, s→3308).
2. **3308–3317 — Depressão rochosa.** 3308 The Diverging Paths
   (n→3307, e→3341, s→3309, w→3359); 3309 (n→3308, w→3310, u→3308);
   3310 (e→3309, s→3314, w→3311); 3311 (e→3310, w→3312); 3312 (n→3313, e→3311);
   3313 The Overlook (s→3312, é **beco sem saída**); 3314 (n→3310, w→3315);
   3315 (e→3314, s→3316); 3316 (n→3315, e→3317); 3317 A Cave Entrance
   (e→3318, w→3316).
3. **3318–3340 — Caverna dos bandidos (labirinto, 23 salas).** Corredores
   3318–3331 com um ramo de "U" (3331→3335→3336→3340) e um quarto de
   armas (3323). 3329→3330 [porta de madeira] → caverna-escritório.
4. **3341–3358 — Vila de Stanneg by the Mountains.** 3341/3342 encostas;
   3343 Main Road (n→3344 taverna, e→3346, s→3345 loja, w→3342);
   3344 The Mountain Tavern (s→3343); 3345 General Store (n→3343);
   3346 Main Road (e→3348, s→3347 curral, w→3343); 3347 The Corral (n→3346);
   3348 The Intersection (n→3349, e→3355, s→3353, w→3346); 3349 (n→3351,
   s→3348, w→3350 mercado); 3350 Farmer's Market (e→3349); 3351 (e→3352 casa
   [porta], s→3349); 3352 A Private Home (w→3351); 3353 (n→3348, s→3354 casa
   [porta]); 3354 A Private Home (n→3353); 3355 Main Road (n→3356 estalagem
   [porta], w→3348); 3356 Stanneg Inn (s→3355, w→3357, u→3358);
   3357 The Common Room (e→3356); 3358 The Reception (d→3356).
5. **3359–3375 — Monte maldito e covil do dragão.** 3359 (n→3308, s→3360);
   3360 A Ledge (n→3359, u→3363, d→3361); 3361 Outside Of A Cottage (s→3362,
   u→3360); 3362 The Torched Cottage (n→3361); 3363–3366 trilha de montanha
   em cadeia (3363: w→3364, u→3360; 3366: n→3367, e→3365);
   3367 (s→3366, d→3368); 3368 (n→3369, u→3367); **3369 The Cave Entrance**
   (s→3368, d→3370, u→3373) — duas descidas; 3370→3371→**3372 The Pit**
   (sala-armadilha, só s→3371: "você cai através do piso ilusório e morre");
   3373→3374→**3375 The Lair** (d→3374) = covil do dragão **Aglandiir**.

Pontos de interesse para teste: a sala-armadilha **3372**, o dragão
**Aglandiir** em 3375 com o *Dragon's Crown* (obj 3307) e o *Halberd* (obj 3305),
e a porta secreta do quarto de tesouro da zona 73 (não relacionada).

---

## 5. Zona 36 — Chessboard (o tabuleiro)

**67 salas:** `3600` (portão/arco) + **64 casas** `3601`–`3664` + `3665` Black
Treasury + `3666` White Treasury.

**Como as casas se ligam.** É uma grelha 8×8 perfeita. Convenção observada nos
vnums: os blocos de 8 consecutivos formam faixas; `3601`–`3608` é a fileira do
lado preto (rainha, bispos, cavalos, torres), `3609`–`3616` a fileira de peões
pretos, `3617`–`3624` a terceira faixa, … até `3649`–`3656` (peões brancos) e
`3657`–`3664` (oficiais brancos).

Regras verificadas nos blocos `D`:
- Casa de **canto** → 2 saídas (ex.: `3601` e→3602, s→3609; `3608` s→3616, w→3607;
  `3657` n→3649, e→3658; `3664` n→3656, w→3663).
- Casa de **borda** → 3 saídas (ex.: `3602` e,s,w; `3640` n,s,w).
- Casa **interior** → 4 saídas (ex.: `3610` n,e,s,w).
- `3632` (casa branca colada ao portão) tem `e→3600` além das normais — é a
  **porta de entrada** do tabuleiro.
- `3604` (casa da **Rainha Preta**) e `3660` (**Rainha Branca**) têm uma saída
  extra `D5` (escada secreta) para `3665`/`3666` (tesourarias), e as tesourarias
  voltam por `D4`.

**Resets (`zon/36.zon`) — quem nasce onde:**

| Peça (mob vnum) | Quantos | Casas (vnum) |
|---|---|---|
| Black Pawn (3600) | 8 | 3609, 3610, 3611, 3612, 3613, 3614, 3615, 3616 |
| White Pawn (3601) | 8 | 3649, 3650, 3651, 3652, 3653, 3654, 3655, 3656 |
| Black Rook (3602) | 2 | 3602, 3608 |
| White Rook (3603) | 2 | 3657, 3664 |
| Black Knight (3604) | 2 | 3602, 3607 |
| White Knight (3605) | 2 | 3658, 3663 |
| Black Bishop (3606) | 2 | 3603, 3606 |
| White Bishop (3607) | 2 | 3659, 3662 |
| Black Queen (3608) | 1 | 3604 |
| Black King (3610) | 1 | 3605 |
| White Queen (3609) | 1 | 3660 |
| White King (3611) | 1 | 3661 |

= **32 peças** (16 pretas, 16 brancas). Cada peão carrega *Pawn Armour* (obj
3600) e *Pawn Sword* (obj 3602); os oficiais carregam armas próprias (3604–3613).
Os reis carregam as chaves das tesourarias (**Black Treasury Key** 3614,
**White Treasury Key** 3615). Nas tesourarias: **Black Treasury Gold** (obj 3616)
em 3665 e **White Treasury Gold** (obj 3617) em 3666.

---

## 6. Zonas 70–73 — Sewers (175 salas)

Estrutura geral (nomes e graus verificados):

- **Zona 70 — "The Sewer, First Level" (62 salas, `7000`–`7070` com lacunas:**
  faltam 7019, 7020, 7023, 7027, 7032, 7033, 7040, 7042, 7054). Contém:
  - esgoto **lamacento** (`7001`–`7014`, ciclo de curvas com lama);
  - poço velho `7015` (`d`→7105);
  - junções limpas `7016`–`7021`;
  - sala de paredes lisas `7022` (`d`→7112, **sala que derruba você**);
  - esgoto "normal" `7024`–`7039`;
  - eixo `7041` (`d`→7123), entrada `7043`, `7044`;
  - sala com cadeiras `7045`↔`7046`↔`7047` (piscina, `e`→7053 [porta]);
  - corredores escuros em cadeia `7056`–`7060`;
  - esgoto **alagado** `7055`, `7061`–`7070` (água até a cintura, 4 salas de
    travessia);
  - **`7030` The Quadruple Junction Under The Dump** = `n→7029, e→7036,
    s→7031, w→7022, u→3030` (a única ligação Midgaard↔esgoto, via `3030` O
    Depósito de Lixo).
- **Zona 71 — "The Second Sewer" (26 salas, `7100`–`7129` + `7190`).**
  Câmara sob o buraco de lama (`7101`), sob o poço escuro (`7102`, com alçapão
  secreto `d`→7300), junção `7104`, poço velho `7105` (`d`→-1, sem saída).
  Depois a **Borda do Abismo**: `7106`→`7107`→`7108`→`7109`→`7110`→`7111`
  (borda oeste, sentido único), `7113`→`7116` (borda leste), `7115` The Broad
  Ledge, `7117`–`7121` (borda leste em cadeia). Várias salas têm saída `e`/`d`
  para **`7190`/"Mid-Air"** — sala de queda ("9,82 m/s²") que é morte certa.
  `7106`, `7111`, `7121` têm a saída `d` (rocha/step) para `7279` (escada na
  parede do abismo); `7116` tem alçapão secreto para `7280`.
- **Zona 72 — "The Sewer Maze" (41 salas, `7200`–`7299` com lacunas).**
  Três blocos: (a) o **covil dos devoradores de mente** (`7200`–`7208`, esqueleto
  de corredores com portas de pedra/madeira, corredor `7209`, junção `7210`);
  (b) o labirinto de drenos secos/úmidos `7211`–`7234` (inclui `7216` **debaixo
  d'água**, `7218` "The Very Small Room", `7234` The Rat's Lair);
  (c) o **submundo/Abismo**: `7279` (parede do abismo, `d`→7299), `7280` The
  Entrance (altar secreto), `7281` corredor vermelho, `7282` **Realm Of Lost
  Souls** (o "Vazio" — "você está no nada, cercado de estrelas"), `7283`
  T-Crossing, `7284` **The Firedeath** (sala **sem saída** — morte por fogo),
  `7285` The Torture Room, `7286` The Hell Yard, `7299` (fim da descida).
- **Zona 73 — "The Tunnels In The Sewer" (46 salas, `7300`–`7345`, dentro de
  `72.wld`).** Caverna `7300` (com `u`→7102), túneis `7301`–`7313` (lama, vermes,
  sala secreta `7305`, buraco de lama `7306`), estalagmites `7311`–`7314`,
  quarto do tesouro secreto `7316` (atrás de `7315`, "sol de 7 pés"),
  **o covil quadrado** `7317`–`7320` (com as duas placas em verso — "Reyemle
  Grug", "Corama"), a **sala circular com três cabeças de dragão** `7324`
  (vermelha ao norte, verde a leste, azul ao sul; `d` vermelho/azul = porta
  falsa), o cruzamento `7326`, o **covil do dragão vermelho** `7328`,
  `7330` The Windy Tunnel, `7331`–`7334` (sala cintilante, massas cinzentas),
  a **caverna do basilisco** `7336`–`7341` (4 quadrantes + pequena caverna),
  e a **piscina** `7342`–`7345`.

**Mobs dos esgotos (`zon/70.zon`…`73.zon`) — o que nasce onde:**

| Zona | Mob (vnum) | Onde |
|---|---|---|
| 70 | The Mean Bat (7001) ×4 | 7041, 7025, 7004, 7004 |
| 70 | The Sewer Rat (7002) ×2 | 7049, 7031 |
| 70 | The Small Hairy Spider (7003) ×6 | 7039 ×3, 7037 ×2, 7050 |
| 71 | The Earth Beetle (7004) ×1 | 7102 |
| 71 | The Giant Maggot (7005) ×3 | 7112 ×2, 7122 |
| 71 | The Sewer Rat (7002) ×1 | 7104 |
| 71 | The Horrifying Mudmonster (7000) ×2 | 7103 |
| 71 | The Slithering Snake (7006) ×3 | 7113, 7122 ×2 |
| 72 | **Master Mindflayer (7200)** | 7201 (+ Devil Rod, Cloak, Key) |
| 72 | Senior Mindflayer (7201) | 7203 |
| 72 | Junior Mindflayer (7202) ×2 | 7205, 7207 |
| 72 | Wererat (7203) ×10 | 7214, 7213, 7215, 7217, 7219, 7221, 7223, 7225, 7233 ×2 |
| 72 | Gigantic Rat (7204) | 7234 |
| 72 | The Sewer Rat (7002) ×3 | 7285 |
| 72 | The Horrifying Mudmonster (7000) ×5 | 7286 ×2, 7281 ×2, 7280 |
| 73 | **The Red Dragon (7040)** | **7328** |
| 73 | The Sea Hag (7041) | 7344 |
| 73 | The Good Guardian Naga (7042) | 7335 |
| 73 | **The Basilisk (7043)** | **7339** |
| 73 | The Lemure Blob (7044) | 7306 |
| 73 | Jones The Ettin (7045) | 7319 |
| 73 | Herald The Ettin (7046) | 7324 |
| 73 | Chr-eff'n (7010) | 7329 |

---

## 7. Zona 186 — Newbie Zone (41 salas)

`18600`–`18612` (13 salas, entrada e corredores) + `18620`–`18647` (28 salas,
cavernas, ala da guilda e galerias). **18613–18619 não existem.**

Estrutura:

- **Entrada:** `18600` (n→18601, w→3061) → `18601` (e→18602, s→18600) →
  `18602` The Dirty Hallway (e→18603, s→18606 [porta], w→18601).
- **Nó `18603` A Nexus:** n→18644 [porta], e→18646 [porta], s→18607, w→18602.
- **Ala da guilda (limpa):** `18640` The Statue's Room (e→18641, s→18644;
  estátua de **Maynard, Death Jester of the Harlequins**) → `18641` hallway
  (e→18642, w→18640) → `18642` North Stairs (s→18647, w→18641, **u→18643
  sacada**) → `18643` Balcony (s→18645, **d→18642**) / `18645` Balcony
  (n→18643, **d→18647**) → `18647` South Stairs (n→18642, s→18604, w→18646,
  **u→18645**). `18644`/`18646` são os dois corredores iluminados (ambos com
  design do brasão da Guilda Harlequin).
- **Ala suja (cavernas):** `18604` Narrow Passage (n→18647, s→18612 [porta]);
  `18612` The Alchemist's Room (n→18604 [porta], w→18611 [porta], **d→18632**
  escada escura); `18632` The Entrance (n→18627, s→18635, w→18631, u→18612);
  `18605` The Dark Pit (**única saída:** u→18606 [grade]) ↔ `18606` A Small
  Room (n→18602 [porta], e→18607 [porta], d→18605 [grade]);
  `18607` (n→18603, s→18611, w→18606 [porta]); `18611` Another Corner
  (n→18607, e→18612 [porta], w→18610); `18610` (e→18611, w→18609);
  `18609` (e→18610, w→18608); `18608` An Open Field (e→18609, n→3061);
  `18620` A Turn In The Passage (e→18621, s→18629); `18621` T-Intersection
  (e→18622, s→18633, w→18620); `18622` (s→18628, w→18621); `18623` (e→18624,
  s→18627); `18624` (s→18630, w→18623); `18625` A Large Room (e→18626, s→18631);
  `18626` (e→18627, w→18625); `18627` A Crossing Of Corridors (n→18623, e→18628,
  s→18632, w→18626); `18628` (n→18622, w→18627); **`18629` The Red Room**
  (n→18620, e→18630, **d→3061** portal no chão — o "portal vermelho" que
  devolve ao Grande Campo); `18630` (n→18624, s→18634, w→18629);
  `18631` A Passage (n→18625, e→18632, s→18638); `18633` (n→18621, e→18634);
  `18634` (n→18630, s→18637, w→18633); `18635` (n→18632, e→18636);
  `18636` A Branch To The South (e→18637, s→18639, w→18635); `18637` (n→18634,
  w→18636); `18638` A Large Room (n→18631, e→18639); `18639` A Large Room
  (n→18636, w→18638 — na parede: **"beware the Minotaur…"**).

**Mobs (`zon/186.zon`):**

| Mob (vnum) | Onde | Observação |
|---|---|---|
| Pit Beast (18601) | 18605 | no Poço Escuro; carrega um **Cloak** (obj 18604) |
| Newbie Monster (18602) ×2 | 18600, 18607 | — |
| Annoying Newbie (18611) | 18646 | — |
| Clueless Newbie (18612) | 18642 | leva Leggings (18612) |
| Friendly Newbie (18613) | 18640 | leva Vest (18602) |
| Lost Newbie (18614) | 18604 | — |
| Smart Newbie (18615) | 18645 | leva Sleeves, Leggings, Vest, Mace |
| **Dragon (18603)** | 18602 | carrega **Collar** (obj 18607) |
| Newbie Guard (18604) | 18606 | carrega Ring, **Key** (obj 18608), **Helm** (18603) |
| Alchemist (18605) | 18612 | carrega **Light** (obj 18609) |
| Crawler (18606) ×3 | 18602, 18606, 18609 | — |
| Zombie (18607) ×4 | 18620, 18624, 18637, 18633 | — |
| Quasit (18608) ×4 | 18627, 18636, 18638, 18621 | — |
| **Minotaur (18609)** | **18629** (The Red Room) | carrega Horns (18610) e Hide (18611) |
| Spectre (18610) | 18639 | na sala com o aviso do Minotauro |

---

## 8. Comparação com o mapa local

Fonte local: `data/heroes/grebolius/mapa.json` (359 salas) e
`data/heroes/grebolius/mapa_vivo.json` (308 salas). Nomes locais em português;
nomes padrão em inglês.

### 8.a Salas do mapa local que parecem corresponder ao mundo padrão

**Midgaard — correspondências fortes (nome E topologia):**

| Local (`mapa.json`) | Nome local | Padrão (vnum) | Veredito |
|---|---|---|---|
| `templo_midgaard` | O Templo de Midgaard | 3001 | topologia 4/4 + 2 extras (u,d) |
| `altar_templo` | O Altar do Templo | 3054 | **idêntico** (n→3059, s→3001) |
| `atras_do_altar` | Atrás do Altar | 3059 | idêntico (n→3060, s→3054) |
| `sala_leitura` | A Sala de Leitura | 3000 | 1 saída → Templo ✓ |
| `sala_doacoes` | A Sala de Doações | 3063 | 1 saída → Templo ✓ (mas local mostra 2: w e s) |
| `praca_templo` | A Praça do Templo | 3005 | 4/4 ✓ |
| `praca_comercio` | A Praça do Comércio | 3014 Market Square | **4/4 idêntico** |
| `praca_comum` | A Praça Comum | 3025 Common Square | **4/4 idêntico** |
| `rua_oeste_1` | A Rua Principal (Oeste) | 3013 | **4/4 idêntico** |
| `rua_leste_1` | Rua Principal (Leste I) | 3015 | **4/4 idêntico** |
| `rua_leste_2` | Rua Principal (Leste II) | 3016 | **4/4 idêntico** |
| `termino_rua_oeste` | Término da Rua Principal | 3012 | **4/4 idêntico** |
| `guilda_magos` | A Entrada da Guilda dos Magos | 3017 | idêntico (n,s) |
| `bar_magos` | O Bar dos Magos | 3018 | idêntico (n,e) |
| `laboratorio_magos` | O Laboratório dos Magos | 3019 | idêntico (w,d→esgoto) |
| `loja_magias` | A Loja de Magias | 3033 The Magic Shop | idêntico (s→3012) |
| `loja_armas` | A Loja de Armas | 3011 Weapon Shop | idêntico |
| `loja_armaduras` | A Loja de Armaduras | 3020 Armory | idêntico |
| `padaria` | A Padaria | 3009 Bakery | 1 de 1 ✓ (+1 extra) |
| `loja_animais` | A Loja de Animais | 3031 Pet Shop | idêntico |
| `armazem` | O Armazém | 3010 General Store | topologia ✓, nome divergente |
| `entrada_javali` | Estalagem Javali Roncador | 3006 Grunting Boar Inn | 4/4 ✓ (+1 extra) |
| `bar_javali` | O Bar da Estalagem | 3007 The Grunting Boar | idêntico |
| `recepcao_javali` | A Recepção da Estalagem | 3008 Reception | 1 de 2 (falta n→3064) |
| `correio_midgaard` | O Escritório dos Correios | 3062 Post Office | idêntico |
| `portao_oeste` | Dentro do Portão Oeste | 3040 | 2/3 (o `w` local vai para a ponte) |
| `portao_leste` | Dentro do Portão Leste | 3041 | 2/3 (falta a loja de água) |
| `rua_muralha` | A Rua da Muralha (Oeste) | 3042+3043 (2 salas) | comprimida em 1 |
| `ponte_rio` | A Ponte Sobre o Rio | 3051 | **idêntico** (n→muralha, s→Afluência) |
| `canto_afluencia` | O Canto Noroeste Da **Afluência** | 3100 Northwest End Of The **Concourse** | nome = tradução de *concourse*; topologia 1 de 3 |
| `deposito_lixo` | O Depósito de Lixo | 3030 The Dump | idêntico (n,d→esgoto) |
| `beco_escuro` | O Beco Escuro | 3026 Dark Alley | 2 de 3 |
| `guilda_ladroes_entrada` | Entrada da Guilda dos Ladrões | 3027 | idêntico (n,e) |
| `bar_ladroes` | O Bar dos Ladrões | 3028 | 1 de 2 (falta s→3029) |
| `beco_pobre` | O Beco Pobre | 3044 Poor Alley | 2/2 ✓ (+1 extra) |
| `fim_beco_pobre` | O Fim do Beco Pobre | 3024 Eastern End Of Poor Alley | **3/3 idêntico** |
| `taverna_encardida` | A Taverna Encardida | 3048 Grubby Inn | idêntico |
| `guilda_clerigos_entrada` | Entrada da Guilda dos Clérigos | 3004 | 1 de 2 + 3 falsas |
| `atras_do_altar`→`grande_campo_sul` | O Grande Campo (Sul) | 3060 | idêntico (n,s) + 2 extras |
| `grande_campo_bifurcacao` | O Grande Campo (Bifurcação) | 3061 | 4/4 conceitual (n,e,s,w) ✓ |
| `caminho_sujo_xadrez` | O Caminho Sujo | 3066 The Dirt Path | idêntico (e→campo, w→tabuleiro) |
| `grande_tabuleiro_portao` | O Grande Tabuleiro de Xadrez | 3600 | 2 de 2 ✓ (e,w) + 1 extra (n) |

**Área dos Novatos — correspondência quase linha-a-linha com `186.wld`:**

| Local | Padrão | Veredito |
|---|---|---|
| `entrada_novatos` | 18600 | idêntico (w→campo, n→18601) |
| `comeco_passagem` | 18601 | idêntico |
| `corredor_sujo` | 18602 | **idêntico** (w,e,s) |
| `cruzamento_novatos` | 18603 A Nexus | 3 de 4 (falta e→18646) |
| `mais_corredor` | 18607 | **idêntico** (n,s,w) |
| `pequena_sala_guarda` | 18606 | 1 de 3 + 2 links estranhos |
| `outro_canto` | 18611 | **idêntico** (n,e,w) |
| `sala_alquimista` | 18612 | idêntico (w,d,n) |
| `passagem_estreita` | 18604 | idêntico (s→alquimista) |
| `a_entrada` | 18632 The Entrance | **4/4 idêntico** |
| `cruzamento_corredores` | 18627 | **4/4 idêntico** |
| `canto_corredor` | 18623 | idêntico (s,e) |
| `outra_curva` | 18624 | idêntico (w,s) |
| `ramificacao_passagem` | 18630 | 1 de 3 (só s) |
| `intersecao_passagens` | 18634 | 1 de 3 (só s) |
| `mais_outro_canto` | 18637 | 1 de 2 |
| `ramificacao_ao_sul` | 18636 | 2 de 3 (w,s) |
| `curva_passagem` | 18620 **ou** 18635 (homônimos) | funde dois nós |
| `sala_no_canto` | 18628 | n,w (troca n↔s) |
| `outro_canto_subsolo` | 18622 | w ✓, s em vez de n |
| `intersecao_t_passagem` | 18621 | w ✓ (perde e,s) |
| `longa_passagem_leste_oeste` | 18626 | idêntico (e,w) |
| `uma_grande_sala` | 18625 | idêntico (e,s) |
| `uma_passagem` | 18631 | idêntico (n,e,s) |
| `uma_sala_enorme` | 18638 | n,w (padrão tem n,e) |
| `uma_sala_enorme_oeste` | 18639 | idêntico (n,w) |
| `sala_estatua` | 18640 | idêntico (s,e) |
| `o_salao` | 18641 | idêntico (w,e) |
| `escadaria_norte` | 18642 | 1 de 3 (só u) |
| `sacada_norte` / `sacada_sul` | 18643 / 18645 | 1 de 2 cada |
| `escadaria_sul` | 18647 | 1 de 4 |
| `caminho_iluminado_norte` | 18644 | 1 de 2 |
| `caminho_iluminado_leste` | 18646 | 1 de 2 |
| `corredor_iluminado` | 18610 | idêntico (e,w) |
| `fim_corredor_abate` | 18609 | idêntico (e,w) |
| `campo_aberto_elo` | 18608 | idêntico (e,n) |

**Esgotos — correspondência com `70.wld`/`71.wld`:**

| Local | Padrão | Veredito |
|---|---|---|
| `esgotos_entrada` | 7030 Quadruple Junction Under The Dump | **5/5 idêntico** (n,e,s,w,u) |
| `juncao_tripla_norte` | 7029 | 1 de 3 |
| `juncao_tripla_sul` | 7031 | 1 de 3 |
| `esgoto_poco` | 7036 The Pit | idêntico (w,d) |
| `abaixo_do_poco` | 7122 Under The Pit | idêntico (w) |
| `sala_paredes_lisas` | 7022 | idêntico (d) |
| `estranha_intersecao` | 7112 | 2 de 3 (n,e) |
| `esgotos_juncao` | 7017 | 2 de 4 (n,w) — e `u`→3019 ✓ |
| `esgotos_curva` | 7016 | idêntico (s,e) |
| `esgotos_calma` | 7021 | 1 de 3 (só w) |
| `esgotos_enorme` | 7009 | 1 de 4 (só e) |
| `canto_sudoeste_borda` | 7111 | 2 de 4 (n,s) |
| `borda_estreita_sul` | 7108+7109+7110 (3 salas) | comprimidas em 1 |
| `borda_estreita_norte` | 7107 | 1 de 3 |
| `canto_noroeste_borda` | 7106 | 2 de 3 (e,s) |
| `estreita_borda_leste_oeste` | 7113 | 1 de 2 |
| `canto_nordeste_borda` | 7116 | 1 de 3 (perde o alçapão d→7280) |

**Tabuleiro:** `mapa_vivo.json` r0116 = 3600 portão; r0117 = 3632; r0118 = 3624;
r0119 = 3616; r0120 = 3608; r0121 = 3607; r0122 = 3615 — **6 casas**, todas com
topologia **exatamente** igual ao padrão (inclusive `3616 w→3615` e
`3615 n→3607`). `mapa.json` só nomeia duas (`casa_branca_xadrez`,
`casa_preta_xadrez`) além do portão.

### 8.b Ligações que divergem

| # | Divergência | Local | Padrão | Gravidade |
|---|---|---|---|---|
| D1 | Templo com **6** saídas (u→Panteão, d→Praça duplicando s→Praça) | `templo_midgaard` | 3001 tem 5 (sem "up") | alta — o Panteão é conteúdo que não existe no padrão |
| D2 | `guilda_clerigos_entrada` com 4 saídas (e,n,s,w), incluindo n/s/w que no padrão vão para o bar interno e a praça | `guilda_clerigos_entrada` | 3004: n→3003 (bar), e→3005 | alta — a **Sala Interna dos Clérigos (3002) e o Bar da Adivinhação (3003) não existem no mapa local** |
| D3 | `guilda_guerreiros` aponta `s=bar_magos` (bar dos magos) | `guilda_guerreiros` | 3021: e→3022 Bar Of Swordsmen | alta — provável erro de dado local; o **Bar dos Espadachins (3022) e o Pátio de Treino (3023) não existem no mapa local** |
| D4 | `portao_oeste` tem `w=ponte_rio` | `portao_oeste` | 3040: w→3052 (fora do portão) e s→3042 | alta — no padrão a ponte só é alcançável por Wall Road (3047→3051) |
| D5 | `rua_muralha` é **uma** sala com e→beco_pobre | `rua_muralha` | 3042 e 3043 (duas Wall Roads) + 3047 | média — compressão de 3 salas em 1 |
| D6 | `canto_afluencia` com 1 saída | `canto_afluencia` | 3100 tem n→3051, e→3101, s→3127 | média — perde ligação com Promenade e Concourse |
| D7 | `padaria` com `n=grande_campo_bifurcacao` | `padaria` | 3009: só s→3013 | média — provável link espúrio |
| D8 | `entrada_javali` com `s=guilda_magos` | `entrada_javali` | 3006: n,e,w,u (nada ao sul) | média |
| D9 | `recepcao_javali` só com `d` | `recepcao_javali` | 3008: d→3006 **e** n→3064 (Cryogenic Center) | média — a Sala Criogênica não existe localmente |
| D10 | `portao_leste` com `e=a_entrada` | `portao_leste` | 3041: e→3053 (Outside The East Gate) | média |
| D11 | `grande_tabuleiro_portao` / r0116 com `n` para uma casa preta | `grande_tabuleiro_portao` | 3600: **e**→3066 e **w**→3632 apenas (2 saídas) | média |
| D12 | `armazem` (nome "O Armazém") na posição do General Store | `armazem` | 3010 The General Store | baixa — nome divergente, topologia ok |
| D13 | `curva_passagem` é um nó único servindo **dois** vnums homônimos | `curva_passagem` | "A Turn In The Passage" = 18620 **e** 18635 | média — funde dois nós; a própria camada "jareth_fazenda" do `mapa.json` declara a política de "não completar caminhos entre homônimos" |
| D14 | `outro_canto_subsolo` liga por **s** a `sala_no_canto` | `outro_canto_subsolo` | 18622→18628 é **norte** | baixa — inversão de direção |
| D15 | `uma_sala_enorme` liga `w=uma_sala_enorme_oeste` | `uma_sala_enorme` | 18638→18639 é **leste** | baixa |
| D16 | `sala_doacoes` com 2 saídas (w e s) | `sala_doacoes` | 3063: só w→3001 | baixa |
| D17 | `pequena_sala_guarda` com `w=fazenda_fim_estrada` e `s=lb031` | `pequena_sala_guarda` | 18606: n→18602, e→18607, d→18605 | alta — ligação entre a Área dos Novatos e a Fazenda sem correspondência no padrão |

### 8.c Salas do mundo padrão **ausentes** do nosso mapa

**Zona 30 (18 de 65 ausentes):** 3002 (Clerics' Inner Sanctum), 3003 (Bar Of
Divination), 3022 (Bar Of Swordsmen), 3023 (Practice Yard), 3029 (Secret Yard),
3032 (Pet Shop Store), 3055 (Odin's Store), 3058 (Ye Olde Water Shoppe),
3064 (Cryogenic Center), 3045 (Dark Alley At The Levee), 3046 (Eastern End Of The
Alley), 3047 (Wall Road), 3050 (Deserted Warehouse), 3052 (Outside West Gate),
3053 (Outside East Gate), 3065 (Great Field bloqueado ao norte), 3042 (Wall Road
comprimida), 3043 (idem).

**Zona 31 — praticamente inteira ausente.** Não há nenhum equivalente local
para: Promenade (3101–3103), Park Entrance (3105), Park Cafe (3106), os caminhos
do parque (3107–3109, 3112–3116), **The Pond** (3114), Cityguard HQ (3110),
**Park Road** (3111, 3118, 3122, 3126, 3131, 3135, 3136), **Emerald Avenue**
(3117, 3119, 3121, 3125, 3132, 3133, 3134), **The Road Crossing** (3120, com a
corrente para a Cidadela Voadora em `u`), **Elm Street** (3123, 3124),
**Penny Lane** (3139–3141), **Town Hall / Waiting Room / Mayor's Office**
(3137, 3138), **o Concourse inteiro** (3100, 3104, 3127–3130),
**o Cemitério** (3150–3154) e a **Capela** (3155). Exceção: a ponte (3051→
`ponte_rio`) e o canto noroeste do Concourse (3100→`canto_afluencia`).
Nenhuma sala local se chama "Parque", "Jardim" ou "Cemitério" (busca negativa em
`mapa.json` e `mapa_vivo.json`).

**Zona 36 — 58 das 64 casas ausentes** (só a coluna 3607/3608/3615/3616 e
3624/3632 foram levantadas), mais as duas tesourarias (3665, 3666).

**Zonas 70–73 — ~159 das 175 salas ausentes.** O mapa local cobre apenas 16
salas de esgoto. Não há equivalente para: todo o esgoto lamacento (7000–7014),
o poço velho (7015), as salas 7010/7011/7014/7018/7024–7028/7034/7035,
7037–3039, 7041, 7043–7070 (**nenhuma** das salas de água 7055–7070), a
zona 71 quase inteira (7100–7105, 7113–7123, 7129, 7190), **todo** o labirinto
7200–7234 e o submundo 7279–7299, e **toda** a zona 73 (7300–7345).

**Zona 186 — 6 das 41 salas ausentes:** 18605 (The Dark Pit) e 18629 (The Red
Room) não têm equivalente nomeado local — o local não tem Poço Escuro nem Sala
Vermelha; 18633, 18635 (parcial, fundido) e 18644/18646 aparecem só pela metade.

### 8.d Salas do mapa local **sem** correspondente nas zonas baixadas

| Local | Nome | Observação |
|---|---|---|
| `panteao_centenarios` | O Panteão dos Centenários | acima do Templo (`u`); não existe no padrão |
| `guilda_necromantes`, `bar_necromantes` | Guilda/Bar dos Necromantes | saída `n` do Beco Pobre; **não existe** no padrão |
| `vila_residencial_entrada`, `vila_rua_larga`, `vila_caminho_cascalhos` | Vila Residencial de Midgaard | não existe nas zonas baixadas |
| `jareth_*` (5 salas) | Cidade de Jareth | "Jareth" não aparece em nenhum `.wld`/`.zon` baixado |
| `estrada_*`, `vila_estrada_*` (8) | Estrada Midgaard-Jareth | corredor longo que não existe no padrão |
| `fazenda_*` (13) | Fazenda próxima a Jareth | não bate com nenhuma casa de Stanneg (zona 33) |
| `floresta_*` (5) | Floresta | provavelmente zona não baixada |
| `lv001` | A Agência Lotérica de Midgaard | conteúdo próprio |
| `lv008` | Na Base da Torre | provavelmente "High Tower Of Sorcery" (zona 25, **não baixada**) |
| `lv040`, `lv049`, `lv050`, `lv052`, `lv053`, `lv041/052/053` | Moinho de Vento | nenhuma zona baixada tem moinho |
| `lv046` | A Entrada do Labirinto | não identificado |
| `lv014`, `lv022`, `lv036` + 10 outras | Rio | provavelmente zona 32 (arquivo ausente) |
| `lv057` e +14 | Avenida Floris | "Floris" não existe nas zonas baixadas — possivelmente o nome DeBo de Emerald Avenue ou rua própria |
| `paraiso_plano`, `portal_paraiso`, `caminho_vazio`, `fonte_vida` | Paraíso / Vazio / Fonte da Vida | conceito que só existe parcialmente (7282 Realm Of Lost Souls) no padrão |

---

## 9. Vnums e nomes de mobs/objetos interessantes para testar

**(a) O Templo (3001/3054/3059).** No padrão **não nasce nenhum mob** no Templo
nem no Altar — o `zon/30.zon` não traz nenhuma linha `M ... 3001` ou `M ... 3054`.
O que existe lá é **objeto**: um **ATM** (obj 3034) resetado na sala 3001
("O 0 3034 10 3001 ATM") e a **Fountain** (obj 3035) na Praça do Templo (3005).
O `Priest Templar Guard` (mob 3025) nasce em **3004** (entrada da guilda dos
clérigos), não no templo. → teste no DeBo: verificar se o templo do DeBo tem
caixa eletrônico, fonte e nenhum mob.

**(b) Guardas de Midgaard.** `Peacekeeper` (mob 3059) ×5 nas salas
3004, 3014, 3017, 3021, 3027; `Cityguard` (mob 3060) ×5 nas mesmas salas +
`Cityguard` (mob 3067) nas duas entradas internas (3040, 3041); em `zon/31.zon`
mais **4 Cityguards** na Park Road (3111) e o `Mad Guard` ×4 na HQ (3110).
Todos carregam **Long Sword** (obj 3022).

**(c) Chaves — alvos de teste claros:**
`Sewer Key` (3005) com o **Beggar** (mob 3065, sala 3044 Poor Alley);
`Key To Graveyard` (3106) com o **Sexton** (mob 3101, Park Cafe 3106);
`Key To HQ` (3105) com um Cityguard da Park Road (3111);
`Key To Safe` (3108) dentro da **Desk** (obj 3109) na HQ 3110;
`Key To The Desk` (3107) com o **Chief Guard** (3102, sala 3110);
**City Key** (3112) com o **Mayor** (3105, sala 3138) — abre os portões;
`Black/White Treasury Key` (3614/3615) com os reis do tabuleiro;
`Key` (18608) com o **Newbie Guard** (18604).

**(d) Tabuleiro.** 32 peões; mobs 3600–3611; aos domingos/vazios o tabuleiro
tem só o que o `.zon` repõe (10 % de chance de reset por tick, zona `3600 3699
10 1`). Peões: obj 3600 (armadura) + 3602 (espada). Teste: matar um peão e
esperar o repop; descer na casa da rainha (3604/3660) para a tesouraria.

**(e) Esgotos.** Mindflayers (7200/7201/7202) no covil 7200–7208 — o texto do
7202 descreve "crânios com um buraco de três polegadas na testa"; o
**Master Mindflayer** carrega o **Devil Rod** (obj 7200) e uma **Key** (7205).
No nível 3: **Red Dragon** (7040) em 7328, **Basilisk** (7043) em 7339,
**Sea Hag** (7041), **Good Guardian Naga** (7042), **Jones/Herald the Ettin**
(7045/7046), **Chr-eff'n** (7010). Objeto notável: **Dragon's Crown** (obj 3307)
no covil da *zona 33* 3375, não no esgoto.

**(f) Newbie Zone.** O **Minotaur** (18609) está na **Red Room (18629)** e o
aviso "beware the Minotaur" está em 18639 — coerente com o `.zon`, mas o
`M 0 18609 1 18629` põe o Minotauro na sala **anterior** do aviso. O **Dragon**
(18603) fica em 18602 (corredor sujo!), não no Poço. O **Alchemist** (18605)
fica em 18612 com uma `Light` (18609). A regra do `sign` de 18612: "abaixo do
nível 7 e sozinho, ou abaixo do 4, cai fora".

---

## 10. Limites desta pesquisa

1. **Nada aqui prova o DeBo.** O DeBo é traduzido e modificado. Um nome ausente
   no `mapa.json` **não prova** que a sala não existe no DeBo: pode simplesmente
   não ter sido levantada ainda. Das 359 salas locais, **218 (61 %)** estão na
   camada "Levantamento (Dias 96-141)" — muitas delas são capturas de tela, não
   salas propriamente (ex.: `lv072`–`lv074` "Em que você deseja lançar a
   magia?", `lv085`/`lv086` "Sua garganta parece secar…", `lv092` "Um aventureiro
   chegou do sul.", `lv095` "[Pontos e atributos]…", `lv043`/`lv096`–`lv103`
   nomes de *prompt*/barra de status do cliente, não nomes de sala).
2. **Dois arquivos do repositório não existem:** `wld/32.wld`, `zon/32.zon` e
   `wld/73.wld` retornaram **404**. A zona 32 (Midgaard River) **não pôde ser
   comparada de forma alguma**; a zona 73 só pôde ser lida porque seu conteúdo
   está embutido em `72.wld`.
3. **Comparação de topologia só é conclusiva para 16–20 salas locais** onde o
   grafo fecha perfeitamente (Templo, Praça do Templo, Praça do Comércio, Praça
   Comum, as 4 ruas principais, Guilda dos Magos, Guilda dos Ladrões, becos,
   Praça dos Correios/Estalagem, entrada do esgoto 7030, boa parte da Área dos
   Novatos). Fora disso, o `mapa.json` tem **muitos nós de grau 1 e 0** que são
   simplesmente levantamento incompleto, não becos sem saída reais — comparar
   "grau de saída" nessas salas produziria falso positivo.
4. **`mapa.json` e `mapa_vivo.json` divergem entre si**: o primeiro tem 359
   salas, o segundo 308; o segundo usa identidade **por posição no grafo** e
   declara **194 salas com texto idêntico** e **41 destinos de fronteira**
   (`resumo`). Ou seja: o próprio projeto avisa que o texto não é identificador.
   Onde os dois discordam (ex.: Graveyard/Park ausentes em ambos, mas o número
   de salas difere), não sei qual é o mais fiel ao DeBo.
5. **Homônimos.** O padrão repete nomes ("A Turn In The Passage" em 18620 e
   18635; "A Large Room" em 18625, 18638, 18639; "On The River" em 3201–3205;
   "A Gravel Road In The Graveyard" em 3150–3153; "A Small Path In The Park" em
   3107–3109; "The Promenade" ×3). Minhas atribuições `local → vnum` nesses
   casos são **inferência topológica**, não prova. O `mapa.json` já declara a
   política de não fundir homônimos, mas `curva_passagem` parece violá-la.
6. **Não verifiquei** o `src/util/wld2html.c` nem o código-fonte do CircleMUD
   (`src/`): toda a leitura de formato veio dos próprios `.wld`/`.zon`. Também
   não baixei as zonas 0, 9, 12, 15, 25, 26, 35, 40, 41, 50–56, 60–65, 79, 120,
   150 — **qualquer sala local que aponte para `lv008` (torre), `lv046`
   (labirinto), `lv040` (moinho), "Avenida Floris", "Vila Residencial", a
   floresta, o pântano ou a Fazenda/Jareth pode pertencer a uma dessas zonas e
   por isso aparece aqui como "sem correspondente", o que é apenas
   **não-verificado**, não "ausente do CircleMUD padrão".
7. **Truncamento**: quero registrar que **não houve** — todos os 200 OK
   terminaram com `$`. Portanto, dentro do que foi baixado, a contagem de salas
   por zona (§2, §4, §5, §6, §7) é exata, e a lista de ausências (§8.c) é
   exaustiva *para essas zonas*.
8. **`mapa.json` diz `total_rooms: 359`**, não 361 como no pedido; e o campo
   `last_updated_cycle` é "Ciclo X (Dia 156…)" enquanto a camada "Levantamento"
   se chama "(Dias 96-141)" — há uma inconsistência interna de datas no próprio
   arquivo que não investiguei.
