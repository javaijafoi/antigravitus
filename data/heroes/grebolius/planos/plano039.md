# Plano 039 — Xeque-mate: recomeçar pela rotina em Python e matar o Rei Negro por kite

| | |
|---|---|
| **Criado em** | 2026-10-20 · Dia 157 |
| **Por** | Claude Sonnet 5.5 (claude-sonnet-5-5) |
| **Herói** | grebolius |
| **Objetivo** | Capítulo 12: concluir a autoquest Xeque-mate (cetro do Rei Negro) |
| **Sessão encerrada?** | sim — Templo de Midgaard, dormindo; save e sleep confirmados; driver parado; sem quit. |

Este plano **substitui o 038** (meu, não é editado). A cascata foi refeita até a **Rainha Negra** (morta) e **perdida pela morte #12**: fiquei esperando a ordem do Bispo em **E1, a casa do Rei Branco**, que mata quem está na Xeque-mate ("Herege! Você deu xeque-mate no rei errado!"). A causa foi um `look` atrasado que me fez julgar estar em F1. Por isso nasceram o mapa do tabuleiro e o `xadrez_cascata.py`.

## 1. Onde o objetivo está
A Xeque-mate **não está ativa**. Recomeçar com o Bispo Branco em F1 e refazer a cascata numa conexão (fechar a sessão também a derruba). Falta, no fim, matar o **Rei Negro pessoalmente** (o servidor recusa cetro de outro monstro: "não é o item correto ou você não é o dono original"). Tática decidida pelo autor: **chegar, sleep, curse, blind e kite** (um raio, recall), sem escolta.

## 2. Estado exato
- **Local:** O Templo de Midgaard (`templo_midgaard`), dormindo.
- **Vida/mana/MV:** 226/226 · 426/490 · 146/146 · **nível 33** · EXP 8.315.136 (próximo nível em 9.000.000).
- **Alinhamento:** 486 (Bom) · wimpy 45 · CA 112 com tudo vestido, sem buffs (148 com `armor`) · morreu 11 vezes e 1 DT.
- **Atributos:** força 13, constituição 9, destreza 17, inteligência 19, sabedoria 17, carisma 12 · acerto 12, dano 5 (sem arma empunhada).
- **Ouro:** 72.078 (67.301 banco + 4.777 mão) → rodar `prepara.py --forcar` antes de sair.
- **Vestida:** Coroa da Rainha Branca, brinco de novato, colar com pedra púrpura (ANTI-DT) e coleira do dragão, mochila de Pellinore (sobre o corpo), veste de escamas, braçadeiras, luvas, bracelete, rosário, dois anéis, escudo de aço, cinturão, calça, botas negras.
- **Mochila** (só alivia peso vestida): 4 Lanças do Cavaleiro Negro (4.000 cada), coroas da Rainha Negra, Armadura da Torre Branca, Cetro do Bispo Negro, manto, gorro, rolo, pergaminho, bainha de Excalibur, Cruz Ansada. Peso ~76/140 kg. **Armeiro e Ferreiro estão sem caixa**: vender depois.
- **Treino:** 70 sessões sobrando (nada a treinar agora); `charm person` 95% (inútil no Rei e na Rainha: Santuário).
- **Fonte:** `state.json` (as_of dia 157, live). Conferir com `score tudo` ao conectar.

