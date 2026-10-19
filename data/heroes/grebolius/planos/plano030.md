# Plano 030 — Capítulo 12: achar a biblioteca da Assistente em Jareth (e recuperar a etapa de Lemin)

| | |
|---|---|
| **Criado em** | 2026-10-19 · Dia 157 |
| **Por** | Claude Sonnet 5.5 (claude-sonnet-5-5) |
| **Herói** | grebolius |
| **Objetivo** | Concluir Ajuda Mágica no Capítulo 12. Xeque-mate segue opcional. |
| **Sessão encerrada?** | sim — Templo de Midgaard; save e sleep confirmados por `_CLOSE sleep`; driver fechado; sem quit. |

## 1. Onde o objetivo está

Executei o Plano 029: subi o driver, andei até Jareth e levantei a cidade a pé. **A biblioteca da Assistente de Bibliotecária ainda não foi encontrada**, e nenhum tomo foi obtido. Achei uma biblioteca privada dentro do castelo do Lorde, mas ela é outra e estava vazia de objetos. O Beco Escuro de Jareth é o trecho que sobrou e é perigoso. **Descoberta nova e importante:** a Ajuda Mágica pode não estar mais ativa (ver §3). Capítulo 12 continua em curso; NÃO está concluído.

## 2. Estado exato

- Templo de Midgaard, dormindo; HP 199/199, mana 430/430, MV 145/145; nível 32, alinhamento 412 (sem queda).
- Ouro 16.059: 359 na mão, 15.700 no banco. Nenhum gasto. 9 mortes e 1 DT, sem mudança. Wimpy 45.
- Inventário: cantil, rosário, mochila de Pellinore (3 pães, segundo o Plano 029), pergaminho de sabedoria. Peso 71 kg.
- armor +36, 17 horas no último score. Invisibility sumiu da lista (expirou ou foi dissipada).
- Cota Claude no início da sessão: 5% usado na janela de 5h, 1% no semanal (`get_usage`). Cota Codex do 029 é outra conta.
- Evidência: `evidence/dia157-biblioteca.json`; transcript `automato/runtime/transcript_dia157_20261019_141906_4cc11d.jsonl`.

## 3. O que já foi descoberto

- **Autoquest possivelmente perdida.** Após o login, `score tudo` não tem a seção [Autoquests em andamento] e `autoquest todas` marca Ajuda Mágica como "Não feita". O Plano 029 dizia "ativa na entrega". Não sei quando saiu do estado; não houve morte nem quit nesta sessão. **Antes de qualquer give, reativar com Lemin** e reconferir o `score tudo` com os dois-pontos da etapa.
- **`where` só vê a zona atual.** `where bibliotecaria` (sem acento) devolve "a Assistente de Bibliotecária - A Biblioteca" nas ruas de Jareth e "Ninguem com esse nome" dentro do castelo. Logo a biblioteca dela fica na zona das ruas. Use isso como bússola: o nome da sala é "A Biblioteca".
- **Castelo do Lorde mapeado** em `mapa.json` (prefixo `jz_`): norte da Avenida Floris (sala antes do Portão Leste) → rua de pedra → Paço do Lorde → ponte → Grande Salão → Saguão → corredor. Biblioteca privada do Lorde no ramo leste do corredor; vazia ("nada parecido" para prateleiras, mesas, livro, tomo). Portas abrem com `open`. A porta leste do Saguão (recepção do Lorde) e a porta sul não foram abertas.
- **Rota Templo → Jareth** por marcos está em `conhecimento.md` §63.
- **Salas de Jareth sem biblioteca:** lista completa na evidência (lojas, guilda, delegacia, templo, tavernas, margem do rio).

## 4. Os bloqueios, e o que já foi tentado

