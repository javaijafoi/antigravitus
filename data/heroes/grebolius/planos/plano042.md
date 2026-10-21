# Plano 042 — Fonte de cura: fechar a sondagem (Lyon de dia e o teste com déficit)

| | |
|---|---|
| **Criado em** | 2026-10-21 · Dia 157 (sessão marcada Dia 158 nos registros) |
| **Por** | DeepSeek deepseek-flash (dsh) |
| **Herói** | grebolius |
| **Objetivo** | Subtrama "fonte de cura" do capítulo 12 (ordem do autor: **antes** das missões) e, depois, Ajuda Mágica / Torre da Magia |
| **Sessão encerrada?** | sim — Templo de Midgaard, `save` e `sleep` confirmados, driver fechado, sem `quit` |

Substitui o plano 041 (não editado).

## 1. Onde o objetivo está
A sondagem de cura do Dia 158 fechou metade: **nenhum item de cura** no catálogo da Loja de Magias de Midgaard, **guildas de clérigos fechadas** para mago (Midgaard e Jareth), **Banco de Sangue não cura** (é doação remunerada), e o **Hospital de Jareth** foi achado e mapeado — mas `curar` respondeu `Como?!?` ali e em mais cinco salas **com vida cheia (211/211)**. Falta o teste decisivo com **vida abaixo do máximo** e os catálogos de **Lyon de dia** (Pierre e Toulouse), que são a última via barata. Ajuda Mágica segue parada (tomo sem fonte; Xeque-mate bloqueada no Rei).

## 2. Estado exato
- **Local:** O Templo de Midgaard (`templo_midgaard`), dormindo.
- **Vida/mana/MV:** 211/211 · 500/500 · 146/146 (medido no `score tudo` do login e no fecho).
- **Nível:** 33 · EXP 8.576.616 (faltam 423.384 para o 34).
- **Alinhamento:** 462 (Bom) · wimpy 45 · CA 121 base / **147 no login e 177 depois do `cuidar`** (armor relançado; os 30 de diferença não estão explicados).
- **Ouro:** 31.445 (≈30.445 no banco + ~300 na mão + trocados da doação de sangue). Total antes do `prepara`: 31.769.
- **Comida/água:** 4 pães, cantil cheio (repostos na padaria e na fonte do Templo nesta sessão).
- **Autoquests:** nenhuma em andamento (Ajuda Mágica inativa desde o Dia 157).
- **Fonte:** `state.json` (as_of Dia 157, verificação live). Conferir com `score tudo` ao conectar.

## 3. O que já foi descoberto
- **`curar` existe** (`help curar`: "Alguns lugares fornecem serviços de cura... utilize este comando") e deu **`Como?!?`** em: Templo de Midgaard (controle), Entrada da Guilda dos Clérigos (Midgaard), Templo de Todos e Ninguém, Banco de Sangue, **Hospital de Jareth** e Meditação/Oração — todos com 211/211. Não distingue "não existe" de "não aqui" com vida cheia.
- **Hospital de Jareth (novo, mapeado):** de `jr_tabuas_2` (Caminho de Tábuas, o da Biblioteca) **oeste** → `jr_tabuas_3` ("Ao sul você pode seguir para o Hospital") → **sul** → `jr_hospital`. Enfermeira e Pacificador. `heal` também `Como?!?`; `say oi` e `ask enfermeira ...` sem resposta.
- **Banco de Sangue (`jv_banco_sangue`):** aviso manda "GIVE BLOOD"; medido 211→201 hp, moedas na mão e vida restaurada no comando seguinte. **Doação não serve de déficit.**
- **Salão dos Deuses (`templo_salao_deuses`):** "ventos sagrados curam mais rápido" — regeneração, não serviço.
- **Guildas dos Clérigos:** oeste de `templo_meditacao` (Jareth) e norte de `guilda_clerigos_entrada` (Midgaard) dão "O guarda te humilha e não deixa você passar." Classe bloqueada.
- **Loja de Magias de Midgaard:** 10 itens, **nenhum de cura**; `list <número>` devolve "Por enquanto, nada disto está sendo vendido" — o que funciona é `list <palavra>`.
- **Sala de Doações:** "Há muitos objetos jogados aqui." e nenhum `look`/`look chao`/`look all`/`look junk` enumera.
- **Direções:** `baixo` por extenso → `Como?!?` (usar `d`); `oeste` idem (`w`).
- **Mapa:** 11 salas novas + arestas (`jr_tabuas_3`, `jr_hospital`, `jv_veneracao_1..3`, `jv_banco_sangue`, `templo_todos`, `templo_salao_deuses`, `templo_capela_altar`, `templo_sala_sugestoes`, `templo_meditacao`); `jr_tabuas_2` ganhou `w` e `lb020` ganhou `s`.

