# Season 02 — modelo de Temporadas, Tomos e Capítulos

> Regra central: **a unidade de publicação da Season 02 é o capítulo, não o dia.**
> Capítulos podem durar quantos dias forem necessários. Dormir não fecha capítulo; o capítulo fecha quando o **objetivo dele** é resolvido.

## Conceitos
- **Temporada (season):** agrupa a obra de um herói. A Season 01 é jogada/registrada por **dias** (`posts.json` + `ciclos.json`). A Season 02 em diante é por **capítulos**.
- **Tomo:** volume que agrupa **10 capítulos**. O Tomo I cobre os capítulos **0 a 10** (11 capítulos, começando no prólogo).
- **Capítulo:** unidade narrativa e de objetivo. Tem um `goal` (a meta), `parts` (as partes salvas a cada sessão/dia) e um `content` final (a crônica do capítulo). Fecha por objetivo cumprido (`status: concluido`), nunca por noite de sono.

## Arquivos
- `data/heroes/<id>/temporadas.json` — catálogo de temporadas e ferramenta de seleção.
- `data/heroes/<id>/capitulos.json` — tomos e capítulos da Season 02.
- Season 01 continua em `posts.json` e `ciclos.json` (intocados), exposta no site como **S01 — Legacy** (`id: s01-legacy`).
- `data/heroes/<id>/capitulos_s01.json` — a Season 01 **recontada** em um tomo de 10 capítulos (`id: s01`, `rewrite_of: s01-legacy`). Mesmo formato do `capitulos.json`; cada capítulo cobre um arco de dias e as `parts` trazem o resumo de cada dia, com `posts.json` como fonte. Não traz fato novo: é reescrita editorial do legado.
- O mesmo vale para outros heróis: o Antigravitus tem os seus 50 dias recontados em um tomo de 7 capítulos (`data/heroes/antigravitus/capitulos_s01.json`), com `temporadas.json` próprio. O número de capítulos segue os arcos da história, não uma conta fixa.

### Season reescrita em tomo
- Toda temporada com `model: "capitulos"` no `temporadas.json` tem a sua fonte validada pelo `check_project.py` com as mesmas regras do `capitulos.json`, e o campo `season` do arquivo precisa casar com o `id` da temporada.
- `rewrite_of` aponta para a versão original preservada; no site, as partes aparecem como "Resumo dos dias".
- Link antigo de dia (`?season=s01&day=N`) cai na versão Legacy, que tem o mesmo número de temporada.

## `temporadas.json`
```json
{
  "schema_version": 1,
  "hero_id": "grebolius",
  "current": "s02",
  "seasons": [
    { "id": "s01", "number": 1, "title": "Season 01", "subtitle": "...",
      "model": "dias", "unit": "Dia", "source": "posts.json", "cycles": "ciclos.json",
      "range": [1, 100], "cover": "..." },
    { "id": "s02", "number": 2, "title": "Season 02", "subtitle": "...",
      "model": "capitulos", "unit": "Capítulo", "source": "capitulos.json",
      "started_day": 101 }
  ]
}
```

## `capitulos.json`
```json
{
  "schema_version": 1,
  "hero_id": "grebolius",
  "season": "s02",
  "tomos": [
    { "id": "tomo-1", "number": 1, "roman": "I", "title": "Tomo I",
      "chapter_start": 0, "chapter_end": 10, "subtitle": "..." }
  ],
  "chapters": [
    {
      "id": 0, "tomo": 1, "title": "Prólogo", "kind": "prologo",
      "status": "concluido", "goal": "...", "closed_on_day": 100,
      "days": [1, 100], "date": "2026-10-15", "in_game_time": "...",
      "excerpt": "...", "tags": ["..."],
      "content": ["parágrafo 1", "parágrafo 2"],
      "source_kind": "documental",
      "evidence": [{ "document": "posts.json", "day": 100, "note": "..." }],
      "parts": [
        { "day": 1, "date": "2026-10-14", "summary": "...", "source_kind": "live",
          "evidence": [{ "document": "posts.json", "day": 1, "note": "..." }] }
      ]
    }
  ]
}
```

### Campos do capítulo
| Campo | Regra |
| --- | --- |
| `id` | inteiro ≥ 0, único. 0 é sempre o prólogo do Tomo I. |
| `tomo` | inteiro; precisa casar com `chapter_start`/`chapter_end` do tomo. |
| `kind` | `prologo`, `missao`, `intervalo`, `reflexao` ou `marco`. |
| `status` | `aberto` (criado), `em_curso` (partes sendo salvas) ou `concluido` (fechado pelo objetivo). |
| `goal` | a meta que decide o fechamento. Obrigatório. |
| `days` | dias de jogo cobertos (lista). Nunca é o critério de fechamento. |
| `parts` | partes salvas dia a dia, com fonte. |
| `content` | crônica final do capítulo. Obrigatória somente quando `concluido`. |
| `source_kind` | `documental` ou `live`. |
| `evidence` | fontes; caminhos relativos à pasta do herói. |

## Fluxo de trabalho (substitui o ciclo diário na Season 02)
1. **Abrir** o capítulo com título e objetivo: `add_chapter.py --chapter N --tomo 1 --title ... --goal ...`.
2. A cada sessão/dia, **salvar uma parte**: `add_chapter.py --chapter N --part --day D --summary ... --evidence-file ...`.
3. Quando o objetivo é cumprido, **fechar** o capítulo com a crônica: `add_chapter.py --chapter N --close --content-file ... --source-kind live --evidence-file ...`.
4. **Publicar o capítulo** fechado. Partes podem ser salvas sem publicar.
5. O site mostra o capítulo fechado na íntegra; capítulos abertos aparecem como "em produção" (somente título e objetivo).

## O que muda na mecânica (não no jogo)
- O sono e o `save` continuam encerrando a **sessão**; não encerram o **capítulo**.
- O antes "dia" vira "parte do capítulo"; a contagem de dias continua existindo internamente para evidência.
- A publicação (`publish_daily.py`) passa a poder publicar um capítulo inteiro, mesmo que ele atravesse vários dias.
