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


## 7. Duas regras de magia e covardia (Dia 113, verificadas no servidor)
- **Wimpy tem teto: metade da vida máxima.** Com 87 de vida, `wimpy 45` foi recusado (*"Você não pode ajustar seu nível de covardia acima da metade de seus pontos de vida"*); **`wimpy 43`** foi aceito. Reajustar sempre que a vida máxima subir.
- **O Templo de Midgaard BLOQUEIA magia.** Dentro dele, `cast 'armor'` (e qualquer feitiço) responde *"Sua magia falha e desaparece"*. **Conjurar na Praça do Templo** ou em qualquer sala comum: ali a armadura pegou de primeira.
  - Isso vale também para a **Loja de Magias** (*"as paredes desta sala parecem impedir você"*).
  - Se `armor` falhar fora dessas salas, é azar: **insistir** até *"Você sente alguém te protegendo"*.


## 8. SEMPRE `stand` antes de andar (a lição que custou rodadas)
- O jogo recusa movimento enquanto a personagem está **descansando/dormindo**: a resposta é *"Nah... você está muito relaxado.."*. Parece falha de rota, mas é postura.
- **Todo script de deslocamento deve começar com `wake; stand`** — e, de preferência, reconferir depois de qualquer `rest`/`sleep`.
- Isso explica boa parte das "viagens que falhavam" entre os Dias 110 e 122: eu culpava o parser e a rota, quando era a postura.
- Rota curta confirmada para o tabuleiro: `recall` → `stand` → 4 norte (Grande Campo) → oeste (Caminho Sujo) → oeste (Grande Tabuleiro) → oeste (Casa Branca) → norte, norte.


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

## 10. Higiene de personagem — os três "relaxamentos" que parecem bug
| Sintoma | Causa real | Correção |
|---|---|---|
| *"Nah... você está muito relaxado.."* | a personagem está **descansando**; o jogo recusa andar | **`wake; stand`** antes de qualquer deslocamento |
| Caçada com muitos *"inconclusivo"* | **mana seca** (chegou a 10 de 240); a magia falha | **`sleep` ~80 s** antes de sair (20 → 218 de mana) |
| Combate fraco e regeneração ruim | **fome e sede**: "morrendo de fome!" | comer na **padaria** e beber do **cantil** a cada ciclo |

Outras conferências de rotina: `score tudo` (peso/limite, ouro, fome, sede), `equipment` (o que está no corpo), `identify` **antes** de vestir, `consider` **antes** de atacar.

## 11. O que é limite do MUNDO, e não da personagem
- O **armeiro de Midgaard** tem bolso finito: paga ~3 armaduras de 8.500 e seca. O **feiticeiro** não compra armaduras nem bastões usados. O **ferreiro** compra armas.
- Quando o gargalo é o **caixa de um NPC**, registrar e parar — insistir é só gastar rodada.
- **Não fechar capítulo antes dos alvos:** fechei o Capítulo 2 no Dia 136 com a fortuna parcial, e o próprio sistema devolveu o capítulo para `em_curso`. Fechar é ato final, não pausa.


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


## 15. PROIBIDO vender armaduras (diretiva do autor, Dia 150)
> **"NÃO VAMOS MAIS VENDER ESSAS ARMADURAS, PERDEMOS MAIS DINHEIRO DO QUE GANHAMOS COM ELAS, OK?"**

Regra permanente e vale para todas as temporadas:
- **Nenhuma** rotina de venda de armaduras — nem as da **Torre Negra** (8.500), nem as de **peão** (150);
- **Não** comprar o pergaminho de remover maldições (8.509) com a intenção de vender a armadura;
- A rotina **`xadrez` foi suspensa** e guardada em `scripts/local/rotinas/_suspensas/` (nao reativar sem ordem expressa);
- Os scripts antigos `farm_armaduras.py` e `ciclo_peao.py` ficam **igualados a suspenso**.

**Onde buscar ouro, então:** espolio de combate, recompensas de missao/autoquest, itens unicos e o **banco do Templo** (que já guarda 7.032). Nada de transporte de armadura.


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
- **O que NÃO muda:** §15 (proibido vender armaduras), §6 (armadilhas mortais — **DT continua sendo o
  único risco que o `wimpy` não segura**, e é por isso que o brinco ANTI-DT importa), e a proibição de
  `quit` com missão em andamento.
- **A justificativa narrativa é dela, e vai para a crônica:** a morte já não a atinge como antes; a
  memória tem ficado mais clara e ela só perde o que aprendeu **recentemente**; o poder que ela carrega a
  protege — **por enquanto**. *"Quem quer ser rainha não pode ficar parada."*

**Rota de entrada e saída (verificada no Dia 95, e a única de mão dupla):**
`O Depósito de Lixo` (a partir da `Praça Comum`, `n`) → **`d`** → *A Junção Quádrupla Abaixo do Depósito
de Lixo* → e **`u`** volta. **NUNCA descer pelo buraco do Laboratório dos Magos** — aquela queda é de
mão única.
