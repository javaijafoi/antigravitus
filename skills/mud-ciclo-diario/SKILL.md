---
name: mud-ciclo-diario
description: "Continuar uma sessão autorizada do Devil's Bob MUD e reconciliar seus registros e crônicas, preservando evidências, continuidade e a doutrina de exploração de Grebolius. Não autoriza jogar nem publicar por si só."
---

# Devil's Bob MUD — sessão, memória e crônica

Use esta skill para uma sessão autorizada em `debomud.org:4000` ou para revisar os registros da campanha. Uma solicitação de edição de arquivos não autoriza jogar, enviar comandos ao servidor ou publicar. A skill orienta o método; os acontecimentos vêm das evidências da sessão e dos documentos identificados como fontes.

## 1. Evidência antes da prosa

Antes de escrever, separar:

- **Fato com fonte:** resposta do servidor ou acontecimento explicitamente registrado em documento. Uma crônica antiga é evidência documental, não uma transcrição de comando nem uma nova conferência ao vivo.
- **Crença da personagem:** interpretação, bravata, medo ou ambição presentes no relato. “Sou invulnerável” não comprova imunidade; diálogo não comprova aliança.
- **Plano ou hipótese:** ação pretendida, mecânica sugerida ou resultado possível. Não registrar como ocorrido, concluído ou confirmado.

Registrar primeiro o que aconteceu, a fonte e o grau de certeza em `data/heroes/<slug>/events.json`, conforme o esquema existente. Usar `source_kind=server_log` apenas quando houver resposta real do servidor; registros migrados de documentos usam `source_kind=document` e sua referência. Não inventar transcrições, horários ou comandos executados. Manter o evento e o dia de jogo distintos da data de revisão editorial.

Atualizar estado e missões com essas evidências antes de elaborar a crônica. Fonte ausente ou divergente pede uma pendência explícita, não uma cena de ligação inventada.

### Continuidade e voz

- Nunca acrescentar recompensa, diálogo, relação, promessa, deslocamento, perda de memória, vitória ou desfecho que não esteja sustentado pela sessão. Não concluir uma missão por ter ocorrido um combate próximo ao NPC.
- Preservar emoções e fatos das crônicas históricas. Só corrigir um acontecimento se uma fonte o resolver; enquanto não houver fonte, acrescentar nota editorial fora da voz da personagem. Não diagnosticar negação nem declarar trauma superado para reparar uma divergência.
- **Regra de Ouro dos Números (Desconhecimento Total da Ficha):** A personagem NÃO conhece nem menciona números de sua ficha mecânica. Ela NÃO sabe seus pontos de vida (HP), sua quantidade de mana (MP), seus pontos de movimento/estamina (MV), sua classe de armadura (AC), bônus de itens (+2E), dano numérico de armas/magias, percentuais de treino ou pontos de experiência (EXP/XP — terminantemente proibido disfarçar como "passos de maturidade" ou "passos de experiência"). **O MÁXIMO e ÚNICO número que Grebolius conhece e menciona é DINHEIRO** (moedas de ouro, prata e cobre tilintando nas algibeiras). Todo o restante deve ser percebido e narrado exclusivamente por sensações físicas e mágicas tangíveis: cansaço nos músculos, peso nas pernas, fôlego curto ou pleno, dor da carne ferida, frescor místico no peito, zumbido de eletricidade nas têmporas, firmeza da couraça nos ombros e precisão calejada do punhal.
- **Proibida a transposição literal de regras na voz da personagem:** Diretrizes de projeto (ex.: "orçamento de estamina", "evitar três passos", "reflexão de 9 dias", comandos como `save`, `autogold`, `autoquest`) JAMAIS devem ser descritas pela personagem como regras, disciplinas ou doutrinas inventadas. As mudanças de postura devem ser expressas de forma sutil, orgânica e psicológica: ela sente mais confiança, mais segurança, curiosidade, audácia, pragmatismo ou prudência. Mesmo nos dias de reflexão (terminados em 9), os pensamentos devem ser pessoais e existenciais, nunca formulados como regras de sistema ou métodos burocráticos.
- Descrever ações e sensações apoiadas no ocorrido, com espaço para humor, curiosidade, tensão e silêncio. Não exigir clímax, vitória épica, descoberta nova, número mínimo de cenas ou três combates. Preparação, bloqueio e recuo podem ser o resultado real de uma sessão.
- Uma sessão pode avançar uma pista ou descartar uma hipótese; não fabricar mudança de personalidade ou consequência emocional para cumprir uma cota narrativa.

