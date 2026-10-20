# Plano 036 — Capítulo 12: reaceitar Ajuda Mágica com Lemin e testar o livro de Jooh

| | |
|---|---|
| **Criado em** | 2026-10-19 · Dia 157 |
| **Por** | Claude Opus 5.5 (claude-opus-5-5) |
| **Herói** | grebolius |
| **Objetivo** | Capítulo 12: reconstruir o livro de Merlin |
| **Sessão encerrada?** | sim — Templo de Midgaard, dormindo; última conexão fechada às 22:23 com `recall` + `_CLOSE sleep` (save e sleep confirmados); driver fechado; sem quit. |

Este plano **substitui o 035** (Claude Haiku 5.5), que não é editado. Não houve jogo novo além de fechar
a conexão deixada aberta. O 035 tinha três problemas que este corrige: (1) o §5 mandava perguntar ao
autor a palavra de abertura, e a cadeia de diálogo está no `conhecimento.md` §61/§64; (2) dizia "não há
pão", mas a mochila nunca foi aberta; (3) a parada do `navegar.py` era erro do **mapa**, já corrigido.
O `state.json` e o `missoes.json` foram atualizados com o que o 035 viu.

## 1. Onde o objetivo está

Capítulo 12, objetivo: concluir Ajuda Mágica. A missão está **inativa no servidor** (segunda vez no Dia
157; causa desconhecida) e precisa ser **reaceita** com Lemin. A cadeia já funcionou duas vezes. Depois
de reaceita, falta o tomo: "um tomo de pergaminho bem grosso, que pode ser usado". O livro de Jooh
está no inventário como teste mais barato. Nada foi entregue até agora.

## 2. Estado exato
- **Local:** O Templo de Midgaard (`templo_midgaard`)
- **Vida/mana/MV:** 199/199 · 430/430 · 145/145
- **Nível:** 32 · EXP 7.225.093 (próximo nível em 8.000.000)
- **Alinhamento:** 393 (Bom) · wimpy 45
- **Ouro:** 15.920
- **CA:** base 89 / com magias 165
- Save e sono confirmados no Templo; conexão fechada sem quit.
- Sem fome nem sede às 22:14 (cantil bebido no Templo); pães na mochila não reconferidos.
- 9 mortes e 1 DT históricas; um combate não iniciado por ela (rato preto em Lyon) com queda de alinhamento 412 -> 393.
- Ouro: 15.700 banco + 220 mão = 15.920 (gastos: rolo de pergaminho 103, seis pães 36). Peso 69/115 kg.
- Ajuda Mágica INATIVA no servidor no login de 22:07 do Dia 157: score tudo sem [Autoquests em andamento]; autoquest listar a mostra como disponível, iniciada com Lemin. Causa desconhecida (segunda vez no dia; a primeira está no conhecimento §64). Nenhum give executado.
- CA 125 no score tudo de 22:13, só com armor +36 (23 horas); invisibility ausente.
- **Inventário:** cantil, o livro "Equipamentos para Primeira Encarnação", de Jooh, rolo de pergaminho (NOTA, não é o tomo), rosário, pergaminho de sabedoria ("A Lenda de Nambor", não serve), mochila de Pellinore (registrados dentro: 3 pães — **não reconferidos**, `look in mochila` —, manto de pano, colar púrpura, bainha de Excalibur, Cruz Ansada, Cetro do Bispo Negro).
- **Fonte:** `state.json` (as_of dia 157, verificação live). Confira com `score tudo` ao conectar.

## 3. O que já foi descoberto

- **Lemin:** no Centro da Cidade de Lyon (`cap12_026`). Rota por script, verificada contra o transcript real:
  `navegar.py --de templo_midgaard --para cap12_026` (23 passos: `d s w w w w w w w w w n n w n w n n e s s s s`).
- **Cadeia de (re)aceitação (conhecimento §61, §64):** olhar Lemin (`look lemin`) aciona o convite →
  aceitar → ouvir a pergunta inteira sobre o mago autor da mochila → responder **Merlin** só depois do
  fim da fala → ouvir o relato → responder às confirmações, conferindo `score tudo` entre cada uma → até
  aparecer `Ajuda Mágica: Você deve entregar objeto ao personagem.` `ask lemin ajuda` **não** funciona.
- **Confirmar se está inativa:** `autoquest listar` mostra "Ajuda Mágica … iniciada com: Lemin" entre as
  disponíveis quando ela caiu.
- **Sala de Doações e Templo bloqueiam magia:** para `identify`, vá à Praça do Templo (`d` a partir do Templo).
- **Já descartados para o tomo:** lojas de Lyon, Midgaard e Jareth; Pergaminhos e Afins (só um rolo,
  que é NOTA); Biblioteca da cidade de Jareth (Caminho de Tábuas, sem tomo); biblioteca do Lorde; Paris;
  alas da catedral; A Pequena Capela; casas de Lyon; Sala de Doações (salvo o livro de Jooh).
- **Pistas abertas, da mais barata para a mais cara:** (a) livro de Jooh, já no inventário; (b) carruagem
  de Lyon para o centro de Paris (85 moedas); (c) O Campanário da Catedral (entrada não achada; `where`
  mostra o corcunda lá); (d) QG trancado dos Mosqueteiros; (e) Torre da Magia (`help mapa 29`).
