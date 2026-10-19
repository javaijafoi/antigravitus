# Controle de versão do automato

Versionamento semântico adaptado a um jogo: **MAIOR** muda o contrato das rotinas,
**MENOR** acrescenta camada/rotina, **CORREÇÃO** conserta comportamento.
As datas usam o **dia de jogo**.

## v1.7.1 — Dia 157 · Quarentena dos scripts que falam/entregam por conta própria (Claude Opus 5.5)
- **`automato/acoes/_proibidos/` (nova):** os oito scripts que automatizam `say`/`ask`/`give`/`buy` de missão (`falar_fazendeiro`, `encontrar_fazendeiro`, `falar_minerador`, `iniciar_gargamel`, `ativar_gargamel`, `interagir_alquimista`, `entregar_alquimista`, `comprar_pocao`) foram movidos para lá com `git mv`. Cada um ganhou na primeira linha `raise SystemExit('PROIBIDO …')`. Fecha o "próximo desafio" da DECISOES §10. `LEIA.md` na pasta explica.
- **`scripts/check_project.py` — `validate_forbidden_imports`:** **ERRO** (`automato.import_proibido`) se qualquer `.py` de `automato/` ou `scripts/` fora da pasta mencionar `_proibidos` em código (import, sys.path, runpy, subprocess). Comentários não contam.
- **Catraca:** `automato.import_proibido` e a trava dos scripts entram em `docs/agentes/catraca.json`. Cinco testes novos em `test_catraca.py` (suíte: 204 OK).
- **Custo:** evidências antigas (`dia156l/m/o.json`) citam os caminhos antigos em `automato/acoes/`. Ficaram intactas (legado), e o `LEIA.md` da pasta registra a mudança.

