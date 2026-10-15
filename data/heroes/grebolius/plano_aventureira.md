# Plano da Aventureira — Grebolius

Plano futuro a partir do encerramento documental do Dia 60. Grebolius é uma mulher goblin sem disfarce e de classe **Mago**. Explora, investiga e assume compromissos; XP e níveis são consequência. Nenhum passo abaixo aconteceu só por estar previsto aqui.

## 1. Preparar a próxima saída
- Conferir o estado no MUD antes de jogar. A migração para `state.json` usa os documentos existentes e não equivale a uma conferência ao vivo.
- Referência documental: nível 8; vida máxima 52; mana máxima 140; 1.051 moedas; seis sessões de treino. Movimento diverge entre 94/95 e 95/95 em instantâneos do encerramento: verificar em vez de fabricar uma recuperação entre eles.
- Conferir equipamento e inventário, inclusive recipientes e mochila. O anel arcano foi guardado no Dia 43, mas sua posse atual e os requisitos exatos de uso precisam ser conferidos. Não contar com seu bônus antes disso.
- Verificar se `armor` está ativa, seu custo e a duração informada pelo jogo. Não pressupor imunidade ou efeito permanente.
- Manter `wimpy 13` como referência vigente até nova avaliação. A heurística antiga de 25% não prova uma margem segura: considerar dano observado por golpe, vida restante, mana, movimento e uma saída utilizável. Sem margem ou retorno conhecido, adiar o confronto.
- Distinguir o **Laboratório dos Magos**, último acampamento registrado, do **Panteão dos Centenários**, referência histórica de repouso. Sala vazia, limpa ou com NPC conhecido não garante proteção contra ataque, patrulha ou reaparecimento.

## 2. Escolher um objetivo verificável
Consultar `missoes.md` e `missoes.json`, diferenciando tarefa oficial, investigação e objetivo pessoal.

1. **Limpando Monstros:** retomar a tarefa aceita no Dia 36 e mencionada novamente no Dia 60. Consultar o Alquimista e o diário de missões para obter alvos, quantidades, progresso e condição de conclusão. Não contar abates anteriores como progresso sem confirmação.
2. **Dicas Mágicas:** voltar ao Mago Aventureiro e consultar a tarefa iniciada no Dia 32; registrar a próxima instrução efetivamente recebida.
3. **Investigações abertas:** Pacificador, guildas hostis, Beco Escuro ou Pranteador, conforme acesso e respostas reais. Conversa não cria aliança. Invisibilidade não comprova acesso a guildas nem ausência de detecção; “ladra arcana” não comprova habilidade de furto.
4. **Reino Livre:** procurar uma oportunidade concreta ligada ao futuro goblin — contato, abrigo ou recurso — apenas se o mundo apresentar essa possibilidade. Registrar inclusive uma busca sem resultado; não criar habitantes, seguidores, terreno ou acordos.

Antes de sair, definir o que pode comprovar avanço: instrução recebida, pista confirmada ou descartada, rota observada, recurso obtido ou condição de missão verificada. Falta de acesso e necessidade de recuo também são resultados úteis.

### Gatilhos de Exploração de Lugares Novos
Desbravar novas rotas ou áreas desconhecidas deve estar fundamentado em um destes três motivos:
1. **Digestão de trauma recente:** Morte, queda brutal ou fuga desesperada (`wimpy`). O horizonte amplo e rotas abertas servem para clarear as ideias, digerir a derrota e recalibrar o instinto antes de encarar o subsolo sufocante.
2. **Combate ao tédio (dois dias seguidos de repetição):** Se passar dois dias consecutivos nas mesmas rotinas mecânicas sem novidade, a inquietação goblin exige explorar uma nova frente no mapa.
3. **Marcos decenais do ciclo:** Dias redondos (10, 20, 30, 40, 50, 60, 70...) exigem expansão proposital de fronteiras e desafio a zonas inexploradas.
### Cadência Operacional: Tempo Real vs. Script Autônomo
- **Dias com final 5 e final 0 (5, 10, 15, 20, 25, 30, ...): Tempo Real (Interativo).** Nesses dias, a sessão é jogada comando a comando via conexão interativa contínua (`live_session.py`), sem script enlatado de rota. Cada resposta do MUD é avaliada em tempo de execução para reagir a salas, mobs, saídas e oportunidades.
- **Demais dias (finais 1, 2, 3, 4, 6, 7, 8): Modo Script Autônomo (Batch).** Execução programada da rota para máxima eficiência de tokens e velocidade, com pausa tática automática para assumir em tempo real se surgir anomalia ou jogador.
- **Dias com final 9 (9, 19, 29, 39, ...): Reflexão Pessoal e Existencial.** O dia encerra um ciclo decenal e traz na crônica a reflexão psicológica/existencial da heroína, estritamente sem jargão de regras e sem números de ficha (apenas moedas de ouro).

