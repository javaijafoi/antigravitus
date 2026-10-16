# Textos das missões do Capítulo 05 e do Andarilho — Dia 156

> **Para que serve este arquivo.** O autor pediu *"todos os textos da missão do novato"* e não entendeu
> o ponto do déjà vu. Aqui estão **os textos literais**, separados por origem, sem interpretação minha
> no meio — a leitura é sua.
>
> **Fonte:** transcript `automato/runtime/transcript_dia156_20261016_172506_15eb57.jsonl` (sessão de
> hoje) e comandos ao vivo.

---

## 1. 🔴 O DÉJÀ VU — não é da missão. É o ANDARILHO MISTERIOSO

O texto **completo**, como apareceu de uma vez (registro 4727 do transcript), enquanto ela estava com
fome e sede no corredor da Área dos Novatos:

```
Você está morrendo de fome! (-2hp, -3mn e -2mv)
Você solta um gemido agudo ao sentir seu corpo consumindo a si próprio pela falta de alimento... [-2]
Você está morrendo de sede! (-2hp, -3mn e -2mv)
Sua garganta parece secar, enquanto você sente seu corpo desidratando! [-2]
Energias obscuras podem ser sentidas vindas de Uma Cela de Prisão.
QUE PRESENÇA ASSUSTADORA!! Digite AJUDA ANDARILHO
```

**E a ajuda que o próprio jogo mandou ler — `help andarilho`:**

```
ANDARILHO MISTERIOSO

De tempos em tempos um misterioso andarilho surge no mundo de Devil's Bob.
Seu poder é tamanho que é possível sentir de qualquer lugar a obscura
presença que o acompanha, gerando visões e alucinações que fazem até os
maiores e corajosos aventureiros questionarem a própria sanidade.

Não se sabe muito sobre ele, mas durante os períodos de sua permanência
em nosso mundo você receberá mensagens que revelam sua sombria aparição.

Caso você seja capaz de encontrá-lo, esteja preparado para enfrentar
temidas criaturas das trevas e disposto a arriscar sua vida e alma.
```

**O que isso é, em termos simples:**

| | |
|---|---|
| **O que é** | Um **evento de mundo recorrente** ("de tempos em tempos […] surge") |
| **O que ele faz** | Emite **visões e alucinações** de qualquer lugar — **inclusive dentro de Midgaard e da Área dos Novatos** |
| **Como se acha** | Pelas **mensagens** que ele emite. A de hoje apontou **"Uma Cela de Prisão"** |
| **O que esperar** | **Criaturas das trevas** — *"arriscar sua vida e alma"* |
| **Comando de consulta** | **`help andarilho`** — `ajuda andarilho` responde `Como?!?` (só o verbo em inglês) |

> **O "déjà vu" que eu citei era a frase introdutória** — *"Por um instante, algo parece chamar sua
> atenção para Uma Cela de Prisão. Deve ter sido apenas um déjà vu."* — que é a **versão suave do
> aviso**. Quando o evento se intensifica, a mesma sala vem com *"QUE PRESENÇA ASSUSTADORA"*.
>
> **Ou seja: eu estava lendo um evento de mundo como se fosse pista da missão.** Eram coisas
> diferentes que apareceram juntas.

**"Uma Cela de Prisão" não está no mapa nem nos `docs/circlemud`** — é sala do DeBo, não do CircleMUD
padrão. **Para achá-la, é exploração nova.**

---

## 2. MISSÃO — "Novela dos Novatos"

### 2.1 O que o catálogo diz

```
Novela dos Novatos:
    Até o nível 30, iniciada com: o novato esperto.
```

### 2.2 O objetivo, no `score tudo`

```
[Autoquests em andamento]
Novela dos Novatos: Você deve dizer algo ao personagem.
Limpando Monstros: Você deve matar criatura.
```

**A missão quer que ela DIGA algo a um personagem.** É a única instrução que o servidor dá.

### 2.3 Como ela foi iniciada

```
say oi   -> Você diz: 'oi'
say sim  -> Você diz: 'sim'
            Você começa a participar da aventura.
```

### 2.4 Todos os novatos que aparecem — e as frases exatas do jogo

