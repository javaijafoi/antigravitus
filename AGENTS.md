# AGENTS.md — guia de operação para agentes

> Este é o **primeiro arquivo** que um agente deve ler. Ele não conta a história da campanha:
> diz **como o projeto funciona**, **o que não se quebra** e **onde registrar**. A narrativa vive
> em `data/heroes/<id>/`; o método, em `docs/agentes/`; o detalhe, nos ponteiros da §7.

> ## ▶ Comece aqui — vale para qualquer modelo
>
> 1. `python scripts/mandabala.py` — plano vigente, pré-voo e a **primeira ação**.
> 2. [`docs/agentes/PROTOCOLO.md`](docs/agentes/PROTOCOLO.md) — a sessão inteira em comandos.
> 3. `data/heroes/<id>/diretiva_de_jogo.md` §19–§26 — as regras que custaram caro.
>
> **Encerrar são dois comandos:** `python scripts/encerrar.py --agente "<modelo/versão>"` e
> `python scripts/devolutiva.py`. O `devolutiva.py` já roda `check_project.py`, `verificar.py` e
> — só se algum `.py` mudou — a suíte. **Não rode esses três de novo à parte.**
>
> Se `python` abrir a Microsoft Store, rode **uma vez**
> `powershell -ExecutionPolicy Bypass -File scripts\configurar_python.ps1 -Aplicar` e reabra o terminal.

