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
- **Recompensa verificada (`identify cinturão` e comparação empírica de `score tudo`):** `um belo cinturão de rodeio` (Tipo: `ARMADURA`, Flags: `BRILHO`, Peso: `5`, Valor: `1250`, Nível: `15`, Slot: `CINTURA`) aplica `CA -12` na convenção interna do CircleMUD (medido no `score` do DeBo como **+22 CA**: `112 -> 134`), **+5 Acerto** (`5 -> 10`), **+5 Dano** (`2 -> 7`), **+1 Destreza** (`15 -> 16`) e **+1 Carisma** (`11 -> 12`).

