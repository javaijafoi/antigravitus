# Controle de versão do automato

Versionamento semântico adaptado a um jogo: **MAIOR** muda o contrato das rotinas,
**MENOR** acrescenta camada/rotina, **CORREÇÃO** conserta comportamento.
As datas usam o **dia de jogo**.

## v1.7.18 — Dia 158 · Fecho de capítulo com critério ou bypass do autor (DeepSeek deepseek-flash)

Origem: Lote C da decisão sobre as seções sem trava, refinado por uma exigência do autor — *"pra fechar tem que confirmar comigo se não obedeceu, porque eu posso dar bypass"*. A regra vivia em prosa na diretiva §11 e já tinha falhado uma vez (Dia 136: o capítulo foi fechado com a fortuna parcial e o próprio servidor devolveu para `em_curso`).

- **`capitulos.json`:** o capítulo passa a ter `closing_criteria` (os alvos do fecho, cada um com `done` e `evidence`) e `closing` (`confirmed_with_author`, `at`, `decision` = `cumprido|bypass`, `reason`). O capítulo 12 nasceu com dois: **Xeque-mate** e **Ajuda Mágica**.
- **`check_project.validate_fecho_do_capitulo`** (`fecho.do_capitulo`), a partir do capítulo 12 — o legado 0–11 fica intocado:
  - `concluido` sem `closing.confirmed_with_author` + `at` → **ERRO** (fechou sem falar com o autor);
  - critério aberto com `decision: cumprido` → **ERRO** (o caso do Dia 136);
  - `decision: bypass` sem `reason` → **ERRO** (bypass sem motivo é esquecimento);
  - critério `done: true` sem `evidence` → **ERRO** (fato sem fonte).
- **`devolutiva.bypass_do_ultimo_fecho`** (`fecho.bypass_visivel`): capítulo fechado por bypass gera **aviso** no fechamento, para a crônica não tratar como cumprimento normal.
- **Diretiva §11:** a linha "vira campo no `capitulos.json` — pendente no Lote C" passou a descrever o check em vigor.
- **Testes:** `test_check_project.py` (+8) e `test_devolutiva.py` (+3). Suíte: 366 OK. 2 IDs novos na catraca.
- **Limite:** o check prova que existe o **registro** da confirmação, não que a pergunta foi feita — registro falso é o mesmo problema que evidência falsa. O que ele impede é o fecho **silencioso**. E critério frouxo passa: se o alvo declarado for vago, o check aceita.

## v1.7.17 — Dia 158 · §6 e §8 viram default no código: a armadilha aborta e a postura não custa a viagem (DeepSeek deepseek-flash)

Origem: a decisão sobre as 8 seções da diretiva sem trava. Duas delas não eram dívida de documento, eram **lacuna de comportamento**:

- **§6 (armadilha mortal).** O aviso *"Você percebe que há algo perigoso por perto!"* só era tratado em `milharal.py` e `milharal_v2.py`. `navegar`, `xadrez_cascata`, `esgoto` e `novatos` andavam para dentro. Agora `base._checar_dt()` levanta `PerigoMortal` em todo `andar()` e o `navegar.py` para com **código 7** antes de dar o passo.
- **§8 (`stand` antes de andar).** O `navegar.py` tratava "muito relaxado" como recusa de rota e parava com código 5 — a viagem inteira morria por postura. Agora `base.andar()` e o `navegar.py` mandam `wake; stand` e repetem **uma vez**.
- **Diretiva:** §3 e §7 ganharam etiqueta de **referência** (fatos e mecânica que o código já cumpre); §6 e §8 ganharam **nota datada** dizendo que viraram default. Sem apagar nada do autor.
- **Testes:** `test_sobrevivencia.py` (+6): aborto no aviso, código 7 no navegar, levantada única, recusa de rota ainda falsa. Suíte: 355 OK. 3 IDs novos na catraca.
- **Limite:** nada exercitado ao vivo. O risco do §6 é **falso positivo** — se o servidor usar a frase em contexto inofensivo, a rotina para. Por isso o aborto é explícito e registrado no log; medir numa sessão antes de confiar.

## v1.7.16 — Dia 158 · Coesão: um comando de fechamento e a tabela de modos presa à diretiva (DeepSeek deepseek-flash)

