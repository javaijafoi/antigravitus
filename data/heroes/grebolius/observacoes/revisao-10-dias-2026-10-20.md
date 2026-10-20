# Revisão das sessões de 2026-10-10 a 2026-10-20 (Dias 155 a 158)

Agente: Claude Opus 5.5 (claude-opus-5-5). Pedido do autor: *"vc tem ignorado a forma melhor de jogar; revise os jogos dos últimos 10 dias e veja o que pode aprender"*.

**Fonte:** os 39 `automato/runtime/transcript_*.jsonl` do período (só há transcript de 16 a 20/10), `scripts/auditar_sessao.py` rodado em cada um, `docs/agentes/boletim.jsonl`, planos 027 a 040 e `conhecimento.md` §64 a §75. As contagens são de comandos do transcript. O transcript não diz se o comando veio de script ou de mão (limite da diretiva §23).

## 1. A forma melhor existe e quase não foi usada

O `automato/README.md` diz que o automato **é** a forma de jogar: `turno.py` → `vigia` → `cuidar` → `prepara` → rotina, com o vigia lendo o log a cada 60 s. A invariante 7 do README avisa: *conduzir a sessão à mão com `play.py` deixa a personagem sem vigia*.

- **`turno.py` e `trabalhar.py` não aparecem em nenhum plano de 027 a 040.** O log do turno (`automato/rotina.log`) foi gravado pela última vez em **16/10 às 15:10** (rotinas `cartografa` e `mercado`). De lá até 20/10, cerca de 80 mil comandos, **nenhuma rotina rodou supervisionada**. (O `config.LOG_ROTINA` aponta para `automato/runtime/rotina.log`, que não existe; o `turno.py` grava em `automato/rotina.log`. São dois caminhos para o mesmo log.)
- O jogo foi conduzido por `play.py`, comando a comando, por laços de PowerShell no scratchpad (`idas_*.ps1`, plano 038) e por ferramentas novas que duplicavam as existentes (`rotas/nav.py` × `camadas/navegar.py`, plano 033).

## 2. Os números por dia

| Dia (data) | Sessões | Comandos | Movimentos | `look` | `cast` | `consider` | "morrendo de fome" | "não pode ir" | Andou com vida < 60 |
|---|---|---|---|---|---|---|---|---|---|
| 16/10 | 9 | 47.150 | 18.005 | 11.667 | 1.569 | 334 | 321 | 790 | 25 |
| 17/10 | 7 | 60.749 | 25.505 | 15.081 | 2.760 | 66 | 42 | 915 | 0 |
| 18/10 | 6 | 7.728 | 3.117 | 1.673 | 463 | 27 | 67 | 65 | 4 |
| 19/10 | 9 | 3.251 | 1.722 | 364 | 297 | 8 | 13 | 120 | 7 |
| 20/10 | 8 | 6.758 | 1.801 | 2.514 | 589 | **1** | **100** | **9** | **37** |

Leitura:

- **O que funcionou:** recusas de movimento caíram de 915 para 9 quando a rota passou para o `mapa.json` e o andar para `navegar.py` e `xadrez_cascata.py`. A sessão de 19/10 15:03, toda por `nav.py`, teve 0 falhas e 0 avisos. Também deixou de haver `give` fora da etapa: foram 15+ falhas `give-sem-etapa` em 16 e 17/10 (as poções aquosas) e nenhuma depois das diretivas §19 a §21.
- **O que piorou em 20/10, depois de escrita a diretiva §23:** 1 `consider` em 589 magias (ataques ao bispo, peões e Rei sem `consider`); 37 movimentos com vida abaixo de 60 (mínimos de 3, 14 e 15 de vida); 100 linhas de "morrendo de fome" (a sessão de 15:06 teve 45 e terminou sem pão); `look` acima do número de movimentos, ou seja, a posição era conferida por `look` e não pela resposta do movimento.

## 3. As três mortes de 20/10 no tabuleiro tiveram a mesma raiz

