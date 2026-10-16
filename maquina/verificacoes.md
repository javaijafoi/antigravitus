# Verificações da máquina — 15/10/2026

## Identify: gratuito nas condições observadas

`identify anel` revelou propriedades do anel. Ouro permaneceu 612 e mana 170 antes/depois, com Grebolius no nível 11 da primeira encarnação. Não foi necessário aprender a magia de nível 22. `identificar anel` respondeu “Como?!?” no perfil atual em inglês.

`help identificar` descreve o comando disponível “até o nível 80 da primeira encarnação”. `help identify` descreve a magia e fala em comando “abaixo do nível 80”. Portanto: uso gratuito confirmado no nível 11; acesso descrito até perto do 80; inclusão do nível 80 e custo em outros níveis não testados. Não afirmar que Grebolius aprendeu a magia.

O anel identificado exige nível 90 e encarnação 3 e modifica INT, WIS e CON em +1 e mana máxima em +116, segundo a resposta de identificação. Continua no inventário: identificação não comprova que pode ser equipado agora.

## Tips e encerramento

Última resposta a `tips`: “Você verá as dicas do jogo.” O alias temporário de leitura foi removido, e o terminal retornou a 22 linhas e 80 colunas. Último score: dormindo, 67/67 HP, 170/170 mana, 101/101 MV, 612 moedas, AC 19, sem efeito armor listado e sem alerta de fome/sede. Save respondeu “Salvando os seus atalhos.” antes e depois de dormir; a conexão foi fechada.

A consulta foi técnica, sem deslocamento ou combate. Foram consumidos os dois pães que restavam após o Dia 91 e água do cantil. Inventário final não tem pão: repor comida antes da próxima viagem. A crônica e as evidências do encerramento do Dia 91 continuam representando aquele momento anterior.

O score técnico não exibiu seção de autoquest. Não houve confirmação de cancelamento ou conclusão de Problemas Agrícolas: conservar o último registro conhecido e conferir a situação na próxima sessão autorizada.

## Corrigir após testar

Ao observar divergência: registrar data, comando, alvo, condição relevante, resposta literal e fonte; atualizar só a orientação prática afetada. Ajuda, hipótese e teste são categorias distintas. Preservar os anexos importados.

[Comparação resumida](comparacao_commands.md) · [Evidências selecionadas](evidencias/consulta_2026-10-15.json).

## Atualização — caçada dos Dias 92–93

Os resultados anteriores de manutenção permanecem históricos. Após a caça, equipamentos e recursos mudaram; o Dia 93 foi interrompido, sem confirmação de encerramento. Consultar [aprendizados da caçada](aprendizados-cacada-92-93.md) e a ficha atual antes de assumir que Grebolius continua dormindo ou sem armor. Identify funcionou para itens carregados e recusou itens ainda vestidos (“Você não tem nenhum…”); as identificações de peças antigas foram feitas após removê-las.

## 2026-10-16 — comandos na continuação do Dia 156

Fonte: [evidence/dia156e.json](../data/heroes/grebolius/evidence/dia156e.json). Agente: GPT-6 / Codex (versão específica não informada).

- `help where` documentou localização de monstro/jogador da mesma área. `where minotauro`, `where perturbador`, `where tagarela` e `where confuso` localizaram alvos. `where 2.novato` até `where 7.novato` repetiram o primeiro resultado; não tratar como enumeração. `where chato` não encontrou; a chave real observada foi perturbador.
- `buy 6 pao` comprou seis unidades por 36 moedas. `put all.punhal mochila` guardou oito punhais; `look in mochila` confirmou os oito.
- Diálogo de missão é literal: `say retornar` foi reconhecido pelo confuso, enquanto `say recall` não acionou a resposta. `say ajuda remortar` foi reconhecido pelo esperto. Isso não invalida recall como comando de deslocamento, que funcionou na mesma sessão.
- Entrega antes da etapa pronta: `give veste tagarela` tirou a veste do inventário sem avançar; quando score tudo passou a pedir entregar objeto, uma segunda entrega gerou “Você atingiu seu objetivo”. Esperar a cadência do NPC e conferir a etapa.
- Catálogo `autoquest todas` guardava conclusão histórica de Limpando Monstros enquanto o ciclo reiniciado permanecia ativo em score tudo. Fim do ciclo confirmado por recompensa atual e remoção do objetivo no score, não apenas pelo catálogo.
