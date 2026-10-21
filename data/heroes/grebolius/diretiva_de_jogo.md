# Diretiva de jogo de Grebolius

Regra-mãe: **nunca sair de aventura sem preparo, e nunca lutar do jeito errado.** Isto resume o que os 100 dias ensinaram; cada item tem origem registrada.

## 1. Checklist obrigatório ANTES de sair (o que eu vinha esquecendo)
1. **`stand`** — acordar/levantar antes de qualquer coisa.
2. **`wimpy 30`** — conferir; 30 é o valor vigente (≈38% da vida atual de 79).
3. **`cast 'armor'`** — a armadura arcana é a prioridade nº 1. Repetir até ouvir "Você sente alguém te protegendo". Ela expira: reconferir em `score` (campo [Duração]) e **recastar antes de entrar em zona hostil**.
4. **Comer até "Você está cheio"** — pão recheado custa 6 na Padaria de Midgaard. Fome e sede causam dano direto (-1hp por tick) e impedem recuperação.
5. **Água**: encher o cantil (`fill cantil fonte`) **ou** beber direto da fonte (`drink fonte` → "Você não sente mais sede"). Sem cantil, falta água em viagem longa.
6. **Arma empunhada** (`wield brilhante` = espada de novato, 4D8, +3 acerto/+3 dano — melhor que a do Peão).
7. **Bastão na mão se for usar magia de bastão**: `hold cetro` e então `use cetro` (sanctuary, 5 cargas).
8. **`save`** antes de partir.
9. **Rota definida** (mapa/BFS) e objetivo claro do capítulo.

## 2. Combate — matar rápido e com segurança
- **Antes de atacar, `consider`**. Perigo duro = *suicídio, mataria, menor chance, muito superior, sem chance, massacrado* → **não atacar**.
- **Vida "Você é louco?"** = luta longa (aceitável 1v1 se os outros eixos forem verdes). **Armadura "precisaria de sorte"** = arriscado → evitar ou lutar com sanctuary.
- **Magia de dano: `cast 'burning hands'`** (99%, o melhor dano observado: 12 a 41). `magic missile` (99%) é o reserva barato. `chill touch` (95%) serve para alvos resistentes a fogo. **`shocking grasp` está a 10% — não usar** (candidata a treino).
- **Um comando por vez** sob ameaça. Nunca enfileirar dois ataques com a vida incerta.
- **Parada dura em 60% da vida** em zona densa; **fugir a 40%** (perfil corajoso usa 30%). Depois de um disparo de wimpy, **fuga é emergência**: sair da zona, curar, comer — não reengajar.
- **Nunca lutar em sala com 2+ monstros** sem sanctuary ativo. Com sanctuary, no máximo 2.
- **Atordoamento existe**: a 13 de vida ela não consegue fugir. Por isso a parada é em 60%, não em 30%.

## 3. Magias conhecidas (nível 15) e treino
| Magia | Proficiência | Uso |
| --- | --- | --- |
| armor | 99% | sempre ligada |
| burning hands | 99% | dano principal |
| magic missile | 99% | dano reserva |
| chill touch | 95% | alvos resistentes a fogo |
| invisibility | 97% | infiltração |
| detect invisibility / magic / infravision | 95% | utilidade |
| shocking grasp | 10% | **não usar**; treinar ou ignorar |

**27 sessões de treino disponíveis.** Próximas magias por nível: 16 detect poison, 20 **lightning bolt**, 21 curse, 22 identify. Guardar treino para o lightning bolt ou subir shocking grasp são as opções.

> **2026-10-21 — etiqueta:** tabela de **referência** (fatos do herói), não regra. A única parte
> operativa é "shocking grasp 10%: não usar", e ela não tem check.

## 4. Economia e logística
- **Armeiro de Midgaard compra SÓ armaduras** (paga 8.500 na Armadura da Torre Negra, 150 na do Peão) e **tem caixa limitado**: quando ele diz "caro demais — tente um feiticeiro", é caixa, não item. Tentar vender de novo mais tarde.
- **Feiticeiro (Loja de Magias) compra bastões/cajados**, não armaduras. Também vende pergaminhos (retorno 9.202, remover maldições 8.509, identificação 4.601).
- **`sell [#] <item>`** vende vários; **`value <item>`** cota antes de vender.
- **`recall` é grátis até o nível 70** — usar como saída de emergência.
- **Maldição impede largar/doar**; remover com pergaminho, **recitado fora da loja** (as paredes da loja bloqueiam magia).

## 5. Regras de ouro que custaram caro
- A morte #04 (Dia 100) aconteceu por **insistir no ataque a 13 de vida**: nunca repetir.
- **Morte falha as autoquests** — recomeçar exige voltar ao NPC e responder `sim`.
- **Molhar o pé no desconhecido sem preparo** já matou uma vez (esgotos): não entrar sem armadura, comida e rota de fuga.