Origem: auditoria de coesão pedida pelo autor. Duas contradições reais, as duas nascidas do que eu mesmo escrevi antes:

- **`AGENTS.md` dizia "encerrar são dois comandos"** (`encerrar.py` e `devolutiva.py`), mas o `encerrar.py --fechar` **já roda** o `devolutiva.py` internamente. O agente pagaria 18 s e uma suíte de novo por nada. Agora o fechamento é **um** comando; o `devolutiva.py` sozinho só para investigar uma falha. O checklist e o §6 foram alinhados.
- **`PROTOCOLO.md` §3 dizia que o `encerrar.py` (fase de preparo, sem `--fechar`) rodava o `devolutiva.py`.** Ele não roda: nessa fase são `sync_hero --check`, `check_project` e o auditor.
- **`mandabala.MODOS` é cópia da tabela da §26.** Cópia sem check envelhece — foi assim que o projeto acumulou regra sem verificação. Novo teste `modos.batem_com_a_diretiva` lê a §26 e compara nome a nome, na ordem; mudar a diretiva sem mudar o `MODOS` reprova a suíte.
- **Testes:** `test_mandabala.py` (+1). Suíte: 349 OK. 1 ID novo na catraca.

## v1.7.15 — Dia 158 · O radar de uso: a ferramenta existe e não está sendo usada (DeepSeek deepseek-flash)

Origem: proposta do autor — "deveria ter um `quality_run.py` vendo se o número de vezes que os scripts rodaram parece normal… e perguntar se ele leu e está fazendo de acordo com a diretiva". Não existia nada assim: o `vigia.py` olha o **estado** da personagem, o `auditar_sessao.py` olha o **uso depois** da sessão, e nada olhava o uso **durante**. Foi por isso que 4 dias passaram sem rotina supervisionada com o vigia respondendo OK.

- **`camadas/vigia.py`:** `uso_do_transcript(janela_min=30)` — lê o transcript mais recente e conta, por `origem`, quantos comandos vieram de cada script, separando passos e ataques feitos pelo `play.py`. `diagnostico_de_uso()` transforma isso em `USO_ANOMALO` acima de **60 passos** ou **25 ataques** à mão na janela (o auditor usa 80/30 na sessão inteira). `rotina_recente()` detecta turno supervisionado pelo `rotina.log`.
- **Silêncio explícito:** nada de alerta dormindo (o `dormir()` novo bloqueia até 45 min; a janela de silêncio é 50) nem com rotina rodando nos últimos 10 min. Sem isso o radar vira ruído no primeiro dia.
- **`scripts/quality_run.py`:** `--loop --intervalo 30` para job em segundo plano, `--janela`, `--json`, `--sem-registro`. Grava uma linha por verificação em `automato/runtime/qualidade.jsonl` (fora do git) e só imprime quando há o que dizer. Códigos: 0 ok, 1 anomalia, 2 sem sessão.
- **O alerta afirma, não pergunta.** Auto-relato já falhou aqui (planos 037–039 "justificaram" falhas do auditor). O texto exige uma resolução: rodar a ferramenta do modo, ou mudar o modo com motivo registrado.
- **`PROTOCOLO.md`:** §2 manda subir o radar enquanto a sessão for à mão; §3 passa a fechar com `--fechar --tipo <chefe|moagem|expedicao|mapeamento|missao|outro>` (combina com as métricas do boletim).
- **`automato/README.md`:** linha nova na tabela "Ferramentas".
- **Testes:** `scripts/test_qualidade.py` (12). 2 IDs novos na catraca.
- **Limite:** os limiares 60/25 são escolha a partir dos do auditor, não medição — a primeira sessão real calibra. E o radar mede **adesão ao modo**, não qualidade da jogada: tática ruim com o script certo rodando continua passando.

## v1.7.14 — Dia 158 · O placar do boletim e os números do sono e do Rei (DeepSeek deepseek-flash)

Origem: as fases 4 e 5 do plano de solução — "sinto que o Claude ignora" só se prova com dado, e o `boletim.jsonl` tinha 10 linhas, todas Claude, sem nenhum número de jogo dentro.

