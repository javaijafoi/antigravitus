# Boas práticas — o que fazer, o que não fazer, e por quê

> Este documento é **prescritivo sobre método**, não sobre narrativa. Ele não diz o que a personagem
> deve fazer; diz como um agente deve trabalhar neste repositório. Cada regra tem origem declarada —
> quando a origem for uma sessão real, ela está citada.

Ordem de prioridade quando duas regras colidirem:
**diretiva do autor** > **segurança em jogo** > **honestidade documental** > **conveniência**.

---

## 1. Verificação antes de afirmação

O projeto distingue cinco graus de confirmação (`maquina/README.md`). Nunca promova um grau por
conveniência:

| Grau | Significa | Não significa |
| --- | --- | --- |
| **Importado** | existe no anexo CircleMUD | que o DeBo se comporta assim |
| **Listado** | aparece em `commands` do perfil | que a personagem consegue usar |
| **Documentado no servidor** | um `help` retornou o verbete | que o comando faz o que você supõe |
| **Executado** | comando + alvo + resposta real registrados | que vale para outro nível, classe ou item |
| **Divergente / pendente** | fontes discordam ou a resposta não resolve | complete por suposição |

Práticas decorrentes:

- **`help` é fonte documental, não teste.** Dica, TIP e manual não são execução.
- **Uma resposta não é o estado.** A latência corta `exits`, mistura `inventory` com `score` e devolve
  resposta vazia. Confira o marcador da resposta antes de derivar conclusão.
- **`None` não é zero.** "Não sei" não vira "acabou" — trate como pendência.
- **Sinal exige a linha inteira.** Um `Menu Principal` dentro de uma dica do servidor já foi lido como
  morte por um vigia; a detecção correta ancora a linha inteira.
- **Meça antes de acreditar em melhoria.** Fronteira se resolve com caminho, não com peso local.
- **Registre o que divergiu**, com data, contexto, resposta e fonte, em
  [`maquina/verificacoes.md`](../../maquina/verificacoes.md) — preservando o texto importado original.

---

## 2. Evidência: o que conta e onde fica

| Fonte | Onde | Vale como |
| --- | --- | --- |
| Evidência estruturada da sessão | `data/heroes/<id>/evidence/<dia>.json` | prova documental do dia |
| Nota curta de observação | `data/heroes/<id>/observacoes/*.md` | resumo do que o MUD informou |
| Transcrição bruta do driver | `automato/runtime/transcript_*.jsonl` | corpus fiel (algumas cópias em `scripts/local/`, fora do git) |
| Log de sessão | `automato/runtime/session_live_*.log` | leitura pelo vigia |

Práticas:

- **Toda entrada nova precisa de conteúdo real e evidência.** `add_day.py` e `add_chapter.py` recusam o
  contrário; o caminho `document` da referência é relativo à pasta do herói e **precisa existir**.
- **`source_kind=live`** = sessão observada; **`documental`** = reconstrução apoiada em documentos.
  Nenhum dos dois dispensa a fonte.
- **Escreva o `agent`** (`{"agent": "<modelo/versao>", "via": "automato"}`) e declare no relatório.
- **Não fabrique log bruto.** A nota pode resumir observações; não invente uma transcrição inexistente.
- **Separe observação, interpretação e dúvida** — especialmente em `conhecimento.md` e em notas
  editoriais.
- **Segredo nunca entra em evidência.** Nada de senha, token ou transcrição com credencial; o driver já
  sanitiza, mas não confie nisso ao colar texto em documento.

---

## 3. Separação máquina × personagem

`maquina/` e `docs/circlemud/` são **conhecimento do operador**. Eles orientam escolhas de interação;
não criam acontecimentos, habilidades, lembranças, relações, descobertas ou conhecimento da aventureira.

- Um feitiço no manual não habilita a personagem.
- Uma passagem secreta no lore não é revelada à personagem.
- O executor não altera a campanha: consumir eventos JSONL é evidência, não acontecimento.
- Ao reconciliar, **só fato comprovado**; hipótese, comando recusado e tentativa não viram cena,
  recompensa ou sentimento.

---

## 4. Derivados e validação

- **Nunca edite** `ficha.md`, `hero.json`, `data/heroes.json` ou `mapa_vivo.json` à mão: são saída de
  `sync_hero.py` / `digerir_mapa.py`.
