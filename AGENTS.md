# AGENTS.md — guia de operação para agentes

> Este é o **primeiro arquivo** que um agente deve ler neste repositório. Ele não conta a história da
> campanha: descreve **como o projeto funciona**, **o que é boa prática aqui**, **onde procurar cada
> coisa** e **onde registrar o que você evoluiu**. A narrativa vive em `data/heroes/<id>/`, não aqui.

> ## ▶ Comece aqui — vale para qualquer modelo
>
> 1. `python scripts/mandabala.py` — o plano vigente e a **sequência de abertura**, com a sua primeira ação.
> 2. [`docs/agentes/PROTOCOLO.md`](docs/agentes/PROTOCOLO.md) — a sessão inteira em comandos:
>    abertura, cada bloco de jogo, encerramento/handoff. **Se só for ler uma coisa, leia esta.**
> 3. Para encerrar: `python scripts/encerrar.py --agente "<modelo/versão>"`. Ele cria o esqueleto do
>    próximo plano e roda todas as verificações.
>
> Se `python` abrir a Microsoft Store ou disser "Python was not found", a máquina não tem o Python no
> PATH: rode **uma vez** `powershell -ExecutionPolicy Bypass -File scripts\configurar_python.ps1 -Aplicar`
> e reabra o terminal. Até lá, use `py` ou o caminho completo
> `%LOCALAPPDATA%\Programs\Python\Python312\python.exe`. O `automato/verificar.py` avisa quando isso acontece.
>
> O resto deste arquivo explica **por quê**. As invariantes da §4 valem sempre.

