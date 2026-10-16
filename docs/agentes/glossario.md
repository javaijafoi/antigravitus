# Glossário — cada artefato e cada termo

> Inventário do que existe no repositório e do vocabulário usado nos documentos. Serve para dois
> propósitos: **saber o que é cada arquivo antes de mexer nele** e **falar a mesma língua** que os
> registros anteriores.
>
> Colunas: **Caminho** · **O que é** · **Quem escreve / gera** · **Versionado?**

Legenda de versionamento: **sim** = rastreado pelo git · **não** = ignorado (`.gitignore`) ·
**derivado** = rastreado, mas gerado por ferramenta e nunca editado à mão.

---

## 1. Raiz do repositório

| Caminho | O que é | Quem escreve | Versionado |
| --- | --- | --- | --- |
| `AGENTS.md` | **Ponto de entrada de qualquer agente**: regra de identificação, lógica resumida, invariantes, checklists, trabalho concorrente | agente (este guia) | sim |
| `README.md` | README humano do projeto: temporadas, arquivos de campanha, rotina de sessão, comandos, publicação | agente/humano | sim |
| `TEMPLATE_NOVO_HEROI.md` | Guia de criação de nova campanha sem inventar histórico | agente | sim |
| `TEST_READY.md` | Estado da infraestrutura de testes offline (milestone M_TEST) e comandos de execução | agente | sim |
| `index.html` | Home do site: seletor de herói, temporadas, grade de dias/capítulos | humano | sim |
| `ficha.html` | Página de ficha do personagem (lê `ficha.md`/`hero.json`) | humano | sim |
| `mapa.html` | Mapa interativo (lê `mapa.json`) | humano | sim |
| `sobre.html` | Página institucional do cronista/herói | humano | sim |
| `relatorio_auditoria_grebolius.html` | Relatório HTML autônomo da auditoria offline de conformidade | `scripts/run_offline_tests.py` | derivado |
| `add_day.py` | CLI que registra uma crônica/dia em `posts.json`, com fonte obrigatória e `--replace` explícito | humano/agente | sim |
| `add_chapter.py` | CLI que abre, salva partes e fecha capítulos da Season 02 (`capitulos.json`) | humano/agente | sim |
| `create_hero.py` | CLI que cria o **rascunho** de um herói (`record_status: draft`), sem inventar despertar | humano/agente | sim |
| `publish_daily.py` | Valida e monta **uma** revisão; só `--publish` cria commit e só `--push` envia. Aplica lista de caminhos publicáveis | humano/agente | sim |
| `vercel.json` | Configuração de deploy estático + cabeçalhos de segurança | humano | sim |
| `.gitignore` | Exclusões de segredo, sessão, log e pasta local | humano | sim |
| `test_local.js` | Servidor HTTP local mínimo para testar o site | humano | **não** (untracked) |
| `assets/portal.svg` | Arte gráfica do site | humano | sim |
| `css/style.css`, `css/layout.css` | Estilo e layout do site | humano | sim |
| `js/main.js` | Motor do site multi-herói: carrega JSON, monta grade de dias, paginação, dock de leitura | humano | sim |
| `audio/manifest.json` | Mapa `herói → dia → arquivo de áudio` | `scripts/tts/narrate.py` | sim |
| `audio/<herói>/dia_NN.mp3` | Narração em áudio de cada dia | `scripts/tts/narrate.py` | sim |
| `audio/test_samples/*.mp3` | Amostras de voz usadas para calibrar a narração | humano | **não** |

> **`publish_daily.py` — lista de caminhos.** Publicáveis: `data/**` (`.json`, `.md`), `css/**` (`.css`),
> `js/**` (`.js`), `scripts/**` (`.py`, `.md`), `skills/**` (`.md`, `.py`, `.json`), `docs/**` (`.md`),
> `automato/**` (`.py`, `.md`, `.json`), `audio/**` (`.json`, `.mp3`, `.wav`, `.ogg`, `.m4a`) e um
> conjunto fixo de arquivos da raiz. **`maquina/**` e `docs/*.json` não entram** — são preservados fora
> da revisão. A lista também bloqueia qualquer caminho com parte iniciada por `.`, e as pastas
> `local`, `work`, `node_modules`, `__pycache__`, `test_samples`.