- **Consulta rápida ao repositório:** `python scripts/mandabala.py --sobre <nome>`.

## 4. Os bloqueios, e o que já foi tentado

- **Missão inativa:** visto no login de 22:07 (`score tudo` sem a seção; `autoquest listar` com ela
  disponível). Tentado só `ask lemin ajuda` (sem resposta) e `look rapaz`. A cadeia da §61 **não** foi tentada.
- **Fonte do tomo:** ver a lista de descartados no §3. O livro de Jooh é um guia de equipamentos e pode
  não ser o que Lemin pede.
- **Por que a missão cai:** desconhecido. Não é o `_CLOSE` (§65). Aconteceu depois de sessões fechadas
  com save e sleep, sem quit e sem morte. Registre se acontecer de novo, com o horário.

## 5. O próximo passo, e só ele

**Ir a Lemin pelo script e reaceitar Ajuda Mágica pela cadeia da §61, à mão.** Conectar, `score tudo`
(conferir o §2), `python automato/camadas/navegar.py --de templo_midgaard --para cap12_026`. No
Centro da Cidade, `look lemin` e seguir a cadeia do §3 uma resposta por vez, lendo a fala inteira
antes de responder (AGENTS #14). Com `Você deve entregar objeto ao personagem` no `score tudo`, o
`give livro lemin` é permitido, à mão e sem outra fala antes (AGENTS #13).
- Se Lemin recusar o livro, ou o identify (na Praça do Templo) mostrar outra coisa, o padrão é a pista
  (b): carruagem de Lyon para o centro de Paris (85 moedas) e procurar livreiro ou biblioteca lá.
- Se a cadeia não abrir a missão, registre a fala inteira na evidência e siga para a pista (b) sem dar
  give: o tomo continua sendo preciso, e a reaceitação pode ser tentada de novo na volta.

## 6. NÃO REPITA

- Não usar `ask lemin ajuda` nem responder com palavras chutadas. A cadeia é a do §3.
- Não concluir "não há pão" sem `look in mochila`.
- Não usar `identify` na Sala de Doações nem no Templo: lá a magia falha.
- Não entrar no Túnel Escuro de Lyon (o rato ataca sozinho; matá-lo custou 412 → 393 de alinhamento).
- Não procurar o tomo de novo nos lugares descartados do §3.
- **Não reconectar depois do handoff** sem fazer outro handoff. A última conexão ficou parada em Lyon e
  teve de ser fechada por fora. O `devolutiva.py` reprova isso (`sessao.aberta`).
- Não usar `quit`; não editar planos antigos; não dar give sem a etapa no `score tudo`.

## 7. Ferramentas e comandos

Python: `C:\Users\peter\AppData\Local\Programs\Python\Python312\python.exe` (o `python` do PATH cai no
atalho da Microsoft Store). Driver: `$env:MUD_DAY='157'; $env:MUD_WIMPY='45'; python
automato\nucleo\driver\live_daemon.py` em segundo plano. Comando: `python automato\nucleo\driver\play.py
"<cmd>"`. Fechar: `play.py "recall"` e depois `play.py "_CLOSE sleep"`. Navegar:
`automato\camadas\navegar.py --de <id> --para <id> [--seco]` (aceita o título do jogo, os `aliases` e o
nome sem o sufixo de curadoria). Consulta: `scripts\mandabala.py --sobre <nome>`. Fim de sessão:
`scripts\encerrar.py --agente "<modelo/versão>"`, preencher o plano e rodar de novo com
`--fechar --avanco sim|nao`. Auditor: `scripts\auditar_sessao.py`.

## 8. Devolutiva técnica

| Descobri | Registrei em | O quê |
|---|---|---|
| mapa | `mapa.json` | Nova sala `fora_portao_oeste`; aresta falsa `ponte_rio`→`cap12_001` removida; `aliases` "Rua Principal" e "Dentro do Portão Oeste de Midgaard" (do plano 035) |
| referência do servidor | `maquina/verificacoes.md` | `autoquest listar` mostra a missão perdida; Sala de Doações bloqueia magia; `ask` sem eco de NPC; títulos do Portão Oeste |
| fato do mundo | `conhecimento.md` §67 | missão inativa outra vez; livro de Jooh; pães na mochila; trecho do Portão Oeste; conexão deixada aberta |
| erro do motor | `automato/CHANGELOG.md` | nada: a parada do `navegar.py` era do mapa (v1.7.3 já cobre `sessao.aberta` e `state.desatualizado`) |

## 9. Como encerrar a sua sessão

Siga `docs/agentes/PROTOCOLO.md` §3: Templo (`recall`), comer e beber, `_CLOSE sleep`, evidência com
`agent`, `state.json`/`missoes.json`/`mapa.json`/`conhecimento.md` atualizados,
`python scripts/encerrar.py --agente "<modelo/versão>"`, preencher o plano 037, e
`python scripts/encerrar.py --agente "<modelo/versão>" --fechar --avanco sim|nao`. **Depois disso, não reconecte.**
