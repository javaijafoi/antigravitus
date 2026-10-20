# Verificações da máquina — 15/10/2026

## Identify: gratuito nas condições observadas

`identify anel` revelou propriedades do anel. Ouro permaneceu 612 e mana 170 antes/depois, com Grebolius no nível 11 da primeira encarnação. Não foi necessário aprender a magia de nível 22. `identificar anel` respondeu “Como?!?” no perfil atual em inglês.

`help identificar` descreve o comando disponível “até o nível 80 da primeira encarnação”. `help identify` descreve a magia e fala em comando “abaixo do nível 80”. Portanto: uso gratuito confirmado no nível 11; acesso descrito até perto do 80; inclusão do nível 80 e custo em outros níveis não testados. Não afirmar que Grebolius aprendeu a magia.

O anel identificado exige nível 90 e encarnação 3 e modifica INT, WIS e CON em +1 e mana máxima em +116, segundo a resposta de identificação. Continua no inventário: identificação não comprova que pode ser equipado agora.

## Tips e encerramento

Última resposta a `tips`: “Você verá as dicas do jogo.” O alias temporário de leitura foi removido, e o terminal retornou a 22 linhas e 80 colunas. Último score: dormindo, 67/67 HP, 170/170 mana, 101/101 MV, 612 moedas, AC 19, sem efeito armor listado e sem alerta de fome/sede. Save respondeu “Salvando os seus atalhos.” antes e depois de dormir; a conexão foi fechada.

A consulta foi técnica, sem deslocamento ou combate. Foram consumidos os dois pães que restavam após o Dia 91 e água do cantil. Inventário final não tem pão: repor comida antes da próxima viagem. A crônica e as evidências do encerramento do Dia 91 continuam representando aquele momento anterior.

O score técnico não exibiu seção de autoquest. Não houve confirmação de cancelamento ou conclusão de Problemas Agrícolas: conservar o último registro conhecido e conferir a situação na próxima sessão autorizada.

## Corrigir após testar

Ao observar divergência: registrar data, comando, alvo, condição relevante, resposta literal e fonte; atualizar só a orientação prática afetada. Ajuda, hipótese e teste são categorias distintas. Preservar os anexos importados.

[Comparação resumida](comparacao_commands.md) · [Evidências selecionadas](evidencias/consulta_2026-10-15.json).

## Atualização — caçada dos Dias 92–93

Os resultados anteriores de manutenção permanecem históricos. Após a caça, equipamentos e recursos mudaram; o Dia 93 foi interrompido, sem confirmação de encerramento. Consultar [aprendizados da caçada](aprendizados-cacada-92-93.md) e a ficha atual antes de assumir que Grebolius continua dormindo ou sem armor. Identify funcionou para itens carregados e recusou itens ainda vestidos (“Você não tem nenhum…”); as identificações de peças antigas foram feitas após removê-las.

## 2026-10-16 — comandos na continuação do Dia 156

Fonte: [evidence/dia156e.json](../data/heroes/grebolius/evidence/dia156e.json). Agente: GPT-6 / Codex (versão específica não informada).

- `help where` documentou localização de monstro/jogador da mesma área. `where minotauro`, `where perturbador`, `where tagarela` e `where confuso` localizaram alvos. `where 2.novato` até `where 7.novato` repetiram o primeiro resultado; não tratar como enumeração. `where chato` não encontrou; a chave real observada foi perturbador.
- `buy 6 pao` comprou seis unidades por 36 moedas. `put all.punhal mochila` guardou oito punhais; `look in mochila` confirmou os oito.
- Diálogo de missão é literal: `say retornar` foi reconhecido pelo confuso, enquanto `say recall` não acionou a resposta. `say ajuda remortar` foi reconhecido pelo esperto. Isso não invalida recall como comando de deslocamento, que funcionou na mesma sessão.
- Entrega antes da etapa pronta: `give veste tagarela` tirou a veste do inventário sem avançar; quando score tudo passou a pedir entregar objeto, uma segunda entrega gerou “Você atingiu seu objetivo”. Esperar a cadência do NPC e conferir a etapa.
- Catálogo `autoquest todas` guardava conclusão histórica de Limpando Monstros enquanto o ciclo reiniciado permanecia ativo em score tudo. Fim do ciclo confirmado por recompensa atual e remoção do objetivo no score, não apenas pelo catálogo.

## 2026-10-16 — `onde` é documentado e **não existe**; `where` sozinho lista jogadores

Fonte: sessão ao vivo do Dia 156 (Templo de Midgaard, nível 21). Agente: `deepseek-flash`.

