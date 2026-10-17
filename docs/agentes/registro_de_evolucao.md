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

### 2026-10-17 · Dia 156 · deepseek-flash

> **Entrada de fechamento e limpeza.** O autor pediu três coisas: **arrumar o entulho**, **fechar e
> publicar o Capítulo 08** e **deixar pronto para o próximo agente**.

- **Mudou:**
  1. **`capitulos.json` id=8 fechado** — `status: concluido`, `closed_on_day: 156`, **13 parágrafos** de
     narrativa, 10 tags, 4 evidências e um campo novo **`carried_over`** dizendo em voz alta que **a
     autoquest `Uma Lição em Gargamel` continua ATIVA** (objetivo do servidor: *"entregar objeto ao
     personagem"*). **O capítulo fecha a expedição, não a missão** — e isso está no **dado**, não só na
     prosa.
  2. **`planos/plano013.md`** — o Capítulo 09: comprar a poção, entregar o jarro, e a porta trancada com
     o Papai Smurf atrás.
  3. **`state.json`** — `next_objective` apontando o plano 013, com **8 itens de preparação**, mantendo o
     campo **`missing_preparation`** que o `sync_hero.py` lê **por nome**.
  4. **Entulho limpo:** **18 scripts soltos** em `scripts/` (um por tentativa de fala) movidos para
     **`scripts/local/entulho_dia156/`**, que é gitignored.
- **Por quê:** o autor identificou o problema certo — *"o Argon começou o Gargamel e no meio, sem
  rastreio, o 3.8 assumiu e ficou em círculos"*. A auditoria **confirmou a causa**, e ela está escrita no
  `conhecimento.md` **§42.1**: **com `Limpando Monstros` ativa ao mesmo tempo, o `O Novato Alquimista`
  prioriza a própria missão, não dispara o diálogo do jarro — e ENG OLE a poção se a receber naquele
  estado.** O agente anterior tentou **18 frases diferentes em 18 scripts** em vez de ler essa regra.
- **Como foi verificado:** **leitura ao vivo** do `score` (nível 28, 4.229 de ouro, missão ativa, objetivo
  *"entregar objeto"*); `check_project.py` **0 erros**; `verificar.py` **18/18**; derivados conferidos; e
  **`scripts/devolutiva.py` → 0 falhas**.
- **Custo:** nenhum de ferramenta. **De jogo:** o Capítulo 08 fecha com a missão **pela metade** — por
  decisão do autor, e declarada no `carried_over`.
- **Próximo:** (a) **o ouro é o único bloqueio** — faltam **5.521** para a poção de 9.750; (b) **não
  reiniciar `Limpando Monstros`** antes de entregar a poção, ou o Alquimista engole o item de novo;
  (c) a pendência do **`mapa.json`** (4 arestas dos anéis do esgoto) **segue aberta** e o `devolutiva.py`
  a avisa em toda execução; (d) os 18 scripts estão em `scripts/local/entulho_dia156/` — se algum prestar,
  ele está lá, **fora do git**.

### 2026-10-17 · Dia 156 · Gemini 4 Argon / Gemini 3.8 Flash

> **Nona entrada do dia.** Avanço para o **Nível 27**, grind de 4.054 moedas de ouro, confinamento espacial no milharal (v1.6.2) e diagnóstico do Alquimista.
> **Divisão de autoria:** a primeira metade das ações e o início do levantamento da autoquest foram jogados por **`Gemini 4 Argon`**; com o esgotamento de tokens do modelo, o encerramento seguro, a otimização da rotina financeira no milharal, a criação de salvaguardas e o handoff foram assumidos e concluídos por **`Gemini 3.8 Flash`**.

- **Mudou:**
  1. **Evolução do Herói e Grind de Ouro** (`evidence/dia156i.json`, `state.json`, `hero.json`, `ficha.md`, `data/heroes.json`): Grebolius avançou do Nível 22 ao **Nível 27** (HP 172/172, Mana 330/330, MV 139/139, CA 136 com `armor` ativo por 31h, EXP 3.892.670, 64 treinos disponíveis). Saldo em dinheiro vivo elevado para **4.054 moedas de ouro** em incursões no milharal.
  2. **Motor e Rotinas v1.6.2** (`automato/rotinas/milharal.py`, `automato/nucleo/base.py`, `automato/CHANGELOG.md`, `scripts/farm_ouro_milharal.py`): confinamento espacial estrito no milharal (`'Milharal' not in t2`), prevenindo dispersão para `O Gramado` e preservando a segurança contra o DT `Adentro do Milharal Destruído` (Morte #5); suporte a `Cima` e `Baixo` em `base.py`; detecção ampla de todos os graus de fome e sede com abastecimento automático de pão e água antes e após o sono.
  3. **Diagnóstico de Concorrência de Autoquest** (`conhecimento.md` §42, `missoes.json`): diagnosticada a razão pela qual `O Novato Alquimista` não dispara o diálogo do `jarro brilhante` — ele monopoliza sua interação com a missão `Limpando Monstros`. Mapeada a estratégia de reset limpo com `quit` no Templo (autorizada pelo autor) assim que o saldo de 9.800 moedas for alcançado.
  4. **Novo plano de continuação**: criado `data/heroes/grebolius/planos/plano011.md` com a sequência exata de retomada e a devolutiva técnica preenchida.
- **Por quê:** executar a meta do autor de levantar fundos para a poção aquosa de `Uma Lição em Gargamel`, resolver o bloqueio do Alquimista e garantir sobrevivência automatizada sem riscos.
- **Como foi verificado:** sessões reais de caça e regeneração no Templo (`evidence/dia156i.json`), `sync_hero.py --check` (exit 0), `check_project.py` (0 erros), `automato/verificar.py` (18/18 itens OK), `devolutiva.py` (0 falhas).
- **Custo:** nenhum de inventário ou mortes (permanecem 8 mortes); personagem salva no Templo com vitais 100%.
- **Próximo:** executar `planos/plano011.md` — subir o daemon, farmar as ~5.750 moedas restantes até 9.800 no milharal, efetuar `quit` no Templo para limpar a concorrência, comprar a poção em Clariss (9.750), entregar a poção ao Alquimista pelo jarro, levar o jarro ao Minerador e resgatar Papai Smurf no Covil de Gargamel.

### 2026-10-17 · Dia 156 · Gemini 4 Argon / Gemini 3.8 Flash

> **Oitava entrada do dia.** Execução do `planos/plano009.md` e abertura do **Capítulo 08 — "Uma Lição em Gargamel"**.
> **Divisão de autoria:** a sessão ao vivo no MUD (diálogos, caminhada, exploração das áreas e lojas) foi jogada por **`Gemini 4 Argon`**; com o esgotamento de tokens do modelo, o encerramento seguro no Templo, a reconciliação documental, a fusão do mapa vivo e a redação do `planos/plano010.md` foram assumidos e concluídos por **`Gemini 3.8 Flash`**.

- **Mudou:**
  1. **Início da autoquest `Uma Lição em Gargamel`** (`evidence/dia156h.json`, `missoes.json`, `state.json`): aceita com `o smurf minerador` em `O Fim Do Túnel` na Vila dos Smurfs. O minerador precisa de iluminação confiável sem ferir ninguém. `O Novato Alquimista` (Escola de Treinamento) exige em troca `uma poção aquosa` de Clariss em Jareth (`As Misturas de Clariss`, custo: 9.750 moedas).
  2. **Mapeamento da Vila dos Smurfs e arredores** (`mapa.json`, `mapa_vivo.json`): expansão de 381 para 510 salas (+129 salas integradas via `fundir_mapa.py`), incluindo a rota da Estrada do Rei, Entrada da Vila dos Smurfs, Estrada Smurf, Travessa da Smurfette, Travessa do Papai Smurf, Pomar dos Smurfigos, Terra das Brincadeiras de Barney, Estrada e Entrada do Castelo de Gargamel, e O Covil de Gargamel (onde estão Gargamel, Azrael e a porta leste com Papai Smurf).
  3. **Levantamento Econômico e Lojas** (`maquina/verificacoes.md`, `conhecimento.md` §41): testadas lojas de armas e armaduras de Midgaard e Jareth; documentadas respostas de recusa de lojistas (*"não compro de forasteiros"*, *"não trabalhamos para sua classe"*, caixa limitado do ferreiro e armeiro de Midgaard). Saldo em moedas elevado para 4.880 (3.999 banco + 881 mão).
  4. **Conquista 34 desbloqueada**: *Cai Fora!* desbloqueada em `As Margens do Rio` ao avaliar o barco com o capitão aposentado.
  5. **Novo plano de continuação**: criado `data/heroes/grebolius/planos/plano010.md` com a devolutiva técnica preenchida.
- **Por quê:** avançar a campanha no Capítulo 08 conforme solicitado pelo autor e preparar a entrega segura para o próximo agente.
- **Como foi verificado:** sessão real no MUD, `save` no Templo de Midgaard (141/141 HP, 280/280 mana, 133/133 mv), `automato/acoes/digerir_mapa.py` e `fundir_mapa.py` (510 salas), `sync_hero.py`, `check_project.py` e `devolutiva.py`.
- **Custo:** nenhum; vitais cheios, zero mortes.
- **Próximo:** executar `planos/plano010.md` — levantar as ~4.870 moedas restantes para a poção aquosa na loja de Clariss em Jareth, entregá-la ao Alquimista, levar o jarro ao Minerador e resgatar Papai Smurf.

### 2026-10-16 · Dia 156 · Gemini 4 Argon

> **Sétima entrada do dia.** Execução integral do `planos/plano008.md` e fechamento do **Capítulo 07 —
> "O Que Eu Deixei no Meio"** (`Problemas Agrícolas` concluída após 66 dias de campanha).

- **Mudou:**
  1. **Autoquest `Problemas Agrícolas` concluída ao vivo** (`evidence/dia156g.json`, `missoes.json`,
     `state.json`, `capitulos.json` cap. 07): reiniciada com `O Pacificador` e executada nas **4 etapas**
     com `O fazendeiro` (10 `um monstro invasor`, 10 `um monstro esfomeado`, 5 `um monstro agressivo` e
     1 `o líder dos monstros`). Recompensa: **+9.088 EXP** e **`um belo cinturão de rodeio`** equipado
     na cintura (**CA 112 → 134**, **Acerto 5 → 10**, **Dano 2 → 7**, **DEX 15 → 16**, **CAR 11 → 12**).
     Avanço ao **Nível 22** (`141 HP`, `280 Mana`, `133 MV`, `1.572.738 EXP`) e depósito de **2.648 moedas**
     no banco (`3.999` banco + `300` mão = `4.299`).
  2. **`automato/rotinas/milharal.py` e `automato/CHANGELOG.md` (v1.6.1):** corrigido o filtro de
     `count_mobs(text)`, que exigia `'está aqui'` ou `'está jogado'` e por isso **ignorava todos os
     `um monstro invasor`** (*"Uma estranha criatura, verde e peluda, está procurando algo."*) e mirava
     cadáveres no chão.
  3. **`maquina/verificacoes.md` e `conhecimento.md` (§40):** documentadas as três causas do bloqueio
     histórico da missão (sair antes da 13ª fala do Pacificador; o filtro do `milharal.py`; e o fato de
     `score tudo` permanecer em *"Você deve matar criaturas."* ao fim das Etapas 1–3 até o jogador voltar
     à sala do fazendeiro), além dos atributos medidos do cinturão de rodeio.
  4. **`data/heroes/grebolius/mapa.json`:** atualizadas as salas da fazenda (`fazenda_milharal_borda`,
     `fazenda_entrada_casa`, `fazenda_sala_estar`, `fazenda_cozinha`) com os 4 tipos de monstros do
     milharal e os 3 membros da família do fazendeiro verificados ao vivo.
  5. **`data/heroes/grebolius/planos/plano009.md`:** criado o plano de transição pós-Capítulo 07 com a
     devolutiva técnica preenchida.
- **Por quê:** cumprir o objetivo do Capítulo 07 definido pelo autor em `planos/plano008.md` e eliminar o
  bug silencioso de `milharal.py` que impedia o fechamento da Etapa 1.
- **Como foi verificado:** sessão ao vivo no servidor (`evidence/dia156g.json`), `identify cinturão` +
  comparação empírica de `score tudo` antes/depois de vestir, `prepara.py --forcar`, `cuidar.py` (exit 0)
  e `save` no Templo. Validadores: `automato/verificar.py` **18/18 OK**, `sync_hero.py --check` **exit 0**,
  `check_project.py` **0 erros**, `devolutiva.py` **0 falhas**.
- **Custo:** nenhum de ferramenta; 0 mortes na sessão (permanecem 8).
- **Próximo:** aguardar diretriz do autor para o **Capítulo 08** em `planos/plano009.md` (faltam apenas
  **27.262 EXP** para o Nível 23; candidatas: `Uma Lição em Gargamel`, destravar `Dicas Mágicas` ou
  retornar aos Esgotos para a Serpente/Aligátor e gravar as 4 arestas pendentes dos anéis do esgoto).

### 2026-10-16 · Dia 156 · deepseek-flash

> **Sexta entrada do dia.** O autor entregou `Problemas Agrícolas` ao próximo agente. Esta entrada
> registra o plano e **as duas descobertas que o tornaram necessário**.

- **Mudou:** o **`planos/plano008.md`** — o plano do **Capítulo 07**, cujo objetivo é concluir
  **`Problemas Agrícolas`**. Ele traz o **briefing literal do Pacificador** (extraído dos transcripts), a
  rota verificada até a fazenda, o **bloqueio histórico** (a entrega que nunca foi confirmada, com o que
  já foi tentado por `ask` e o que **não** foi), os **valores medidos** dos bichos do milharal, o
  **perigo da armadilha mortal** que já matou uma vez lá dentro, e as ferramentas prontas
  (`milharal.py`, `encontrar_fazendeiro.py`, `falar_fazendeiro.py`). Também: **`conhecimento.md` §39**,
  e a **atualização do `state.json` e do `automato/DECISOES.md`**, que ainda diziam *"vetada"*.
- **Por quê:** **duas descobertas factuais** que mudam o planejamento:
  1. **O veto do autor CAIU.** A missão estava marcada *"vetada; não retomar"* desde o Dia 150, em três
     lugares. **Onde ainda se ler "vetada", está desatualizado** — exceto no `plano_capitulo_05.md`, que é
     **histórico** e registra o que valia naquele capítulo.
  2. **A missão está PERDIDA, não ativa.** O `score tudo` **não tem mais o bloco `[Autoquests em
     andamento]`** e o catálogo diz **`Não feita`** — mas o `autoquest listar` ainda a oferece. **Os onze
     abates acumulados não contam mais:** o próximo agente reinicia do zero. A causa provável é a que o
     §26 já documenta — **`quit` com missão em andamento zera o progresso**.
- **Como foi verificado:** tudo conferido **ao vivo** (`score tudo`, `autoquest todas`, `autoquest
  listar`), e o **briefing do Pacificador** extraído dos transcripts com as falas literais. Os valores
  por bicho foram medidos **abate a abate** (não por bloco de texto — a primeira medição inflava os
  números com recompensas de missão, e eu refiz). `check_project.py` **0 erros**; `verificar.py`
  **18/18**; derivados conferidos.
- **Custo:** nenhum de ferramenta. **De jogo:** o Capítulo 07 vai gastar sessão refazendo o que já foi
  feito no Dia 90 — **onze abates perdidos** por uma desconexão.
- **E a devolutiva funcionou — inclusive contra mim.** Na primeira versão, o plano declarava devolutiva
  do trabalho da **sessão anterior**; o **`scripts/devolutiva.py` reprovou** com duas falhas
  (*"promete referência de servidor, mas `maquina/verificacoes.md` NÃO foi tocado"*). **Foi o primeiro
  caso real de uso, e ele pegou exatamente o que existe para pegar.** Corrigi a tabela, escrevi o que
  faltava de verdade (**`conhecimento.md` §39**) e a verificação passou: **0 falhas, 4 avisos**.
- **Próximo:** (a) **a missão em si** — reiniciar com o Pacificador (`where pacificador`; ele anda entre a
  Praça do Templo, o Término da Rua e o Portão Oeste) e responder `say sim`; (b) **a aposta central do
  plano:** ler o `score` **antes** de cada ação, usar a **palavra literal**, tentar **`give`**, e **falar
  com a esposa e o filho** — que nenhum plano meu tentou; (c) a pendência que **continua aberta** e segue
  declarada: **as quatro arestas dos anéis do esgoto** no `mapa.json`.

### 2026-10-16 · Dia 156 · deepseek-flash

> **Quinta entrada do dia.** A pergunta do autor foi *"ele deixou de fazer algo de devolutiva técnica
> que devemos deixar mais explícito?"* — e a resposta virou ferramenta.

- **Mudou:** o motor ganhou a **v1.6** (`CHANGELOG.md`) com três peças:
  1. **`scripts/devolutiva.py`** — verificador de **fim de sessão**, **obrigatório**;
  2. **`scripts/test_devolutiva.py`** — **20 testes** (suíte **121 → 141**);
  3. a seção **`## 8. Devolutiva técnica`** no modelo do plano (`planos/LEIA.md`), o **`AGENTS.md`
     §6.2** e o item obrigatório no checklist de encerramento.
  Também: **`planos/plano007.md`** (o plano vigente, com a devolutiva preenchida como modelo), e a
  **renumeração da §29 → §38** no `conhecimento.md`.
- **Por quê:** o autor auditou o trabalho do `Gemini 3.8 Flash` e a resposta é que **ele atendeu o
  narrativo e deixou a devolutiva técnica pela metade** — nos **dois lugares exatos** que o
  `AGENTS.md` §5 nomeia:
  - **`mapa.json` intocado**, apesar de ele ter escrito uma seção chamada *"O mapa revelado: fechando os
    anéis do esgoto"*. **Quatro arestas que ele andou e provou serem de mão dupla continuam registradas
    como becos.**
  - **`maquina/verificacoes.md` nunca aberto**, apesar de ele ter encontrado o **aviso prévio de
    armadilha mortal** do servidor, um **rótulo novo de `consider`** (`Você é LOUCO!`) e a **mordida de
    um turno** do Dragão.
  E o sintoma que explica os dois: **nenhum validador enxerga isso.** O `check_project.py` confere
  **estrutura**, não **cobertura** — ele não sabe que uma caminhada aconteceu. **A lacuna é invisível, e
  foi por isso que ela se repetiu comigo (a crônica errada do capítulo 5) e com ele (o mapa).**
- **Como foi verificado:** as provas dele foram conferidas no transcript e **confirmadas**
  (`ajuda mapas` na linha **5562**, `ajuda remortar` na **8230**); e o próprio `devolutiva.py` foi rodado
  no repositório real: **0 falhas, 4 avisos, exit 2**. `check_project.py` **0 erros**; `verificar.py`
  **18/18**; suíte **141 testes OK**. Corrigi **quatro bugs meus** durante o desenvolvimento:
  (a) o `PENDENTE` era lido só na terceira coluna, e ele está na segunda; (b) a checagem lia **a prosa
  inteira** em vez das **linhas de tabela**, então qualquer menção a "mapa.json" disparava falha;
  (c) `HEAD~1` como janela erra quando a sessão já publicou — trocado pelo **commit que criou o plano
  anterior**; (d) **recursão infinita**, porque o script roda a suíte e o teste dele a chamava.
- **Custo:** mais uma seção obrigatória por plano e mais um passo no fim da sessão. **E o custo de NÃO
  ter isto já está medido: seis rodadas** procurando um NPC cuja sala estava num doc do repositório, e
  **uma crônica publicada errada**.
- **Próximo:** (a) a pendência que a devolutiva **declara em voz alta** — **corrigir as quatro arestas
  dos anéis no `mapa.json`**, o que exige **descer e conferir o `exits` ao vivo** (gravar sem andar
  seria inventar, §4.1); (b) o `maquina/dicionario_comandos.md` merece o mesmo tratamento que dei ao
  `verificacoes.md`; (c) o `check_project.py` ainda **não sabe validar cobertura** — enquanto não
  souber, o `devolutiva.py` é a única rede.

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

### Handoff · 2026-10-17 · Dia 156 · `deepseek-flash`

> **O primeiro handoff preenchido deste livro-razão.** Até aqui o §7 era só o modelo.

- **Estado da ferramenta:** `automato/` na **v1.6** (`CHANGELOG.md`). **Estável e verificado:**
  `verificar.py` **18/18**, `check_project.py` **0 erros**, suíte **141 testes**, e
  `devolutiva.py` **0 falhas**. O que existe de novo e funciona: **planos numerados** (§6.1),
  **`mandabala.py`** (retomada) e **`devolutiva.py`** (fechamento) — **os dois últimos são de uso
  obrigatório.**
- **Estado da campanha:** **Capítulos 0 a 8 `concluido`; o 9 está `em_curso`.** O 08 fechou
  **incompleto por decisão do autor** (ver `carried_over` nele). **Documentos vivos:**
  `planos/plano013.md` (é o plano vigente — rode `mandabala.py`), `capitulos.json` (id=9,
  "O Preço Não Se Mata com Raio"), `state.json` (`next_objective`), `conhecimento.md` §41-43 (a
  geografia dos Smurfs e **a regra da concorrência de autoquests no §42.1**), e `diretiva_de_jogo.md`
  §15-17.
- **Processos:** **nenhum.** O driver foi **encerrado depois de `save` + `sleep`** — não há processo
  python nem job em segundo plano, e a conexão caiu. **Quem continuar sobe um daemon novo.** O
  controlador ficou em `automato/runtime/.controller` (owner `DSH`).
- **Bloqueios:** **um só, e é numérico.** A missão `Uma Lição em Gargamel` está **ATIVA** com o objetivo
  *"entregar objeto ao personagem"*, e falta **ouro**: a `poção aquosa` de Clariss custa **9.750** e ela
  tem **4.229** — faltam **5.521**. O caminho já tentado e **falhado**: vender para os três lojistas de
  Jareth (recusam — ver plano 013 §4) e a rotina `xadrez` (proibida pelo autor). **Além disso, ela está
  com FOME E SEM COMIDA na bolsa** — `cuidar.py` acusou *"fome sem comida na bolsa"*.
- **Próximo passo sugerido:** **comprar comida na Padaria de Midgaard e comer** — antes de qualquer
  outra coisa. Depois disso, o plano 013 §4: juntar as 5.521 moedas.
- **Não repetir:**
  1. **Reiniciar `Limpando Monstros` antes de entregar a poção** — com ela ativa, o `O Novato
     Alquimista` **engole a poção sem dar o jarro** (`conhecimento.md` §42.1). **Foi o que fez o agente
     anterior girar em círculos.**
  2. **Escrever um script por tentativa de fala** — o Dia 156 deixou **18** desses; foram para
     `scripts/local/entulho_dia156/`. Use `play.py "say <frase>"` direto.
  3. **Inventar sinônimo** para o diálogo de missão — ele é **literal**.
  4. **`onde`** — não existe; só `where`.
  5. **`autoquest todas` como prova** — é histórico; a prova é o `score`.
  6. **Vender armaduras** (§15) e **`quit` com missão em andamento** (zera o progresso).
  7. **Fechar capítulo sem declarar a pendência** — se fechar incompleto, use os três lugares: o campo
     `carried_over`, o último parágrafo da narrativa e o plano seguinte.

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


### 2026-10-17 · Dia156 · GPT-6 / Codex (versão específica não informada)
- **Mudou:** evidência156j,estado/missões,parte factual do Cap08 em curso,mapa com12 correções e Poço Smurf,conhecimento§43,evolução e plano012; referências e decisão acrescentadas.
- **Por quê:** retomar plano011,entregar ciclo de Limpando sem reset,corrigir hipóteses e topologia com fonte.
- **Como foi verificado:** transcript72663a e trechos históricos curados; consultas finais em2026-10-17T10:17:27-03:00,linha1130. Validação estrutural/sincronização devem ser executadas pela root após esta gravação; não alegadas como já feitas.
- **Custo:** nenhum quit; sete abates de quest e recompensa94.227EXP confirmados. Demais custos constam nos registros/estado final,sem presumir resultado de caça.
- **Próximo:** Conferir o estado real e completar o saldo para a poção aquosa de Clariss (9.750; faltam 5.521 moedas), sem quit/reset: o Alquimista já pediu a poção e score marcou entregar objeto. Usar a rota pelo norte/Jareth comprovada no transcript156j, nunca a rota curta do plano011. Rever os guardas da caça antes de automatizar; o worker temporário teve falso alarme e não comprovou rendimento. Com peso 109/115 kg, conferir capacidade. Ao ter a poção, entregar somente com objetivo vigente e aguardar o jarro no diálogo completo. Não abrir outra conexão automaticamente em falha. Conexão fechada:True;save:True;sono:True. Motivo:Medidor da janela de 300 minutos caiu para 8% restantes; retirada e handoff conforme pedido do autor.. Sem GitHub.

Validação final desta retomada: derivados conferidos; check_project 0 erros/7 avisos (legado, metajogo, 68 treinos e capítulo aberto); verificar18/18 e suíte offline OK; devolutiva 0 falhas/1 aviso de arquivos locais pendentes. Aviso preservado: publicação proibida para este agente, sem GitHub; alterações anteriores permanecem locais. Daemon finalizou com código0; save/sono/socket confirmados.

### 2026-10-17 · Dia 156 · Gemini 3.8 Flash (High)
- **Mudou:** Criação de `data/heroes/grebolius/planos/plano014.md`, atualização da meta do Capítulo 09 em `data/heroes/grebolius/capitulos.json`, e inclusão da aba `abates.html` no site.
- **Por quê:** Diretiva direta do autor: *"o capitulo nove é terminar a missão e chegar no level 50"*. O Capítulo 09 foi formalmente redefinido para cobrir tanto o desfecho da cadeia de autoquests dos Smurfs/Gargamel quanto o ciclo de escalada de poder de Grebolius do Nível 28 até o patamar veterano no Nível 50.
- **Como foi verificado:** `python scripts/mandabala.py` validou a sequência, autoria e modelo do Plano 014; `python scripts/check_project.py` (0 erros), `automato/verificar.py` (18/18 OK), `python -B -m unittest discover -s scripts -p "test_*.py"` (141 testes OK) e `python scripts/devolutiva.py` (0 falhas).
- **Custo:** Nenhum. Grebolius segue em segurança absoluta no Templo de Midgaard (178/178 HP, 340/340 mana, 141/141 MV, 4.229 moedas, 5 pães recheados guardados na mochila de Pellinore, save e sono confirmados).
- **Próximo:** Executar a Fase 1 do Plano 014: acordar no Templo, alimentar-se com o pão da mochila, caçar no Milharal até levantar as 5.521 moedas restantes (alcançando 9.800 de ouro), comprar a poção aquosa em Clariss (Jareth), entregá-la ao Alquimista sem reativar Limpando Monstros, levar o jarro brilhante ao minerador, averiguar Papai Smurf no Covil de Gargamel, e gastar as 68 sessões de treino para a escalada até o Nível 50.

### 2026-10-17 · Dia 156 (sessão 2) · Gemini 3.8 Flash (High)
- **Mudou:** `automato/rotinas/milharal.py` (resiliência a emboscadas no trânsito e recall garantido entre tentativas falhas), `conhecimento.md` §44, `data/heroes/grebolius/evidence/dia156k.json`, `data/heroes/grebolius/state.json`, derivados via `sync_hero.py`, `automato/CHANGELOG.md` (v1.6.3), e criação de `data/heroes/grebolius/planos/plano015.md`.
- **Por quê:** Execução ao vivo do Plano 014 ("Mandabala"). Farm intensivo no Milharal para acumular o saldo de ouro necessário para comprar a `poção aquosa` de Clariss (9.750 moedas).
- **Como foi verificado:** 8 rodadas de caça executadas no Milharal via `automato/camadas/trabalhar.py --rotina milharal` supervisionada. 57 abates confirmados (invasores, agressivos, esfomeados e líder dos monstros). Ouro vivo saltou de 4.229 para 7.189 moedas (+2.960 líquido, descontados 30 ouros na compra de 5 pães na Padaria). EXP avançou para 4.191.978 (+191.977). Suprimentos plenos (3 pães na mochila, 3 na mão, cantil cheio). Armor mantido (+34, 24h restantes).
- **Custo:** Desconexão limpa por socket EOF pelo servidor DeBo ao término da 8ª rodada. Conforme AGENTS.md §13, a conexão foi encerrada e o estado consolidado em plano015 sem tentativa de reconexão forçada. Nenhuma armadura vendida.
- **Próximo:** Executar o Plano 015: iniciar o driver, rodar ~5 rodadas finais de milharal para levantar as 2.611 moedas restantes (atingindo 9.800 de ouro), viajar a Jareth para comprar a poção em Clariss, entregá-la ao Alquimista para obter o jarro brilhante, entregar ao minerador no Poço Smurf, investigar Papai Smurf no Covil de Gargamel, e avançar à Fase 2 (Nível 50).

