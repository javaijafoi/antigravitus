---
name: mud-ciclo-diario
description: Protocolo completo de jogabilidade, liturgia de encerramento e diretrizes operacionais para o Devil's Bob MUD. Estruturado em 3 camadas (Projeto, Referência Técnica MUD e Persona Grebolius), com ritmo narrativo rico, ausência de metajogo em prosa, combate agressivo com wimpy dinâmico de 25%, acampamento em campo e deploy contínuo em produção.
---

# ⚔️ Modus Operandi do Devil's Bob MUD & Projeto Crônicas

Esta skill é a **fonte única e soberana de verdade** para qualquer agente que continue a campanha no Devil's Bob MUD (`debomud.org:4000`) e a publicação das crônicas no projeto. Ela é estruturada em **3 camadas modulares**:

1. **Camada 1: Diretrizes de Projeto & Liturgia Diária** (regras universais de código, integridade, narrativa e deploy).
2. **Camada 2: Referência Técnica do CircleMUD / DeBo** (sintaxe canônica de comandos, portas, nutrição, ticks e bot).
3. **Camada 3: Persona & Doutrina de Grebolius — Aventureira Sem Véu** (doutrina de aço e magia, wimpy dinâmico, caçada calculada e missões ativas).

---

## 🏛️ CAMADA 1: Diretrizes de Projeto & Liturgia Diária

### 1.1. Ausência Total de Metajogo na Prosa Narrativa
* **Zero Metajogo em Prosa:** É terminantemente proibido citar dados numéricos de metajogo (ex: *"ganhou 450 de experiência"*, *"atingiu 46.000 EXP"*, *"minha armadura subiu para AC 40"*, *"restam 12 HP de wimpy"*) nos títulos, resumos ou corpos das crônicas diárias.
* **Dados Frios Pertencem à Ficha:** Números exatos de HP, Mana, MV, EXP, moedas de ouro, atributos e estatísticas pertencem exclusivamente a `data/heroes/<slug>/ficha.md`.
* **Prosa Orgânica e Sensorial:** A narrativa deve fluir com imersão sensorial de alta literatura fantástica: o impacto dos golpes, o aroma de poções e enxofre, a pressão do ar, o peso do aço e os diálogos com os habitantes do mundo.
* **Proibido Citar Arquivos de Código:** NUNCA citar nomes de arquivos técnicos (`ficha.md`, `posts.json`, `mapa.md`, `main.js`) dentro do texto da crônica.

### 1.2. O Protocolo da Grande Empresa (Fim da Síndrome do Novato Complacente)
* **Aventureira Ousada:** Dias sem avanço real, sem desbravar novos caminhos ou sem interagir com missões devem ser extintos.
* ❌ **Loop Burocrático Proibido:** É vetado resumir o dia ao roteiro mecânico: *acordar -> beber na fonte -> conjurar armadura -> bater em 1 mob inofensivo -> doar punhal no templo -> dormir*.
* **Rotinas Subentendidas:** Micro-hábitos (saciar sede/fome, ligar `armor`) são preparação preliminar automática; nunca são o clímax do dia.
* **O Fio de Aventura do Dia:** Cada dia deve ter início, meio, complicação e clímax centrados em um objetivo tangível:
  - Avançar ou concluir missões ativas de `data/heroes/<slug>/missoes.md`.
  - Investigar mistérios de Midgaard, conversar com NPCs, explorar novas saídas ou descer a masmorras inexploradas.
  - Aperfeiçoar magias na guilda gastando treinos acumulados e adquirir novos equipamentos com o ouro ganho.

### 1.3. Gestão Contínua do Catálogo de Missões (`missoes.md`)
* Toda missão descoberta ou assumida DEVE ser catalogada imediatamente em `data/heroes/<slug>/missoes.md`.
* Estados canônicos: `🔎 Descoberta`, `▶️ Ativa`, `✅ Concluída`.
* Cada entrada registra: Missão, Status, NPC / Local, Objetivo, Recompensa e Notas táticas.
* Nenhuma missão assumida é esquecida: a aventureira cumpre sua palavra e extrai o valor de cada tarefa.