**Corrige e amplia a entrada acima**, que registrou `where <nome> / onde <nome>` como equivalentes.

- **A ajuda documenta um comando que o servidor recusa.** `help where` responde com o cabeçalho
  **`4.3.5 ONDE WHERE`** e a linha **`Uso: onde <monstro ou jogador>`** — mas:
  - `onde` (sem argumento) → **`Como?!?`**
  - `onde minotauro` → **`Como?!?`**
  - `where` (sem argumento) → **`Jogadores na sua área`** seguido da lista
  - `where tagarela` → **`Ninguem com esse nome.`**
  **O servidor só aceita o verbo em inglês.** A entrada anterior do dicionário registrou os dois como
  equivalentes porque leu a ajuda, não o teste — é exatamente a distinção que o `AGENTS.md` §4.1 faz
  entre *ajuda* e *teste executado*.
- **`where` sem argumento tem comportamento próprio:** lista **os jogadores da área** (cabeçalho
  `Jogadores na sua área`), e não os monstros. Com argumento, localiza **monstro ou jogador** — e apenas
  **dentro da área**, como a própria ajuda explica.
- **O escopo é a área, não o mundo.** `where tagarela` respondeu `Ninguem com esse nome.` estando no
  Templo, onde a tagarela de fato não está. **Isso não é falha do comando** — é o limite documentado.
- **Precedência aplicada:** resposta real do servidor > ajuda do DeBo. Aqui as duas discordam, e a
  divergência fica registrada em vez de resolvida em silêncio.

## 2026-10-16 — o alerta de armadilha mortal, o `consider` **"Você é LOUCO!"** e o Dragão de um turno

Fonte: [evidence/dia156f.json](../data/heroes/grebolius/evidence/dia156f.json) — incursão aos Esgotos
de Midgaard. Agente da coleta: **`Gemini 3.8 Flash`**; registro aqui feito por `deepseek-flash`, porque
**ele não tocou neste arquivo** e são achados de referência de servidor, não fatos do mundo.

**Estes três achados existiam só em prosa (`conhecimento.md` §38) — que é onde o código não lê.**

- **Existe um AVISO PRÉVIO de armadilha mortal, e ele é do servidor.** Na sala do `Passo-Em-Falso`, o
  jogo emite: **`Você percebe que há algo perigoso por perto!`** — e **nada mais** acontece até a
  personagem pisar. Isso muda o tratamento de DT no motor: hoje o `RISCO_A_EVITAR` do `config.py` é uma
  **lista de salas escrita à mão**, mas o servidor **avisa em tempo real**. Vale investigar se o aviso é
  genérico (qualquer DT) ou específico daquela sala — **não foi testado**.
- **`consider` tem um rótulo acima de `danger`: `Você é LOUCO!`.** Dois NPCs o receberam —
  **Clodoaldison**, o advogado de divórcios do submundo (`Um Escritório Pouco Iluminado`, ao norte de
  `O Poço Escuro`), e os **3 besouros gigantes** que dormem abaixo do poço. **A escala conhecida até
  aqui parava em `danger`;** este rótulo é novo e **não foi calibrado** — não se sabe se indica nível
  muito acima, imortalidade ou apenas recusa de avaliação. **Clodoaldison é pacífico** (não atacou).
- **O Dragão Vermelho do Covil abate 135 HP em um único turno** — a vida máxima dela no nível 21.
  Mecânica exata **não** confirmada: pode ser dano fixo alto, morte por script ou efeito especial.
  Mensagem observada: **`rasga sua jugular com uma mordida`**, seguida de `< Morto >`. Ele habita
  `A Borda Estreita (Covil do Dragão)` e tem **aura multicolorida**. **Não é alvo de nível 21.**
- **O inventário SOBREVIVE à morte.** Depois da Morte #8, *"todos os itens e equipamentos foram
  preservados"* e ela os revestiu com `wear all` no Templo. Isso responde a uma dúvida antiga do
  registro: **a morte custa experiência, não equipamento.**
- **A ressurreição é automática**, pelo fluxo do `Paraíso` até a `Fonte da Vida`, terminando no Templo
  de Midgaard — **sem comando do jogador**. Já era sabido (§ do Dia 111); reconfirmado aqui.

## 2026-10-16 — `Problemas Agrícolas`: briefing completo do Pacificador, `score tudo` entre etapas e `um belo cinturão de rodeio`

Fonte: [evidence/dia156g.json](../data/heroes/grebolius/evidence/dia156g.json). Agente: `Gemini 4 Argon`.