- Sequência canônica antes de publicar:

```bash
python scripts/sync_hero.py --hero grebolius
python scripts/sync_hero.py --hero grebolius --check
python scripts/check_project.py
python -B -m unittest discover -s scripts -p "test_*.py"
```

- **Leia os avisos.** `check_project.py` distingue erro de aviso: erro bloqueia, aviso é para ler.
  Zerar um aviso de legado reescrevendo crônica antiga é **pior** que conviver com ele.
- **Não avance `evidence_policy.legacy_through_day`** para contornar a validação. O campo fixa o alcance
  do legado.
- **Não digira corpus parcial.** `digerir_mapa.py` seguido de `fundir_mapa.py` com um recorte de
  transcripts **encolhe** o mapa curado — aconteceu de 360 para 224 salas (v1.4). O `--glob` precisa
  cobrir **todo** o corpus; o sintoma de erro é o `TOTAL` do `fundir_mapa.py` **diminuir**. O curado
  nunca é sobrescrito (só a camada `levantamento` é refeita), mas o resultado mesclado fica incompleto.
- **Registre a origem de cada mudança.** Um item visto no passado cuja posse é incerta vai para
  `inventory.pending_verification`, não para o inventário confirmado.
- Conjuntos offline (Zero-Network) e o relatório HTML saem de `scripts/run_offline_tests.py`.

---

## 5. Segurança em jogo (invariantes operacionais)

| Regra | Motivo (origem real) |
| --- | --- |
| Rotina **nunca** roda sem supervisão: job em segundo plano + leitura do log a cada ~60 s | 4 das mortes vieram de script solto |
| Se o vigia acusar problema, **mate o job** | o script continua sem supervisão e a personagem morre |
| O vigia **lê o log**, não manda comando ao jogo | `score` durante a rotina dessincroniza a sessão |
| `wake; stand` antes de qualquer deslocamento | *"Nah... você está muito relaxado.."* parece bug de rota, é postura |
| **Um comando por vez** sob ameaça | enfileirar ataques com vida incerta mata |
| Vida < 60% em zona densa = hora de sair | atordoamento a 13 de vida impediu a fuga |
| Aviso de DT: *"algo perigoso por perto"* → **parar e voltar** | armadilha mortal mata na hora e destrói itens |
| `save`, **nunca `quit`**, com missão em andamento | `quit` apaga o progresso das missões |
| Ouro dorme no banco; reserva na mão só para comprar | a morte leva o que está no bolso |
| **Proibido itens amaldiçoados**; Torre Negra permitida apenas se NÃO for amaldiçoada (dupla checagem com `identify` no chão antes do `get`) | diretiva do autor (Dia 150, atualizada Dia 156) |
| Invisibilidade **bloqueia comércio** | o balconista recusa: *"Não negocio com quem não vejo!"* — `visible` antes de `list`/`buy` |
| Conjurar **fora** do Templo e da Loja de Magias | essas salas bloqueiam magia; a falha diz "desaparece", palavra que também aparece no sucesso |
| Não concluir que um alvo é invencível sem ler a doutrina do modo | já se declarou o Minotauro invencível atacando de adaga, sendo ela maga |

Fonte detalhada: [`automato/README.md`](../../automato/README.md) § invariantes e § lições de campo;
[`data/heroes/grebolius/diretiva_de_jogo.md`](../../data/heroes/grebolius/diretiva_de_jogo.md).

---

## 6. Método de automação (a ordem importa)

1. **Mapeie à mão primeiro**, sala a sala, e anote o trajeto (de preferência no `mapa.json`).
2. **Leia `exits`** para os **nomes** das saídas — o `look` mostra apenas a lista de direções.
3. **Ande por marco de sala**, não por contagem de passos.
4. **Teste em trechos curtos**, lendo o retorno de cada um: viagem, depois o trecho seguinte, depois a
   caçada. Só junte quando cada trecho passa sozinho.
5. **Limite dentro do script**: teto de passos e de tempo; ao estourar, salvar e sair.
6. **Grave o caminho que funcionou** e reproduza-o.
7. **Edite, confira o arquivo, e só então execute** — em chamadas separadas. Editar e rodar "no mesmo
   bloco" faz o ensaio testar o código anterior.
8. **Depois de editar, varra o AST** procurando reatribuição de variável de estado (um título já foi
   sombreado por um `for ... in do_look.items()` dentro da própria correção).