- **`scripts/encerrar.py`:** `metricas_do_transcript()` — comandos, minutos, `consider`, `casts`, `armor`, `recalls`, linhas de fome, mortes, vida com que a sessão começou e `consider_por_100_magias`. Tudo do transcript, nada declarado pelo agente.
- **Boletim:** a linha ganha `metricas` e `tipo` (`--tipo chefe|moagem|expedicao|mapeamento|missao|outro`). Sem o tipo, "20 minutos no Rei" e "20 minutos no milharal" viram o mesmo número.
- **`--placar`:** tabela por modelo — sessões, falhas da devolutiva e do auditor, comandos/sessão, minutos/sessão, considers por 100 magias, mortes e % de avanço declarado. Sessão antiga, sem métricas, aparece como `—` e não como zero.
- **`conhecimento.md` §83:** o sono em números (mana em 3 min, vida a ~5 hp/min, fome cancela). **§84:** o Rei Negro em números nas duas lutas — dano por raio, vida perdida por rodada, 10 segmentos, regeneração, e a conta de 25 a 35 raios que fecha o kite como inviável.
- **`maquina/verificacoes.md`:** o sono como mecânica do servidor, com data e fonte.
- **Testes:** `test_encerrar.py` (+7). Suíte: 336 OK. 2 IDs novos na catraca.
- **Limite:** o placar só fica comparável daqui para frente — as 10 linhas antigas não têm `metricas` e não dá para reconstruir o tipo de conteúdo delas. `mortes` conta a linha "Você está morto" e pode contar duas vezes se o servidor repetir a mensagem.

## v1.7.13 — Dia 158 · Modo breve, fechamento em um comando e AGENTS.md pela metade (DeepSeek deepseek-flash)

Origem: pedido do autor — "otimizar para garantir menos regras escritas que podem ser ignoradas" e "não usar um monte de token de forma boba (verificações excessivas ou jogar de forma burra)". Medido: 85 a 110 tokens por comando de jogo; 3,1 milhões de tokens em 14 sessões; 24% dos comandos são movimento, cada um devolvendo a descrição inteira da sala (~304 chars, ~85 tokens); o protocolo custava ~19 mil tokens fixos por sessão, dos quais 8.345 só de `AGENTS.md`.

- **`nucleo/base.py`:** `display_breve()` e `brief(ligar)` — leem o estado do `toggle` e só trocam quando precisa, devolvendo o estado anterior para restaurar. `navegar.py` liga o modo breve na rota conhecida e restaura no `finally` (`--sem-brief` para mapear); `turno.py` faz o mesmo em volta do laço (novo `_laco`, para o `finally` cobrir tudo). Nunca em `explorar`: ali a descrição é o dado.
- **`scripts/devolutiva.py`:** `codigo_mudou(desde)` — a suíte de 330 testes só roda se algum `.py` mudou desde o commit-base. Sessão que só mexeu em `data/` deixava de provar qualquer coisa e custava 7,3 s (o `devolutiva.py` inteiro levava 17,9 s).
- **`AGENTS.md`:** 30.043 → 14.344 bytes (~8.345 → ~3.984 tokens, −52%). Saiu a prosa duplicada (o detalhe já vive no `PROTOCOLO`, `arquitetura` e `glossario`), saiu o §11 "estado verificado" (números de 16/10, stale). Ficaram as 15 invariantes, a regra zero, a fonte da verdade, o registro, os checklists, a concorrência e as diretivas §12/§13/§14. O checklist de encerramento passa a mandar **um** comando: `devolutiva.py` (que já roda `check_project`, `verificar` e a suíte condicional).
- **§14.5 nova:** ordem de preferência — **default no código > check > prosa**. Regra que não vira nenhum dos dois é dívida.
- **Testes:** `test_sobrevivencia.py` (+3 do modo breve) e `test_devolutiva.py` (+1: sessão sem `.py` pula a suíte). Suíte: 330 OK. 4 IDs novos na catraca.
- **Limite:** nada exercitado ao vivo. O `brief` depende de o DeBo aceitar o `toggle` (o texto "Modo breve: SIM/NÃO" foi visto em 17/10); se o servidor responder outra coisa, `display_breve()` devolve `False` e o par liga/restaura continua correto. O corte de `look` não foi feito: são 78 chamadas legítimas de posição nos scripts, e o `brief` já barateia todas.