- **Sair da sala antes do fim da fala do NPC trava o gatilho da etapa seguinte.** Após `say sim` para `O Pacificador`, ele emite 13 linhas espaçadas por vários segundos (terminando em `O Pacificador exclama: 'Se esquecer o caminho, digite HISTÓRICO DIZER. E vá encontrar o fazendeiro!'`). Quando a personagem saiu da sala antes da 13ª linha, `[Autoquests em andamento]` exibiu apenas `Problemas Agrícolas` (sem dois-pontos nem objetivo) e `O dono da fazenda` permaneceu mudo na fazenda. Ao permanecer na sala até a 13ª linha terminar, `O dono da fazenda` falou imediatamente ao vê-la entrar em `A Sala de Estar`.
- **Em `Problemas Agrícolas`, concluir a cota das Etapas 1, 2 e 3 NÃO altera o `score tudo` nem imprime aviso de objetivo concluído.** Durante as três primeiras etapas (10 `um monstro invasor`, 10 `um monstro esfomeado` e 5 `um monstro agressivo`), o `score tudo` permanece estático em `Problemas Agrícolas: Você deve matar criaturas.` mesmo após o 10º/5º abate. O avanço ocorre exclusivamente ao retornar à sala onde está `O fazendeiro` (`A Sala de Estar` ou `A Entrada da Casa`) e aguardar ~10–16 segundos pelo disparo do *mobprog*. Apenas na Etapa 4 (1 `o líder dos monstros`) o texto muda para o singular (`Problemas Agrícolas: Você deve matar criatura.`) e o abate imprime `Você já atingiu este objetivo.`.
## 2026-10-16 — `Uma Lição em Gargamel`, políticas de comércio de Jareth e Conquista 34 ("Cai Fora!")

Fonte: [evidence/dia156h.json](../data/heroes/grebolius/evidence/dia156h.json). Agentes: `Gemini 4 Argon` (sessão de jogo) / `Gemini 3.8 Flash` (encerramento e handoff).

- **Políticas de compra de lojistas em Jareth e Midgaard:**
  - `A Loja de Armaduras de Maris` (Ilena) avalia armaduras de qualidade (ex.: `armadura de metal da OME` avaliada em 2.250 moedas), mas recusa a compra com a resposta: **`Desculpe, mas eu não compro de forasteiros.`**. Porém, comprou `luvas de couro` por 37 moedas.
  - `A Loja de Armas de Maris` (Maris) e `Dalston Tralhas e Cia` (Elias Dalston): avaliam armas/itens, mas recusam compras com **`Eu não compro!`**.
  - `A Loja de Trapos da Vovó` (Granny): recusa atendimento a magos com **`Nós não trabalhamos para sua classe aqui!`**.
  - `A Loja de Armaduras de Midgaard`: possui limite rígido de caixa por dia/ciclo. Comprou o `peitoral de couro` por 200 moedas, mas recusou a armadura da OME com a mensagem: **`Isso é caro demais para mim - Tente um feiticeiro!`**.
- **Conquista 34 ("Cai Fora!"):** Desbloqueada ao interagir com o capitão aposentado em `As Margens do Rio` com `value barco`: o capitão responde **`O capitão aposentado exclama: 'Volte mais tarde!'`** seguido pelo anúncio de conquista **`* Você desbloqueou a conquista 34: Cai Fora! Que tal guardar segredo e deixar que os outros a descubram por conta própria?`**.
- **Preços em `As Misturas de Clariss` (Jareth):**
  - `Uma poção amarela de detectar invisibilidade` (nível 10): 4.605 moedas de ouro.
  - `Uma poção aquosa` (nível 10, item de quest do Alquimista): 9.750 moedas de ouro.




## 2026-10-17 — respostas intercaladas e histórico de morte

Agente: GPT-6 / Codex (versão específica não informada). Fonte: [dia156j](../data/heroes/grebolius/evidence/dia156j.json). Transcript72663a: linha202 entrega recompensa do Alquimista sob eat pao,com consumo em preroll203;274 recebe DICA para exits,saídas em idle275;300 recebe saídas para n,chegada em preroll301/look302. Prompt isolado não confirma a semântica esperada. Conter por sala/saídas/objetivo e não repetir comando de risco por resposta incompleta. Palavra morte em histórico ou relato não equivale a morte atual; consultar estado real. Não houve alteração do código do driver nesta reconciliação.

## 2026-10-17 — Sub-etapas de Autoquest em `score tudo` (Invariante 13)