## 6. ARMADILHAS MORTais (DT) — regra nova, custou a morte #5
- **DT = armadilha mortal**: mata na hora e pode destruir itens (5% por item na 1ª encarnação). Fonte: `help death`/`help morte`.
- **Aviso de proximidade**: *"Você percebe que há algo perigoso por perto!"* — **PARAR, não andar, e sair por onde veio**. Todo script deve abortar ao ler isso.
- **Ao morrer**: o caminho de volta é achar o **portal escondido** do Paraíso/Inferno que leva ao Purgatório e à **Fonte da Vida** (`drink fonte`). A sala certa traz a dica *"uma curiosa energia mágica... chama sua atenção para o oeste"* → `oeste` → portal → `enter portal` → `norte` até a fonte.
- **Nunca** rodar script de movimento/combate sem supervisão: foi assim que a morte #5 aconteceu (o script andou e lutou sozinho no milharal).
- **Wimpy não salva de DT** e nem sempre salva de atordoamento: subir para **45** e, ainda assim, tratar vida < 60% em zona densa como hora de sair.


> **2026-10-21 — virou default:** o aviso "algo perigoso por perto" passou a abortar em **todo**
> script (`base.PerigoMortal`; `navegar` para com código 7). Antes só o milharal tratava, e as outras
> rotinas andavam para dentro da armadilha.

## 7. Duas regras de magia e covardia (Dia 113, verificadas no servidor)
- **Wimpy tem teto: metade da vida máxima.** Com 87 de vida, `wimpy 45` foi recusado (*"Você não pode ajustar seu nível de covardia acima da metade de seus pontos de vida"*); **`wimpy 43`** foi aceito. Reajustar sempre que a vida máxima subir.
- **O Templo de Midgaard BLOQUEIA magia.** Dentro dele, `cast 'armor'` (e qualquer feitiço) responde *"Sua magia falha e desaparece"*. **Conjurar na Praça do Templo** ou em qualquer sala comum: ali a armadura pegou de primeira.
  - Isso vale também para a **Loja de Magias** (*"as paredes desta sala parecem impedir você"*).
  - Se `armor` falhar fora dessas salas, é azar: **insistir** até *"Você sente alguém te protegendo"*.


> **2026-10-21 — etiqueta:** **referência**. O comportamento já está no código
> (`cuidar.sair_da_area_sem_magia`, `prepara.garantir_armor`); a regra escrita é consulta, não trava.

## 8. SEMPRE `stand` antes de andar (a lição que custou rodadas)
- O jogo recusa movimento enquanto a personagem está **descansando/dormindo**: a resposta é *"Nah... você está muito relaxado.."*. Parece falha de rota, mas é postura.
- **Todo script de deslocamento deve começar com `wake; stand`** — e, de preferência, reconferir depois de qualquer `rest`/`sleep`.
- Isso explica boa parte das "viagens que falhavam" entre os Dias 110 e 122: eu culpava o parser e a rota, quando era a postura.
- Rota curta confirmada para o tabuleiro: `recall` → `stand` → 4 norte (Grande Campo) → oeste (Caminho Sujo) → oeste (Grande Tabuleiro) → oeste (Casa Branca) → norte, norte.


> **2026-10-21 — virou default:** `base.andar` e `navegar` mandam `wake; stand` e repetem o passo
> **uma vez**; a recusa por postura deixou de custar a viagem inteira (antes `navegar` parava com código 5).

## 9. Método de automação — a lição que custou três mortes (Dias 110-140)
> Regra-mãe: **o motor só anda sozinho depois de provar que anda.** Enquanto não provou, cada passo é observado.

**Ordem obrigatória antes de soltar qualquer script:**
1. **Mapear a região à mão primeiro.** Ir e voltar eu mesma, conferindo sala a sala, e só depois escrever o trajeto. Foi assim que o bosque caiu: depois de registrar que a fazenda abre ao norte de uma sala `[norte, sul]` logo após a sala com "O Pequeno Bosque".
2. **Ler `exits` para os NOMES das saídas.** O `look` só mostra "[ Saídas: leste, sul ]", sem destino. Todo navegador que li do lugar errado abortou.
3. **Andar por MARCO, não por contagem.** "Avance até a sala cujo nome é X" resiste à desincronização de lotes; "ande 13 leste" não resiste.
4. **Rodar o motor em trechos curtos e ler o retorno** — viagem, bosque, caçada, um de cada vez — e só juntar quando cada trecho passa sozinho.
5. **Limite dentro do próprio script.** Teto de passos e de tempo; ao estourar, **salvar e sair**. Sem isso ele vira job, e job solto já matou três vezes.
6. **Nunca** deixar caçada em segundo plano. Se o programa estourar o tempo, o script continua sem supervisão e a personagem morre — mortes #5, #6 e #7 vieram todas daí.
7. **Gravar o caminho quando ele funciona** e reproduzi-lo depois (o motor imprime `CAMINHO BOSQUE: ...`).

## 10. Higiene de personagem — hoje é diagnóstico, não regra (2026-10-21)

