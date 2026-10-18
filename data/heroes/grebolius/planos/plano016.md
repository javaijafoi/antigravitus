# Plano 016 — Benchmark Xadrez V2 vs Milharal V2, Blindagem de Entrega de Itens e Rota Segura para o Nível 50

| | |
|---|---|
| **Criado em** | 2026-10-17 · Dia 156 |
| **Por** | Gemini 3.8 Flash (High) |
| **Herói** | grebolius |
| **Objetivo** | Benchmark do Xadrez V2 vs Milharal V2, blindagem da entrega de poções e rota limpa para conclusão de Uma Lição em Gargamel e Nível 50 |
| **Sessão encerrada?** | Sim — socket telnet fechado com segurança pelo servidor; processo live_daemon ativo em 14888 com estado salvo no Templo de Midgaard |

## 1. Onde o objetivo está
A meta do Capítulo 09 estabelecida pelo autor é dupla: **concluir a missão `Uma Lição em Gargamel`** e **avançar a personagem até o Nível 50**.
Nesta sessão:
1. **Gargamel está oficial e comprovadamente ATIVA no servidor:** Grebolius foi a *O Fim Do Túnel* sob o Poço Smurf e conversou com o *smurf minerador*, confirmando em `score tudo` o cabeçalho `[Autoquests em andamento]: Uma Lição em Gargamel`.
2. **Diagnóstico e Blindagem da perda da poção:** Descobriu-se que o Alquimista não entregou o jarro brilhante anteriormente porque *Limpando Monstros* estava ativa simultaneamente e o diálogo `say sim` acionou a quest repetível dele. Foi adicionada a Invariante 13 em `AGENTS.md`, Seção 19 em `diretiva_de_jogo.md` e Seção 46 em `conhecimento.md`, além de trava programática em `entregar_alquimista.py`.
3. **Desenvolvimento e Benchmark do Xadrez V2:** Criados `xadrez_v2.py` e `cacador_xadrez.py`. O benchmark de 3 rodadas provou que o Xadrez gera rajadas rápidas de ouro (~200 moedas/min com peões vivos, vendendo armaduras de peão a 150 e escudos a 200 no Armeiro), mas seca rapidamente pelo respawn lento. O Milharal V2 é 3x superior em EXP (~36k vs ~12k por rodada) para atingir o Nível 50.
4. Saldo vivo fechou em **2.936 moedas** (+1.100 na sessão) e EXP em **4.833.750** (+53.964 na sessão, restando apenas **166.250 para o Nível 30**).

## 2. Estado exato
- **Nível:** 29 (Mago Elfo).
- **Vida:** 182 / 182.
- **Mana:** 350 / 350.
- **Movimento:** 142 / 142.
- **Experiência:** 4.833.750 (próximo nível em 5.000.000; faltam 166.250 EXP).
- **Ouro:** 2.936 moedas na mão (0 no banco).
- **Alinhamento:** 274 (Bom).
- **CA:** 137 com Armor místico (+34, 43 horas restantes).
- **Localização:** `O Templo de Midgaard` (dormindo, save executado).
- **Inventário:** um cantil, a mochila de Pellinore, um pergaminho de sabedoria.
- **Dentro da Mochila:** 2 espadas do peão negro, 2 pães recheados, 2 chifres do minotauro, manto de pano, colar com pedra púrpura, pele do minotauro, bainha de Excalibur, Cruz Ansada, Cetro do Bispo Negro.
- **Processos:** live_daemon rodando na porta 14888 com token ativo em `.controller`. Socket DeBo desconectado em repouso.

## 3. O que já foi descoberto
- **Autoquest Gargamel:** O minerador precisa de iluminação (*"o jarro brilhante"*). O Alquimista exige *uma poção aquosa* vendida por Clariss na Avenida Floris de Jareth (9.750 moedas).
- **Conflito de Concorrência do Alquimista (§42.1):** O Novato Alquimista prioriza *Limpando Monstros*. Para receber o jarro brilhante, *Limpando Monstros* **NÃO PODE** estar ativa. O procedimento ótimo é juntar 9.800 moedas, dar `quit` intencional no Templo (reseta as quests ativas sem perder 1 moeda nem XP), reconectar o daemon, pegar apenas Gargamel no Minerador, comprar a poção em Clariss e entregar ao Alquimista.
- **Economia do Xadrez V2:**
  - `a armadura do Peão Preto`: vende por 150 moedas no Armeiro de Midgaard.
  - `um escudo`: vende por 200 moedas no Armeiro de Midgaard.
  - `a espada do Peão Negro`: vende por 40 moedas no Ferreiro de Midgaard.
  - Peões fogem em pânico com vida baixa: o burst ideal é `lightning bolt` (80 dmg) + `burning hands` (35 dmg).

