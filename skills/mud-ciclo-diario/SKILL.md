---
name: mud-ciclo-diario
description: Protocolo completo de jogabilidade e encerramento para cada dia no Devil's Bob MUD. Define ritmo narrativo rico (dias longos), 3 ações diárias obrigatórias, combate/treino frequente, reflexão decenal, ausência total de metajogo, ficha viva sincronizada, doutrina de aço e magia, e deploy contínuo em produção.
---

# ⚔️ Skill: Modus Operandi Completo do Devil's Bob MUD

Esta skill formaliza todas as regras de jogo, liturgia de encerramento e diretrizes operacionais para qualquer agente que continue a campanha no Devil's Bob MUD (`debomud.org:4000`), inclusive em outros computadores.

---

## 🗡️ 1. Doutrina do Personagem (Grebolius — Ladra Arcana)
* **Aço e Magia Inseparáveis:** Estudar magia com voracidade para obter vantagens à distância e emboscadas, mas **NUNCA largar a adaga**. O punhal na cintura e as lâminas secundárias continuam sendo a extensão primordial de seu instinto de sobrevivência.
* **Multiplicidade de Caminhos para o Poder (A Luta é Apenas Um Deles):** A luta é uma via de ascensão, mas **não é a única e nem sempre a mais inteligente**. Grebolius precisa de **todos os caminhos** e, dentre eles, escolher sempre **os melhores e mais eficientes**:
  - **Aventuras e Tarefas Oficiais (Autoquests):** Ganhar experiência, respeito cívico e ouro cumprindo missões para cidadãos e sentinelas sem desgaste cego de sangue.
  - **Treino e Refinamento de Técnicas:** Praticar com mestres, desbloquear feitiços utilitários (vidência, proteção) e estudar auras.
  - **Diplomacia Clandestina e Informação:** Conversar com NPCs, mercadores e veteranos para descobrir fraquezas de inimigos e segredos da cidade.
  - **Comércio e Economia:** Negociar espólios, acumular ouro e equipar-se com o melhor que Midgaard tem a oferecer.
  - **Combate Seletivo e Cirúrgico:** Lutar quando necessário, com foco cirúrgico em alvos de alto retorno e baixo risco inútil.
* **Aproveitamento Total de Recursos:** Se a guilda dos ladrões fechou as portas e os guardas a humilham, ela **não lamenta**: ela aproveita todo e qualquer poder que conseguir (guilda dos magos, venenos, artefatos, alianças cívicas e magia) e transforma a rejeição em aventura.
* **Toda Missão Assumida Deve Ser Concluída e Catalogada:** Jamais abandonar tarefas cívicas ou pedidos de NPCs (como a missão do Bebê Dragão e do Guarda Novato). Toda missão descoberta entra em `missoes.md` e segue até a entrega; a palavra dada é o que consolida alianças.
* **Disfarce como Ferramenta Tática:** Manter a postura de guerreiro novato quando proteger sua identidade de mulher goblin for útil. É uma escolha de cada situação, não um dever diário.
* **Pano de Fundo:** O sonho do Reino Livre dos Goblins e a dívida contra a serpente do Dia 11 continuam como arcos de longo prazo. Valem como missões entre as outras, nunca como justificativa para farm ou vingança cega.

---

## 🏹 2. Diretrizes Narrativas e de Jogabilidade
1. **Extensão e Profundidade (Dias 5x mais longos):**
   * As crônicas devem ser densas, detalhadas, exploratórias e imersivas (cerca de 5 vezes maiores que relatos básicos).
