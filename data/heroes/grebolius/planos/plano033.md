# Plano 033 — Capítulo 12: tomo de Lemin (fecha as pendências de registro do Plano 032)

| | |
|---|---|
| **Criado em** | 2026-10-19 · Dia 157 |
| **Por** | Claude Sonnet 5.5 (claude-sonnet-5-5) |
| **Herói** | grebolius |
| **Objetivo** | Concluir Ajuda Mágica: achar o tomo na etapa de entrega e entregá-lo a Lemin só com a etapa confirmada. |
| **Sessão encerrada?** | sim — Templo de Midgaard; save e sleep confirmados; driver fechado, sem quit. Nenhuma conexão nova ao jogo desde o Plano 032. |

Este plano **não repete a investigação**: o estado de jogo é o do Plano 032 (não editado, vale na íntegra para o que não for dito aqui). Ele existe porque, depois do 032, rodei o auditor de sessão e achei lacunas de registro que a regra de append-only me impede de corrigir no 032.

## 1. Onde o objetivo está

Igual ao Plano 032: *Ajuda Mágica* ativa em "Você deve entregar objeto ao personagem"; o tomo não foi achado; a biblioteca da cidade de Jareth não foi localizada. Nenhum give. Capítulo 12 em curso. O que mudou aqui é só documental: `state.json` agora aponta para este plano e descreve a segunda parte do dia; `missoes.json` registra o bloqueio e as evidências novas; `capitulos.json` ganhou a segunda parte do Capítulo 12.

## 2. Estado exato

Sem mudança desde o Plano 032: Templo de Midgaard, dormindo; 199/199 de vida, 430/430 de mana, 145/145 de movimento; nível 32; alinhamento 412; ouro 16.059 (359 na mão, 15.700 no banco); 9 mortes e 1 DT. Buffs: armor lançada, invisibility lançada; validade a reconferir.

## 3. O que já foi descoberto

Tudo o do Plano 032. Acrescento a **auditoria mecânica** (`python scripts/auditar_sessao.py automato/runtime/<transcript>.jsonl`, escrito por outra sessão Claude Sonnet 5.5 em paralelo):

| Transcript (conexão) | Resultado | Leitura |
|---|---|---|
| `transcript_dia157_20261019_141906_4cc11d` (1ª minha) | 5 falhas, 2 avisos | Reconhecido abaixo. |
| `transcript_dia157_20261019_144821_52609a` | 0 falhas, 0 avisos | Rota por comandos curtos. |
| `transcript_dia157_20261019_150357_4afc69` | 0 falhas, 0 avisos | Rota por `nav.py`. |

**As 5 falhas de repetição de recusa (diretiva §12)** são reais e minhas. Conferidas no transcript, uma a uma, cada uma com 3 recusas seguidas do mesmo comando dentro de um lote de PowerShell que não parava na primeira: (1) `e` na Estrada Midgaard-Jareth, antes de chegar à curva, porque contei passos de cabeça; (2) `n` na Joalheria, que é beco sem saída ao norte; (3) `s` contra a porta fechada do Saguão no castelo do Lorde ("A porta está fechada"); (4) `s` na Avenida Floris, onde não há saída ao sul, na volta do castelo; (5) `w` no fim da passarela de tábuas. Causa comum: eu contava passos de cabeça em vez de usar marco, e o laço do lote não parava na recusa. Todas foram recusas sem efeito ("Você não pode ir por aí" ou "A porta está fechada"), sem dano. **Correção:** a partir do `nav.py` o lote para na primeira divergência; as duas últimas conexões saíram limpas.

**Os 2 avisos de recuo a pé com 50 de vida** (diretiva §2): no Beco Escuro mandei `n`, `n`, `e` em um único lote ao ver dois malandros, e só ao fim do lote vi a vida em 50. O certo era `recall` no primeiro golpe. Fiz `recall` logo depois. Por isso o Plano 032 já diz "ao primeiro golpe, recall".

**O que o auditor não vê (INFO):** de onde veio o comando (script ou à mão). Declaro: a 1ª conexão foi à mão, e foi o erro; a 2ª e a 3ª usaram comandos curtos e `nav.py`. As falas de missão com Lemin foram todas manuais, uma por vez, depois de ler o log.

## 4. Os bloqueios, e o que já foi tentado

Os do Plano 032 (Beco Escuro sem matar os malandros, porta leste trancada da Vovó, cadeia, castelo do Lorde, Pequena Passagem de Welmar). Nada novo tentado em jogo depois do 032.

## 5. O próximo passo, e só ele

O do Plano 032: `score tudo` na abertura para confirmar a etapa; depois decidir com o autor a porta da Vovó e o Beco antes de qualquer tentativa.

## 6. NÃO REPITA

O do Plano 032, mais: **não mandar lote de passos sem parada na primeira recusa**; **não recuar a pé abaixo de 60% de vida** (`recall`); não editar planos antigos; não usar `quit`.

## 7. Ferramentas e comandos

Os do Plano 032, mais o auditor: `python scripts/auditar_sessao.py automato/runtime/transcript_dia157_<...>.jsonl`. **Duplicidade a resolver:** `automato/rotas/nav.py` (minha) e `automato/camadas/navegar.py` (da outra sessão) fazem papel parecido; manter um só.

## 8. Devolutiva técnica

| Descobri | Registrei em | O quê |
|---|---|---|
| mapa | nada | Sem caminhada nova depois do Plano 032 (o mapa dos 29 salas `jz_` foi gravado antes). |
| referência do servidor | nada | Sem resposta nova do servidor. |
| fato do mundo | `state.json`, `missoes.json`, `capitulos.json` | Missão reativada, sobrevive ao fechamento, tomo não achado, Beco fora; segunda parte do Capítulo 12. |
| erro do motor | PENDENTE | Lote de PowerShell sem parada na recusa (corrigido em `nav.py`, não no `play.py`); duplicidade `nav.py` × `navegar.py`; `sala=None` no `play.py`. |

## 9. Como encerrar a sua sessão

Templo, comer e beber, `sleep` e `save`, `_CLOSE sleep` com `sleep_confirmed=True`, evidência com autoria, plano 034, `auditar_sessao.py` sobre o transcript e `devolutiva.py`.
