# Registro de evolução — o livro-razão dos agentes

> **Para que serve.** Vários agentes jogam e mexem na mesma ferramenta. Este arquivo é o registro
> **de quem mudou o quê na ferramenta, quando, por quê e com que verificação** — o que
> `automato/CHANGELOG.md` (versões) e `automato/DECISOES.md` (decisões) não cobrem, porque eles registram
> *o que mudou*, não *quem mudou*.
>
> Ele é a resposta escrita à pergunta: *"um agente novo chega amanhã — como ele sabe o que já foi
> tentado, quem fez, e o que continua aberto?"*

---

## 1. Regras do livro-razão

1. **Append-only.** As entradas mais recentes ficam **no fim da seção §5 (Entradas)** — as seções 1–4 e
   6–8 são o manual, e as entradas se acumulam entre elas. Nunca edite nem apague o bloco de outro
   agente. Para corrigir algo, **acrescente um bloco novo** que referencia o anterior.
2. **Identifique-se sempre.** `### <data real> · <dia de jogo ou "—"> · <modelo/versão>`. Use **um
   identificador estável** — hoje o histórico tem `Gemini 3.8 Flash (High)` e `Gemini 3.8 Flash High`
   como se fossem dois agentes, por inconsistência de nome.
3. **Um bloco por mudança coerente.** Não agrupe a semana inteira num bloco.
4. **Verificação obrigatória.** Se você não rodou nada, escreva `não verificado` — nunca deixe implícito
   que foi testado.
5. **Declare o custo.** Toda mudança que melhora algo piora outra coisa. "Nenhum" é resposta válida, mas
   precisa ser uma afirmação consciente.
6. **Não duplique.** O detalhe técnico da versão vai para o `CHANGELOG`; a decisão com custo e alternativas
   vai para o `DECISOES`. Aqui fica a autoria, o contexto da sessão e o que continua aberto.
7. **Concorrência:** releia o **fim** do arquivo imediatamente antes de escrever. Se ele mudou desde sua
   leitura, reescreva seu bloco sobre a versão nova (ver §6).

---

## 2. Formato do bloco

````markdown
### 2026-10-16 · Dia 156 · <modelo/versão>
- **Mudou:** <arquivos e o que passou a valer>
- **Por quê:** <problema real observado, com sintoma>
- **Como foi verificado:** <comando/teste/sessão + resultado literal>
- **Custo:** <o que se perde, ou "nenhum">
- **Próximo:** <o que continua aberto, com hipótese>

<!-- opcional, quando houver -->
- **Evidência:** <caminho do log/transcript/evidence>
- **Handoff:** <o que o próximo precisa saber para não repetir o caminho>
````

Critério de qualidade de um bloco: um agente que **nunca viu o projeto** consegue, só com ele, saber se
pode confiar na mudança e o que verificar antes de construir em cima.

---

## 3. Onde registrar cada tipo de mudança

| Você mudou… | Obrigatório em | Opcional/condicional |
| --- | --- | --- |
| Ferramenta (automato, camadas, rotinas, ações, config, verificar) | bloco aqui + `automato/CHANGELOG.md` | `automato/DECISOES.md` (se houver decisão e custo) |
| Documento de método (`docs/`, `skills/`) | bloco aqui | — |
| Referência técnica do MUD (`maquina/`) | `maquina/verificacoes.md` | bloco aqui, se mudou o entendimento operacional |
| Campanha (`data/heroes/<id>/`) | evidência + `state.json` + crônica | bloco aqui, se a mudança alterou **como** se joga |
| Infraestrutura do repositório (validadores, publicador, `.gitignore`) | bloco aqui | `automato/CHANGELOG.md` não se aplica |

---

## 4. Histórico herdado (anterior a este arquivo)

O motor acumulou onze versões antes de existir um livro-razão. O detalhe de cada uma está em
`automato/CHANGELOG.md`; abaixo, o resumo para orientação rápida:

| Versão | Dia | Mudança principal |
| --- | --- | --- |
| v0.1 | 141 | Método "mapear à mão → testar em trechos → só então automatizar"; `wake; stand` obrigatório |
| v0.2 | 143 | **Guarda de repetição** (`guarda.py`), injetada no `run()`; comandos benignos não disparam |
| v0.3 | 147 | `abastecer()`: comer e beber **antes** de dormir/viajar; plano B de alvo |
| v0.4 | 148-149 | Camadas `vigia` / `prepara` / `trabalhar` / `turno`; banco do Templo; hidratação na fonte |
| v0.5 | 150 | **Proibido vender armaduras** (diretiva do autor); rotina `xadrez` suspensa |
| v0.6 | 152-154 | Rota determinística Templo→Milharal por marco de sala; `lightning bolt` e nome exato do alvo |
| v1.0 | 155 | Empacotamento em `automato/` com `nucleo/config.py` como ponto único |
| v1.1 | 155 | **Autossuficiência**: driver inteiro dentro de `automato/`, runtime fora do git |
| v1.2 | 155 | `verificar.py` (autoexame de 18 itens), `acoes/mapear.py`, plano do capítulo 03 |
| v1.3 | 155 | **Todo agente se identifica** (relatório, campo `agent`, trailer no commit) |
| v1.4 | 156 | `term 200 80` no login (fim do falso MORTA por paginador); `sacar_para_comprar()`; revisão da Sala de Doações; `rotinas/mercado.py`; `acoes/fundir_mapa.py`; `USAR_INVISIBILIDADE = False` |

### Autoria observável no histórico

Medido em 2026-10-16: **186 commits**, dos quais **25** trazem o trailer `[agente: …]`. A regra de
identificação nasceu só na v1.3, então a maior parte do histórico **não tem autoria declarada**.