| Morte (fonte) | O que aconteceu | Regra que já existia |
|---|---|---|
| 1ª (plano 038, "#10") | `charm person` na Rainha, numa sala com um Cavaleiro Negro extra; a fuga falhou ("PÂNICO!") com 48 de vida | diretiva §2: `consider` antes, não lutar com 2+ monstros sem sanctuary |
| 2ª (plano 039, "#12") | parada em E1 (Rei Branco) por um `look` atrasado | §9.3 e §23: andar por marco, conferir a chegada pela resposta |
| 3ª (conhecimento §73, "#13") | kite no Rei: ~25 raios necessários contra 2 por ida; morreu na ida 3 | README, "Método": **medir antes de acreditar** |

Cada morte cancelou a Xeque-mate e jogou fora uma cascata de ~1h30. Nas três, a tática nova foi testada **ao vivo e com a missão ativa**, sem antes medir o alvo (`consider`, vida, dano por rodada). O plano 040 chegou à conta certa ("o kite não fecha"), mas só depois da morte.

Divergência de registro: a numeração não fecha. O plano 039 diz "morreu 11 vezes" no §2 e "morte #12" no texto; o `state.json` e o plano 040 dizem 12 mortes; o `conhecimento.md` §73 chama a última de "morte #13". Conferir com `score` na próxima abertura e corrigir com nota datada.

## 4. O auditor avisou, e as falhas foram justificadas em vez de corrigidas

O `auditar_sessao.py` apontou em quase toda sessão `alinhamento-caiu`, `repeticao-de-recusa` e `recuo-a-pe`. Os planos 037 a 039 registraram essas falhas como "justificadas" e seguiram. A queda de 491 para 464/469 continua sem causa isolada. A §22 manda parar na hora e auditar a causa; não manda explicar no handoff.

## 5. Dinheiro

45.998 gastos em dois Cetros de Bispo que não serviam (o ouro foi de 72.078 para 33.438). Isso gerou a diretiva §25 (compra acima de 5% do ouro só com permissão).

## 6. O que aprendi

1. **XP, caça e ida e volta rodam por rotina e `turno.py`, não por `play.py`.** O plano 040 manda fazer um "mutirão de XP". Isso é `turno.py --rotina <caça> --turnos N` (`milharal_v2`, `novatos`), supervisionado, e não 1.000 comandos à mão. Se nenhuma rotina servir para a zona, escrever a rotina (contrato do README) antes de caçar.
2. **À mão só o que a diretiva manda fazer à mão:** fala de missão, `give`, compra e o primeiro mapeamento de uma área. Todo o resto vai por script com conferência por marco.
3. **Tática nova contra chefe primeiro se mede, e só depois se luta.** Com a missão inativa: `consider`, vida estimada, dano por rodada dele e o meu, regeneração entre visitas. Fazer a conta "raios necessários × raios por ida" **antes**. Só refazer uma cascata cara quando a conta fechar.
4. **`consider` antes de cada alvo novo** e **`recall` com vida < 100** (regra do autor, §72) valem também dentro do script: o script tem que fazer as duas coisas sozinho, senão elas não acontecem.
5. **Fome é sinal de que `prepara`/`cuidar` não está no laço.** Com o `turno.py` isso é automático. Sem ele, cada bloco começa com `prepara.py`.
6. **Falha do auditor se corrige na sessão seguinte**, com mudança de script ou de rotina, e não com parágrafo de justificativa no plano.

## 7. Propostas de catraca (para o autor aprovar; nenhuma implementada aqui)

Pelo §4 do `PROTOCOLO.md`, uma regra só vale com verificação em script, teste e ID no `catraca.json`. Candidatas:

- `auditar_sessao.py`: **FALHA** quando a sessão tem mais de N comandos de movimento e nenhum registro de `turno.py`/rotina (`rotina.log` ausente ou sem linha no horário da sessão).
- `auditar_sessao.py`: **FALHA** (hoje é AVISO) para `ataque-sem-consider` contra um alvo que ainda não teve `consider` na sessão.
- `devolutiva.py`: reprovar plano que marque uma FALHA do auditor como "justificada" sem citar a mudança de código que a evita.
- `xadrez_cascata.py`: `consider` automático no primeiro encontro com cada peça, e parar a ida **antes** do segundo raio com vida < 100 (o §73 já pede isso).