2. **Ação Contínua e a Grande Empresa (Fim da Síndrome do Novato Complacente):**
   * **Grebolius é uma aventureira curiosa e ousada:** Dias sem avanço real, sem resolução de pendências ou sem desbravar algo novo devem ser **extintos**.
   * ❌ **Loop Burocrático Proibido:** É terminantemente vedado resumir o dia ao script mecânico: *acordar -> beber na fonte -> castar armadura -> matar 1 monstro novato no corredor -> doar punhal no templo -> dormir*. Ela não é uma "gamer farmando mob".
   * Micro-hábitos de sobrevivência (saciar sede/fome, ligar armadura mágica) são **preparação preliminar automática**, nunca o tema ou o clímax do dia.
   * Cada dia jogado DEVE girar em torno de **um fio de aventura** (missão ou mistério), consultando `data/heroes/<slug>/missoes.md` e `plano_aventureira.md` quando existirem:
     - Concluir ou avançar missões ativas (Alquimista, Bar dos Magos...);
     - Descobrir e catalogar missões novas, falando com NPCs, lendo placas e testando `autoquest`;
     - Investigar mistérios (guildas hostis, Beco Escuro, convites de NPCs poderosos);
     - Consumir sessões de treino e investir o ouro em itens e magias úteis à aventura;
     - Mapear territórios inéditos.
3. **Equilíbrio de Aventura:**
   * Prioridade: missões e exploração. Treino e comércio sustentam a aventura.
   * Luta é meio, não fim: serve a uma missão, pista, item ou história. Repetir mobs só por EXP não é tema de um dia.
   * Criatividade é bem-vinda: invisibilidade para espionar, conversa, furto astuto, alianças, testar mecânicas e arriscar lutas calculadas (ver §6.6).

---

## 🏛️ 2.1 O Fluxo de Pensar o Dia: O Protocolo da Grande Empresa

Antes de gerar qualquer script ou comando para o dia, o agente DEVE conceber a jornada em 4 etapas mentais obrigatórias:

1. **O Fio de Aventura Ativo (O Vetor Estratégico):**
   * Que missão, mistério ou fronteira do mundo Grebolius está empurrando para a frente hoje? Consultar `missoes.md`.
   * *Exemplos prioritários:*
     - **Conclusão de Quests:** alcançar o Alquimista para entregar "Limpando Monstros"; ir ao Bar dos Magos desvendar "Dicas Mágicas".
     - **Novas Missões:** conversar com NPCs ainda não explorados, ler placas, testar `autoquest` e catalogar o que surgir.
     - **Mistérios:** guildas hostis, Beco Escuro, convite do Pacificador.
     - **Treino e Tesouro:** usar sessões de treino pendentes e o ouro acumulado (valores atuais na `ficha.md`) em magias e itens úteis à aventura.
     - **Expansão Territorial:** Floresta Élfica, Cemitério ou Estradas Reais.
     - **Arcos de fundo (ocasionais):** a dívida contra a Serpente Venenosa do Dia 11, tratada como missão e não como obsessão.

