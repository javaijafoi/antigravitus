# Plano 018 — Sub-etapa de Gargamel Validada, Otimização de Caça (v1.6.9) e Rumo ao Nível 50

| | |
|---|---|
| **Criado em** | 2026-10-17 · Dia 156 |
| **Por** | Gemini 3.8 Flash (High) |
| **Herói** | grebolius |
| **Objetivo** | Acumular ouro para a poção aquosa (9.750 moedas) via caçador híbrido otimizado, comprar em Clariss (Jareth), entregar ao Alquimista para obter o jarro brilhante, entregar ao Minerador e resgatar Papai Smurf no Covil de Gargamel |
| **Sessão encerrada?** | sim — personagem em total segurança no Templo de Midgaard; HP 196/196, Mana 370/370, MV 144/144, wimpy 45, Nível 31 consolidado, save confirmado; live_daemon ativo |

---

## 1. Onde o objetivo está

A autoquest **`Uma Lição em Gargamel`** está no estágio mais avançado de sua história mecânica: a sub-etapa de entrega está **oficialmente ativada e reconhecida pelo servidor** no `score tudo`:
`[Autoquests em andamento] Uma Lição em Gargamel: Você deve entregar objeto ao personagem.`

A causa raiz das perdas de poção em sessões anteriores foi completamente resolvida:
1. O monólogo do Smurf Minerador em *O Fim Do Túnel* foi ouvido até a fala final (*"Estarei te esperando com o que preciso."*).
2. O diálogo de identificação na *Sala do Alquimista* foi executado manualmente em tempo real (`say Grebolius` -> *"Deixe-me adivinhar: você quer um jarro brilhante, certo?"* -> `say sim` -> solicitação formal da poção aquosa de Clariss).
3. A magia `sleep` de Nível 31 foi descoberta e treinada até **95% (perfeito)** na Mestre da Guilda dos Magos em *O Laboratório dos Magos*.
4. Todos os scripts de caça mais acionados foram auditados e otimizados na versão **v1.6.9** (>10% a >30% de melhoria de tempo, sem risco de flood).
5. O saldo de ouro subiu para **1.560 moedas** e a EXP para **6.365.184** (Nível 31 consolidado).

---

## 2. Estado exato

- **Nível:** 31 (Mago Elfo, 1ª encarnação).
- **EXP:** 6.365.184 (próximo nível: 7.000.000 — faltam 634.816 EXP).
- **Vitals:** HP 196/196, Mana 370/370, MV 144/144.
- **Wimpy:** 45 (estritamente mantido).
- **Armadura:** CA 138 (magia `armor` ativa com 47 horas de jogo restantes).
- **Ouro:** 1.560 moedas na mão (0 no banco).
- **Local:** Templo de Midgaard (ponto seguro de retorno).
- **Autoquests em andamento:** `Uma Lição em Gargamel: Você deve entregar objeto ao personagem.` (validada ao vivo).
- **Equipamentos:** Coroa da Rainha Branca, Armadura da Torre Negra, Espada Curta, Escudo, Manto de Pano, Cinturão de Rodeio, Rosário, Luvas e Calça de Couro, Mochila de Pellinore.
- **Suprimentos:** Mochila de Pellinore com pães recheados, cantil cheio de água cristalina, pergaminho de sabedoria.

---

## 3. O que já foi descoberto

1. **Validação Estrita da Sub-etapa (Invariante 13):**
   - No MUD DeBo, ter a quest listada em `[Autoquests em andamento]` NÃO significa que o NPC alvo aceitará a entrega. É obrigatório que o `score tudo` exiba a instrução textual exata: `Você deve entregar objeto ao personagem.` Sem essa instrução, qualquer entrega (`give`) é tratada como doação avulsa e o item é destruído!
2. **Magia Sleep de Nível 31:**
   - Localizada na Mestre da Guilda dos Magos em *O Laboratório dos Magos* (`e` do Bar dos Magos, na Praça do Templo). Treinada de 10% para 95%.