9. **Para uma rotina nova:** `rotinas/nova.py` seguindo o contrato de `base.py`, testada em trechos,
   rodada via `turno.py`; se for suspensa, vai para `rotinas/_suspensas/` com um LEIA-ME.

---

## 7. Git e publicação

- **Uma mudança, um propósito.** Mensagem com prefixo e escopo: `feat(grebolius): …`, `fix(automato): …`,
  `docs(circlemud): …`, `chore: …`.
- **Sempre termine a mensagem com `[agente: <modelo/versao>]`.** É o único rastro de autoria confiável
  quando vários agentes escrevem no mesmo repositório.
- **Editar arquivos não autoriza publicar.** `publish_daily.py --publish` cria commit local; `--push`
  envia pelo destino já configurado e só existe com `--publish`. Nenhum dos dois é automático.
- **O publicador bloqueia** se `check_project.py` acusar erro, se o índice Git já tiver alterações
  preparadas, ou se o repositório não for o deste projeto.
- **Ele também filtra**: só entram caminhos da lista permitida (`data`, `css`, `js`, `scripts`, `skills`,
  `docs/*.md`, `automato`, `audio`) e um conjunto fixo de arquivos da raiz. `maquina/**` e
  `docs/*.json` **não** estão nessa lista e são preservados fora da revisão — comite-os à parte.
- **Nunca versione** `automato/runtime/`, `scripts/local/`, `.agents/`, logs, sessões, `__pycache__`,
  `play_dia*.py`, `mudclient.py`, `test_samples/`.
- **Não altere identidade ou credenciais globais do Git.**

---

## 8. Escrita documental

- **Não reescreva o passado.** Crônica antiga preservada; correção entra como nota datada.
- **Âncora do autor ≠ fato de servidor.** Quando o autor estabelece uma premissa sem evidência, ela é
  registrada como tal e não reescreve crônicas.
- **Metajogo fora das descrições de capítulo.** O detalhe técnico pertence à descrição do dia e ao
  `registro de evolução`.
- **Incerteza se escreve como incerteza.** Dúvida de continuidade não vira deslocamento, recompensa,
  diálogo ou efeito de morte inventado.
- **Uma fonte por dado.** Não copie número de `state.json` para um `.md` narrativo; referencie.
- **Datas**: `add_day.py` não injeta data fixa nem parágrafo genérico. Substituir um dia ou resumo já
  existente exige `--replace` explícito — releia a evidência e preserve os fatos.

---

## 9. Antipadrões observados (sintoma → regra)

| Sintoma | Causa real | Regra |
| --- | --- | --- |
| Rota "quebrada" | origem calculada do Templo, mas a personagem estava na Praça | a origem da rota é `sala_atual()` |
| Robô girando na mesma sala | recusa lida como sucesso | conferir a chegada pela **sala ter mudado** |
| Porta vira ímã | guarda barra, rotina marca bloqueio e continua mirando a mesma sala | porta recusada sai da fronteira |
| BFS devolve `None` sem motivo | destino gravado com nome cru, grafo normalizado; `?` da linha de colchetes sobrescrevendo nome real | normalizar todo destino; `setdefault`, nunca `update` |
| Muitos "inconclusivo" na caçada | mana seca | `sleep` ~80 s antes de sair |
| Loja não responde ao `list` | invisibilidade ativa | `visible` antes de negociar |
| Falso MORTA | paginador do `commands` deixou o driver em `dead_or_menu` | `term 200 80` no login; nunca rodar `commands` no meio de rotina |
| Progresso de missão zerado de um dia para o outro | `quit` com missão em andamento | encerrar com `save` e deixar a conexão cair |
| "A melhoria piorou" sem prova | bônus de fronteira usado como peso local | medir antes de acreditar |
| Avaliar navegação por replay | o grafo gravado só tem saídas de salas correntes | política de navegação só se avalia com sessão real instrumentada |
| **Crônica publicada errada** (Dia 156) | **leu o FIM de uma cadeia e narrou como se fosse o começo** — a missão só terminou depois de `ajuda mapas → diretrizes → veste → retornar → ajuda remortar` | **o transcript é a fonte; o resumo é interpretação.** Antes de narrar, ler as falas de NPC gravadas |
| **Seis rodadas procurando um NPC** (Dia 156) | não leu `docs/circlemud/`, que dizia **mob por mob, sala por sala**, onde ele nasce | **ler os docs do padrão ANTES de varrer o mundo.** E tentar `where <nome>` antes de andar |
| **~35 frases inventadas numa missão de diálogo** (Dia 156) | tratou diálogo **literal** como enigma | **o NPC diz a palavra; repita A PALAVRA DELE** — `retornar` funcionou, `recall` não |
| **"Missão concluída" com o ciclo ainda ativo** (Dia 156) | usou `autoquest todas` como prova | **`autoquest todas` é HISTÓRICO.** A prova é o **`score`**: objetivo fora do bloco e recompensa entregue |
| **Ação que não conta** | falou/entregou antes de o objetivo pedir | **`score tudo` antes de cada fala e cada entrega**; a etapa muda |
| **Comando registrado que não existe** (Dia 156) | copiou o `Uso:` da **ajuda** — `help where` documenta `onde`, e o servidor responde `Como?!?` | **ajuda não é teste executado** (§1). Testar antes de registrar |
| **Autoria atribuída por inferência** (Dia 156) | viu "o arquivo mudou" e concluiu "outro agente" | **autoria está no campo `agent` e no trailer do commit — nunca se infere de "mudou"** |
| **`sync_hero.py` quebra com `missing_preparation`** | trocou `next_objective` inteiro e apagou um campo lido **por nome** | **não substituir dicionário inteiro**; conferir os campos que o código lê antes |
| **Cabeçalho comido numa edição** | a substituição levou junto o `##` da seção seguinte | ao inserir antes de uma seção, **incluir o cabeçalho dela no texto de substituição** |

