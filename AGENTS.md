# AGENTS.md — guia de operação para agentes

> Este é o **primeiro arquivo** que um agente deve ler neste repositório. Ele não conta a história da
> campanha: descreve **como o projeto funciona**, **o que é boa prática aqui**, **onde procurar cada
> coisa** e **onde registrar o que você evoluiu**. A narrativa vive em `data/heroes/<id>/`, não aqui.

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
10. **Diretivas do autor vencem.** Ex.: **proibido vender armaduras** (Torre Negra ou peão); rotina
    `xadrez` suspensa em `automato/rotinas/_suspensas/` — não reativar sem ordem expressa.
11. **Encerrar sessão = `save`.** A publicação é passo separado e explícito.
12. **Editar arquivo e executá-lo não cabem no mesmo bloco de ferramentas** — elas rodam em paralelo;
    edite, confira o arquivo e só então execute, em chamadas separadas.

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
| Evoluiu a **ferramenta** (automato, scripts, camadas, rotinas, config, skills) | bloco novo em [registro_de_evolucao.md](docs/agentes/registro_de_evolucao.md) **+** `automato/CHANGELOG.md` (versão) **+** `automato/DECISOES.md` (se houver decisão e custo) |
| Evoluiu a **campanha** (jogou, descobriu, corrigiu o mundo) | `data/heroes/<id>/` conforme o laço documental, com evidência |
| Corrigiu uma **referência técnica** do MUD | `maquina/verificacoes.md` e o resumo em `maquina/dicionario_comandos.md` |
| Abriu/decidiu algo que o próximo precisa saber | bloco de **handoff** no fim do seu registro |

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

**Antes de começar**

- [ ] Li o `README.md` da raiz e este arquivo.
- [ ] Sei qual herói, qual temporada/capítulo e qual o objetivo verificável.
- [ ] Li `diretiva_de_jogo.md` e as pendências em `missoes.json` / plano do capítulo.
- [ ] Sei onde vou escrever e qual é a fonte da verdade daquele dado.
- [ ] `git status` e `git log -5` conferidos (ver §10).
- [ ] Se vou jogar: driver no ar, `automato/verificar.py` sem FALHA, supervisão combinada.

**Antes de encerrar**

- [ ] Evidência gravada, com `agent` e origem.
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
