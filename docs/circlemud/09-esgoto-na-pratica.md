# 09 — O esgoto na prática (DeBo): os mobs têm força parecida? Qual nível limpa o esgoto?

Pergunta desta investigação: **"os mobs têm força parecida? qual nível é bom para limpar o esgoto?"** — respondida
só com evidência local (logs de servidor do Devil's Bob MUD, dossiês do projeto e documentos de tese).

**Resposta curta, com o que existe registrado:**

1. **Parecida, sim — dentro dos esgotos.** Os bichos de esgoto medidos (`rato de esgoto`, `cobra`, `pequeno morcego`,
   `larva gigante`) batem todos na mesma faixa: **2 a 36 de dano por acerto**, com a maioria entre 10 e 25. O que muda
   não é a força deles, é o **HP dela**: 61 HP (Dia 81) morre em 3 golpes; 87 HP + AC 50 (Dia 95) foge com 10 HP;
   108 HP + AC 77 (Dia 111) foge com 40 HP.
2. **Nível bom para limpar: não há nenhum nível registrado em que o esgoto tenha sido limpo.** Não existe **um único
   abate** de rato, cobra ou larva em todo o corpus. O melhor resultado registrado é do **Grau 15 (Dia 108)**: ela
   atravessou 4 salas de esgoto sem levar um golpe (só havia uma `larva gigante`, passiva) e saiu por `recall`.
   No **Grau 19 (Dia 111)** o primeiro `rato de esgoto` da primeira sala do esgoto ainda a obrigou a fugir duas vezes.
   No **Grau 11 (Dia 95)** seis cobras em bando a derrubaram de 87 para 10 HP e ela dormiu envenenada na beira do abismo.
3. **A leitura de força (`consider`) é quase idêntica para rato e cobra** no Grau 19 — o que reforça "força parecida"
   entre os mobs do esgoto, e também mostra que o `consider` ali é um alarme pessimista, não uma medida útil.

---

## Fontes consultadas

| Arquivo | Tamanho | Como foi varrido |
|---|---:|---|
| `scripts/local/session_dia81.log` | 112.151 B | **Lido em blocos** (a incursão real mais rica: ratos, morcegos, morte pela cobra) |
| `scripts/local/session_dia95_esgotos.log` | 20.247 B | Lido inteiro (2 conexões no mesmo arquivo) |
| `scripts/local/session_dia95_deep.log` | 3.295 B | Lido inteiro |
| `scripts/local/session_dia95_return.log` | 6.842 B | Lido inteiro (única fonte literal do dragão vermelho) |
| `scripts/local/run_dia95_esgotos.py` | 13.877 B | Lido inteiro |
| `scripts/local/run_dia95_sewers_deep.py` | 754 B | Lido inteiro |
| `scripts/local/run_dia95_return_and_hunt.py` | 1.947 B | Lido inteiro |
| `scripts/local/sewer_hunt.py` | 3.133 B | Lido inteiro |
| `scripts/local/sewer_hunt_log.txt` | 11.377 B | Lido inteiro (execução que **não** chegou ao esgoto) |
| `scripts/local/session_dia61_step1.log` | 3.353 B | Lido inteiro (Grau 8, diante do buraco do Laboratório) |
| `scripts/local/session_live_dia108_20261016_011439_c35da6.log` | 267.689 B | Grep + leitura do trecho do esgoto (linhas 865–1.113) |
| `scripts/local/session_live_dia111_20261016_013534_fcd6da.log` | 5.523.188 B | **Só por grep/leitura de janelas** (~98.800–99.100 e ~111.600) |
| `scripts/local/transcript_dia111_20261016_013534_fcd6da.jsonl` | 8.891.298 B | **Só por grep** |
| `scripts/local/transcript_dia9{6,7,8,9}_*.jsonl` | 2 KB – 215 KB | Grep (esgoto: só menção de passagem pelo Laboratório no Dia 98) |
| `data/heroes/grebolius/evidence/dia95.json` | 20.652 B | Lido inteiro (dossiê do Dia 95) |
| `data/heroes/grebolius/evidence/dia108.json`, `dia111.json` | 755 – 1.193 B | Lidos inteiros |
| `data/heroes/grebolius/evidence/dia9{1..99}.json` | vários | Grep por `esgoto/cobra/serpente/Borda/rato/larva/morcego` |
| `data/heroes/grebolius/monstros.md` | 6.598 B | Lido inteiro |
| `data/heroes/grebolius/conhecimento.md` | 77.279 B | Grep + leituras em blocos (§1, §8, §10, §17) |
| `data/heroes/grebolius/mapa.md` | 24.567 B | Grep + leitura (linhas 62–106 e 198–217) |
| `data/heroes/grebolius/npcs.md` | 26.405 B | Grep + leitura (linhas 252–265) |
| `data/heroes/grebolius/events.json` | 40.196 B | Grep + leitura (linhas 1–30, 380–401, 617–641) |
| `data/heroes/grebolius/missoes.json` | 20.256 B | Grep + leitura (linhas 240–299) |
| `data/heroes/grebolius/state.json` | 18.063 B | Lido (cabeçalho e vitais) |
| `data/heroes/grebolius/evolucao.md` | 155.396 B | Grep + leitura (linhas 1.218–1.227) |
| `data/heroes/grebolius/posts.json` | 366.435 B | **Só por grep** (prosa; não confundir com resposta de servidor) |
| `docs/expedicao_esgotos_dia95.md` | 4.075 B | Lido inteiro |
| `docs/rotinas.md` | 2.518 B | Lido inteiro |
| `docs/circlemud/06-evidencias-debo.md` | 58.055 B | Grep + leitura (linhas 355–392) |
| `automato/rotinas/esgoto.py` | 1.323 B | Lido inteiro |
| `automato/rotinas/_suspensas/` | — | Só contém `xadrez.py`; **nenhuma rotina de esgoto suspensa** |
| `automato/runtime/session_live_dia156_*.log`, `transcript_dia156_*.jsonl` | 121 KB – 4.644.729 B | **Só grep** (sessão viva; nunca lidos inteiros) |
| `scripts/local/debo_bot.py` | (823 linhas) | Grep + leitura (linhas 620–669) para entender `login()` e o `log_path` em modo append |

### O que não deu para varrer

- **`automato/runtime/` inteiro** (sessão viva gravando agora). Só consultei por padrão. Nada de esgoto apareceu: as
  únicas ocorrências são a descrição do *Laboratório dos Magos* ("Cheira tão mal como em um esgoto") e um *chatter*
  de jogador ("to pegando na base de 8000 no esgoto", `automato/runtime/session_live_dia156_20261016_102159_08e293.log:18847`).
- **`transcript_dia111_*.jsonl` (8,9 MB)** e **`session_live_dia111_*.log` (5,5 MB)**: varridos apenas por padrões
  específicos (rato/cobra/esgoto/Borda). Outros encontros no mesmo arquivo podem existir fora dos padrões usados.
- **`data/heroes/grebolius/posts.json` (366 KB)** e **`evolucao.md` (155 KB)**: só por grep. São **crônica**, não log.
- **Não existe nenhum log do Dia 11** (a "primeira morte nos esgotos"). O dia mais antigo com log ao vivo em
  `scripts/local/` é o Dia 61. Tudo sobre o Dia 11 é prosa → confiança **Provável**.

## Limites desta pesquisa

1. **Numeração de linhas**: as linhas citadas seguem a numeração das ferramentas de leitura deste ambiente (split por
   `\n`). Ferramentas que quebram linha de outro jeito (ex.: `Select-String` do PowerShell neste arquivo) devolvem
   números inflados — por isso todas as citações de `session_dia81.log` foram conferidas por leitura direta.
2. **`session_dia95_esgotos.log` contém DUAS conexões.** `DeboClient` abre o log em modo append
   (`scripts/local/debo_bot.py:93`), então o arquivo acumula sessões: a 1ª conexão vai das linhas 1–265 (entrada pelo
   *Depósito de Lixo*, termina com `score`/`save`/`sleep` em *A Estranha Sala Com Paredes Lisas*), e a 2ª conexão
   (linhas 266–490) já começa em *A Borda Estreita* — porque a sessão anterior (`session_dia95_return.log`, 21:06)
   deixou a personagem ali, ao lado do dragão.
3. **`evidence/dia95.json` preserva só a 2ª conexão.** Os 33 `records` têm carimbo 21:09:02–21:09:32, e o campo
   `source_line` é **sintético** (`len(records)+1`, ver `run_dia95_esgotos.py:90`), não a linha real do log. Para o
   Dia 95 eu cito o **log**, não o `source_line` do dossiê.
4. **`source_kind` misturados**: `dia95.json` é `server_log` (Testado); `events.json` é misto (`live` em uns, `document`
   em outros); `posts.json`/`ciclos.json` são crônica (**Provável**).
5. **Não usei `web_fetch`.** Nada foi verificado contra o servidor ao vivo nesta pesquisa.

---

## Tabela de fatos

| # | Fato observado | Fonte (arquivo:linha) | Trecho literal | Confiança |
|---|---|---|---|---|
| 1 | Ela entra no esgoto pelo **Depósito de Lixo** (`d` na Praça Comum) | `scripts/local/session_dia95_esgotos.log:55` | `O Depósito de Lixo … [ Saídas: norte e baixo ]` → `A Junção Quádrupla Abaixo do Depósito de Lixo` (`:61`) | Testado |
| 2 | A **Junção Quádrupla** é a porta de entrada/saída reversível | `scripts/local/session_dia95_esgotos.log:61-66` | `…há uma escada de metal construída na parede de concreto, levando para cima, através de um amontoado de lixo. [ Saídas: norte, leste, sul, oeste e cima ]` | Testado |
| 3 | No Dia 81 ela entra pelo mesmo lugar, no **Grau 10** com **61 HP** | `scripts/local/session_dia81.log:200-206`, `:481-489` | `>>> CMD: d` → `A Junção Quádrupla Abaixo do Depósito de Lixo` ; `nível 10` / `Vida: {<<<<<>>>>>}  61 de 61` | Testado |
| 4 | Mob `um rato de esgoto` ataca ao entrar na sala (aggro por chegada) | `scripts/local/session_dia81.log:362-366` | `Um rato de esgoto chegou do oeste.` / `Você se abaixa para desviar do golpe de um rato de esgoto.` | Testado |
| 5 | Variante do rato com descrição própria | `scripts/local/session_dia81.log:515` | `Um enorme e faminto rato dos esgotos está aqui.` | Testado |
| 6 | Dano do rato no Grau 10/11 (61 HP) | `scripts/local/session_dia81.log:369,405,418,537,575,640,653,680,798,814,916,921,945` | `Um rato de esgoto massacra você com um golpe. [-14]` … `Um rato de esgoto ESTRAÇALHA você com um golpe mortal! [-34]` … `[-36]` | Testado |
| 7 | Ela **foge de rato** 6 vezes no Dia 81, com **custos de XP diferentes** | `scripts/local/session_dia81.log:427,584,688,830,953,1742` | `Você consegue fugir para o oeste.` / `Você perdeu 54 pontos de experiência na sua fuga.` … `[-]` `119`, `251`, `276`, `282` | Testado |
| 8 | **Nenhum rato, cobra ou larva foi morto** em nenhuma sessão registrada | busca por `rato de esgoto está morto` / `uma cobra está morto` / `larva gigante está morto` em todo o corpus | — (só `morcego está morto` aparece) | Testado |
| 9 | Mob `um pequeno morcego` (dormindo no teto) — passivo até ser atacado, dano baixo | `scripts/local/session_dia81.log:1409-1410`, `:1433`, `:1446` | `Um pequeno morcego está dormindo aqui.` / `Um pequeno morcego golpeia seus braços, com dificuldades. [-2]` | Testado |
| 10 | Ela **mata 2 morcegos** e sobe de nível | `scripts/local/session_dia81.log:1915-1917`, `:2046-2051` | `Um pequeno morcego está morto!` / `Você recebe 4.000 pontos de experiência pelo combate.` … `Você recebe 8.400 pontos de experiência pelo combate.` / `Você avançou um nível!` | Testado |
| 11 | Morcego **não dropa moeda** | `scripts/local/session_dia81.log:2052` | `Você não encontra moeda dentro do corpo de um pequeno morcego.` | Testado |
| 12 | XP de morcego ≈ **6.430** e **10.938** (combate + dano) | `scripts/local/session_dia81.log:1915-1918`, `:2046-2050` | `4.000 … pelo combate` + `2.430 … pelo dano causado` ; `8.400` + `2.538` | Testado |
| 13 | A sala **`Uma Intersecção Lamacenta`** contém **larva + cobra** | `scripts/local/session_dia81.log:2196-2202` | `Uma Intersecção Lamacenta` … `Uma larva gigante está aqui, simplesmente existindo.` / `Uma cobra serpenteia em sua direção. Ela parece bastante vil.` | Testado |
| 14 | A **larva gigante não atacou** em nenhum registro (nem no Dia 108) | `scripts/local/session_dia81.log:2201`; `scripts/local/session_live_dia108_20261016_011439_c35da6.log:914` | `Uma larva gigante está aqui, simplesmente existindo.` (sem linha de ataque nas mesmas saídas de sala) | Provável |
| 15 | O servidor chama o bicho de **`cobra`**, nunca de "serpente" | `scripts/local/session_dia81.log:2202`; `scripts/local/session_dia95_esgotos.log:371` | `Uma cobra serpenteia em sua direção. Ela parece bastante vil.` | Testado |
| 16 | Dano da cobra no Grau 11 (61 HP) | `scripts/local/session_dia81.log:2231,2247,2253,2258` | `Uma cobra arrebenta você com uma mordida mortal! [-22]` / `[-18]` / `Uma cobra morde seus braços com força. [-9]` / `[-21]` | Testado |
| 17 | Ela **morre para a cobra** no Dia 81, sem chance de fuga | `scripts/local/session_dia81.log:2256-2266` | `Você tenta furar uma cobra mas faz apenas buracos no ar!` / `Uma cobra arrebenta você com uma mordida mortal! [-21]` / `-3hp …` / `Uma cobra rasga sua jugular com uma mordida…` / `Você está morto!` / `Você perdeu 1.337 pontos de experiência pela sua morte.` | Testado |
| 18 | A "proteção" do wimpy era **13** no início do Dia 81 (não 30) | `scripts/local/session_dia81.log:18` | `Certo, você irá se acovardar se você ficar abaixo de 13 pontos de vida.` | Testado |
| 19 | Ela **deita e dorme dentro do esgoto/Borda** no Dia 95 (e no Laboratório no fim do Dia 81) | `scripts/local/session_dia95_esgotos.log:488` ; `scripts/local/session_dia95_deep.log:89` ; `scripts/local/session_dia81.log:2984-2985` | `10hp 170mn 101mv > Você se deita e dorme.` (Dia 95, na Borda) / `>>> CMD: sleep` → `Você se deita e dorme.` (Dia 81, no Laboratório) | Testado |
| 20 | No Dia 95 (Grau 11, 87 HP, **AC 25 → 50** com `armor`) ela reentra e vai parar na **Borda** | `scripts/local/session_dia95_esgotos.log:208,216,227,443` | `nível 11` / `Vida: 87 de 87` / `Classe de Armadura: 25` → `Classe de Armadura: 50` / `armor ( 51 horas ) +25 em ARMADURA` | Testado |
| 21 | **Escorregador unidirecional**: a sala a oeste da Junção Quádrupla despenca | `scripts/local/session_dia95_esgotos.log:169-178` | `A Estranha Sala Com Paredes Lisas` / `…você ouve um estalido baixo de uma das paredes... e você cai, cai e cai...` / `[ Saídas: baixo ]` | Testado |
| 22 | A Borda fica **abaixo** dessa queda e não é mais "cano": é túnel de pedra | `scripts/local/session_dia95_deep.log:39-43` | `Uma Estranha Interseção` / `Os canos realmente não parecem ser canos de esgoto. Eles parecem ser um túnel de pedra ou uma passagem talhada na rocha.` | Testado |
| 23 | O servidor avisa de **armadilha mortal (DT)** em toda a Borda | `scripts/local/session_dia95_esgotos.log:296,303,346,369,382` | `Você percebe que há algo perigoso por perto!` | Testado |
| 24 | **6 cobras ao mesmo tempo** na `A Estreita Borda Indo de Leste a Oeste` | `scripts/local/session_dia95_esgotos.log:371-376` | `Uma cobra serpenteia em sua direção. Ela parece bastante vil.` (×6) | Testado |
| 25 | Dano das cobras em bando no Grau 11 (87 HP) | `scripts/local/session_dia95_esgotos.log:394-404` | `[-12]` / `[-17]` / `[-19]` / `Uma cobra arrebenta você com uma mordida mortal! [-25]` | Testado |
| 26 | **Envenenamento** confirmado no `score` | `scripts/local/session_dia95_esgotos.log:401-402,456,461` | `Uma cobra te picou!` / `Você se sente muito doente!` / `Você está envenenado!` / `poison ( 9 horas ) -2 em FORÇA` | Testado |
| 27 | **Wimpy disparou** e a fuga salvou a vida, mas cobrou XP | `scripts/local/session_dia95_esgotos.log:407,413-414,416` | `Você sente que está muito fraco e tenta fugir!` / `Você consegue fugir para o leste.` / `Você perdeu 1 ponto de experiência na sua fuga.` / `14hp 170mn 100mv` | Testado |
| 28 | O veneno continuou sangrando HP **depois** da fuga | `scripts/local/session_dia95_esgotos.log:485,488` | `Você sente um veneno queimar em suas veias, e sofre. [-10]` / `Seus ferimentos estão sangrando MUITO!` / `10hp … Você se deita e dorme.` | Testado |
| 29 | **Dragão vermelho** só aparece no log de retorno, não no do esgoto | `scripts/local/session_dia95_return.log:87-88` | `Um ameaçador dragão vermelho encara você, furioso.` / `...ele está rodeado por uma aura multicolorida!` | Testado |
| 30 | O script de retorno **falhou em silêncio** e dormiu ao lado do dragão | `scripts/local/run_dia95_return_and_hunt.py:73` ; `scripts/local/session_dia95_return.log:171` | `print("Retorno concluído com sucesso!")` — mas o log termina em `A Borda Estreita` com `Você se deita e dorme.` | Testado |
| 31 | `sewer_hunt.py` (Grau 8) **nunca chegou ao esgoto** | `scripts/local/sewer_hunt_log.txt:25,117` | `nível 8` … `A Loja de Armaduras` (a rota "s", "w", "s", "w", "e" caiu na loja; nenhum combate, nenhum esgoto) | Testado |
| 32 | No **Grau 15** (Dia 108) ela entra pelo **buraco do Laboratório** e só encontra uma larva | `scripts/local/session_live_dia108_20261016_011439_c35da6.log:890,911-914,932` | `Baixo - A Junção no Esgoto` / `A Junção no Esgoto` / `Uma larva gigante está aqui, simplesmente existindo.` / `nível 15` | Testado |
| 33 | No Grau 15 ela sai do esgoto por **`recall`** — sem escalar de volta | `scripts/local/session_live_dia108_20261016_011439_c35da6.log:1008-1009` | `Retornando para sua cidade natal...` / `Lembre-se, você só poderá retornar gratuitamente até o nível 70.` | Testado |
| 34 | No **Grau 19** (Dia 111) o esgoto tem rato + cobra **na primeira sala** | `scripts/local/session_live_dia111_20261016_013534_fcd6da.log:98823-98833` | `A Junção no Esgoto` / `Um enorme e faminto rato dos esgotos está aqui.` / `Uma cobra serpenteia em sua direção.` | Testado |
| 35 | `consider` no Grau 19 dá veredito quase igual para rato e cobra | `scripts/local/session_live_dia111_20261016_013534_fcd6da.log:98841-98854` | `Nível: 19 Você vence, mas com dificuldades` / `Vida: 108 Você é LOUCO!` (rato) vs `Vida: 108 Você é louco?` (cobra) / `Poder: 9 Você é louco?` / `Precisão: 15 Perfeito!` / `Armadura: 78 Perfeito!` | Testado |
| 36 | No Grau 19 ela **não consegue matar o rato**: 45 de dano e ele continua de pé | `scripts/local/session_live_dia111_20261016_013534_fcd6da.log:98916,98921,98926,98938,98943,98952` | `Você golpeia os braços de um rato de esgoto, que quase nem sente o golpe. [1]` … `[3]` … `Você queima um rato de esgoto com suas pequenas mãos quentes!   [22]` … `[18]` | Testado |
| 37 | No Grau 19 o rato ainda tira 14–21 por golpe e ela foge **duas vezes** | `scripts/local/session_live_dia111_20261016_013534_fcd6da.log:98915,98927,98939,98957-98958,98966-98967,99027` | `Um rato de esgoto golpeia seu peito com muita força. [-21]` / `Você sente que está muito fraco e tenta fugir!` / `Você perdeu 80 pontos de experiência na sua fuga.` / `Você perdeu 73 pontos de experiência na sua fuga.` | Testado |
| 38 | No Grau 19 a cobra **se move para fora da sala** em vez de lutar | `scripts/local/session_live_dia111_20261016_013534_fcd6da.log:98858,111636` | `Uma cobra vai para norte.` / `Uma cobra vai para oeste.` | Testado |
| 39 | **Mana nunca secou nos esgotos** | `scripts/local/session_dia95_esgotos.log:433` ; `scripts/local/session_live_dia111_20261016_013534_fcd6da.log:98977` | `Mana: {<<<<<>>>>>} 170 de 170` (Dia 95, depois do combate) ; `Mana: {<<<<<>>>>-} 224 de 255` (Dia 111) | Testado |
| 40 | Estado atual da personagem (para situar o nível de hoje) | `data/heroes/grebolius/state.json:5,10,21,26,30` | `"day": 156` / `"level": 20` / `"hp": {"current": 113, "max": 113}` / `"mana": 260` / `"mv": 114` | Testado |
| 41 | A sessão viva (Dia 156) **não desceu ao esgoto** | `automato/runtime/session_live_dia156_20261016_121159_9eb61a.log:1165`; `automato/runtime/session_live_dia156_20261016_102159_08e293.log:18847` | só `Cheira tão mal como em um esgoto` (descrição do Laboratório) e um *chatter* de jogador | Testado |
| 42 | A política de risco declarada na rotina atual | `automato/rotinas/esgoto.py:9,35-36` | `DESCRICAO = 'Reconhecer os esgotos sob o Laboratorio dos Magos com cuidado, sem entrar em luta desfavoravel.'` / `if hp_frac(t) < 0.70: print('[esgoto] vida baixa: recuando')` | Testado (código) |
| 43 | A doutrina do projeto: serpente é "letal" e o veredito de rato em esgoto é mortal | `data/heroes/grebolius/conhecimento.md:31`; `data/heroes/grebolius/monstros.md:50-51` | `**Serpente dos Esgotos** … **LETAL NO DIA 11**` ; `**rato** — A Junção no Esgoto — "Você é LOUCO!" — não, mas o veredito engana` ; `**cobra** — A Junção no Esgoto — "Você é louco?"` | Provável (curadoria) |
| 44 | A doutrina de dano da serpente (18–22) é contradita pelos logs | `data/heroes/grebolius/conhecimento.md:172` vs `scripts/local/session_dia81.log:2253` e `scripts/local/session_dia95_esgotos.log:404` | doc: `mordidas brutais de 18 a 22 de dano por turno, nível estimado entre 12 e 15` ; log: `[-9]` e `[-25]` | Testado (o log) |
| 45 | A primeira morte (Dia 11) só existe como **prosa** | `data/heroes/grebolius/events.json:3-14` | `"id": "primeira-morte", "day": 11, … "summary": "Primeira morte nos esgotos e retorno pela Fonte da Vida.", "source_kind": "document"` … `"note": "Migração de registro preexistente; não é transcrição nova do servidor."` | Provável |
| 46 | O projeto diz que o dragão fica em `A Borda Estreita` | `data/heroes/grebolius/mapa.md:211`; `data/heroes/grebolius/npcs.md:263` | `Uma Estranha Interseção → N → O Canto Sudoeste da Borda → N → A Borda Estreita (Covil do Dragão) (habitada por Um ameaçador dragão vermelho)` ; `**LETAL / CRÍTICO.**` | Provável |
| 47 | O plano do Dia 95 previa limpar tudo e prometia Nível 12 com 1–2 abates | `docs/expedicao_esgotos_dia95.md:5,35` | `abatendo todos os monstros avaliados como favorable (rato, morcego, larva, etc.)` ; `1 ou 2 abates nos esgotos já garantirão a ascensão ao Nível 12` | Testado (o texto existe) |
| 48 | O resultado real do Dia 95: **0 abates, 0 XP, 1 sala catalogada** | `data/heroes/grebolius/evidence/dia95.json:10-12` | `"kills": 0, "kill_details": [], "combat_gold": 0, "xp_gained": 0` | Testado |
| 49 | A tese do projeto diz que fugir custa **1 XP** | `docs/circlemud/06-evidencias-debo.md:379,384-385` | `fugir custa 1 ponto de experiência` / `Você perdeu 1 ponto de experiência na sua fuga.` | Provável (mas refutado — ver Divergências) |
| 50 | A regra "não avançar a oeste sem preparo" foi escrita como lição do Dia 95 | `data/heroes/grebolius/conhecimento.md:397` | `**Regra tática:** Nunca avançar a oeste da entrada dos esgotos sem preparo prévio de retorno místico ou cartografia completa das galerias profundas.` | Testado (o texto existe) |
| 51 | O `rato de esgoto` aguentou **123 de dano** sem morrer | `scripts/local/session_dia81.log:743-819` | `[7]`, `[15]`, `[7]`, `[11]`, `[12]`, `[22]`, `[17]`, `[8]`, `[12]`, `[12]` — e o rato ainda aparece como `um rato de esgoto está aqui, lutando contra VOCÊ!` | Testado |
| 52 | A fuga automática (wimpy) **pode falhar** no esgoto | `scripts/local/session_dia81.log:817-818` | `Você sente que está muito fraco e tenta fugir!` / `PÂNICO!  Você não pode escapar!` | Testado |
| 53 | Ela passou de **4 HP para 61 HP sem sair dos canos** (mecanismo não identificado no log) | `scripts/local/session_dia81.log:822,834,838,852,858` | `4hp …` → `30hp 152mn 99mv` → `42hp` → `55hp` → `61hp 160mn 99mv` | Testado |

---

## Mobs encontrados nos esgotos do DeBo

Nome pelo que **o servidor mostrou** (não pelo que o projeto nomeia):

| Mob (literal do servidor) | Sala (literal) | Aggro? | Dano por acerto (observado) | Fugiu? | Fonte |
|---|---|---|---|---|---|
| `um rato de esgoto` | `O Cano do Esgoto Lamacento`, `O Encanamento Lamacento`, `A Junção no Esgoto` | **Sim** — `Um rato de esgoto chegou do oeste.` então ataca | **10, 12, 14, 16, 18, 19, 21, 23, 34, 36** | Não fugiu; ela é que fugiu 6× (Dia 81) | `session_dia81.log:362-369`, `:405`, `:575`, `:798`; `session_live_dia111_*.log:98915-98939` |
| `Um enorme e faminto rato dos esgotos` | `O Cano do Esgoto Lamacento` | Sim (já está na sala) | idem (mesma linhagem de dano) | — | `session_dia81.log:515`, `:618`, `:738`, `:881`, `:904` |
| `uma cobra` | `Uma Intersecção Lamacenta`, `A Estreita Borda Indo de Leste a Oeste`, `A Junção no Esgoto` | **Mordeu por iniciativa**, em bando de 6 (Dia 95) | **9, 12, 17, 18, 19, 21, 22, 25** + veneno (`-10` por pulso, `poison 9 horas -2 FOR`) | Não fugiu do combate; no Dia 111 `Uma cobra vai para norte.` (moveu-se) | `session_dia81.log:2202`, `:2231-2258`; `session_dia95_esgotos.log:371-404`, `:485`; `session_live_dia111_*.log:98827` |
| `Uma larva gigante` | `Uma Intersecção Lamacenta`, `A Junção no Esgoto`, `A Curva Regular` | **Não** — `está aqui, simplesmente existindo` | **Nenhum dano registrado** | — | `session_dia81.log:2201`; `session_live_dia108_*.log:914`, `:977`; `session_live_dia111_*.log:98965` |
| `um pequeno morcego` | `A Entrada do Encanamento` (teto) | Não, se **dormindo**; acorda quando atacado | **2, 3** | — | `session_dia81.log:1409-1410`, `:1433-1446` |
| `Um ameaçador dragão vermelho` | `A Borda Estreita` (**borda do abismo**, abaixo do esgoto por um escorregador) | Sim (encara, furioso) | **Nenhum dano — nunca foi engajado** | — | `session_dia95_return.log:87-88` |
| `Um zumbi` / `novato zumbi` / `Um monstro novato` / `Uma coisa assustadora` | **NÃO nos esgotos**: `O Começo Da Passagem`, `O Corredor Sujo`, `A Passagem` (Área dos Novatos / Catacumbas) | Sim | — | — | `evidence/dia93.json:530`, `evidence/dia94.json:1541` |
| `aligátor` / `jacaré` / `basilisco` / `mindflayer` | — | — | — | — | **Não há nenhuma evidência em nenhum arquivo varrido** |

**Sobre "os mobs têm força parecida?":**

- O veredito comparativo do servidor (`consider`) no Grau 19 dá **o mesmo alarme** para rato e cobra
  (`Vida: "Você é LOUCO!"` vs `"Você é louco?"` — um degrau de diferença) e o mesmo `Poder: "Você é louco?"`.
  Ou seja: **o próprio servidor diz que os dois são ameaça do mesmo porte** para ela.
- A faixa de dano medida é **contínua e sobrepostas**: rato 10–36, cobra 9–25. Não há um "mob fraco" e um "mob forte"
  claramente separados dentro do esgoto.
- O que **diferencia muito** é o HP do grupo: a `cobra` apareceu em **bando de 6** (Dia 95) e o rato em **dupla/chegando
  reforço** (Dia 111: um chegou do leste durante o combate). A força vem do número, não da espécie.
- A exceção real de comportamento é a **`larva gigante`**: aparece repetidas vezes e nunca atacou → é o único mob de
  esgoto que dá para atravessar sem luta.

---

## Números de combate

### Dia 81 — Grau 10 (61 HP) → Grau 11 (67 HP). A incursão real.

| Encontro | O que ela causou | O que ela levou | Fim |
|---|---|---|---|
| Rato #1 (`O Cano do Esgoto Lamacento`) | 16 + 19 + 11 = **46** (perfurou, não matou) | `[-14]`, `[-18]`, `[-19]` = **51** | **fugiu** oeste a `10hp`, `-54 XP` (`:427`) |
| Rato #2 (`Um enorme e faminto rato dos esgotos`, mesma sala) | 11 + 4 + 12 + 7 + 15 + 11 + 10 = **70** | `[-16]`, `[-34]` = **50** | **fugiu** oeste a `11hp`, `-54 XP` (`:584`) |
| Rato #3 | burning hands `[21]` + 13 + 16 + 17 + 11 = **78** | `[-12]`, `[-23]`, `[-19]` = **54** | **fugiu** sul a `7hp`, `-119 XP` (`:688`) |
| Rato #4 | 7 + 15 + 7 + 11 + 12 + 22 + 17 + 8 + 12 + 12 = **123** — **e o rato continuou vivo** | `[-36]`, `[-21]` = **57** | `PÂNICO!  Você não pode escapar!` (`:818`) → só depois **fugiu** leste a `4hp`, `-251 XP` (`:830`) |
| Rato #5 | 12 + 10 + 10 + 5 + 9 = **46** | `[-12]`, `[-14]`, `[-23]` = **49** | **fugiu** leste a `25hp`, `-276 XP` (`:953`) |
| Morcego #1 | míssil `[14]` + `[4]` + `[3]` + burning hands `[19]`, `[38]` + espada `[10]` | `[-2]`, `[-3]` | **morto**: `4.000` (combate) + `2.430` (dano) = **6.430 XP** (`:1915-1918`) |
| Morcego #2 | míssil/burning hands + `[16]` | `[-3]` | **morto**: `8.400` + `2.538` = **10.938 XP** e **`Você avançou um nível!`** → Grau 11, 67 HP (`:2046-2051`) |
| **Cobra** (`Uma Intersecção Lamacenta`) | 13 + 16 + 14 + 20 = **63** (não matou) | `[-22]`, `[-18]`, `[-9]`, `[-21]` = **70** | **MORTE** (`-3hp` → `Você está morto!`), **`-1.337 XP`** (`:2256-2266`) |

Nota: os valores por rato foram lidos bloco a bloco no log (mesma luta contígua). O **rato #4** é o dado mais forte
deste relatório: ela causou **123 de dano** a um único rato e ele **não morreu**. A regeneração dela no esgoto também
está registrada: de `4hp` (`:822`) de volta a `61hp` (`:858`), parada nas salas.

Total de XP de combate no Dia 81: **+17.368** (bate com `events.json:384`). Abates: **2 morcegos**. Mortes: **1**.

### Dia 95 — Grau 11 (87 HP, AC 25→50).

| Encontro | O que ela causou | O que ela levou | Fim |
|---|---|---|---|
| 6 × `uma cobra` (`A Estreita Borda Indo de Leste a Oeste`) | **nada** (o executor estava em fase de catalogação; não atacou) | `[-12]`, `[-17]`, `[-19]`, `[-25]` = **73 de dano em um turno** | **fuga automática** (wimpy 30) para `O Canto Nordeste da Borda`, `14hp`, **`-1 XP`** |
| Veneno (pulso) | — | `[-10]` | `10hp`, dorme no chão da Borda |

Abates: **0**. XP total: **0** (líquido **−1**). Mana: 170/170 intacta.

### Dia 108 — Grau 15 (79 HP, AC 48). Reconhecimento sem combate.

Salas: `A Junção no Esgoto` → `A Curva Regular` → `Uma Calma Junção de Canos` → `A Junção Regular`.
Único mob visto: `Uma larva gigante está aqui, simplesmente existindo.` **Nenhum golpe dado ou recebido.** Saída por `recall`.

### Dia 111 — Grau 19 (108 HP, AC 77, mana 255).

| Encontro | O que ela causou | O que ela levou | Fim |
|---|---|---|---|
| `Um enorme e faminto rato dos esgotos` + `uma cobra` (`A Junção no Esgoto`) | burning hands `[22]`, `[18]` + espada `[1]`, `[3]`, `[1]` = **45** (não matou) | `[-14]`, `[-10]`, `[-21]`, `[-19]`, `[-2]` fome, `[-2]` sede | **2 fugas**: `-80 XP` e `-73 XP`; terminou em `40hp` → `47hp` → `50hp` e saiu por `recall` |

Abates: **0**. A cobra simplesmente `vai para norte`.

### Dano recebido, consolidado por mob

| Mob | Mínimo | Máximo | Média dos valores registrados |
|---|---:|---:|---:|
| `um rato de esgoto` (Graus 10–19) | 10 | 36 | ≈ 20 |
| `uma cobra` (Graus 10–11) | 9 | 25 | ≈ 17 |
| `um pequeno morcego` | 2 | 3 | 2,5 |
| `Uma larva gigante` | — | — | **0 (nunca atacou)** |

---

## O que deu errado

1. **Morte real para a cobra (Dia 81).** Com **wimpy 13**, o golpe de `-21` levou o HP de `18` direto para `-3`: o
   wimpy **não teve chance de disparar**, porque o gatilho só age *depois* do dano do turno. Fonte:
   `scripts/local/session_dia81.log:2256-2266`.
2. **O wimpy também pode FALHAR.** No rato #4 do Dia 81, o gatilho disparou a `4hp` e o servidor respondeu
   `PÂNICO!  Você não pode escapar!`; a fuga só saiu no turno seguinte. Fonte: `scripts/local/session_dia81.log:814-829`.
3. **Rato que aguenta 123 de dano.** O rato #4 recebeu 123 de dano somado e continuou lutando — ela fugiu a `4hp`.
   Fonte: `scripts/local/session_dia81.log:743-819`.
4. **A escorregador unidirecional.** Entrar a oeste da Junção Quádrupla custa a sessão inteira: as cinco tentativas
   seguintes viraram `Você não pode ir por aí...` e a conexão terminou com `score`/`save`/`sleep` ali. Fonte:
   `scripts/local/session_dia95_esgotos.log:169-204`.
5. **A emboscada de 6 cobras (Dia 95).** 73 de dano em um turno só, com envenenamento; ela chegou a `10 HP` — **um HP
   acima da morte** depois do pulso de veneno. Fonte: `scripts/local/session_dia95_esgotos.log:394-404, 485`.
6. **O retorno "de sucesso" que não voltou.** `run_dia95_return_and_hunt.py` mandou comandos cegos (`e`,`u`,`w`,`u`,
   `n,n,n,u`) contando com uma posição que não era a real; o log mostra que ela **andou para o norte até a Borda**, foi
   encarada pelo **dragão vermelho** e terminou com `save` + `sleep` **a poucos passos dele**. O script imprimiu
   `Retorno concluído com sucesso!`. Fonte: `scripts/local/session_dia95_return.log:75-88, 169-171`;
   `scripts/local/run_dia95_return_and_hunt.py:73`.
7. **Esgotamento de fuga no Grau 19 (Dia 111).** Ela atacou primeiro (45 de dano sem matar) e pagou duas fugas
   (`-80` e `-73 XP`) saindo a `40 HP`. Fonte: `scripts/local/session_live_dia111_20261016_013534_fcd6da.log:98915-98967`.
8. **`sewer_hunt.py` (Grau 8) errou a rota inteira.** O script andou `s`, `w`, `s`, `w`, `e` e parou na *Loja de
   Armaduras*; passou o resto do tempo em `Você não pode ir por aí...`, deu `save`/`sleep` e não encontrou **nenhum**
   mob de esgoto. Fonte: `scripts/local/sewer_hunt_log.txt:100-215`.
9. **Mana seca? Nunca nos esgotos.** O único aperto de mana registrado no Dia 81 foi durante a caçada aos **morcegos**
   (`29mn` em `session_dia81.log:2038`) — e ainda sobrou mana. Nos esgotos: `170/170` (Dia 95) e `224/255` (Dia 111).
10. **Sangramento + veneno empilhados.** `Seus ferimentos estão sangrando MUITO!` aparece junto com o pulso de veneno,
    ou seja: mesmo fora de combate ela continua perdendo HP dentro do esgoto.

---

## Até onde ela chegou

### Mapa real percorrido (só o que tem log)

```
O Depósito de Lixo  (Praça Comum, s)
      │ d
A Junção Quádrupla Abaixo do Depósito de Lixo   ← saída reversível ("cima")
      ├ n → A Junção Tripla → (l) A Curva No Cano De Esgoto  / (o) Uma Calma Junção de Canos
      ├ s → Uma Junção Tripla → (l) A Junção que Leva a Três Caminhos / (o) A Junção Regular
      ├ l → O Poço ── d ── Abaixo do Poço ── o ── Uma Estranha Interseção
      └ o → A Estranha Sala Com Paredes Lisas   ← ESCORREGADOR SEM VOLTA
                     │ (queda)
                     ▼
        Uma Estranha Interseção   ("os canos não parecem canos de esgoto")
             ├ n → O Canto Sudoeste da Borda → n → A Borda Estreita  ← DRAGÃO VERMELHO
             │                                        → n → O Canto Noroeste da Borda
             │                                                  → l → A Estreita Borda Indo de Leste a Oeste
             │                                                        ← 6 COBRAS / fuga → O Canto Nordeste da Borda
             ├ l → Abaixo do Poço
             └ o → Uma Junção nos Canos de Esgoto
```

Salas profundas adicionais visitadas no Dia 81 (a partir da malha superior):
`O Encanamento Lamacento`, `O Cano do Esgoto Lamacento`, `O Encanamento`, `A Beira do Encanamento de Esgoto`,
`A Entrada do Encanamento` (morcegos), `O Encanamento no Esgoto`, `A Junção Regular`,
`A Junção no Esgoto` (a "enorme", sob a **coluna de ar** — `Parece ser impossível forçar qualquer caminho para cima`),
`Uma Intersecção Lamacenta` (**local da morte**), com saídas para `A Curva no Encanamento Lamacento`, `O Poço Escuro`
(**nunca visitada**) e `O Encanamento Lamacento`.

**O que a fez recuar, em cada caso:**

| Dia | Grau / HP | Recuou por | Como saiu |
|---|---|---|---|
| 61 | 8 / 52 HP, AC 16 | nem desceu — ficou no *Laboratório dos Magos* olhando o buraco | `sleep` no laboratório |
| 81 | 10→11 / 61→67 HP | **morte** para a cobra em `Uma Intersecção Lamacenta` | `Fonte da Vida` → Templo (`events.json:384`) |
| 95 | 11 / 87 HP, AC 50 | **6 cobras** + veneno; wimpy 30 disparou | fugiu leste e **dormiu na Borda**, envenenada, 10 HP |
| 108 | 15 / 79 HP, AC 48 | nada a fez recuar — só havia uma larva passiva | `recall` (linha 1008) |
| 111 | 19 / 108 HP, AC 77 | **um rato** que não morreu com 45 de dano | 2 fugas + `recall` |

### Tabela "nível dela → o que conseguiu"

| Grau | HP máx | AC | Dia | O que conseguiu no esgoto | Abates | Mortes |
|---:|---:|---:|---:|---|---:|---:|
| 8 | 52 | 16 | 61 | **Nada**: não desceu (só olhou o buraco do Laboratório) | 0 | 0 |
| 8 | 52 | 40 | (s/ dia) | **Nada**: `sewer_hunt.py` errou a rota e parou na Loja de Armaduras | 0 | 0 |
| 10 | 61 | — | 81 | Chegou ao **fundo** da malha (Encanamento/Beira do Encanamento, `A Junção no Esgoto` sob a coluna de ar) | 0 (só 2 morcegos) | 0 |
| 11 | 67 | — | 81 | Limpou os **morcegos**, subiu de nível, e **morreu para a cobra** | 2 (morcegos) | **1** |
| 11 | 87 | 25 → 50 | 95 | Atravessou a malha superior, caiu no escorregador e chegou à **Borda do Abismo**; fugiu do bando de cobras com 10 HP | 0 | 0 |
| 15 | 79 | 48 | 108 | **Atravessou 4 salas de esgoto sem um único golpe** (só larvas passivas) e saiu por `recall` | 0 | 0 |
| 19 | 108 | 77 | 111 | Entrou pela primeira sala, tomou 2 fugas de um rato, 153 XP de custo, e saiu por `recall` com 50 HP | 0 | 0 |
| 20 | 113 | 80 | 156 (hoje) | **Não desceu** — a sessão viva só passou pelo Laboratório | — | — |

**Leitura:** o esgoto nunca foi "limpo". A melhor passagem registrada é do **Grau 15**, e ela só foi tranquila porque
**não havia mob agressivo na sala** — não porque o nível bastasse. No **Grau 19** o mesmo primeiro `rato de esgoto`
ainda expulsou a personagem. Portanto, com a evidência disponível, **não existe nível comprovado em que o esgoto do
DeBo seja limpável**; o que existe é uma janela em que ele é *atravessável sem luta* quando os mobs agressivos não
estão na sala.

---

## O que o projeto já concluiu

- **Política da rotina atual (`automato/rotinas/esgoto.py`)**: "Reconhecer os esgotos sob o Laboratorio dos Magos com
  cuidado, sem entrar em luta desfavoravel" (`:9`); recua se a vida cair abaixo de **70%** (`:35-36`); explora **no
  máximo 12 salas** e volta ao Templo com `save` (`:30, :44`). Ou seja, a automação de hoje **não** é "limpar": é
  **espionar**. Estado declarado em `docs/rotinas.md:33`: `esgoto … em teste`.
- **Doutrina tática (`conhecimento.md:171-173`)**: a serpente tem "dano massivo (mordidas brutais de 18 a 22 de dano
  por turno, nível estimado entre 12 e 15)"; contra 67 HP e AC 16 o combate frontal é "letal em 3 turnos"; e "o mob não
  ataca no milissegundo de entrada: há uma janela de 1 a 2 turnos de observação antes do bote".