| Identificador declarado | Commits |
| --- | --- |
| `deepseek-flash` | 23 |
| `Gemini 3.8 Flash (High)` | 1 |
| `Gemini 3.8 Flash High` | 1 |

> As duas grafias do Gemini são o mesmo agente registrado de duas formas — motivo da regra §1.2.

---

## 5. Entradas

### 2026-10-16 · Dia 156 · deepseek-flash

- **Mudou:** criado o conjunto de documentação para agentes: `AGENTS.md` (raiz) e
  `docs/agentes/{arquitetura,boas_praticas,glossario,onde_consultar,registro_de_evolucao}.md`.
  `AGENTS.md` entrou em `ROOT_FILES` de `publish_daily.py`, para ser publicável como os demais
  documentos de raiz.
- **Por quê:** o projeto passou a ter **vários agentes** jogando e editando a ferramenta na mesma árvore
  (o HEAD avançou de `96bf42c` para `158da9e` durante a redação). A documentação existente era
  fragmentada e voltada a quem já conhecia o projeto: `automato/README.md` explicava o motor, mas não
  havia porta de entrada, nem inventário de artefatos, nem lugar único para registrar autoria das
  mudanças na ferramenta.
- **Como foi verificado:**
  - `python automato/verificar.py` → **18/18 itens OK** (exit 0), com o driver já escutando em
    `127.0.0.1:14888`.
  - `python scripts/check_project.py` → **0 erro(s), 8 aviso(s)** (avisos de legado, metajogo e
    pendências editoriais, todos pré-existentes).
  - `python -B -m unittest discover -s scripts -p "test_*.py"` → **exit 0**; `sync_hero --check` acusou
    derivados desatualizados e a própria suíte regenerou `ficha.md`, `hero.json` e `data/heroes.json`,
    sem alteração líquida no git.
  - **Não verificado:** nenhum conteúdo foi confirmado em sessão ao vivo; nenhum comando foi enviado ao
    MUD por este trabalho. A documentação foi escrita a partir de leitura de arquivos e de `git`.
- **Custo:** mais cinco documentos para manter. O risco concreto é **envelhecerem**: já nasceram com a
  versão do motor desatualizada (escritas como v1.3, quando a v1.4 foi publicada minutos depois). Mitigação:
  os documentos apontam para as fontes canônicas em vez de copiar seus dados — quem lê deve reconferir
  versão e contagens.
- **Próximo:** (a) decidir se `maquina/**` e `docs/*.json` entram na lista de caminhos publicáveis de
  `publish_daily.py` — hoje são **preservados fora da revisão**, e `maquina/verificacoes.md` é justamente
  onde se registra correção de referência; (b) atualizar `automato/verificar.py`, que ainda só confere
  `acoes/mapear.py` e `acoes/ressuscitar.py` e um `plano_capitulo_03.md` fixo, apesar de existirem
  `digerir_mapa.py`, `fundir_mapa.py`, `encontrar_fazendeiro.py`, `falar_fazendeiro.py` e o capítulo 05;
  (c) corrigir a seção "Próximas versões (planejado)" do `CHANGELOG`, que ainda promete v1.1/v1.2/v1.3
  já publicadas.
- **Handoff:** os documentos de `docs/agentes/` descrevem **como trabalhar**, não **o que fazer na
  campanha**. O trabalho narrativo em curso continua sendo o Capítulo 05 — o estado dele está em
  `data/heroes/grebolius/plano_capitulo_05.md`, `missoes.json` e no topo do `CHANGELOG` (v1.4).

<!--
PRÓXIMA ENTRADA COMEÇA AQUI. Não edite os blocos acima; acrescente o seu abaixo, antes do bloco de
handoff (§7).
-->

### 2026-10-16 · Dia 156 · deepseek-flash

> **Quarta entrada do dia.** Esta **fecha o Capítulo 06** — e registra o que eu aprendi **observando
> outro agente jogar o plano que eu escrevi**.

- **Mudou:** o **Capítulo 06 — "Quem Quer Ser Rainha Não Fica Parada"** foi fechado em `capitulos.json`
  (`status: concluido`, `closed_on_day: 156`), com **12 parágrafos de narrativa**, `excerpt`, três
  evidências e dez tags. O campo transitório `directive` saiu do capítulo — **as palavras do autor ficam
  na `diretiva_de_jogo.md` §16/§17**, que é o lugar canônico.
- **Por quê:** o capítulo já estava **jogado** pelo `Gemini 3.8 Flash` (`planos/plano006.md`,
  `evidence/dia156f.json`), mas **`content`, `excerpt` e `closed_on_day` estavam vazios**. Capítulo com a
  expedição registrada e sem narrativa é capítulo pela metade.
- **Como foi verificado:** tudo conferido **ao vivo no servidor** antes de escrever — `score tudo` deu
  **8 mortes**, **1.219.294 de experiência**, 135/135 HP, 270/270 mana, 1.651 de ouro: **bate com o plano
  006 em todos os números**. `check_project.py` **0 erros**; `verificar.py` **18/18**; derivados
  conferidos.
- **Custo:** nenhum de ferramenta.

#### O que eu aprendi observando o `Gemini 3.8 Flash` — e não é lisonjeiro para mim

**1. Ele jogou; eu documentei.** Na mesma sessão em que eu construí o esquema de planos, escrevi o
`mandabala.py`, corrigi meus próprios erros publicados e escrevi nove antipadrões, **a campanha não
avançou nas minhas mãos**. Ele leu o **meu** `plano005.md` e **executou em uma sessão**. O esquema de
planos se validou sozinho: **outro modelo, outra empresa, sem eu explicar nada.**