## 4. Os bloqueios, e o que já foi tentado
- **Tentativa 1 (anterior):** Entrega de poção aquosa sem verificar status no servidor e com `say sim` no Alquimista. Resultado: poção consumida sem entrega do jarro brilhante.
- **Tentativa 2 (nesta sessão):** Deslocamento à Vila dos Smurfs e ativação formal de Gargamel com o Minerador. Resultado: 100% de sucesso, quest ativa confirmada em `score tudo`.
- **Tentativa 3 (nesta sessão):** Benchmark do Xadrez V2. Resultado: 4 peões abatidos, 500 moedas obtidas em 2.5 min; peões demoram a renascer na 3ª rodada.

## 5. O próximo passo, e só ele
Subir o saldo de 2.936 para 9.800 moedas (~16 rodadas no Milharal V2 via `cacador_milharal.py`, alternando com 1 rodada de Xadrez V2 caso os peões tenham renascido) — o que simultaneamente passará Grebolius pelo **Nível 30** rumo ao Nível 50 sob DoubleXP.

## 6. NÃO REPITA
- **NÃO** responder `say sim` ao Alquimista com a poção aquosa na mão se *Limpando Monstros* estiver aberta.
- **NÃO** tentar entregar poção sem checar `score tudo` antes (Invariante 13).
- **NÃO** pegar nem tentar vender `Armadura da Torre Negra` (amaldiçoada).
- **NÃO** atacar Cavaleiro Branco, Torre Negra, Rei ou Rainha no Tabuleiro de Xadrez.
- **NÃO** esquecer mantimentos: sempre conferir se há pão e cantil cheio antes de dormir para regenerar mana.

## 7. Ferramentas e comandos
- `python automato/acoes/cacador_milharal.py --rodadas 5 --meta-ouro 9800`: executa o farm autônomo no Milharal V2 com autoloot de moedas e abastecimento de comida/água.
- `python automato/acoes/cacador_xadrez.py --rodadas 2`: executa 2 rodadas rápidas no Tabuleiro de Xadrez com venda de armaduras/escudos no Armeiro.
- `python automato/acoes/comprar_pocao.py`: viaja até Clariss em Jareth e compra a poção aquosa por 9.750 moedas.
- `python automato/acoes/entregar_alquimista.py`: valida precondições e realiza a entrega segura da poção ao Alquimista.
- `python scripts/sync_hero.py --hero grebolius --check`: valida sincronismo dos derivados.
- `python scripts/devolutiva.py`: validação do protocolo de fechamento.

## 8. Devolutiva técnica
| Descobri | Registrei em | O quê |
|---|---|---|
| mapa | `mapa.json` | PENDENTE: 4 arestas de anéis de mão dupla dos esgotos documentadas em prosa no Dia 156 seguem abertas para reconciliação topológica futura |
| referência do servidor | `maquina/verificacoes.md` | PENDENTE: Nenhuma mensagem nova de servidor; comportamento de bolsas locais fixas de mercadores e respawn do xadrez mantidos |
| fato do mundo | `conhecimento.md` §46 | Protocolo de proteção contra perda de itens de autoquest e conflito de concorrência com Novato Alquimista; benchmark Xadrez V2 vs Milharal V2 |
| erro do motor | `automato/CHANGELOG.md` | v1.5: adicionada rotina xadrez_v2.py, cacador_xadrez.py, cacador_milharal.py e blindagem prévia de entrega em entregar_alquimista.py |

## 9. Como encerrar a sua sessão
- Salvar e dormir no Templo de Midgaard (`save`).
- Criar a próxima evidência `evidence/dia156m.json` caso jogue nova sessão.
- Atualizar `state.json` com os números reais e rodar `python scripts/sync_hero.py --hero grebolius`.
- Criar o `plano017.md` (append-only) com a devolutiva técnica preenchida.
- Executar `python scripts/devolutiva.py` e certificar-se de 0 falhas antes do handoff.
