# Onde consultar — mapa das fontes do projeto

> Este documento responde uma pergunta só: **"para decidir/escrever isto, qual arquivo eu leio?"**
> Ele não substitui as fontes; ele aponta para elas. Nomes e definições de cada artefato estão em
> [glossario.md](glossario.md); contratos internos, em [arquitetura.md](arquitetura.md).

---

## 1. Ordem de precedência

Quando duas fontes discordarem, esta é a ordem — e a divergência **se registra**, não se resolve em
silêncio:

| # | Fonte | Vale porque |
| --- | --- | --- |
| 1 | **Resposta real do servidor nesta sessão**, com comando, alvo e resposta registrados | é o único dado executado |
| 2 | **Observação registrada com data** (`evidence/`, `observacoes/`) | é o que foi visto, ainda que em outra data |
| 3 | **Ajuda do DeBo** (`maquina/dicionario_comandos.md`, `maquina/verificacoes.md`) | é documentação do servidor |
| 4 | **Engine CircleMUD** (`docs/circlemud/`) | é o motor de origem — provável, não confirmado para o DeBo |
| 5 | **Manual/anexo importado** (`maquina/commands.md`, `info.md`, `spells.md`, `historia_mundo.md`) | é referência histórica |

Regra prática: **nível 1 vence; níveis 3–5 nunca viram "testado"**. Ao corrigir um nível 3–5, preserve o
texto importado e acrescente a correção datada.

E, acima de tudo: **diretiva do autor > qualquer fonte técnica.** As diretivas vigentes estão em
`data/heroes/<id>/diretiva_de_jogo.md` e no relatório de cada sessão.

---

## 2. Decisão rápida: "preciso de X"

| Preciso de… | Leia |
| --- | --- |
| Começar do zero neste repositório | [`../../AGENTS.md`](../../AGENTS.md) |
| Entender a estrutura e os fluxos | [arquitetura.md](arquitetura.md) |
| Saber o que é boa prática aqui | [boas_praticas.md](boas_praticas.md) |
| Saber o que é um arquivo/termo | [glossario.md](glossario.md) |
| Registrar o que evoluí | [registro_de_evolucao.md](registro_de_evolucao.md) |
| Jogar uma sessão autorizada | [`skills/mud-ciclo-diario/SKILL.md`](../../skills/mud-ciclo-diario/SKILL.md) |
| Conduzir/abrir/fechar um capítulo | [`skills/mud-capitulo/SKILL.md`](../../skills/mud-capitulo/SKILL.md), [`docs/season_capitulos.md`](../season_capitulos.md) |
| Operar o motor, rodar uma rotina | [`automato/README.md`](../../automato/README.md), [`docs/rotinas.md`](../rotinas.md) |
| Saber o que já custou caro (não repetir) | [`automato/DECISOES.md`](../../automato/DECISOES.md), [`automato/README.md`](../../automato/README.md) § lições de campo |
| Versão atual do motor | [`automato/CHANGELOG.md`](../../automato/CHANGELOG.md) |
| Ajustar caminhos, limites, magias do motor | [`automato/nucleo/config.py`](../../automato/nucleo/config.py) (ponto único) |
| Confirmar que o ambiente está no lugar | `python automato/verificar.py` |
| Escolher um verbo/comando no jogo | [`maquina/dicionario_comandos.md`](../../maquina/dicionario_comandos.md), [`maquina/commands.md`](../../maquina/commands.md) |
| Saber onde o DeBo difere do CircleMUD | [`maquina/comparacao_commands.md`](../../maquina/comparacao_commands.md) |
| Números de magias, combate, mobs, zonas | [`docs/circlemud/`](../circlemud/) (entrar por [`00-afirmacoes-e-validacao.md`](../circlemud/00-afirmacoes-e-validacao.md)) |
| Corrigir uma referência técnica do servidor | [`maquina/verificacoes.md`](../../maquina/verificacoes.md) **+** o resumo em `maquina/dicionario_comandos.md` |
| Regras de jogo vigentes do herói | `data/heroes/<id>/diretiva_de_jogo.md` |
| Estado mecânico do herói | `data/heroes/<id>/state.json` (e `ficha.md` para leitura) |
| Missões e pendências | `data/heroes/<id>/missoes.json` e `missoes.md` |
| Plano do capítulo em curso | `data/heroes/<id>/plano_capitulo_0N.md` |
| Rotas, economia, ameaças conhecidas | `data/heroes/<id>/conhecimento.md` |
| Grafo de salas e riscos | `data/heroes/<id>/mapa.json`; levantamento derivado em `mapa_vivo.json` |
| Quem vende o quê, por quanto | `data/heroes/<id>/itens.md` |
| NPCs / monstros | `data/heroes/<id>/npcs.md`, `monstros.md` |
| Separar decisão do autor de fato do servidor | `data/heroes/<id>/notas_editoriais.md` |
| Rodar a expedição modular (V2) | [`docs/expedicao_modular.md`](../expedicao_modular.md), [`skills/mud-expedicao-modular/SKILL.md`](../../skills/mud-expedicao-modular/SKILL.md), `scripts/expedition_runner.py` |
| Comandos do executor modular | [`docs/expedicao_comandos.md`](../expedicao_comandos.md) |
| Criar um herói novo | [`../../TEMPLATE_NOVO_HEROI.md`](../../TEMPLATE_NOVO_HEROI.md), `create_hero.py` |
| Entender os testes offline | [`../../TEST_READY.md`](../../TEST_READY.md), `scripts/run_offline_tests.py` |
| Gerar áudio-livro | `scripts/tts/narrate.py --list-heroes` |