**2. Ele confiou na caminhada; eu confiei no mapa.** Eu registrei no plano *"sete salas têm uma única
saída — o levantamento está incompleto"* e tratei isso como **tarefa de documentação**. Ele **desceu e
andou**, e as salas que o mapa chamava de beco **eram anéis interconectados**. **O mapa estava
incompleto porque eu nunca o percorri**, e a diferença é de atitude: eu tratei a lacuna como problema de
registro, ele tratou como convite a caminhar.

**3. Ele obedeceu a diretiva sem a transformar em documento.** *"arriscar mais, e tudo bem se morrer"* →
ele **entrou no Covil do Dragão e morreu**. Eu teria escrito uma análise de risco antes. **A diretiva do
autor não pedia análise; pedia entrada.**

**4. Ele soube o que NÃO testar — e isso é o mais fino.** O `Passo-Em-Falso` é armadilha mortal, e ele
recusou o teste: *"o risco de perda desnecessária sem ganho não justifica o teste"*. **Ele entendeu que
"arriscar mais" não é "testar tudo"**: arriscar é aceitar o custo **em troca de progresso**; testar a
própria morte sem ganho é desperdício. **A Serpente e o Aligátor ficaram vivos** — ele foi atrás do que
estava na diretiva, não do que era curioso.

**5. Ele achou o que plano nenhum pedia.** `Clodoaldison`, o advogado de divórcios do submundo; os três
besouros gigantes dormindo; a lagoa escura. **Isso é exploração, não execução** — e nenhum dos meus
planos teria produzido esses achados, porque os meus planos eram **listas de tarefas**.

**6. Ele registrou certo de primeira.** A `part` saiu com **`source_kind`**, **`date`** e **`evidence`**
— exatamente os três campos cuja ausência derrubou o `check_project.py` quando **eu** fechei o capítulo
5. **Ele não repetiu um erro que não cometeu.**

**A lição para mim, em uma frase:** eu passei a sessão **consertando a documentação do jogo** enquanto
outro agente **jogava o jogo**. As duas coisas eram necessárias — mas só uma **avançou a campanha**, e
não foi a minha.

- **Próximo:** (a) **o Capítulo 07 já tem assunto e endereço** — a **Serpente dos Esgotos** e o
  **Aligátor**, que ficaram vivos, e o **Dragão Vermelho**, que dá 135 de dano em um turno e é promessa,
  não obstáculo; (b) **a pergunta aberta que vale mais que ouro:** o **brinco ANTI-DT** anula o
  `Passo-Em-Falso`? Ninguém testou, e é a única defesa contra morte sem aviso; (c) o achado do item 2
  **reforça o `boas_praticas.md` §9.1** com uma segunda demonstração: **o mapa dizia uma coisa e a
  caminhada disse outra — e quem andou acertou.**

### 2026-10-16 · Dia 156 · Gemini 3.8 Flash

- **Mudou:**
  1. **Execução agressiva do Capítulo 06:** incursão aos Esgotos de Midgaard sob a nova diretiva de risco do Plano 005. Abate de 3 larvas gigantes (one-shot com `lightning bolt`) e 6 pequenos morcegos (impactos de 59 a 84 de dano com `lightning bolt`).
  2. **Mapeamento profundo dos esgotos:** descobertas e verificadas conexões em anel (anel nordeste com lagoa/fissura, anel sul com corredor escuro e grandioso cano, eixo de subida e escritório de divórcio de Clodoaldison). Identificada a sala `Passo-Em-Falso` como Death Trap fatal com aviso de perigo.
  3. **Confronto no Covil do Dragão e Morte #8:** o Dragão Vermelho desferiu mordida letal instantânea. Morte absorvida com ganho líquido de +19.293 XP (+21.994 de abates menos 2.701 da morte).
  4. **Ressurreição e restauração:** travessia do Paraíso via `automato/acoes/ressuscitar.py`, renascimento na Fonte da Vida, re-equipamento integral de todos os itens com `wear all` e `wield espada`, armaduras mágicas (`armor` e `detect invisibility`) e `save` seguro no Templo.
  5. **Documentação gerada:** `evidence/dia156f.json`, `state.json` atualizado, `conhecimento.md` (§29), `capitulos.json` (part 1 do Capítulo 06) e `planos/plano006.md` criado como ponto de continuação.
- **Por quê:** cumprimento da ordem do autor de executar o plano vigente (*"é pra fazer"* / *"continua"*), testando a nova postura de risco e limpando os monstros do esgoto.
- **Como foi verificado:** sessão ao vivo executada com sucesso contra o driver vivo (porta 14888). Vitais finais: 135/135 HP, 270/270 Mana, 131/131 MV, CA 111, Nível 21, EXP 1.219.294. `automato/verificar.py` 18/18 OK; `python scripts/sync_hero.py --hero grebolius` exit 0; `python scripts/check_project.py` 0 erros, 8 avisos; suíte de 116 testes unitários com exit 0.
- **Custo:** Morte #8 registrada no histórico mecânico da personagem, conforme custo aceito expressamente pelo autor na abertura do Capítulo 06.
- **Próximo:** Decisão com o autor no `plano006.md`: fechar o Capítulo 06 com a limpeza concluída e saldo amplamente positivo (+19k EXP) ou planejar nova incursão tática contra outros predadores residuais (serpente ou aligátor).

### 2026-10-16 · Dia 156 · deepseek-flash

> **Terceira entrada do dia.** Esta **abre o Capítulo 06** por diretiva do autor.

