# As Crônicas de Midgaard

Diário de roleplay e compêndio de múltiplos personagens em Devil's Bob MUD (`debomud.org:4000`). O site é estático; cada herói mantém seus próprios documentos em `data/heroes/<id>/`.

## Temporadas e capítulos

A obra de cada herói é dividida em **temporadas**. A **Season 01** é narrada por **dias** (`posts.json` + `ciclos.json`) e está encerrada no Dia 100. A partir da **Season 02** a narrativa passa a ser por **capítulos**: cada capítulo tem um objetivo verificável, pode durar quantos dias forem necessários e **não fecha quando se dorme** — fecha quando a meta é cumprida. Capítulos são agrupados de dez em dez em **tomos**; o Tomo I cobre os capítulos 0 a 10, começando pelo Prólogo (capítulo 0).

Ferramentas: `data/heroes/<id>/temporadas.json` (catálogo), `data/heroes/<id>/capitulos.json` (tomos e capítulos) e [add_chapter.py](add_chapter.py). O método está em [docs/season_capitulos.md](docs/season_capitulos.md) e na skill [mud-capitulo](skills/mud-capitulo/SKILL.md). O sono e o `save` encerram a **sessão**; a publicação é do **capítulo**.

## Fonte e alcance da revisão

A Grebolius foi reconciliada documentalmente até o **Dia 60**, a partir dos registros existentes. Esta revisão não jogou, não verificou conta ou mecânicas ao vivo e não criou acontecimentos para as crônicas. Os posts históricos foram preservados. Dúvidas de continuidade estão registradas como dúvidas, sem inventar deslocamentos, recompensas, diálogos ou efeitos da morte.

`state.json` é o último estado **registrado**, com dia, fonte, natureza da verificação e incertezas. Ele não representa uma conexão em tempo real ao MUD. O mapa também identifica a revisão documental: atualizar a consolidação não prova que todas as saídas ou riscos foram novamente testados em jogo.

## Arquivos de cada campanha

| Arquivo | Responsabilidade |
| --- | --- |
| `hero.json` | Apresentação, voz, identidade resumida e cartões gerados. Metadados completos devem concordar com `data/heroes.json`. |
| `state.json` | Nível, classe mecânica, vitais, recursos, habilidades, equipamento, inventário e localização, com origem explícita. Implementado para Grebolius; legado ainda pode não ter esse arquivo. |
| `ficha.md` | Para heróis com estado estruturado, deriva de `state.json` e `missoes.json`; não editar seus números isoladamente. |
| `missoes.json` | Missões oficiais, investigações e intenções pessoais, com status, evidência e próximo passo. |
| `missoes.md` | Guia editorial de leitura das missões e pendências. |
| `events.json` | Fatos documentais selecionados e referências; não é uma transcrição bruta nem prova automática de toda a narrativa. |
| `posts.json` | Crônicas do que ocorreu. Novas entradas precisam de conteúdo real e evidência. |
| `ciclos.json` | Resumos de blocos de dez dias já encerrados; planos futuros pertencem ao plano de aventura. |
| `identidade.md` / `evolucao.md` | Motivações, contradições da personagem e evolução apoiada nos acontecimentos. |
| `conhecimento.md` | Saber acumulado, separando observação, interpretação e dúvida. |
| `mapa.json` / `mapa.md` | Salas e saídas documentadas, riscos e limites de confirmação. |
| `plano_aventureira.md` | Próximas decisões possíveis, sempre como intenções, sem desfechos garantidos. |

## Rotina de uma sessão

1. Ler a [orientação local](skills/mud-ciclo-diario/SKILL.md), a identidade e as pendências do herói. Escolher um objetivo verificável e preparar recursos e retirada conforme o risco observado.
2. Registrar o que o MUD realmente informou em uma nota curta dentro de `data/heroes/<id>/observacoes/`. Não guardar senha, token ou transcrição contendo credenciais. A nota pode resumir observações; não precisa inventar um log bruto inexistente.
3. Atualizar estado, missões, eventos e conhecimento com a origem de cada mudança. Um item visto no passado, cuja posse atual é incerta, fica em `inventory.pending_verification`.
4. Escrever a crônica a partir dos fatos registrados. Ambição e bravata são voz da personagem; não comprovam invulnerabilidade ou mecânicas. Alternar ação, descoberta, relação e reflexão conforme a sessão efetiva, sem fabricar cenas para preencher uma quota.
5. Atualizar mapa quando houver descoberta ou correção. A cada dez dias, consolidar somente o bloco realmente encerrado.
6. Sincronizar os derivados e validar o conjunto antes de publicar.

```bash
python scripts/sync_hero.py --hero grebolius
python scripts/sync_hero.py --hero grebolius --check
python scripts/check_project.py
python -B -m unittest discover -s scripts -p "test_*.py"
```

