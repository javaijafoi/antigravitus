# Plano012 — continuar Uma Lição em Gargamel

| | |
|---|---|
| **Criado em** | 2026-10-17 · Dia156 |
| **Por** | GPT-6 / Codex (versão específica não informada) |
| **Herói** | grebolius |
| **Objetivo** | Concluir Uma Lição em Gargamel com confirmação do servidor |
| **Sessão encerrada?** | conexão fechada:True;save:True;sono:True |

Este plano não se edita. Próximo plano013. Ler AGENTS§12–13 e LEIA.md.

## 1. Onde o objetivo está
Gargamel ativa;Limpando entregue sem quit,manto e94.227EXP. Nenhum resgate confirmado.

## 2. Estado exato
Fonte:evidence/dia156j.json,consulta2026-10-17T10:17:27-03:00,linha1130. Local:O Templo de Midgaard (templo_midgaard). Nível28;HP{'current': 178, 'max': 178};mana{'current': 340, 'max': 340};MV{'current': 141, 'max': 141};EXP4000001,meta4500000;ouro4229mão+0banco;treinos68;pães5;armor+34/10h. Inventário completo em state/evidência. Limpando Monstros concluída sem quit: sete abates, manto de pano e 94.227 EXP de entrega; nível 28. Minerador completou a fala final e Alquimista pediu poção aquosa de Clariss: Gargamel está na etapa de entregar objeto. Nenhum jarro ou resgate confirmado, nenhuma nova morte. A rota gravada pelo norte/Jareth chegou à fazenda; nenhuma nova caça no milharal foi confirmada. Compra de cinco pães por 30 moedas; final no Templo com 178/178 HP, 340/340 mana, 141/141 MV, 4.229 moedas, cinco pães, save e sono confirmados, socket e daemon encerrados.

## 3. O que foi descoberto
Ver conhecimento§43 e evidência156j. Poço Smurf separado dos esgotos;12 correções de saídas,511 salas. Concluir diálogo antes de entrega;prompt pode acompanhar resposta antiga.

## 4. Bloqueios e tentativas
Hipótese de conflito do§42 não isolada;Limpando concluída semreset. Minerador aguardava item;falas soltas não provam resgate. Rota011 ao milharal falhou na muralha/ponte. Motivo da parada:Medidor da janela de 300 minutos caiu para 8% restantes; retirada e handoff conforme pedido do autor..

## 5. O próximo passo, e só ele
Conferir o estado real e completar o saldo para a poção aquosa de Clariss (9.750; faltam 5.521 moedas), sem quit/reset: o Alquimista já pediu a poção e score marcou entregar objeto. Usar a rota pelo norte/Jareth comprovada no transcript156j, nunca a rota curta do plano011. Rever os guardas da caça antes de automatizar; o worker temporário teve falso alarme e não comprovou rendimento. Com peso 109/115 kg, conferir capacidade. Ao ter a poção, entregar somente com objetivo vigente e aguardar o jarro no diálogo completo. Não abrir outra conexão automaticamente em falha.

## 6. NÃO REPITA
Não resetar/comprar/entregar por hipótese;aguardar diálogo/objetivo. Não seguir rota011cegamente. Não inferir proteção de DT pelo brinco ou substring Milharal. Não confundir histórico de morte com morte atual;worker fora da aplicação pode gerar falso alarme. Não iniciar segunda conexão se esta ainda estiver aberta. Não publicar GitHub.

## 7. Ferramentas e comandos
mandabala.py lê este plano;sync_hero.py gera derivados. Ler AGENTS§13:medidor antes de risco/a cada~5min,retirada e handoff ao atingir10%restante da janela300min. Helpers locais não são reparo do motor.

## 8. Devolutiva técnica
| Descobri | Registrei em | O quê |
|---|---|---|
| mapa | `mapa.json` |12 correções com precondições e novo Poço Smurf;511 salas |
| referência do servidor | `maquina/verificacoes.md` | Respostas intercaladas,prompt e histórico de morte |
| fato do mundo | `conhecimento.md` §43 | Limpando semquit,Gargamel ativa,revisão§42 e rota |
| erro do motor | `automato/DECISOES.md` | Sintoma documentado e contenção externa;driver sem alteração |

## 9. Como encerrar
Save,verificar,repousar e fechar na mesma conexão quando possível. Criar plano013. Rodar sync_hero e--check,check_project,verificar e devolutiva;resolver falhas e ler avisos. Preservar arquivos prévios;sem publicação GitHub.
