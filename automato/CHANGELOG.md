# Controle de versão do automato

Versionamento semântico adaptado a um jogo: **MAIOR** muda o contrato das rotinas,
**MENOR** acrescenta camada/rotina, **CORREÇÃO** conserta comportamento.
As datas usam o **dia de jogo**.

## v1.6 — Dia 156 · a devolutiva técnica obrigatória
- **NOVO**: **`scripts/devolutiva.py`** — o verificador de **fim de sessão**. Confere o protocolo
  inteiro e **reprova** o que passar despercebido: plano numerado (número, autoria, seção de
  devolutiva **preenchida**), **coerência da devolutiva contra o `git diff`**, `parts` de capítulo
  (`source_kind`/`date`/`evidence`), autoria das evidências, bloco no livro-razão, e segredo rastreado.
  Códigos: **0** ok, **1** falha, **2** só avisos.
- **NOVO**: a seção **`## 8. Devolutiva técnica`** no modelo do plano (`planos/LEIA.md`), com os quatro
  destinos do `AGENTS.md` §5 — **mapa, referência do servidor, fato do mundo, erro do motor**.
- **NOVO**: `scripts/test_devolutiva.py` — **20 testes**. Suíte offline: **121 → 141**.
- **NOVO**: `AGENTS.md` **§6.2** e item **obrigatório** no checklist *"Antes de encerrar"*.
- **MOTIVO**: **duas sessões seguidas falharam do mesmo jeito no mesmo dia.** A primeira publicou uma
  crônica errada (leu o fim de uma cadeia e narrou como começo). A segunda **andou os esgotos,
  descobriu que quatro salas eram anéis de mão dupla**, escreveu o achado em prosa numa seção chamada
  *"fechando os anéis do esgoto"* — **e não tocou no `mapa.json`**. **Nos dois casos nenhum validador
  percebeu**: o `check_project.py` confere **estrutura**, não **cobertura** — ele não sabe que uma
  caminhada aconteceu. **É essa cegueira que este script cobre.**
- **DETALHE DE PROJETO**: a janela do diff é **o commit que criou o plano ANTERIOR** (o plano anterior
  nasce no fim da sessão passada). `HEAD~1` erra quando a sessão já publicou — aconteceu no primeiro
  teste, com o `conhecimento.md` já commitado.
- **ARMADILHA RESOLVIDA**: o script **roda a suíte de testes**, e pode ser chamado **de dentro dela** —
  `devolutiva.py` → suíte → `test_devolutiva.py` → `devolutiva.py`… **travou de verdade** durante o
  desenvolvimento. A guarda é a variável de ambiente **`DSH_DEVOLUTIVA_RODANDO`**, e há um teste que
  a exige.

## v1.5 — Dia 156 · planos numerados e o "mandabala"
- **NOVO**: **planos numerados** em `data/heroes/<id>/planos/planoNNN.md` — **append-only**, um por
  sessão, com **autoria** no cabeçalho. O autor chega, diz *"executa o plano NNN"*, e quem pegar
  continua como se fosse o anterior. Regra no `AGENTS.md` **§6.1** e no checklist de encerramento.
- **NOVO**: **`scripts/mandabala.py`** — acha o **plano mais alto** do herói e imprime, num bloco só, a
  **ordem de leitura**, as regras que não se negociam e o **conteúdo integral** do plano. Avisa quando
  a numeração tem **lacuna**, quando o plano pedido **não é o mais recente** e quando ele **não declara
  autoria**. `--listar`, `--numero N`, `--hero`, `--so-caminho`. Não edita, não joga, não publica.
- **NOVO**: `scripts/test_mandabala.py` — **25 testes** (descoberta, resolução de herói, cabeçalho,
  lacunas, modos da linha de comando, e a integridade do plano real do repositório).
- **MOTIVO**: a passagem de um agente para outro estava custando **rodadas inteiras de redescoberta** —
  seis delas só para achar um NPC cuja sala estava escrita num documento do próprio repositório. Um
  arquivo que se *atualiza* perderia a informação de quem veio antes; um **plano novo por sessão**, não.
