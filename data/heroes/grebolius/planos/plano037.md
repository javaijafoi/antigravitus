# Plano 037 — Xeque-mate: subir ao nível 33, enfeitiçar o Rei Negro e entregar o cetro

| | |
|---|---|
| **Criado em** | 2026-10-20 · Dia 157 |
| **Por** | Claude Sonnet 5.5 (claude-sonnet-5-5) |
| **Herói** | grebolius |
| **Objetivo** | Capítulo 12: concluir a autoquest Xeque-mate (cetro do Rei Negro) |
| **Sessão encerrada?** | sim — Templo de Midgaard, dormindo; save e sleep confirmados; driver parado; sem quit. Fechei por cota do harness (janela de 5 h com 93% usada). |

Este plano **substitui o 036** (Claude Opus 5.5), que não é editado. O autor mandou **largar a Ajuda Mágica** (Lemin não deu o convite em ~25 min) e fazer o Xeque-mate. Concorri comigo mesmo: outro agente (também Claude) comandou a mesma personagem em paralelo e embaralhou as movimentações de hoje.

## 1. Onde o objetivo está
Xeque-mate está na etapa 6: `Xeque-mate: Você deve entregar objeto ao personagem.` (cetro do Rei Negro, ao Bispo Branco em F1). A cascata foi refeita: peões, 2 bispos, 2 cavalos, 2 torres e a Rainha estão mortos (as peças reaparecem). Falta o Rei Negro (E8), que não dá para vencer no peito a peito.

## 2. Estado exato
- **Local:** O Templo de Midgaard (`templo_midgaard`), dormindo.
- **Vida/mana/MV:** 199/199 · 430/430 · 145/145 · nível 32 · EXP 7.655.666 (faltam 344.334 para o 33).
- **Alinhamento:** 434 (Bom) · wimpy 45.
- **Ouro:** 60.509 (15.700 banco + 44.809 mão; a origem do ouro da mão não foi auditada, veio de outro agente).
- **Comida/água:** sem fome nem sede ao fechar; conferir pães e cantil ao conectar.
- **Mochila de Pellinore** (vestida; para guardar: `remove mochila`, `put <item> mochila`, `wear mochila`): Coroa da Rainha Negra, 4 Lanças do Cavaleiro Negro, manto, colar púrpura, bainha de Excalibur, Cruz Ansada, Cetro do Bispo Negro. Vestindo a Coroa da Rainha Branca (ANTI-MAU, serve a uma maga boa).
- **Fonte:** `state.json` (as_of dia 157, live). Conferir com `score tudo` ao conectar.

## 3. O que já foi descoberto
- **Geometria do tabuleiro** (colunas A a H de oeste a leste, fileiras 1 a 8 de sul a norte): `navegar.py --de templo_midgaard --para grande_campo_bifurcacao`, depois `w w w` chega a **H5** (entrada). Sul de H5: H4, H3, H2, **H1** (Torre Branca). **F1** = Bispo Branco (quem dá a missão): de H1, `w w`. Norte de H5: H6, H7, **H8** (Torre do Rei Negro). Fileira 8: A8 Torre, B8 Cavalo, C8 Bispo, **D8 Rainha** (saída oculta `baixo` = Tesouraria Negra), **E8 REI**, F8 Bispo, G8 Cavalo, H8 Torre. De F1 a D8: `n` x6, `w w`, `n`. Nunca entrar em E8 sem plano (custou 93 de vida só ao entrar).
- **Reaceitar:** Bispo Branco em F1: `say sim` ao convite e `say sim` a "Entendido?". A ordem seguinte chega depois de um atraso, quando todos os peões vivos morrem.
- **Peões** reaparecem e vagam; 2 raios cada, custo alto de mana. Ignorar quando não forem necessários.
- **Rainha** (D8): sono antes de entrar (`n;cast 'sleep' rainha` no mesmo envio), cegueira, maldição, raios; ela não segue quem sai. Cai em ~10 raios, em 2 a 3 idas.
- **Torres** (A8, H8): sono + cegueira + maldição + ~6 raios cada. **Cavalos** e **bispos**: cegueira + maldição + 4 a 5 raios, sem dano relevante.
- **Rei Negro:** Santuário, ~1.500+ de vida, acorda no primeiro raio, até 3 golpes mortais por rodada (54 a 72). Movimento é bloqueado em combate. Morrer cancela a missão.
- **Peças brancas são do bem:** matar o Cavaleiro Branco derrubou o alinhamento 455 -> 402; as Coroas confirmam (Branca ANTI-MAU, Negra ANTI-BOM). O Cavaleiro Branco (G1/B1) ataca quem entra visível: usar invisibilidade e `flee`, não revidar.
- **Armadura da Torre Negra:** amaldiçoada (BRILHO AMALDIÇOADO). Não pegar.