Os três "relaxamentos" que pareciam bug viraram **estado do vigia** (`TRAVADO`, `MANA_BAIXA`, `FOME`)
e são resolvidos por `cuidar.py`/`prepara.py`: *"muito relaxado"* → `wake; stand` (agora **default** em
`base.andar`, v1.7.17); mana seca → sono; combate fraco → comeu/bebeu. A tabela sintoma→causa está no
[`docs/agentes/glossario.md`](../../../docs/agentes/glossario.md) §11 — duplicá-la aqui era manter duas
cópias, e a do código é a que não envelhece.

O que continua **operativo**:

- `score tudo` antes de cada bloco (peso/limite, ouro, fome, sede) e `equipment` para o que está no corpo.
- **`identify` antes de vestir** e **`consider` antes de atacar**.


## 11. O que é limite do MUNDO, e não da personagem (consolidado 2026-10-21)

Os fatos de comércio (caixa de cada NPC) saíram para o [`conhecimento.md`](conhecimento.md) §85 — fato
do mundo mora lá, não em regra de jogo. Aqui fica o processo:

- **Quando o gargalo é o caixa de um NPC, registrar e parar** — insistir é só gastar rodada.
- **Não fechar capítulo antes dos alvos:** fechar é ato final, não pausa (Dia 136: o capítulo voltou a
  `em_curso` sozinho). Desde 2026-10-21 isso é check: o capítulo (do 12 em diante) declara
  `closing_criteria` e só fecha com `closing.confirmed_with_author`; critério aberto exige **bypass
  explícito do autor** com motivo (`fecho.do_capitulo`).


## 12. Guarda de repetição — o vigia dos robôs (ideia do autor, Dia 143)
> **Se a MESMA resposta vier 3 vezes seguidas, o robô para, salva e devolve o controle.**

Implementado em `scripts/local/guarda.py` e injetado no `run()` de **todos** os robôs de `scripts/local`:
- normaliza a resposta (espaços, quebras e a linha de vitais `113hp 260mn 114mv`) e compara;
- ao atingir **3 repetições**, imprime `[GUARDA] mesma resposta 3x seguidas: ...` (o texto exato, para eu diagnosticar), executa **`recall` + `save`** e sai com código **9**;
- mantém um histórico curto das últimas respostas distintas.

**Por que isso importa:** as mortes #5, #6 e #7 vieram de scripts **insistindo** num estado travado. A repetição é o sinal mais barato de "isto não vai andar" — e agora o robô se cala em vez de teimar até a personagem cair.

**O que dispara:** sala bloqueada (`Você não pode ir por aí`), alvo inexistente (`Em que você deseja lançar a magia?`), personagem descansando (`Nah... você está muito relaxado..`), peso (`Você já está carregando muito peso`), comando inválido (`Como?!?`).

**Teste feito:** enviando 4× um comando inválido, a guarda disparou na **3ª** resposta, salvou e saiu. Confirmado ao vivo.


## 13. Fome e sede matam devagar — e o sono acelera (Dia 147)
- O jogo **consome vida e mana por ciclo** quando a personagem está *"morrendo de fome"*: vi **-2hp, -3mn e -2mv** no log, repetidamente.
- O motor **dormia para recuperar mana** — e dormir faminta é o pior dos mundos: a mana não sobe e a vida cai.
- **Regra**: `abastecer()` **antes** de qualquer sono ou viagem. O motor passou a checar `score tudo`, ir à **Padaria** (pão recheado, 6 moedas), comprar 5, comer 4 e beber do cantil.
- **Sintoma de alarme no log**: `Você está morrendo de fome!` — se aparecer, parar o robô e alimentar.

## 14. Supervisão por minuto (pedido do autor)
- **Nunca** soltar o robô e ir embora: rodar em segundo plano e **ler a cauda do log do daemon a cada ~60 s** (`scripts/local/session_live_*.log`, o mais recente por data de modificação).
- A leitura do log **não interfere** no jogo — diferente de mandar comandos paralelos, que podem desincronizar a sessão.
- Se o log mostrar morte, fome crítica, ou a mesma mensagem repetindo, **matar o job** na hora.
- A **guarda de repetição** já disparou duas vezes em produção nesta rodada: uma em *"Em que você deseja lançar a magia?"*, outra em *"Você não pode ir por aí..."* — o robô parou, salvou e saiu, em vez de insistir.


## 15. Restrição de Armaduras e Maldições (atualizado pelo autor, Dia 156)
> Diretiva original (Dia 150): *"NÃO VAMOS MAIS VENDER ESSAS ARMADURAS, PERDEMOS MAIS DINHEIRO DO QUE GANHAMOS COM ELAS, OK?"*
> Ajuste do autor (Dia 156): *"a armadura de cavaleiro só nao pode se oega por causa da maldição, se nao tiver amaldiçoada, de boa. Ajusta jsso"*
> Esclarecimento do autor (Dia 156): *"não era para ser proibido pegar coisas da torre Negra é proibido só pegar coisas amaldiçoadas... dar um double cheque se for torre Negra verificar se é amaldiçoado"*