---

## 2. `data/` — catálogo e campanha

### 2.1 Catálogo e legado de topo

| Caminho | O que é | Observação |
| --- | --- | --- |
| `data/heroes.json` | Catálogo de heróis do site: identidade resumida, runa, avatar, cores, cartões e `quick_stats` | **derivado** de `hero.json` por `sync_hero.py` |
| `data/posts.json` | Crônicas agregadas (formato do site) | derivado/legado |
| `data/identidade.md`, `data/evolucao.md`, `data/conhecimento.md` | **Duplicatas exatas** dos arquivos de `data/heroes/antigravitus/` | ⚠️ legado do layout de um único herói; ao atualizar, atualize o arquivo do herói, não estes |

### 2.2 `data/heroes/<id>/` — arquivos de campanha

| Caminho | O que é | Quem escreve | Versionado |
| --- | --- | --- | --- |
| `hero.json` | Identidade/apresentação: nome, título, runa, avatar, citação, perguntas, cartões, `evidence_policy` | agente (campos de apresentação) + `sync_hero.py` (cartões) | derivado em parte |
| `state.json` | **Último estado REGISTRADO**: nível, raça/classe mecânica, vitais, XP, ouro, atributos, armadura, habilidades, equipamento, inventário, localização, `as_of` | agente, com fonte | sim |
| `ficha.md` | Ficha legível derivada de `state.json` + `missoes.json` | `sync_hero.py` | **derivado** |
| `posts.json` | Crônicas por **dia** (Season 01): título, data, conteúdo, referências | `add_day.py` | sim |
| `ciclos.json` | Resumos de **blocos de dez dias** encerrados | agente (consolidação) | sim |
| `temporadas.json` | Catálogo de temporadas: modelo (`dias`/`capitulos`), intervalo, status, obra | `add_chapter.py`/agente | sim |
| `capitulos.json` | **Season 02+**: tomos e capítulos com `goal`, `parts`, `content`, `status`, `days` | `add_chapter.py` | sim |
| `missoes.json` | Missões oficiais, autoquests, investigações e intenções pessoais, com status, evidência e próximo passo | agente | sim |
| `missoes.md` | Guia **editorial** de leitura das missões; evidências e lacunas | agente | sim |
| `events.json` | Fatos documentais selecionados, com `source_kind` e referências (não é transcrição bruta) | agente | sim |
| `conhecimento.md` | Saber acumulado: rotas, economia, ameaças, armadilhas — separando observação, interpretação e dúvida | agente | sim |
| `identidade.md` | Matriz de identidade viva: motivações, contradições, voz | agente (orientação, não crônica) | sim |
| `evolucao.md` | Log de evolução da personagem apoiado nos acontecimentos | agente | sim |
| `diretiva_de_jogo.md` | **Regras de como jogar** (checklist, combate, economia, DT, método de automação, diretivas do autor) | autor via agente | sim |
| `mapa.json` | **Mapa curado**: salas (id, nome, camada, zona, risco, coords, saídas) e camadas do mundo | agente | sim |
| `mapa_vivo.json` | Levantamento **digerido** dos transcripts: grafo, arestas verificadas, fronteiras, resumo | `automato/acoes/digerir_mapa.py` (+ `fundir_mapa.py`) | **derivado** |
| `mapa.md` | Mapa em prosa — **histórico**, parado no Dia 60; **não é a fonte de verdade** | agente (histórico) | sim |
| `itens.md` | Tabela de itens: quem vende o quê, por quanto, com ID por item e por oferta | `automato/rotinas/mercado.py` + agente | sim |
| `npcs.md` | Compêndio de NPCs: comércio, diálogos, requisitos de quest | agente | sim |
| `monstros.md` | Bestiário: monstros e o que se sabe deles (irmão de `npcs.md`; a separação importa) | agente | sim |
| `notas_editoriais.md` | Separa **decisão do autor** de **fato do servidor** (ex.: a âncora do Dia 100) | agente | sim |
| `plano_aventureira.md` | Próximas decisões possíveis, como intenções (sem desfecho garantido) | agente | sim |
| `plano_capitulo_0N.md` | Plano operacional de um capítulo: missões, rotas, ferramentas, passos de execução | agente | sim |
| `capitulo-0N-fecho.md` | Texto do **fecho** do capítulo (crônica de encerramento) | agente | sim |
| `andarilho_e_novatos.md` | Compilação de **textos literais** de missões/eventos, sem interpretação embutida | agente | sim |
| `evidence/<dia>.json` | **Evidência estruturada** do dia: `agent`, `day`, `source_kind`, `note`, documentos | agente | sim |
| `observacoes/*.md`, `observacoes/*.json` | Notas curtas do que o MUD informou na sessão | agente | sim |