Fonte: [evidence/dia156n.json](../data/heroes/grebolius/evidence/dia156n.json). Agente: Gemini 3.8 Flash (High).
- No DeBo, a listagem de uma autoquest sob `[Autoquests em andamento]` não indica prontidão para entrega. O servidor possui sub-etapas discretas:
  - Quando a quest está apenas aceita (etapa 0), o título aparece sozinho sem instruções adicionais. Entregar (`give`) neste estado resulta na perda do item sem avanço da missão nem recebimento de recompensa.
  - Apenas após a cadeia de diálogos e ativações necessárias ser concluída (ex: Minerador monologar completamente e Alquimista dialogar com identificação), o servidor altera o cabeçalho para exibir a instrução de etapa:
    `[Autoquests em andamento] Uma Lição em Gargamel: Você deve entregar objeto ao personagem.`
  - A presença da string literal `: Você deve entregar objeto ao personagem.` é a confirmação técnica de que o servidor habilitou o manipulador de entrega do NPC.

## 2026-10-18 — `identify` como comando, consider de Gargamel/Azrael e propriedades do Colar Púrpuro

Fonte: [evidence/dia156o.json](../data/heroes/grebolius/evidence/dia156o.json). Agente: `Gemini 3.8 Flash (High)`.

- **`identify` opera como comando até o nível 80:** Invocar `cast identify colar` acarreta falhas ("Sua magia falha e desaparece") ou requer sintaxe de magia. O comando direto `identify colar` é gratuito, não consome mana e retorna imediatamente a ficha completa do objeto carregado.
- **Vereditos de `consider` em *O Covil de Gargamel*:**
  - `Gargamel`: Nível: "Muito fácil!", Vida: "É uma perda de tempo", Poder: "Você tem PROBLEMAS!?", Precisão: "Muito fácil!", Armadura: "Fácil!". O veredito indica poder de ataque bruto elevado se acertar, mas precisão e vida irrisórias contra um personagem de Nível 31 com CA 138.
  - `Azrael`: Nível: "Muito fácil!", Vida: "É uma perda de tempo", Poder: "Fácil!", Precisão: "Fácil!", Armadura: "Fácil!". Mob completamente inofensivo.
- **Eficácia de `cast 'sleep'` em chefes de missão:**
  - Gargamel não possui imunidade a sono arcano: `cast 'sleep' gargamel` (95% proficiência) colocou-o para dormir na primeira tentativa, concedendo +1.200 EXP e neutralizando completamente qualquer contra-ataque. Em seguida, um único `cast 'lightning bolt' gargamel` desferiu 66 de dano e encerrou a luta (+1.080 EXP), sem nenhum ponto de vida perdido por Grebolius.
- **Propriedades mecânicas de `um colar com uma pedra púrpura`:**
  - Objeto: Tipo ARMADURA, slot PEGAR PESCOÇO, Peso 1, Valor 20.000.000, Nível 10, Encarnação 1.
  - Flags: `BRILHO MÁGICO ABENÇOADO NÃO-VENDER ANTI-DT ENTALHADO`.
  - Modificadores: Armadura +10, Acerto +1, Dano +1, Destreza +1, Máx-Mana +25.
  - O personagem possui 2 slots de pescoço no DeBo e pode vestir a coleira do dragão concomitantemente ao colar púrpuro.

## 2026-10-18 — Mecânica do Sono Arcano (`sleep`) e Dano, Agressividade da Rainha Negra e Pets da Pet Shop

Fonte: [evidence/dia156p.json](../data/heroes/grebolius/evidence/dia156p.json). Agente: `Gemini 3.8 Flash (High)`.

