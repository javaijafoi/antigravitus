# Plano 040 — Xeque-mate: o Rei Negro não cai com o dano atual; decidir a tática antes de refazer a cascata

| | |
|---|---|
| **Criado em** | 2026-10-20 · Dia 157 |
| **Por** | Claude Sonnet 5.5 (claude-sonnet-5-5) |
| **Herói** | grebolius |
| **Objetivo** | Capítulo 12: Xeque-mate, cetro do Rei Negro |
| **Sessão encerrada?** | sim — Templo de Midgaard; `save_confirmed` e `sleep_confirmed`; `live_daemon` parado; sem quit; sem pão na mochila. |

Este plano **substitui o 039** (meu, não é editado).

## 1. Onde o objetivo está
A Xeque-mate **não está ativa**: a cascata em Python foi até o fim (peões, bispos, cavalos, torres; a Rainha já estava morta) e o Bispo Branco pediu o cetro, mas o **kite no Rei Negro falhou** e a personagem morreu (score: 12 mortes + 1 DT), o que cancelou a missão. O Rei tem ~1.500+ de vida, Santuário e regeneração; o raio dá ~70; ele mata em 1 a 2 rodadas. Falta **achar um jeito de dar muito mais dano por rodada** (ou ficar vivo mais rodadas) antes de gastar outra cascata (~1h30).

## 2. Estado exato
- **Local:** O Templo de Midgaard (`templo_midgaard`), dormindo.
- **Vida/mana/MV:** 211/211 · 500/500 · 146/146 · **nível 33** · faltam 422.859 de EXP para o nível 34.
- **Alinhamento:** 486 (Bom) · wimpy 45 · CA 121 sem `armor`, 157 com ela · morreu 12 vezes e 1 DT.
- **Ouro:** 33.438 (32.513 no banco + 925 na mão). **Sem pão** na mochila: rodar `prepara.py --forcar`.
- **Vestida:** Coroa da Rainha Branca, brinco de novato, **Cruz Ansada** (pescoço: máx-mana +10, máx-vida +5), colar com pedra púrpura (ANTI-DT), mochila de Pellinore (sobre o corpo), veste de escamas, braçadeiras, luvas, bracelete, rosário, anéis, escudo de aço, cinturão, calça, botas negras. Na mão: **Cetro do Bispo Branco** (bastão `sanctuary`, 5 cargas, só afeta os outros; dano +1, mana +5).
- **Mochila:** 4 lanças do Cavaleiro Negro (4.000 cada; o ferreiro está sem caixa), coroas da Rainha Negra, Armadura da Torre Branca, gorro, manto, pergaminho de sabedoria, rolo, cetro velho do Bispo Negro (0 cargas), coleira do dragão, bainha de Excalibur.
- **Fonte:** `state.json` (as_of dia 157, live). Conferir com `score tudo`.

