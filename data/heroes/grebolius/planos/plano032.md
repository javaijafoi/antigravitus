# Plano 032 — Capítulo 12: tomo de Lemin, ruas de Jareth esgotadas

| | |
|---|---|
| **Criado em** | 2026-10-19 · Dia 157 |
| **Por** | Claude Sonnet 5.5 (claude-sonnet-5-5) |
| **Herói** | grebolius |
| **Objetivo** | Concluir Ajuda Mágica: achar o tomo na etapa de entrega e entregá-lo a Lemin só com a etapa confirmada. |
| **Sessão encerrada?** | sim — Templo de Midgaard; save e sleep confirmados; driver fechado, sem quit. |

Este plano continua o 031 (não editado). Onde divergirem, vale este.

## 1. Onde o objetivo está

Executei o Plano 031. A missão **sobreviveu** ao fechamento e à reabertura do driver: `score tudo` ainda mostra `Ajuda Mágica: Você deve entregar objeto ao personagem.` Percorri por script o que restava das ruas de Jareth fora do Beco Escuro e **não achei a biblioteca da cidade nem o tomo**. Nenhum give. Capítulo 12 segue em curso.

## 2. Estado exato

- Templo de Midgaard, dormindo; HP 199/199, mana 430/430, MV 145/145; nível 32, alinhamento 412.
- Ouro 16.059 (359 na mão, 15.700 no banco). 9 mortes e 1 DT, sem mudança. Wimpy 45.
- Inventário: cantil, rosário, mochila de Pellinore (com pães; contagem não conferida), pergaminho de sabedoria (é "A Lenda de Nambor").
- armor e invisibility lançadas hoje; conferir validade em `score tudo`.
- Evidência: `evidence/dia157-jareth-varredura.json`. Uma única conexão nesta rodada.

## 3. O que já foi descoberto

- Fechar o driver (`_CLOSE`) **não** derruba a missão; o driver nunca envia `quit`. Quem desconfiar, leia `live_daemon.py` `handle` e `close_session`. O motivo de a missão ter aparecido inativa no começo da sessão anterior segue desconhecido: possivelmente já estava perdida antes do fechamento final do Plano 029.
- **Ferramenta nova: `automato/rotas/nav.py`.** Anda por sala-marco, para na primeira divergência, em combate ou recusa, e recusa `say/ask/give/quit/kill`. Rota pronta: `templo-praca-jareth` (26 passos). Uso: `python automato/rotas/nav.py templo-praca-jareth`. Mais rotas se acrescentam ao dicionário `ROTAS`.
- Salas de Jareth sem a biblioteca: ver evidências `dia157-biblioteca.json` e `dia157-jareth-varredura.json`. A zona das ruas tem a Assistente (`where bibliotecaria`), mas a sala não está em nenhum cômodo aberto visitado.
- Candidato único ao tomo: "tomo da sabedoria druídica" ("Um rústico e pesado tomo de livro"), na Sala de Doações de 16 a 17/10, destruído por limpeza nossa. Hoje a sala não tem tomo.

## 4. Os bloqueios, e o que já foi tentado

- A biblioteca da cidade só pode estar atrás de: (a) o **Beco Escuro de Jareth**, onde há malandros hostis (autor: NÃO matar); (b) a **porta leste trancada** da Loja de Trapos da Vovó (`open leste`: "parece estar trancado"); (c) a porta leste da Delegacia (cadeia); (d) as portas fechadas do castelo do Lorde (leste e sul do Saguão, sala de jantar). Nada disso foi forçado.
- Magias de abrir (knock) e chaves não foram investigadas. Perguntar à Vovó ou ao dono do clube não foi tentado.

## 5. O próximo passo, e só ele

**Decidir, com o autor, como lidar com os bloqueios acima.** A minha recomendação: pesquisar nas docs (`help` de magias e de chaves, `maquina/spells.md`) se existe forma legítima de abrir a porta da Vovó, antes de qualquer tentativa no Beco. Só depois, com HP cheio e armor, ir ao Beco **sem lutar**: avaliar se dá para passar invisível ou por trás. Se o autor liberar combate, um malandro por vez e `recall` ao primeiro golpe de 50.

## 6. NÃO REPITA

- Não reconectar sem necessidade (uma conexão por sessão) e jamais `quit`.
- Não andar sala a sala o que está no `nav.py` ou no `mapa.json`.
- Não forçar portas trancadas; não atacar a Vovó, o dono do clube, guardas ou clérigos.
- Não entrar no Beco Escuro de Jareth sem decisão do autor.
- Não pegar nem entregar item fora da etapa; fala de missão sempre manual.
- Não procurar de novo nas lojas, guildas, templo, tavernas, margem do rio, Rua do Rio, Floris inteira, Bourbon, castelo do Lorde (biblioteca vazia).

## 7. Ferramentas e comandos

Python: `C:\Users\peter\AppData\Local\Programs\Python\Python312\python.exe`. Driver: `MUD_DAY=157 MUD_WIMPY=45 python automato/nucleo/driver/live_daemon.py` em segundo plano; cliente `play.py "<cmd>"`; `_CLOSE sleep` só no fim (se `sleep_confirmed` vier False, mandar `sleep` e `save` antes). Navegação: `automato/rotas/nav.py`.

## 8. Devolutiva técnica

| Descobri | Registrei em | O quê |
|---|---|---|
| mapa | nada | Nenhuma sala nova nesta rodada (Sapataria, Meditação e Oração, restaurante do clube vistos; não adicionados ao `mapa.json`). |
| referência do servidor | nada | Porta da Vovó: `open leste` responde "parece estar trancado" (já cabe no bloco anterior). |
| fato do mundo | `conhecimento.md` §65 | Missão sobrevive ao fechamento; ruas de Jareth esgotadas; bloqueios restantes. |
| erro do motor | `docs/agentes/registro_de_evolucao.md` | Criada `automato/rotas/nav.py`; `sala=None` em `play.py` segue sem correção. |

## 9. Como encerrar a sua sessão

Templo, comer e beber, `sleep` e `save` à mão, `_CLOSE sleep` com `sleep_confirmed=True`, evidência com autoria, plano 033, devolutiva.
