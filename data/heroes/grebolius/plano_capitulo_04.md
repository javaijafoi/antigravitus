# Plano do Capítulo 04 — "O Levantamento"

> **Título proposto, pendente do autor.** "Modo Cartógrafa" é nome de ferramenta, não de
> capítulo — a diretiva proíbe metajogo nas descrições. Alternativas: *"Aquilo que Se Vê Sem
> Ser Vista"*, *"A Carta Invisível"*, *"Os Olhos que Ninguém Vê"*.

**Goal do capítulo:** levantar o mundo inteiro **sem travar um único combate** — entrar no
desconhecido em invisibilidade, anotar cada sala e cada perigo, e **voltar viva todos os dias**.
A morte não é o preço do mapa; é a falha do método.

**Estado:** **aguardando** o fecho do Capítulo 03 ("Três Ofícios"), que está em curso.
**Não abrir antes.** O Capítulo 03 é do outro agente; este documento não toca nele.

**Gatilho que legitima o capítulo** (doutrina da skill, seção 2): o Capítulo 03 é feito de
caçadas repetidas no milharal — incide o gatilho *"dois dias seguidos de tarefas repetitivas"*.
Além disso, o **Dia 160** é marco decenal (*"dias terminados em zero exigem expansão
intencional de horizontes"*). O capítulo abre entre o 157 e o 160.

**Justificativa dentro do mundo (não é capricho):** duas missões do Capítulo 03 ficaram sem
pista de **onde** acontecem — *Novela dos Novatos* (procurar "o novato esperto" nas
encruzilhadas) e *Uma Lição em Gargamel* (procurar "o smurf minerador" em minas e colinas).
Levantar o terreno é a forma de achar as duas. O mapa é o subproduto; a missão é a busca.

---

## 1. Doutrina do capítulo — o que NÃO se faz

| Proibição | Por quê |
|---|---|
| **Não conjurar magia de dano.** Nenhuma. | O capítulo não é combate. `magic missile`, `burning hands`, `chill touch` e `lightning bolt` ficam fora. |
| **Não entrar em sala marcada `nao_entrar`.** | É o ponto do capítulo: o mapa serve para *não* passar por lá. |
| **Não sondar direção no escuro.** | Ver risco R1: sondar cega dispara a guarda de repetição e mata a rotina. |
| **Não continuar depois de uma fuga.** | Ver risco R2: `wimpy` salva o corpo e **destrói a posição**. Fuga = abortar o dia naquela região. |
| **Não saquear.** | A Armadura da Torre Negra ocupa 60 kg. Sem espaço. E "carregando muito peso" está na lista de falhas da guarda. |
| **Não vender armadura.** | Diretiva do autor, Dia 150. |
| **Não rodar sem supervisão.** | As mortes #5, #6 e #7 vieram de script solto insistindo em estado travado. |

---

## 2. Estado de partida (Dia 143, verificado ao vivo)

| | |
|---|---|
| Grau / classe | 20 — Mago |
| Vida / Mana / Movimento | 113 / 265 / 114 |
| CA | 95 (armadura arcana + Coroa da Rainha Branca), efeito **verificado** |
| Ouro | 7.360 |
| `wimpy` atual | **48** |
| Local / acampamento | Templo de Midgaard |
| Santuário | Panteão dos Centenários |
| Mortes | 7 (última no Dia 126, por script sem supervisão) |
| Peso preso ao corpo | Armadura da Torre Negra, 60 kg, amaldiçoada |

**Magias úteis ao capítulo, todas com proficiência 95–99%:** `invisibility`, `armor`,
`infravision`, `detect invisibility`, `detect magic`, `swim`.

> ⚠️ **Estes números são do Dia 143 e o jogo já andou até o Dia 156** (o Capítulo 03 ocupa
> os Dias 141–156). Vida, mana, ouro e ouro no banco **precisam ser reconferidos ao vivo**
> antes de abrir o capítulo. `as_of_day` do `state.json` está 13 dias atrás.

`infravision` importa para sala escura. `swim` importa para as Margens do Rio.

---

## 3. O que JÁ existe — não reinventar

**O modo já está doutrinado no `state.json`.** O perfil `batedor` existe com `wimpy 33` e a
regra escrita:

> *"Mapeamento em invisibilidade; coleta de oportunidade de itens no chão/doações permitida;
> evasão total de combate (zero engajamento, fuga imediata no 1º turno)."*

| Peça | Onde | O que já resolve |
|---|---|---|
| `nucleo/guarda.py` | já pronto | **Já protege o labirinto.** Só conta repetição de *assinatura de problema*, e o comentário no código diz literalmente que sem isso *"andar num labirinto de salas homônimas dispararia a guarda"*. Salas de texto idêntico são 61% do mundo. |
| `nucleo/base.py` | já pronto | `sala()` (exits + look), `andar()`, `ate()`, `voltar_ao_templo()`, `vida_frac()` |
| `camadas/prepara.py` | já pronto | comer, beber, **depositar ouro no banco**, dormir, voltar ao Templo |
| `camadas/vigia.py` | já pronto | diagnóstico: OK / FOME / SEDE / VIDA_BAIXA / MORTA / TRAVADO / SEM_SESSAO |
| `camadas/turno.py` | já pronto | turno supervisionado, vigilância a cada minuto |
| `acoes/mapear.py` | já pronto | anda uma sequência imprimindo **cada** sala; `--buscar "marca"` faz busca aleatória |
| `config.py` | já pronto | **o único lugar** de caminho e limite (regra do projeto) |
| `config.DOC_MAPA` | já pronto | `mapa.json` é declarado *"o mapa vivo das salas (fonte das rotas)"* |

---

## 4. O que precisa ser construído

### 4.1 Absorver o levantamento que já foi digerido — **bloqueante**

O `scripts/local/digerir_mapa.py` já produziu `data/heroes/grebolius/mapa_vivo.json` a partir
dos registros dos Dias 96–141:

| | |
|---|---|
| Salas com identidade própria | **266** |
| Arestas observadas | **551** (90% com volta confirmada) |
| Salas ausentes do `mapa.json` curado | **162 (61%)** |
| Salas de texto idêntico (só a posição separa) | 163 |
| Destinos nomeados e nunca visitados | **41** |

**O `mapa.json` tem 141 salas.** Se o capítulo começar sem absorver isso, a cartógrafa
re-percorre terreno que já está levantado e gasta o dia redescobrindo. Antes de abrir o
capítulo: revisar as **14 divergências** entre digerido e curado (todas em salas descobertas
nos Dias 97–99 que o mapa curado, parado no Dia 96, nunca absorveu) e mesclar.

> ⚠️ **O digestor está em pasta ignorada pelo git.** `scripts/local/` está no `.gitignore`
> (linha 14), então `digerir_mapa.py` não é versionado — e sem ele o levantamento do capítulo
> não é reproduzível por outro agente. O `README.md` do automato é explícito: *"nada essencial
> vive fora desta pasta"*. **Mover o digestor para `automato/`** antes de abrir o capítulo.

### 4.2 Acréscimos no `nucleo/config.py`

```python
# --- modo batedor (Capitulo 04) ---
LIMITE_TEMPO_BATEDOR = 900      # mapear e lento: exits+look+passo por sala
VIDA_MINIMA_BATEDOR  = 0.80     # nao e cacada: qualquer arranhao ja e motivo de saida
MANA_MINIMA_BATEDOR  = 60       # invisibilidade e armadura custam mana; 265 e finito
PASSOS_SEM_SALA_NOVA = 12       # detector de "perdida": 12 passos sem sala nova -> recall
```

`VIDA_MINIMA` global é 0.45 e `VIDA_PARA_LUTAR` é 0.70 — **nenhum dos dois serve aqui.**
A cartógrafa não está caçando; 0.80 é o piso dela.

### 4.3 `rotinas/cartografa.py`

Segue o contrato do `README.md`: parte do Templo, verifica por **marco de sala** (nunca por
contagem de passos), termina no Templo com `save`, e é interrompível.

Laço por sala:
1. `exits` → **todas** as direções e nomes de destino, de uma vez;
2. se a sala é nova, gravar: título, descrição, saídas nomeadas, dia;
3. classificar presença com `consider` — **sem atacar**;
4. escolher o próximo passo **somente entre as direções anunciadas** (risco R1);
5. gravar a aresta e empilhar a sala no caminho de volta.

### 4.4 `mapear.py --retrato`

Hoje o `mapear.py` imprime texto livre. Para o capítulo, precisa cuspir um **registro JSON por
sala** (título, saídas, presenças, `consider`, dia) para alimentar o mapa direto.

### 4.5 Campo `risco` no `mapa.json`

```json
"risco": {
  "nivel": "alto",
  "nao_entrar": true,
  "criaturas": ["um monstro invasor"],
  "evidencia": "consider = 'vai te massacrar' (Dia 155)",
  "dia": 155,
  "ultima_visita": 155
}
```

Níveis: `seguro` · `baixo` · `medio` · `alto` · `armadilha` · `morte`.
Regra dura: **sala com `nao_entrar: true` é excluída de toda rota que o automato calcular.**

---

## 5. Riscos reais — e o tratamento de cada um

### R1 — A guarda de repetição mata a cartógrafa
`'não pode ir'` está na lista `FALHAS` do `guarda.py`. Uma cartógrafa que sonda direções
bloqueadas recebe essa mesma resposta; **na terceira seguida a guarda dispara
`recall` + `save` + `SystemExit(9)`** e a sessão morre no meio do levantamento.

**Tratamento:** nunca sondar. O comando `exits` **já informa quais direções existem** e o nome
do vizinho. Andar só pelo que foi anunciado. Isso elimina a sondagem cega, é mais barato e é
mais seguro.

### R2 — `wimpy` alto salva o corpo e destrói o mapa
Este é o conflito direto entre os dois pedidos do autor ("winky alto" + "retornar se se perder").

`wimpy` faz a personagem **fugir**. Fuga joga ela numa sala adjacente **aleatória** — e a
partir daí o mapa **não sabe mais onde ela está**. Num mundo onde 61% das salas têm texto
idêntico, isso não se recupera por observação.

**Tratamento, sem abrir mão do `wimpy` alto:**
- fuga **não** é contratempo, é **abortar**: marcar a sala que causou como `nao_entrar: true`,
  `recall`, e reiniciar a rota do zero;
- **nunca** continuar mapeando depois de uma fuga;
- registrar o evento para o perigo ficar no mapa com evidência.

### R3 — A guarda fica quase inerte neste modo
O `guarda.py` **zera o contador** a cada comando benigno, e `exits` e `look` estão na lista de
benignos. A cartógrafa emite `exits` e `look` o tempo todo → a guarda praticamente não conta nada.

**Tratamento:** não confiar nela como rede de segurança. A rede real é
**orçamento de tempo + piso de vida + piso de mana + detector de "perdida"** (os quatro
limites da seção 4.2).

### R4 — Duração das magias não está verificada
A skill é explícita: *"Não pressupor atividade contínua, AC imutável ou imunidade"* — o mesmo
vale para `invisibility`. Duração e custo só valem pelo que o servidor responder.

**Tratamento:** reconjurar **quando o servidor avisar que acabou**, nunca por relógio suposto.
Abortar se a mana cair abaixo do piso. Registrar no log cada resposta de conjuração.

### R5 — `recall` pode estar bloqueado
`recall` é grátis até o nível 70 (ela é 20) e é o mecanismo de retorno. Mas pode haver sala que
bloqueie.

**Tratamento:** o **caminho de volta é uma pilha**. Cada passo empilha a sala de origem; se o
`recall` falhar, a cartógrafa **desempilha e refaz o caminho ao contrário**. É isso, e não o
`recall`, que cumpre o "retornar se se perder".

### R6 — Perigos já conhecidos, para nunca entrar
| Sala | Perigo | Fonte |
|---|---|---|
| **Adentro do Milharal Destruído** | armadilha letal | plano do Cap. 03 §2-A |
| **As Margens do Rio** | afogamento | mapa (risco Alto) |
| **O Beco Escuro** | mercenários armados hostis | mapa (risco Alto) |
| **Na Base da Torre / Torre Negra** | "sussurra a morte a quem chega perto" | prólogo |
| **Dentro do Portão Leste** | 8 guardas de elite | mapa (risco Alto) |

### R7 — Peso e provisões
A armadura amaldiçoada de 60 kg fica presa ao corpo: o peso não muda. Sem saquear, isso é
**estável** — e estável é bom. Mas fome e sede **consomem vida e mana por ciclo**, e *"dormir
faminto é o pior caso"*. `prepara.py` antes de cada sessão, sem exceção.

### R8 — Teto de conexões
Máximo **3 conexões por dia**. Levantamento é lento; o capítulo vai durar vários dias. Isso é
esperado, não é falha.

---

## 6. Alvos do levantamento, em ordem de rendimento

### Prioridade 1 — Avenida Floris (a melhor relação rendimento/risco do capítulo)
Descoberta no **Dia 99**, **não existe no `mapa.json`**. É uma **avenida de cidade**, com
**7 destinos nomeados e nunca visitados**:

| Saída | Destino nomeado | Nunca visitado |
|---|---|---|
| norte | A Loja de Arcos | sim |
| norte | A Sapataria | sim |
| norte | A Delegacia | sim |
| norte | Uma Rua de Pedra Esburacada | sim |
| norte | A Loja de Armas de Maris | sim |
| sul | A Via da Veneração | sim |
| sul | A Loja de Carriolas | sim |

Rua de comércio: risco baixo, sala nova a cada passo. **Começar por aqui.**

### Prioridade 2 — Jareth
`O Centro da Cidade de Jareth` tem `Rua Bourbon` ao norte e ao sul, e mais: O Banco de Jareth,
A Loja de Provisões, A Recepção do Clube Kitty-Kat, Grottas - A Loja de Móveis, Estábulos,
A Loja de Montarias. A `Avenida Floris` já liga a cidade.

### Prioridade 3 — A vila e as planícies (oeste)
`Numa Pequena Vila` → `Um Casebre` (leste e oeste), `O Centro do Vilarejo` →
`O Caminho Para as Planícies Nobres`, `Uma Praça` → `A Rua do Rio` (norte e sul).

### Prioridade 4 — A fronteira restante
41 destinos nomeados e nunca visitados, 30 nomes únicos. Inclui `O Panteão dos Centenários`
pela via `u` do Templo — que é o **santuário** dela e não foi visitado nos Dias 96–141.
`A Entrada Para o Bosque Sombrio` merece cautela: "sombrio" no nome.

### Prioridade 5 — Busca dirigida
Com o mapa levantado, procurar **"o novato esperto"** (encruzilhadas civis) e **"o smurf
minerador"** (minas e colinas). Isso fecha pendências do Capítulo 03 usando o mapa do 04.

---

## 7. Orçamento do dia e encerramento

| | |
|---|---|
| Conexões | máximo 3 |
| Tempo por rotina | `LIMITE_TEMPO_BATEDOR` = 900 s |
| Passos úteis por jornada | 40 a 70 (doutrina vigente) |
| Vida mínima | 80% |
| Mana mínima | 60 |
| Abortar por "perdida" | 12 passos sem sala nova |

**Encerramento padrão, nesta ordem:** `recall` → Templo → `deposit` (ouro no banco) →
`save` **com resposta verificada** → `sleep`. Nunca declarar `save` ou repouso se a ação falhou.
Se houver `save`, a sessão seguinte acorda no Templo — que é a âncora e o que torna o capítulo
reiniciável.

---

## 8. O plano de execução, em ordem

1. **Esperar o Capítulo 03 fechar.** Não abrir o 04 antes — o outro agente está nele.
2. **Verificar as magias antes de partir:** conjurar `invisibility` e `armor` numa sessão
   autorizada e **anotar o que o servidor responder** (duração, custo, aviso de expiração).
   Sem isso o planejamento de mana é chute.
3. **Testar o teto do `wimpy`.** Está em 48; a metade da vida máxima (113) é 56. Subir em
   sessão autorizada e **registrar a resposta**; se recusar, fica 48 e o plano não muda.
4. **Absorver `mapa_vivo.json` no `mapa.json`** (266 salas), revisando antes as 14 divergências.
   Sem isso a cartógrafa redescobre o que já sabe. **Mover `digerir_mapa.py` para `automato/`**
   — hoje ele vive em `scripts/local/`, que o git ignora.
5. **Acrescentar os limites do batedor** no `config.py` e o campo `risco` na convenção do mapa.
6. **Escrever `rotinas/cartografa.py`** conforme o contrato, e `mapear.py --retrato`.
7. **Ensaio em terreno conhecido:** rodar a rotina no anel de Midgaard (já levantado) e conferir
   contra o mapa digerido. O ensaio só passa se: registrar sala, marcar perigo, abortar no piso
   de vida, e voltar ao Templo sozinha. **Antes disso, não pisar em terreno novo.**
8. **Primeira incursão real:** Avenida Floris, 20–30 salas, **supervisionada**, lendo o log a
   cada ~60 s.
9. **Abrir o capítulo:**
   ```
   python add_chapter.py --hero grebolius --chapter 4 --tomo 1 \
     --title "<título aprovado pelo autor>" \
     --goal "Levantar o terreno desconhecido sem travar combate, marcando os perigos, e voltar viva todos os dias."
   ```
10. **Por dia:** `add_chapter.py --chapter 4 --part --day <N> --summary "..." --evidence-file <...>`.
11. **No fim:** fechar com `--close --content-file --evidence-file`, a crônica do capítulo.

---

## 9. Decisões pendentes do autor

1. **Título do capítulo** — precisa ser narrativo, sem metajogo.
2. **`wimpy`:** sobe para 56 (novo teste) ou fica 48?
3. **Coleta:** a regra do `batedor` permite *"coleta de oportunidade de itens no chão/doações"*.
   O capítulo mantém isso ou é mapeamento puro, sem pegar nada?
4. **Armadura da Torre Negra** (herdada do Cap. 03): continuar carregando os 60 kg presos, ou
   pagar **8.509** para desamaldiçoar e doar?
5. **Regiões proibidas:** alguma área que a cartógrafa **não** deve levantar (ex.: Torre Negra,
   margens do rio, esgotos)?

---

## 10. Regras permanentes (do autor) — valem para este capítulo

- **Proibido vender armaduras** (Torre Negra ou peão) — prejuízo comprovado.
- **Nada de metajogo** nas descrições dos capítulos; o detalhe técnico fica nas descrições dos dias.
- **Nunca** rodar robô sem supervisão; ler o log a cada minuto e matar o job se algo piorar.
- O **ouro dorme no banco** — a morte não leva o que está guardado.
