# Plano 031 — Capítulo 12: o tomo de Lemin, com a missão ativa e na etapa certa

| | |
|---|---|
| **Criado em** | 2026-10-19 · Dia 157 |
| **Por** | Claude Sonnet 5.5 (claude-sonnet-5-5) |
| **Herói** | grebolius |
| **Objetivo** | Concluir Ajuda Mágica: obter o tomo na ordem das etapas e entregar a Lemin só com a etapa confirmada. |
| **Sessão encerrada?** | sim — Templo de Midgaard; save confirmado; sono NÃO confirmado; driver fechado, sem quit. |

Este plano substitui o 030 (não editado). Onde divergirem, vale este.

## 1. Onde o objetivo está

Reativei a missão. No começo da sessão ela NÃO estava ativa (o Plano 029 dizia que estava). Refiz a conversa com Lemin em Lyon e o `score tudo` agora mostra **`Ajuda Mágica: Você deve entregar objeto ao personagem.`** O primeiro material é "um tomo de pergaminho bem grosso. Pode ser usado mesmo." Falta achar esse tomo. Nenhum give foi feito. Capítulo 12 segue em curso.

## 2. Estado exato

- Templo de Midgaard; HP 199/199, mana 430/430, MV 145/145; nível 32, alinhamento 412. Ouro 16.059 (359 na mão, 15.700 no banco). 9 mortes e 1 DT, sem mudança.
- Comi 1 pão da mochila e bebi do cantil durante a conversa; sem fome nem sede ao sair. Quantos pães restam na mochila não foi conferido; conferir antes de sair.
- armor +36 (cerca de 17 horas) e invisibility lançada no início; revalidar com `score tudo`.
- Sessão fechada com `_CLOSE sleep`: save confirmado, **sleep não confirmado**. Evidência: `evidence/dia157-lemin-reativacao.json`.

## 3. O que já foi descoberto

- **Cadeia que reativa a missão (feita ao vivo, sem script):** `look lemin`; `say sim`; esperar a pergunta inteira até "esperando a resposta"; `say Merlin`; ouvir a história; quando o `score tudo` pedir, `say sim`; de novo `say sim` ao "pode trazê-los?". Cada resposta só depois de ler o texto e conferir o score. Lemin repete o pedido do tomo a cada ~30 s.
- **Experimento aberto:** a missão estava ativa no fim da sessão anterior e sumiu até o início desta. Pode ser que fechar o driver derrube a missão, apesar do §59 do conhecimento. **A primeira coisa da próxima sessão é rodar `score tudo` e ver se a linha continua lá.** Se sumir de novo, o motivo é o fechamento da conexão, e então só se deve fechar a sessão depois de entregar o material, ou a cadeia refeita a cada retomada.
- Candidato ao tomo: só o `tomo da sabedoria druídica` ("Um rústico e pesado tomo de livro"), visto na Sala de Doações de 16 a 17/10 e destruído com junk por uma limpeza nossa. Sem prova de ser o item do Lemin. Hoje a sala não tem nenhum tomo.
- Biblioteca da Assistente de Bibliotecária em Jareth: não achada; está na zona das ruas (ver `where bibliotecaria`). A biblioteca privada do Lorde (castelo) está vazia. O Beco Escuro de Jareth tem malandros hostis e o autor mandou NÃO matá-los.
- Rota Templo→Lyon por script a partir do `mapa.json` (camada `franca_cap12`): d, s, w, w, w, w, w (portão), w, w, w, w (Borda), w (Trilha Iluminada, a primeira, com saída norte), n, n, w (Bifurcação), n, w, n, n, e (Entrada Para a França), s, s, s, s (Centro). Conferir a primeira Trilha Iluminada: andei 2 salas a mais à oeste porque contei mal.

## 4. Os bloqueios, e o que já foi tentado

- Fonte do tomo desconhecida. Descartados hoje: Sala de Doações (3 livros, nenhum é tomo), pergaminho de sabedoria (é "A Lenda de Nambor"), lojas de Midgaard, Lyon e Jareth, guilda dos magos de Jareth, castelo do Lorde.
- Ainda não vistos: Beco Escuro de Jareth (perigoso), sala de jantar e portas leste/sul do castelo do Lorde, Pequena Passagem do castelo de Welmar, e a biblioteca da cidade de Jareth.
- Pesquisa do 029 não prova equivalência do mundo original.

## 5. O próximo passo, e só ele

**Conferir se a missão sobreviveu ao fechamento** (`score tudo`, primeira linha de trabalho). Depois, procurar o tomo SEM comprar nem entregar nada às cegas: o próximo alvo é a biblioteca da cidade de Jareth, pela zona das ruas, sem entrar no Beco Escuro. Quando achar um candidato, trazer a Lemin, ouvir, reconfirmar o `score tudo` com a instrução da etapa e o `inventory`, e só então `give`.

## 6. NÃO REPITA

- Não andar sala a sala o que já está no `mapa.json`: usar script de navegação por sala-marco (diretiva §9, §20). Conversas de missão continuam manuais.
- Não pegar nem entregar item antes da missão estar ativa e na etapa de entrega (diretivas §19 e §21).
- Não matar os malandros do Beco Escuro (decisão do autor). Não atacar inocentes.
- Não editar planos antigos; não usar quit; não publicar; não usar xadrez_v2/v3.
- Não dizer `say sim` a quem não for o Lemin enquanto o tomo não for entregue.

## 7. Ferramentas e comandos

Python: `C:\Users\peter\AppData\Local\Programs\Python\Python312\python.exe`. Driver: `MUD_DAY=157 MUD_WIMPY=45 python automato/nucleo/driver/live_daemon.py` em segundo plano; cliente `play.py "<cmd>"`; fechar com `play.py "_CLOSE sleep"`. A fala do NPC chega no log (`automato/runtime/session_live_dia157_*.log`) depois do retorno do `play.py`; ler o log antes de responder. Cota Claude: `get_usage` (5% e 1% no início).

## 8. Devolutiva técnica

| Descobri | Registrei em | O quê |
|---|---|---|
| mapa | `mapa.json` (feito antes, no Plano 030) | Nenhuma sala nova neste trecho; rota para Lyon só reutilizada. |
| referência do servidor | `maquina/verificacoes.md` | Nenhuma resposta nova além das do bloco anterior. |
| fato do mundo | `conhecimento.md` §64 | Cadeia de reativação, missão inativa no login, único candidato ao tomo e sua destruição, estado de fome na conversa. |
| erro do motor | PENDENTE | `_CLOSE sleep` devolveu sleep_confirmed=False nesta vez; `play.py` mostra `sala=None`; xadrez v2/v3 inalteradas. Sem correção. |

## 9. Como encerrar a sua sessão

Templo, comer e beber, `_CLOSE sleep` e conferir `sleep_confirmed`; se vier False, mandar `sleep` e `save` à mão e conferir. Evidência com autoria, plano 032, devolutiva.
