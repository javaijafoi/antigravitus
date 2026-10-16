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