- **Economia (`conhecimento.md:182`)**: "Mobs selvagens de esgoto (ratos, morcegos, larvas) dropam **zero moedas de
  ouro**, embora morcegos forneçam picos expressivos de experiência (6.000 a 10.000 EXP cada)".
- **Lição do Dia 95 (`conhecimento.md:395-404`)**: o escorregador é unidirecional; `Passo-Em-Falso` é meio-ar e deve
  ser bloqueado; e "A margem conservadora de fuga (`wimpy 30`) é essencial".
- **Plano do Dia 95 (`docs/expedicao_esgotos_dia95.md`)**: entrada **exclusiva** pelo Depósito de Lixo, "Nunca descer
  pelo buraco do *Laboratório dos Magos* sem pergaminho de retorno, pois a queda lá é de mão única", e contorno
  automático (`avoided_nodes`/`avoided_edges`) ao ver `risky`/`danger`.
- **`docs/circlemud/06-evidencias-debo.md:367-392`** já havia destilado o bloco de fuga do Dia 95 e cravado o custo de
  `1 ponto de experiência`.
- **`mapa.md:75`** marca a `A Junção no Esgoto (Enorme)` como **LETAL / EMBOSCADA** e `mapa.md:72` avisa
  "Fundo do buraco do Laboratório dos Magos. **Não há subida direta**".
