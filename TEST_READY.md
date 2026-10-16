# TEST_READY — Infraestrutura de Testes MUD & Matriz de Auditoria Zero-Network

**Milestone**: M_TEST  
**Data**: 2026-10-15  
**Ambiente**: 100% Offline (Zero-Network)  
**Status**: Suíte Pronta e Operacional (87 Testes Totais, 33 na Nova Suíte MUD)

---

## 1. Comandos de Execução dos Testes

### 1.1 Execução Unificada com Relatório HTML
Executa todas as 4 suítes sob proteção estrita do `ZeroNetworkGuard` e gera `relatorio_auditoria_grebolius.html` na raiz do projeto:

```powershell
# Execução padrão (gera o relatório e retorna código de saída com status das pendências)
python scripts/run_offline_tests.py --lenient

# Execução estrita (exige 100% de aprovação para código de saída 0 — para Milestone M4)
python scripts/run_offline_tests.py
```

### 1.2 Execução Modular por Suíte

```powershell
# Nova suíte de automação MUD (Tiers 1 a 4)
python -m unittest scripts/local/test_mud_automation.py

# Execução específica por Tier da suíte MUD:
python -m unittest scripts/local/test_mud_automation.py -k TestTier1
python -m unittest scripts/local/test_mud_automation.py -k TestTier2
python -m unittest scripts/local/test_mud_automation.py -k TestTier3
python -m unittest scripts/local/test_mud_automation.py -k TestTier4

# Suíte pura de parsers existentes
python -m unittest scripts/local/test_parsers.py

# Suítes documentais e de integridade do projeto
python -m unittest scripts/test_check_project.py
python -m unittest scripts/test_sync_hero.py
```

---

## 2. Inventário e Contagem de Testes por Tier

| Suíte / Tier | Arquivo | Foco / Escopo | Total | Pass | Pendentes |
|:---|:---|:---|:---:|:---:|:---:|
| **Tier 1: Feature Coverage** | `scripts/local/test_mud_automation.py` | Casos positivos de fechamento, save canônico, vitais normais, estado in_game, recepção e Zero-Network | 9 | 9 | 0 |
| **Tier 2: Boundary & Corner** | `scripts/local/test_mud_automation.py` | IAC split (0xFF), -30hp, score negativo, save em combate/sono, recusa "ok", bloqueio `--quest`, sanitização | 17 | 14 | 3 (M2/M3) |
| **Tier 3: Cross-Feature** | `scripts/local/test_mud_automation.py` | Emboscada espontânea em background, fuga wimpy abortando rota, WinError 10054 (RST), save em combate | 4 | 4 | 0 |
| **Tier 4: Real-World Scenarios** | `scripts/local/test_mud_automation.py` | Ciclo completo mock (connect, login, look, move, save, close), logs sem sobrescrita, ausência de senhas | 3 | 1 | 2 (M3) |
| **Parsers Unit Tests** | `scripts/local/test_parsers.py` | Parsing de salas, saídas cardeais, recusas canônicas, export JSONL | 11 | 11 | 0 |
| **Project & Hero Checks** | `scripts/test_check_project.py` + `test_sync_hero.py` | Integridade documental, fichas, metajogo, sincronização e limites | 43 | 43 | 0 |
| **TOTAL GERAL** | — | — | **87** | **82** | **5** |

---

## 3. Matriz de Cobertura de Requisitos (R1 a R7)

- [x] **R1. Fechamento Confiável e Seguro da Sessão (T01)**
  - `test_t1_r1_lifecycle_normal_close`: Encerramento limpo sem travas ou descritores órfãos.
  - `test_t1_r1_save_confirmed_explicit`: Confirmação canônica estrita (`"Salvando os seus atalhos."` / `"Salvo."`).
  - `test_t2_r1_eof_drop_during_close`: Tratamento seguro de queda/EOF durante o fechamento.
  - `test_t2_r1_save_rejected_in_combat`: Rejeição de salvamento em combate.
  - `test_t2_r1_save_rejected_while_sleeping`: Rejeição de salvamento dormindo/descansando sem postura em pé.
  - `test_t2_r1_save_loose_ok_rejected`: Rejeição de falsos positivos com a palavra `"ok"`.
  - `test_t3_connection_reset_winerror_handled_cleanly`: Resiliência contra reset TCP (WinError 10054).

- [x] **R2. Interpretação Precisa de Vitais e Estados do Jogo (T02)**
  - `test_t1_r2_positive_vitals_parsed`: Extração de inteiros normais no prompt.
  - `test_t1_r2_state_classification_in_game`: Estado operacional `in_game`.
  - `test_t2_r2_negative_hp_in_prompt`: Extração de vitais negativos (`-30hp`).
  - `test_t2_r2_negative_hp_in_score`: Extração de HP negativo na tela de score (`-15`).
  - `test_t2_r2_incapacitated_state`: Classificação do estado `incapacitated` (HP <= 0 e > -10).
  - `test_t2_r2_dead_or_menu_state`: Classificação imediata de morte (`dead_or_menu`) e menu.
  - `test_t2_r2_missing_vitals_classified_unknown`: Tratamento de vitais ausentes como `unknown` (bloqueio de avanço cego).

