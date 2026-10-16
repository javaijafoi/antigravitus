# Plano 003 — Capítulo 5 concluído; escolher a próxima meta

| | |
|---|---|
| **Criado em** | 2026-10-16 · Dia 156, continuação |
| **Por** | GPT-6 / Codex (versão específica não informada) |
| **Herói** | grebolius |
| **Objetivo** | Escolher com o autor a meta do próximo capítulo antes de iniciar outra missão |
| **Sessão encerrada?** | Sim — save e sleep confirmados no Templo; daemon encerrado |

## 1. Onde o objetivo está

O Capítulo 5 foi concluído: Novela dos Novatos e o novo ciclo de Limpando Monstros tiveram entregas verificadas. Fonte: [evidence/dia156e.json](../evidence/dia156e.json). Nenhuma nova missão foi iniciada. Continuação da conexão identificada como Dia 156; não foi inventado um novo dia/login.

## 2. Estado exato

- Nível 21, Mago Elfo, primeira encarnação; 135/135 HP, 270/270 mana, 131/131 MV.
- EXP 1.200.001; próxima meta 1.400.000. Sete mortes; uma DT histórica, nenhuma nova.
- Ouro: 300 na mão, 1.351 no banco (total 1.651). PA: 0.
- CA 110 com armor (+30, 16 horas no último score); CA sem armor 80 observada antes da reconjuração. Wimpy 45 mantido.
- Brinco de novato na orelha direita: +15 HP, +15 MV, +1 acerto e +1 dano. Acerto 4 / Dano 2. Flag ANTI-DT do item não é prova de imunidade da personagem.
- Armadura da Torre Negra vestida, espada curta empunhada. Manto da recompensa guardado (identificado: armadura +30); manto anterior continua vestido.
- Quatro pães, cantil com água; sem fome ou sede no score final. 15/22 itens, 88/115 kg. Oito punhais guardados na mochila.
- Quarenta treinos; curse recém-aprendida a 10%. Practice final em evidence/dia156e.json.
- Dormindo no Templo de Midgaard; conexão fechada por `_CLOSE sleep`, save_confirmed e sleep_confirmed verdadeiros. Não há rotina deixada por esta retomada.

## 3. O que já foi descoberto

**Correção ao plano 002, preservado sem edição:** a Novela não fechou por `say oi` à tagarela na Escadaria Norte. A entrega das vestes ocorreu na Passagem Estreita; a conclusão veio com o esperto na Sacada após `ajuda remortar`. Limpando Monstros não foi completada por fazer o mico fugir: houve a cadeia do Alquimista até o Minotauro, com objetivo atingido após seu abate. O mico foi defesa incidental durante a devolutiva. O brinco tem flag ANTI-DT, mas imunidade da personagem não foi verificada. A crônica recém-reconstruída foi corrigida pela transcrição; evidence/dia156d.json permanece como registro anterior e a fonte desta revisão é dia156e.json.

Leia a seção “Retomada do Dia 156” em [conhecimento.md](../conhecimento.md). A correção central do plano 001 é que **o esperto já havia falado**: a instrução `ajuda mapas` estava nas linhas 5535–5562 do transcript anterior. Não faltava disparar uma fala nova; faltava ler a fala já registrada.

Novela: perdido → ajuda mapas; perturbador → diretrizes e depois sim; veste para tagarela; confuso → retornar; esperto → ajuda remortar. O brinco foi recebido e a aventura encerrada. Alquimista: inseto, dois monstros de veste, dois zumbis, espectro invisível, Minotauro, sempre com retorno entre etapas. Manto e 67.068 EXP entregues.

`where <nome>` localiza o alvo na área. Ordinais 2.novato–7.novato não enumeraram NPCs. Os títulos homônimos continuam exigindo conferir saídas. Mapa preservado e corrigido somente nas conexões observadas da ala iluminada, escadarias e sacadas; corpus parcial não foi digerido.

## 4. Bloqueios e tentativas

Não há bloqueio remanescente nas duas missões concluídas. A próxima meta ainda não foi escolhida. Problemas Agrícolas aparece no score, mas continua vetada pelo autor.

Uma veste foi entregue cedo demais e não contou; outra entrega, quando o objetivo já pedia o objeto, foi reconhecida. Os diálogos demoram dezenas de segundos. Para o confuso, recall não serviu como resposta; retornar serviu. Para o esperto, ajuda encarnacao / encarnação / ajuda encarnação não foram reconhecidas nesta tentativa; ajuda remortar foi.

O driver marcou dead_or_menu no Altar enquanto a personagem estava viva, respondia e tinha HP cheio. Também correlacionou respostas a eventos espontâneos em algumas chamadas. Não houve correção de código nesta sessão; conferir raw/transcript antes de deduzir morte. O controle ficou fechado ao fim.

## 5. Próximo passo único

**Definir com o autor o objetivo do próximo capítulo.** Não abrir outra autoquest nem reiniciar as concluídas para preencher tempo.

## 6. NÃO REPITA

- Não tratar resumo anterior como substituto do transcript; ler falas espontâneas e preroll.
- Não entregar antes de o objetivo correspondente aparecer no score; não despejar frases em sequência.
- Não interpretar catálogo Concluída como prova de fim de um ciclo ainda ativo.
- Não lutar em sala com vários monstros sem cumprir a diretiva; aguardar alvo isolado funcionou para o Minotauro.
- Não presumir que ANTI-DT do brinco torna a personagem imune a armadilhas.
- Não retomar Problemas Agrícolas ou Dicas Mágicas; não vender armaduras; não usar quit.
- Não editar os planos 001 ou 003. Ao fim da próxima sessão, criar o próximo número disponível.

## 7. Ferramentas

`scripts/mandabala.py`, `automato/verificar.py`, `automato/nucleo/driver/play.py`, `scripts/sync_hero.py` e `scripts/check_project.py`. Driver está fechado: nova sessão requer as verificações de ambiente do AGENTS.md. Runtime contém segredos e fica fora do git.

## 8. Encerramento futuro

Salvar e verificar repouso sem quit; preservar evidência com autoria; criar próximo plano; sincronizar derivados; conferir o projeto e a suíte offline. Publicação é etapa separada, condicionada à autorização e ao escopo do pedido.