- **`monstros.md:50-56`** já registrava a conclusão metodológica certa: "**Um rato lendo 'Você é LOUCO!' é o sinal de
  que o veredito não é sobre espécie**… o mesmo nome genérico (`monstro`, `rato`) é usado por bichos de forças muito
  diferentes. Não usar o veredito para decidir se é NPC."

---

## Divergências entre a evidência e os documentos

| # | O documento diz | A evidência mostra | Fonte |
|---|---|---|---|
| D1 | `monstros.md:66` põe **zumbi e monstro** nos "Esgotos", com salas `O Começo Da Passagem` e `O Corredor Sujo` | Essas salas são da **Área dos Novatos / Catacumbas** (`mapa.md:91-93`); nos logs de esgoto nunca apareceu zumbi nem "monstro" | `session_dia81.log:2172-2219`; `evidence/dia93.json:530` |
| D2 | `conhecimento.md:31` diz que a serpente "causou **a** primeira morte" | `missoes.json:270` atribui à mesma serpente a **segunda** morte (Dia 81), e `missoes.json:253` liga a primeira ao **Dia 11** → a serpente matou **duas** vezes | `conhecimento.md:31` vs `missoes.json:253,260,270` |
| D3 | `conhecimento.md:172`: dano da serpente **18 a 22** | Medido: **9** (`session_dia81.log:2253`) e **25** (`session_dia95_esgotos.log:404`) — a própria `conhecimento.md:402` diz "12 a 25", contradizendo `:172` | `session_dia81.log:2253`; `session_dia95_esgotos.log:404` |
| D4 | `conhecimento.md:172`: "o mob **não ataca** no milissegundo de entrada: há uma janela de 1 a 2 turnos" | No Dia 95 ela recebeu **73 de dano no mesmo bloco de comandos** em que entrou na sala (`w` → "Você não pode ir por aí" → 4 mordidas); no Dia 81 o rato atacou **ao chegar**: `Um rato de esgoto chegou do oeste.` + golpe no mesmo tick | `session_dia95_esgotos.log:391-404`; `session_dia81.log:362-369` |
| D5 | `docs/expedicao_esgotos_dia95.md:35`: "1 ou 2 abates nos esgotos já garantirão a ascensão ao Nível 12" | Dia 95 fechou com **0 abates, 0 XP** e **nível 11** (faltando 4.799) | `evidence/dia95.json:10-12`; `session_dia95_esgotos.log:220-221` |
| D6 | `docs/expedicao_esgotos_dia95.md:33`: entrada/saída **exclusiva** pelo Depósito de Lixo, buraco do Laboratório é mão única | Ela **entrou pelo buraco do Laboratório** no Dia 108 (Grau 15) e saiu por `recall`; e no Dia 111 idem | `session_live_dia108_*.log:890`; `session_live_dia111_*.log:98821` |
| D7 | `docs/circlemud/06-evidencias-debo.md:379-385`: fugir custa **1 ponto** de experiência | Custo real varia: **54, 54, 119, 251, 276, 282** (Dia 81), **80 e 73** (Dia 111), **1** (Dia 95) | `session_dia81.log:427,584,688,830,953,1742`; `session_live_dia111_*.log:98967,99027` |
| D8 | `mapa.md:211` / `npcs.md:263`: o dragão está em `A Borda Estreita` e o Dia 95 o "contornou com sucesso rumo ao norte" (`evolucao.md:1223`) e depois **dormiu e salvou** | O encontro com o dragão está **fora** do dossiê `evidence/dia95.json`, cujo único `source` é `session_dia95_esgotos.log`; e no log de retorno ela dorme **na mesma sala** (`A Borda Estreita`) onde o dragão apareceu | `session_dia95_return.log:87,171`; `evidence/dia95.json:6-8` |
| D9 | `docs/expedicao_esgotos_dia95.md:5`: a expedição "abate todos os monstros `favorable`" e "**nunca para**" | O executor nunca chegou a combater: parou na catalogação de **1 sala** | `evidence/dia95.json:14-33` |
| D10 | `conhecimento.md:182`: ratos/larvas/morcegos dropam **0 ouro** | Confirmado nos **morcegos** (`Você não encontra moeda…`); **não há nenhum registro** de loot de rato ou larva, porque nenhum foi morto — o "0 ouro" de rato/larva é inferência, não medição | `session_dia81.log:2052` |
| D11 | `docs/rotinas.md:33` apresenta a rotina `esgoto` como funcional-ish ("em teste") | O código é um **reconhecedor de 12 passos** (`automato/rotinas/esgoto.py:30`) com recuo em 70% de HP; não há evidência de execução dela em log nenhum | `automato/rotinas/esgoto.py:30-36` |
| D12 | `docs/expedicao_esgotos_dia95.md:35` chama os morcegos de "~6.000–8.600 EXP" | Medido: **6.430** e **10.938** (o segundo acima da faixa) | `session_dia81.log:1915-1918,2046-2050` |