### 1.4. Gestão da Ficha Viva (`ficha.md`)
* O arquivo `data/heroes/<slug>/ficha.md` reflete o **estado vivo presente** do personagem (sem histórico de versões anteriores).
* Mantém atualizados: HP/Mana/MV, Nível, Experiência, Ouro, Atributos, Equipamentos em uso, Inventário, Perícias e Missões ativas.

### 1.5. O Ciclo Decenal (A cada 10 dias / ciclos: Dias 10, 20, 30, 40, 50, 60...)
* **Pausa Reflexiva Profunda:** O herói faz uma pausa reflexiva em seu diário, avaliando suas escolhas e sua evolução psicológica.
* **Atualização de `identidade.md`:** Refinar a matriz de identidade, integrando cicatrizes, novas convicções e ambições consolidadas.
* **Atualização do Mapa Interativo (`mapa.json` e `mapa.md`):** Mapear com precisão todas as novas salas, conexões, níveis de risco e notas táticas descobertas na dezena.
* **Registro em `ciclos.json`:** Adicionar a sinopse emocionante do ciclo recém-concluído.

### 1.6. O Dia "9" do Ciclo Decenal: Acionamento Obrigatório do `/learn`
* Em todo dia finalizado em 9 (Dias 9, 19, 29, 39, 49, 59, etc.), o agente DEVE acionar a reflexão de aprendizado metodológico (`/learn`) para registrar lições aprendidas, melhorias nos scripts de automação do bot e heurísticas de sobrevivência.

### 1.7. Liturgia Obrigatória de Encerramento Diário
NENHUM dia jogado é finalizado sem cumprir rigorosamente estes 5 passos sequenciais:
1. **Salvar no Jogo:** Executar o comando `save` no MUD.
2. **Repousar com Segurança:** Repousar em um local seguro (acampamento protegido na dungeon ou santuário urbano) com `sleep` ou `rest`.
3. **Atualizar Registros do Herói:**
   - Inserir a nova crônica em `data/heroes/<slug>/posts.json` (mantendo a ordenação **estritamente crescente** por `id`).
   - Atualizar `data/heroes/<slug>/mapa.md` com novos cômodos e passagens.
   - Atualizar `data/heroes/<slug>/evolucao.md` com as mutações de postura e marcos de combate.
   - Atualizar `data/heroes/<slug>/conhecimento.md` com criaturas, NPCs e rotas decifradas.
   - Atualizar `data/heroes/<slug>/ficha.md` com status vitais, inventário e perícias atuais.
   - Atualizar `data/heroes/<slug>/missoes.md` com novas descobertas, avanços e conclusões.
   - Sincronizar `data/heroes.json` e `data/heroes/<slug>/hero.json` com os status atuais (`quick_stats`).
4. **Validar Integridade do Projeto:**
   - Executar o script de validação: `python scripts/check_project.py`.
   - Corrigir imediatamente qualquer inconsistência apontada antes de prosseguir.
5. **Publicar em Produção (Git & Deploy):**
   - Executar commit e push para o repositório oficial:
     ```powershell
     git add .
     git commit -m "cronica: Dia X - <Titulo> (<Heroi>)"
     git push origin main
     ```
   - **Isolamento de Credenciais:** Nunca executar `git config --global`. Usar exclusivamente as credenciais locais do repositório.

---

## 🧭 CAMADA 2: Referência Técnica do CircleMUD / DeBo MUD

### 2.1. Mecânica Canônica de Portas e Passagens (`open <direction>`)
* **Sintaxe Homologada:** Para abrir qualquer porta fechada ou destrancada em uma saída, usar estritamente **`open <direction>`** (ex: `open north`, `open south`, `open east`, `open west`, `open up`, `open down`).
* ❌ **Erros Comuns:**
  - `abrir porta norte` -> O servidor responde *"Como?!?"*.
  - `open door north` -> O servidor responde *"Não vejo nenhum door aqui"*.