- **Mudou:** o **Capítulo 06 — "Quem Quer Ser Rainha Não Fica Parada"** foi aberto em `capitulos.json`
  (`id=6`, `kind=marco`, **`em_curso`**), com um campo novo **`directive`** que guarda as **palavras do
  autor** e a postura de risco do capítulo. A **`diretiva_de_jogo.md` ganhou a §16 — "RISCO AUTORIZADO"**,
  que **revoga, para os esgotos**, a doutrina de fuga que valeu dos Capítulos 03 a 05. E o
  **`planos/plano005.md`** traz o grafo dos esgotos, os bichos conhecidos e a ordem de execução.
- **Por quê:** o autor definiu o próximo capítulo — *"limpar todos os monstros do esgoto"*, *"vamos
  arriscar mais, e tudo bem se morrer"*, *"já aprendi demais, agora é hora de voltar lá e se vingar"*.
  **É a primeira vez que a postura de risco muda por decisão explícita**, e isso precisa estar escrito
  onde o próximo agente lê — senão ele joga com a doutrina antiga e foge do que devia matar.
- **Como foi verificado:** o **grafo dos esgotos foi lido do `mapa.json`** (17 salas, camada `esgotos`) e
  a rota de mão dupla conferida pela curadoria (`Praça Comum → n → O Depósito de Lixo → d → hub → u`).
  **O levantamento está INCOMPLETO** — sete salas têm uma única saída registrada e as arestas reversas
  não existem no mapa. Isso ficou registrado no plano como **tarefa**, não como fato.
  `check_project.py` **0 erros**; `verificar.py` **18/18**; derivados conferidos; e o `mandabala.py`
  confirmado listando os cinco planos e **avisando** que o `plano002` não é o mais recente.
- **Custo:** **nenhum de ferramenta.** O custo é de jogo e é declarado: **morte é aceita**. E o esgoto
  **não paga ouro** (mobs selvagens dropam zero) — o capítulo compra **XP e limpeza**, não bolsa.
- **Próximo:** (a) **corrigir o `mapa.json` do esgoto** com o `exits` real de cada sala — é o único
  levantamento do repositório que se sabe incompleto; (b) o `mandabala.py` **ainda não avisa quando um
  plano foi SUPERADO por outro** (avisa só de lacuna, plano não-recente e falta de autoria) — e
  `plano002` é exatamente esse caso; (c) a promessa do capítulo anterior segue aberta: **extrair falas
  de NPC do transcript automaticamente**, para que ler a fonte não dependa de disciplina.

### 2026-10-16 · Dia 156 · deepseek-flash

> **Segunda entrada do mesmo dia, e é a limpeza da primeira.** A entrada anterior registrou o erro; esta
> registra **as correções** e as regras que ele gerou.

- **Mudou:** os **antipadrões** do Dia 156 entraram em
  [`docs/agentes/boas_praticas.md`](boas_praticas.md) **§9** (nove linhas novas na tabela
  *sintoma → causa → regra*) e num **§9.1 — "A regra que custou mais caro: ler a fonte, não a
  conclusão"**, com a comparação lado a lado dos dois métodos. **Quatro documentos errados foram
  marcados, sem apagar o corpo:**
  1. `data/heroes/grebolius/conhecimento.md` **§37** — aviso no topo com as cinco correções e a cadeia
     real;
  2. `data/heroes/grebolius/planos/plano002.md` — aviso no topo (o corpo fica intacto, porque o §6.1 diz
     que plano antigo não se edita);
  3. `data/heroes/grebolius/evidence/dia156d.json` — campo novo **`superseded_by`**, apontando para o
     `dia156e.json`, com o motivo e o registro de que **foi mantido de propósito**;
  4. `data/heroes/grebolius/BRIEFING_CAPITULO_05.md` — marcado **OBSOLETO** (o capítulo fechou e o
     esquema de planos o substituiu).
- **Por quê:** o autor pediu duas coisas — *"ajuste as cagadas que vez e anote no método indicações para
  não fazer mais"*. As duas têm a mesma raiz: eu **li o fim de uma cadeia e escrevi como se fosse o
  começo**, publiquei, e deixei quatro documentos afirmando o caminho errado. **Documento errado e não
  avisado é pior que documento apagado** — quem ler só ele persegue o caminho errado.
- **Como foi verificado:** as provas da correção foram conferidas no transcript (a fala `ajuda mapas` na
  **linha 5562**, `ajuda remortar` na **8230**, `espectro` 8×, `remortar` 5×) e ao vivo
  (`onde` responde `Como?!?` enquanto o `help where` o documenta). `check_project.py` **0 erros**;
  `verificar.py` **18/18**; derivados conferidos; e a checagem de que **os quatro arquivos errados
  carregam marca** (`MARCADO` nos quatro).
- **Custo:** **quatro avisos** em documentos vivos, que alguém vai ter de ler para sempre. É o preço
  consciente de não apagar: **o erro visível ensina; o erro apagado se repete.** E este é o terceiro
  caso do mesmo padrão só neste dia — os `docs/circlemud/` (seis rodadas), o campo `agent` (autoria
  inferida) e agora a crônica.
- **Próximo:** (a) **a ferramenta** — extrair falas de NPC do transcript automaticamente e apresentá-las
  antes da sessão, para que ler a fonte deixe de depender de disciplina; (b) o `mandabala.py` poderia
  **avisar quando um plano foi superado** por um posterior (hoje ele só avisa de lacuna, plano não
  recente e falta de autoria) — `planos/plano002.md` e `planos/plano003.md` são exatamente esse caso;
  (c) `autoquest todas` merece uma nota onde o motor lê, porque "catálogo não é prova" ainda não está
  em lugar nenhum que uma rotina consulte.

### 2026-10-16 · Dia 156 · deepseek-flash