3. **Desempenho Otimizado dos Scripts de Caça (v1.6.9):**
   - `novatos.py`: eliminado `consider` redundante, saque direto em 1 comando (`get all corpo`), triagem e guarda de mochila em lote único pós-masmorra, roteamento de venda condicional (pula lojas se só houve moedas). Ganho: >30%.
   - `xadrez_v3.py`: eliminado `consider peao`, saque unificado e corrigida coleta no chão eliminando chamadas a corpos inexistentes. Ganho: >20%.
   - `milharal_v2.py`: removida checagem duplicada de combate em `matar()`. Ganho: >10%.
   - `cacador_hibrido.py`: sono de regeneração a cada 4s (evita 4-6s de ociosidade por descanso) e leitura direta de ouro. Ganho: >15%.

---

## 4. Os bloqueios, e o que já foi tentado

- **Bloqueio:** Saldo atual de 1.560 moedas; faltam 8.190 moedas para atingir as 9.750 moedas da poção aquosa.
- **Solução pronta:** O `cacador_hibrido.py` v1.6.9 acumula ~500-600 moedas líquidas por ciclo com respawns intercalados (Milharal + Novatos). Rodar 15-16 ciclos ou farmar Milharal V2 direto atinge a meta com segurança.

---

## 5. O próximo passo, e só ele

Executar ciclos de caça híbrida (`python automato/acoes/cacador_hibrido.py --ciclos 5 --meta-ouro 9800`) até atingir 9.750 moedas. Assim que atingir:
1. Comprar a poção aquosa em Clariss (`python automato/acoes/comprar_pocao.py`).
2. Ir à Sala do Alquimista (`open leste; e`), abater eventuais monstros na sala e conferir se `score tudo` mantém `Você deve entregar objeto ao personagem.`.
3. Emitir `give aquosa alquimista` e receber `o jarro brilhante`.
4. Ir ao Smurf Minerador em *O Fim Do Túnel* e entregar o jarro (`give jarro minerador`).
5. Resgatar Papai Smurf no Covil de Gargamel.

---

## 6. NÃO REPITA

1. **NUNCA usar `give` sem confirmar formalmente a sub-etapa no `score tudo`** (Invariante 13).
2. **NUNCA automatizar falas e diálogos com NPCs de missão por scripts cegos** (Invariante 14).
3. **NUNCA dar `quit`** enquanto a autoquest estiver ativa (apaga o progresso). Sempre `save`.
4. **NUNCA vender armaduras da Torre Negra ou peças com flag amaldiçoada.**
5. **NUNCA entrar em `Adentro do Milharal Destruído`** (sala perigosa de armadilha).

---

## 7. Ferramentas e comandos

- `python automato/acoes/cacador_hibrido.py --ciclos 5 --meta-ouro 9800`: laço híbrido otimizado de caça.
- `python automato/acoes/comprar_pocao.py`: viagem expressa até Clariss (Jareth) e compra da poção aquosa.
- `python scripts/sync_hero.py --hero grebolius --check`: sincronização dos derivados.
- `python scripts/check_project.py`: validador estrutural e de integridade.
- `python scripts/mandabala.py`: leitura unificada do plano vigente.
- `python scripts/devolutiva.py`: conferência obrigatória de cobertura contra o git.

---

## 8. Devolutiva técnica

| Descobri | Registrei em | O quê |
|---|---|---|
| mapa | `mapa.json` | PENDENTE (salas da guilda e rota de Jareth já registradas no mapa curado) |
| referência do servidor | `maquina/verificacoes.md` | Mensagem exata de sub-etapa de entrega de autoquest no DeBo: `[Autoquests em andamento] Uma Lição em Gargamel: Você deve entregar objeto ao personagem.` |
| fato do mundo | `conhecimento.md` §51 | Máquina de estados de autoquests: exigência de monólogo completo do Minerador e diálogo prévio do Alquimista antes do aceite de `give` |
| erro do motor | `automato/CHANGELOG.md` | Otimização v1.6.9 dos scripts de caça (`novatos.py`, `xadrez_v3.py`, `milharal_v2.py`, `cacador_hibrido.py`) com speedup de 10% a 30% |

---

## 9. Como encerrar a sua sessão

1. Confirmar Grebolius no Templo de Midgaard (`recall`, `stand`, `save`).
2. Gravar evidência com `agent` e dados estruturados (`evidence/dia156n.json`).
3. Atualizar `state.json` com os vitais e EXP exatos.
4. Rodar `python scripts/sync_hero.py --hero grebolius` e `python scripts/check_project.py`.
5. Criar o próximo plano numerado sequencial (`plano019.md`).
6. Rodar `python scripts/devolutiva.py` com zero falhas.