## v1.7.12 — Dia 157/158 · O portão da §26: fome, sede e armadura antes de sair, e os cinco modos (DeepSeek deepseek-flash)

Origem: o autor cobrou que "não passar fome nem sono nem ficar sem armadura", que a estrutura de fluxo "seja obedecida e não contornada", e que "tudo que é novo entre na estrutura de forma estruturada". Medido nos transcripts de 16 a 20/10: última rotina supervisionada em 16/10 15:10; nas últimas 24 h, 5 de 11 sessões sem nenhum `armor`, 159 linhas de fome e 2 `consider` em 846 magias.

- **`camadas/prepara.py`:** `dormir()` deixa de dormir 75 s fixos e passa a mirar a **vida**. Funções puras `hp_do_score()` e `minutos_de_sono()` (taxa medida ~5 hp/min; teto de 45 min; piso de 3). Medido nos 374 episódios de sono: a mana enche em ~3 min (+231 num episódio), a vida dá **+0 na mediana** e só sobe em 34 de 591 intervalos fora de combate; com fome/sede o ganho não acontece (`morrendo de fome! (-3hp, -6mn)`), então `dormir()` devolve `False` e manda comer primeiro.
- **`camadas/navegar.py`:** `cuidado_antes()` roda o `cuidar.py` antes de sair e respeita o contrato dele (0 segue, 2 manda rodar o `prepara.py`, 1 para). `--sem-cuidado` para teste/mapeamento. Sai com 2 ou 1 em vez de andar com fome.
- **`camadas/turno.py`:** `socorrer()` roda uma vez **antes** do laço, sempre — o vigia não acusa armadura, e ela estava sendo esquecida.
- **`scripts/auditar_sessao.py`:** três FALHAS de estado, não de proxy: `fome-em-sessao` e `sede-em-sessao` (uma por sessão) e `armadura-ausente` (ataque com CA < 140 no último `score`). Sem CA no transcript, não inventa.
- **`data/heroes/grebolius/diretiva_de_jogo.md` §26:** os cinco modos (`caminhar`, `explorar`, `moer`, `missão`, `chefe`) com dono e proibição, e a regra do que é novo (tabela de ferramentas + `DECISOES.md` + catraca + teste no mesmo commit).
- **`scripts/mandabala.py`:** `pre_voo()` na abertura — vida/mana/mv registrados, minutos de sono até ~98%, CA com e sem `armor`, há quantos dias não roda rotina supervisionada, e a tabela dos cinco modos.
- **Testes:** `scripts/test_sobrevivencia.py` (14). Suíte: 326 OK. 6 IDs novos na catraca. `check_project.py` 0 erros, `verificar.py` 19/19.
- **Limite:** nada exercitado ao vivo. Os limiares (98% de vida, 45 min, CA 140) vêm de medição, mas a taxa de 5 hp/min tem amostra pequena (34 intervalos) e deve ser reconferida na primeira sessão que dormir de verdade.

## v1.7.11 — Dia 157 · `ressuscitar.py` pela base, com origem e o menu de morte (Claude Opus 5.5)

- `acoes/ressuscitar.py`: a docstring descrevia outro script (`farm_armaduras.py`); agora diz o que ele faz. O cliente próprio saiu: fala com o driver por `base.run`, ou seja, com o token de `automato/runtime/.controller` (antes lia `scripts/local/.controller`, caminho antigo), com a origem `ressuscitar` no transcript e com a guarda de repetição da base.
- Decisão de cada passo em `proximo_comando(texto)`, função pura: menu de morte → `_RAW 1` (o travamento do §73); Fonte da Vida → `drink fonte`; portal → `enter portal`; Vazio → `n`; dica "chama sua atenção para o <direção>"; e a dica que o código antigo ignorava, "Uma curiosa saída, para cima, chama sua atenção" → `u`. Textos dos logs do Dia 156.
- Teste novo: `scripts/test_ressuscitar.py` (7). Não exercitado ao vivo (exige morrer).

## v1.7.10 — Dia 157 · `mandabala.py --sobre` lê o histórico de combate dos transcripts (Claude Opus 5.5)