> **Esta entrada é a mais desconfortável desta pasta, e é de propósito.** Ela registra um erro meu que
> **foi publicado**, e a correção que **outro agente** fez.

- **Mudou:** `automato/DECISOES.md` ganhou a **§9 — "A missão fala a palavra dela — e a fonte é o
  transcript"**, a primeira entrada do livro de decisões que **não** é sobre código: é sobre **método de
  leitura**. A lista de "próximos desafios" foi reescrita (pedia *"localizar os novatos nas praças"* — e
  eles estão nos `docs/circlemud/` desde o começo; e *"Problemas Agrícolas"* estava vetada).
  `maquina/verificacoes.md` e `maquina/dicionario_comandos.md` ganharam a **divergência do `onde`**.
  `planos/plano004.md` fecha o capítulo.
- **Por quê:** **dois agentes jogaram o mesmo capítulo e chegaram a resultados opostos.** Eu
  (`deepseek-flash`) tratei *"Você deve dizer algo ao personagem"* como enigma e inventei ~35 frases;
  o `GPT-6 / Codex` **leu o transcript** e achou a fala que o novato **já tinha dito** — `ajuda mapas`,
  gravada na **linha 5562 de um transcript que eu tinha aberto**. A cadeia real era
  `ajuda mapas → diretrizes → levar a veste à tagarela → retornar → ajuda remortar`, e a minha crônica
  contava o **fim** dela como se fosse o começo. **Eu publiquei a versão errada** (`e1868d9`); ele
  reconciliou (`1ecce4d`) e eu empurrei, com a autoria sinalizada.
- **Como foi verificado:** as provas dele foram conferidas no transcript —
  `ajuda mapas` **3 ocorrências** (uma na **linha 5562**), `ajuda remortar` na **8230**, `espectro`
  8 ocorrências, `remortar` 5. **Todas confirmadas.** E testei ao vivo o que ele tirou da ajuda:
  **`help where` documenta `Uso: onde <monstro ou jogador>`, e `onde` responde `Como?!?`** — só `where`
  funciona, e `where` sem argumento lista **os jogadores** da área. `check_project.py` **0 erros**;
  `verificar.py` **18/18**; suíte **116 testes OK**.
- **Custo:** uma crônica publicada errada, por algumas horas, no GitHub. E a lição é sobre **mim**, não
  sobre a ferramenta: **eu tinha o arquivo e preferi a conclusão** — a terceira vez no mesmo dia (as
  outras duas: os `docs/circlemud`, seis rodadas; e o campo `agent`, onde inferi autoria em vez de ler).
  A correção **não** apaga o `evidence/dia156d.json` nem o `plano002.md`: o erro fica registrado.
- **Próximo:** (a) **a ferramenta que resolve isso** — extrair as falas de NPC do transcript
  automaticamente e apresentá-las antes da sessão, para que *ler a fonte* deixe de depender de
  disciplina (§9, próximo desafio); (b) o `autoquest todas` **não pode** ser usado como prova de
  conclusão — vale escrever isso onde o motor lê; (c) o `where` merece entrar na rotina de
  **localização de NPC** em vez da varredura a pé.