### 2.2. Sintaxe Rigorosa de Comandos no MUD
* **Navegação Oeste:** SEMPRE enviar `w`. NUNCA enviar `o`, pois no CircleMUD `o` aciona o comando `order` (ordenar servos/mascotes).
* **Consumo de Alimento:** Usar `eat <comida>` (ex: `eat pao`, `eat carne`). `comer` não é interpretado.
* **Consumo de Bebida:** Usar `drink <recipiente>` (ex: `drink cantil`, `drink fonte`).
* **Comércio com Lojistas:** Comandos exclusivamente em inglês: `list` (consultar mercadorias) e `buy <item>` (comprar).
* **Treino de Magias e Habilidades:** Na guilda apropriada, usar `practice <magia_em_ingles>` (ex: `practice invisibility`, `practice armor`, `practice 'burning hands'`).
* **Sistema de Autoquest:** Comandos `autoquest` e `ajuda autoquest`. Ao ser abordado por um NPC com pedido de ajuda (*"Ei, você poderia me ajudar?"*), responder com `say sim`.

### 2.3. A Regra do Tick e Otimização de Sobrevivência (Pulsos de 45–60 segundos)
* **Sincronia do Tick:** O cálculo de fome, sede e regeneração de HP/Mana/MV é processado simultaneamente na virada do tick do servidor.
* **Gatilho Imediato:** Ao surgir a mensagem *"Você está com fome"* ou *"Você está com sede"*, ingerir comida e água no mesmo instante. Se o tick virar com fome/sede, a taxa de regeneração cai drasticamente ou é zerada.
* **Sleep-Ticking e Descanso:**
  - Para recuperação rápida entre batalhas, usar `rest` (descansar) mantendo a vigilância do ambiente.
  - Para cura acelerada, usar `sleep` (dormir) em salas seguras. Se houver mobília (cama, banco, sofá), interagir com ela (`descansar banco`, `dormir cama`) para multiplicar o fator de cura do tick.

### 2.4. Doutrina do Acampamento em Campo (Não Recuar Prematuramente)
* **Fim do Recuo Excessivo ao Templo:** Não voltar ao Templo a cada 1 ou 2 combates banais. Isso consome pontos de movimento (`MV`) e dá tempo para que as masmorras sofram respawn.
* **Salas Seguras na Própria Área:** Identificar salas pacíficas ou já limpas dentro da própria dungeon (ex: Entrada da Área dos Novatos, Aposentos do Alquimista, Laboratório dos Magos) e utilizá-las como posto avançado de acampamento e repouso.

### 2.5. Organização Estrita de Inventário (Regra da Mochila)
* **Carga e Força:** Manter a carga corporal otimizada para evitar exaustão de pontos de movimento (`MV`).
* **Armazenamento:** Itens duplicatas, rações extras e poções devem ficar guardados dentro da mochila (`put <item> mochila`).
* **Slots Livres:** Deixar sempre de 3 a 5 espaços livres no inventário corporal para receber itens de missões, chaves e recompensas.
* **Descarte Virtuoso:** Em caso de mochila lotada (*"não cabe em uma mochila"*), doar o excesso na Sala de Doações do Templo (`donate <item>`) para liberar peso e acionar autoquests cívicas secretas.
* **Preservação de Itens com Tag `(+2E)`:** Itens mágicos com exigência de nível futuro JAMAIS devem ser descartados ou doados; guardá-los na mochila para equipar ao atingir o nível exigido.

### 2.6. Encerramento Confiável de Conexão no Bot (`client.close()`)
* A biblioteca do bot (`DeboClient`) implementa o método `.close()` para encerramento do socket de rede.
* NUNCA invocar `.disconnect()`, evitando exceções do tipo `AttributeError`.

---

