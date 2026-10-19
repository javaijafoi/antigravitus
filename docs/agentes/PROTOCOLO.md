# PROTOCOLO — a sessão inteira em comandos

> **Se só for ler uma coisa, leia esta.** Vale para **qualquer modelo**. Cada passo é um comando ou
> uma pergunta com resposta sim/não. O porquê de cada regra está no link — aqui só está **o que
> fazer, em que ordem**. Onde este roteiro e outro doc divergirem, vale a regra de origem citada; e
> corrija este arquivo.

## 1. Abertura (antes de qualquer ação)

| # | Faça | Pronto quando |
|---|---|---|
| 1 | `python scripts/mandabala.py` | leu o plano vigente **inteiro** e a "SEQUÊNCIA DE ABERTURA" que ele imprime |
| 2 | `git status --porcelain` e `git log --oneline -5` | sabe se há trabalho de outro agente na árvore ([AGENTS §10](../../AGENTS.md#10-trabalho-concorrente-leia-antes-de-editar)) |
| 3 | Leia `data/heroes/<id>/diretiva_de_jogo.md` **§19 a §23** | as regras de `give`, fala de missão, etapa, ética e o ritual de bloco |
| 4 | Cota: `python scripts/checar_cota.py` (Antigravity) ou o indicador do seu harness | diária > 10% **e** semanal > 5% ([AGENTS §13](../../AGENTS.md)). Abaixo disso: vá direto ao §3 |
| 5 | Se vai jogar: driver no ar e `python automato/verificar.py` sem FALHA | — |
| 6 | Ao conectar: `score tudo` | estado e etapa da autoquest conferidos **contra o §2 do plano**; divergiu → registre antes de agir |
| 7 | **Execute o §5 do plano** ("o próximo passo, e só ele") | é a sua primeira ação. Não reabra a investigação que o plano já fechou |

**Não pergunte ao autor o que o plano já responde.** Pergunte só nos casos de
[AGENTS #13](../../AGENTS.md#4-invariantes-não-quebrar) (`give`/compra cara sem etapa confirmada) e
[#15](../../AGENTS.md#4-invariantes-não-quebrar) (ética), ou quando uma diretiva mandar. Se houver
bloqueio, escolha a opção mais segura que o plano recomenda e siga.

## 2. Cada bloco de jogo (repita as 4 perguntas antes de **cada** envio)

Fonte: [diretiva §23](../../data/heroes/grebolius/diretiva_de_jogo.md).

1. **A rota está no `mapa.json`?** Sim → `python automato/camadas/navegar.py --para <id>`. Não → à mão,
   um passo, `exits`, e depois **grave a rota no `mapa.json`**.
2. **Há NPC ou item de missão?** Fala, `give` e compra são **à mão, linha a linha**, com `score tudo`
   mostrando a sub-etapa exata ([AGENTS #13/#14](../../AGENTS.md#4-invariantes-não-quebrar)).
3. **Alguém está lendo o retorno a cada passo?** Rotina só com `turno.py` ou leitura do log a cada ~60 s.
4. **Se a vida cair?** `recall` ao primeiro golpe grave. Nunca recuar andando.

Sempre: `save`, nunca `quit` · não ataque o que não é ameaça · `identify` antes de `get` · descoberta
vai para o **artefato** (mapa/verificações/conhecimento/CHANGELOG) **na hora**, não só em prosa.

**Antes de criar ferramenta nova:** procure na tabela "Ferramentas" do
[automato/README.md](../../automato/README.md#ferramentas--uma-por-função). Se já existir uma para a
função, melhore a existente.

## 3. Encerramento / handoff (cota no fim, fim do tempo ou objetivo cumprido)

| # | Faça | Pronto quando |
|---|---|---|
| 1 | No jogo: Templo (`recall`), comer pão, beber do cantil, `_CLOSE sleep` (faz stand + save + sleep com confirmação) | o driver devolve `save_confirmed` e `sleep_confirmed`. **Nunca `quit`** |
| 2 | Grave a evidência com `"agent": "<modelo/versão>"` | — |
| 3 | Atualize `state.json`, `missoes.json`, `mapa.json`, `conhecimento.md` com a origem; crônica se houve fato novo | — |
| 4 | `python scripts/encerrar.py --agente "<modelo/versão>"` | ele roda sync/check/auditor/devolutiva e **cria o esqueleto do próximo plano** com o estado do `state.json` |
| 5 | Preencha o esqueleto: §1, §3–§6, §8. Regras do plano v2 ([LEIA.md](../../data/heroes/grebolius/planos/LEIA.md)) | o plano **se sustenta sozinho** e o §5 é **uma ação executável** |
| 6 | `python scripts/encerrar.py --agente "<modelo/versão>" --fechar` | 0 FALHA; o boletim da sessão foi gravado |
| 7 | Bloco no [registro de evolução](registro_de_evolucao.md) se mexeu na ferramenta; commit com caminhos explícitos e `[agente: …]` | **sem push** se não houve pedido ([AGENTS §12](../../AGENTS.md)) |

## 4. Como o padrão muda (só para melhor)

Uma regra nova **só vale** quando entra com: (a) uma verificação num script
(`devolutiva.py`, `auditar_sessao.py`, `mandabala.py` ou `encerrar.py`), (b) um teste em
`scripts/test_*.py`, (c) o ID dela em [`catraca.json`](catraca.json). O teste `test_catraca.py`
reprova quem remover uma verificação. Afrouxar uma regra exige a aprovação do autor citada em
`automato/DECISOES.md`. Prosa sem verificação é sugestão, não padrão.