- **Sono Arcano (`sleep`) e Dano Não Letal:** No CircleMUD/DeBo, uma criatura colocada para dormir via `cast 'sleep'` permanece adormecida até expirar ou sofrer dano. Se o dano infligido NÃO for letal (ex.: um único raio de 65 de dano num `besouro gigante` com mais de 300 HP), a criatura acorda imediatamente no mesmo turno de combate e contra-ataca com fúria total! Grebolius tomou 190 pontos de dano instantâneo e foi salva a 6 HP pelo recuo de emergência `wimpy 45` pela escada de ferro. Contra alvos com vida massiva, `sleep` não serve para ataque direto a menos que haja dano concentrado capaz de encerrar o combate em um golpe.
- **Agressividade no Tabuleiro de Xadrez (Rank 8):** Ao contrário dos peões passivos dos ranks inferiores, peças reais como `A Rainha Negra` atacam à vista assim que o personagem entra na sala. O recuo via `flee` funciona, mas o rank 8 exige extrema cautela.
- **Comportamento de Animais de Estimação (`Loja de Animais`):** Criaturas adquiridas na Loja de Animais (`buy gatinho`, `buy cachorrinho`, `buy beagle` por 300 moedas cada; `buy rottweiler` por 900 moedas) tornam-se pets seguidores automáticos. Elas acompanham o jogador por comandos de movimento. Uma vez fora da cidade em campo aberto (ex.: `O Grande Campo de Midgaard`), é possível atacá-las e abatê-las livremente sem intervenção de guardas urbanos ou repercussão de crime, concedendo EXP (+252, +288, +522 e +810 EXP respectivamente) e qualificando-as como abates válidos no registro de caça do MUD (embora sumariamente rejeitadas para heróis de alinhamento bom).
- **Distribuição de Mobs e Saques nos Kobolds de Jareth:**
  - `where lider` localizou com precisão o líder kobold (`o líder kobold - Um Amplo Salão`) a partir da caverna.
  - Veredito `consider` para kobolds e para o líder kobold no nível 31 é "É uma perda de tempo" (fácil).
  - Saques observados: `um ladrão kobold` (100 moedas), `um kobold` (60 moedas), `o líder kobold` (160 moedas, carregando no cadáver uma lâmina improvisada e um escudo pequeno).
  - Geografia de perigo: A caverna ao norte de Jareth possui saída norte logo na entrada (*Entrando na Caverna*) que leva a *Um Pequeno Abismo* (queda/risco de DT). A rota segura para os kobolds segue ao sul (*Avançando na Caverna*) e depois a oeste.

## 2026-10-18 — Nobreza das Sombras do Xadrez, Rato de Esgoto Gigante e Escala Moral de Alinhamento

Fonte: [evidence/dia156p.json](../data/heroes/grebolius/evidence/dia156p.json). Agente: `Gemini 3.8 Flash (High)`.

- **Nobreza das Sombras no Tabuleiro de Xadrez (Rank 4):**
  - `O Cavaleiro Negro` (Casa Branca): Veredito `consider`: Vida "Você é LOUCO!", Poder "Perfeito!". Resiste a 2 raios e tomba no 3º raio. Rendimento: **23.298 EXP** e **300 moedas de ouro**.
  - `O Bispo Negro` (Casa Preta): Veredito `consider`: Vida "Você é LOUCO!", Poder "Você precisaria de muita sorte!". Alta resistência arcana, necessitou de 4 descargas de raio (`lightning bolt`) e 1 golpe marcial de finalização. Rendimento: **17.810 EXP** e **500 moedas de ouro**.
  - Ambos são passivos na entrada da sala (não agram imediatamente), permitindo preparação de feitiços pelo atacante.
- **Rato de Esgoto Gigante em *O Poço Escuro* (Esgotos de Midgaard):**
  - Criatura com veredito `consider` de Vida "Você é LOUCO!" (Nível: Muito fácil). Necessitou de 3 descargas de `lightning bolt` consecutivas. Rendimento extraordinário: **27.868 EXP** e 30 moedas de ouro.
- **Dinâmica Matemática de Alinhamento Moral:**
  - O abate de criaturas inequivocamente malignas e de alta experiência nos esgotos e no exército das sombras elevou o alinhamento moral de Grebolius de 198 para **311** (`{<<<<<>>---} Você é bom`), confirmando que a eliminação do mal no DeBo MUD atua como alavanca mecânica direta de virtude arcana.

## 2026-10-18 — Hipótese Técnica a Testar: Sono Arcano (`sleep`) como Controle de Multidão (CC) contra Múltiplos Alvos

- **Hipótese formulada pelo autor Peter:** A magia `sleep` pode ser empregada como mecânica de controle de multidão (CC) para converter encontros 2v1 em dois combates sequenciais 1v1.
- **Protocolo de Teste Proposto:**
  - Em sala com dois monstros hostis (ex.: *Curva Lamacenta* nos esgotos com dois monstros da lama):
    1. Entrada na sala e conjuração imediata de `cast 'sleep' 2.monstro` (ou no alvo secundário).
    2. Combate direcionado estritamente ao monstro acordado (`kill monstro`, `cast 'lightning bolt' monstro`), sem nenhuma magia de dano em área.
    3. Inspeção do estado do segundo monstro durante e após a morte do primeiro.
    4. Eliminação do segundo monstro adormecido ou recuo estratégico caso o sono expire prematuramente.
- **Questões mecânicas abertas a verificar:**
  - Se a morte de um monstro na mesma sala acorda o parceiro adormecido no DeBo/CircleMUD ou se ele permanece dormindo até sofrer dano direto.
  - Imunidade ou resistência a sono (`save vs spell`) em criaturas do tipo monstro da lama/elementais.
  - Duração do sono com Grebolius no nível 31 (420 mana).