O sincronizador atualiza a ficha, os cartões locais e a entrada completa no catálogo. A validação confere tipos, vitais, wimpy, estado, metadados, referências, missões, salas e saídas, totais, datas de consolidação e limites dos ciclos. Ela acusa campos que não conseguiu interpretar. `hero.json.evidence_policy.legacy_through_day` fixa o alcance do legado sem evidência estruturada: Dia 60 para Grebolius, Dia 50 para Antigravitus e zero para novos heróis. Dias posteriores exigem fonte mesmo quando o JSON é editado manualmente. Não avance esse limite para contornar a validação. Avisos históricos de metajogo não reescrevem crônicas e não transformam documentação antiga em verificação ao vivo. Coerência emocional e fidelidade literária continuam precisando de leitura humana.

## Registrar uma nova crônica

Escreva a crônica em um arquivo UTF-8 com parágrafos separados por linhas em branco. Prepare um JSON de referências, por exemplo:

```json
[
  {
    "document": "observacoes/sessao-61.md",
    "day": 61,
    "note": "Observações realmente registradas na sessão; conferir antes de narrar."
  }
]
```

O caminho `document` é relativo à pasta do herói e precisa existir. O exemplo é um formato de preenchimento, não comprovação de que a sessão 61 aconteceu. `source_kind=live` identifica uma sessão observada; `documental` identifica uma reconstrução apoiada em documentos existentes. Nenhum deles dispensa a fonte.

```bash
python add_day.py --hero grebolius --day 61 --title "TÍTULO REAL" --date "DATA DA SESSÃO" --time "REFERÊNCIA NO JOGO" --content-file "cronica.txt" --evidence-file "fontes.json" --source-kind live --tags "Jornada"
```

Não use o comando antes de a sessão acontecer. Substituir um dia ou resumo existente exige `--replace` explícito; leia a evidência e preserve os fatos. A CLI não injeta parágrafo genérico nem usa uma data fixa. O mesmo cuidado vale para a função `add_chronicle`, que também exige origem, evidência e `replace=True` quando aplicável.

Para um bloco já encerrado:

```bash
python add_day.py --hero grebolius --cycle 6 --title "TÍTULO REVISADO" --cycle-summary "RESUMO APOIADO NOS DIAS 51 A 60" --replace
```

## Criar um novo herói

```bash
python create_hero.py boris --name "Boris Barba-de-Ferro" --race "Guerreiro Anão" --rune "🛡️" --avatar "🧔"
```

O comando cria um **rascunho explícito** (`record_status: draft`), com crônicas, eventos, ciclos e missões vazios, mapa sem salas e ficha sem números presumidos. Não cria um despertar fictício. Após a primeira observação real, preencha `state.json` segundo o contrato da Grebolius, com os dados desse novo herói; sincronize e valide. A primeira crônica registrada pelo utilitário encerra o estado de rascunho, exigindo que a ficha passe pelas checagens normais. Veja [o guia de criação](TEMPLATE_NOVO_HEROI.md).

## Ler localmente

Sirva a pasta com um servidor HTTP, pois o site carrega JSONs:

```bash
python -m http.server 8000
```

Abra `http://localhost:8000/index.html?hero=grebolius`. O seletor de heróis também funciona em ficha, perfil e mapa.

## Publicação opcional

```bash
python publish_daily.py
python publish_daily.py --publish --message "Revisa registros documentais da campanha"
python publish_daily.py --publish --push --message "Revisa registros documentais da campanha"
```

O primeiro comando **simula** após validar. `--publish` cria um único commit local da revisão; `--push` explícito envia pelo destino Git já configurado. O publicador não cria repositórios, não envia um arquivo por commit e não altera identidade ou credenciais globais. Alterações já preparadas no índice Git bloqueiam uma nova publicação para preservar a revisão do usuário. O `.gitignore` e uma lista de caminhos permitidos excluem sessões, logs, arquivos locais e credenciais.

Repositório: [javaijafoi/antigravitus](https://github.com/javaijafoi/antigravitus). Se o repositório estiver conectado à Vercel, o envio pode acionar o deploy configurado. Esta revisão local não executou publicação ou deploy.

## Referências da máquina

[Guia prático e manuais](maquina/README.md): comandos úteis, diferenças do DeBo, tips, informações, magias e história do mundo. A base orienta a operação sem atribuir conhecimento ou acontecimentos à personagem.

## Orientação para agentes

Se quem está operando este repositório é um agente (e não uma pessoa), o ponto de entrada é
[AGENTS.md](AGENTS.md). Ele traz a regra de identificação (modelo/versão em relatório, evidência e
commit), os invariantes de segurança, os checklists de início e encerramento e o mapa de onde consultar
cada coisa.

O detalhamento fica em [docs/agentes/](docs/agentes/): [arquitetura](docs/agentes/arquitetura.md),
[boas práticas](docs/agentes/boas_praticas.md), [glossário de cada artefato](docs/agentes/glossario.md),
[onde consultar](docs/agentes/onde_consultar.md) e o
[registro de evolução](docs/agentes/registro_de_evolucao.md) — o livro-razão onde cada agente documenta
o que mudou na ferramenta, por quê, com que verificação e a que custo.