## v1.7.0 — Dia 157 · Um padrão para todos os modelos: protocolo, encerramento e catraca (Claude Opus 5.5)
- **`docs/agentes/PROTOCOLO.md` (novo):** a sessão inteira em comandos — abertura, cada bloco de jogo, encerramento/handoff. O AGENTS.md ganhou um quadro "Comece aqui" que aponta para ele; `CLAUDE.md` e `GEMINI.md` (novos) levam cada harness à mesma porta.
- **`scripts/mandabala.py`:** imprime a SEQUÊNCIA DE ABERTURA e a primeira ação (o §5 do plano); avisa quando o plano não é autossuficiente ou devolve o próximo passo ao autor (`checar_plano_v2`); a ordem de leitura caiu de ~2.100 linhas para o PROTOCOLO + plano + AGENTS §4 + diretiva §19–§23.
- **`scripts/encerrar.py` (novo):** handoff em duas etapas. Sem `--fechar`: confere o `_CLOSE sleep` no transcript, roda sync/check/auditor e gera o esqueleto do próximo plano com §2 tirado do `state.json`. Com `--fechar --avanco sim|nao`: plano v2, `devolutiva.py` e uma linha no `docs/agentes/boletim.jsonl`.
- **`scripts/devolutiva.py`:** regras do plano v2 viram FALHA a partir do plano 034 (`PLANO_V2_DESDE`); mensagens ganharam IDs da catraca.
- **Catraca:** `docs/agentes/catraca.json` + `scripts/test_catraca.py` — nenhuma verificação some sem decisão registrada (DECISOES §13).
- **`automato/README.md` — tabela "Ferramentas — uma por função":** cada script como canônico/legado/pontual/PROIBIDO. `navegar.py` é a navegação canônica; `rotas/nav.py` fica como legado. Oito scripts de `acoes/` que automatizam `say`/`ask`/`give`/`buy` de missão ficam marcados PROIBIDOS (AGENTS #13/#14), sem apagar. `check_project.py` avisa sobre script fora da tabela (`validate_tool_registry`).
- **Testes:** `test_plano_v2.py`, `test_encerrar.py`, `test_catraca.py` (suíte: 199 OK).
- **Custo:** mais um comando no fim da sessão; planos mais longos (copiam em vez de remeter).

## v1.6.17 — Dia 157 · Navegador por mapa e auditor de sessão (Claude Sonnet 5.5)
- **`camadas/navegar.py` (novo):** leva a personagem de uma sala a outra pelo `mapa.json`, conferindo o nome de cada sala. Só envia direções, `look` e `exits`; nunca fala, entrega, compra, pega nem ataca. Para em combate, vida baixa, recusa, porta fechada, sala inesperada ou teto de passos/tempo (códigos 3 a 6). Recusa rotas por sala `danger`/`high`/`fatal`/`critical` sem `--permitir-risco`. `--seco` imprime o caminho sem conectar; `--listar` procura salas.
- **`scripts/auditar_sessao.py` (novo):** audita um `transcript_*.jsonl` contra regra escrita: recusa repetida, `quit`, `give` sem etapa, fala em lote ou rajada, ataque sem `consider`, `get` sem `identify`/`get all`, compra cara, alinhamento em queda, recuo a pé com vida baixa, sessão sem fecho. Não consegue auditar §9/§14 (origem do comando não é registrada).
- **Testes:** `scripts/test_auditar_sessao.py` (20 testes, sem conexão com o MUD).
- **Diretiva de jogo §23:** ritual de quatro perguntas antes de cada bloco de jogo.
- **Custo:** o navegador confia no `mapa.json`; rota derivada do levantamento pode ter aresta falsa (a conferência de título pega e para). O auditor tem falsos positivos possíveis (AVISO pede explicação, não é veredito).

## v1.6.16 — Dia 156 · Venda da Coroa da Rainha Negra, Recomposição de Estoque e Geografia de Autoquests (Plano 026)
- **EXECUÇÃO DO PLANO 026 (Capítulo 12 / Tomo II)**:
  - Cotação (`value coroa`) e venda bem-sucedida da `Coroa da Rainha Negra` no Armeiro de Midgaard por 1.500 moedas de ouro, aliviando 4 kg de peso morto e eliminando riscos da flag ANTI-GOOD sem jamais vesti-la.
  - Depósito de 1.700 moedas no Banco do Templo, elevando a reserva bancária para 15.700 moedas (patrimônio total: 16.059 moedas de ouro, mantendo 359 moedas líquidas na mão).
  - Recomposição do estoque na Padaria de Midgaard: compra de 5 pães recheados por 30 moedas e armazenamento na mochila de Pellinore (estoque restabelecido para 6 pães, atendendo a regra `LIMIAR_PAO = 2`).
  - Abastecimento completo do cantil com água cristalina na grande fonte da Praça do Templo.
- **DESCOBERTA DOCUMENTAL DE AUTOQUESTS**:
  - Auditoria in-game de `help autoquest` e `help notre dame` comprovou que o patrono `Lemin` da autoquest `Ajuda Mágica` localiza-se na zona de **Notre Dame/França** (e não em Midgaard).
  - Rota terrestre completa até a França e Notre Dame extraída e documentada em `conhecimento.md` §60.

## v1.6.15 — Dia 156 · Validação Tática de Sleep/Blindness em Chefes e Cotação Mercantil (Capítulo 11)
- **TÁTICA ARCANA EM COMBATE DE ELITE**:
  - Validação empírica de `cast 'sleep'` em monstros de grande porte e estruturas blindadas (Torre Negra, Rainha Negra), comprovando que o adormecimento impede retaliação e permite preparação tática.
  - Validação de `cast 'blindness'` contra alvos com múltiplos ataques por round (Rainha Negra): a penalidade severa (-4 hitroll, -40 AC) fez com que a oponente errasse mais de 80% dos golpes, viabilizando bombardeio de raios arcanos.
- **COMÉRCIO E IDENTIFICAÇÃO**:
  - Validação do comando `value <item>` com o Armeiro de Midgaard para cotação formal de revenda antes de transacionar.
  - Venda de armadura limpa por 8.500 moedas e catalogação da Coroa da Rainha Negra (ANTI-GOOD, não NODROP, valor 3.000 moedas).

## v1.6.14 — Dia 156 · Incorporação da Bateria de Testes de Mecânicas Inéditas ao Capítulo 11 (Plano 025)
- **DIRETIVA DO AUTOR (Diretiva de Jogo §23 / Plano 025)**:
  - Integração mandatória de bateria de testes de mecânicas e comandos inéditos de CircleMUD/DeBo ao ciclo do Capítulo 11 (Tomo II — As Chaves do Tabuleiro).
  - Escopo de testes mapeado e dividido em 4 fases: Percepção Arcana (`detect alignment`, `detect invisibility`, `sense life`, `locate object`), Sobrevivência (`sip`, `taste`, `pour`, `diagnose`, `track`), Economia/Logística (`cashcard` como banco portátil no Empório, `donate <item>`, `junk <item>`) e Comunicação (`check`, `receive`, `mail` nos Correios 3062 e leitura em murais públicos).
  - Execução integrada como apoio preparatório e ferramental tático antes e durante as autoquests `Xeque-mate` e `Ajuda Mágica`.

## v1.6.13 — Dia 156 · Monitoramento de Weekly Limit (< 5%) e Janela Curta (< 10%) na Guarda de Cota
- **DIRETIVA DO AUTOR (AGENTS.md §13 / Guarda de Cota)**:
  - Adicionado monitoramento do **weekly limit** do modelo: se o tempo de reset for superior a 24 horas (como a janela semanal do Gemini de ~129h), o corte crítico de segurança é acionado ao atingir **<= 5%** (`0.05`).
  - Para limites diários / janelas curtas (reset <= 24h), mantém-se o corte crítico em **<= 10%** (`0.10`).
  - Em ambos os casos de corte, executa-se o mesmo protocolo rigoroso: retorno ao Templo por `recall`, alimentação com pão, hidratação com água do cantil, salvamento (`save`), sono (`sleep`), fechamento limpo de socket e geração do plano de handoff numerado documentando o motivo e tempo até o reset.
- **MOTOR (`automato/camadas/guarda_cota.py`)**:
  - Implementada função `consultar_detalhes_cota(modelo_alvo)` com extração precisa de `horas_restantes`, `is_weekly`, `tipo` ("semanal" vs "diario"), `threshold` (0.05 vs 0.10) e `reset_formatado`.
  - **ISOLAMENTO ESTRITO DO MODELO ATIVO**: Removido qualquer fallback para outros modelos em `consultar_detalhes_cota()`. O automato monitora única e exclusivamente o modelo que está rodando a sessão (`gemini-3.8-flash` por padrão ou via `MUD_MODEL`/`ANTIGRAVITY_MODEL`). Se a cota de outro modelo (ex.: Argon em 0.6%) estiver esgotada, ela é 100% ignorada e jamais interrompe a execução.
  - Função `intervalo_recomendado` adaptada para janelas semanais (35 min para >20%, 15 min para >10%, 5 min para >6%, 1 min para <=6%).
- **CLI (`scripts/checar_cota.py`)**:
  - Exibição de colunas `Tipo` (Semanal/Diário), `Corte` (5%/10%), `Reseta Em` e `Status` (OK/ATENÇÃO/CRÍTICO).
- **TESTES**: Suíte `scripts/test_guarda_cota.py` com 7 testes unitários validando thresholds, intervalos, handoffs e garantia de isolamento do modelo ativo contra falsos positivos (148 testes OK no projeto).

## v1.6.12 — Dia 156 · Postura Heroica Proativa e Dever de Questionar o Autor (AGENTS.md Invariante 15)
- **DIRETIVA DO AUTOR (AGENTS.md Invariante 15 / Diretiva de Jogo §22)**:
  - Reorientação doutrinária fundamental: a conduta moral de Grebolius é **proativa e heroica**, não apenas reativa.
  - O agente deve enxergar o mundo com empatia (ver um cachorro como um animalzinho inocente e indefeso, e não como alvo/número). Não fazer o mal, não bater em pessoas pacíficas, não machucar animais indefesos. Nunca matar para descobrir se era pecado.
  - **Dever de questionar o autor:** Se o próprio autor Peter emitir ordem para bater em pessoas inocentes ou machucar animais indefesos, o agente tem o dever expresso de questioná-lo antes de executar.
  - O monitoramento do compass `{<<<<<>----}` atua como *double check* de segurança.

## v1.6.11 — Dia 156 · Preservação de Moral e Alinhamento (AGENTS.md Invariante 15)
- **DIRETIVA DO AUTOR (AGENTS.md Invariante 15 / Diretiva de Jogo §22)**:
  - Estabelecida a regra mandatória de preservação de alinhamento moral: qualquer ação ou abate que reduza a moral de Grebolius (compass `{<<<<<>----}` e valor numérico no `score` / `score tudo`) exige parada imediata da sessão, auditoria de causa raiz no log e proibição permanente de reincidência.
  - Banido em definitivo o abate de animais domésticos da Pet Shop (gatinhos, cachorrinhos, beagles, rottweilers) e criaturas inocentes.
- **PARSER**: Adicionada função pura `parse_alignment(text)` em `automato/nucleo/driver/parsers.py` para extração determinística do valor numérico, representação visual do compass e descrição textual do alinhamento a partir de saídas de `score`.

## v1.6.10 — Dia 156 · Dupla checagem com identify no chão e liberação de itens limpos da Torre Negra
- **DIRETIVA DO AUTOR (AGENTS.md Invariante 10 / Diretiva de Jogo §15)**:
  - Esclarecido que itens da Torre Negra **NÃO** são categoricamente proibidos: proibidos são apenas itens **amaldiçoados** (com flag `ITEM_NODROP` / maldição), que prendem ao inventário e causam prejuízo. Itens limpos (inclusive da Torre Negra) são permitidos.
  - Implementada inspeção obrigatória no chão com `identify armadura` antes de executar `get` em armaduras da Torre Negra em `automato/rotinas/xadrez_v3.py`.
  - Se identificada maldição ou NO-DROP, o item permanece no chão e nunca entra no inventário.

## v1.6.9 — Dia 156 · Otimização de Performance dos Scripts de Caça (>10% a >30% speedup)
- **OTIMIZAÇÃO (novatos.py, >30% mais rápido)**:
  - Eliminado `consider` redundante em mobs de nível 1 a 4 para Grebolius (nível 31), economizando 1 round-trip de rede por mob.
  - Saque unificado com `get all corpo` (e saque cirúrgico no minotauro) em vez de 5 comandos `get` individuais por corpo.
  - Empacotamento em lote (`organizar_espolios`): substituídos os 6 comandos por mob (guarda e checagem contínua de inventário) por uma única triagem ao término da masmorra.
  - Roteamento inteligente de venda (`vender_espolios`): se nenhum equipamento vendável foi obtido no percurso, o robô pula integralmente as caminhadas até o Armeiro e Ferreiro, economizando ~12 segundos.
- **OTIMIZAÇÃO (xadrez_v3.py, >20% mais rápido)**:
  - Removido `consider peao` redundante antes de cada peão.
  - Saque unificado com `get all corpo`.
  - Corrigida coleta de chão: removidas chamadas desnecessárias a corpos inexistentes ao pegar armaduras/escudos do piso.
- **OTIMIZAÇÃO (milharal_v2.py, >10% mais rápido)**:
  - Removida checagem duplicada de término de combate em `matar()`.
- **OTIMIZAÇÃO (cacador_hibrido.py, >15% mais rápido)**:
  - Reduzido o intervalo de sondagem de mana durante o sono de 8s para 4s em `descansar_ate_mana_cheia()`, capturando o tick de regeneração sem tempo ocioso excessivo (~36s economizados em 3 ciclos).
  - Eliminada chamada duplicada a `score tudo` em `ouro_atual()`.

## v1.6.8 — Dia 156 · validação estrita de sub-etapa de autoquest e treino de sleep (AGENTS.md Invariante 13)
- **DOUTRINA / CONTRATO**: Reforçada a Invariante 13 em `AGENTS.md` e criada a Seção 21 em `diretiva_de_jogo.md`: "Estar na etapa certa para fazer a coisa certa". Nenhuma entrega (`give`) ou compra cara de missão pode ser realizada se o `score tudo` não explicitar textualmente a instrução da sub-etapa (ex.: `Você deve entregar objeto ao personagem`).
- **RESOLUÇÃO DE MISSÃO**: Descoberta a causa do consumo incorreto da poção aquosa (Smurf Minerador não havia concluído o envio oral e Alquimista não havia ativado o pedido do jarro). Diálogo completo executado manualmente em tempo real, destravando oficialmente a máquina de estados no servidor (`Uma Lição em Gargamel: Você deve entregar objeto ao personagem.`).
- **MAGIA / EVOLUÇÃO**: Descoberta da sala da Mestre da Guilda dos Magos em *O Laboratório dos Magos* (`e` do Bar dos Magos) e treino integral da magia do Nível 31 (`sleep`) de 10% para 95% (perfeito).

## v1.6.7 — Dia 156 · guarda de cota inteligente e handoff automatizado (AGENTS.md §13)
- **NOVO**: `automato/camadas/guarda_cota.py` — módulo de monitoramento adaptativo da cota de IA via endpoint Connect RPC local (`GetUserStatus`). Consulta com frequência inteligente (a cada 35 min se cota > 40%; a cada 10-15 min se entre 20%-40%; a cada 1-5 min se próxima do corte), evitando overhead desnecessário de chamadas.
- **NOVO**: Protocolo de handoff automático: quando a cota atinge <= 10% (tolerância 5%-10%), aciona parada de caça, retorno seguro ao Templo, alimentação, hidratação, `save`, `sleep`, encerramento limpo da conexão e geração automática do próximo plano numerado de handoff.
- **INTEGRAÇÃO**: `automato/acoes/cacador_hibrido.py` e `automato/camadas/trabalhar.py` agora acionam a guarda de cota de forma transparente entre ciclos.

## v1.6.6 — Dia 156 · Invariante 14: proibição de diálogos automatizados com NPCs de missão
- **CONTRATO / REGRA**: Em cumprimento à nova diretiva do autor (AGENTS.md Invariante 14 e Diretiva de Jogo §20), fica expressamente proibido automatizar falas e diálogos (`say`, `ask`, etc.) com NPCs em scripts em lote.
- **AJUSTE**: Scripts em `automato/acoes/` atuam apenas como posicionadores de rota e limpadores de sala hostil. Todo diálogo e entrega de missão deve ser executado diretamente pelo operador/agente em resposta consciente ao contexto ao vivo.

## v1.6.5 — Dia 156 · caçador híbrido, rota milharal v2 e protocolo canônico de autoquests
- **NOVO**: `automato/acoes/cacador_hibrido.py` — laço híbrido de caça contínua alternando Milharal V2 (ouro direto em corpos) e Masmorra dos Novatos (espólios e abates rápidos), com abastecimento de pão/água e sono regenerativo no Templo; para automaticamente ao bater meta de ouro.
- **NOVO**: `automato/acoes/ativar_gargamel.py` — rota automática do Templo até O Fim Do Túnel e execução do diálogo canônico com o Smurf Minerador (`say sim` -> `say Grebolius` -> `say sim`), ativando oficialmente *Uma Lição em Gargamel* em `score tudo`.
- **NOVO**: `automato/acoes/pegar_jarro.py` — rotina de inspeção e coleta em A Sala do Alquimista.
- **CORREÇÃO**: `automato/rotinas/milharal_v2.py` — restauração estrita do `CAMINHO_BOSQUE` até a sala-marco (*O Pequeno Bosque a leste*) e 2x norte até *A Entrada da Fazenda*, eliminando passos erráticos e atingindo 100% de taxa de chegada.
- **CORREÇÃO**: `automato/acoes/entregar_alquimista.py` — eliminação preventiva de combate (novato zumbi) ao abrir a porta da Sala do Alquimista e obrigatoriedade de diálogo prévio (`say Grebolius` -> `say sim`) antes de emitir `give aquosa alquimista`.

## v1.6.4 — Dia 156 · xadrez_v2, benchmark de grind e blindagem de entrega de autoquests
- **NOVO**: `automato/rotinas/xadrez_v2.py` e `automato/acoes/cacador_xadrez.py` — combate ativo focado em peões no Grande Tabuleiro de Xadrez, consider defensivo, triagem imediata de itens amaldiçoados (descarte de Armadura da Torre Negra), armazenamento na mochila de Pellinore e venda de espólios no Armeiro (armadura de peão 150, escudo 200) e Ferreiro.
- **NOVO**: `automato/acoes/cacador_milharal.py` — executor supervisionado para grind no Milharal com controle de hidratação, pães na mochila e recarga de mana no Templo.
- **CORREÇÃO**: `automato/acoes/entregar_alquimista.py` refatorado com função `verificar_preparacao_entrega()` que impede entrega de itens se a missão não constar em `score tudo` ou se a poção não estiver pronta no inventário, eliminando risco de perda de itens caros por diálogos concorrentes.

## v1.6.3 — Dia 156 · resiliência a emboscadas no trânsito e blindagem contra itens amaldiçoados
- **CORREÇÃO**: `da_floresta_ao_milharal()` em `automato/rotinas/milharal.py` agora detecta combate espontâneo durante o trânsito da fazenda (`lutando` no retorno de look). Em vez de falhar repetindo passos bloqueados com `"Não dá! Você está muito ocupado, lutando!"`, contra-ataca com `matar('monstro')`, despacha a ameaça via `lightning bolt` e retoma o deslocamento até o milharal.
- **CORREÇÃO**: `ir_ao_milharal()` agora executa `run('recall'); run('stand')` entre tentativas falhas de trânsito, garantindo que toda repetição parta limpa do Templo de Midgaard em vez de iniciar desorientada de onde a rota anterior parou.
- **CORREÇÃO**: `revisar_doacoes()` em `automato/camadas/prepara.py` agora inspeciona o retorno de `identify` antes de tentar equipar qualquer peça do chão da Sala de Doações. Se o item contiver flags de maldição (`amaldiçoado`, `nodrop`, `aura vermelha`), ele é descartado (`drop`) imediatamente sem ser vestido, impedindo que a personagem fique presa com equipamentos amaldiçoados de doação.

## v1.6.2 — Dia 156 · confinamento espacial no milharal e salvaguardas de sono
- **CORREÇÃO**: `automato/rotinas/milharal.py` atualizado com restrição espacial: o laço de busca de monstros agora rejeita salas fora do milharal (`'Milharal' not in t2`), impedindo dispersão para `O Gramado` e `Uma Pequena Estrada` (onde não há mobs) e mantendo a salvaguarda estrita contra o DT `Adentro do Milharal Destruído` (`Morte #5`).
- **CORREÇÃO**: `scripts/farm_ouro_milharal.py` recebeu suporte a todos os estados de fome e sede (`ficando com`, `com`, `com muita`, `morrendo de`) antes e após os ciclos de regeneração por sono no Templo, com compra automática de pão na Padaria e abastecimento de cantil na fonte, eliminando risco de desidratação ou inanição durante grind prolongado.

## v1.6.1 — Dia 156 · correção de `count_mobs` em `milharal.py`
- **CORREÇÃO**: `count_mobs` em `automato/rotinas/milharal.py` filtrava linhas apenas por `'está aqui'` ou `'está jogado'`, o que **ignorava todos os exemplares de `um monstro invasor`** (cuja descrição de sala é *"Uma estranha criatura, verde e peluda, está procurando algo."*, sem `'está aqui'`) e confundia cadáveres no chão (`'está jogado'`) com monstros vivos. Corrigido para ignorar `'corpo de'`/`'está jogado'` e casar as quatro descrições reais do milharal (`invasor`, `esfomeado`, `agressivo` e `lider`).
- **MOTIVO**: foi a causa técnica pela qual a Etapa 1 de `Problemas Agrícolas` (10 `um monstro invasor`) nunca fechava nas execuções automatizadas anteriores — a rotina só matava `esfomeado` e `agressivo`.

## v1.6 — Dia 156 · a devolutiva técnica obrigatória
- **NOVO**: **`scripts/devolutiva.py`** — o verificador de **fim de sessão**. Confere o protocolo
  inteiro e **reprova** o que passar despercebido: plano numerado (número, autoria, seção de
  devolutiva **preenchida**), **coerência da devolutiva contra o `git diff`**, `parts` de capítulo
  (`source_kind`/`date`/`evidence`), autoria das evidências, bloco no livro-razão, e segredo rastreado.
  Códigos: **0** ok, **1** falha, **2** só avisos.
- **NOVO**: a seção **`## 8. Devolutiva técnica`** no modelo do plano (`planos/LEIA.md`), com os quatro
  destinos do `AGENTS.md` §5 — **mapa, referência do servidor, fato do mundo, erro do motor**.
- **NOVO**: `scripts/test_devolutiva.py` — **20 testes**. Suíte offline: **121 → 141**.
- **NOVO**: `AGENTS.md` **§6.2** e item **obrigatório** no checklist *"Antes de encerrar"*.
- **MOTIVO**: **duas sessões seguidas falharam do mesmo jeito no mesmo dia.** A primeira publicou uma
  crônica errada (leu o fim de uma cadeia e narrou como começo). A segunda **andou os esgotos,
  descobriu que quatro salas eram anéis de mão dupla**, escreveu o achado em prosa numa seção chamada
  *"fechando os anéis do esgoto"* — **e não tocou no `mapa.json`**. **Nos dois casos nenhum validador
  percebeu**: o `check_project.py` confere **estrutura**, não **cobertura** — ele não sabe que uma
  caminhada aconteceu. **É essa cegueira que este script cobre.**
- **DETALHE DE PROJETO**: a janela do diff é **o commit que criou o plano ANTERIOR** (o plano anterior
  nasce no fim da sessão passada). `HEAD~1` erra quando a sessão já publicou — aconteceu no primeiro
  teste, com o `conhecimento.md` já commitado.
- **ARMADILHA RESOLVIDA**: o script **roda a suíte de testes**, e pode ser chamado **de dentro dela** —
  `devolutiva.py` → suíte → `test_devolutiva.py` → `devolutiva.py`… **travou de verdade** durante o
  desenvolvimento. A guarda é a variável de ambiente **`DSH_DEVOLUTIVA_RODANDO`**, e há um teste que
  a exige.

## v1.5 — Dia 156 · planos numerados e o "mandabala"
- **NOVO**: **planos numerados** em `data/heroes/<id>/planos/planoNNN.md` — **append-only**, um por
  sessão, com **autoria** no cabeçalho. O autor chega, diz *"executa o plano NNN"*, e quem pegar
  continua como se fosse o anterior. Regra no `AGENTS.md` **§6.1** e no checklist de encerramento.
- **NOVO**: **`scripts/mandabala.py`** — acha o **plano mais alto** do herói e imprime, num bloco só, a
  **ordem de leitura**, as regras que não se negociam e o **conteúdo integral** do plano. Avisa quando
  a numeração tem **lacuna**, quando o plano pedido **não é o mais recente** e quando ele **não declara
  autoria**. `--listar`, `--numero N`, `--hero`, `--so-caminho`. Não edita, não joga, não publica.
- **NOVO**: `scripts/test_mandabala.py` — **25 testes** (descoberta, resolução de herói, cabeçalho,
  lacunas, modos da linha de comando, e a integridade do plano real do repositório).
- **MOTIVO**: a passagem de um agente para outro estava custando **rodadas inteiras de redescoberta** —
  seis delas só para achar um NPC cuja sala estava escrita num documento do próprio repositório. Um
  arquivo que se *atualiza* perderia a informação de quem veio antes; um **plano novo por sessão**, não.
- **MUDOU**: a suíte offline passou de **91 para 116 testes**.

## v1.4 — Dia 156 · segurança de sessão, comércio e mapa derivado
- **CORREÇÃO (segurança)**: **`term 200 80` no login** (`driver/debo_bot.py`, constantes
  `TERM_LINHAS`/`TERM_COLUNAS`). Sem isto, `commands`, `help` longo e `autoquest todas` abrem
  **paginador**, e enquanto ele espera o driver entra em `estado=dead_or_menu` — **que o vigia lê como
  MORTA**. Era a **segunda** fonte de falso positivo de morte (a primeira foi uma DICA com "Menu
  Principal").
- **CORREÇÃO**: **`sacar_para_comprar()`** em `camadas/prepara.py`. A padaria cobra da **mão** e o
  `prepara` só depositava: no Dia 156 ela ficou com fome, com 2 moedas na mão e 369 no banco. O alvo é
  `config.SAQUE_PARA_COMPRAR` (300) e **o banco não cobrindo emite AVISO**, não falha silenciosa.
- **NOVO**: **revisão da Sala de Doações** em `camadas/prepara.py` (`revisar_doacoes()`), por diretiva
  do autor. Critério **empírico**: veste a peça, lê `Classe de Armadura`/`Acerto`/`Dano` do `score tudo`
  e compara. Não superou → devolve a peça à sala. `--sem-doacoes` desliga.
- **NOVO**: `rotinas/mercado.py` — auditoria de comércio: anda até cada loja pelo mapa, roda `visible`
  e `list`, e grava a tabela (item, preço, nível, encargo, estoque).
- **NOVO**: `acoes/fundir_mapa.py` — mesclagem **idempotente** do levantamento no mapa curado, com
  `ALIAS_CAMINHADA` (identidade provada pela caminhada) e `ARESTAS_VERIFICADAS` (correção ao vivo).
- **MUDOU**: `acoes/digerir_mapa.py` passou a viver em `automato/acoes/` (era `scripts/local/`, fora do
  git) e aceita `--glob` **repetível**.
- **MUDOU**: `config.USAR_INVISIBILIDADE = False` — invisibilidade **bloqueia comércio**
  (*"Não negocio com quem não vejo!"*). A proteção passou a ser a **rota**, via
  `config.RISCO_A_EVITAR` (`danger`, `high`, `fatal`, `critical`).
- **AVISO OPERACIONAL**: **digerir corpus PARCIAL encolhe o mapa.** Rodar `digerir_mapa.py` só com um
  recorte e fundir levou o mapa de **360 para 224 salas**. O `--glob` precisa cobrir **todo** o corpus.
  Sintoma: o `TOTAL` do `fundir_mapa.py` **diminuir**.

## v1.3 — Dia 155 · identificação do agente
- **NOVO**: todo agente que operar o automato deve **dizer qual modelo é** no início do relatório e
  registrá-lo nos arquivos de evidência (campo `agent`) e na mensagem do commit (`[agente: <modelo>]`).
- **MOTIVO**: com mais de um agente mexendo no mesmo jogo, é preciso saber quem mudou o quê — e poder
  comparar o desempenho entre modelos.

## v1.2 — Dia 155 · autoexame e plano do capítulo
- **NOVO**: `automato/verificar.py` — autoexame em 18 itens (ambiente, core, driver, runtime, conhecimentos, rotinas, documentação).
- **NOVO**: `data/heroes/grebolius/plano_capitulo_03.md` — o plano do capítulo para o agente (missões, rotas, ferramentas, execução em 5 passos).
- **NOVO**: `automato/acoes/mapear.py` — mapear à mão uma sequência e buscar sala/saída por nome, gravando o caminho.
- **CORREÇÃO**: a guarda de repetição passou a contar **apenas assinaturas de problema** — salas homônimas de labirinto não a disparam mais.
- **CORREÇÃO**: a rotina `milharal` percorre o labirinto do bosque pela sala-marco ("O Pequeno Bosque" a leste) e a reta final é verificada sala a sala.

## v1.1 — Dia 155 · automato autossuficiente
- **MUDOU**: o **driver inteiro** (debo_bot.py, parsers.py, live_daemon.py, play.py) passou a viver em `automato/nucleo/driver/`.
- **MUDOU**: token, senha e logs foram para `automato/runtime/` — **fora do git** (`.gitignore`).
- **NOVO**: `automato/acoes/ressuscitar.py` (a ressurreição virou ação do automato).
- **NOVO**: `config.py` aponta os documentos do herói (`conhecimento.md`, `diretiva_de_jogo.md`, `mapa.json`) — referenciados, não copiados.
- **REQUISITO**: subir o driver antes de qualquer camada.

## v1.0 — Dia 155 · empacotamento
- **NOVO**: pasta `automato/` com núcleo, camadas, rotinas e documentação (README, CHANGELOG, DECISOES).
- **NOVO**: `nucleo/config.py` — um único ponto de configuração (caminhos, limites, magias).
- **MUDOU**: as rotinas leem `config` em vez de ter caminhos fixos; o automato roda fora de `scripts/local/`.
- **NÃO MUDOU**: o contrato das rotinas (partir do Templo, voltar, salvar).

## v0.6 — Dias 152-154 · trajeto determinístico
- **CORREÇÃO**: `base.py` apontava o token para o caminho errado — todas as rotinas liam vazio.
- **CORREÇÃO**: a rota da fazenda é **oeste, oeste, oeste** (Entrada da Fazenda → Pequena Estrada → Fim da Estrada → Milharal).
- **NOVO**: rota completa Templo→Milharal documentada no `conhecimento.md` §24: n5 → n,e,n → n6 → l6 → n,n,l,l,s → o3.
- **NOVO**: o caçador usa **LIGHTNING BOLT** (48-64 de dano) e mira o **nome exato** do monstro.

## v0.5 — Dia 150 · diretiva do autor
- **REMOVIDO**: venda de armaduras (rotina `xadrez` **suspensa** para `rotinas/_suspensas/`).
- **MOTIVO**: "perdemos mais dinheiro do que ganhamos com elas" — caixa finito do armeiro + armadura amaldiçoada (60 kg) + pergaminho de 8.509 para vender por 8.500.

## v0.4 — Dias 148-149 · camadas de decisão
- **NOVO**: `vigia.py` (diagnóstico pelo log), `prepara.py` (arrumador + banco), `trabalhar.py` (despachante), `turno.py` (encarregado).
- **NOVO**: **banco do Templo** no prepara (`deposit`), com reserva de 300 na mão.
- **NOVO**: hidratação na **fonte de mármore azul** da Praça do Templo (`fill cantil fonte` / `drink fonte`).
- **CORREÇÃO**: o prepara só compra pão se não tiver (ela acumulou 10 e ficou em 130/115 kg).

## v0.3 — Dia 147 · higiene e alvo
- **NOVO**: `abastecer()` — comer e beber **antes** de dormir/viajar (dormir faminto consumia vida e mana).
- **CORREÇÃO**: caçador com **plano B de alvo** quando a magia pergunta "em que?".

## v0.2 — Dia 143 · guarda de repetição
- **NOVO**: `guarda.py` — mesma resposta **3× seguidas** → `recall` + `save` + saída (código 9).
- **NOVO**: injeção da guarda no `run()` de **33 robôs**.
- **CORREÇÃO**: a guarda passou a **ignorar comandos benignos** (buy/eat/drink/look/score/rest/sleep) — compras legítimas a disparavam.

## v0.1 — Dia 141 · método
- **NOVO**: o método "mapear à mão → testar em trechos → só então automatizar".
- **NOVO**: `wake; stand` obrigatório antes de qualquer deslocamento.
- **MOTIVO**: 7 mortes, das quais **4 causadas por script sem supervisão**.

## Próximas versões (planejado)
- **v1.1**: rotina `dicas-magicas` (descobrir o gatilho do ciclo do "sim").
- **v1.2**: rotina `esgoto` de verdade (reconhecimento com mapa incremental).
- **v1.3**: o turno relançar a rotina sozinho quando o vigia voltar a OK.