### Gasto Ativo e Aproveitamento da Estamina (MV)
Superar roteiros curtos e estáticos. A estamina alta (101 MV no Grau 11) é o motor da exploração:
- **Dias ativos e proveitosos:** Explorar, patrulhar, caçar e mapear gastando a estamina de forma produtiva ao longo de dezenas de passos (40 a 90 passos), em vez de encerrar a sessão após breves caminhadas.
- **Incursões de Mapeamento com Batedor Furtivo (Stealth Scout):**
  - Descarregar peso morto na base (armazenar punhais/vestes excedentes para aliviar Força 10).
  - Levar carga alimentar eficiente: 6 a 8 pães recheados da padaria (leves e baratos) + cantil(is) cheios de água.
  - Ativar `armor` e `invisibility` antes da marcha. A invisibilidade não quebra ao andar e previne aggro de mobs comuns.
  - Andar e mapear sala a sala até a margem de segurança de estamina (`MV ~ 15-20`).
- **Recuperação Eficiente em Campo (Sono vs. Fome):**
  - Para restaurar 100% de MV e Mana sem voltar para casa: encontrar uma sala vazia/segura (sem mobs agressivos nem fluxo de patrulha, checada com `scan` e `look`).
  - Comer pão e beber água para manter o estômago saciado (fome e sede travam a regeneração).
  - Renovar `armor` e `invisibility` antes de deitar se a duração (~24 ticks) estiver acabando.
  - Executar `sleep` por 3 a 4 ticks (~3 a 5 min reais) para recarregar todos os vitais (0 a 101 MV e 170 Mana), despertar (`wake`), levantar (`stand`) e retomar a marcha.
- **Retorno e encerramento seguro somente se:**
  1. A estamina atingir a margem de retorno seguro e não houver abrigo viável para dormir em campo.
  2. Impossibilidade de recuperação em campo (emboscada contínua, dano persistente ou ausência de abrigo seguro).
  3. Mochila saturada de espólios de valor que exijam guardar/vender.
  4. Anomalia hostil grave, bloqueio ou perigo mortal iminente.

### Protocolo Tático de Exploração e Engajamento (Anti-Morte)
- **Reconhecimento prévio:** Em áreas perigosas ou labirintos fechados (como esgotos), espiar saídas com `look <direção>` (`look n`, `look s`, `look e`, `look w`) e usar `scan` para mapear salas vizinhas antes do avanço.
- **Invisibilidade de batedor:** Usar `invisibility` para caminhar por zonas de predadores sem disparar aggro automático, permitindo avaliar a sala em segurança. Lembrar que a invisibilidade quebra no primeiro golpe ou magia agressiva.
- **Avaliação de risco obrigatória (`consider <alvo>`):** Proibido atacar mobs desconhecidos sem rodar `consider <alvo>`. Se houver alerta de massacre ou alto risco, abortar o ataque.
- **Recuo pré-combate vs. Fuga em combate (`flee` obrigatório):**
  - Se entrar na sala e o mob perigoso ainda não atacou: recuar imediatamente usando a direção normal inversa (ex.: `s`).
  - Se o combate já tiver iniciado (aggro sofrido ou monstro acertar golpe pesado): **NUNCA tentar andar por direções normais (`n`, `s`, `e`, `w`)**, pois o MUD trava o comando (*"Não dá! Você está muito ocupado, lutando!"*). O único comando para desengajar e salvar a vida é **`flee`** (ou **`fugir`**).

## 3. Matriz de Modos Operacionais (Overrides de Comportamento)
Os modos operacionais definem a postura tática, a alocação de risco, a gestão de inventário e os gatilhos de recuo/fuga para cada dia de expedição. Eles dão override no comportamento padrão:

1. **Modo Padrão (Equilibrado):**
   - **Postura:** Exploração balanceada, patrulha rotineira e treino.
   - **Combate:** Engaja presas conhecidas e seguras com `consider` prévio; recua se o risco for médio/alto.
   - **Wimpy:** Configuração padrão (~25%, atualmente 13-17 HP).
   - **Logística:** Carga intermediária, retorno ao santuário/laboratório para pernoite.

2. **Modo Aventura (Foco na Missão / Quest):**
   - **Objetivo:** Concluir a autoquest ou missão ativa designada.
   - **Postura:** Foco estrito no objetivo da missão; ignora o que não for relevante ao redor.
   - **Combate:** Abate apenas mobs fracos necessários para abrir caminho ou cumprir requisito; desvia de qualquer mob arriscado.
   - **Gestão de Bloqueios:** Se encontrar um obstáculo intransponível (falta de nível, monstro forte demais bloqueando passagem, falta de ouro para item de entrega), anota a pendência específica em `missoes.json` e na crônica, encerra o dia em segurança e sugere para o dia seguinte a transição para o modo adequado (ex.: Modo Dungeon para farmar ouro/EXP).