---

## Lacunas

O que **precisa de sessão nova** para ser respondido (nada disso existe no corpus):

1. **Qualquer abate de `rato de esgoto`, `cobra` ou `larva gigante`.** Nunca aconteceu. Sem isso não se sabe o HP real
   desses mobs, nem o XP que dão, nem se dropam item.
2. **Um `consider` completo e limpo dos mobs de esgoto em vários níveis.** O único `consider` de esgoto registrado com
   tabela é do Grau 19 (e as duas leituras vieram sem o comando visível no log). Falta `consider rato/cobra/larva` no
   Grau 12, 15, 20 e 25 para saber **onde a régua vira**.
3. **`O Poço Escuro`** (saída oeste de `A Junção no Esgoto`): nunca visitado. É a única fronteira conhecida do esgoto
   que nunca foi aberta.
4. **`Passo-Em-Falso`**: a saída existe em três salas da Borda e nunca foi testada. Não se sabe se é queda, morte por
   armadilha (DT) ou conexão — só a descrição ("meio-ar", "quedas livres").
5. **O que há a leste de `A Estreita Borda Indo de Leste a Oeste`.** A única vez que ela tentou ir a leste foi a fuga
   bem-sucedida para `O Canto Nordeste da Borda`; e este nunca foi explorado além disso.