## 2026-10-18 — Autoquests de Nível 30+ no DeBo: `Xeque-mate` e `Ajuda Mágica`

Fonte: [evidence/dia156j.json](../data/heroes/grebolius/evidence/dia156j.json:1022) (`autoquest listar`). Agente: `Gemini 3.8 Flash (High)`.

- **Desbloqueio de Autoquests ao Atingir o Nível 30:**
  - `Xeque-mate`: Requisito: A partir do nível 30, qualquer alinhamento. Desenvolve-se no Grande Tabuleiro de Xadrez.
  - `Ajuda Mágica`: Requisito: A partir do nível 30, qualquer alinhamento.
  - O catálogo do DeBo MUD remove automaticamente de `Autoquests Disponíveis Futuramente Nesta Encarnação` as missões cujos requisitos de nível forem preenchidos, movendo-as para `Autoquests Disponíveis Agora:`.
## 2026-10-18 — Protocolo Técnico de Verificação: Comandos e Mecânicas Inéditas de CircleMUD/DeBo

Fonte: Consolidação das referências `maquina/commands.md` e `docs/circlemud/04-especiais-easter-eggs.md`. Diretiva do autor Peter.

- **Comandos Arcanos a Testar (Grebolius Nível 31 / 420 Mana):**
  - `cast 'detect alignment'`: Verificar sintaxe no DeBo, custo de mana e se a aura exibida no `look` discrimina claramente azul/branca (bem) de vermelha (mal).
  - `cast 'detect invisibility'`: Verificar detecção de itens ocultos e ladrões invisíveis.
  - `cast 'sense life'`: Verificar mensagem e eficácia em salas escuras.
  - `cast 'locate object <item>'`: Verificar se o servidor responde a localização exata de itens do catálogo.
  - `cast 'blindness' <alvo>`: Testar contra peça negra no xadrez e observar redução de capacidade combativa do oponente.
- **Comandos de Economia e Sobrevivência:**
  - `cashcard`: Comprar no Empório (item 3036) e testar comandos `balance`, `deposit` e `withdraw` em trânsito fora do Templo de Midgaard.
  - `donate <item>`: Testar envio de item dispensável e verificar se chega à sala de doação do Templo.
  - `junk <item>`: Testar descarte destrutivo e registrar retorno de moedas ou EXP.
  - `taste` e `sip`: Testar ingestão fracionada em fonte e cantil.
  - `pour`: Testar transferência e esvaziamento de recipientes de líquido.
  - `diagnose`: Testar diagnóstico clínico em combate para aferição qualitativa de HP.
  - `track <monstro>`: Testar sintaxe de busca e rastro em zonas conhecidas.
- **Sistemas de Mensagens:**
  - MMS nos Correios (sala 3062): testar `check`, `receive` e sintaxe de `mail`.
  - Murais comunitários: testar `read 1` e leitura de tópicos na Praça do Comércio.

## 2026-10-18 — Comportamento do Servidor DeBo: Cancelamento de Autoquest por Morte e por Quit

Fonte: Captura literal do log de combate contra o Rei Negro em `automato/runtime/session_live_dia156_20261018_124258_79991b.log:11259` e verificação de desconexão voluntária.

- **Morte em Combate:**
  - Resposta literal do servidor ao atingir 0 HP:
    ```text
    Você está morto!
    Você perdeu 4.173 pontos de experiência pela sua morte.
    *Você falhou em sua aventura! Se quiser concluí-la deverá recomeçá-la!*
    ```
  - Efeito mecânico: cancela a aventura ativa e remove-a da lista `[Autoquests em andamento]`. O progresso nas etapas da missão é zerado (deve-se reiniciar com o patrono), mas o nível, equipamentos, vitais e ouro permanecem intactos.
- **Comando `quit`:**
  - O comando `quit` (ao contrário de `save` seguido de fechamento de socket) executa a rotina de encerramento de sessão que limpa os slots de autoquest ativa exibindo: `*Você falhou em suas aventuras! Se quiser concluí-las deverá recomeçá-las!*`.
- **Conclusão:** Autoquests falham **tanto na morte quanto no `quit`**. Para preservar autoquest ativa entre pausas, deve-se usar `save` e repouso (`sleep`), nunca `quit`, e evitar mortes em combate.

## 2026-10-18 — Localização Canônica de Autoquests (`help autoquest`) e Rota de Notre Dame (`help notre dame`)

Fonte: Sessão ao vivo via `automato/runtime/session_live_dia156_20261018_173435_612baf.log`. Agente: `Gemini 3.8 Flash (Medium)`.