### 2.3 `data/heroes/_template/`

`identidade.md`, `ficha.md`, `evolucao.md`, `conhecimento.md`, `mapa.md`, `missoes.md` — modelos usados por
`create_hero.py`. Todos declaram explicitamente que **nenhum acontecimento foi registrado**; o rascunho
termina quando a primeira crônica real é gravada.

---

## 3. `docs/` — método e pesquisa

| Caminho | O que é |
| --- | --- |
| `docs/agentes/` | **Este conjunto**: guia de agentes, arquitetura, boas práticas, glossário, mapa de consulta, registro de evolução |
| `docs/rotinas.md` | Proposta e catálogo das rotinas de trabalho e das camadas (visão documental; a implementação canônica é `automato/`) |
| `docs/season_capitulos.md` | Modelo de Temporadas, Tomos e Capítulos: conceitos, arquivos, formato e regra de publicação |
| `docs/expedicao_modular.md` | Expedição modular V2: como as peças se encaixam, contratos das ações, vigilância, repouso |
| `docs/expedicao_comandos.md` | Recorte técnico de comandos essenciais (consultas de 15/10/2026) para o executor modular |
| `docs/expedicao_esgotos_dia95.md` | Aplicação do motor modular aos Esgotos de Midgaard (Dia 95+): fluxo, contornos, definição de pronto |
| `docs/expedicao_grebolius.json` | Configuração de expedição do herói (modo, alvos de comida, tetos de comando/tempo, melee verificado) |
| `docs/expedicao_legado.json` | Manifesto do modo Dungeon V1 preservado: origem, status `legacy`, hashes dos arquivos |
| `docs/circlemud/00-afirmacoes-e-validacao.md` | **Como ler os níveis de confiança** das afirmações sobre o CircleMUD e o protocolo de validação |
| `docs/circlemud/01-comandos.md` | Comandos do CircleMUD 3.x: afirmações verificáveis |
| `docs/circlemud/02-navegacao.md` | Movimento, setores, portas, `look`/`exits`, paginação e fuga |
| `docs/circlemud/03-magias.md` | Números do motor para magias (para validar no DeBo) |
| `docs/circlemud/04-especiais-easter-eggs.md` | Special procedures, subsistemas e easter eggs |
| `docs/circlemud/05-mundo-padrao-vs-mapa.md` | Mundo padrão do CircleMUD vs. o mapa do DeBo (zonas) |
| `docs/circlemud/06-evidencias-debo.md` | O que já foi observado no servidor real |
| `docs/circlemud/07-mobs-e-esgoto.md` | Mobs dos esgotos: nível, HP, dano e "para que nível é o esgoto" |
| `docs/circlemud/08-combate-e-progressao.md` | Matemática de combate e progressão do CircleMUD 3.1 |
| `docs/circlemud/09-esgoto-na-pratica.md` | O esgoto na prática no DeBo: mobs equivalentes, nível que limpa |

---

## 4. `maquina/` — referência técnica do MUD

> Camada do **operador**, não da personagem. Conhecer isto não concede habilidade, lembrança ou
> descoberta à aventureira.