6. **A saída `!baixo`** que aparece em `O Canto Noroeste da Borda` e `O Canto Nordeste da Borda`
   (`[ Saídas: leste, sul e !baixo ]`) — nunca tentada; pode ser a "saída bloqueada" do abismo.
7. **Se o buraco do Laboratório é mesmo mão única.** A afirmação de `docs/expedicao_esgotos_dia95.md:33` nunca foi
   testada: nas duas vezes em que ela desceu por lá (Graus 15 e 19) ela saiu por `recall`, não por `u`.
8. **Dano e comportamento da `larva gigante`.** Ela nunca atacou; não se sabe se é inofensiva por design ou se só não
   foi provocada.
9. **Nível real de cada mob de esgoto.** Nenhum log traz `Nível: N` do oponente — o formato `consider` mostra o número
   **dela** e o veredito comparativo. O "nível 12–15" da serpente em `conhecimento.md:172` é estimativa, não medição.
10. **O Dia 11.** Não existe log. Para confirmar a primeira morte (mob, sala, dano, XP perdido) é preciso um registro
    de servidor daquele dia, que não está no repositório.
11. **A sessão viva (Dias 155–156) não foi varrida inteira** (arquivos de até 4,6 MB gravando durante esta pesquisa).
    Se ela entrou no esgoto nesses dias, isso não aparece nos padrões que usei.