## 2. Objetivo da expedição e risco

### Gatilhos para Descobrir Lugares Novos

A exploração de novas rotas, áreas desconhecidas ou desvios do itinerário habitual não deve acontecer por capricho. Ela deve estar fundamentada em pelo menos um destes três gatilhos:

1. **Experiência traumática recente:** Morte recente, fuga brutal no limite da vida (`wimpy`) ou colapso de plano. A personagem precisa clarear as ideias, digerir a queda e recalibrar o foco em espaço aberto antes de encarar o ambiente sufocante do trauma.
2. **Dois dias seguidos de tarefas repetitivas:** Sensação de tédio goblin, estagnação ou rotina monótona após 2 dias consecutivos fazendo a mesma tarefa/trajeto sem novidade.
3. **Marcos decenais do ciclo:** Dias redondos terminados em zero (10, 20, 30, 40, 50, 60, 70...) que exigem expansão intencional de horizontes e quebra de limites conhecidos.

### Fluxo de Conexão e Execução em Jogo

- **Cadência Operacional (Tempo Real vs. Script Autônomo):**
  - **Dias com final 5 e final 0 (5, 10, 15, 20, 25, 30, ...): Tempo Real (Interativo).** Nesses dias, jogar comando a comando via conexão interativa contínua (`live_session.py`), sem script enlatado da rota. A IA avalia cada resposta do MUD em tempo de execução, reagindo a salas, mobs, perigos, portas e oportunidades táticas ao vivo.
  - **Demais dias (finais 1, 2, 3, 4, 6, 7, 8, 9): Modo Script Autônomo (Batch).** Execução programada da rota para máxima eficiência de tokens e execução rápida, preservando a pausa tática para o agente assumir caso ocorra anomalia.
  - **Dias com final 9 (9, 19, 29, 39, ...): Reflexão Pessoal e Existencial.** O dia encerra um ciclo decenal e traz na crônica a reflexão psicológica/existencial da heroína, estritamente sem jargão de regras e sem números de ficha (apenas moedas de ouro).
- **Teto rígido de conexões:** No máximo **3 conexões** ao MUD por dia. É proibido fatiar o dia em 6, 7 ou 8 logins/logouts artificiais.
- **Fluxo contínuo automático:** Se as salas, rotas e saídas forem as esperadas para o plano do dia, o script avança normalmente e sem hesitação.
- **Gasto Ativo e Aproveitamento da Estamina (MV):** Os dias têm que ser proveitosos e a estamina deve ser gasta ao máximo no dia a dia, explorando e avançando. Andar em terreno padrão consome apenas 1 a 2 MV por passo; portanto, sessões curtas de 5 a 10 passos gastam quase nada e a regeneração passiva recupera tudo antes de dormir. A expedição deve gastar o fôlego ativamente (40 a 70 passos úteis por jornada) patrulhando setores, mapeando câmaras, caçando alvos ou viajando para comprar provisões.
  - **Avançar enquanto houver estamina:** A personagem explora, patrulha, mapeia e viaja continuamente enquanto seu fôlego estiver acima da reserva de segurança (`MV > 25-30`).
  - **Abate ou objetivo intermediário NÃO encerra o dia:** Matar um monstro ou cumprir uma etapa de missão NÃO significa ir dormir se a estamina ainda estiver alta. A aventureira segue ativa aproveitando o dia até esgotar a estamina planejada.
  - **Diferença entre Pausa Tática e Retorno Definitivo:**
    - **Pausa de Recuperação em Campo (HP/Mana):** Queda de HP (< 35) ou Mana (< 40) após combates NÃO exige retorno ao acampamento. A aventureira faz uma pausa tática (`rest` / sentar e vigiar) em sala limpa ou recua 1 passo para um cômodo seguro por 2 a 3 ticks (ingerindo pão ou água se necessário) para recuperar HP e Mana antes de retomar a marcha.
    - **Critérios para Rota de Retorno Definitivo e Encerramento do Dia:**
      1. A estamina diária atingir a margem de retorno seguro (`MV <= 25-30`), indicando que o fôlego do dia foi aproveitado ao máximo.
      2. Inviabilidade de recuperação em campo (ex.: perigo contínuo na área, veneno sem cura, emboscada grave ou ausência de sala segura para descansar).
      3. Mochila cheia de espólios valiosos que precisem ser guardados/vendidos.
      4. Anomalia crítica, jogador hostil ou bloqueio insuperável que imponha retirada.