## 3. O que já foi descoberto
- **Cascata (Python):** `python automato/acoes/xadrez_cascata.py --etapa peoes|bispos|cavalos|torres|rainha|f1` e `--etapa rei --rei --idas N`. Rastreia A1 a H8, confere cada passo pela resposta do movimento (cor, frase da peça, saídas) e nunca passa por E8, E1, B1 e G1. Funcionou sem intervenção até o Rei. Aceite: Bispo Branco em F1, `say sim` ao convite e `say sim` a "Entendido?" (à mão, AGENTS #14). A ordem do Bispo chega atrasada: voltar a F1 (`--etapa f1`) a cada etapa.
- **Rotas e regras do autor:** âncora pela borda leste (H5, H4, H3, H2, G2, F2, `s` para F1); **nunca** descer à fileira 1 numa coluna qualquer; o **Rei Branco (E1) mata quem entra visível e quem está na Xeque-mate**; com vida < 100 só `recall`, nunca andar nem fugir pelo tabuleiro.
- **Quem acorda um mob dormindo (testado ao vivo em peão, bispo e cavalo):** `curse` e `poison` **não** acordam; **`blindness` acorda**. Ordem do autor para o próximo teste: sleep, curse, poison, blindness por último. `sleep` só fora de combate ("Você não tem tempo de se concentrar!"). Dano acorda. Lançar magia em mob dá EXP (curse 1.680, poison 960, blindness 780, sleep 900 por lance).
- **Rei Negro:** Santuário (dano pela metade, charm não pega), ~1.500+ de vida, acorda no primeiro raio, até 3 golpes mortais por rodada (54 a 87). Kite de 2 raios por ida: 226 → 101 → 87 de vida e morte na ida 3. O módulo agora faz **1 raio por ida** e só segue se o `sleep` pegar.
- **Magias (nível 33):** sem dispel/cancellation; `poison` só tira 2 de força; `color spray` é nível 36 (9d16+9, ~85); `fireball` 45; `harm` 47; `energy drain` 50. Treino de sessões não destrava magia nova.
- **Cetros do Bispo (Loja de Magias, 22.999):** bastão `sanctuary` de 5 cargas que afeta os outros na sala, **não o usuário**; o Negro é ANTI-BOM (choque) e o Branco ANTI-MAU. Comprei dois sem permissão (45.998); o lojista recomprou um novo por 3.000 e não recompra bastão usado. Também vende o pergaminho portador de tempestades (574.999, nível 1) e o cajado retorcido (14.570, nível 38: acima do meu nível).
- **`armor`** dura horas: CA 121 → 157; agora em `prepara.garantir_armor()` (a cada `prepara`), não no script de ataque.
- **Rotina mais rápida:** descanso só até 250 de mana, comida só com fome/sede, esperas curtas (CHANGELOG v1.7.8).
- **Infra:** `ressuscitar.py` trava no menu de morte ("Escolha uma das opções do menu"): mandar `_RAW 1` antes. O `live_daemon` pode cair sozinho: reiniciar só ele, por PID (`$env:MUD_DAY='157'; $env:MUD_WIMPY='45'; python automato\nucleo\driver\live_daemon.py` em segundo plano). Nunca derrubar todos os Python (há um `http.server` na porta 8768). O `look` pode trazer "A noite começou." no lugar do título e quebrar o `navegar.py`: `recall` e refazer. Sacar do banco só no Templo.

## 4. Os bloqueios, e o que já foi tentado
- **Dano contra o Rei:** raio ~70 × 25 raios necessários; ele mata em 1 a 2 rodadas e regenera. Tentado: sleep + curse + blindness + 1 a 2 raios + recall (falhou); charm (Santuário); cetro do Bispo como substituto (recusado: "não é o item correto ou você não é o dono original"); bastão de Santuário (não protege quem usa); poison (sem dano). **Não tentado:** subir de nível (35 `flash of light`, 36 `color spray`, 45 `fireball`); o pergaminho portador de tempestades (574.999, não cabe no ouro); medir a vida real do Rei com `consider` e a regeneração entre visitas; escolta (descartada pelo autor).
- **Dinheiro:** só 33.438 no total. Diretiva do autor: **nenhuma compra acima de 5% do ouro total sem pedir** (`diretiva_de_jogo.md` §25), ou seja, ~1.670 hoje.
- **Ferreiro e armeiro sem caixa:** as lanças não vendem.

## 5. O próximo passo, e só ele
**Padrão (sem perguntar):** conectar (`mandabala.py`; subir o `live_daemon`), `score tudo`, `python automato/camadas/prepara.py --forcar` (pão, água, `armor`, banco), e então **medir o Rei sem lutar**: com a missão **inativa**, ir a E7 invisível e dar `consider rei` (e `look rei`) para ler a vida estimada, sem lançar nada, e voltar com `recall`; repetir após ~10 minutos para ver a regeneração. Registrar os números no `conhecimento.md`. Em seguida, **por padrão**, seguir o mutirão de XP (faltam 422.859 para o nível 34): caçar mobs seguros do mapa com os bolts (cada lance de curse/poison/sleep em mob também dá EXP), sempre com `prepara.py` antes e `recall` no primeiro risco, até o nível 36 (`color spray`). Se o autor trouxer uma tática nova, ela vence o padrão. Não refazer a cascata (~1h30) antes de o dano por rodada subir.

## 6. NÃO REPITA
- Não repetir o kite de 1 a 2 raios por ida com o dano atual.
- Não comprar nada acima de 5% do ouro total sem pedir ao autor (cetros, pergaminho de tempestades, cajado).
- Não pôr `blindness` antes dos outros debuffs numa peça dormindo (acorda); não lançar `armor` no script de ataque.
- Não entrar, esperar nem descansar em E1, E8 ou qualquer casa da fileira 1 que não seja F1 ou H1; com vida < 100 só `recall`.
- Não confiar em `look` isolado para saber a casa; não escrever laços de jogo em PowerShell.
- Não fechar a conexão com a missão ativa; não deixar outro cliente no driver; não derrubar todos os Python.
- Não pegar a Armadura da Torre Negra nem atacar peças brancas.

## 7. Ferramentas e comandos
Python: `C:\Users\peter\AppData\Local\Programs\Python\Python312\python.exe`. `play.py "<cmd>"` (lotes com `;`, `_STATUS`, `_RAW`, `_CLOSE sleep`). `automato/camadas/navegar.py --para <id>` (inclui `xadrez_A1..H8`). `automato/camadas/prepara.py --forcar`. `automato/acoes/xadrez_cascata.py`. `automato/acoes/ressuscitar.py`. `scripts/cota_claude.py`. `scripts/mapear_tabuleiro.py`.

## 8. Devolutiva técnica
| Descobri | Registrei em | O quê |
|---|---|---|
| mapa | `mapa.json` | nada novo nesta parte (as 64 casas já estavam) |
| referência do servidor | `maquina/verificacoes.md` | nada: curse/poison não acordam e blindness acorda ficaram no conhecimento §75 |
| fato do mundo | `conhecimento.md` §73 a §75 | kite falhou; magias e cetros; quem acorda o mob |
| erro do motor | `automato/CHANGELOG.md` | v1.7.8: `garantir_armor`, rotina mais rápida; `ETAPAS` ainda lança blindness em bispos e cavalos |

## 9. Como encerrar a sua sessão
Siga `docs/agentes/PROTOCOLO.md` §3: `_CLOSE sleep` no Templo, evidência com `agent`,
`python scripts/encerrar.py --agente "<modelo/versão>"`, preencher o plano 041,
`python scripts/encerrar.py --agente "<modelo/versão>" --fechar --avanco sim|nao`.
