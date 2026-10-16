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