| Caminho | O que é |
| --- | --- |
| `maquina/README.md` | Índice e **graus de confirmação** (importado → listado → documentado → executado → divergente) e rotina de TIP |
| `maquina/dicionario_comandos.md` | Seleção curta dos verbos úteis, orientada pelo `commands` e pela ajuda atual |
| `maquina/comparacao_commands.md` | Diferenças CircleMUD × DeBo que mudam decisões |
| `maquina/commands.md` | Os 99 verbetes originais de `commands.hlp`, com índice |
| `maquina/info.md` | Os 19 verbetes de `info.hlp` |
| `maquina/spells.md` | Os 44 verbetes de `spells.hlp` (não é ficha de magias aprendidas) |
| `maquina/historia_mundo.md` | Texto integral da história do mundo, sem marcas de paginação |
| `maquina/verificacoes.md` | O que foi executado, observado, corrigido ou continua incerto — **onde se registra correção de referência** |
| `maquina/tips.md` | Dicas capturadas, interpretação e aplicação prática |
| `maquina/aprendizados-cacada-92-93.md` | Estudo comparativo de armas/magias/equipamento/saque (amostra pequena) |
| `maquina/fontes.json` | Manifesto de fontes: origem, hashes, quantidade de verbetes e tratamento dos anexos |
| `maquina/evidencias/consulta_2026-10-15.json` | Respostas preservadas da consulta técnica de 15/10/2026 |

---

## 5. `automato/` — o motor de jogo

### 5.1 Documentação do motor

| Caminho | O que é |
| --- | --- |
| `automato/README.md` | Arquitetura das camadas, contrato das rotinas, invariantes de segurança, **lições de campo** e diretivas do autor |
| `automato/CHANGELOG.md` | Versões do motor (MAIOR muda contrato das rotinas, MENOR acrescenta camada/rotina, CORREÇÃO conserta) |
| `automato/DECISOES.md` | Cada mudança com **por que**, **o que**, **custo** e próximo desafio |
| `automato/verificar.py` | Autoexame: ambiente, core, driver, runtime, conhecimentos referenciados, rotinas, documentação |
| `automato/rotina.log` | Saída das rotinas | 

### 5.2 `automato/nucleo/` — o núcleo

| Caminho | O que é |
| --- | --- |
| `nucleo/config.py` | **O único lugar** de configuração do motor: caminhos do herói, caminhos de runtime, limites (`LIMITE_REPETICAO`, `LIMITE_TEMPO`, `RESERVA_OURO`, `VIDA_MINIMA`), magias, parâmetros do batedor, relógio do jogo, `TITULOS_LABIRINTO`, `RISCO_A_EVITAR` |
| `nucleo/base.py` | Infraestrutura das rotinas: `run()`, navegação por checkpoints/marcos, `voltar_ao_templo()`, injeção da guarda |
| `nucleo/guarda.py` | **Guarda de repetição**: mesma resposta 3× seguidas (só assinaturas de problema) → `recall` + `save` + saída 9 |
| `nucleo/inventario.py` | Leitura de bolsa/cantil desconfiando de resposta corrompida: a resposta precisa se identificar; `None` não é zero |
| `nucleo/driver/debo_bot.py` | Cliente Telnet do DeBo (CircleMUD 3.x): thread de recepção, desfragmentador IAC, reconstrução UTF-8, vitais assinados, classificação de estado, sanitização de credenciais, `term 200 80` no login (mata o paginador que gerava falso MORTA) |
| `nucleo/driver/parsers.py` | Funções **puras** de parsing (Zero-Network): vitais, sala, saídas, estados, confirmação de `save` |
| `nucleo/driver/live_daemon.py` | **Sessão viva única** em `127.0.0.1:14888`, com token obrigatório, log por sessão e transcrição JSONL; verbos `_PING`, `_STATUS`, `_RESYNC`, `_CLOSE`, `_RAW` |
| `nucleo/driver/play.py` | Cliente IPC de linha de comando para o daemon |

### 5.3 `automato/camadas/` — vigilância, cuidado e recarga

| Caminho | Papel | Contrato |
| --- | --- | --- |
| `camadas/vigia.py` | **OBSERVA** — lê a cauda do log e o `_STATUS`; nunca manda comando ao jogo | diagnósticos `OK/FOME/SEDE/VIDA_BAIXA/MANA_BAIXA/MORTA/TRAVADO/SEM_SESSAO` |
| `camadas/cuidar.py` | **CUIDA** — em campo: come, bebe, veste; nunca vai à cidade | saída `0` resolvido, `1` não resolveu, `2` precisa recarregar |
| `camadas/prepara.py` | **RECARREGA** — a ida à cidade: padaria, fonte, banco, sono; decide por **estoque**. Saca para comprar (`sacar_para_comprar()`, alvo `SAQUE_PARA_COMPRAR`) e revisa a Sala de Doações (`revisar_doacoes()`, critério empírico pelo `score`; `--sem-doacoes` desliga) | saída `0` reposto/nada a fazer, `1` falhou |
| `camadas/trabalhar.py` | **DESPACHA** — `--rotina X` carrega `rotinas/X.py` e chama `executar()`; `--listar` mostra o catálogo | — |
| `camadas/turno.py` | **ENCARREGADO** — vigia → cuidar → (prepara) → rotina → vigia a cada 60 s; mata a rotina se o vigia acusar problema | — |