- **Beco Escuro de Jareth.** Entrada pela Rua Bourbon (3ª sala ao sul do Centro, antes da Loja de Trapos da Vovó) para oeste, depois sul, sul. Na 3ª sala há malandros arruaceiros hostis (1 e depois 2). Um golpe = 55 de vida. Fugi duas vezes por `recall` com ~50 de vida. A saída sul e a leste dessa sala não foram exploradas; a biblioteca pode estar lá ou não.
- Sem biblioteca no resto das ruas: Rua do Rio, Floris inteira, Bourbon, margem e passarela de tábuas.
- Nível 60-100 do autoquest "Arrumando a Biblioteca" (visto no catálogo) significa que a biblioteca da Assistente NÃO serve a Grebolius como missão. O que importa é o **cenário**: a sala "A Biblioteca" pode ter livros à venda ou à vista.
- Pesquisa do 029 (`observacoes/pesquisa-tomo-2026-10-19.md`): sem equivalência provada com o DeBo. Não tratar como fonte.

## 5. O próximo passo, e só ele

**Decidir como passar pelo Beco Escuro sem morrer.** Opções, na ordem em que eu tentaria: (a) com HP cheio, armor ativa e wimpy 45, ir só até a 2ª sala do beco e dar `consider malandro` para ver se um só vem; (b) pedir ao autor autorização para matar os malandros, já que são agressores hostis (o AGENTS §15 item 15 permite combate a hostis; a morte aqui NÃO é custo previsto como no Capítulo 6); (c) explorar antes as saídas que sobraram sem entrar na 3ª sala. Só depois reativar Ajuda Mágica em Lyon.

## 6. NÃO REPITA

- Não andar para fora do Beco Escuro: recuar a pé custou ~150 de vida; ao primeiro golpe, `recall`.
- Não procurar a biblioteca nas lojas, guilda, delegacia, templo, tavernas ou castelo: já vistos.
- Não usar `where biblioteca` dentro do castelo, nem com acento.
- Não dar give sem a etapa confirmada (AGENTS #13). Não automatizar falas de missão (#14).
- Não atacar guardas, hóspedes, servos, cavaleiro, ferreiro nem a Mestre da Guilda.
- Não usar xadrez_v2/v3. Não publicar. Não usar quit.
- Não repetir 5x o mesmo comando recusado (andar no escuro): conferir a saída antes.

## 7. Ferramentas e comandos

`python` do PATH é o atalho da Microsoft Store; usar `C:\Users\peter\AppData\Local\Programs\Python\Python312\python.exe`. Driver: `MUD_DAY=157 MUD_WIMPY=45 python automato/nucleo/driver/live_daemon.py` em segundo plano; cliente `python automato/nucleo/driver/play.py "<cmd>"`; encerrar com `play.py "_CLOSE sleep"`. Autoexame: `automato/verificar.py` (18/18 OK). Cota: `mcp__ccd_session_mgmt__get_usage`.

## 8. Devolutiva técnica

| Descobri | Registrei em | O quê |
|---|---|---|
| mapa | `mapa.json` | 29 salas novas (`jz_*`): castelo do Lorde, biblioteca privada, Beco Escuro de Jareth; arestas em `lb021` (norte) e `lv136` (oeste). |
| referência do servidor | `maquina/verificacoes.md` | where só vê a zona; recall em combate; custo de recuar; `open` nas portas do castelo. |
| fato do mundo | `conhecimento.md` §63 | Rota Templo→Jareth, castelo, biblioteca do Lorde, perigo do Beco, autoquest possivelmente perdida. |
| erro do motor | PENDENTE | Nada tocado. `play.py` imprime `sala=None` e o parser não identifica a sala; v2/v3 do xadrez ainda coletam antes da triagem (herdado do 029). |

## 9. Como encerrar a sua sessão

Templo, comida e água, `_CLOSE sleep` (save e sleep confirmados), fechar o driver sem quit, evidência com autoria, plano 031. Respeitar os cortes de cota do AGENTS §13 usando a cota do modelo que estiver jogando.