---

## 3. Inventário das pastas de consulta

### `docs/` — método e pesquisa

| Documento | Papel |
| --- | --- |
| [`agentes/`](.) | este conjunto (guia, arquitetura, práticas, glossário, consulta, registro) |
| [`rotinas.md`](../rotinas.md) | proposta e catálogo das rotinas e camadas |
| [`season_capitulos.md`](../season_capitulos.md) | modelo de temporadas, tomos e capítulos |
| [`expedicao_modular.md`](../expedicao_modular.md) | motor de expedição modular V2 |
| [`expedicao_comandos.md`](../expedicao_comandos.md) | recorte de comandos para o executor |
| [`expedicao_esgotos_dia95.md`](../expedicao_esgotos_dia95.md) | aplicação do motor aos esgotos |
| [`expedicao_grebolius.json`](../expedicao_grebolius.json) | configuração de expedição do herói |
| [`expedicao_legado.json`](../expedicao_legado.json) | manifesto do modo Dungeon V1 preservado |
| [`circlemud/`](../circlemud/) | pesquisa sobre o motor CircleMUD 3.x, em 10 volumes, com níveis de confiança |

**Como ler `docs/circlemud/`:** comece por
[`00-afirmacoes-e-validacao.md`](../circlemud/00-afirmacoes-e-validacao.md) — ele explica os níveis
(certo / provável / dúvida) e o protocolo de validação. Nenhum volume substitui uma sessão autorizada.

### `maquina/` — referência técnica do MUD

Camada do operador: comandos, magias, comparação com o CircleMUD, história do mundo, verificações e
dicas. **Conhecer isto não concede habilidade, lembrança ou descoberta à personagem.** Índice e graus de
confirmação: [`maquina/README.md`](../../maquina/README.md).

### `skills/` — procedimento operacional

`mud-ciclo-diario/`, `mud-capitulo/`, `mud-expedicao-modular/`. Cada skill descreve **como conduzir**
uma modalidade; ela **não autoriza** jogar, conectar ou publicar. Pedido de edição de arquivo não é
autorização para sessão ao vivo.

### `automato/` — o motor

Documentação (`README.md`, `CHANGELOG.md`, `DECISOES.md`), autoexame (`verificar.py`), núcleo
(`nucleo/`), camadas (`camadas/`), rotinas (`rotinas/`), ações pontuais (`acoes/`) e runtime com
segredos e logs (`runtime/`, fora do git).

### `data/heroes/<id>/` — a campanha

A memória do herói. Antes de qualquer sessão, os três arquivos que mudam a decisão são
`diretiva_de_jogo.md` (como jogar), `missoes.json` (o que está pendente) e `mapa.json` (por onde ir).

### `.agents/` — coordenação entre agentes (não versionado)

Histórico de trabalho de sessões anteriores: pedido original, incumbências (`DISPATCH.md`), contexto
(`BRIEFING.md`), progresso e entregas (`handoff.md`). Útil para reconstruir **por que** uma decisão foi
tomada quando ela não chegou aos documentos versionados. Não é fonte de verdade: se discordar dos
arquivos versionados, vale o arquivo versionado.

### `scripts/local/` — legado local (não versionado)

Histórico de execução: `play_dia*.py`, `session_dia*.txt`, `transcript_*.jsonl`, o driver antigo e a
suíte de mocks. `automato/acoes/digerir_mapa.py` ainda lê transcripts daqui. **Não construa em cima
disso**: o motor canônico é `automato/`.

---

## 4. Regras de uso das fontes

1. **Separe as camadas.** Conhecimento de `maquina/` e `docs/circlemud/` orienta a interação; não vira
   cena, habilidade ou lembrança. Fato da personagem exige aquisição comprovada no jogo.
2. **Não promova.** Manual não é comando; `help` consultado não é execução; listado não é usável.
3. **Preserve o importado.** Ao corrigir, mantenha o texto original e acrescente a correção datada com
   contexto, resposta e fonte — em `maquina/verificacoes.md` e no resumo do dicionário.
4. **Uma pergunta, uma fonte principal.** Se precisar de duas, cite ambas e diga qual prevaleceu.
5. **Referencie, não copie.** Duplicar número ou rota entre arquivos cria duas verdades; a próxima
   validação vai discordar de uma delas.
6. **Registre a lacuna.** Se a fonte não existe (nenhuma tip capturada, nenhuma evidência do dia),
   escreva que não existe. Lacuna declarada é dado; lacuna preenchida por suposição é erro.
7. **Anexo e dica não autorizam ação.** Material de referência não é permissão para executar comandos
   nem para contatar jogadores.