## 4. Os bloqueios, e o que já foi tentado
- **`curar` com vida cheia:** seis salas, sempre `Como?!?`. Não repetir sem déficit. Hipótese (não medida): o gatilho da sala só existe com vida abaixo do máximo.
- **Déficit:** a doação de sangue devolve a vida; fome/sede custam vida devagar. Falta um combate curto (com `consider`) ou outra fonte de dano.
- **Lyon:** lojas fecham de noite ("Volte mais tarde!"). O jogo anda ~75 s reais por hora; conferir `time` antes de sair.
- **Tomo (Ajuda Mágica):** nada em Midgaard/Lyon/Jareth, doações, pergaminhos, Campanário e segundo andar de Notre Dame. Abertos: Loja do Escriba (Silverthorne, rota desconhecida), book of riddles (Pirâmide, zona 53), Torre da Magia (`help mapa 29`).
- **Driver:** já houve duas quedas por reconexão que derrubaram a autoquest; conferir `_STATUS` a cada poucos minutos.

## 5. O próximo passo, e só ele
Conectar (`python scripts/mandabala.py`, `live_daemon.py` com `MUD_DAY=158 MUD_WIMPY=45`), `prepara.py --forcar`, `cuidar.py` e, **se o jogo estiver de dia** (`time`), `navegar.py --para cap12_027` e, em Pierre (`cap12_027`) e Toulouse, `list` mais `list` pela palavra do item em cada produto — procurar `heal`/`cure`. **Padrão, se estiver de noite:** ir ao Hospital de Jareth (`jr_hospital`), tirar uma amostra de vida num combate curto com `consider` e rodar `curar` com a vida abaixo do máximo; se curar, medir **ouro ÷ HP** na segunda vez. Nada de compra acima de 5% do ouro (1.572) sem o autor.

## 6. NÃO REPITA
- Não testar `curar` com vida cheia (já são seis negativos); não repetir `curar` três vezes seguidas na mesma sala.
- Não comprar cetro (22.999), poção mágica (9.835) nem cajado retorcido (14.570) "no escuro".
- Não tentar entrar nas guildas de clérigos (guarda humilha); não insistir em `baixo`/`oeste` por extenso.
- Não insistir em `list <número>`; não usar `look`/`look all`/`look junk` para enumerar a Sala de Doações.
- Não doar sangue esperando déficit; não dar `give` fora de etapa; não `quit`; não testar magia no Templo nem em loja.
- Não repetir o kite no Rei com o dano atual (§73, §76).

## 7. Ferramentas e comandos
Python: `C:\Users\peter\AppData\Local\Programs\Python\Python312\python.exe`. `play.py "cmd;cmd"`, `navegar.py --de <id> --para <id>`, `prepara.py --forcar`, `cuidar.py`, `mandabala.py --sobre <alvo>`. Abertura: `python scripts/mandabala.py`. O `navegar` recusa `--de` quando o título da sala repete (ex.: "Rua Principal" tem 3 ids) — passar o id certo.

## 8. Devolutiva técnica
| Descobri | Registrei em | O quê |
|---|---|---|
| mapa | `mapa.json` | 11 salas e 13 arestas novas (Hospital de Jareth, Via da Veneração, Templo de Todos e Ninguém, Salão dos Deuses, Banco de Sangue, Meditação/Oração, capela, sugestões) |
| referência do servidor | `maquina/verificacoes.md` | tabela com a resposta literal de `curar` em 6 salas, `list <n>` na Loja de Magias, `give blood`, `baixo` por extenso |
| fato do mundo | `conhecimento.md` §86 e §87 | Hospital, Banco de Sangue, Salão dos Deuses, guildas fechadas, catálogo sem cura, o que ficou aberto |
| erro do motor | `automato/CHANGELOG.md` | nada novo; `auditar_sessao.py` marca `give blood` como `give-sem-etapa` (falso positivo a tratar) e o `_CLOSE` perde o `save_confirmed` quando a dica chega no lugar da confirmação |

## 9. Como encerrar a sua sessão
Siga `docs/agentes/PROTOCOLO.md` §3: `_CLOSE sleep` no Templo (se `save_confirmed` vier falso, repetir `_CLOSE` que a resposta "Salvando os seus atalhos." confirma), evidência com `agent`, `python scripts/encerrar.py --agente "<modelo/versão>"`, preencher o plano 043, `python scripts/encerrar.py --agente "<modelo/versão>" --fechar --avanco sim --tipo missao`.