Mais casos, com contexto: [`automato/README.md`](../../automato/README.md) § lições de campo e
[`automato/DECISOES.md`](../../automato/DECISOES.md) — em especial a **§9**, que é a lição de método do
Dia 156.

### 9.1 A regra que custou mais caro: **ler a fonte, não a conclusão**

O Dia 156 teve **dois agentes jogando o mesmo capítulo com resultados opostos**, e a diferença não foi
habilidade — foi **de onde cada um leu**:

| Leu a conclusão | Leu a fonte |
| --- | --- |
| Inventou ~35 frases para um diálogo **literal** | Achou a fala que o NPC **já tinha dito** |
| Narrou o fim da cadeia como começo | Reconstruiu a cadeia inteira |
| Usou o catálogo histórico como prova | Conferiu o `score` e a recompensa |
| Varreu o mundo atrás do NPC | Achou a sala nos docs e o alvo com `where` |

**A fala que resolvia a missão estava gravada na linha 5562 de um transcript já aberto**, e passou
despercebida. **O padrão é sempre o mesmo: o arquivo existe, e a conclusão é mais rápida de escrever.**

**Três hábitos que quebram o padrão:**

1. **Antes de narrar ou afirmar, citar a linha.** Se não há linha, é hipótese — e hipótese se rotula.
2. **Antes de varrer, procurar nos docs e tentar `where`.** O mundo é grande; os docs são pequenos.
3. **Antes de escrever a conclusão, reler o que o servidor disse.** Fala espontânea de NPC não se perde:
   está no transcript.

**E a correção não se esconde.** O erro do Dia 156 **ficou**: o `evidence/dia156d.json` e o
`planos/plano002.md` continuam lá, **marcados** e apontando para a correção. **Apagar apagaria a lição.**

---

## 10. Encerramento e handoff

Antes de parar, deixe o próximo agente em condição de continuar:

1. **Estado consistente**: evidência → `state.json` → derivados sincronizados → validadores verdes.
2. **Pendências explícitas**: o que ficou aberto, com hipótese e próximo passo. Onde elas vivem hoje:
   `automato/DECISOES.md` § próximos desafios, `missoes.json` (`next_step`) e o plano do capítulo.
3. **Registro de evolução** com o bloco do §formato (ver
   [registro_de_evolucao.md](registro_de_evolucao.md)), incluindo **custo** e **o que continua aberto**.
4. **Nenhum processo pendurado**: jobs finalizados, driver encerrado com `_CLOSE` (save), nenhum script
   rodando sem supervisão.
5. **Nenhum segredo ou arquivo local** adicionado ao git; `git status` conferido.