2. **A Missão do Dia (The Day's Enterprise):**
   * O dia DEVE ter um **tema unificador** e uma narrativa com início, meio, complicação e clímax.
   * Grebolius sai do santuário com uma **intenção declarada** (ex: *"A Incursão ao Laboratório do Alquimista"*, *"O Julgamento dos Mestres Arcanos"*, *"A Caçada nas Galerias Negras"*).

3. **Escala e Profundidade da Ação (Sem Recuos Prematuros):**
   * Grebolius não se contenta em abater 1 criatura inofensiva e fugir para a cama.
   * A incursão vai até o fundo: alcança o laboratório, confronta os guardiões reais, desvenda as portas trancadas, interage com NPCs-chave e consome a estamina ou recursos com ambição de soberana.

4. **Transformação Tangível de Status:**
   * O dia só é válido se terminar com algo concreto transformado:
     - Uma sala nunca antes pisada foi mapeada e dominada;
     - Uma conversa ou pista decisiva foi colhida de um NPC;
     - Um novo poder arcano ou perícia foi aperfeiçoada na guilda;
     - Uma missão oficial foi entregue ou progredida;
     - Ouro foi transformado em poder real ou uma vingança foi consumada.
4. **Gestão de Estamina (Limiar do Movimento):**
   * O dia de exploração deve ir até quase o esgotamento total dos pontos de movimento (`MV`), deixando apenas a margem estritamente suficiente para retornar a um santuário seguro.
5. **Zero Metajogo, Rotinas Subentendidas e Ausência de Números em Prosa:**
    * **Rotinas Subentendidas:** Micro-ações mecânicas repetitivas (beber da fonte, comer ração, conjurar `armor`) tornam-se implícitas após estabelecidas. NUNCA narrar essas rotinas a cada dia como se fossem rituais solenes; estão subentendidas na rotina prática da aventureira.
    * **Menção de Recursos Apenas em Marcos Decisivos:** NUNCA citar valores numéricos de EXP ganha ("mais 450 de experiência"), saldo de moedas de ouro ou passos nos títulos e textos do dia a dia. Somente citar recursos em **grandes marcos**:
      - Subida de grau / ascensão de nível;
      - Grandes compras ou gastos massivos (troca de equipamento, grimórios, artefatos);
      - Espólio lendário ou conquista monumental.
    * No dia a dia comum, a narrativa flui de modo orgânico, focada em acontecimentos, exploração, diálogos e cenários. Os números exatos pertencem estritamente à `ficha.md`.
    * **NUNCA** citar nomes de arquivos técnicos (`mapa.md`, `posts.json`, `ficha.md`, etc.).
6. **Protocolo Obrigatório de Subida de Nível & Recursos:**
   * **Treino Imediato na Guilda:** Ao avançar de grau, ir imediatamente ao mestre da guilda (`practice <magia>`) e alocar as sessões de treino para maximizar a nova habilidade desbloqueada (ex: Nv 5 `infravision`, Nv 6 `invisibility`, Nv 7 `armor`).
   * **Revisão de Equipamentos:** Verificar se os equipamentos em uso são os melhores disponíveis; doar ou vender excedentes.
   * **Autonomia em Dungeons (Comida, Água e Cura):** Manter sempre a mochila abastecida com comida (`put carne mochila`, `put laranja mochila`), cantis cheios na fonte e um pergaminho de retorno (`scroll of recall`). Alimentos e itens de cura evitam recuos prematuros da masmorra.

---

## 📜 3. Gestão da Ficha Viva da Personagem
* Em `data/heroes/<slug>/ficha.md` e na aba `/ficha.html` do site:
  - Manter sempre a **ficha viva** da personagem refletindo o estado real do MUD (HP, Mana, MV, Atributos, Perícias conhecidas, Sessões de treino pendentes, Equipamentos em uso e Inventário).
  - **Sem histórico de versões passadas**: o arquivo reflete unicamente o estado presente e vivo do herói.

---

## ⏳ 4. Ciclo Decenal (A cada 10 ciclos / dias)
* A cada 10 dias ou ciclos de jornada (Dias 10, 20, 30... / Ciclo I, II, III...):
  1. O herói faz uma **pausa reflexiva profunda** em seu diário, avaliando friamente se sua rota e escolhas estão acelerando sua chegada ao topo.
  2. Modificar de forma **sutil** o arquivo `data/heroes/<slug>/identidade.md`, incorporando as fissuras, aprendizados e novas táticas consolidadas.
  3. Aplicar as novas táticas imediatamente no ciclo decenal seguinte.
  4. **Atualização Obrigatória do Mapa Interativo (A cada 10 ciclos):** Atualizar e sincronizar rigorosamente o mapa interativo do aventureiro (`data/heroes/<slug>/mapa.json` e `data/heroes/<slug>/mapa.md`) com todas as novas salas desbravadas, conexões, níveis de risco, NPCs e anotações táticas, mantendo o mapa visual do blog atualizado por aventureiro.

---

## 📌 5. Liturgia Obrigatória de Encerramento Diário
NENHUM dia jogado é encerrado sem cumprir esta sequência de 5 passos:

1. **Salvar no Jogo:** Executar o comando `save` no MUD.
2. **Repousar com Segurança:** Retornar a um santuário protegido (Templo de Midgaard ou Panteão dos Centenários) e emitir `sleep`.
3. **Atualizar Registros do Herói:**
   - Adicionar o novo dia em `data/heroes/<slug>/posts.json` (mantendo a ordem estritamente crescente).
   - Atualizar `data/heroes/<slug>/mapa.md` com novos cômodos e conexões.
   - Atualizar `data/heroes/<slug>/evolucao.md` com as mutações de comportamento e combates.
   - Atualizar `data/heroes/<slug>/conhecimento.md` com criaturas, perigos e rotas decifradas.
   - Atualizar `data/heroes/<slug>/ficha.md` com os status vitais e inventário atuais.
   - Atualizar `data/heroes/<slug>/missoes.md` (se o herói tiver catálogo): novas missões entram como 🔎, aceitas como ▶️, entregues como ✅, sempre com NPC, local, objetivo e recompensa.
4. **Atualizar Feed Geral e Index:**
   - Manter `data/posts.json` ou feed integrado sincronizado.
5. **Subir em Produção Imediatamente (Git & Vercel):**
   - Executar commit e push para `origin main`:
     ```powershell
     git add .
     git commit -m "cronica: Dia X - <Titulo> (<Heroi>)"
     git push origin main
     ```
   - Respeitar estritamente o isolamento de credenciais locais (nunca alterar configs globais de git).

---

## 🛡️ 6. Heurística Avançada de Combate, Carga e Sobrevivência (CircleMUD / DeBo)
Para destravar o avanço de nível sem loop de morte:

1. **Configuração de Fuga de Emergência:**
   - Rodar `wimpy 12` ao iniciar a sessão (detalhes e justificativa no item 6). O valor vigente fica em `ficha.md`.
2. **Gerenciamento de Carga com Força 10 (Descarte de Peso Morto):**
   - Com STR 10, carregar itens pesados (como picareta +10L, espadas militares pesadas, lâminas improvisadas e gorros reservas) drena os 84 MV velozmente e trava a esquiva.
   - Vender sucata nos comerciantes certos de Midgaard:
     * Loja de Armas / Ferreiro (Rua Leste II): espada longa, lâmina improvisada, adaga extra, picareta.
     * Loja de Armaduras (Rua Oeste): gorro de couro reserva.
     * Loja de Magias (Término da Rua Oeste): bastões e itens arcanos excedentes.
   - Usar sacolas/mochilas (`backpack`, `bag`) para driblar o limite de itens soltos nas mãos.
3. **Otimização de Equipamento em Uso:**
   - Conferir sempre itens melhores na mochila: remover gorro comum (`remove gorro`) e vestir o elmo encantado de novato (`wear elmo`) para maximizar Classe de Armadura e auras místicas.
4. **Avaliação Obrigatória com `con <alvo>`:**
   - **NUNCA** executar `kill` ou lançar feitiço ofensivo sem antes rodar `con <alvo>`.
   - Ler rigorosamente o quadro comparativo:
     * Se a Vida do oponente for *"Você é louco?"* ou *"Precisaria de muita sorte"*: **Fugir / ignorar imediatamente (ex: bebê dragão)**.
     * Se Poder for *"perda de tempo"* e Precisão for *"Fácil!"*: **Atacar**.
5. **O Combo de 'Ladra Arcana' (Abertura Mágica + Finalização no Aço):**
   - Abrir o combate à distância com `cast 'magic missile' <alvo>` (10 de dano instantâneo com 95%+ de acerto).
   - Deixar o punhal novato empunhado e o escudo apararem o contra-ataque e finalizarem a presa no combate corpo a corpo para economizar mana.
6. **Risco Calculado e Fuga (Wimpy 12):**
   - `wimpy 12` é o padrão. Dá margem para fugir de um golpe forte e ainda permite arriscar lutas que valham a história (missão, pista, item, aliado).
   - Não recuar por arranhões, mas também não lutar "até a destruição" por teimosia: se a luta não serve a uma missão ou a uma boa história, contornar (invisibilidade, conversa, furto, desvio).
   - Mudar o valor de wimpy só por decisão explícita e registrada na `ficha.md`.
7. **Varredura e Portas de Fuga Abertas:**
   - Checar saídas e salas adjacentes com `look <direcao>` antes de entrar.
   - Manter portas destrancadas e abertas nas costas para que qualquer recuo tático seja desimpedido.
8. **Auto-Saque e Sacrifício aos Deuses:**
   - Ativar `autogold` e `autoloot` (ou conferir em `config`).
   - Após saquear (`get all corpo`), usar `sac corpo` para oferecer o cadáver aos deuses em troca de moedas de ouro ou bônus de XP.
9. **Monitoramento de Luz, Hidratação e Suprimentos:**
   - Vigiar alertas da tocha para não lutar cego no escuro (inviabiliza conjuração).
   - Beber nos cantis assim que a sede surgir.
   - Passar na Sala de Doações do Templo para checar itens e pergaminhos gratuitos deixados por veteranos antes de comprar.
10. **Superação do Medo da Morte e o Risco Certo:**
    - A morte roubou memórias outrora, mas a covardia roubaria seu futuro. Ser muito prudente nunca a fará rainha de nada.
    - Grebolius enfrenta seus medos ativamente: não toma riscos burros (não ataca criaturas cósmicas ou dragões veteranos), mas assume o RISCO CERTO com ferocidade — caça, sangra, avança e conquista seu trono no aço e no fogo arcano.
11. **Organização Estrita de Inventário (Regra da Mochila):**
    - **JAMAIS** destruir, sacrificar ou descartar itens úteis para liberar peso.
    - Manter itens duplicatas (punhais extras, cantis sobressalentes, gorros reservas e alimentos) **DENTRO da mochila** (`put <item> mochila`).
    - Deixar sempre 3 a 5 slots de inventário livres para receber itens de missões, recompensas e chaves.
12. **Sintaxe Canônica de Comandos no CircleMUD / DeBo MUD:**
    - **Navegação Oeste:** SEMPRE enviar `w` (oeste). NUNCA usar `o`, pois `o` no CircleMUD aciona o comando `order` (ordenar).
    - **Consumo de Alimento:** Usar `eat <comida>` (ex: `eat carne`, `eat laranja`). `comer` não é reconhecido pelo interpretador.
    - **Comércio com Lojistas:** Comandos estritamente em inglês: `list` (ver catálogo) e `buy <item>` (comprar).
    - **Treino de Habilidades:** Utilizar `practice <nome_da_magia_em_ingles>` (ex: `practice invisibility`, `practice armor`) no laboratório da guilda.
    - **Sistema de Autoquest:** Utilizar `autoquest` e `ajuda autoquest`. Para aceitar qualquer missão ao ouvir *"Ei, você poderia me ajudar?"*, SEMPRE responder `say sim`.
    - **Itens de Missão:** Não tentar entregar itens caídos no chão da sala do NPC (erro de dono original); buscar o item legítimo na área de fuga da criatura.
13. **Gestão de Transbordo de Container (Overflow de Mochila):**
    - Quando o MUD avisar *"não cabe em uma mochila"*, a capacidade máxima foi atingida.
    - NUNCA manter excesso de armas ou vestes nas mãos: doar imediatamente na Sala de Doações (`donate <item>`), o que também aciona e conclui autoquests cívicas secretas (ex: missão *Altruísmo*).
14. **Dia "9" do Ciclo Decenal (Obrigatório /learn):**
    - Todo dia "9" de cada dezena (Dia 9, 19, 29, 39, 49, etc.), o agente DEVE acionar a reflexão de aprendizado metodológico (`/learn`) para registrar melhorias na automação, nos scripts do bot e nas heurísticas de sobrevivência, consolidando a inteligência operacional do sistema antes do marco decenal da personagem.
15. **`cast 'armor'` é Rotina, não Decisão:**
    - `armor` fica ativo o tempo todo em que Grebolius estiver fora de santuário, e é reconjurado ao expirar, antes de qualquer risco ou masmorra.
    - Com a couraça sempre ligada, ela pode assumir riscos criativos maiores (ver item 6).
16. **Aberturas Orgânicas e Variadas nas Crônicas (Antirrepetição Estrita):**
    - **NUNCA** iniciar crônicas com fórmulas repetitivas do tipo *"O [ordinal] despertar/alvorecer..."*, *"O silêncio do panteão..."* ou narração burocrática de descida de escadas e hidratação.
    - **SEMPRE** iniciar com elementos imersivos, sensoriais e vivos: o zumbido de uma magia na pele, o aroma acre de reagentes alquímicos, o vento fustigando as folhas de carvalhos na zona rural, a observação tática de heróis veteranos (como Negelok em seu Grifo ou Valgren) ou o choque súbito de um combate in media res.
17. **Governança de Itens com Exigência de Nível (`(+2E)`):**
    - Joias e armas raras encontradas com tags como `(+2E)` exigem círculos superiores para uso (ex: o Anel Arcano que retornou *"Você não tem experiência para usar um anel arcano"*).
    - Esses itens são preciosidades patrimoniais: **JAMAIS** doá-los ou descartá-los por frustração de uso imediato; devem ser preservados na mochila para equipar assim que o nível correspondente for atingido.
18. **Regra do Tick e Sincronia de Nutrição:**
    - O pulso vital do servidor (tick) ocorre a cada 45-60s e recalcula fome, sede e regeneração simultaneamente.
    - No instante em que surgir o alerta de fome ou sede, ingerir alimento e bebida imediatamente (`eat <alimento>` e `drink <recipiente>`) para garantir que o próximo tick venha com 100% de regeneração vital.
19. **Tier List de Provisões e Otimização de Carga:**
    - Preferir rações de viagem e frutas mágicas (Sala de Doações) ou pães/tortas comprados na Padaria (Rua Principal Oeste).
    - Manter no máximo 3 a 5 unidades de comida guardadas DENTRO da mochila (`put pao mochila`) para não estourar o limite de peso e não onerar o custo de Movimento (MV).
20. **Doutrina do Acampamento em Campo (Não Recuar Prematuramente):**
    - Não recuar ao Santuário/Templo a cada 1 ou 2 lutas banais; isso queima MV e permite o respawn da área.
    - Estabelecer acampamentos em salas pacíficas ou limpas na própria dungeon (Entrada da Área dos Novatos, Pequena Sala do Guarda Novato ou Campo Aberto).
    - Usar `descansar` (`rest`) para pausas breves com vigilância ativa e interagir com mobília se houver (`descansar banco` / `dormir cama`) para multiplicar a regeneração do tick.
21. **Mecânica Canônica de Portas e Ferrolhos (`open <direction>`):**
    - Portas trancadas ou fechadas que bloqueiam saídas (como ao norte do Cruzamento da Masmorra dos Novatos) **NUNCA** devem ser acionadas com comandos em português (`abrir porta norte` gera *"Como?!?"*) nem com nomes genéricos (`open door north` gera *"Não vejo nenhum door aqui"*).
    - A sintaxe correta e homologada do CircleMUD/DeBo é estritamente **`open <direction>`** (ex: `open north`, `open south`, `open east`, `open west`).
    - O comando retorna *"Certo."* e desobstrui o trânsito da sala imediatamente.
22: **Encerramento Gracioso de Conexão no Bot (`client.close()`):**
    - A classe `DeboClient` implementa o método `.close()` para encerramento de sockets TCP.
    - Jamais invocar `.disconnect()`, garantindo que scripts locais finalizem sem lançar `AttributeError`.
23. **Topografia Bipartida da Masmorra dos Novatos:**
    - A masmorra é dividida pelo Cruzamento central:
      * Ala Sul / Sudoeste: corredores lodosos, câmara de vigia do guarda, covis de monstros e aberrações rastejantes.
      * Ala Norte (acesso via `open north`): *Um Caminho Iluminado*, piso decorado com projetos alquímicos, levando diretamente aos aposentos e missões do Alquimista.
24. **Sinergia Tática de `armor` + `burning hands`:**
    - Sob efeito de `armor`, o dano sofrido contra novatos é praticamente nulo; `burning hands` treinado aniquila monstros fracos em 1 ou 2 turnos.
    - Valores atuais (AC, dano, graus) vivem **somente** em `ficha.md`. Esta skill não os repete.
