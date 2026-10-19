# Plano 029 — Capítulo 12: investigar a biblioteca de Jareth após reset de cota

| | |
|---|---|
| **Criado em** | 2026-10-19 · Dia 157 |
| **Por** | GPT-6 / Codex (versão específica não informada) |
| **Herói** | grebolius |
| **Objetivo** | Concluir Ajuda Mágica no Capítulo 12, encontrando o tomo de Lemin por investigação autônoma. Xeque-mate permanece opcional. |
| **Sessão encerrada?** | sim — nenhuma nova conexão nesta retomada; último encerramento confirmado no Templo com save, sleep e driver fechado, conforme dia157-cap12.json. |

## 1. Onde o objetivo está

Ajuda Mágica ativa na primeira entrega; falta um tomo de pergaminho bem grosso, podendo ser usado. Capítulo 12 continua em curso. O autor reiterou: **fazer as buscas e ler a documentação por conta própria, sem pedir a ele a solução**. A pergunta anterior sobre localização deixa de ser dependência da execução.

Nova pista documental: `help autoquest`, preservado em `evidence/dia156j.json`, lista **Arrumando a Biblioteca: Assistente de Bibliotecária (Jareth)**. Isso confirma a referência de uma biblioteca no catálogo do servidor; NÃO confirma que o tomo de Lemin esteja lá. A topologia de Jareth já está parcialmente descrita em conhecimento §18. Investigar a biblioteca é mais fundamentado que percorrer salas aleatórias ou atacar NPCs por espólios.

## 2. Estado exato

Último estado ao vivo confirmado, sem mudança de jogo nesta retomada: Templo de Midgaard, dormindo; HP 199/199, mana 430/430, MV 145/145. Nível 32, EXP 7.225.102, alinhamento 412; 9 mortes, 1 DT. Ouro 16.059 (15.700 banco, 359 mão); 3 pães na mochila; cantil reabastecido e utilizado no encerramento; peso 74/115 kg; wimpy 45. CA 165 com armor +36 (2 horas restantes) e invisibility +40 (9 horas) no último score. Revalidar buffs fora do Templo antes da próxima expedição.

## 3. O que já foi descoberto

Lemin fica no Centro da Cidade de Lyon, região Notre Dame. A resposta Merlin passou no teste; monólogos e confirmações foram completados. `score tudo` terminou com `Ajuda Mágica: Você deve entregar objeto ao personagem.` Nenhum give ou gasto foi feito.

O Plano 028 guarda o percurso até Lyon e as tentativas já feitas; lê-lo inteiro. Pesquisa posterior em `observacoes/pesquisa-tomo-2026-10-19.md` distingue oito candidatos do mundo original, sem equivalência comprovada no DeBo. Não transformar um livro do original em fonte confirmada do tomo.

## 4. Os bloqueios, e o que já foi tentado

- **Corte de cota agora:** 7% restantes na janela de 5h, abaixo do limite de 10%; semanal 85%, acima do corte de 5%. Reset diário previsto **19/10/2026 às 15:13:17, São Paulo**; restavam **3h20min22s** na consulta. Evidência: `evidence/cota-cap12-20261019.json`.
- Não abrir jogo antes de recuperar cota suficiente; reconsultar ao retomar.
- Tomo não encontrado nas lojas verificadas de Lyon/Midgaard, na doação atual, no laboratório, sala de leitura ou partes visitadas do castelo. Não concluir ausência em áreas inteiras não percorridas.
- `locate object` indisponível ao nível 32; help informa nível 34 e espelho localizador. Não substituir a missão por grind sem avaliar custo e necessidade.
- Rotinas xadrez_v2/v3 NÃO servem como atalho seguro nesta retomada: código lido ainda permite peões brancos e `get all corpo` antes da triagem. Não executadas nem alteradas. Isso conflita com postura heroica e identificação prévia dos itens; evitar seu uso até correção autorizada no contexto necessário.

## 5. O próximo passo, e só ele

**Depois do reset e da conferência de cota, localizar e investigar a biblioteca de Jareth**, usando mapa e conhecimento §18 para trânsito por salas-marco. Ler descrições, procurar livro/tomo e verificar catálogos antes de comprar. Não aceitar uma missão concorrente por simples resposta sim nem entregar item sem reconfirmar pedido, inventory e etapa exata com Lemin. Não pedir ao autor a localização: investigar autonomamente.

## 6. NÃO REPITA

Não procurar Lemin em Midgaard ou no altar. Não recolher/entregar livro por tentativa. Não atacar bibliotecários, moradores, animais ou outros inocentes para descobrir loot. Não coletar amaldiçoados. Não automatizar falas de missão em lote. Não usar quit. Não fechar capítulo sem concluir Ajuda Mágica. Não publicar no GitHub. Não reabrir sessão só para repetir save já confirmado quando não houve nova conexão.

## 7. Ferramentas e comandos

Python e driver: caminhos do Plano 028. `mandabala.py` mostra este plano. Antes de conexão: verificar cota via ferramenta do app, estado do driver e automato/verificar.py. Durante a sessão, um comando por decisão sob ameaça e vigia a cada ~60s. A cota Gemini do language server não substitui a cota real Codex.

## 8. Devolutiva técnica

| Descobri | Registrei em | O quê |
|---|---|---|
| mapa | nada | Nenhuma nova caminhada; mapa do Dia 157 preservado. |
| referência do servidor | nada | Nenhuma nova resposta do DeBo; catálogo anterior consultado documentalmente. |
| fato do mundo | `conhecimento.md` §62 | Pista documental da biblioteca de Jareth, sem afirmar localização do tomo. |
| erro do motor | PENDENTE | v2/v3 do xadrez lidas, não executadas: coleta antes de triagem e possibilidade de peões brancos. |

## 9. Como encerrar a sua sessão

Se jogar: Templo, comida, água, save e sleep confirmados, fechar driver sem quit, evidência com autoria, atualizar os artefatos e criar Plano 030. Se apenas pesquisar, distinguir pesquisa de observação ao vivo. Respeitar cota diária <=10% e semanal <=5%; não marcar o objetivo concluído por encerrar sessão.
