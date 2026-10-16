# Arquitetura — como a lógica deste projeto funciona

> Documento de leitura obrigatória antes de editar ou jogar. Ele descreve **estrutura e contratos**.
> Regras de conduta estão em [boas_praticas.md](boas_praticas.md); nomes de arquivo, em
> [glossario.md](glossario.md); e o que consultar onde, em [onde_consultar.md](onde_consultar.md).

---

## 1. Três planos, ligados por arquivos

O projeto não tem banco de dados nem serviço: **tudo se liga por arquivo em disco**. Isso é decisão de
arquitetura, não acaso — qualquer agente (ou processo) pode entrar, ler o estado e sair sem coordenar
nada em memória.

```text
┌──────────────────────────────────────────────────────────────────────────┐
│ APRESENTAÇÃO   index.html · ficha.html · mapa.html · sobre.html          │
│                js/main.js · css/ · audio/                                │
│                Só LÊ data/**/*.json no navegador. Não escreve conteúdo.   │
└───────────────────────────────▲──────────────────────────────────────────┘
                                │ fetch de JSON estático
┌───────────────────────────────┴──────────────────────────────────────────┐
│ CAMPANHA       data/heroes.json · data/heroes/<id>/**                    │
│                A memória: crônicas, estado, missões, mapa, evidência.     │
│                Escrita à mão só COM FONTE; derivados só por gerador.      │
└───────────────────────────────▲──────────────────────────────────────────┘
                                │ evidência e atualização documental
┌───────────────────────────────┴──────────────────────────────────────────┐
│ MOTOR          automato/  (jogar)   scripts/ (documentar, expedir)        │
│                skills/    (método)  maquina/ (referência do MUD)          │
└──────────────────────────────────────────────────────────────────────────┘
```

| Plano | Entrada típica | Nunca faz |
| --- | --- | --- |
| Apresentação | `python -m http.server 8000` → `index.html?hero=<id>` | criar fato, calcular estado, gravar arquivo |
| Campanha | edição de `data/heroes/<id>/…` com fonte | editar derivado à mão, inventar acontecimento |
| Motor | `automato/camadas/turno.py`, `scripts/expedition_runner.py` | publicar, alterar crônica, decidir lore |

---

## 2. Laço de sessão (ao vivo, no MUD)

O motor está organizado em **camadas com uma responsabilidade cada**. Misturar as camadas foi o que, no
passado, fez a rotina parar no meio do mato e voltar à padaria por fome com seis pães na mochila.

```text
turno.py  ── o encarregado: vigia → cuidar → (prepara, se o cuidar pedir) → rotina → vigia/min
   │
   ├── vigia.py      OBSERVA   lê o log do driver e o _STATUS (IPC). Nunca manda comando ao MUD.
   ├── cuidar.py     CUIDA     em campo: come, bebe, veste. Nunca vai à cidade.
   ├── prepara.py    RECARREGA a ida à cidade: padaria, fonte, banco, sono. Decide por ESTOQUE.
   └── trabalhar.py  DESPACHA  --rotina X carrega rotinas/X.py e chama executar()
```

Três decisões estruturais por trás disso:

1. **O vigia não pergunta ao jogo, ele lê o log.** Mandar `score` enquanto a rotina roda desincroniza a
   sessão (custo já pago: rodadas perdidas achando que a rota estava errada).
2. **Fome pede comida; a cidade entra quando a comida acaba.** `cuidar` resolve em campo; `prepara` só
   é chamado quando o **estoque** cai abaixo do limiar (`LIMIAR_PAO = 2` em `config.py`).
3. **Toda rotina parte do Templo e volta para lá, terminando com `save`.** É isso que a torna
   reiniciável: qualquer interrupção é recuperável pelo `prepara.py`.

### Contrato de uma rotina

```python
NOME = 'minha-rotina'
DESCRICAO = 'o que ela faz, em uma linha'

def executar() -> bool:
    run('wake'); run('stand')        # o jogo recusa andar "relaxado"
    if not ir_ao_lugar():            # trajeto verificado por MARCO de sala
        return False
    ...                              # laço de trabalho
    voltar_ao_templo(); run('save')
    return True
```

1. parte do Templo e volta para lá; 2. confere a sala por **marco**, não por contagem de passos;
3. nunca luta abaixo de `VIDA_MINIMA`; 4. termina com `save`; 5. pode ser interrompida a qualquer
momento — `prepara.py` conserta o resto.

### Cadeia de processos

```text
live_daemon.py  ── sessão única com debomud.org:4000, escuta 127.0.0.1:14888
   ▲ token obrigatório em automato/runtime/.controller
   │
play.py / base.py (run)  ── cliente IPC: "<token>\n<comando>"
   │
guarda.py  ── mesma resposta 3× seguidas (assinatura de PROBLEMA) → recall + save → saída 9
```

