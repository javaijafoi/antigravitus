# Dicionário prático da máquina

Seleção curta para jogar melhor com Grebolius. Fonte: `commands` e ajuda do DeBo consultados em 15/10/2026; comparação com os anexos CircleMUD. A lista do servidor contém 244 comandos, mas este guia mantém só os mais úteis. **Ajuda consultada não significa execução testada ou habilidade aprendida.**

| Comando no perfil em inglês | Para quê | Como aplicar / limite |
| --- | --- | --- |
| `help <tema> / commands` | Consultar ajuda e descobrir verbos disponíveis. | A lista foi obtida; a ajuda pode usar nomes em português com comandos em inglês. |
| `look [alvo] / examine <alvo>` | Observar sala, objeto ou criatura antes de agir. | Escolher palavras do que está visível; ler a resposta antes do próximo passo. |
| `look in <recipiente>` | Inspecionar conteúdo de recipiente. | Confirmar se está aberto e acessível. |
| `exits` | Reconhecer saídas diretas. | Não transformar uma saída observada em rota segura ou já percorrida. Scan exige ladrão nível 17 na ajuda atual; não é recurso confirmado de Grebolius. |
| `read <objeto>` | Ler placas, inscrições e textos encontrados. | Exige um alvo que o mundo reconheça. |
| `consider <criatura> / diagnose <criatura>` | Avaliar confronto e condição do alvo. | No DeBo, considerar apresentou vários eixos de risco; não decidir só pelo nível. |
| `inventory / equipment` | Conferir itens carregados e peças vestidas. | Ter no inventário não significa poder equipar. |
| `identify <item>` | Obter propriedades de um item. | identify anel funcionou sem cobrar ouro no nível 11; ver verificações. |
| `list / value <item> / buy <item>` | Consultar comércio, avaliar e comprar. | Confirmar preço, capacidade e nome antes da compra. |
| `get <item> / put <item> <recipiente>` | Pegar e organizar objetos. | Conferir propriedade, peso e destinatário; não pegar por suposição. |
| `eat <comida> / drink <recipiente> / fill <recipiente> <fonte>` | Cuidar de alimentação e água. | Água e comida foram consumidas nesta consulta; reabastecer antes da próxima saída. |
| `say <mensagem> / ask <alvo> <pergunta>` | Interagir com personagens presentes. | A ajuda foi consultada; perguntas não garantem diálogo programado ou missão. |
| `practice / cast '<magia>' [alvo]` | Conferir aprendizado e usar magia aprendida. | Nível e efeito do manual CircleMUD podem divergir; conferir ajuda local e ficha. |
| `flee / wimpy [valor]` | Preparar retirada de um combate. | Fuga não é garantia; conservar o perfil vigente, sem impor o valor antigo do runner. |
| `rest / sleep / wake / stand` | Administrar postura e descanso. | Dormir exige acordar e levantar antes de certas ações; checar resposta real. |
| `save` | Solicitar salvamento. | Resposta observada: “Salvando os seus atalhos.” Não inventar confirmação adicional. |
| `tips` | Alternar dicas periódicas. | Ficou ligado: “Você verá as dicas do jogo.” É toggle; não repetir às cegas. |

## Uma interação melhor

Observar a sala → inspecionar um detalhe presente → escolher um verbo adequado → ler a resposta → decidir a próxima ação. Uma recusa também informa: registrar o alvo e a sintaxe antes de tentar outra forma. Parar deslocamentos quando o destino não corresponder ao esperado.

Antes de combater: considerar o alvo, conferir recursos e retirada. Antes de viajar: inventário, comida, água e proteção vigente. Antes de encerrar: conferir postura, solicitar save e verificar a resposta.

Para ampliar este guia, adicionar apenas um comando que tenha utilidade concreta. Consultar `help <comando>`, registrar a fonte e distinguir ajuda de teste. Uma divergência observada entra em [verificações](verificacoes.md), sem adulterar o manual original.

Ver [diferenças importantes](comparacao_commands.md), [tips](tips.md) e [evidências selecionadas](evidencias/consulta_2026-10-15.json). Os manuais completos ficam separados: [comandos](commands.md), [informações](info.md), [magias](spells.md).