### 5.4 `automato/rotinas/` — trabalhos de ponta a ponta

| Caminho | O que faz | Estado |
| --- | --- | --- |
| `rotinas/milharal.py` | Caça os invasores do milharal (missão *Problemas Agrícolas*), com trajeto de bosque verificado por marco | funcional |
| `rotinas/esgoto.py` | Reconhece os esgotos sob o Laboratório dos Magos sem entrar em luta desfavorável | em teste |
| `rotinas/cartografa.py` | **Modo batedor**: levanta salas novas sem travar combate; só anda por direção anunciada em `exits`; fome/sede/arranhão abortam | funcional |
| `rotinas/mercado.py` | Auditoria de comércio: rota por BFS a partir da sala real, `visible` antes de `list`, grava a tabela de preços | funcional |
| `rotinas/_suspensas/xadrez.py` | Coleta/venda de armaduras de peão | **suspensa** por diretiva do autor (Dia 150) |
| `rotinas/_suspensas/LEIA-ME.md` | Por que a rotina foi suspensa e o que entrava na conta | — |

### 5.5 `automato/acoes/` — ações pontuais

| Caminho | O que é |
| --- | --- |
| `acoes/mapear.py` | Anda uma sequência de passos imprimindo **cada** sala (a ferramenta que a doutrina exige antes de automatizar) |
| `acoes/ressuscitar.py` | Caminho de volta após a morte (porta do Paraíso/Inferno → Purgatório → Fonte da Vida) ⚠️ o cabeçalho do arquivo ainda diz "farm_armaduras.py": **docstring desatualizada**, o código é de ressurreição |
| `acoes/digerir_mapa.py` | Reconstrói o mapa a partir dos `transcript_*.jsonl`, com identidade de sala por **posição no grafo**; aceita `--glob` **repetível** (precisa cobrir todo o corpus — recorte encolhe o mapa) |
| `acoes/fundir_mapa.py` | Absorve o levantamento no mapa curado de forma **idempotente** (curado nunca é sobrescrito; a camada `levantamento` é refeita a cada rodada), com `ALIAS_CAMINHADA` e `ARESTAS_VERIFICADAS` |
| `acoes/encontrar_fazendeiro.py` | Busca o fazendeiro nos cômodos da casa e entrega a missão |
| `acoes/falar_fazendeiro.py` | Navega até a casa da fazenda e dialoga com o fazendeiro |

### 5.6 `automato/runtime/` — segredos, logs e transcrições (**não versionado**)

| Caminho | O que é |
| --- | --- |
| `runtime/.controller` | Token do driver (JSON com `owner` e `token`) |
| `runtime/.mud_pass` | Senha do MUD (alternativa: variável de ambiente `MUD_PASS`) |
| `runtime/session_live_dia<dia>_<carimbo>_<id>.log` | Log da sessão ao vivo — é o que o vigia lê |
| `runtime/transcript_*.jsonl` | Transcrição fiel da sessão; insumo de `digerir_mapa.py` |
| `runtime/cartografa.jsonl`, `runtime/mercado.jsonl` | Saídas estruturadas das rotinas correspondentes |

---

## 6. `scripts/` — ferramentas documentais e de expedição