Regra vigente ajustada:
- **PROIBIDO:** pegar qualquer item **amaldiçoado** (ex: Armadura da Torre Negra amaldiçoada / itens com flag `ITEM_NODROP` ou maldição). Se pegar um item amaldiçoado, não é possível largá-lo (`drop`) nem doá-lo, ficando preso ao inventário e exigindo pergaminho de remover maldição (8.509 moedas) para liberar.
- **PERMITIDO:** pegar e vender armaduras e equipamentos da Torre Negra, de cavaleiro ou de peão que **NÃO estejam amaldiçoados** (como armaduras limpas encontradas no tabuleiro ou na sala de doação), desde que respeitem o limite de peso e caixa do armeiro/mercador.
- **Identificação prévia OBRIGATÓRIA (dupla checagem no chão):** antes de executar `get` em armaduras da Torre Negra caídas no chão, usar `identify armadura` no chão para confirmar que não possui maldição ou NO-DROP. Se estiver amaldiçoada, NUNCA pegar.
- As rotinas de farm automático devem sempre aplicar essa triagem prévia antes do recolhimento.


## 16. RISCO AUTORIZADO — o Capítulo 06 inverte a regra da fuga (diretiva do autor, Dia 156)

> **"vamos arriscar mais, e tudo bem se morrer"**
> **"a meta é matar tudo que dê pra matar no esgoto, e o que não der, fugir, desviar"**
> **"já aprendi demais, agora é hora de voltar lá e se vingar"**

**Isto REVOGA, para os esgotos, a doutrina que valeu dos Capítulos 03 a 05** — onde fugir era sempre a
vitória e o corpo a corpo estava desligado por precaução.

- **Alvo:** os **Esgotos de Midgaard** (camada `esgotos`, 17 salas mapeadas). **Matar tudo o que for
  abatível.** E isso inclui **o que o Dia 95 mandou contornar**: a **Serpente dos Esgotos** e o
  **Aligátor** — e o **Covil do Dragão** (`borda_estreita_sul`).
- **O que não der para matar:** **desviar ou fugir**, e seguir. **Não** insistir até morrer à toa — isso
  não é coragem, é desperdício de rodada.
- **Morrer é aceitável.** Não é falha de execução; é custo previsto. **Mas** as regras de segurança
  continuam valendo: `stand` antes de andar, `score` antes de agir, e `save` — **nunca `quit`**.
- **O que NÃO muda:** §15 (proibido pegar itens amaldiçoados; Torre Negra permitida se limpa com pré-checagem), §6 (armadilhas mortais — **DT continua sendo o
  único risco que o `wimpy` não segura**, e é por isso que o brinco ANTI-DT importa), e a proibição de
  `quit` com missão em andamento.
- **A justificativa narrativa é dela, e vai para a crônica:** a morte já não a atinge como antes; a
  memória tem ficado mais clara e ela só perde o que aprendeu **recentemente**; o poder que ela carrega a
  protege — **por enquanto**. *"Quem quer ser rainha não pode ficar parada."*

**Rota de entrada e saída (verificada no Dia 95, e a única de mão dupla):**
`O Depósito de Lixo` (a partir da `Praça Comum`, `n`) → **`d`** → *A Junção Quádrupla Abaixo do Depósito
de Lixo* → e **`u`** volta. **NUNCA descer pelo buraco do Laboratório dos Magos** — aquela queda é de
mão única.


## 17. A camada de FICÇÃO sobre morte e memória (movida em 2026-10-21)

O texto completo está em [`notas_editoriais.md`](notas_editoriais.md), e o registro canônico continua em
`capitulos.json` → capítulo 6 → `directive.fiction_layer`. Esta seção não é regra de jogo; é instrução
editorial para a crônica.

Em uma linha: **é adaptação deliberada do metajogo, não fato do servidor.** Pode narrar a morte como
perda do aprendizado recente; **não pode** afirmar imunidade a morte como fato, e **não usa número cru**
de XP/HP/mana.


## 18. A Mochila de Pellinore — Contêiner Mágico de Redução de Peso (Bag of Holding)

- **Natureza do Item:** `a mochila de Pellinore` é um contêiner encantado com propriedade de `weight_reduction`. Conforme comprovado pela carta de Merlin em seu interior (*"Usando esta mochila, o peso dos itens que você carregar irá diminuir. Assim, você poderá viajar longas distâncias sem se cansar"*), itens guardados nela têm seu peso efetivo no inventário drasticamente reduzido.
- **Importância Vital para Grebolius:** Grebolius é maga de Força 11 (limite máximo de 115 kg). Com a `Armadura da Torre Negra` pesando 60 kg e os demais equipamentos vestidos somando ~25 kg, resta uma margem minúscula de carga livre. A mochila é o que permite carregar reservas de armadura (como a OME de 2.250 ouros), chifres de minotauro, comida e espólios sem sobrecarga.
- **Diretrizes Operacionais:**
  1. **Proibição Absoluta de Perda:** A mochila **NUNCA** deve ser vendida, doada, largada (`drop`) ou descartada (`junk`).
  2. **Armazenamento Ativo:** Toda rotina e agente deve guardar espólios e rações imediatamente com `put <item> mochila`.
  3. **Controle de Carga:** Manter a carga total sempre abaixo de 110 kg para preservar mobilidade e fôlego em trânsito e combate.