Índice: [Regra zero](#0-regra-zero--identifique-se) · [Repositório](#1-o-que-é-este-repositório) ·
[Lógica](#2-como-a-lógica-funciona-em-uma-tela) · [Fonte da verdade](#3-fonte-da-verdade--não-duplique) ·
[Invariantes](#4-invariantes-não-quebrar) · [Boas práticas](#5-boas-práticas) ·
[Registro](#6-registrar-o-que-você-evoluiu) · [Onde consultar](#7-onde-consultar) ·
[Glossário](#8-glossário) · [Checklists](#9-checklists) ·
[Trabalho concorrente](#10-trabalho-concorrente-leia-antes-de-editar) ·
[Catraca](#14-catraca--o-padrão-só-muda-para-melhor)

---

## 0. Regra zero — identifique-se

Todo agente que **jogar, editar ou publicar** declara **modelo e versão** em quatro lugares:

1. no **início do relatório** entregue ao autor;
2. no campo `"agent"` da evidência: `{"agent": "<modelo/versao>", "via": "automato"}`;
3. no fim da **mensagem do commit**: `[agente: <modelo/versao>]`;
4. no bloco do [registro de evolução](docs/agentes/registro_de_evolucao.md).

**Motivo:** vários agentes jogam e mexem na mesma ferramenta, às vezes ao mesmo tempo. Sem autoria não
há como comparar desempenho entre modelos — e é o placar que decide qual padrão vira check.

---

## 1. O que é este repositório

Três planos que se comunicam **por arquivos**, nunca por estado em memória compartilhada:

| Plano | Onde | O que é |
| --- | --- | --- |
| **Apresentação** | `index.html`, `ficha.html`, `mapa.html`, `css/`, `js/`, `audio/` | site estático que **lê** `data/`; não escreve conteúdo |
| **Campanha** | `data/` | crônicas, estado, missões, mapa, evidência — só com fonte registrada |
| **Motor** | `automato/` (canônico), `scripts/` (documental), `skills/` (método) | como se joga: driver, camadas, rotinas, validadores |

Detalhe em [arquitetura.md](docs/agentes/arquitetura.md).

---

## 2. Como a lógica funciona, em uma tela

**Ao vivo (MUD):** `localizar/preparar → trânsito por sala-marco → trabalhar (rotina)`, com
`vigia` + `cuidar` + guarda de repetição. Quem orquestra é o `automato/camadas/turno.py`.

**Offline (repositório):** observação real → evidência → `state.json` → crônica/mapa/missões →
derivados por `sync_hero.py` → `check_project.py` → publicação.

**A regra que costura os dois:** nada entra em `data/` sem fonte registrada, e nenhum derivado é
editado à mão. Season 01 publica por **dia**; da Season 02 em diante, por **capítulo**.

**Os cinco modos de jogar estão na diretiva §26.** Declare o modo antes do bloco; se a intenção não
cabe em nenhum, pare e proponha ao autor — não invente um sexto.

---

## 3. Fonte da verdade — não duplique

| Domínio | Canônico | Derivados (nunca editar à mão) |
| --- | --- | --- |
| Estado do herói | `data/heroes/<id>/state.json` | `ficha.md`, `hero.json`, `data/heroes.json` |
| Crônicas | `posts.json` (dias), `capitulos.json` (capítulos) | site, `ciclos.json` |
| Missões | `missoes.json` | `ficha.md`, `missoes.md` |
| Mapa | `mapa.json` | `mapa_grade.json`, `mapa_vivo.json` (`mapa.md` é histórico) |
| Rotas e economia | `conhecimento.md` | — |
| Regras de jogo | `diretiva_de_jogo.md` | rotinas e camadas |
| Configuração do motor | `automato/nucleo/config.py` | — |
| Versão e decisões | `automato/CHANGELOG.md`, `automato/DECISOES.md` | este guia |

Vontade de copiar dado de um arquivo para outro é sinal de que o certo é **referenciar** ou
**regenerar**.

---

## 4. Invariantes (não quebrar)

1. **Fonte antes de afirmação.** Observação, interpretação e dúvida separadas. Manual, `help` e dica
   **não** são teste executado.
2. **Identifique-se** (§0) em relatório, evidência e commit.
3. **Não invente acontecimento.** Sem evidência, é pendência ou dúvida — nunca cena.
4. **Derivados só via `sync_hero.py`.**
5. **Não reescreva o legado.** Crônica antiga preservada; correção entra como nota datada.
6. **Rotina nunca roda sem supervisão.** Job em segundo plano + leitura do log a cada ~60 s.
7. **O vigia lê o log, não o jogo.** `score` no meio da rotina desincroniza a sessão.
8. **`save`, nunca `quit`, com missão em andamento.** `quit` apaga o progresso.
9. **Segredos ficam em `automato/runtime/`** (fora do git). Nunca colar senha, token ou transcrição
   com credencial em documento, log ou commit.
10. **Diretivas do autor vencem.** Proibido pegar ou comercializar itens **amaldiçoados**: dupla
    checagem com `identify` no chão antes do `get` (NODROP impede descarte).
11. **Encerrar sessão = `save`.** Publicação é passo separado e explícito.
12. **Editar arquivo e executá-lo não cabem no mesmo bloco de ferramentas** — edite, confira, depois
    execute, em chamadas separadas.
13. **Estar na etapa certa para fazer a coisa certa.** `give` e compra cara só com a sub-etapa
    confirmada no `score tudo` (`"Você deve entregar objeto"`), inventário conferido e diálogo
    ouvido até o fim. O comando consome o item de forma irreversível.
14. **Falar com NPC em missão NUNCA é automatizado.** `say`/`ask`/`whisper` são resposta direta do
    agente ao contexto, lendo a fala integral e checando objetivo, sala e inventário.
15. **Postura heroica proativa.** Não fazer o mal, não bater em pessoa pacífica nem em animal
    indefeso; se o autor pedir algo que viole isso, **questione antes**. Se o `score` acusar queda de
    alinhamento, pare, audite a causa e banir a reincidência.

---

## 5. Boas práticas

- **Verificar antes de acreditar.** Resposta cortada pela latência não é estado do jogo; `None` não é
  zero; sinal de morte exige a linha inteira.
- **Mapear à mão → testar em trechos curtos → só então automatizar** (diretiva §9).
- **Andar por sala-marco**, com origem na sala onde a personagem **está**.
- **Registrar a divergência quando ela aparece:** `maquina/verificacoes.md` (referência),
  `conhecimento.md` (fato do mundo), `mapa.json` (mapa).
- **Uma mudança, um propósito.** Commit pequeno, com prefixo e trailer de agente.
- **Não publique sem pedido.** Editar arquivo não autoriza `--publish`/`--push`.
- **Mudança no motor entra no `CHANGELOG.md`** e, se tiver custo, no `DECISOES.md`.

---

## 6. Registrar o que você evoluiu

| O que você fez | Onde registra |
| --- | --- |
| Encerrou sessão de jogo | crie o **próximo plano numerado**: `data/heroes/<id>/planos/planoNNN.md` — **nunca edite o anterior** |
| Evoluiu a ferramenta | bloco novo em [registro_de_evolucao.md](docs/agentes/registro_de_evolucao.md) **+** `CHANGELOG.md` (+ `DECISOES.md` se houver custo) |
| Evoluiu a campanha | `data/heroes/<id>/` com evidência |
| Corrigiu referência do MUD | `maquina/verificacoes.md` e o resumo em `maquina/dicionario_comandos.md` |

**Planos são append-only.** Três dígitos, o próximo número, autoria no cabeçalho, e o que não pode
faltar: estado em números, o próximo passo único, bloqueios com o que já foi tentado, e o que não
repetir. Modelo em [`LEIA.md`](data/heroes/grebolius/planos/LEIA.md). Para retomar:
`python scripts/mandabala.py`.

**A devolutiva técnica (§8 do plano) é conferida contra o `git diff`.** Uma descoberta que não virou
artefato não existe para o próximo. `PENDENTE` é resposta honesta; prometer mapa e não mexer no
`mapa.json` é falha. Rode `python scripts/devolutiva.py` e **resolva as FALHAS**.

Formato do bloco no livro-razão (append-only; não edite bloco alheio):

```markdown
### <AAAA-MM-DD> · <dia de jogo ou "—"> · <modelo/versão>
- **Mudou:** <arquivos e o que passou a valer>
- **Por quê:** <problema real observado>
- **Como foi verificado:** <comando/teste/sessão, com resultado>
- **Custo:** <o que se perde, ou "nenhum">
- **Próximo:** <o que continua aberto>
```

---

## 7. Onde consultar

| Preciso de… | Consulte |
| --- | --- |
| Operar o motor / rodar rotina | `automato/README.md`, `docs/rotinas.md` |
| O que já foi tentado e custou caro | `automato/DECISOES.md`, `automato/README.md` |
| Comandos, magias, diferenças do servidor | `maquina/README.md`, `maquina/dicionario_comandos.md` |
| Regras de jogo vigentes | `data/heroes/<id>/diretiva_de_jogo.md` |
| Estado, missões, mapa | `state.json`, `missoes.json`, `mapa.json` |
| Método de sessão / capítulo | `skills/mud-ciclo-diario/`, `skills/mud-capitulo/` |
| Mapa completo e precedência | [onde_consultar.md](docs/agentes/onde_consultar.md) |

**Precedência:** resposta real nesta sessão > observação registrada com data > ajuda do DeBo
(`maquina/`) > engine CircleMUD (`docs/circlemud/`) > manual importado. Quando discordarem,
**registre a divergência** em vez de escolher em silêncio.

---

## 8. Glossário

Cada artefato, cada campo de JSON recorrente (`schema_version`, `as_of`, `verification`, `risk_code`…),
os conceitos do domínio (dia, ciclo, temporada, capítulo, parte, autoquest, sala-marco, wimpy, DT) e
os diagnósticos do vigia: [glossario.md](docs/agentes/glossario.md).

---

## 9. Checklists

A versão executável é o [PROTOCOLO.md](docs/agentes/PROTOCOLO.md). Se divergirem, corrija os dois.

**Antes de começar**

- [ ] `python scripts/mandabala.py` lido **inteiro**, com o plano vigente e o pré-voo.
- [ ] Sei qual herói, qual temporada/capítulo e qual o objetivo verificável.
- [ ] Li a diretiva §19–§26 e as pendências em `missoes.json`.
- [ ] `git status --porcelain` e `git log -5` conferidos (§10).
- [ ] Se vou jogar: driver no ar, `python automato/verificar.py` sem FALHA, supervisão combinada.
- [ ] **Modo declarado** (§26): caminhar, explorar, moer, missão ou chefe — e o dono dele.

**Antes de encerrar**

- [ ] `python scripts/encerrar.py --agente "<modelo/versão>"`.
- [ ] **`python scripts/devolutiva.py` com 0 falhas** (avisos lidos, não silenciados).
      Ele já cobre `check_project`, `verificar` e a suíte — **não repita os três à parte**.
- [ ] Evidência gravada, com `agent` e origem.
- [ ] **Plano seguinte criado**, sem editar o anterior.
- [ ] `state.json`, missões, mapa e conhecimento atualizados com a origem de cada mudança.
- [ ] Bloco no registro de evolução; `CHANGELOG.md` se mexeu no motor.
- [ ] Nada de segredo, sessão, log ou credencial no git.

---

## 10. Trabalho concorrente (leia antes de editar)

Esta árvore é **compartilhada** — já houve commit de outra sessão levando arquivos que estavam só no
disco. Na prática:

- **Confira antes e depois:** `git status --porcelain`, `git log -5`, `git diff --stat`.
- **Nunca `git add -A`, `git add .` nem `git commit -a`.** Prepare caminhos explícitos.
- **Nunca reescreva histórico** (`rebase`, `amend` alheio, `reset --hard`, `push --force`).
- **O publicador varre arquivos não rastreados** (`publish_daily.py` usa `git diff HEAD` + `git ls-files
  --others`): arquivo novo seu pode entrar no commit de outro agente.
- Mudança em `maquina/` ou `docs/*.json` fica **fora** da lista publicável: comite à parte.
- **Não publique por conta própria.**

---

## 12. Diretiva do autor — ChatGPT não publica no GitHub (2026-10-16)

> "se for o chatgpt, nunca publique no github"

Para agentes ChatGPT/Codex, manter alterações e commits **apenas locais**. Sem push, sem conector do
GitHub, sem PR remoto, sem delegar o envio. Só nova instrução explícita do autor revoga.

---

## 13. Diretiva do autor — handoff com limites de cota (2026-10-17 / 2026-10-18)

> "quando o limite de 5h cair abaixo de 10%, faça o handoff" · "monitorar o weekly limit… se tiver
> abaixo de 5%, faz o mesmo"

- **Janela de 5 h:** ao restar **≤ 10%**, parar de explorar e acionar o handoff.
- **Semanal:** ao restar **≤ 5%**, o mesmo.

No corte: levar a personagem ao Templo de Midgaard, comer, beber, `save`, `sleep`, fechar a conexão e
gerar o próximo plano com o estado real. Instrumentos: `automato/camadas/guarda_cota.py` e
`scripts/checar_cota.py` (Antigravity); no Claude Code, `scripts/cota_claude.py` com `get_usage`; em
outro harness, o indicador do próprio harness com os mesmos cortes. Passo a passo no
[PROTOCOLO.md §3](docs/agentes/PROTOCOLO.md).

---

## 14. Catraca — o padrão só muda para melhor

1. **Regra nova só vale com verificação:** check num script + teste em `scripts/test_*.py` + ID em
   [`docs/agentes/catraca.json`](docs/agentes/catraca.json), no mesmo commit. **Prosa sem verificação
   é sugestão** — e sugestão é ignorada.
2. **Ninguém remove verificação sozinho.** `test_catraca.py` reprova se um ID sumir. Afrouxar exige
   aprovação do autor citada em `DECISOES.md`, no mesmo commit.
3. **Cada sessão deixa um boletim.** `encerrar.py --fechar` grava uma linha em
   `docs/agentes/boletim.jsonl` com modelo, falhas, avisos e avanço: é assim que se compara modelo
   com dado.
4. **Uma ferramenta por função.** Antes de criar script em `automato/`, procure na tabela
   "Ferramentas" do [`automato/README.md`](automato/README.md). Script novo entra na tabela no mesmo
   commit; `check_project.py` acusa quando surge um fora dela.
5. **Regra que não vira check, vira default no código — ou sai do arquivo.** Ordem de preferência:
   **default no código > check > prosa**. Seção da diretiva sem nenhuma das duas primeiras é dívida.