| Caminho | O que é |
| --- | --- |
| `scripts/check_project.py` | **Validador documental**: tipos, vitais, wimpy, estado, metadados, referências, missões, salas e saídas, totais, datas de consolidação. Não certifica mecânica nem estado ao vivo |
| `scripts/sync_hero.py` | **Sincronizador**: gera ficha, cartões locais e entrada no catálogo a partir do último estado documentado; `--check` valida sem escrever |
| `scripts/run_offline_tests.py` | Runner unificado **Zero-Network** das suítes + gerador do relatório HTML de auditoria |
| `scripts/test_check_project.py`, `scripts/test_sync_hero.py` | Testes dos validadores/sincronizador |
| `scripts/test_fixtures/` | Fixtures de herói usadas pelos testes |
| `scripts/expedition_runner.py` | Entrada do **motor de expedição modular V2**; prévia por padrão, execução ao vivo exige `--live` e `MUD_PASS` |
| `scripts/expedition/models.py` | `Result`, `Status`, `Vitals`, `Supplies`, `Config`, `PROFILES` |
| `scripts/expedition/actions.py` | Ações: observar, localizar, ambientar, mover, lutar, recuperar, saquear, acampar |
| `scripts/expedition/engine.py` | `Travel` (ponto A→B) e `Expedition`; rota nunca autoriza sequência cega de passos |
| `scripts/expedition/policy.py` | Política de recursos: reservas de HP/mana/MV, `can_work`, decisão de saque |
| `scripts/expedition/observations.py` | Parsing puro: prompt de vitais, direções, sala, saídas nomeadas, recusas, sinais de combate/fuga |
| `scripts/expedition/adapters.py` | `ReplayTransport` (determinístico, sem socket) e `LiveTransport` |
| `scripts/expedition/guardian.py` | `ReactionGuard`: watchdog por tempo ocioso com trava única de dono dos comandos |
| `scripts/expedition/knowledge.py` | `CommandBook`: lê o dicionário de ajuda vivo; não promove manual a comando testado |
| `scripts/expedition/actions.py` … | (ver acima) |
| `scripts/tts/narrate.py` | CLI de narração: transforma dias/capítulos em capítulos de **áudio-livro** (`--hero`, `--day`, `--all`, `--preview`) |
| `scripts/tts/engine.py`, `scripts/tts/preprocessor.py` | Motor de TTS e pré-processamento prosódico do texto |
| `scripts/local/**` | **Legado local, fora do git.** Histórico de scripts por dia (`play_dia*.py`, `session_dia*.txt`, `transcript_*.jsonl`), o antigo driver e a suíte de mocks. Nada essencial depende dele; `digerir_mapa.py` ainda lê transcripts daqui quando existem |

---

## 7. `skills/` — método reutilizável

| Caminho | Quando usar |
| --- | --- |
| `skills/mud-ciclo-diario/SKILL.md` | Sessão autorizada no MUD e reconciliação de registros: referências da máquina, tips, evidência, crônica |
| `skills/mud-capitulo/SKILL.md` | Conduzir a Season 02+: abrir capítulo com objetivo, salvar partes, fechar por meta cumprida |
| `skills/mud-expedicao-modular/SKILL.md` | Conduzir pelo executor modular V2 (localizar → preparar → trânsito → explorar → recuperar → repousar) |

---

## 8. Pastas não versionadas

| Caminho | O que é |
| --- | --- |
| `.agents/teamwork/` | Coordenação entre agentes. `ORIGINAL_REQUEST.md` (pedido original), `<agente>/{DISPATCH,BRIEFING,progress,handoff}.md` (incumbência, contexto, progresso, entrega) e artefatos de projeto (`PROJECT.md`, `plan.md`, `GATE_STATUS.md`). **Ignorado pelo git**: é histórico de trabalho, não documentação publicada |
| `scripts/local/` | Execução local e legado (ver §6) |
| `automato/runtime/` | Segredos, logs e transcrições (ver §5.6) |
| `__pycache__/`, `.pytest_cache/` | Artefatos de execução |

---

## 9. Conceitos do domínio

### 9.1 Estrutura da obra

| Termo | Significado |
| --- | --- |
| **Dia** | Unidade da Season 01: uma entrada em `posts.json`, com fonte e evidência |
| **Ciclo** | Bloco de **dez dias já encerrados**, resumido em `ciclos.json`. Plano futuro não é ciclo |
| **Temporada (season)** | Agrupa a obra de um herói. S01 por dias; S02+ por capítulos |
| **Tomo** | Volume que agrupa **dez capítulos**. O Tomo I cobre os capítulos 0 a 10 |
| **Capítulo** | Unidade de objetivo e de publicação da S02+; tem `goal`, `parts`, `content` e fecha por meta |
| **Prólogo (capítulo 0)** | O primeiro capítulo do Tomo I: reúne a temporada anterior |
| **Parte (`parts`)** | Trecho salvo a cada sessão dentro de um capítulo aberto |
| **Fecho** | Crônica de encerramento do capítulo (`capitulo-0N-fecho.md`) |
| **`kind`** | Tipo do capítulo: `prologo`, `missao`, `intervalo`, `reflexao`, `marco` |

