# CircleMUD × DeBo: diferenças que mudam decisões

Comparação curta, baseada nos anexos fornecidos e na ajuda atual do servidor em 15/10/2026. **Documentado** significa que o help diz; **observado** significa resposta real de execução.

| Tema | Manual CircleMUD fornecido | DeBo / consequência prática |
| --- | --- | --- |
| Idioma | Exemplos em inglês. | Lista atual em inglês, ajuda frequentemente em português. `identify anel` funcionou; `identificar anel` foi recusado. Não traduzir automaticamente o verbo. |
| Consider | Compara nível, sem avaliar vida e dano. | No Dia 91 a resposta comparou nível, vida, poder, precisão e armadura. Pesar todos os riscos observados. |
| AC | Escala genérica negativa, menor é melhor. | Help AC diz que cada 10 pontos reduz 1 de dano antes de sanctuary. AC 19 foi medida sem armor; 44 com armor +25 no Dia 91. Não importar a escala negativa. |
| Armor | Melhoria de 2 AC; mago 4/clérigo 1. | Help local indica mago 7/clérigo 9/paladino 1. Efeito +25 observado no nível 11. Cabeçalho do help tem sinal negativo e prosa fala em aumento: divergência preservada. |
| Identify | Não consta como verbete de magia no spells.hlp fornecido. | Comando identificou o anel no nível 11 sem reduzir ouro/mana. Ajuda do comando diz “até 80”; ajuda da magia diz “abaixo de 80”, na primeira encarnação. Nível 80 exato não testado. |
| Invisibilidade | Mago 4, duração 24h. | Help local: mago 6, duração 6 + nível/4, +40 AC, ataque quebra o efeito. Dados documentados; não todos testados. |
| Locate object | Mago 6. | Help local: mago 34 e espelho localizador. Não tratar como recurso já disponível à personagem. |
| Offer | Cotação de hospedagem com RENT. | `help offer` retorna oferenda/sacrifício de cadáver. Colisão perigosa: não executar como consulta de preço. |
| Circle | No info.hlp é tópico sobre CircleMUD. | `help circle` retorna habilidade de combate CIRCLE AROUND. Conferir se o tópico corresponde ao pretendido. |
| Save / quit | Descreve necessidade de rent para guardar equipamento. | Help local de quit diz que os itens permanecem com você. Save respondeu “Salvando os seus atalhos.” Não transplantar a regra genérica de hospedagem. |
| Tips | Ausente no manual de comandos fornecido. | `tips` alterna dicas; ficou ligado e produziu mensagens DICA. |

Fonte e trechos de ajuda: [evidências selecionadas](evidencias/consulta_2026-10-15.json). O texto original dos anexos foi preservado como referência, com correções locais separadas em [verificações](verificacoes.md).
