# Plano 038 — Xeque-mate: recomeçar a cascata e matar o Rei Negro com escudos enfeitiçados

| | |
|---|---|
| **Criado em** | 2026-10-20 · Dia 157 |
| **Por** | Claude Sonnet 5.5 (claude-sonnet-5-5) |
| **Herói** | grebolius |
| **Objetivo** | Capítulo 12: concluir a autoquest Xeque-mate (cetro do Rei Negro) |
| **Sessão encerrada?** | sim — Templo de Midgaard, dormindo; save e sleep confirmados; driver parado; sem quit. |

Este plano **substitui o 037** (o meu), que não é editado. A Xeque-mate foi refeita até a etapa do cetro e **cancelada pela morte #10** (Rainha Negra + um cavaleiro, fuga do wimpy falhou). Nível 33 alcançado e `charm person` treinado a 95%.

## 1. Onde o objetivo está
A missão **não está ativa** (morte cancela). É preciso recomeçar com o Bispo Branco em F1 e refazer a cascata numa única conexão (fechar a sessão também a derruba). A cascata leva ~1h30 com a rotina de idas curtas. A etapa final exige **matar o Rei Negro eu mesma**: o servidor recusa o Cetro do Bispo Negro ("não é o item correto ou você não é o dono original").

## 2. Estado exato
- **Local:** O Templo de Midgaard (`templo_midgaard`), dormindo.
- **Vida/mana/MV:** 226/226 · 490/490 · 146/146 · **nível 33** · EXP 8.023.660 (próximo nível em 9.000.000).
- **Alinhamento:** 491 (Bom) · wimpy 45 · CA 112 com tudo vestido, sem buffs · morreu 10 vezes e 1 DT.
- **Ouro:** 67.601 (67.301 banco + 300 mão).
- **Vestida:** Coroa da Rainha Branca, brinco de novato, coleira do dragão e colar com pedra púrpura (ANTI-DT), mochila de Pellinore (sobre o corpo), veste de escamas, braçadeiras, luvas, bracelete, rosário, anéis, escudo de aço, cinturão, calça, botas negras. Conferir `equipment` ao conectar (a morte desveste tudo).
- **Mochila** (vestida): Coroa da Rainha Negra, Armadura da Torre Branca, 4 Lanças do Cavaleiro Negro (4.000 cada), Cetro do Bispo Negro, um segundo colar púrpura, manto, gorro, rolo, pergaminho, bainha de Excalibur, Cruz Ansada. Carga 89/140 kg.
- **Fonte:** `state.json` (as_of dia 157, live). Conferir com `score tudo` ao conectar.

## 3. O que já foi descoberto
- **Rota ao tabuleiro:** `navegar.py --de templo_midgaard --para grande_campo_bifurcacao`, depois `w w w` = **H5**. Coordenadas e salas no conhecimento §69 (F1 Bispo Branco, D8 Rainha, E8 REI, A8 e H8 torres, B8 e G8 cavalos, C8 e F8 bispos). De F1 a D8: `n` x6, `w w`, `n`.
- **Cascata (cada etapa só vale com mortes depois da ordem do Bispo; ele fala com atraso quando você volta a F1):** (1) ~8 mortes de peões (há 40+ acumulados, não são "todos"); (2) bispos F8 e C8: cegueira + maldição + 4 raios; (3) cavalos G8 e B8: igual; (4) duas torres (empilham em A8, 2 a 4): dormir as duas (`cast 'sleep' 1.torre`, depois `2.torre`) e só raios na 1.torre, sem blindness/curse; (5) Rainha em D8: sono ao entrar (`n;cast 'sleep' rainha`), cegueira, 1 a 3 raios e recall quando a vida cair abaixo de 150 (cada rodada dela chega a 94); 5 idas; (6) cetro do Rei.
- **`charm person` (95%):** funciona em alvo de nível <= 33 (Cavaleiro Negro e Bispo Negro viraram seguidores); a **Rainha Negra não encanta** (nível maior). O Rei Negro provavelmente também não: conferir com `consider rei` na entrada (se disser que é de nível superior, não tentar). Seguidores servem de escudo: `order <seguidor> kill rei`; um mob que já luta com a minha peça não troca de alvo.
- **Rei Negro:** Santuário, ~1.500+ de vida, acorda no primeiro raio, até 3 golpes mortais por rodada (54 a 72). Cada raio meu custa uma rodada dele. O `sleep` só pega antes da luta.
- **`prepara.py --forcar`** deposita ouro e troca equipamento pela Sala de Doações; rode antes de sair. Vale também para comprar pães e encher cantil.
- **Armadura da Torre Negra** é amaldiçoada (proibida). **Armeiro e Ferreiro estão sem caixa** (armadura, coroa e lanças): vender depois.
- **Peças brancas são do bem:** nunca atacar (Cavaleiro Branco ataca quem entra visível; usar invisibilidade e `flee`).