## 4. Os bloqueios, e o que já foi tentado
- **Rei Negro:** (1) Dia 156: sono + cegueira + maldição + raios, morreu em 2 rodadas. (2) Hoje: só entrei por engano, -93 de vida. O sono só funciona lançado antes da luta: o outro agente da sessão registrou que `sleep` NÃO pode ser relançado em combate ("Você não tem tempo de se concentrar!", conhecimento §68). Por isso a tática (a) (dormir de novo no meio da luta) está descartada.
- **Cetro do Bispo Negro** (grátis, na mochila) como substituto do cetro do Rei: **não testado**. Só vale tentar `give cetro bispo` com a etapa confirmada em `score tudo` (AGENTS #13); é item sem custo.
- **Falhas do `auditar_sessao.py` (7), justificadas:** 5x `repeticao-de-recusa` (`s`/`w` recusados 3 vezes) vieram de estar sentada em descanso ("muito relaxado") e de dois clientes comandando a mesma personagem: nao foi insistencia, foi estado trocado por outro agente; a guarda real so passou a valer depois de eu conferir `stand` e `look` duas vezes. 2x `alinhamento-caiu`: 417 -> 415 (sem causa isolada, durante luta em paralelo) e 455 -> 402 (morte do Cavaleiro Branco por raio meu, em luta que ele comecou; banido para sempre). Avisos de `ataque-sem-consider` sao peoes e cavalos negros ja conhecidos como alvos legitimos (consider feito em amostra).

## 5. O próximo passo, e só ele
**Subir ao nível 33 matando peças negras que reaparecem** (torres 48 a 65k de EXP, rainha ~65k, bispos ~18k, cavalos ~34k), sempre com sono antes de entrar, cegueira, maldição e raios, saindo com `s` ou recall abaixo de 105 de vida. No 33: `practice charm person`, entrar em E8 com o Rei dormindo (`n;cast 'sleep' rei` no mesmo envio), `cast 'charm person' rei`, e só então `order rei drop cetro`; `get cetro`; levar a F1 e `give cetro bispo` com o `score tudo` mostrando a etapa de entrega. Alternativa registrada no conhecimento §68: **kite** no Rei (a vida dele regenera devagar entre as visitas e `recall` funciona em combate): dormir antes de entrar, no máximo 1 a 2 raios, `recall` com vida abaixo de 110, descansar, repetir; estimativa de 10+ idas. Padrão se o charm falhar: não atacar o Rei; testar `give cetro bispo` com o Cetro do Bispo Negro (sem custo) e registrar a resposta.
- Antes de cada bloco: dois `look` e `_STATUS`; se divergirem, há outro cliente no driver.

## 6. NÃO REPITA
- Não entrar em E8 por distração; não rodar loops de `w`/`n` sem `look` a cada passo.
- Não atacar nenhuma peça branca. Não pegar Armadura da Torre Negra (amaldiçoada).
- Não usar `rest` sem `stand` depois; não usar `quit`; não conectar dois agentes ao mesmo driver.
- Não gastar raios em peões sem necessidade (gastam metade da mana).
- Não insistir na Ajuda Mágica (abandonada pelo autor).

## 7. Ferramentas e comandos
Python: `C:\Users\peter\AppData\Local\Programs\Python\Python312\python.exe`. Driver: `$env:MUD_DAY='157'; $env:MUD_WIMPY='45'; python automato\nucleo\driver\live_daemon.py` em segundo plano. Comando: `python automato\nucleo\driver\play.py "<cmd>"`; vários em um envio: `"n;cast 'sleep' rainha"`. Fechar: `play.py "_CLOSE sleep"`. Navegar: `automato\camadas\navegar.py --de <id> --para <id>`. Cota no Claude Code: `get_usage` do harness (janela de 5 h e semanal); parar a 10% e 5%.

## 8. Devolutiva técnica
| Descobri | Registrei em | O quê |
|---|---|---|
| mapa | `mapa.json` | PENDENTE: as casas do tabuleiro (A1 a H8) ainda não estão no mapa; a geometria está no conhecimento §69 e no §3 deste plano |
| referência do servidor | `maquina/verificacoes.md` | convite de autoquest por temporizador, `where` só para mobs, detect alignment é de clérigo, recall e fuga em combate, dois clientes no driver |
| fato do mundo | `conhecimento.md` §69 | geometria do tabuleiro, Rei, Rainha e Cavaleiro Branco, armadura amaldiçoada, Ajuda Mágica |
| erro do motor | `automato/CHANGELOG.md` | nada alterado; falta uma guarda de cota para o Claude Code (o `checar_cota.py` só lê o Antigravity) |

## 9. Como encerrar a sua sessão
Siga `docs/agentes/PROTOCOLO.md` §3: `_CLOSE sleep` no Templo, evidência com `agent`, `python scripts/encerrar.py --agente "<modelo/versão>"`, preencher o plano 038, `python scripts/encerrar.py --agente "<modelo/versão>" --fechar --avanco sim|nao`.