- **Mapeamento de Patrono e Zona via `help autoquest`:**
  - O comando `autoquest listar` exibe apenas o nome da missão e o NPC iniciador, sem indicar a zona.
  - O comando `help autoquest` lista as 51 aventuras do servidor com seus respectivos patronos e áreas.
  - Entrada 44: `44) Ajuda Mágica: Lemin (Notre Dame)`.
  - Prova cabal de que Lemin **não está em Midgaard**, mas na zona de Notre Dame/França.
- **Rota Oficial para a França (`help notre dame`):**
  - O tópico oficial documenta a travessia a partir do Templo de Midgaard:
    - `s` -> Praça do Comércio -> `w` pela Rua Principal até `Trilha em Meio a Floresta`.
    - `Caminho Sombreado Através da Floresta` -> primeira saída a oeste -> `Bifurcação no Caminho` -> `n`, depois `w`.
    - No Caminho Sombreado -> `n` até `Densa Floresta Entre as Colinas` -> leste (`e`) até a `Entrada Para a França`.
- **Cotação Mercantil de Itens Especiais (`value coroa`):**
  - O Armeiro de Midgaard comprou a `Coroa da Rainha Negra` (ANTI-GOOD, valor 3.000 moedas de catálogo) por exatamente 1.500 moedas de ouro (50% do valor de face).



## 2026-10-19 — Dia 157: Lemin, locate object e proteções

Agente: GPT-6 / Codex (versão específica não informada). Fonte: data/heroes/grebolius/evidence/dia157-cap12.json e transcript citado.

- **where Lemin executado:** mostrou Lemin no Centro da Cidade, em Lyon. Esse uso localiza NPC na região; where sem argumento havia mostrado apenas jogadores.
- **Ajuda Mágica executada parcialmente:** convite por look lemin; resposta Merlin aceita após pergunta integral. Primeira resposta prematura não avançou. Pedidos de sim aparecem na ficha; monólogos longos não devem ser truncados. Etapa de entrega confirmada com dois-pontos e instrução específica; nenhum give foi feito.
- **locate object testada:** conjuração em nível 32 recusada por falta de experiência. help locate informa Mago nível 34 e necessidade de espelho localizador. Isso é ajuda consultada, não execução bem-sucedida ao 34 nem compra testada.
- **Armor/invisibility executadas:** score no nível 32 mostrou armor +36 e invisibility +40; CA base 89 passou a 165. Não atribuir o total somente a armor. Durações decrescem; último score: armor 2 horas, invisibility 9 horas.
- **Saída leste/castelo:** ajuda omite salas intermediárias; trajeto observado passa pela Entrada da Cidade, Intersecção e Estrada do Rei antes de Fora do Castelo e ponte ao norte. Abrir portão norte funcionou; porta leste da Escadaria Principal estava trancada.
- **Diagnóstico de driver:** dead_or_menu apareceu com personagem viva, 199 HP, sem combate e prompt normal. A janela contém histórico de login ou dica citando Menu Principal; look e score limpos voltaram a in_game. Causa completa e correção permanecem pendentes; não ignorar alerta sem auditar.


## 2026-10-19 — Dia 157 (sessão Claude): where por zona e fuga por recall

Agente: Claude Sonnet 5.5 (claude-sonnet-5-5). Fonte: data/heroes/grebolius/evidence/dia157-biblioteca.json.

- **where <nome> só vê a zona atual:** `where bibliotecaria` respondeu "a Assistente de Bibliotecária - A Biblioteca" nas ruas de Jareth e "Ninguem com esse nome" dentro do castelo do Lorde; a forma acentuada "bibliotecária" também falhou. Hipótese operacional, vista em quatro tentativas, não lida em ajuda.
- **recall em combate funcionou:** duas vezes, com 49 e 50 de vida, a personagem voltou ao Templo sem perda de itens. Nenhuma falha vista (sorte não excluída).
- **Fugir andando tem custo:** recuar de uma sala com dois malandros arruaceiros hostis gastou ~150 de vida em três passos; preferir `recall` assim que a vida cair, em vez de andar.
- **open <direção> é suficiente para portas sem tranca no castelo de Jareth** (norte e sul do Grande Salão, norte do Saguão, oeste do corredor, norte do quarto de hóspedes, norte do fim do corredor leste).

## 2026-10-19 — Dia 157 (Plano 033): mapas de ajuda, lojas comuns e where como radar

Agente: Claude Opus 5.5 (claude-opus-5-5). Fonte: data/heroes/grebolius/evidence/dia157-biblioteca-paris.json.