`_PING`, `_STATUS`, `_RESYNC`, `_CLOSE`, `_RAW <cmd>` são os verbos internos do driver. `_STATUS` é o
que o vigia usa para saber o estado sem tocar no jogo.

---

## 3. Laço documental (offline, no repositório)

```text
1. OBSERVAR      sessão real → nota em data/heroes/<id>/observacoes/  e/ou evidência JSON
2. EVIDENCIAR    data/heroes/<id>/evidence/<dia>.json   (agent, day, source_kind, note, document)
3. ESTADO        state.json  = último estado REGISTRADO, com day/verification/source/uncertainties
4. NARRAR        posts.json (dia)  ou  capitulos.json (capítulo)   ← só fato registrado
5. MAPEAR        mapa.json (curado) com risco e saídas; mapa_vivo.json é levantamento derivado
6. REGISTRAR     missoes.json, events.json, conhecimento.md, identidade/evolucao
7. DERIVAR       python scripts/sync_hero.py --hero <id>   → ficha.md, hero.json, data/heroes.json
8. VALIDAR       python scripts/sync_hero.py --hero <id> --check
                 python scripts/check_project.py
                 python -B -m unittest discover -s scripts -p "test_*.py"
9. PUBLICAR      python publish_daily.py [--publish] [--push]   (revisão única, só com ordem)
```

**Regra de ouro do plano documental:** *estado registrado não é conexão ao vivo.* `state.json` diz o que
foi registrado e com que natureza de verificação — não que o MUD está sendo observado agora.

### O que é derivado (e por isso nunca se edita à mão)

| Derivado | Gerado por | Fonte |
| --- | --- | --- |
| `data/heroes/<id>/ficha.md` | `scripts/sync_hero.py` | `state.json` + `missoes.json` |
| `data/heroes/<id>/hero.json` (cartões) | `scripts/sync_hero.py` | `hero.json` base + estado |
| `data/heroes.json` (catálogo) | `scripts/sync_hero.py` | todos os heróis |
| `data/heroes/<id>/mapa_vivo.json` | `automato/acoes/digerir_mapa.py` (+ `fundir_mapa.py`) | `transcript_*.jsonl` |
| `relatorio_auditoria_grebolius.html` | `scripts/run_offline_tests.py` | suítes de teste |
| `automato/runtime/*` | driver e rotinas | sessão ao vivo (fora do git) |

Se você editar um derivado, a próxima execução do gerador apaga sua edição — e `check_project.py`
provavelmente acusa a inconsistência antes disso.

---

## 4. Modelo editorial: dia, ciclo, temporada, capítulo

```text
Season 01 (modelo "dias")        Season 02+ (modelo "capítulos")
─────────────────────────        ─────────────────────────────────
posts.json   = 1 entrada/dia     capitulos.json = tomos + capítulos
ciclos.json  = blocos de 10      capítulo tem goal, parts[], content, status
unidade de publicação: DIA       unidade de publicação: CAPÍTULO
```

- **Capítulo não fecha quando se dorme** — fecha quando o `goal` é resolvido (`status: concluido`).
  Fechar cedo é ato final, não pausa; fechar antes dos alvos já fez o sistema devolver o capítulo para
  `em_curso`.
- **Tomo** agrupa 10 capítulos; o Tomo I cobre os capítulos 0 a 10, começando pelo Prólogo (capítulo 0).
- **`parts`** são as partes salvas a cada sessão/dia; o `content` final é a crônica do capítulo.
- Ferramentas: `add_chapter.py` (abre/salva partes/fecha), `temporadas.json` (catálogo),
  `capitulos.json` (dados). Método em [../season_capitulos.md](../season_capitulos.md).

---

## 5. Contratos de dados (JSON)

Todo JSON de campanha carrega `schema_version` e um bloco de origem. Os campos que um agente precisa
saber ler:

| Campo | Onde | Significado |
| --- | --- | --- |
| `as_of.day` / `as_of.verification` / `as_of.source` | `state.json` | **quando**, **como** (live/documental) e **de onde** veio o último estado |
| `verification.mode`, `autoquest_check_day` | `missoes.json` | natureza da conferência e dia dela |
| `source_kind` | `events.json`, referências de crônica | `live` = sessão observada; `documental` = reconstrução |
| `evidence_policy.legacy_through_day` | `hero.json` | até que dia o legado é aceito **sem** evidência estruturada |
| `record_status` | `hero.json` | `draft` = rascunho criado por `create_hero.py`, sem observação real |
| `risk_code` | `mapa.json` | classe de risco da sala; alimenta `RISCO_A_EVITAR` |
| `status` | `missoes.json`, `capitulos.json` | estado do item (ver glossário) |
| `layers[].id` | `mapa.json` | camada do mundo (superfície, novatos, esgotos…) |

**Piso de honestidade:** `legacy_through_day` existe para **fixar o alcance do legado**, não para ser
avançado e contornar a validação. Grebolius 60, Antigravitus 50, heróis novos zero.