Índice: [Regra zero](#0-regra-zero--identifique-se) ·
[O repositório](#1-o-que-é-este-repositório) ·
[Lógica](#2-como-a-lógica-funciona-em-uma-tela) ·
[Fonte da verdade](#3-fonte-da-verdade--não-duplique) ·
[Invariantes](#4-invariantes-não-quebrar) ·
[Boas práticas](#5-boas-práticas) ·
[Registro de evolução](#6-registrar-o-que-você-evoluiu) ·
[Onde consultar](#7-onde-consultar) ·
[Glossário](#8-glossário) ·
[Checklists](#9-checklists) ·
[Trabalho concorrente](#10-trabalho-concorrente-leia-antes-de-editar)

Documentos de apoio, em `docs/agentes/`:

| Arquivo | Para quê |
| --- | --- |
| [arquitetura.md](docs/agentes/arquitetura.md) | a lógica do projeto em detalhe: planos, fluxos, contratos, o que é derivado |
| [boas_praticas.md](docs/agentes/boas_praticas.md) | o que fazer e o que não fazer, com o motivo de cada regra |
| [glossario.md](docs/agentes/glossario.md) | cada artefato do repositório e cada termo do domínio |
| [onde_consultar.md](docs/agentes/onde_consultar.md) | mapa de consulta e ordem de precedência das fontes |
| [registro_de_evolucao.md](docs/agentes/registro_de_evolucao.md) | o livro-razão onde cada agente registra o que mudou na ferramenta |

---

## 0. Regra zero — identifique-se

Todo agente que **jogar, editar ou publicar** declara **modelo e versão** em quatro lugares:

1. no **início do relatório** entregue ao autor;
2. no campo `"agent"` do arquivo de evidência que gravar: `{"agent": "<modelo/versao>", "via": "automato"}`;
3. no fim da **mensagem do commit**: `[agente: <modelo/versao>]`;
4. no bloco que você acrescenta ao [registro de evolução](docs/agentes/registro_de_evolucao.md).

**Motivo:** mais de um agente joga e mexe na mesma ferramenta, às vezes ao mesmo tempo. Sem autoria não
há como saber quem mudou o quê, nem comparar o desempenho entre modelos. Fonte:
`automato/DECISOES.md` §8 e `automato/CHANGELOG.md` v1.3.

---

## 1. O que é este repositório

Três planos que se comunicam **por arquivos**, nunca por estado em memória compartilhada:

| Plano | Onde | O que é | Escreve o quê |
| --- | --- | --- | --- |
| **Apresentação** | `index.html`, `ficha.html`, `mapa.html`, `sobre.html`, `css/`, `js/`, `audio/` | site estático (Vercel) que **lê** os JSON de `data/` no navegador | nada de conteúdo: só exibe |
| **Campanha** | `data/` | a memória documental: crônicas, estado, missões, mapa, evidência, fichas | o agente-escritor, sempre com fonte |
| **Motor** | `automato/` (canônico), `scripts/` (documental + expedição), `skills/` (método) | como se joga: driver, camadas, rotinas, validadores, sincronizador | o agente-operador, e registra em `automato/` |

`docs/` guarda método e pesquisa; `maquina/` guarda **referência técnica do MUD** (comandos, magias,
comparação CircleMUD × DeBo); `skills/` guarda o procedimento operacional reutilizável.

---

## 2. Como a lógica funciona, em uma tela

**Laço de sessão (ao vivo, no MUD):**

```text
localizar/preparar → trânsito verificado por sala-marco → trabalhar (rotina)
        ↑                                                        ↓
        └──────── vigia + cuidado + recarga ←── guarda de repetição
```

**Laço documental (offline, no repositório):**

```text
observação real → evidência (evidence/, observacoes/, transcript)
                → state.json (último estado REGISTRADO, com origem)
                → crônica (posts.json) / mapa (mapa.json) / missões (missoes.json)
                → derivados por sync_hero.py (ficha.md, hero.json, data/heroes.json)
                → check_project.py → publish_daily.py
```

**A regra que costura os dois:** nada entra em `data/` sem **fonte registrada**, e nenhum derivado é
editado à mão. A unidade de publicação da Season 01 é o **dia**; da Season 02 em diante é o
**capítulo** — o sono encerra a sessão, não o capítulo.

Detalhamento completo em [arquitetura.md](docs/agentes/arquitetura.md).

---

## 3. Fonte da verdade — não duplique

| Domínio | Arquivo canônico | Derivados (nunca editar à mão) |
| --- | --- | --- |
| Estado mecânico do herói | `data/heroes/<id>/state.json` | `ficha.md`, `hero.json`, cartões em `data/heroes.json` |
| Crônicas | `posts.json` (dias) e `capitulos.json` (capítulos) | `site` (leitura), `ciclos.json` para blocos fechados |
| Missões | `missoes.json` | `ficha.md`, `missoes.md` (leitura editorial) |
| Mapa | `mapa.json` (curado) | `mapa_vivo.json` (levantamento derivado), `mapa.md` é **histórico** |
| Rotas e economia | `conhecimento.md` | — |
| Regras de como jogar | `diretiva_de_jogo.md` | rotinas e camadas do `automato/` |
| Referência de servidor | `maquina/` e `docs/circlemud/` | `docs/expedicao_comandos.md` |
| Configuração do motor | `automato/nucleo/config.py` (**ponto único**) | — |
| Versão e decisões do motor | `automato/CHANGELOG.md`, `automato/DECISOES.md` | este guia |

Se você sentir vontade de copiar um dado de um arquivo para outro, provavelmente o certo é
**referenciar** (link) ou regenerar pelo sincronizador.

---

## 4. Invariantes (não quebrar)

1. **Fonte antes de afirmação.** Observação, interpretação e dúvida se registram separadas. Manual,
   `help` e dica **não** são teste executado.
2. **Identifique-se** (§0) em relatório, evidência e commit.
3. **Não invente acontecimento.** Sem evidência, o fato fica como pendência ou dúvida — nunca como cena.
4. **Derivados só via `sync_hero.py`.** Números em `ficha.md` e cartões são saída, não entrada.
5. **Não reescreva o legado.** Crônicas antigas preservadas; correções entram como nota datada.
6. **Rotina nunca roda sem supervisão.** Job em segundo plano + leitura do log a cada ~60 s; se o vigia
   acusar problema, mate o job.
7. **O vigia lê o log, não o jogo.** Mandar `score` durante a rotina desincroniza a sessão.
8. **`save`, nunca `quit`, com missão em andamento.** `quit` apaga o progresso das missões.
9. **Segredos ficam em `automato/runtime/`** (fora do git). Nunca colar senha, token ou transcrição com
   credencial em documento, log ou mensagem de commit.
10. **Diretivas do autor vencem.** Ex.: **proibido pegar ou comercializar itens/armaduras amaldiçoados**
    (itens da Torre Negra ou de peão são permitidos se NÃO forem amaldiçoados; fazer dupla checagem com `identify`
    no chão antes do `get`, pois NODROP impede descarte); rotina xadrez só coleta espólios limpos com triagem prévia.
11. **Encerrar sessão = `save`.** A publicação é passo separado e explícito.
12. **Editar arquivo e executá-lo não cabem no mesmo bloco de ferramentas** — elas rodam em paralelo;
    edite, confira o arquivo e só então execute, em chamadas separadas.
13. **Estar na etapa certa para fazer a coisa certa — NUNCA entregar item (`give`) ou comprar suprimento caro sem confirmação formal da etapa** (diretiva urgente do autor, Dia 156).
    O comando `give <item> <npc>` consome o item de forma irreversível e compras de alto valor (ex.: poção aquosa de 9.750 moedas) drenam o caixa do herói.
    - **Regra de Ouro:** Estar na etapa certa antes de agir. Constar a quest em `score tudo` **não basta** se não estiver na **sub-etapa exata** de entrega.
    - **Como validar a etapa:** Rodar `score tudo` e confirmar que a autoquest sob `[Autoquests em andamento]` exibe a **instrução específica da etapa**, por exemplo:
      `Uma Lição em Gargamel: Você deve entregar objeto ao personagem.`
      Se constar apenas o título da quest (ex.: `Uma Lição em Gargamel`) sem a instrução de entrega, a etapa anterior (monólogo de ativação do NPC anterior, direcionamento ou pergunta do NPC alvo) AINDA NÃO FOI CONCLUÍDA e o NPC **não** reconhecerá a entrega, consumindo o item no vazio!
    - Todo diálogo prévio com NPCs da cadeia deve ser ouvido integralmente até o fim (sem cortar monólogos nem dar `recall` no meio da fala);
    - Nunca responder `say sim` a convites de outras quests concorrentes na mesma sala antes da entrega;
    - Confirmar presença no `inventory`;
    - Parar se o estado não for o esperado — nunca doar item no escuro.
14. **Falar com NPC em missões NUNCA é automatizado** (diretiva do autor, Dia 156).
    Interações verbais de missão (`say`, `ask`, `whisper`, gatilhos de diálogo) **jamais** devem ser executadas por scripts automáticos em lote. A interação é feita **exclusivamente por resposta direta do agente ao contexto em tempo real**: lendo a fala integral do NPC, checando o objetivo em `score tudo`, verificando a sala e o inventário, e respondendo conscientemente para evitar aceitar missões erradas, engolir etapas ou perder itens.
15. **Postura Heroica Proativa — Não fazer o mal, proteger inocentes e questionar o autor** (diretiva essencial do autor, Dia 156).
    A moral de Grebolius é regida por uma **ética heroica proativa**, nunca apenas por reação mecânica a números:
    - **Olhar de heroína:** Olhar para um cachorro e enxergar *um cachorro, um animalzinho inocente e indefeso*, e não um alvo de estatística para cumprir meta. De forma genérica: **não fazer o mal, não bater em pessoas pacíficas, não machucar animais indefesos**.
    - **Criatividade com consciência:** Ao bolar planos criativos, ter discernimento prévio. **Nunca abater uma criatura para "descobrir depois" se era errado.** Se não for comprovadamente uma ameaça hostil, monstro invasor ou criatura do mal, não atacar.
    - **Dever de questionar o autor:** Se o próprio autor Peter der uma instrução que implique bater em inocentes, maltratar animais ou violar a postura heroica, o agente **DEVE QUESTIONÁ-LO** antes de executar.
    - **Double check reativo:** Se, por imprevisto mecânico do servidor, qualquer ação reduzir a moral/alinhamento (compass `{<<<<<>----}` e pontuação no `score`), parar imediatamente, auditar a causa no log e banir a reincidência.


---

## 5. Boas práticas

Resumo do que mais custa caro quando é ignorado (detalhe e motivo em
[boas_praticas.md](docs/agentes/boas_praticas.md)):

- **Verificar antes de acreditar.** Uma resposta cortada pela latência não é o estado do jogo; `None`
  não é zero; sinal de morte exige a linha inteira.
- **Mapear à mão → testar em trechos curtos → só então automatizar.** Esta ordem é a doutrina do
  projeto, registrada em `diretiva_de_jogo.md` §9.
- **Andar por sala-marco**, nunca por contagem de passos; a origem da rota é a sala onde a personagem
  **está**, não onde se supõe que esteja.
- **Registrar a divergência quando ela aparece**: correção de referência vai para
  `maquina/verificacoes.md` (com data, contexto, resposta e fonte); fato novo do mundo vai para
  `conhecimento.md`; mapa corrigido vai para `mapa.json`.
- **Validar antes de publicar:** `sync_hero.py --check`, `check_project.py`, suíte offline.
- **Uma mudança, um propósito.** Commit pequeno, com prefixo (`feat`, `fix`, `docs`, `chore`), escopo e
  trailer de agente.
- **Não publique sem pedido.** Editar arquivos **não** autoriza `--publish`/`--push`.
- **Mudança no motor entra no `CHANGELOG.md` e, se for decisão com custo, no `DECISOES.md`.**

---

## 6. Registrar o que você evoluiu

Este projeto é feito para **vários agentes**. Duas coisas diferentes precisam ser registradas:

| O que você fez | Onde registra |
| --- | --- |
| **Encerrou uma sessão de jogo** | **crie o próximo plano numerado**: `data/heroes/<id>/planos/planoNNN.md` — **nunca edite o anterior** (ver §6.1) |
| Evoluiu a **ferramenta** (automato, scripts, camadas, rotinas, config, skills) | bloco novo em [registro_de_evolucao.md](docs/agentes/registro_de_evolucao.md) **+** `automato/CHANGELOG.md` (versão) **+** `automato/DECISOES.md` (se houver decisão e custo) |
| Evoluiu a **campanha** (jogou, descobriu, corrigiu o mundo) | `data/heroes/<id>/` conforme o laço documental, com evidência |
| Corrigiu uma **referência técnica** do MUD | `maquina/verificacoes.md` e o resumo em `maquina/dicionario_comandos.md` |
| Abriu/decidiu algo que o próximo precisa saber | bloco de **handoff** no fim do seu registro |

### 6.1 Planos numerados — o ponto de continuação da campanha

> **Regra de encerramento de sessão.** Toda sessão de jogo termina criando o **próximo plano
> numerado**. O autor chega, diz **"executa o plano 98"**, e quem pegar continua **como se fosse o
> anterior continuando** — sem redescobrir, sem repetir caminho errado, sem perder conquista.

```
data/heroes/<heroi>/planos/
    LEIA.md        <- como funciona e o modelo do plano
    plano001.md
    plano002.md
    ...
```

1. **Nunca edite um plano antigo.** São **append-only**. Errou? Crie o próximo e diga nele no que o
   anterior falhava. *(Mesma regra do registro de evolução.)*
2. **Sempre crie um novo, com o próximo número** — três dígitos, com zeros à esquerda
   (`plano002.md`). O número é **local ao herói**.
3. **Todo plano diz quem o fez** — modelo/versão no cabeçalho. Sem isso não se sabe a quem perguntar,
   nem se compara desempenho entre modelos.

**O que um plano não pode deixar faltar:** número, data, **autor**, estado exato (números, não
adjetivos), o **próximo passo único**, os **bloqueios com o que já foi tentado**, e a lista do que
**não repetir**. O modelo completo está em
[`data/heroes/grebolius/planos/LEIA.md`](data/heroes/grebolius/planos/LEIA.md).

**Para retomar, o autor diz "mandabala" e roda:**

```bash
python scripts/mandabala.py            # o plano vigente + a ordem de leitura
python scripts/mandabala.py --listar   # todos os planos, com autor e objetivo
python scripts/mandabala.py --numero 3 # um plano específico
```

O `scripts/mandabala.py` acha o plano mais alto, **avisa** se a numeração tem lacuna, se o plano pedido
não é o mais recente ou se ele não declara autoria, e imprime o **conteúdo integral** do plano junto com
a ordem de leitura. Não edita, não joga, não publica.

**Por que assim:** se cada um editasse o mesmo arquivo, a informação do anterior sumiria — e é
exatamente essa informação que evita refazer seis rodadas de busca.

### 6.2 A devolutiva técnica é obrigatória — e é conferida contra o git

> **`python scripts/devolutiva.py`** — rode **antes de encerrar** e **resolva todas as FALHAS**.
> Código 0 = tudo certo; 1 = falha; 2 = só avisos.

A §6.1 resolve **onde o próximo começa**. Esta resolve **o que o próximo precisa saber** — e o problema
que ela ataca é sutil: **a descoberta existe, e o artefato não mudou.**

**O caso real (Dia 156), duas vezes no mesmo dia:**

- uma sessão **publicou uma crônica errada** — leu o fim de uma cadeia e narrou como começo;
- outra **andou os esgotos, descobriu quatro anéis de mão dupla**, escreveu o achado em prosa numa
  seção chamada *"fechando os anéis do esgoto"* — **e não tocou no `mapa.json`**.

**Nenhum validador percebeu, nos dois casos.** O `check_project.py` confere **estrutura**, não
**cobertura**: ele não sabe que uma caminhada aconteceu. **É essa cegueira que o `devolutiva.py`
cobre.**

**Como funciona.** O plano ganha uma seção **`## 8. Devolutiva técnica`** (modelo no `LEIA.md`), com uma
tabela de quatro linhas — **mapa, referência do servidor, fato do mundo, erro do motor** — dizendo em
qual artefato cada descoberta foi gravada. O verificador então:

1. exige a seção no plano mais alto, **preenchida** (só o modelo não conta);
2. **confere cada linha da tabela contra o `git diff`**: se diz `mapa.json`, o `mapa.json` **tem** de ter
   mudado na sessão;
3. trata **`PENDENTE` como aviso, não falha** — declarar o que não se fez é o comportamento **certo**;
4. confere `parts` de capítulo (`source_kind`, `date`, `evidence`), autoria das evidências, bloco no
   livro-razão, e se há segredo rastreado.

**A janela do diff é o commit que criou o plano ANTERIOR** — porque o plano anterior nasceu no **fim** da
sessão passada. `HEAD~1` erra quando a sessão já publicou (foi o que aconteceu: o arquivo já estava
commitado).

**Custo:** mais uma seção obrigatória por plano, e mais uma coisa para rodar no fim. **O ganho é o que
não se perde** — e o custo de não ter isto já foi medido: **seis rodadas** procurando um NPC cuja sala
estava num doc do repositório, e uma **crônica publicada errada**.

Formato mínimo de um bloco (copie de [registro_de_evolucao.md](docs/agentes/registro_de_evolucao.md)):

```markdown
### <AAAA-MM-DD> · <dia de jogo ou "—"> · <modelo/versão>
- **Mudou:** <arquivos e o que passou a valer>
- **Por quê:** <problema real observado>
- **Como foi verificado:** <comando/teste/sessão, com resultado>
- **Custo:** <o que se perde, ou "nenhum">
- **Próximo:** <o que continua aberto>
```

Regra do livro-razão: **append-only**. Não edite bloco alheio; corrija acrescentando um novo bloco que
referencia o anterior.

---

## 7. Onde consultar

Mapa completo e ordem de precedência em [onde_consultar.md](docs/agentes/onde_consultar.md). Atalho:

| Preciso de… | Consulte |
| --- | --- |
| Como operar o motor / rodar uma rotina | `automato/README.md`, `docs/rotinas.md` |
| O que já foi tentado, decidido e custou caro | `automato/DECISOES.md`, `automato/README.md` (§ lições de campo) |
| Comandos, magias, diferenças do servidor | `maquina/README.md`, `maquina/dicionario_comandos.md`, `maquina/spells.md` |
| Números do motor CircleMUD (para validar no DeBo) | `docs/circlemud/00-afirmacoes-e-validacao.md` e os demais `docs/circlemud/` |
| Método de sessão / de capítulo | `skills/mud-ciclo-diario/`, `skills/mud-capitulo/` |
| Modelo de temporadas, tomos e capítulos | `docs/season_capitulos.md` |
| Expedição modular (motor V2) | `docs/expedicao_modular.md`, `skills/mud-expedicao-modular/` |
| Regras de jogo vigentes do herói | `data/heroes/<id>/diretiva_de_jogo.md` |
| Estado, missões, mapa do herói | `data/heroes/<id>/state.json`, `missoes.json`, `mapa.json` |
| O que cada arquivo é | [glossario.md](docs/agentes/glossario.md) |

**Precedência:** resposta real do servidor nesta sessão > observação registrada com data > ajuda do DeBo
(`maquina/`) > engine CircleMUD (`docs/circlemud/`) > manual importado. Quando as fontes discordarem,
**registre a divergência** em vez de escolher em silêncio.

---

## 8. Glossário

[glossario.md](docs/agentes/glossario.md) cobre: cada artefato (raiz, `data/`, `docs/`, `maquina/`,
`automato/`, `scripts/`, `skills/`, pastas não versionadas), os campos recorrentes de JSON
(`schema_version`, `as_of`, `verification`, `source_kind`, `evidence_policy.legacy_through_day`,
`risk_code`, `record_status`), os conceitos do domínio (dia, ciclo, temporada, tomo, capítulo, parte,
fecho, autoquest, sala-marco, fronteira, wimpy, DT), os códigos de saída das camadas e os diagnósticos
do vigia.

---

## 9. Checklists

> **A versão executável destes checklists é o [PROTOCOLO.md](docs/agentes/PROTOCOLO.md)** (abertura
> §1, encerramento §3), com `mandabala.py` na entrada e `encerrar.py` na saída. As listas abaixo
> explicam o conteúdo. Se divergirem do PROTOCOLO, corrija os dois.

**Antes de começar**

- [ ] Li o `README.md` da raiz e este arquivo.
- [ ] **Rodei `python scripts/mandabala.py`** e li o plano vigente **inteiro** (§6.1).
- [ ] Sei qual herói, qual temporada/capítulo e qual o objetivo verificável.
- [ ] Li `diretiva_de_jogo.md` e as pendências em `missoes.json` / plano do capítulo.
- [ ] Sei onde vou escrever e qual é a fonte da verdade daquele dado.
- [ ] `git status` e `git log -5` conferidos (ver §10).
- [ ] Se vou jogar: driver no ar, `automato/verificar.py` sem FALHA, supervisão combinada.
- [ ] Se vou jogar: li o **ritual** de `diretiva_de_jogo.md` §23 e o aplico antes de **cada bloco**: rota no mapa => `automato/camadas/navegar.py`, nunca sala a sala; fala/`give`/compra de missão => à mão, linha a linha; vida cai => `recall`, não recuar andando.

**Antes de encerrar**

> **🔴 OBRIGATÓRIO: `python scripts/devolutiva.py`** — e **resolver todas as FALHAS**. Ele é a
> verificação do protocolo inteiro, e existe porque duas sessões seguidas falharam do mesmo jeito no
> Dia 156: uma publicou crônica errada, a outra andou os esgotos e **não gravou no `mapa.json` o que
> descobriu**. **Nos dois casos nenhum validador percebeu** — o `check_project.py` confere
> **estrutura**, não **cobertura**; ele não sabe que uma caminhada aconteceu. Ver §6.2.

- [ ] **`python scripts/devolutiva.py` rodado, com 0 falhas** (avisos lidos, não silenciados).
- [ ] **`python scripts/auditar_sessao.py`** rodado sobre o transcript da sessão; cada FALHA corrigida ou justificada no plano, cada AVISO explicado (não confere §9/§14: origem do comando não é registrada).
- [ ] Evidência gravada, com `agent` e origem.
- [ ] **Plano numerado criado** em `data/heroes/<id>/planos/planoNNN.md` — o **próximo** número,
      **sem editar o anterior** (§6.1). É o ponto de continuação que o autor executa dizendo
      *"executa o plano NNN"*.
- [ ] `state.json`, missões, mapa e conhecimento atualizados com a origem de cada mudança.
- [ ] Crônica escrita a partir dos fatos registrados; incertezas marcadas como incertezas.
- [ ] `python scripts/sync_hero.py --hero <id>` e `--check`.
- [ ] `python scripts/check_project.py` (0 erros; avisos lidos, não silenciados).
- [ ] Bloco no [registro de evolução](docs/agentes/registro_de_evolucao.md) e, se mexeu no motor,
      `automato/CHANGELOG.md` (+ `DECISOES.md`).
- [ ] Nada de segredo, sessão, log ou credencial adicionado ao git.

---

## 10. Trabalho concorrente (leia antes de editar)

Esta árvore de trabalho é **compartilhada** — e isso foi observado, não suposto: durante a escrita deste
guia, outra sessão publicou três commits (o HEAD avançou de `96bf42c` para `158da9e` em ~15 minutos) e a
revisão `158da9e` **levou junto dois arquivos deste conjunto** que estavam apenas no disco, ainda não
rastreados. Consequências práticas:

- **Confira antes e depois.** `git status --porcelain`, `git log -5` e `git diff --stat` no começo e no
  fim do seu trabalho. O arquivo que você leu pode ter mudado.
- **Nunca `git add -A` / `git add .`** e nunca `git commit -a`: você arrastaria o trabalho de outro
  agente para a sua revisão. Prepare caminhos explícitos.
- **Nunca reescreva histórico** (`rebase`, `amend` de commit alheio, `reset --hard`, `push --force`).
- **O publicador varre arquivos não rastreados.** `publish_daily.py` monta a revisão a partir de
  `git diff HEAD` **mais** `git ls-files --others --exclude-standard`; arquivos novos seus podem entrar
  no commit de outro agente. Se isso importa, avise no seu registro e confira `git log` depois.
- **Se sua mudança toca `maquina/` ou `docs/*.json`,** o publicador a **exclui** da revisão (a lista de
  caminhos publicáveis em `publish_daily.py` cobre `data`, `css`, `js`, `scripts`, `skills`, `docs/*.md`,
  `automato`, `audio` e um conjunto fixo de arquivos da raiz). Comite esses arquivos à parte, ou trate a
  ampliação da lista como uma decisão registrada.
- **Não publique por conta própria.** Editar arquivos não autoriza `--publish`/`--push`; a sessão que
  joga é a dona da sessão, não do repositório.

---

## 11. Estado verificado

Conferido em **2026-10-16**, durante trabalho concorrente de outra sessão (HEAD mudou três vezes no
intervalo da conferência). Revalide antes de confiar nestes números.

- Dois heróis em `data/heroes/`: **grebolius** (campanha ativa, Season 02 por capítulos, estado
  estruturado) e **antigravitus** (legado, Season 01 por dias, sem `state.json`).
- Motor: `automato/` na versão **v1.4** (`automato/CHANGELOG.md`), com driver próprio e runtime fora
  do git.
- `python automato/verificar.py` → **18/18 itens OK**.
- `python scripts/check_project.py` → **0 erro(s), 8 aviso(s)** (avisos de legado, metajogo e pendências
  editoriais — são para ler, não para zerar).
- `python -B -m unittest discover -s scripts -p "test_*.py"` → exit 0.
- Versionados: `data/` (117), `automato/` (34), `docs/` (17), `maquina/` (12), `skills/` (3).
  **Não** versionados: `scripts/local/` (legado local) e `.agents/` (coordenação entre agentes).
- Pendências conhecidas da ferramenta: ver §8 de
  [registro_de_evolucao.md](docs/agentes/registro_de_evolucao.md).

## 12. Diretiva do autor — ChatGPT não publica no GitHub (2026-10-16)

> "se for o chatgpt, nunca publique no github"

Para agentes ChatGPT/Codex baseados em modelos OpenAI, manter as alterações e os commits apenas locais. Não executar push, publicação por API/conector do GitHub, criação de PR remoto ou delegação do envio para contornar esta restrição. A autorização genérica anterior para publicar o layout não autoriza publicação por esses agentes após esta diretiva. Somente nova instrução explícita do autor pode revogar a regra.

Registro desta preferência: GPT-6 / Codex (versão específica não informada). A tentativa de envio da reconciliação do Capítulo 5 foi rejeitada pela revisão automática de aprovação e não foi executada; commit 1ecce4dd756e0fff797bea64fc6fd3529c709333 permanece local.


## 13. Diretiva do autor — handoff com limites de cota: janela diária (< 10%) e semanal (< 5%) (2026-10-17 / 2026-10-18)

> "importante, quando o limite de 5h cair abaixo de 10%, faça o handoff" (2026-10-17)  
> "Adiciona monitorar o weekly limit do modelo tbm, se tiver abaixo de 5%, faz o mesmo que faz hoje quando o diário está acabando" (2026-10-18)

A guarda de cota (`automato/camadas/guarda_cota.py` e `scripts/checar_cota.py`) monitora em tempo real a cota do modelo ativo via language server local:
- **Janela diária / 5 horas (reset <= 24h):** ao atingir **<= 10%** restantes, interromper a exploração e acionar o handoff.
- **Weekly limit / janela semanal (reset > 24h):** ao atingir **<= 5%** restantes, interromper a exploração e acionar o handoff.

Em ambos os casos de corte, conduzir a personagem imediatamente a um local seguro (Templo de Midgaard), alimentar com pão, hidratar com cantil, salvar (`save`), colocar em repouso (`sleep`), fechar a conexão do driver e gerar o próximo plano numerado de handoff com local e estado reais, evidências, confirmação do encerramento e tempo restante para reset da janela.

**Passo a passo:** [PROTOCOLO.md §3](docs/agentes/PROTOCOLO.md) e `python scripts/encerrar.py`. O
`checar_cota.py` só lê a cota do Antigravity. Em outro harness (Claude Code, Codex…), use o indicador
de uso do próprio harness com os mesmos cortes.

## 14. Catraca — o padrão só muda para melhor (2026-10-19)

Vários modelos trabalham aqui. Para o padrão ser o mesmo para todos e **não regredir**:

1. **Regra nova só vale com verificação.** Ela entra com (a) um check num script (`mandabala.py`,
   `devolutiva.py`, `auditar_sessao.py`, `encerrar.py` ou `check_project.py`), (b) um teste em
   `scripts/test_*.py` e (c) o ID dela em [`docs/agentes/catraca.json`](docs/agentes/catraca.json).
   Prosa sem verificação é sugestão.
2. **Ninguém remove verificação sozinho.** O `scripts/test_catraca.py` reprova a suíte se um ID da
   catraca sumir do script. Afrouxar exige a aprovação do autor, citada em `automato/DECISOES.md`, e a
   edição da catraca no mesmo commit.
3. **Cada sessão deixa um boletim.** O `encerrar.py --fechar` grava uma linha em
   `docs/agentes/boletim.jsonl` com o modelo, as falhas e avisos e o avanço declarado. É assim que
   se compara modelo com dado. Quando um modelo faz algo melhor, isso vira check e passa a valer para
   todos.
4. **Uma ferramenta por função.** Antes de criar um script em `automato/`, procure na tabela
   "Ferramentas" do [`automato/README.md`](automato/README.md#ferramentas--uma-por-função). O
   `check_project.py` avisa quando surge script fora da tabela.