- **`help mapas` e `help mapa <n>` existem e dão rota:** a lista tem 33 regiões (2 = Jareth, 19 = Notre Dame, 29 = Torre da Magia). `help mapa 2` descreve o Caminho de Tábuas (onde está a Biblioteca) e `help mapa 19` cita Lyon e o bosque de Champs Elysées. Ajuda consultada; as rotas de Jareth e de Paris foram depois percorridas.
- **`list <número>` em loja comum não inspeciona:** na Pergaminhos e Afins respondeu "Por enquanto, nada disto está sendo vendido." Só na loja dos deuses (`autoquest loja`) ele mostra os atributos (conhecimento §32.2). `buy #<número>` funcionou ("Você comprou um rolo de pergaminho").
- **`list` fora de loja:** "Você não pode fazer isto aqui!" (Biblioteca de Jareth, Cabana em Lyon).
- **`look <npc>` pode disparar a fala de missão do NPC:** `look bibliotecaria` casou com a assistente, que respondeu "Eu preciso de ajuda! Pode me ajudar? Sim?". Olhar não aceita missão, mas exige não responder em seguida.
- **`where <nome>` revela salas fora do mapa:** em Notre Dame devolveu "o padre Tintoreto - A Pequena Capela" e "o corcunda - O Campanário da Catedral" antes de qualquer caminhada.
- **O Templo de Midgaard bloqueia magia (de novo):** três `cast 'armor'` responderam "Sua magia falha e desaparece"; na Praça do Templo, "Você sente alguém te protegendo". Já constava na diretiva §7; a repetição foi erro de método, não divergência do servidor.
- **`identify` sobe com o uso:** "Você sente seu 'identify' melhorar." na primeira conjuração bem-sucedida da sessão.

## 2026-10-19 — Dia 157 (Plano 034): autoquest listar, Sala de Doações e títulos do Portão Oeste

Agente da sessão: Claude Haiku 5.5 (claude-haiku-5-5); registro de Claude Opus 5.5 (claude-opus-5-5). Fonte: data/heroes/grebolius/evidence/dia157-handoff-lyon.json e automato/runtime/transcript_dia157_20261019_220653_b7ecb1.jsonl.

- **`autoquest listar` mostra a missão perdida como disponível:** com Ajuda Mágica fora do `score tudo`, a lista trouxe "Ajuda Mágica: Até o nível 45, iniciada com: Lemin." em *Autoquests Disponíveis Agora*. Serve para confirmar que a missão precisa ser reaceita.
- **Sala de Doações de Midgaard bloqueia magia:** `cast 'identify' livro` → "Certo. / Sua magia falha e desaparece." duas vezes, a mesma resposta do Templo.
- **`ask <npc> <palavra>` pode não ter resposta nenhuma:** `ask lemin ajuda` devolveu só o eco "Você pergunta para Lemin: 'ajuda'". Lemin responde à cadeia de olhar/aceitar/responder (conhecimento §61), não a `ask`.
- **Títulos reais do Portão Oeste:** "Rua Principal" (fim da Rua Principal de Midgaard), "Dentro do Portão Oeste de Midgaard", "Fora do Portão Oeste de Midgaard". Os nomes curados do mapa diferiam e travavam o `navegar.py`; agora são `aliases`.

### 2026-10-20 · Claude Sonnet 5.5 (claude-sonnet-5-5) · Autoquests e driver
- Convite de autoquest vem por temporizador do NPC (ex.: "Lemin questiona: ..."), nao por `look`. Resposta: `say sim`. Fonte: session_live_dia157_20261019_220653_b7ecb1.log:542 e transcript_dia157_20261019_235647_9b90bf.jsonl.
- `where <nome>` funciona para mobs (mostra so a primeira ocorrencia) e nao para objetos.
- `detect alignment`, `detect evil` e `detect good` sao de clerigo; mago recebe "Voce ainda nao tem experiencia". Nao ha forma gratuita de ver aura; pista indireta: flag ANTI-MAU ou ANTI-BOM nos itens (`identify`).
- `recall` em combate: UMA sessao achou nao confiavel (respostas defasadas por 2 clientes no driver); outra (conhecimento §68) confirmou que funciona. Tratar como funcional e conferir com `look`. Movimento comum e bloqueado em combate ("muito ocupado"); `flee` custa EXP. O driver traz ao Templo abaixo de wimpy 45.
- `sleep` nao pode ser relancado em combate ("Voce nao tem tempo de se concentrar!", conhecimento §68).
- Dois clientes no mesmo driver devolvem respostas defasadas e `look` incoerente; conferir antes de conectar.