- [x] **R3. Recepção Contínua e Buffer Assíncrono (T03)**
  - `test_t1_r3_stream_reception`: Recepção contínua e atualização dinâmica de vitais.
  - `test_t2_r3_telnet_iac_split_across_chunks`: Desfragmentação segura de sequências Telnet IAC (`0xFF`) divididas entre pacotes TCP.
  - `test_t2_r3_split_prompt_word_assembly`: Remontagem de prompts e palavras fatiadas no meio da transmissão.
  - `test_t3_spontaneous_mob_attack_updates_state`: Detecção assíncrona de emboscada espontânea com transição imediata para `in_combat`.

- [x] **R4. Preservação Histórica e Sanitização de Credenciais (T04)**
  - `test_t1_r4_session_logging_and_flush`: Gravação contínua e flush imediato para o disco.
  - `test_t2_r4_credential_sanitization_outgoing`: Censura de senhas em comandos enviados (`***REDACTED***`). *(Pendente M2)*
  - `test_t2_r4_credential_sanitization_incoming`: Censura de senhas ecoadas pelo servidor. *(Pendente M2)*
  - `test_t4_distinct_session_log_filenames_same_day`: Nomenclatura com identificador único/timestamp evitando sobrescrita no mesmo dia. *(Pendente M3)*
  - `test_t4_no_unmasked_credentials_in_session_output`: Garantia de zero ocorrências de senhas em texto claro nos logs finais. *(Pendente M3)*

- [x] **R5. Bloqueio Preventivo da Falsa Opção `--quest` (T05)**
  - `test_t1_r5_runner_dry_run_allowed`: Inicialização normal permitida na ausência da flag `--quest`.
  - `test_t2_r5_block_quest_cli_flag_pre_connection`: Recusa preventiva imediata com erro no `stderr` e código de saída != 0 antes de instanciar socket. *(Pendente M3)*

- [x] **R6. Integridade de Decisões Táticas e Retirada (T06)**
  - `test_t1_r6_successful_move_updates_room`: Movimento válido avança sala e atualiza rotas.
  - `test_t2_r6_movement_rejection_preserves_room`: Recusa de movimento (porta fechada, saída bloqueada) preserva a sala original sem avançar rota.
  - `test_t2_r6_combat_target_absence_not_victory`: Alvo ausente não contabiliza vitória em combate.
  - `test_t3_wimpy_panic_retreat_invalidates_route`: Fuga em pânico (`wimpy`) invalida a rota restante e força reorientação ambiental com `look`.

- [x] **R7. Restrição Offline e Validação Automatizada (T16)**
  - `test_t1_r7_zero_network_allows_localhost`: Permissão exclusiva para loopback (`127.0.0.1` / `localhost`).
  - `test_t2_r7_zero_network_blocks_external_ip`: Bloqueio ativo de qualquer socket externo sob `ZeroNetworkViolation`.
  - `test_t4_full_mock_session_lifecycle`: Ciclo de vida completo mockado operando 100% offline.
  - `relatorio_auditoria_grebolius.html`: Relatório visual e forense gerado na raiz com matriz de conformidade e logs verbatim.

---

## 4. Instruções para os Agentes dos Próximos Milestones

1. **Agente M2 (`debo_bot.py`)**:
   - Implementar método `sanitize_log(self, text: str) -> str` e aplicá-lo em todas as gravações e saídas de log.
   - Validar aprovação imediata de:
     - `test_t2_r4_credential_sanitization_outgoing`
     - `test_t2_r4_credential_sanitization_incoming`
2. **Agente M3 (`creative_runner.py`, `play_dia66.py`, `test_enc.py`)**:
   - Adicionar bloqueio preventivo no início de `main()`:
     ```python
     if args.quest:
         sys.stderr.write("Erro: A opção --quest está bloqueada preventivamente até a conclusão da interface de missões.\n")
         sys.exit(2)
     ```
   - Atualizar a geração de nome de log para incluir timestamp/UUID: `session_dia{day}_{timestamp}_{id}.log`.
   - Renomear `test_encoding()` em `test_enc.py` para `manual_check_encoding()` para evitar descoberta pelo pytest.
   - Validar aprovação imediata de:
     - `test_t2_r5_block_quest_cli_flag_pre_connection`
     - `test_t4_distinct_session_log_filenames_same_day`
     - `test_t4_no_unmasked_credentials_in_session_output`
3. **Agente M4 (Encerramento & Auditoria 100%)**:
   - Executar `python scripts/run_offline_tests.py` (modo estrito sem `--lenient`).
   - Confirmar 87 testes executados com 87 testes APROVADOS (100% Pass).
   - O arquivo `relatorio_auditoria_grebolius.html` será automaticamente regerado com badge verde **100% CONFORME (APROVADO)**.