## 4. Os bloqueios, e o que já foi tentado
- **Rei Negro:** (1) Dia 156: sono + cegueira + maldição + raios, morreu em 2 rodadas. (2) Hoje: só entrei por engano. (3) Trocar o cetro do Bispo: recusado pelo servidor. (4) Encantar a Rainha para usar de escudo: falhou (nível maior) e custou a morte.
- **Morte #10:** Rainha + um Cavaleiro Negro extra em D8, sangramento e fuga falhando ("PÂNICO! Você não pode escapar!") com 48 de vida. Causa raiz: tentei o encanto numa sala com vários monstros sem verificar o nível antes.
- **Auditor:** as FALHAS de `auditar_sessao.py` desta sessão (alinhamento 455->402 por morte do Cavaleiro Branco, repetição de recusa por conexões simultâneas) estão justificadas no plano 037 §4.

## 5. O próximo passo, e só ele
**Antes de conectar:** `python scripts/mandabala.py`, `python scripts/cota_claude.py --registrar ...` com o `get_usage`, e confira que não há outro cliente no driver. **Conectar, `score tudo` (conferir o §2), `python automato/camadas/prepara.py --forcar`** e então **recomeçar a cascata** pela rotina de idas curtas: Bispo Branco em F1 (`say sim` x2), peões, bispos, cavalos, torres (dormindo as duas), Rainha (idas de 1 a 3 raios), chegando ao cetro numa só conexão. Para o Rei, em E8 (nunca entrar sem plano): `consider rei`; se ele for de nível superior, não tente encantá-lo. A ação padrão é a **escolta**: antes de entrar em E8 encante 3 a 4 seguidores (cavalo, bispo, torre), entre com o Rei dormindo (`n;cast 'sleep' rei`), mande `order all kill rei` e só então atire, com recall a 150 de vida. Se algum seguidor não encantar, registre o nível e siga com os que encantaram; sem seguidores, não entre em E8 e deixe tudo pronto no plano 039.

## 6. NÃO REPITA
- Não lançar `charm person` em sala com vários monstros nem sem `consider` antes; a Rainha não encanta.
- Não fugir de D8 pela saída `baixo` (tesouraria) nem contar com o wimpy: recall a 150 de vida, e só com a vida alta.
- Não fechar a conexão com a missão ativa; não deixar outro agente no mesmo driver.
- Não pegar a Armadura da Torre Negra; não atacar peças brancas; não insistir na Ajuda Mágica.
- Não gastar raios em peões além do necessário; evitar `rest` sem `stand` depois.

## 7. Ferramentas e comandos
Python: `C:\Users\peter\AppData\Local\Programs\Python\Python312\python.exe`. Driver: `$env:MUD_DAY='157'; $env:MUD_WIMPY='45'; python automato\nucleo\driver\live_daemon.py` em segundo plano. Comando: `python automato\nucleo\driver\play.py "<cmd>"`; vários: `"n;cast 'sleep' rainha"`. Fechar: `play.py "_CLOSE sleep"`. Navegar: `automato\camadas\navegar.py`. Recarga: `automato\camadas\prepara.py --forcar`. Ressuscitar: `automato\acoes\ressuscitar.py`. Cota: `scripts\cota_claude.py` (registrar com o `get_usage`). Localizar mobs: `where N.nome` (ex.: `where 3.peao`). Se o socket cair, reiniciar o daemon retoma a personagem com a missão.

## 8. Devolutiva técnica
| Descobri | Registrei em | O quê |
|---|---|---|
| mapa | `mapa.json` | PENDENTE: casas do tabuleiro e a saída `baixo` de D8 (tesouraria) ainda não estão no mapa; geometria no conhecimento §69 e §70 |
| referência do servidor | `maquina/verificacoes.md` | cetro com dono original, charm person (nível <= 33), equipamento fica no inventário após a morte, aspas não valem em nomes, lojas sem caixa |
| fato do mundo | `conhecimento.md` §70 | cascata em detalhes, torres empilhadas, Rainha e Rei, morte #10, Keen no D8 |
| erro do motor | `automato/CHANGELOG.md` | nada alterado; a rotina `idas_*.ps1` ficou fora do repositório (scratchpad) |

## 9. Como encerrar a sua sessão
Siga `docs/agentes/PROTOCOLO.md` §3: `_CLOSE sleep` no Templo, evidência com `agent`, `python scripts/encerrar.py --agente "<modelo/versão>"`, preencher o plano 039, `python scripts/encerrar.py --agente "<modelo/versão>" --fechar --avanco sim|nao`.