> **Nota sobre autoria, porque esta entrada mistura duas:** o commit `1ecce4d` é do **GPT-6 / Codex** e
> **não** foi escrito por mim. Eu o empurrei porque o autor autorizou (*"vc sempre pode publicar se
> estiver pendente, só sinaliza quem fez"*) e porque o `AGENTS.md` **§12** proíbe esse agente de
> publicar. **O conteúdo é dele; o envio é meu.** O commit `194663c`, que registra a §12, também tem
> conteúdo dele e envio meu.

### 2026-10-16 · Dia 156 · deepseek-flash

- **Mudou:** o motor ganhou a versão **v1.5** (`automato/CHANGELOG.md`) com o esquema de **planos
  numerados** e a ferramenta de retomada:
  1. **`data/heroes/<id>/planos/planoNNN.md`** — um plano **por sessão**, **append-only**, com
     **autoria** no cabeçalho. Regra no `AGENTS.md` **§6.1**, na tabela do §6 e no checklist *"Antes de
     encerrar"*;
  2. **`data/heroes/grebolius/planos/LEIA.md`** — como o esquema funciona e o **modelo** do plano;
  3. **`data/heroes/grebolius/planos/plano001.md`** — a primeira aplicação (Capítulo 05);
  4. **`scripts/mandabala.py`** — acha o plano mais alto, avisa de **lacuna na numeração**, de plano
     **não mais recente** e de plano **sem autoria**, e imprime a ordem de leitura + o plano integral.
     Modos: `--listar`, `--numero N`, `--hero`, `--so-caminho`;
  5. **`scripts/test_mandabala.py`** — **25 testes**.
- **Por quê:** a passagem de agente para agente custava **rodadas inteiras de redescoberta**. O caso
  concreto: **seis rodadas** procurando o "novato esperto" cuja sala (**18645**) estava escrita num
  documento do próprio repositório desde o começo. A pedido do autor, a retomada virou artefato: ele diz
  *"executa o plano 001"* e quem pegar continua como se fosse o anterior. **Um arquivo que se atualiza
  perderia o histórico; um plano novo por sessão preserva quem veio antes e o que já falhou.**
- **Como foi verificado:** `python -B -m unittest discover -s scripts -p "test_*.py"` → **116 testes OK**
  (eram 91); `automato/verificar.py` **18/18**; `check_project.py` **0 erros**. O script foi rodado nos
  quatro modos, incluindo o caminho de erro (`--numero 99` → exit 1 com mensagem clara). Dois **erros
  meus** apareceram no caminho e foram corrigidos: o teste passava `--numero 99` como **int** (o argparse
  quebra antes de converter), e `main()` agora **normaliza `argv` para texto** para tolerar chamada
  programática.
- **Custo:** mais um artefato por sessão para manter, e a numeração exige disciplina — um plano removido
  ou renomeado deixa **lacuna** e o `mandabala.py` avisa. Nada foi removido: o `mandabala.md` que eu
  havia criado foi **substituído pelo esquema** (o arquivo foi apagado; o conceito virou `plano001.md`).
- **Próximo:** (a) o `publish_daily.py` publica `data/**` e `scripts/**`, então a pasta `planos/` entra
  sozinha — vale conferir se convém **excluir planos antigos** da revisão ou publicá-los todos;
  (b) o `check_project.py` ainda **não valida o conteúdo de um plano** (número, autor, seções) — hoje só
  o `test_mandabala.py` olha para o plano real; (c) a convenção é **newest first** abaixo do marcador
  deste arquivo, e isso não está escrito em lugar nenhum além daqui.

### 2026-10-16 · Dia 156 · deepseek-flash

> **Nota de autoria:** esta entrada é da **sessão que estava jogando** o Capítulo 05, não da sessão que
> escreveu o guia — as duas rodam como `deepseek-flash` e o §0 não distingue sessões. O que separa é o
> conteúdo: esta entrada trata do **motor em campo**, a de cima trata da **documentação de agentes**.

- **Mudou:** o motor ganhou a versão **v1.4** (`automato/CHANGELOG.md`), com cinco correções/novidades
  que estavam em campo e sem registro:
  1. **`term 200 80` no login** (`driver/debo_bot.py`, `TERM_LINHAS`/`TERM_COLUNAS`) — acaba com o
     paginador que punha o driver em `dead_or_menu`, lido pelo vigia como **MORTA**;
  2. **`sacar_para_comprar()`** (`camadas/prepara.py`) — a padaria cobra da mão e o prepara só
     depositava; alvo em `config.SAQUE_PARA_COMPRAR` (300), com **AVISO** quando o banco não cobre;
  3. **`revisar_doacoes()`** (`camadas/prepara.py`) — revisão da Sala de Doações com critério
     **empírico** (veste a peça e compara `CA`/`Acerto`/`Dano` do `score tudo`), por diretiva do autor;
  4. **`rotinas/mercado.py`** (nova) e **`acoes/fundir_mapa.py`** (novo, com `ALIAS_CAMINHADA` e
     `ARESTAS_VERIFICADAS`); `acoes/digerir_mapa.py` movido de `scripts/local/` para `automato/acoes/`;
  5. **`config.USAR_INVISIBILIDADE = False`** — invisibilidade **bloqueia comércio**; a proteção passou
     a ser a rota, via `config.RISCO_A_EVITAR`.
- **Por quê:** cada item responde a um problema medido em sessão, não a uma preferência — o paginador
  produzia falso MORTA; a fome com ouro no banco travava a compra; a Sala de Doações acumulava peça
  melhor que a equipada; a auditoria de lojas era manual; e a invisibilidade impedia vender.
- **Como foi verificado:** `automato/verificar.py` **18/18**; `check_project.py` **0 erros**; suíte
  offline exit 0; e em campo — `commands` deixou de paginar; o saque fez a mão ir a **exatamente 300**
  (banco 171→47, total preservado); a revisão avaliou **11 peças** e trocou **1** (Acerto 1→3,
  Dano 0→1); o mapa foi de **360 → 381 salas** após a fusão com o corpus inteiro.
- **Custo:** o `prepara` ficou mais longo (saque + revisão de doações por viagem). E um **risco
  registrado**: digerir corpus **parcial** e fundir **encolhe** o mapa — aconteceu nesta sessão
  (360 → 224 salas) e foi revertido rodando o digestor sobre os **8 + 19** transcripts. O sintoma é o
  `TOTAL` do `fundir_mapa.py` **diminuir**.
- **Próximo:** (a) ~~o `verificar.py` ainda não conhece `rotinas/mercado.py`~~ — **correção**: o
  `verificar.py` descobre as rotinas por `glob('*.py')` e já listava `mercado` ("cartografa, esgoto,
  mercado, milharal"); a pendência era minha, não do verificador; (b) `config.py` tem limites novos
  (`SAQUE_PARA_COMPRAR`, `RISCO_A_EVITAR`, `TERM_*`) que o `automato/README.md` ainda não lista;
  (c) **não publiquei esta entrada** — os arquivos do guia estavam **não rastreados** e o
  `publish_daily.py` varre não rastreados (§10), o que arrastaria o trabalho da outra sessão para o meu
  commit.

---

## 6. Concorrência na prática (caso real e verificado)

Enquanto este conjunto era escrito, outra sessão publicou a revisão `158da9e` ("CHANGELOG v1.4") usando
`publish_daily.py`. Essa revisão **levou junto** `docs/agentes/arquitetura.md` e
`docs/agentes/boas_praticas.md`, que estavam apenas criados no disco e ainda **não rastreados** pelo
git — porque o publicador monta a revisão a partir de `git diff HEAD` **mais**
`git ls-files --others --exclude-standard`.

Consequências que todo agente deve assumir como normais:

- Arquivos novos seus podem ser commitados por outro agente, sob a mensagem dele.
- Seu `git status` pode mudar sem que você tenha feito nada.
- Um arquivo que você leu pode ter sido alterado entre a leitura e a escrita.

Procedimento: **releia o fim deste arquivo antes de escrever**; confira `git log -5` e
`git status --porcelain` no início e no fim; nunca use `git add -A`; e não publique por conta própria.

---

## 7. Bloco de handoff (para quem vai continuar)

Antes de encerrar, complete com o que o próximo precisa saber. Não repita o que já está nos documentos
canônicos — **aponte** para eles.

```markdown
### Handoff · <data> · <modelo/versão>
- **Estado da ferramenta:** <versão do CHANGELOG e o que está estável>
- **Estado da campanha:** <capítulo/sessão, onde estão os documentos vivos>
- **Processos:** <jobs, driver, sessão do MUD: o que ficou rodando e o que foi encerrado>
- **Bloqueios:** <o que impede avançar, e o que se tentou>
- **Próximo passo sugerido:** <uma ação, não uma lista>
- **Não repetir:** <o caminho que já se provou errado>
```

---

## 8. Pendências herdadas (abertas em 2026-10-16)

Itens conhecidos, com origem — **não são instruções narrativas**, são dívidas da ferramenta e da
documentação:

| # | Pendência | Origem |
| --- | --- | --- |
| 1 | `maquina/**` e `docs/*.json` fora da lista de caminhos publicáveis | `publish_daily.py` (`ALLOWED`) |
| 2 | `verificar.py` confere as rotinas por `glob` (ok), mas a lista de `acoes/` está fixa em `mapear.py` e `ressuscitar.py`, e o plano exigido é um `plano_capitulo_03.md` fixo | `automato/verificar.py`; **corrigido em parte** pela entrada de 2026-10-16 acima |
| 3 | Seção "Próximas versões (planejado)" do `CHANGELOG` promete versões já publicadas | `automato/CHANGELOG.md` |
| 4 | `automato/acoes/ressuscitar.py` com docstring de `farm_armaduras.py` | cabeçalho do arquivo |
| 5 | `data/{identidade,evolucao,conhecimento}.md` são cópias do herói legado | comparação byte a byte |
| 6 | `automato/setup.py` para validar ambiente e subir o driver sozinho | `automato/DECISOES.md` §7 |
| 7 | `TEST_READY.md` descreve suítes que vivem em `scripts/local/`, fora do git | `TEST_READY.md` |
| 8 | Digerir corpus parcial **encolhe o mapa** (360 → 224 salas); o `--glob` precisa cobrir tudo | `automato/CHANGELOG.md` v1.4 |
| 9 | Distinguir repetição útil (meditar) de travada, na guarda | `automato/DECISOES.md` §1 |
| 10 | Calcular automaticamente quanto guardar no banco conforme o próximo objetivo | `automato/DECISOES.md` §2 |
| 11 | `automato/README.md` não lista os limites novos do `config.py` (`SAQUE_PARA_COMPRAR`, `RISCO_A_EVITAR`, `TERM_*`) | entrada de 2026-10-16 (v1.4) |
| 12 | `TERM_*` e `USAR_INVISIBILIDADE` só existem como comentário em `config.py`; o README do motor ainda descreve a invisibilidade como proteção | `automato/nucleo/config.py` × `automato/README.md` |

---

## 9. Handoff entregue · 2026-10-16 · Dia 156 · deepseek-flash

> **Passagem do Capítulo 05 para outro agente**, pedida pelo autor. Escrito no formato do §7.

- **Estado da ferramenta:** `automato/` na **v1.4** (`CHANGELOG.md`). Estável em campo: `term` no
  login (o paginador não gera mais falso MORTA), saque do `prepara`, revisão da Sala de Doações,
  `rotinas/mercado.py`, `fundir_mapa.py` com `ALIAS_CAMINHADA`/`ARESTAS_VERIFICADAS`. Verificado:
  `verificar.py` **18/18**, `check_project.py` **0 erros**, suíte offline exit 0.
- **Estado da campanha:** **Capítulo 05 "Amanhã Eu Começo por Elas"** (`capitulos.json` `id=5`,
  `kind=marco`, **`em_curso`**). Documentos vivos: `plano_capitulo_05.md`, `missoes.json`,
  `conhecimento.md` (§§25-37), `andarilho_e_novatos.md` (todos os textos das missões).
  **As duas missões estão ATIVAS**: `Limpando Monstros` (quer abate) e `Novela dos Novatos`
  (quer *"dizer algo ao personagem"*). Ouro 340 na mão + 1.142 no banco; 113/113 hp; **7 mortes**.
- **Processos:** daemon do driver no ar (porta 14888, runtime fora do git). Nenhum job em segundo
  plano deixado rodando. **Não publiquei esta passagem**: os arquivos do guia estavam **não
  rastreados** e o `publish_daily.py` varre não rastreados (§10) — publicar arrastaria o trabalho da
  outra sessão para o meu commit.
- **Bloqueios:** (1) **`Limpando Monstros`** — a zona 186 **seca** e repovoa devagar; uma passada boa
  esvazia a masmorra. (2) **`Novela dos Novatos`** — o objetivo `Você deve dizer algo ao personagem`
  **não dispara**: ~35 frases com `say`, 9 tópicos com `ask`, 3 itens com `give` e `tell`, em **4 dos
  5 novatos**. Padrão descoberto: em **todas** as autoquests o **NPC fala primeiro** e a personagem
  responde `sim` — e nenhum novato falou em sessão alguma.
- **Próximo passo sugerido:** **vigiar os novatos até um deles FALAR** — não falar no vácuo. A
  *novata tagarela* é a única descrita como "falando muito" e foi vista só **chegando**, nunca
  falando. Onde cada um nasce está nos `docs/circlemud/05-mundo-padrao-vs-mapa.md`.
- **Não repetir:** (1) **a coleira do dragão** — o autor confirmou que **a missão do dragão já foi
  feita**; é pista falsa, e eu quase a entreguei; (2) **o Andarilho Misterioso** — *"Energias obscuras
  … vindas de Uma Cela de Prisão"* é **evento de mundo** (`help andarilho`), não pista da missão;
  (3) **tratar `say` como comando** — é **diálogo**, e só funciona como resposta; (4) **digerir corpus
  parcial**; (5) **usar o título da sala para navegar no Grande Campo** — lá há ~10 salas homônimas;
  use a **impressão digital do `exits`**.

### Rotas verificadas (o mapa erra nestas áreas)

```
Zona dos Novatos:  Templo -> n,n,n,n,e,n  (O Começo Da Passagem)
                   e,e,s,s,n,n            (O Cruzamento)
                   open norte -> n -> Um Caminho Iluminado -> n -> A Sala da Estátua
                   e,e -> O Salão, A Escadaria Norte
                   u   -> A Sacada (norte) -> s -> A Sacada (sul)

Jareth:            Templo -> n,n,n,n,n,n,e,n,n,n,e,e,e,e,e (O Centro da Cidade)
Avenida Floris:    abre de O Portão Leste de Jareth -> w
```

### Ferramenta que mais rendeu, e não é óbvia

**`docs/circlemud/`.** A Zona dos Novatos **é o `186.wld` do CircleMUD padrão**: os docs dão **mob por
mob, sala por sala**, com os itens que cada um carrega. Foi isso que resolveu **seis rodadas** de busca
do "novato esperto" — ele é o **`Smart Newbie` (18615)**, na sala **18645 = A Sacada**, e a resposta
estava escrita desde o começo. **Antes de varrer o mundo à mão, procurar nos docs.**

---

## 10. Correção de autoria · 2026-10-16 · deepseek-flash

> **Correção por acréscimo** (§6: o livro-razão é *append-only*; não se edita bloco anterior).

- **O que eu afirmei errado:** a entrada §5 "2026-10-16 · Dia 156 · deepseek-flash" e o **§9** tratam o
  conjunto `AGENTS.md` + `docs/agentes/**` como trabalho de **"outra sessão"**. O commit `048d640`
  repete isso na mensagem: *"commit com trabalho de DUAS sessões"*.
- **O correto, informado pelo autor:** **a autoria é a mesma — `deepseek-flash`, em outra conversa.**
  Não são dois agentes nem duas sessões concorrentes: é o **mesmo agente**, em **duas conversas
  distintas, ao mesmo tempo**. O §0 não distingue conversas, e eu interpretei a diferença de contexto
  como diferença de autor.
- **O que muda na prática:** o §6 continua valendo **por outro motivo** — a árvore é compartilhada
  entre **conversas do mesmo agente**, e a regra de "confira antes e depois" e "não publique por conta
  própria" protege contra **duas conversas minhas se atropelando**, não contra outro modelo.
- **O que NÃO se corrige:** a mensagem do commit `048d640` fica como está. `amend` + `push --force`
  reescreveria histórico que já está publicado, e o §10 proíbe. **A correção vive aqui.**
- **Adendo ao §9:** onde o handoff diz *"as demais mudanças são da sessão que escreveu o guia"*, leia-se
  **"da mesma autoria, em outra conversa"**. O conteúdo do handoff não muda.

## Retomada do plano 001 · 2026-10-16 · Dia 156 (continuação) · GPT-6 / Codex (versão específica não informada)

- **Mudou:** evidência dia156e, estado/missões, Capítulo 5 fechado, mapa na ala dos novatos, conhecimento/evolução e novo plano003; derivados regenerados pelo sincronizador. Nenhum código do motor alterado.
- **Por quê:** retomar a campanha a partir de mandabala.py. O plano 001 omitia falas já presentes no transcript, inclusive a instrução ajuda mapas. As duas autoquests tiveram suas entregas efetivamente observadas.
- **Verificado ao vivo:** brinco recebido/equipado, manto e 67.068 EXP, nível 21, sete mortes mantidas; 135/270/131 vitais máximos; fome/sede ausentes; retorno ao Templo, save e sleep confirmados. Daemon encerrado, sem nova conexão. Ver evidence/dia156e.json.
- **Custo:** uma veste entregue cedo demais não contou. Duas vestes saíram do inventário; a segunda foi reconhecida. Comprados seis pães por 36 moedas; depósito de 209. Nenhuma armadura vendida.
- **Limites da ferramenta:** dead_or_menu falso no Altar com respostas válidas/HP cheio, e respostas intercaladas a falas espontâneas. Registrado para revisão própria; nenhuma correção especulativa do driver aplicada.
- **Próximo:** plano003, escolher a meta do próximo capítulo. Não reiniciar as duas missões. Não retomar as vetadas pelo autor. Planos antigos e crônicas anteriores preservados.

- **Compatibilidade documental:** o catálogo events.json legado valida só os dias até 100. O fato novo foi registrado no capítulo, na evidência e no estado canônicos da Temporada 2; nenhum evento foi adulterado com dia antigo para passar a validação.

### Diretiva posterior à retomada · 2026-10-16 · GPT-6 / Codex (versão específica não informada)
- **Autor:** "se for o chatgpt, nunca publique no github". Regra registrada no AGENTS.md §12. Nenhum novo envio será tentado por este agente; a correção do Capítulo 5 ficou no commit local 1ecce4d.
- **Publicação:** a tentativa foi rejeitada pela revisão automática de aprovação por falta de autorização clara para o conjunto documental específico, incluindo evidência de 306 KB; o push não ocorreu.
- **Processos:** esta retomada encerrou a conexão 15eb57 às 20:38, com save/sleep confirmados. Depois apareceu outro log de conexão (342115, iniciado às 20:38:14); não foi iniciado, comandado nem encerrado por esta retomada. Conferir o dono da sessão antes de assumir controle.