## 19. PROTOCOLO OBRIGATÓRIO DE ENTREGA DE ITENS E AUTOQUESTS (Diretiva Urgente do Autor, Dia 156)

> **"Tem que atualizar urgente que sempre temos que ver a situacao da missao antes de dar itens , ja oerdemos itens demais !!!"**

O comando `give <item> <npc>` é estritamente irreversível no motor MUD. Se executado quando a missão não estiver no passo exato ou se houver diálogo concorrente, o NPC simplesmente consome o item sem disparar a recompensa/avanço.

### Checklist Obrigatório ANTES de Qualquer `give`:
1. **Conferência em `score tudo`:**
   - A autoquest alvo **DEVE** constar sob o cabeçalho `[Autoquests em andamento]`. Se o cabeçalho estiver vazio ou a missão estiver apenas em `autoquest listar` (disponível), **NÃO ENTREGAR**. Reativar com o NPC inicial primeiro.
   - O texto descritivo do objetivo no servidor deve ser exatamente a etapa de entrega (ex: *"Você deve entregar objeto ao personagem"*).
2. **Isolamento de Diálogos Concorrentes:**
   - **NUNCA** responder `say sim` ou interagir com saudações de outras quests do NPC antes da entrega.
   - Exemplo clássico observado: ao entrar na Sala do Alquimista com a poção aquosa (para Gargamel), o Alquimista diz *"Ei, você poderia me ajudar?"*. Responder `say sim` ativa a autoquest própria dele (*Limpando Monstros*), fazendo com que ele consuma a poção sem entregar o *jarro brilhante*.
3. **Conferência de `inventory`:**
   - Garantir que o item está no inventário principal da personagem (e não guardado dentro da mochila de Pellinore ou ausente). Se estiver na mochila: `get <item> mochila`.
4. **Validação Imediata Pós-Entrega:**
   - Executar `inventory` e `score tudo` logo após o `give`. Se o item de troca não for recebido ou o texto da missão não mudar, interromper a automação imediatamente e registrar no log.

## 20. DIÁLOGOS DE MISSÃO COM NPCS NUNCA SÃO AUTOMATIZADOS (Diretiva do Autor, Dia 156)

> **"falar com npc quando envolve missões, nunca é feito automatizado e sim por resposta direto do agente ao contexto, para evitar dar merda"**

Falar com NPC quando envolve missões (`say`, `ask`, `whisper`, `tell`, gatilhos verbais de missão) **NUNCA é feito de forma automatizada por script**, e sim exclusivamente por **resposta direta do agente ao contexto em tempo real**.

### Motivo da Diretiva ("Para evitar dar merda"):
Scripts cegos ou com tempos fixos (`sleep`) que disparam comandos verbais em lote causaram erros graves na campanha:
1. **Atropelamento de falas longas:** NPCs de autoquest frequentemente têm falas em múltiplos passos; o script dispara a próxima fala antes de receber a instrução completa.
2. **Aceitação acidental de missões concorrentes:** Na presença de NPCs com múltiplas quests (como o Alquimista ou em salas públicas), disparar `say sim` automaticamente faz a personagem entrar em outra missão indesejada, travando ou quebrando o fluxo da missão principal.
3. **Perda de itens valiosos:** Emitir falas automáticas seguidas de `give` sem confirmar a resposta textual exata do NPC fez com que itens caros (como poções de 9.750 moedas) fossem consumidos sem retorno.

### Protocolo Operacional Obrigatório:
1. **Separação de Papéis:** O motor ou script pode apenas **navegar** até a sala do NPC e **eliminar ameaças hostis imediatas** na sala (se houver combate).
2. **Parada Mandatória:** Chegando diante do NPC, a automação para. Nenhum comando de fala é enviado por lote.
3. **Controle Consciente pelo Agente:** O agente operando ao vivo:
   - Lê o texto integral da fala do NPC;
   - Consulta a situação exata da missão em `score tudo`;
   - Confere os itens no `inventory`;
   - Avalia o contexto e responde manualmente com o comando verbal exato exigido pelo servidor (`say <termo>`, etc.).

## 21. ESTAR NA ETAPA CERTA PARA FAZER A COISA CERTA (Diretiva do Autor, Dia 156)

> **"Vamos reforçar na documentação que temos que estar na etapa certa para fazer a coisa certa"**

### O Princípio Fundamental:
No Devil's Bob MUD, quests automáticas possuem máquinas de estados rígidas no servidor. Uma ação mecanicamente correta (como entregar uma poção, comprar um item ou falar uma palavra-chave) torna-se catastrófica se executada **fora da sub-etapa exata**.