Na **A Sacada** (sala onde a missão começou) foram vistos **quatro novatos diferentes**, cada um com
uma descrição de presença distinta:

| Frase exata do jogo | Quem é (pelos `docs/circlemud`) |
|---|---|
| *"Um novato esta aqui e ele **aparenta estar bem confiante**."* | **Smart Newbie (18615)** — "o novato esperto" |
| *"Um novato está aqui, **perturbando você**."* | Annoying Newbie (18611) |
| *"Um novato **está perdido** aqui."* | Lost Newbie (18614) |
| *"**Uma novata** está aqui, **falando muito**."* | Friendly Newbie (18613) — vista em A Sala da Estátua |

> **Nenhum deles fala.** Mesmo a novata, que a descrição diz que "fala muito", **não emite fala
> nenhuma** — seis leituras seguidas de `look` e nada.
>
> **E nenhum reage** a: `say oi`, `say sim`, `say ajuda`, `say novela`, `say livro`, `say problema`,
> `ask novato <tópico>` (testado com 9 tópicos), `give veste/punhal/adaga novato`.

### 2.5 As descrições completas das salas onde eles ficam

**A Sacada** (18645):
```
A Sacada
   Ao observar daqui é possível perder de vista o olhar. Construída em
um semi-círculo em volta da cúpula da sala, a sacada permite que você veja
o exterior para quase todas as direções. Observando ao sul, você pode ver
a grande cidade de Midgaard livre ao sudoeste.
[ Saídas: norte e baixo ]
```

**A Sala da Estátua** (18640):
```
A Sala da Estátua
   Aqui, o corredor entra em uma pequena sala. Saídas seguem ao sul e ao
leste, e você vê uma magnífica, enorme (e lindamente acabada) estátua
ao norte.
[ Saídas: leste e sul ]
```
*(Nos `docs/circlemud`, a estátua desta sala traz a dedicatória: "Maynard, Death Jester of the
Harlequins".)*

**Um Caminho Iluminado** — a sala que deu a dica, com o texto completo:
```
Um Caminho Iluminado
   ...
   ...para que mantenha essa sala deve mesmo agradar os novatos.
```

### 2.6 O que eu NÃO tenho

- **Não sei qual personagem** a missão quer que ela cumprimente
- **Não sei qual frase** ele espera
- **Não sei se é um novato** ou outro NPC qualquer

---

## 3. MISSÃO — "Limpando Monstros"

```
Limpando Monstros: Você deve matar criatura.
```

**Iniciador:** O Novato Alquimista, em **A Sala do Alquimista**. Iniciada com `say sim`.
**Ele não responde** a `say`/`ask`/`give` — é contador de abate puro.

**O que cai dos monstros que ela mata** (textos literais):

```
Você queimou o monstro novato até morte!
O monstro novato está morto!
Você recebe 414 pontos de experiência pelo dano causado.
Seu sangue congela ao ouvir o grito de morte do monstro novato.
Você pega um punhado de moedas de ouro de dentro do corpo de o monstro novato.
Havia 20 moedas.
```

**Na sala, o próprio jogo marca o alvo:**
```
O monstro novato está aqui. MATE-O! MATE-O!
```

---

## 4. A frase que resolveu o bloqueio de seis rodadas

Do `docs/circlemud`, a correspondência entre os mobs da zona 186 e as salas:

```
| Smart Newbie (18615) | 18645 | leva Sleeves, Leggings, Vest, Mace |
| Annoying Newbie (18611) | 18646 | — |
| Friendly Newbie (18613) | 18640 | leva Vest |
| Lost Newbie (18614) | 18604 | — |
```

E a correspondência `sacada_norte` / `sacada_sul` → `18643 / 18645`.

---

## 5. Resumo do que confundiu

| Eu achei que era | Na verdade é |
|---|---|
| O déjà vu apontava para a missão dos novatos | É o **evento do Andarilho Misterioso**, que emite avisos de qualquer lugar |
| "Uma Cela de Prisão" seria sala da zona 186 | **Não está no mapa nem no CircleMUD padrão** — é sala local, ainda não encontrada |
| A novata "falando muito" diria algo | **Ela não fala nada** — a descrição é de atmosfera |