- **Pausa tática diante de anomalia:** Se houver personagem jogador (player), NPC/mob inesperado fora da rota prevista, dano imprevisto ou bloqueio de saída: o script **NÃO desconecta**; ele pausa a marcha automática, mantém a conexão aberta e passa o controle para o agente. O agente assume e joga em tempo real até normalizar a situação. Uma vez normalizado, o agente decide entre **retomar o script original** ou **adaptar o restante do dia com um novo roteiro** (se a ocorrência alterou os recursos, a rota ou a meta), respeitando sempre o teto de até 3 conexões.

### Referência de Grebolius

- Mulher goblin **sem disfarce**, de classe mecânica **Mago**. “Ladra arcana” descreve astúcia e estilo, não furto, apunhalada especial ou habilidades de outra classe.
- `wimpy 13` é a configuração documental vigente para 52 HP máximos. A regra anterior de aproximadamente 25% é uma heurística, **não uma fórmula de fuga segura**: considerar dano por golpe, vida restante, mana, movimento e saída. Só alterar o valor no jogo durante sessão autorizada e registrar a resposta.
- Conferir `armor` antes do risco; custo, duração, efeito e renovação dependem do que o servidor mostrar. Não pressupor atividade contínua, AC imutável ou imunidade. O mesmo vale para `invisibility` e demais magias.
- Último acampamento documental: Laboratório dos Magos, Dia 60. Panteão dos Centenários é uma referência histórica de santuário. Sala limpa, porta fechada, mobília ou NPC conhecido não garantem segurança. Escolher descanso ou retorno conforme as condições observadas, sem tratar o santuário como fraqueza.
- Saldo documental de 1.051 moedas e seis treinos requer conferência. O catálogo antigo cobra 9.202 pelo pergaminho de retorno e 5.370 pela poção amarela; não planejar essas compras com o saldo registrado. Escolher treino e compra conforme necessidade, disponibilidade, preço, peso e requisitos atuais.
- O anel guardado no Dia 43 está ausente da ficha posterior. Posse, requisito de uso e bônus são pendências; não tratá-lo como equipado, perdido ou disponível sem conferir.
- Reino Livre e vingança contra a serpente são objetivos pessoais futuros. Procurar oportunidades que o mundo oferecer, sem criar seguidores, abrigo, acordos ou segredo da serpente. Confronto, decapitação e nível seguinte não são desfechos predefinidos.

## 3. Memória e documentos do projeto

Consultar a estrutura existente antes de editar. Para Grebolius:

| Arquivo | Responsabilidade |
| :--- | :--- |
| `state.json` | Estado estruturado com fonte, dia e indicação de conferência ao vivo. Migração documental mantém `as_of.live_verified=false` até haver conferência real. |
| `events.json` | Eventos com origem e certeza; distingue o que veio do servidor e o que foi consolidado de documentos. |
| `ficha.md`, `hero.json`, `data/heroes.json` | O gerador deriva ficha e `quick_stats` do estado e espelha o perfil no catálogo. O texto de identidade em `hero.json` é editorial: reconciliá-lo com `identidade.md` antes de sincronizar. |
| `missoes.json` | Tipo, estado, evidências, bloqueios e próximos passos das tarefas e objetivos. |
| `missoes.md` | Guia editorial complementar; manter títulos e estados coerentes com o JSON. |
| `identidade.md`, `plano_aventureira.md` | Orientação atual e possibilidades futuras, sem converter intenções em fatos. |
| `conhecimento.md`, `mapa.md`, `mapa.json` | Conhecimento e topografia com origem, riscos e incertezas; distinguir posição, acampamento e santuário. |
| `evolucao.md` | Histórico de instantâneos e interpretações de cada dia. Preservar entradas antigas; anexar reconciliação quando uma divergência continuar aberta. |
| `posts.json` | Crônicas baseadas na sessão; não preencher lacunas históricas por invenção. |
| `ciclos.json` | Resumos de dias já registrados. Planos futuros ficam no plano, não em resumo histórico antecipado. |

### Missões