---

## 6. Contratos de execução

### Códigos de saída das camadas

| Código | Onde | Significado |
| --- | --- | --- |
| `0` | `cuidar.py`, `prepara.py`, rotinas | resolvido / reposto / sucesso |
| `1` | `cuidar.py`, `prepara.py` | não resolveu sozinho / falhou |
| `2` | `cuidar.py` | precisa **recarregar** → o turno chama o `prepara` |
| `9` | `guarda.py` dentro de `run()` | guarda de repetição disparou: `recall` + `save` + saída |

### Diagnósticos do vigia

`OK · FOME · SEDE · VIDA_BAIXA · MANA_BAIXA · MORTA · TRAVADO · SEM_SESSAO`

O vigia sozinho é só um retrato do agora. **Quem pergunta em laço, a cada 60 s, é o `turno.py`.**

### Exit codes do publicador

`0` = simulação validada ou revisão publicada; `1` = bloqueado por inconsistência documental, índice
sujo, ou erro de git.

---

## 7. Legado e alcance da verificação

O repositório mantém dois heróis em estágios diferentes. Entender a diferença evita "corrigir" o que é
documental por natureza:

| | Grebolius | Antigravitus |
| --- | --- | --- |
| Season | 02 (capítulos) | 01 (dias) |
| `state.json` | sim, atualizado ao vivo | ausente (legado) |
| Legado aceito até | Dia 60 | Dia 50 |
| Campanha | ativa | preservada, sem novas sessões |

O que **não** é certificação, em nenhum dos casos: crônicas legadas, bravata da personagem, `help`
consultado, manual importado, aviso histórico de metajogo. Coerência emocional e fidelidade literária
exigem leitura humana — nenhum validador automático substitui isso.

---

## 8. Fronteiras de escrita (quem pode escrever o quê)

| Alvo | Pode escrever | Restrição |
| --- | --- | --- |
| `data/heroes/<id>/state.json`, `missoes.json`, `mapa.json`, `events.json` | agente | com fonte; campos tipados |
| `posts.json`, `capitulos.json` | `add_day.py`, `add_chapter.py` | substitição exige `--replace` explícito |
| `ficha.md`, `hero.json`, `data/heroes.json` | **só** `sync_hero.py` | derivados |
| `mapa_vivo.json` | `digerir_mapa.py` / `fundir_mapa.py` | derivado do corpus de transcripts |
| `automato/nucleo/config.py` | agente | **ponto único** de configuração do motor |
| `.gitignore`, `publish_daily.py` | humano | decisão de política |
| `automato/runtime/**` | driver | segredos/logs, fora do git |
| `data/heroes/<id>/diretiva_de_jogo.md` | autor (via agente) | é a autoridade sobre como jogar |

---

## 9. Onde a lógica pode falhar (e o que o projeto já aprendeu)

Estas são as falhas estruturais que moldaram a arquitetura atual. Cada uma tem registro em
`automato/README.md` (§ lições de campo) e/ou `automato/DECISOES.md`:

| Falha estrutural | Consequência | Defesa embutida |
| --- | --- | --- |
| Robô insistindo em estado travado | 3 das 7 mortes | `guarda.py` (3 repetições → `recall` + `save`) |
| Vigia perguntando ao jogo | sessão dessincronizada | vigia lê o log (leitura pura) |
| Fome tratada como gatilho de viagem | rotina parando no mato | `cuidar` em campo; `prepara` por estoque |
| Ouro no bolso | morte levava o ouro | `deposit` no Templo com reserva de 300 |
| Rota por contagem de passos | laços no labirinto | navegação por **marco de sala** |
| Identidade de sala pelo texto | 202 salas de texto idêntico | identidade por **posição no grafo** |
| Manual tratado como teste | afirmação sem prova | graus de confirmação (`maquina/README.md`) |
| Corrida entre editar e executar | "ensaio" usou o código anterior | editar, conferir e só então executar |

---

## 10. Documentos que descrevem esta arquitetura

| Assunto | Fonte canônica |
| --- | --- |
| Camadas e contrato das rotinas | [`automato/README.md`](../../automato/README.md) |
| Versão do motor | [`automato/CHANGELOG.md`](../../automato/CHANGELOG.md) |
| Decisões e custos | [`automato/DECISOES.md`](../../automato/DECISOES.md) |
| Rotinas e camadas (visão documental) | [`../rotinas.md`](../rotinas.md) |
| Modelo de temporadas e capítulos | [`../season_capitulos.md`](../season_capitulos.md) |
| Expedição modular V2 | [`../expedicao_modular.md`](../expedicao_modular.md) |
| Fluxo de uma sessão autorizada | [`../../skills/mud-ciclo-diario/SKILL.md`](../../skills/mud-ciclo-diario/SKILL.md) |