3. **Modo Dungeon (Limpeza e Pilhagem Máxima):**
   - **Objetivo:** Varrer e limpar a masmorra/catacumba, maximizando espólios e ouro.
   - **Preparação:** Mochila limpa de peso morto (apenas armas equipadas, tocha, 1 cantil e 4-6 pães recheados).
   - **Combate:** Arrisca um pouco mais contra mobs de dificuldade moderada (zumbis, monstros novatos, minotauro com `chill touch` e `armor`), mas NUNCA desafia criaturas muito difíceis ou letais (chefes desproporcionais).
   - **Sustentação em Campo:** Pausas e nutrição necessárias em salas seguras para sustentar a expedição.
   - **Gestão de Carga (Força 10):** Quando o inventário encher de espólios valiosos (punhais, peles, chifres), retorna temporariamente à cidade para vender nas lojas e guardar ouro na caixa do Templo/Guilda antes de retomar a limpeza. Encerra o dia com acampamento flexível ou na cidade.

4. **Modo Batedor (Stealth Scout / Mapeamento Máximo):**
   - **Objetivo:** Mapear o maior número possível de salas da área/zona sem combate.
   - **Camuflagem:** `invisibility` e `armor` mantidos 100% ativos; batedor avança consumindo o MV em dezenas de salas.
   - **Postura de Combate & Fuga:** Evita 100% dos combates possíveis. Zero combate voluntário. Se sofrer aggro inesperado (criatura com visão arcana), executa **`flee` imediatamente no 1º turno**.
   - **Rede de Segurança Mecânica:** **Wimpy elevado para 60% do HP máximo** (`wimpy 40` no Grau 11) para garantir disparo automático de fuga caso a conexão ou comando falhe. Ao desativar o modo, restaura o Wimpy para o padrão (~25%).
   - **Logística e Sono em Campo:** Carga ultra-leve (6 a 8 pães recheados da padaria + 1 ou 2 cantis cheios na Fonte Azul). Ao sobrar 15-20 MV, escolhe uma sala vazia e segura (checada com `scan` e `look`), come, bebe e usa `sleep` por 3 a 4 ticks (~3 a 5 min) para recarga total de MV e Mana, acordando para prosseguir.

5. **Regra de Seleção (Modelo Híbrido):**
   - O usuário pode ativar qualquer modo explicitamente no chat (ex.: *"hoje vamos em modo batedor"*).
   - Quando não especificado, o agente assume o modo mais lógico com base na meta prioritária do dia (se há quest pendente -> Aventura; se há masmorra lucrativa para limpar -> Dungeon; se há área desconhecida -> Batedor), usando o Modo Padrão como fallback.

## 4. Jogar e registrar com continuidade
1. Escolher um fio para a expedição e as condições para interrompê-la.
2. Explorar, observar e interagir segundo o risco. Lutar por defesa, passagem ou objetivo; não há cota mínima de ações, salas novas ou combates.
3. Registrar primeiro fatos e fontes; separar crença da personagem e plano futuro. Atualizar estado, eventos, missões e mapa conforme evidência.
4. Escrever a crônica a partir desse registro. Não inserir diálogos, recompensas, vínculos, perdas ou vitórias ausentes da sessão. Números mecânicos ficam nos registros técnicos; escrevê-los por extenso não os torna prosa de aventura.
5. Dar espaço ao que mudou de verdade, mesmo que seja uma hipótese descartada ou uma retirada. Não forçar clímax, novidade ou aprendizado emocional.

## 5. Usar os recursos com propósito
- **Treinos:** consultar as opções disponíveis e escolher uma capacidade que ajude o objetivo. Não gastar automaticamente as seis sessões acumuladas.
- **Compras:** consultar preços, peso, requisitos e benefício antes de decidir; preservar uma reserva para provisões e deslocamento. Os 1.051 ouros registrados não permitem comprar o pergaminho de retorno a 9.202 nem a poção amarela a 5.370, preços catalogados no Dia 42. Revalidar preços e saldo no jogo.
- **Consumíveis:** não pressupor posse de retorno, cura ou detecção; verificar inventário e efeito antes de incluir o item em uma rota de retirada.
- **Descanso:** escolher conforme segurança e saídas observadas. Não impor acampamento na masmorra nem tratar retorno ao santuário como fraqueza.

## 6. Horizonte de Expedições
O antigo resumo antecipado do ciclo 7 foi retirado de `ciclos.json`: não há crônicas desses dias. Seu fio passa a ser uma possibilidade de planejamento:

1. Reconciliar ficha, anel, treinos e tarefas pendentes.
2. Avançar uma missão ou investigação com evidência verificável.
3. Reconhecer o acesso aos esgotos, ameaças e retorno. O mapa histórico relata uma descida sem subida direta: não entrar supondo reversibilidade.
4. Escolher entre confrontar a serpente, preparar mais recursos ou adiar. Vitória, decapitação e subida de nível não estão garantidas.

Se surgir uma oportunidade real ligada ao Reino Livre ou um compromisso efetivamente assumido, avaliar como ela pesa diante da vingança. O plano não cria esse encontro nem decide a escolha antes de acontecer.