### 9.2 Jogo

| Termo | Significado |
| --- | --- |
| **Autoquest** | Missão automática/repetível do servidor. Inicia quando o NPC fala primeiro e a personagem responde `sim`; o objetivo se revela no `score`. Não há como abandonar; **`quit` apaga o progresso** |
| **Quest oficial / investigação / intenção pessoal** | Três naturezas distintas registradas em `missoes.json`; não confundir intenção com tarefa concedida pelo servidor |
| **DT (armadilha mortal)** | `death trap`: mata na hora e pode destruir itens. Aviso: *"Você percebe que há algo perigoso por perto!"* → parar e voltar |
| **Wimpy** | Nível de covardia: a personagem foge automaticamente ao cair abaixo dele. Tem **teto de metade da vida máxima** e não salva de DT nem sempre de atordoamento |
| **Sala-marco** | Sala cujo nome/identidade confirma a chegada; a navegação correta é por marco, não por contagem de passos |
| **Labirinto homônimo** | Região com muitas salas de texto idêntico (202 no corpus). Identidade vem da **posição no grafo**, não do texto |
| **Fronteira** | Saída conhecida e ainda não aberta/percorrida — o que a cartógrafa prioriza |
| **`risk_code`** | Classe de risco da sala no `mapa.json`; `RISCO_A_EVITAR` (`danger`, `high`, `fatal`, `critical`) define o que a rota evita |
| **Camada (`layer`)** | Grande divisão do mundo no mapa: superfície/Midgaard urbana, novatos, esgotos, etc. |
| **Santuário / Templo** | Âncora do herói: `recall` é barato/grátis até certo nível; toda rotina parte e volta para lá |
| **Invisibilidade** | Proteção que **bloqueia comércio**; hoje é opcional e não é a proteção padrão — a proteção vem de escolher a rota |
| **Encarnação** | Ciclo de vida do personagem no MUD, citado em requisitos de itens e magias |
| **Grau / honorífico** | Título exibido no `score`/perfil (ex.: "o Aprendiz de Mago") |

### 9.3 Motor

| Termo | Significado |
| --- | --- |
| **Rotina** | Trabalho que o herói sabe fazer de ponta a ponta; parte do Templo, trabalha, volta e salva |
| **Camada** | Responsabilidade isolada do motor: observar (vigia), cuidar (campo), recarregar (cidade) |
| **Turno** | Execução supervisionada de uma rotina com vigia a cada 60 s |
| **Guarda de repetição** | Mecanismo que interrompe o robô após 3 respostas idênticas de **problema** (comandos benignos não disparam) |
| **Modo batedor** | Perfil de mapeamento: invisibilidade, evasão total de combate, zero engajamento, piso de vida alto |
| **Driver / daemon** | Processo que mantém a sessão única com o MUD e atende clientes por IPC na porta 14888 |
| **IPC / token** | Protocolo local `"<token>\n<comando>"`; o token vive em `runtime/.controller` |
| **Transcript** | Registro fiel em JSONL de uma sessão; insumo do digestor de mapa |
| **Expedição modular (V2)** | Motor alternativo orientado a ações (observar, mover, lutar, recuperar, acampar) com prévia offline por padrão |

---

## 10. Campos de JSON recorrentes