Distinguir **tarefa oficial**, **investigação** e **objetivo pessoal**. Registrar descoberta, aceite, retomada, progresso e conclusão separadamente, com fonte e dia. Estados disponíveis: descoberta, ativa, adiada, bloqueada, concluída e abandonada, conforme o esquema do projeto. Toda entrada deve permitir saber o próximo passo verificável, o bloqueio e a condição de conclusão; objetivo ou recompensa desconhecidos ficam como desconhecidos.

Para Grebolius, “Limpando Monstros” foi descoberta no Dia 35, aceita no Dia 36 e retomada nos relatos do Dia 60. Isso não comprova um segundo aceite ou reinício. “Dicas Mágicas” tem início narrado no Dia 32. Vingança não é uma autoquest confirmada. Convite, conversa, doação ou morte de monstro não criam nova recompensa ou aliança por inferência.

### Fechamento e conferência

Quando uma sessão tiver ocorrido dentro do escopo autorizado:

1. Salvar no MUD com `save` e verificar a resposta. Escolher repouso e encerramento conforme segurança observada. Não declarar `save`, repouso ou local confirmado se a ação falhou ou a sessão foi interrompida.
2. Registrar evidências e atualizar estado, eventos, missões, mapa e conhecimento. Adicionar a crônica na convenção de IDs do herói; não reordenar silenciosamente arquivos históricos de outro herói.
3. Gerar os derivados de Grebolius com `python scripts/sync_hero.py --hero grebolius`. Conferir sem escrita com `python scripts/sync_hero.py --hero grebolius --check`.
4. Executar `python scripts/check_project.py`; resolver erros ou relatar a limitação restante. Validação estrutural não prova mecânicas do servidor nem coerência emocional.
5. Nos marcos de dez dias, consolidar somente o ciclo realmente ocorrido e atualizar identidade e mapa segundo novas evidências. Dias terminados em 9 podem incluir reflexão de método; usar `/learn` apenas se a ferramenta existir e couber no escopo, sem fingir sua execução.

### Publicação

Publicar somente quando o usuário tiver solicitado ou autorizado a publicação no contexto da tarefa e após a validação. Edição local não implica commit, push ou deploy. Revisar o diff, selecionar arquivos pertinentes por caminho explícito e preparar uma atualização completa; não usar `git add .` indiscriminadamente nem publicar arquivo por arquivo em estados intermediários. Preservar credenciais locais, sem alterar configuração global. Se publicação não estiver no escopo, entregar a revisão local com seu resumo.

## 4. Referência local de comandos e mecânicas

Estas referências provêm dos registros do projeto, não substituem a ajuda nem a resposta atual do servidor:

- **Portas:** `open north` abriu a passagem no Cruzamento no Dia 58. `open <direction>` pode servir para outras portas, mas bloqueio, tranca e requisito precisam de resposta local. Os registros anteriores anotam falhas com `abrir porta norte` e `open door north`.
- **Oeste:** usar `w`; o registro do cliente alerta que `o` pode acionar `order`.
- **Consumo e comércio:** `eat <comida>`, `drink <recipiente>`, `list`, `buy <item>`. Conferir item, preço e resposta.
- **Treino:** `practice <magia_em_ingles>`, por exemplo `practice 'burning hands'`, apenas se a magia estiver disponível e o treino for pertinente.
- **Autoquests:** `autoquest` e `ajuda autoquest`; `say sim` quando o NPC tiver feito um convite e a decisão for aceitar. Guardar o objetivo real e a mensagem de aceite.
- **Combate e espólios:** `cast 'magic missile' <alvo>`, `cast 'chill touch' <alvo>`, `cast 'burning hands' <alvo>`, `get all corpo` e `sac corpo` são referências anteriores, não uma sequência obrigatória. Conferir habilidade, mana, alvo e finalidade dos objetos antes de agir.
- **Inventário:** `put <item> mochila` organiza itens, sem comprovar redução do peso total. Preservar itens de missão ou de uso futuro até entender finalidade e requisitos; a tag `(+2E)` não basta para inferir um bônus ou nível exato.
- **Ticks e descanso:** 45–60 segundos, penalidades exatas de fome/sede e multiplicadores de `rest`, `sleep` ou mobília são hipóteses herdadas até medição ou ajuda do servidor. Não assumir que “sleep-ticking” evita emboscada. Comandos como `dormir cama` e `descansar banco` precisam de confirmação local.
- **Bot:** os registros anteriores indicam `.close()` para encerrar o socket de `DeboClient` e falha com `.disconnect()`. Conferir a implementação disponível antes de usar; esta referência não comprova a API de outra versão do cliente.
