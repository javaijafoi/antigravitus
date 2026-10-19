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

## Conferência prática — 2026-10-16, Dia 156 (continuação)

| Comando | Uso conferido | Limite observado |
|---|---|---|
| `where <nome>` | Localizar **monstro ou jogador dentro da sua área**; testes com minotauro/perturbador/tagarela/confuso. | Um resultado; ordinais não enumeraram NPCs. Fora da área responde `Ninguem com esse nome.` |
| `where` (sem argumento) | Lista **os jogadores da área** (`Jogadores na sua área`). | Não lista monstros. |
| ~~`onde <nome>`~~ | **NÃO EXISTE** — apesar do `help where` documentar `Uso: onde <monstro ou jogador>`. | `onde` e `onde minotauro` respondem `Como?!?`. Ver [verificações](verificacoes.md). |
| `buy 6 pao` | Compra seis unidades, preço confirmado antes pela lista. | Conferir dinheiro e espaço. |
| `put all.punhal mochila` | Guardou oito punhais no contêiner. | Confirmar com `look in mochila`. |
| `score tudo` | Conferir etapa atual antes de fala/entrega. | Falas continuam após o eco do comando; não antecipar entrega. |

As palavras exigidas em falas de missão podem diferir do alias usado pelo operador. Ver [verificações e fonte literal](verificacoes.md).

### Verificação complementar — Dia 157 (2026-10-19)

- `where <NPC>`: testado com Lemin, retornando Centro da Cidade de Lyon na região Notre Dame.
- `cast 'locate object' <objeto>`: recusado no nível 32; help locate informa Mago 34 e espelho localizador. Requisitos superiores ainda não testados.
- `score tudo`: conferir a instrução específica de Ajuda Mágica após cada monólogo; uma resposta antecipada Merlin não avançou a etapa, enquanto a resposta após a fala final foi reconhecida.

Fonte e limites: [verificações de 2026-10-19](verificacoes.md), evidence/dia157-cap12.json. Agente: GPT-6 / Codex (versão específica não informada).