| Campo | Onde aparece | Significado |
| --- | --- | --- |
| `schema_version` | quase todos | versão do formato do arquivo |
| `hero_id` | arquivos do herói | identificador do herói |
| `as_of` | `state.json` | `day`, `verification`, `live_verified`, `source` — quando/como/de onde veio o estado |
| `verification` | `state.json`, `missoes.json` | natureza da conferência (`live`/`documental`) e dia dela |
| `source_kind` | `events.json`, referências | `live` (sessão observada) ou `documental` (reconstrução) |
| `evidence` / `document` / `note` | referências de crônica e evento | fonte exigida para registrar um fato |
| `evidence_policy.legacy_through_day` | `hero.json` | até que dia o legado é aceito **sem** evidência estruturada |
| `record_status` | `hero.json` | `draft` = rascunho sem observação real |
| `inventory.pending_verification` | `state.json` | item visto no passado cuja posse atual é incerta |
| `risk_code` | `mapa.json` | classe de risco da sala |
| `layers[]` / `rooms[]` / `exits{}` | `mapa.json` | camadas, salas e saídas (a chave da saída é **convenção de arquivo**, não comando a enviar) |
| `goal`, `parts`, `content`, `closed_on_day` | `capitulos.json` | meta, trechos salvos, crônica final e dia de fechamento |
| `status` | missões, capítulos, temporadas | ver §11 |
| `agent` | evidência e registros | modelo/versão do agente autor |

---

## 11. Estados e códigos

| Domínio | Valores | Onde |
| --- | --- | --- |
| Missão / investigação | `discovered` (Descoberta), `active` (Ativa), `completed` (Concluída), `blocked` (Bloqueada), `deferred` (Adiada), `abandoned` (Abandonada) | `missoes.json` |
| Capítulo | `em_curso`, `concluido` | `capitulos.json` |
| Temporada | `em_curso`, `concluida` | `temporadas.json` |
| Herói em criação | `draft` | `hero.json` |
| Tarefa/expedição | `done`, `paused`, `rejected`, `fled`, `camped`, `disconnected` | `scripts/expedition/models.py` |
| Saída de `cuidar.py` | `0` resolvido · `1` não resolveu · `2` precisa recarregar | camadas |
| Saída de `prepara.py` | `0` reposto/nada a fazer · `1` falhou | camadas |
| Saída da guarda | `9` = guarda de repetição disparou (`recall` + `save`) | `nucleo/guarda.py` |
| Diagnóstico do vigia | `OK`, `FOME`, `SEDE`, `VIDA_BAIXA`, `MANA_BAIXA`, `MORTA`, `TRAVADO`, `SEM_SESSAO` | `camadas/vigia.py` |
| Estado do personagem no cliente | `in_game`, `in_combat`, `incapacitated`, `dead_or_menu`, `disconnected`, `unknown` | `nucleo/driver/parsers.py` |

---

## 12. Dívidas de documentação conhecidas

Registradas aqui para que ninguém as descubra por acidente:

1. **`automato/acoes/ressuscitar.py`** tem docstring de `farm_armaduras.py` — o conteúdo é de ressurreição.
2. **`data/{identidade,evolucao,conhecimento}.md`** são cópias byte a byte dos arquivos de
   `data/heroes/antigravitus/` — legado do site de um único herói.
3. **`data/heroes/grebolius/mapa.md`** se declara histórico e parado no Dia 60; a fonte viva é `mapa.json`.
4. **`maquina/**` e `docs/*.json`** estão fora da lista de caminhos publicáveis de `publish_daily.py`.
5. **`scripts/local/**`** (não versionado) ainda contém o driver antigo, centenas de `play_dia*.py` e
   transcripts que `digerir_mapa.py` também lê — a ferramenta canônica é a de `automato/`.
6. **`TEST_READY.md`** descreve suítes que vivem em `scripts/local/` (fora do git); o que é versionado é
   `scripts/run_offline_tests.py` e os `scripts/test_*.py`.
7. **`automato/CHANGELOG.md`** § "Próximas versões (planejado)" ainda usa os números `v1.1`–`v1.3`, já
   publicados como versões reais.
8. **`automato/verificar.py`** confere apenas `acoes/mapear.py` e `acoes/ressuscitar.py`, e exige um
   `plano_capitulo_03.md` fixo — não cobre `digerir_mapa.py`, `fundir_mapa.py`,
   `encontrar_fazendeiro.py`, `falar_fazendeiro.py` nem o capítulo em curso.
9. **`publish_daily.py`: `AGENTS.md`** foi incluído em `ROOT_FILES`; `maquina/**` e `docs/*.json`
   continuam fora da lista (pendência 1 acima).