- **MUDOU**: a suíte offline passou de **91 para 116 testes**.

## v1.4 — Dia 156 · segurança de sessão, comércio e mapa derivado
- **CORREÇÃO (segurança)**: **`term 200 80` no login** (`driver/debo_bot.py`, constantes
  `TERM_LINHAS`/`TERM_COLUNAS`). Sem isto, `commands`, `help` longo e `autoquest todas` abrem
  **paginador**, e enquanto ele espera o driver entra em `estado=dead_or_menu` — **que o vigia lê como
  MORTA**. Era a **segunda** fonte de falso positivo de morte (a primeira foi uma DICA com "Menu
  Principal").
- **CORREÇÃO**: **`sacar_para_comprar()`** em `camadas/prepara.py`. A padaria cobra da **mão** e o
  `prepara` só depositava: no Dia 156 ela ficou com fome, com 2 moedas na mão e 369 no banco. O alvo é
  `config.SAQUE_PARA_COMPRAR` (300) e **o banco não cobrindo emite AVISO**, não falha silenciosa.
- **NOVO**: **revisão da Sala de Doações** em `camadas/prepara.py` (`revisar_doacoes()`), por diretiva
  do autor. Critério **empírico**: veste a peça, lê `Classe de Armadura`/`Acerto`/`Dano` do `score tudo`
  e compara. Não superou → devolve a peça à sala. `--sem-doacoes` desliga.
- **NOVO**: `rotinas/mercado.py` — auditoria de comércio: anda até cada loja pelo mapa, roda `visible`
  e `list`, e grava a tabela (item, preço, nível, encargo, estoque).
- **NOVO**: `acoes/fundir_mapa.py` — mesclagem **idempotente** do levantamento no mapa curado, com
  `ALIAS_CAMINHADA` (identidade provada pela caminhada) e `ARESTAS_VERIFICADAS` (correção ao vivo).
- **MUDOU**: `acoes/digerir_mapa.py` passou a viver em `automato/acoes/` (era `scripts/local/`, fora do
  git) e aceita `--glob` **repetível**.
- **MUDOU**: `config.USAR_INVISIBILIDADE = False` — invisibilidade **bloqueia comércio**
  (*"Não negocio com quem não vejo!"*). A proteção passou a ser a **rota**, via
  `config.RISCO_A_EVITAR` (`danger`, `high`, `fatal`, `critical`).
- **AVISO OPERACIONAL**: **digerir corpus PARCIAL encolhe o mapa.** Rodar `digerir_mapa.py` só com um
  recorte e fundir levou o mapa de **360 para 224 salas**. O `--glob` precisa cobrir **todo** o corpus.
  Sintoma: o `TOTAL` do `fundir_mapa.py` **diminuir**.

## v1.3 — Dia 155 · identificação do agente
- **NOVO**: todo agente que operar o automato deve **dizer qual modelo é** no início do relatório e
  registrá-lo nos arquivos de evidência (campo `agent`) e na mensagem do commit (`[agente: <modelo>]`).
- **MOTIVO**: com mais de um agente mexendo no mesmo jogo, é preciso saber quem mudou o quê — e poder
  comparar o desempenho entre modelos.

## v1.2 — Dia 155 · autoexame e plano do capítulo
- **NOVO**: `automato/verificar.py` — autoexame em 18 itens (ambiente, core, driver, runtime, conhecimentos, rotinas, documentação).
- **NOVO**: `data/heroes/grebolius/plano_capitulo_03.md` — o plano do capítulo para o agente (missões, rotas, ferramentas, execução em 5 passos).
- **NOVO**: `automato/acoes/mapear.py` — mapear à mão uma sequência e buscar sala/saída por nome, gravando o caminho.
- **CORREÇÃO**: a guarda de repetição passou a contar **apenas assinaturas de problema** — salas homônimas de labirinto não a disparam mais.
- **CORREÇÃO**: a rotina `milharal` percorre o labirinto do bosque pela sala-marco ("O Pequeno Bosque" a leste) e a reta final é verificada sala a sala.

## v1.1 — Dia 155 · automato autossuficiente
- **MUDOU**: o **driver inteiro** (debo_bot.py, parsers.py, live_daemon.py, play.py) passou a viver em `automato/nucleo/driver/`.
- **MUDOU**: token, senha e logs foram para `automato/runtime/` — **fora do git** (`.gitignore`).
- **NOVO**: `automato/acoes/ressuscitar.py` (a ressurreição virou ação do automato).
- **NOVO**: `config.py` aponta os documentos do herói (`conhecimento.md`, `diretiva_de_jogo.md`, `mapa.json`) — referenciados, não copiados.
- **REQUISITO**: subir o driver antes de qualquer camada.

## v1.0 — Dia 155 · empacotamento
- **NOVO**: pasta `automato/` com núcleo, camadas, rotinas e documentação (README, CHANGELOG, DECISOES).
- **NOVO**: `nucleo/config.py` — um único ponto de configuração (caminhos, limites, magias).
- **MUDOU**: as rotinas leem `config` em vez de ter caminhos fixos; o automato roda fora de `scripts/local/`.
- **NÃO MUDOU**: o contrato das rotinas (partir do Templo, voltar, salvar).

## v0.6 — Dias 152-154 · trajeto determinístico
- **CORREÇÃO**: `base.py` apontava o token para o caminho errado — todas as rotinas liam vazio.
- **CORREÇÃO**: a rota da fazenda é **oeste, oeste, oeste** (Entrada da Fazenda → Pequena Estrada → Fim da Estrada → Milharal).
- **NOVO**: rota completa Templo→Milharal documentada no `conhecimento.md` §24: n5 → n,e,n → n6 → l6 → n,n,l,l,s → o3.
- **NOVO**: o caçador usa **LIGHTNING BOLT** (48-64 de dano) e mira o **nome exato** do monstro.

## v0.5 — Dia 150 · diretiva do autor
- **REMOVIDO**: venda de armaduras (rotina `xadrez` **suspensa** para `rotinas/_suspensas/`).
- **MOTIVO**: "perdemos mais dinheiro do que ganhamos com elas" — caixa finito do armeiro + armadura amaldiçoada (60 kg) + pergaminho de 8.509 para vender por 8.500.

## v0.4 — Dias 148-149 · camadas de decisão
- **NOVO**: `vigia.py` (diagnóstico pelo log), `prepara.py` (arrumador + banco), `trabalhar.py` (despachante), `turno.py` (encarregado).
- **NOVO**: **banco do Templo** no prepara (`deposit`), com reserva de 300 na mão.
- **NOVO**: hidratação na **fonte de mármore azul** da Praça do Templo (`fill cantil fonte` / `drink fonte`).
- **CORREÇÃO**: o prepara só compra pão se não tiver (ela acumulou 10 e ficou em 130/115 kg).

## v0.3 — Dia 147 · higiene e alvo
- **NOVO**: `abastecer()` — comer e beber **antes** de dormir/viajar (dormir faminto consumia vida e mana).
- **CORREÇÃO**: caçador com **plano B de alvo** quando a magia pergunta "em que?".

## v0.2 — Dia 143 · guarda de repetição
- **NOVO**: `guarda.py` — mesma resposta **3× seguidas** → `recall` + `save` + saída (código 9).
- **NOVO**: injeção da guarda no `run()` de **33 robôs**.
- **CORREÇÃO**: a guarda passou a **ignorar comandos benignos** (buy/eat/drink/look/score/rest/sleep) — compras legítimas a disparavam.

## v0.1 — Dia 141 · método
- **NOVO**: o método "mapear à mão → testar em trechos → só então automatizar".
- **NOVO**: `wake; stand` obrigatório antes de qualquer deslocamento.
- **MOTIVO**: 7 mortes, das quais **4 causadas por script sem supervisão**.

## Próximas versões (planejado)
- **v1.1**: rotina `dicas-magicas` (descobrir o gatilho do ciclo do "sim").
- **v1.2**: rotina `esgoto` de verdade (reconhecimento com mapa incremental).
- **v1.3**: o turno relançar a rotina sozinho quando o vigia voltar a OK.
