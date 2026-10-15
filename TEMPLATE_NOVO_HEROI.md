# Criar uma nova campanha sem inventar seu histórico

## 1. Concepção proposta

Estes campos definem uma proposta de personagem. Não são prova de eventos ou mecânicas no servidor.

- Nome, título, runa e aparência: a definir pelo autor.
- Raça e estilo narrativo: a definir; registrar a classe mecânica separadamente quando observada no MUD.
- Objetivo: o que deseja alcançar?
- Temor: o que teme perder?
- Falha: que traço pode levá-la a uma decisão ruim?
- Limite: o que aceita sacrificar e o que deseja preservar?
- Legado: como gostaria de ser lembrada?
- Tom: que espaço haverá para ação, curiosidade, humor, dúvida e relações?

Um mentor, rival, trauma, abrigo ou aliança só entra no histórico se foi estabelecido pelo autor como premissa ou ocorreu na sessão. Marcar a origem claramente. Não presumir que NPCs e regras de outro herói valem para este.

## 2. Gerar o rascunho

```bash
python create_hero.py boris --name "Boris Barba-de-Ferro" --race "Guerreiro Anão" --rune "🛡️" --avatar "🧔"
```

O comando cria `data/heroes/boris/` e sua entrada em `data/heroes.json` com `record_status: draft`. O rascunho tem ficha sem valores não observados, mapa sem salas e listas vazias de crônicas, eventos, resumos e missões. Não cria um Dia 1 fictício. Não sobrescreve personagens existentes.

```text
data/heroes/<id>/
├── hero.json          apresentação e cartões; sincronizado com o catálogo
├── identidade.md     concepção e matriz de decisão
├── evolucao.md       evolução apoiada no que aconteceu
├── conhecimento.md   fatos, hipóteses e dúvidas
├── mapa.md           explicação de rotas e incertezas
├── mapa.json         salas e saídas documentadas
├── ficha.md          rascunho; depois será derivada do estado
├── missoes.md        guia de leitura das missões
├── missoes.json      oficiais, investigações e objetivos pessoais
├── events.json       fatos selecionados com fonte
├── ciclos.json       resumos de blocos já concluídos
└── posts.json        crônicas reais
```

## 3. Primeira observação

Registre dentro de `observacoes/` uma nota factual, sem senhas ou credenciais. Observe nível, classe, vitais, recursos, equipamento, habilidades, localização e condições. Não complete lacunas por analogia.

Crie `state.json` seguindo a estrutura da Grebolius, preenchendo **cada valor com a evidência deste novo herói**. O contrato inclui `schema_version`, `hero_id`, `as_of` (dia, fonte, verificação e `live_verified`), `vitals`, nível, classe mecânica, ouro, XP, armadura, wimpy, treinos, habilidades, equipamento, inventário, localização, acampamento e santuário. Os campos editoriais adicionais exigidos pelo gerador também devem representar este herói. Se ainda faltar observação suficiente, conserve o rascunho em vez de copiar números e passado de outra pessoa.

O inventário separa `recorded` de `pending_verification`. `verification: documental` e `live_verified: false` identificam reconciliação com documentos; `verification: live` identifica sessão conferida. A confirmação se refere ao instantâneo registrado, sem prometer que ainda seja atual.

## 4. Registrar o dia real

Prepare o texto da crônica em UTF-8 e uma lista JSON de fontes. Exemplo de estrutura a preencher após a sessão:

```json
[
  {"document": "observacoes/sessao-1.md", "day": 1, "note": "O que esta nota realmente comprova."}
]
```

```bash
python add_day.py --hero boris --day 1 --title "TÍTULO REAL" --date "DATA REAL" --time "REFERÊNCIA REAL NO JOGO" --content-file "cronica.txt" --evidence-file "fontes.json" --source-kind live
python scripts/sync_hero.py --hero boris
python scripts/check_project.py
```

O caminho da fonte é relativo à pasta do herói e precisa existir. A crônica relata a sessão; intenções futuras são identificadas como intenções. O registro do primeiro dia encerra `record_status: draft`, e a ficha precisa satisfazer as checagens normais. Uma alteração deliberada em dia existente exige `--replace`, preservando os fatos.

## 5. Continuidade e leitura

Antes da sessão seguinte, escolha um objetivo verificável, uma pendência e critérios de preparação/retirada. Depois, registre a diferença efetivamente produzida: pista, caminho, recurso, relação ou decisão. Não fabrique três cenas para cumprir um formato.

Cada resumo em `ciclos.json` contém `cycle`, `start_day`, `end_day`, `title` e `summary`. Só entra após os dez dias correspondentes estarem documentados. Não antecipe vitórias ou movimentos no resumo seguinte.

Mapeie apenas saídas documentadas. Uma saída não implica automaticamente retorno, e local de repouso não comprova proteção. Diferencie onde está, onde acampou e qual santuário usa como referência.

## 6. Publicação

Consulte o [README](README.md) para validação e publicação opcional. `python publish_daily.py` apenas simula; `--publish` cria um commit local após validar, e `--push` explícito envia ao destino já configurado. Não publique o rascunho como uma aventura que já aconteceu.