- `scripts/mandabala.py`: `historico_de_combate(termo)` e `linhas_do_historico()`. O `--sobre <alvo>` passa a listar, por sessão, cada lance contra o alvo (ataque, magia ofensiva ou `consider`; reaproveita `auditar_sessao.alvo_de_ataque`), com vida antes e depois, dano `[N]`, barra de vida do inimigo (`{<<<<<>>>>>} o Rei Negro`, 10 segmentos) e morte. ~3 s sobre os 39 transcripts. ID na catraca: `historico.combate`. Testes: `test_mandabala.py` (+4).
- Motivo: o kite no Rei de 20/10 repetiu o de 18/10, cujos números só estavam no transcript (conhecimento §76, adendo da revisão de 10 dias). A ferramenta corrigiu a própria revisão: a barra do Rei **mexeu** em 20/10 e tem 10 segmentos, não 11.
- Limite: casa o alvo pela primeira palavra do comando (`rei`, `torre`), então `--sobre "Rei Negro"` também traz lances contra o Rei Branco se houver; os textos ficam no transcript.

## v1.7.9 — Dia 157 · O transcript diz de onde veio cada comando; catracas da revisão de 10 dias (Claude Opus 5.5)

Origem: `data/heroes/grebolius/observacoes/revisao-10-dias-2026-10-20.md`. De 16 a 20/10 o `turno.py` não rodou nenhuma vez depois de 16/10 15:10; em 20/10 houve 1 `consider` em 589 magias e as três mortes no tabuleiro vieram de táticas testadas ao vivo.

- **Protocolo do driver:** a primeira linha do pedido passa a ser `<token>\t<origem>` (`live_daemon.ler_cabecalho`; cliente antigo sem origem continua aceito). Cada comando do transcript ganha o campo `origem`: `play` (play.py, à mão), o nome do script (`base.origem()`: `navegar`, `xadrez_cascata`...) ou `turno:<rotina>` (o `turno.py` exporta `MUD_ORIGEM`). Para mapear área nova à mão: `MUD_ORIGEM=mapear`. **Reiniciar o `live_daemon` para valer.**
- **`scripts/auditar_sessao.py`:** novas FALHAS `andar-a-mao` (mais de 80 passos pelo play.py) e `caca-a-mao` (mais de 30 ataques pelo play.py); `ataque-sem-consider` passa de AVISO a FALHA, uma vez por alvo, e passa a cobrir `sleep`, `curse`, `blindness`, `poison`, `charm person`, `color spray` e `fireball`; o consider de `torre` vale para `1.torre`/`2.torre`. Transcript antigo, sem origem, fica fora das duas regras novas (INFO `origem-ausente`).
- **`nucleo/base.py`:** `considerar(alvo)` (um `consider` por alvo e por processo; devolve o perigo duro da diretiva §2) e `perigo_duro()`. `rotinas/milharal_v2.py` e `rotinas/novatos.py` não atacam com perigo duro.
- **`acoes/xadrez_cascata.py`:** `consider` no primeiro encontro com cada peça (perigo duro para a etapa, código 4; no Rei só registra, porque `--rei` é a autorização) e `pode_lancar()`: nenhum lance com vida abaixo de 100 (a ida para **antes** do próximo lance, como o §73 pediu).
- **`scripts/devolutiva.py`:** `plano.falha_justificada`: a partir do plano 041, dar uma FALHA do auditor por "justificada/explicada" exige citar o `.py` que a evita, e ele tem de ter mudado na sessão.
- **Testes:** `test_auditar_sessao.py` (+8), `test_xadrez_cascata.py` (+5), `test_devolutiva.py` (+3). 11 IDs novos no `catraca.json`.
- **Limite:** nada disso foi exercitado ao vivo; os limites 80 e 30 são escolha minha a partir da revisão e podem precisar de ajuste.

## v1.7.8 — Dia 157 · Rotina mais rápida, `armor` no preparo e testes de "quem acorda" (Claude Sonnet 5.5)