### O Caso Real da Poção Aquosa (Várias poções perdidas, ~30.000 moedas):
- Ao longo do Dia 156, múltiplos agentes compraram `uma poção aquosa` por 9.750 moedas em Clariss e foram entregar ao Alquimista com a missão `Uma Lição em Gargamel` aberta no `score tudo`.
- O Alquimista consumiu as poções uma a uma sem entregar `o jarro brilhante`.
- **Causa Raiz Comprovada ao Vivo:** O Smurf Minerador em *O Fim Do Túnel* não havia completado sua fala de direcionamento (*"Converse com o novato alquimista... Estarei te esperando com o que preciso."*). Por consequência, o Alquimista não havia formulado sua pergunta-chave (*"Deixe-me adivinhar: você quer um jarro brilhante, certo?"*). O servidor mantinha a autoquest apenas como `Uma Lição em Gargamel` (etapa genérica/incompleta), sem aceitar a entrega do item de troca!
- **A Virada Definitiva:** Assim que o agente foi ao Minerador, aguardou pacientemente cada linha de sua fala até o encerramento, e em seguida foi à Sala do Alquimista responder conscientemente `say Grebolius` -> `say sim`, o servidor mudou formalmente para:
  ```text
  [Autoquests em andamento]
     Uma Lição em Gargamel: Você deve entregar objeto ao personagem.
  ```

### Regras de Ouro Operacionais:
1. **Gatilho de Compra:** Jamais gaste moedas de ouro em itens de missão caros (> 1.000 moedas) antes que a missão esteja formalmente ativada e na etapa exata de requisição daquele item.
2. **Gatilho de Entrega (`give`):**
   - O `score tudo` **TEM** que exibir os dois-pontos e a instrução exata da etapa:
     `Uma Lição em Gargamel: Você deve entregar objeto ao personagem.`
   - Se estiver apenas `Uma Lição em Gargamel` sem sub-etapa, **É PROIBIDO DAR GIVE**. O NPC engolirá o item sem retorno.
3. **Paciência com Falas de NPCs:** NPCs do MUD possuem intervalos de 3 a 8 segundos entre falas. Nunca emita `recall` ou comandos seguintes antes da mensagem final de fechamento do diálogo.

## 22. A POSTURA HEROICA DE GREBOLIUS: ÉTICA PROATIVA E PRESERVAÇÃO DA MORAL (Diretiva do Autor, Dia 156)

> **"Eu não queria que fosse só uma ação reativa, acho que o reativo é o double check. Eu acho que tem que também ter uma postura, uma postura um pouco mais heroica. De forma mais genérica, não fazer o mal, não bater em pessoas, não bater em animais. Se eu mandar alguma coisa que mande fazer isso, você me questiona. Quando você for criativo, você toma esse cuidado, porque eu não quero matar um bicho para descobrir que fiz errado. Eu queria que você olhasse para o cachorro e visse um cachorro, um animalzinho inocente e indefeso."**

### 1. Postura Heroica Proativa (O Olhar da Heroína):
A moralidade de Grebolius não é gerida por planilhas ou medições frias; ela é guiada pela **conduta heroica de uma maga elfa do bem**:
- **Empatia com o mundo vivo:** Ao avistar um cachorro, gato ou animalzinho no cenário, o agente e a personagem devem ver exatamente isso: *um animalzinho inocente e indefeso*. Jamais reduzi-los a "mobs de teste" ou alvos de estatística para bater meta de missão.
- **Não fazer o mal:** É proibido agredir cidadãos pacíficos, camponeses, transeuntes, guardas da cidade ou animais indefesos. O combate é reservado a monstros hostis, invasores, feras carnívoras e criaturas comprovadamente malignas.
- **Criatividade com discernimento moral:** Ao receber diretivas para criar planos mirabolantes ou caçar alvos inéditos, o agente deve agir com integridade. **É expressamente proibido abater uma criatura para "descobrir depois" se era pecado.** Se houver dúvida ou o alvo parecer inocente, não atacar.

### 2. O Dever de Questionar o Próprio Autor:
- **Exceção mandatória ao princípio geral "execute, não pergunte":** Se o autor Peter, por distração, teste pontual ou instrução acidental, ordenar atacar pessoas inocentes, maltratar animais indefesos ou cometer atos vis, o agente **NÃO DEVE EXECUTAR ÀS CEGAS**. O agente **TEM A OBRIGAÇÃO DE QUESTIONAR O AUTOR**, alertando sobre o impacto moral e a quebra da postura heroica antes de agir.

### 3. O Double Check Reativo (Rede de Segurança):
O monitoramento mecânico do alinhamento moral atua apenas como última camada de contingência:
- Sempre que uma ação inesperadamente resultar em **redução da pontuação de alinhamento moral** (visível na barra compass `{<<<<<>----}` e valor numérico no `score` / `score tudo`):
  1. **PARADA IMEDIATA:** Interromper imediatamente o script ou rotina em execução.
  2. **AUDITORIA DE CAUSA RAIZ:** Averiguar o log para isolar a causa exata.
  3. **NÃO REPETIR:** Banir permanentemente o alvo ou ação de qualquer plano futuro.