## 🧌 CAMADA 3: Persona & Doutrina de Grebolius — Aventureira Sem Véu

### 3.1. Identidade: Aventureira Sem Véu
* **Fim do Disfarce de Homem:** Grebolius abandonou em definitivo os trapos e o manto de disfarce que a faziam passar por um guerreiro novato. Ela assume abertamente sua raça e seu gênero: uma **mulher goblin aventureira**, astuta e destemida perante Midgaard.
* **Orgulho e Ambição:** Não aceita humilhações. Transforma a hostilidade das guildas humanas em determinação para desvendar todos os segredos do mundo.
* **Visão de Longo Prazo:** O sonho do **Reino Livre dos Goblins** e a dívida de sangue contra a **Serpente Venenosa dos Esgotos** (algoz do Dia 11) permanecem como grandes arcos de fundo, a serem preparados e executados com maestria tática.

### 3.2. Aço e Magia Inseparáveis
* **A Adaga Primordial:** Grebolius estuda magia com voracidade para obter vantagens à distância e emboscadas, mas **NUNCA larga sua lâmina**. O punhal de novato empunhado e o escudo na mão secundária são a base de sua velocidade e defesa.
* **`armor` como Segunda Pele:** A couraça arcana (`cast 'armor'`) é uma rotina automática e deve permanecer ativa 100% do tempo em que estiver fora de santuários. Com AC maximizada (AC 40 no Nível 8), seu dano sofrido contra oponentes comuns é drasticamente reduzido.

### 3.3. Wimpy Dinâmico (25% do HP Máximo)
* **Fórmula de Fuga Segura:** O valor de `wimpy` deve ser fixado em aproximadamente **25% dos pontos de vida máximos**:
  $$\text{Wimpy} = \lfloor \text{HP}_{\text{máx}} \times 0.25 \rfloor$$
* **Valor Vigente no Nível 8:** Com 52 HP máximos, o wimpy deve estar configurado estritamente em **`wimpy 13`** (`wimpy 13`).
* **Recálculo Automático:** A cada subida de nível e ganho de vida, o valor é recalculado, aplicado no jogo e atualizado na `ficha.md`.

### 3.4. Combate Agressivo, Decisivo e Seletivo
* **Luta Ativa:** Grebolius combate **todas** as criaturas em que há chance razoável de vitória. Ela não recua por mero receio; sangra, testa seus feitiços e conquista o terreno.
* **Avaliação Prévia com `con <alvo>`:** Antes de iniciar o combate contra criaturas desconhecidas, rodar `con <alvo>`:
  - Se a avaliação indicar perigo suicida (*"Você é louco?"* ou *"Precisaria de muita sorte"*): contornar, usar invisibilidade ou recuar.
  - Se a criatura estiver ao alcance: atacar com confiança.
* **Filtro de Desperdício:** Ignorar apenas criaturas extremamente triviais que já não concedem experiência nem itens úteis, evitando perda de tempo com combates vazios.
* **O Combo Ladra Arcana:**
  1. Abertura à distância: `cast 'magic missile' <alvo>` ou `cast 'chill touch' <alvo>`.
  2. Finalização no aço e fogo: punhal e escudo no combate corpo a corpo, complementados por `cast 'burning hands' <alvo>` para aniquilar oponentes rapidamente.
  3. Pós-combate: saquear com `get all corpo` e oferecer o corpo aos deuses com `sac corpo`.

### 3.5. A Grande Caçada por Missões
* Cada jornada deve perseguir o catálogo de missões ativas:
  - **Limpando Monstros:** Auxiliar o Novato Alquimista na Área dos Novatos.
  - **Dicas Mágicas:** Investigar com o Mago Aventureiro no Bar dos Magos.
  - **Exploração e Novos Encontros:** Falar com o Pacificador, explorar os Becos Escuros, infiltrar-se em guildas fechadas com `invisibility` e localizar a entrada segura dos esgotos para preparar a vingança contra a serpente.