- `camadas/prepara.py`: novo `garantir_armor()` (lê a CA do `score tudo` e relança `armor` na Praça se cair abaixo de 140; roda a cada `prepara`). Diretiva do autor: `armor` dura horas e fica no preparo, não no script de ataque. Teste: `scripts/test_prepara_armor.py`.
- `acoes/xadrez_cascata.py`: descanso só até 250 de mana (antes 440) e nenhum descanso se já estiver pronta; `comer_beber` só com fome ou sede; esperas menores (passo 0,15 s, magia/raio 1,5 s, sleep 2 s, polling do descanso 10 s). O kite no Rei faz 1 raio por ida.
- Resultado dos testes ao vivo: `curse` e `poison` não acordam mob dormindo; `blindness` acorda bispo e cavalo (`conhecimento.md` §75). As listas `ETAPAS` ainda lançam `blindness` em bispos e cavalos: ajustar no próximo teste (ordem do autor: sleep, curse, poison, blindness por último).
- Limite: nenhuma morte do Rei Negro; o kite de 2 raios falhou (§73).

## v1.7.7 — Dia 157 · Cascata do Xeque-mate em Python e o tabuleiro no mapa (Claude Sonnet 5.5)

- Novo `acoes/xadrez_cascata.py`: etapas `peoes|bispos|cavalos|torres|rainha|f1|rei`, rastreio de posição A1 a H8 com verificação de cada passo (cor, frase da peça, número de saídas) e casas proibidas E8, E1, B1 e G1. Nasceu das mortes #10 e #12 (laços em PowerShell perderam a posição por respostas de `look` atrasadas). `--rei` é obrigatório para o kite no Rei Negro.
- Novo `scripts/mapear_tabuleiro.py` + testes: grava as 64 casas (`xadrez_A1` a `xadrez_H8`) no `mapa.json` pela grade da zona 36 e baixa o portão para `medium`, de modo que o `navegar.py` anda até o tabuleiro sem `--permitir-risco`.
- Limite honesto: o módulo foi testado só nas partes puras (verificação, grade, caminho); o fluxo ao vivo ainda não foi exercitado. Nunca derrubar todos os processos Python: há um `http.server` de outro projeto na porta 8768 (derrubar só o `live_daemon`).

## v1.7.6 — Dia 157 · Vigia de cota para o Claude Code (Claude Sonnet 5.5)

- Novo `scripts/cota_claude.py` + `scripts/test_cota_claude.py`: le um snapshot em `automato/runtime/cota_claude.json` registrado a partir do `get_usage` do harness; corta com a janela de 5 h restando <= 10% ou a semanal restando <= 5% (AGENTS §13) e recusa snapshot com mais de 20 min. IDs na catraca: `cota.claude.corte`, `cota.claude.fresco`, `cota.claude.abertura`.
- `mandabala.py` passa a mandar registrar a cota na abertura. Limite: o Python nao alcanca o `get_usage` sozinho; o agente precisa registrar.

## v1.7.5 — Dia 158 · Mochila vestida e espólios dos corpos (Claude Sonnet 5.5)
- **`nucleo/config.py`:** `ESPOLIOS_PROIBIDOS`, `ESPOLIOS_LIMPOS`, `FLAGS_DE_MALDICAO`, `MOCHILA` (medidos ao vivo, `conhecimento.md` §68).
- **`nucleo/base.py`:** `guardar_na_mochila()` (tira → `put` → veste; tira o manto se o slot estiver ocupado) e `espolio_proibido()`.
- **`rotinas/xadrez_v3.py` (legado, ainda "não usar"):** a triagem lista o corpo e pega item por item (nunca `get all corpo` às cegas; a Armadura da Torre Negra é deixada), pega lança/espada/coroa/escudo/cetro, guarda na mochila VESTIDA, e a venda tira a mochila antes de `get ... mochila` e para de vender lança quando o ferreiro diz que não pode pagar.
- **Custo:** a rotina continua suspensa até a revisão do autor; sem teste novo (fluxo ao vivo). Suíte: 231 OK.

## v1.7.4 — Dia 157 · Python acessível para qualquer agente (Claude Opus 5.5)
- **`scripts/configurar_python.ps1` (novo):** acha o Python mais novo em `%LOCALAPPDATA%\Programs\Python` e põe a pasta dele, a `Scripts` e o `Launcher` (`py.exe`) na frente do PATH do **usuário** (sem administrador). Guarda o PATH antigo num arquivo de backup. Por padrão só simula; aplica com `-Aplicar`. Causa observada: o Python não estava no PATH do usuário, e o `python` caía no atalho da Microsoft Store (`WindowsApps\python.exe`).
- **`verificar.py` — item `python no PATH`:** AVISO quando `python` resolve para o `WindowsApps` ou não existe, apontando o script.
- **AGENTS "Comece aqui" e PROTOCOLO §1 passo 0:** o que fazer quando `python` abre a Store.
- **Custo:** nenhum no repositório. Aplicar muda o PATH do usuário da máquina (reversível pelo backup).

