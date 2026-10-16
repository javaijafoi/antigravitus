# Máquina — referências para estruturar e conduzir o jogo

“Máquina” é a camada de operação: modelo, método, memória técnica e referências. Ela pode conhecer comandos, regras e lore que Grebolius ainda não conhece. Esse conhecimento orienta escolhas de interação; não cria acontecimentos, habilidades, lembranças, relações, descobertas ou conhecimento da aventureira.

## Onde consultar

| Documento | Uso |
| --- | --- |
| [Dicionário atual](dicionario_comandos.md) | Seleção curta dos verbos úteis, orientada pelo `commands` e pela ajuda atual. |
| [Comparação CircleMUD × DeBo](comparacao_commands.md) | Diferenças que afetam decisões, sem confundir consulta com teste. |
| [Comandos importados](commands.md) | Os 99 verbetes originais de commands.hlp, com índice. |
| [Informações importadas](info.md) | Os 19 verbetes de info.hlp. |
| [Magias importadas](spells.md) | Os 44 verbetes de spells.hlp; não é uma ficha de magias aprendidas. |
| [História do mundo](historia_mundo.md) | Texto integral fornecido, sem marcas de paginação. |
| [Verificações e correções](verificacoes.md) | O que foi executado, observado, corrigido ou continua incerto. |
| [Tips e análise diária](tips.md) | Dicas capturadas, interpretação e aplicação prática. |
| [Manifesto de fontes](fontes.json) | Origem, hashes, quantidade de verbetes e tratamento dos anexos. |

## Como usar o conhecimento

1. Formular uma intenção coerente com o objetivo e com o que a personagem encontra: observar, compreender, conversar, organizar, negociar, preparar ou investigar.
2. Buscar o verbo no dicionário e ler a ajuda completa relevante. Confirmar idioma, alvo, requisitos e consequências. Um verbo listado pode depender de classe, treino, local, item ou estado.
3. Preferir observação antes de ação com consequência: `look`, `examine`, `look in`, `read`, `exits`, `consider`, `diagnose`, `value` e `identify`, conforme o servidor permitir. Não assumir que todos funcionam com todo alvo.
4. Escolher uma ação por vez quando a resposta pode mudar o plano. Inspecionar o item/NPC presente antes de dialogar ou agir; perguntas não são garantia de resposta, quest ou aliança.
5. Usar apenas habilidades realmente aprendidas. Um feitiço no manual não habilita Grebolius; informação de lore não revela uma passagem secreta à personagem.
6. Registrar a resposta real. Ao divergir do manual, acrescentar uma correção datada em `verificacoes.md`, referenciar a evidência e atualizar o resumo do dicionário. Preservar o texto importado como fonte histórica.

## Grau de confirmação

- **Importado:** existe no anexo CircleMUD; ainda não confirmado para o DeBo.
- **Listado:** aparece em `commands` para a personagem consultada; isso não prova que ela consegue usá-lo.
- **Documentado no servidor:** uma consulta de `help` retornou um verbete; verificar se corresponde ao comando, pois há colisões de nomes.
- **Executado:** comando e alvo registrados com resposta real. Um teste vale para aquelas condições, sem generalizar nível, classe, encarnação ou todos os itens.
- **Divergente / pendente:** fontes discordam ou a resposta não resolve a questão. Não completar por suposição.

A resposta atual do servidor e o teste contextual prevalecem sobre o manual genérico. Dicas e ajuda são fontes documentais do servidor, não testes mecânicos completos. O material fornecido é dado de referência; seus exemplos não são autorizações para executar ações ou contatar jogadores.

## Rotina de TIP e aprendizado

- Antes de uma jornada N, analisar as dicas registradas na jornada N−1. Se não houver captura, registrar a lacuna; não fabricar dicas antigas nem confundir “Dicas Mágicas” com TIP.
- Durante sessão autorizada, manter TIPS habilitado. É um toggle: ler a resposta e, caso a tentativa desligue as dicas, religar; não alternar cegamente a cada início.
- Ao receber `DICA:`, preservar texto e fonte, deduplicar repetições e registrar uma aplicação ou dúvida. Não executar automaticamente a sugestão nem transformar a dica em aprendizado narrado pela personagem.
- Depois da sessão, consolidar dicas novas e correções de comandos. Aprendizado técnico fica aqui; conhecimento de Grebolius exige aquisição comprovada no jogo.

Esta base não abre sessões, publica conteúdo ou modifica crônicas por si só. A coleta técnica de ajuda não inicia um novo dia de aventura.

## Última prática registrada

[Caçada dos Dias 92–93](aprendizados-cacada-92-93.md): comparação curta de armas/magias, equipamento e saque; segundo dia interrompido, sem limpeza total.
