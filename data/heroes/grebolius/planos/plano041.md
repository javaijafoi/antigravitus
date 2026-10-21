# Plano 041 — Ajuda Mágica: achar o tomo na fonte original (Silverthorne, Pirâmide ou Torre da Magia)

| | |
|---|---|
| **Criado em** | 2026-10-20 · Dia 157 (sessão marcada Dia 158 nos registros) |
| **Por** | Claude Sonnet 5.5 (claude-sonnet-5-5) |
| **Herói** | grebolius |
| **Objetivo** | Capítulo 12: Ajuda Mágica (tomo para Lemin); Xeque-mate segue bloqueada no Rei |
| **Sessão encerrada?** | sim — Templo de Midgaard, save e sleep confirmados, `live_daemon` parado, sem quit; fechada por cota (5 h a 99%) |

Substitui o plano 040 (meu, não é editado).

## 1. Onde o objetivo está
Ajuda Mágica foi levada duas vezes ao passo "entregar objeto" (cadeia com Lemin refeita, 6 min) e caiu nas duas (reconexão do driver; `_CLOSE`). Nenhum item testado serve: o servidor recusa sem consumir com "não é o item correto ou você não é o dono original", o que sugere **fonte original** (loja ou mob), não doação. Xeque-mate segue bloqueada (Rei ~1.500+ de vida, raio ~70).

## 2. Estado exato
- **Local:** Templo de Midgaard, dormindo. **HP/mana:** 211/211 · 500/500 · nível 33 (faltam ~422 mil de EXP para o 34). CA 121, 157 com `armor`.
- **Ouro:** 31.769 (27.814 banco + 3.955 mão). **Pães:** 2 e cantil cheio (confirmar com `prepara.py --forcar`).
- **Vestido:** tudo identificado e limpo (túnica dourada CA 18, escudo de aço CA 35, cinturão de rodeio, Cruz Ansada, colar anti-DT, lâmina de ferro...).
- **Mochila (vestida):** 4 Lanças do Cavaleiro Negro, 4 Coroas da Rainha Negra, Armadura da Torre Branca (60 kg), veste de escamas (vida +20), bainha de Excalibur (nível 85), coleira, colar anti-DT reserva. Na mão: tomo druídico (não doa/vende), rosário reserva.
- **Autoquests:** nenhuma em andamento. Fonte: `state.json`; conferir com `score tudo`.

## 3. O que já foi descoberto
- **Cadeia Lemin (Lyon, `cap12_026`):** `say sim` abre; esperar "esperando a resposta"; `say Merlin`; `say sim`; `say sim` → "Você deve entregar objeto". Pedido: "um tomo de pergaminho bem grosso. Pode ser usado mesmo."
- **Descartados:** Pierre e Toulouse (Lyon, catálogos de dia, sem tomo; fecham à noite), Campanário e segundo andar de Notre Dame (sem tomo; armadilha mortal em `nd2_armadilha`; gárgulas atacam quem fica parado), Sala de Doações (tomo druídico = SPELLBOOK de druida, recusado), pergaminhos (dissolvem ao `recite`; `recitar` não existe, é `recite`).
- **Silverthorne** tem Loja do Escriba, Albernathy (espelho do `locate object`, nível 34) e teletransporte para Midgaard/Jareth/Sundhaven. Nenhum `help mapa` dá a rota de Midgaard (`automato/runtime/help_mapas_dia158.txt`).
- **Corcunda do Campanário** grita por Esmeralda: possível quest secreta (`corcunda-esmeralda` em `missoes.json`), só depois do tomo.
- **Mecânicas testadas** e pendentes: `conhecimento.md` §78 a §80. **Regras novas:** compras acima de 5% do ouro só com pedido (`diretiva_de_jogo.md` §25); `armor` no `prepara`; `turno.py` para caça/XP.

## 4. Os bloqueios, e o que já foi tentado
- **Rota a Silverthorne:** ausente no jogo; Estrada do Rei (mapeada até `cap12_033`) vai ao Castelo de Welmar. Não tentado: Portão Leste de Jareth (floresta), ler `help` de outras regiões já salvo no arquivo acima.
- **Tomo:** loja de Lyon, doações, pergaminhos testados. Não tentado: Escriba, livro de enigmas (zona 53, NPC; não atacar sem plano), Torre da Magia (`help mapa 29`).
- **Driver cai** perto de 1 h e derruba a missão: conferir `_STATUS` a cada poucos minutos.

## 5. O próximo passo, e só ele
Conectar (`mandabala.py`; `cota_claude.py --registrar` com `get_usage`; subir o `live_daemon` com `MUD_DAY=158 MUD_WIMPY=45`), `prepara.py --forcar --sem-doacoes`, `cuidar.py`, e ir à **Torre da Magia** (rota do `help mapa 29`, a partir do Centro de Jareth: leste até a Entrada da Floresta, norte, leste na Divisão da Trilha, Bosque Iluminado, 2ª passagem sul e 1ª leste, Pequeno Bosque, norte). Explorar só com `consider`, `where` e o explorador em Python (origem `mapear`), sem lutar; registrar salas no `mapa.json`. Se a Torre não tiver livro, a ordem padrão é: Estrada do Rei até o fim, depois o Portão Leste de Jareth.

## 6. NÃO REPITA
- Não comprar nada acima de 5% do ouro total sem pedir ao autor. Não vestir item sem `identify` antes.
- Não deixar a personagem parada numa sala com gárgula; nunca descer em `nd2_armadilha`; vida < 100 só `recall`.
- Não dar `give` fora da etapa; fala de missão à mão; não fechar a conexão com missão ativa.
- Não repetir o kite no Rei com o dano atual (§73, §76).

## 7. Ferramentas e comandos
Python: `C:\Users\peter\AppData\Local\Programs\Python\Python312\python.exe`. `play.py "<cmd>"`, `navegar.py --de <id> --para <id>`, `prepara.py`, `cuidar.py`, `xadrez_cascata.py`, `cota_claude.py`. Explorador DFS e varredura de maldição estão só no scratchpad da sessão (não commitados).

## 8. Devolutiva técnica
| Descobri | Registrei em | O quê |
|---|---|---|
| mapa | `mapa.json` | 14 salas: Campanário, segundo andar, armadilha mortal; Ponte Francesa com saída norte |
| referência do servidor | `maquina/verificacoes.md` | nada: tudo no conhecimento §77 a §82 |
| fato do mundo | `conhecimento.md` §77 a §82 | tomo, mecânicas, Silverthorne, itens identificados |
| erro do motor | `automato/CHANGELOG.md` | nada novo; `navegar.py` não cuida de fome (sugestão: chamar `cuidar`) |

## 9. Como encerrar a sua sessão
Siga `docs/agentes/PROTOCOLO.md` §3: `_CLOSE sleep` no Templo, evidência com `agent`, `python scripts/encerrar.py --agente "<modelo/versão>"`, preencher o plano 042, `python scripts/encerrar.py --agente "<modelo/versão>" --fechar --avanco sim|nao`.