## v1.7.3 — Dia 157 · Quatro checagens da auditoria do Haiku (Claude Opus 5.5)
- **Brecha do #13 (`DELEGA_MESMA_FRASE`, `mandabala.py`):** citar #13/#15 só libera a delegação ao autor na **mesma frase** do §5. O Plano 035 citava #13 ao falar do give e, em outra frase, mandava "perguntar ao autor a palavra de abertura", e passava.
- **Conhecimento na abertura (`abertura.conhecimento_do_npc`, `--sobre`):** a sequência de abertura lista, para os nomes do §5, as seções do `conhecimento.md` e as linhas mais recentes que os citam. `mandabala.py --sobre <nome>` faz a mesma consulta a qualquer momento. O Haiku tentou `ask lemin ajuda`, e a cadeia (responder "Merlin") estava na §61.
- **`state.desatualizado` (`devolutiva.py`):** se houve conexão ao jogo depois do commit que abriu a sessão e o `state.json` não mudou, FALHA.
- **`sessao.aberta` (`devolutiva.py` + `mandabala.py`):** a última conexão sem `close`/`shutdown` reprova no fechamento e gera aviso na abertura seguinte. Caso real: uma conexão depois do handoff deixou a personagem parada em Lyon. PROTOCOLO §3: depois do handoff, não reconecte sem novo handoff.
- **Testes:** `scripts/test_checagens_haiku.py` (13). A catraca aceita o mesmo id em dois arquivos (`sessao.aberta`). Suíte: 231 OK.

## v1.7.2 — Dia 157 · navegar.py tolera o nome curado e absorve a rota do nav.py (Claude Opus 5.5)
- **`camadas/navegar.py`:** a conferência de sala aceita o título do jogo sem o sufixo de curadoria entre parênteses ("A Rua Principal" bate com "A Rua Principal (Oeste)") e os `aliases` da sala (`nomes_aceitos`, `confere`). A origem sai de `deduzir_origem`: candidato único; entre homônimos, a única sala curada (fora da camada `levantamento`; "A Praça do Templo" → `praca_templo`); senão para com código 2 listando os ids e pedindo `--de`. Com `--de`, o `look` inicial confere que a personagem está mesmo ali (código 3 se não).
- **`data/heroes/grebolius/mapa.json`:** a rota Templo → Praça de Jareth do `nav.py` virou arestas (fonte `rota_verificada_dia157`; saídas reais em `evidence/dia156j.json`). Sala nova `estrada_mj_antes_posto_sul`; `estrada_colina_topo` marcada como duplicata de `lb012`; alias "O Grande Campo de Midgaard" nos três Grandes Campos. Cortados os atalhos falsos que o BFS preferia: Atrás do Altar leste/oeste, Padaria norte, Grande Campo (Sul) leste, Começo da Passagem oeste/norte, Pequena Sala do Guarda oeste/sul ↔ fazenda, Centro do Vilarejo leste, Casebre leste, Aclive→Topo→Proximidades e Portão Oeste/Leste ↔ Centro de Jareth diretos (a Avenida Floris entra no meio).
- **`rotas/nav.py`:** virou um aviso que repassa ao `navegar.py` (`templo-praca-jareth` → `--para lb013`, `praca-floris1` → `--para lb014`). `--de N`/`--ate N` por índice de passo deixam de existir.
- **Testes:** `scripts/test_navegar.py` (14 testes, sem conexão; suíte: 213 OK). `navegar.py --seco --de templo_midgaard --para lb013` = os 26 passos do `nav.py`; `--para jareth_centro` = os mesmos + `e e e` (o Centro fica três salas a leste da Praça).
- **Custo:** outras rotas podem mudar de trajeto, porque arestas falsas saíram do mapa. O levantamento ainda tem atalhos falsos fora desta rota; a conferência de título para no primeiro.

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