## 3. O que já foi descoberto
- **Rotina em Python:** `python automato/acoes/xadrez_cascata.py --etapa peoes|bispos|cavalos|torres|rainha|f1` e `--etapa rei --rei --idas N` (kite). Rastreia a casa A1 a H8, confere cada passo pelo texto da resposta (cor, frase da peça, saídas) e nunca passa por E8, E1, B1 e G1. **Só as partes puras foram testadas (13 testes); o fluxo ao vivo ainda não foi exercitado**: rodar `--etapa f1` e `--etapa peoes` primeiro, de olho no log.
- **Mapa:** 64 casas no `mapa.json` (`xadrez_A1` a `xadrez_H8`), gravadas por `scripts/mapear_tabuleiro.py`. `navegar.py --de templo_midgaard --para xadrez_F1` anda até F1 por F2 sem tocar G1.
- **Geometria** (colunas A a H de oeste a leste, fileiras 1 a 8 de sul a norte): H5 é a entrada (`w w w` do Campo); F1 Bispo Branco; fileira 8 preta: A8 Torre, B8 Cavalo, C8 Bispo, D8 Rainha (`!baixo`), E8 REI, F8 Bispo, G8 Cavalo, H8 Torre.
- **Cascata:** (1) peões (~8 a 9 mortes, ordem chega com atraso a F1); (2) bispos F8 e C8; (3) cavalos G8 e B8; (4) duas torres (empilham em A8; sono nas duas e raios em uma); (5) Rainha (curse + blind, 2 a 5 idas de 1 a 3 raios, recall a 150); (6) cetro. Respostas do Bispo no log (`Bispo Branco diz`).
- **Reaceitar:** Bispo Branco em F1: `say sim` ao convite e `say sim` a "Entendido?" (à mão, AGENTS #14).
- **Rei Negro:** Santuário, ~1.500+ de vida, acorda no primeiro raio, até 3 golpes mortais por rodada (54 a 72); `sleep` só pega fora de combate; `recall` funciona em combate; cada raio custa uma rodada dele; com 226 de vida uma rodada não mata (máximo ~216).
- **Peças brancas são do bem; o Rei Branco (E1) mata quem está na Xeque-mate.** Armadura da Torre Negra é amaldiçoada.
- **Despejo seguro:** nunca `Stop-Process` em todos os Python (há um `http.server` de outro projeto na porta 8768); parar só o `live_daemon`. Nunca dois clientes no mesmo driver.

## 4. Os bloqueios, e o que já foi tentado
- **Rei Negro:** Dia 156: sono + cegueira + maldição + raios, morreu em 2 rodadas. Charm: impossível (Santuário). Cetro do Bispo: recusado. Escolta: descartada pelo autor. Ainda não foi tentado o **kite** de verdade.
- **Posição incerta:** as reancoragens por `look` falharam duas vezes. Só a resposta do movimento vale.
- **Auditor:** as FALHAS de `auditar_sessao.py` deste dia (repetição de recusa por clientes simultâneos, alinhamento 455->402 por morte do Cavaleiro Branco, queda de 491 para 469 sem causa isolada) estão explicadas nos planos 037 e 038 e no conhecimento §68 a §71.

## 5. O próximo passo, e só ele
**Conectar** (`mandabala.py`; `cota_claude.py --registrar` com o `get_usage`; conferir que não há outro cliente no driver; subir o `live_daemon`), `score tudo` (conferir o §2), `python automato/camadas/prepara.py --forcar`, depois **testar o módulo ao vivo**: `python automato/acoes/xadrez_cascata.py --etapa f1` (vai a F1 por F2 e confere cada passo). Em F1, aceitar a Xeque-mate à mão e rodar as etapas em ordem (`peoes`, `bispos`, `cavalos`, `torres`, `rainha`), voltando a F1 a cada ordem (`--etapa f1`). Na etapa do cetro, `python automato/acoes/xadrez_cascata.py --etapa rei --rei --idas 3`: sleep, curse, blind, 1 raio, recall por ida; repetir até o Rei morrer, pegar o cetro à mão e entregar ao Bispo. Se o módulo falhar, ajustar o módulo (com teste) antes de jogar à mão.

## 6. NÃO REPITA
- Não esperar nem descansar em E1, E8, B1, G1 nem em qualquer casa da fileira 1 que não seja F1.
- Não confiar em `look` isolado para saber onde está; não escrever laços de jogo em PowerShell no scratchpad.
- Não encantar Rainha nem Rei; não tentar substituir o cetro; não fugir de D8 pela saída `baixo`.
- Não fechar a conexão com a missão ativa; não deixar outro agente no mesmo driver; não derrubar todos os Python.
- Não pegar a Armadura da Torre Negra nem atacar peças brancas.

## 7. Ferramentas e comandos
Python: `C:\Users\peter\AppData\Local\Programs\Python\Python312\python.exe`. Driver: `$env:MUD_DAY='157'; $env:MUD_WIMPY='45'; python automato\nucleo\driver\live_daemon.py` em segundo plano. Comando: `play.py "<cmd>"`; vários: `"n;cast 'sleep' rainha"`. Fechar: `play.py "_CLOSE sleep"`. Navegar: `automato\camadas\navegar.py`. Recarga: `prepara.py --forcar`. Ressuscitar: `acoes\ressuscitar.py`. Cota: `scripts\cota_claude.py`. Mapa do tabuleiro: `scripts\mapear_tabuleiro.py`. Cascata: `acoes\xadrez_cascata.py`.

## 8. Devolutiva técnica
| Descobri | Registrei em | O quê |
|---|---|---|
| mapa | `mapa.json` | as 64 casas `xadrez_A1` a `xadrez_H8` e o portão `medium`, por `scripts/mapear_tabuleiro.py`; falta confirmar ao vivo a saída oculta `baixo` de D8 e D1 |
| referência do servidor | `maquina/verificacoes.md` | PENDENTE neste plano: o "Herege! xeque-mate no rei errado" do Rei Branco e o look atrasado estão no conhecimento §71 |
| fato do mundo | `conhecimento.md` §71 | E1 mata na Xeque-mate; look atrasado; Rainha com curse; torres; ferramentas |
| erro do motor | `automato/CHANGELOG.md` | v1.7.7: `xadrez_cascata.py` e `mapear_tabuleiro.py`; falta exercitar o fluxo ao vivo |

## 9. Como encerrar a sua sessão
Siga `docs/agentes/PROTOCOLO.md` §3: `_CLOSE sleep` no Templo, evidência com `agent`, `python scripts/encerrar.py --agente "<modelo/versão>"`, preencher o plano 040, `python scripts/encerrar.py --agente "<modelo/versão>" --fechar --avanco sim|nao`.