## 23. RITUAL ANTES DE CADA BLOCO DE JOGO: script ou à mão? (Dia 157, Claude Sonnet 5.5)

> Nasceu de uma cobrança do autor: *"não tinha nenhuma diretiva de saber quando usa scripts e quando joga respondendo cada linha?"* Tinha (§9, §14, §20), e foi ignorada: rota conhecida andada sala a sala, comando recusado repetido, recuo a pé com 50 de vida. Ler a regra uma vez não basta; ela precisa ser cobrada **antes de cada bloco**.

**Antes de enviar o próximo bloco de comandos, responda as quatro perguntas:**

| Pergunta | Se sim | Se não |
| --- | --- | --- |
| 1. A rota está no `mapa.json`? | **script**: `python automato/camadas/navegar.py --para <id>` (confere o nome de cada sala, para em combate, recusa, vida baixa ou sala inesperada; recusa salas `danger` sem `--permitir-risco`) | andar **à mão**, um passo por vez, lendo `exits`; depois **gravar a rota no mapa** (§9.1) |
| 2. Há NPC de missão ou item de missão na jogada? | o script **só navega até lá e para**; fala, `give` e compra são **à mão**, linha a linha (§20, AGENTS #14), com `score tudo` confirmando a etapa (§21, AGENTS #13) | script livre dentro dos limites da §9 |
| 3. Alguém está lendo o log ou o retorno a cada passo? | seguir | não soltar o script (§14); sem `turno.py`, o laço de leitura é seu |
| 4. O que eu faço se a vida cair? | `recall` ao primeiro golpe grave. **Não** recuar andando: recuar de duas salas custou ~150 de vida | definir antes de entrar |

**Sinais de que a regra está sendo quebrada** (o auditor pega todos, ver abaixo): o mesmo comando recusado 3 vezes seguidas; `give` sem `Você deve entregar objeto` no último `score tudo`; `say`/`ask` em rajada ou em lote; `quit`; `get all` ou `get` sem `identify`; ataque sem `consider`; alinhamento caindo; andar com vida abaixo de 45%.

**Conferência mecânica, depois da sessão:** `python scripts/auditar_sessao.py` (sem argumentos lê o transcript mais recente). Código 1 = há FALHA; 2 = só AVISO. Um AVISO pede explicação no plano; uma FALHA pede correção ou justificativa. **Limite honesto:** o transcript não registra se o comando veio de script ou de mão, então §9 (andar por script) e §14 (supervisão) **não** são auditáveis daí. Por isso a pergunta 1 acima é de quem joga.

> **Nota datada (2026-10-20, Claude Opus 5.5, driver v1.7.9):** o limite acima caiu. O transcript agora grava a `origem` de cada comando (`play` = à mão; `navegar`, `xadrez_cascata`, `turno:<rotina>` = script). O auditor dá **FALHA** com mais de 80 passos ou 30 ataques pelo `play.py` numa sessão (`andar-a-mao`, `caca-a-mao`), e `ataque-sem-consider` virou FALHA. Caça e XP vão por `turno.py --rotina <x>`; mapear área nova à mão: `$env:MUD_ORIGEM='mapear'`. Uma FALHA do auditor se corrige com código, não com justificativa: a partir do plano 041 o `devolutiva.py` cobra (`plano.falha_justificada`). Motivo: `observacoes/revisao-10-dias-2026-10-20.md`.


> **Correção datada (Dia 158, 2026-10-20, Claude Sonnet 5.5) ao §18 — medida ao vivo:** a mochila de Pellinore **só reduz o peso quando está VESTIDA** (slot *sobre o corpo*, o mesmo do manto de pano: `remove manto`, `wear mochila`). Na mão, o conteúdo pesa cheio (4 lanças: 123 kg, acima do teto de 115; vestida: 50 kg). O `put` **não enxerga** a mochila vestida ("Não há nenhuma mochila aqui"); o fluxo é **`remove mochila` → `put <item> mochila` → `wear mochila`** (`base.guardar_na_mochila()`). Detalhes em `conhecimento.md` §68.

## 24. PEGAR OS ESPÓLIOS DOS CORPOS IMPORTA (cobrança do autor, Dia 158)

- **Pegar os itens dos corpos é parte do trabalho**, não só o ouro (o ouro vem sozinho). Depois de cada
  abate importante, olhar o corpo (`look in corpo`) e o chão da sala.
- **A única trava é a maldição** (AGENTS #10, §15): `cast 'identify'` no objeto **antes** do `get`; flag
  `AMALDIÇOADO`/`NODROP` = deixar. Use seletor numerado (`get 2.armadura`) quando duas coisas partilham
  a palavra.
- **Destino dos itens:** política de venda, doação e o caixa de cada NPC estão no
  [`conhecimento.md`](conhecimento.md) §85.
- **Verificação no código:** `config.ESPOLIOS_PROIBIDOS`/`ESPOLIOS_LIMPOS`, `base.espolio_proibido()`,
  `base.guardar_na_mochila()` e a triagem de `rutinas/xadrez_v3.py`.


## 25. COMPRAS ACIMA DE 5% DO OURO SÓ COM PERMISSÃO; `armor` NA ROTINA DE PREPARO; KITE SÓ COM O REI DORMINDO (diretivas do autor, Dia 157)

> *"não compre nada que seja mais que 5% do ouro que temos sem me pedir (diretiva MUITO IMPORTANTE)"* · *"armor dura HORAS ... poderia estar em outra rotina, tipo, que nem comer e tudo, sempre verificar se está com armor, e não no script de atacar"* · *"no kite, se o sleep falhou, tem que sair, curar e tentar de novo, não dá pra começar a luta sem ele dormir"*

- **Compra > 5% do ouro total (mão + banco): perguntar ao autor antes**, dizendo item, preço, motivo e risco. Vale para "comprar só para identificar". Custou caro no Dia 157: dois Cetros de Bispo (22.999 cada) que não serviam (o Negro é ANTI-BOM; bastão não protege quem usa). O lojista recomprou um por 3.000 e se recusa a recomprar bastão usado.
- **`armor` fica no preparo**, como comida e água: `prepara.garantir_armor()` lê a CA do `score tudo` e relança se ficar abaixo de 140 (112 sem a magia, 148 com ela). O Templo bloqueia magia, então o lance é na Praça. O script de ataque não lança `armor`.
- **Kite no Rei:** se o `sleep` falhar, `recall`, curar e tentar de novo; nunca iniciar a luta com ele acordado. Um raio por ida (`kite_rei`).
- **Vender as lanças:** o ferreiro continua sem caixa ("Eu não posso pagar por uma arma dessas!"); o ouro gasto na Loja de Magias não chega a ele.

## 26. OS CINCO MODOS DE JOGAR (diretiva do autor, Dia 157 — 2026-10-20)

> *"não ficar esquecendo as mecânicas que a gente tem; se vai mudar a forma de jogar, analisa, justifica e muda, mas não fica inventando sem base... montamos uma estrutura de fluxo importante que deve ser obedecida e não contornada"* · *"tudo que é novo deve entrar na estrutura de forma estruturada"* · *"andar por aí em caminho conhecido já temos; explorar já temos; modo matar um monte de bicho já temos"*

**Antes de cada bloco, declare o modo.** Se a intenção não cabe em nenhum dos cinco, não invente um sexto: pare e proponha ao autor, com número.

| Modo | Intenção | Dono (a ferramenta) | Proibido neste modo |
| --- | --- | --- | --- |
| **caminhar** | chegar a um lugar que o `mapa.json` já tem | `camadas/navegar.py --para <id>` | rota conhecida andada passo a passo; parar fora do previsto |
| **explorar** | descobrir área nova | à mão, um passo por vez, gravando a rota no mapa | atacar sem `consider`; sair sem gravar a rota (§9.1) |
| **moer** | matar muito / XP | `camadas/turno.py --rotina milharal_v2\|novatos` | laço em PowerShell; caça à mão (§23) |
| **missão** | fala de NPC, `give`, compra | à mão, linha a linha | qualquer automação de fala (#14) e `give` sem a etapa (#13) |
| **chefe** | tática contra alvo já enfrentado | roteiro medido antes: `mandabala.py --sobre <alvo>` | tática nova sem medir; entrar com vida < 100 |

**O portão de sobrevivência (a) vale nos cinco modos.** Antes de sair, `cuidar.py` come, bebe e veste `armor` — e agora `navegar.py` e `turno.py` o chamam **antes** de sair, não no meio do caminho. Se falta pão ou água, o bloco **para** e quem recarrega é o `prepara.py`; não se contorna indo assim mesmo. Fome e sede **cancelam a recuperação de vida no sono** (medido: `morrendo de fome! (-3hp, -6mn)`), então passar fome não é incômodo, é perda de vida.

**O sono tem alvo, não tempo.** `prepara.dormir()` mira a vida (~5 hp/min medidos; ~45 min para a barra cheia de 226, ~3 min para a mana). Dormir 75 s fixos devolvia mana e deixava a vida faltando.

**O que é novo entra estruturado (c):** ferramenta, rotina ou modo novo só entra com linha na tabela "Ferramentas" do `automato/README.md`, decisão em `automato/DECISOES.md`, ID em `docs/agentes/catraca.json` e teste em `scripts/test_*.py`, no mesmo commit. Sem isso, é invenção sem base e o `check_project.py` acusa.

**Verificação no código:** `navegar.cuidado_antes()`; `turno.py` (socorrer antes do laço); `auditar_sessao.py` (`fome-em-sessao`, `sede-em-sessao`, `armadura-ausente`); `mandabala.pre_voo()`.
