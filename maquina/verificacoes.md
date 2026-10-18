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


