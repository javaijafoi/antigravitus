# Evidências do DeBo — o que já foi observado no servidor real

Documento de mineração das **evidências locais** do projeto. Ele responde a uma pergunta só:
*quais afirmações sobre comandos, navegação e magias no Devil's Bob MUD (`debomud.org:4000`) já têm
resposta real registrada, e onde está essa resposta?*

Regra da casa: **só uma resposta real do servidor, registrada com `arquivo:linha`, promove uma linha a
Testado.** Ajuda consultada, prosa do projeto e resumo de evidência sem transcrição entram como
**Provável**. Divergência entre fontes entra como **Dúvida** — e as duas versões aparecem.

Isto não transfere conhecimento para a personagem e não substitui `maquina/`, que permanece sendo onde
o servidor **documenta** e o que já foi **verificado**.

## Fontes consultadas

| Fonte | Tamanho aprox. | Tratamento |
| --- | --- | --- |
| `maquina/evidencias/consulta_2026-10-15.json` | 48 KB (552 linhas) | **Lida inteira.** Fonte primária: `command` + `response` + `source_file` + `source_line`. |
| `maquina/commands.md` | 42 KB (1.934 linhas) | Varredura por índice e leitura dirigida (ALIAS, AUTOEXIT, BANK, BRIEF, COMPACT, DISPLAY, OFFER, SAVE, SCORE, SELL, TIME, TOGGLE, VALUE, VISIBLE, WIMPY). É **ajuda importada do CircleMUD**, não do DeBo. |
| `maquina/spells.md` | 18 KB | Varredura por verbete; é manual importado (44 verbetes). |
| `maquina/info.md` | 19 KB | Índice + leitura de AC, SHOPS, SPELLS. Importado do CircleMUD. |
| `maquina/verificacoes.md`, `tips.md`, `dicionario_comandos.md`, `comparacao_commands.md`, `aprendizados-cacada-92-93.md`, `README.md`, `fontes.json` | 1–5 KB cada | Lidas inteiras. |
| `data/heroes/grebolius/evidence/dia91..dia95.json` | 21 KB – 339 KB | Lidas (dia94 por extração programática das entradas `command`/`response`). |
| `data/heroes/grebolius/evidence/dia96..dia156b.json` (+ `autoquests-dia143.json`, `capitulo-*.json`) | 0,3 – 5,5 KB cada | Lidas inteiras, com foco em dia100, dia106, dia113b, dia123, dia148, dia153, dia154, dia155, dia156, dia156b. |
| `data/heroes/grebolius/conhecimento.md` | 75 KB (764 linhas) | Leitura dirigida (§17, §20, §25.1–25.12) + varredura. |
| `data/heroes/grebolius/ficha.md`, `diretiva_de_jogo.md`, `missoes.md`, `observacoes/morte-04-dia-100.md`, `observacoes/checagem-venda-armadura.md` | 1,5–13 KB | Lidos/varridos. |
| `scripts/local/transcript_dia97_…e1d2ac.jsonl`, `…dia98_…ca2c00`, `…dia100_…acc661`, `…dia101_…cd4a79`, `…dia104_…d958b4`, `…dia106_…019cdd`, `…dia141_…5a9f49` | 65 KB – 2,7 MB | Extração programática das entradas `"kind": "command"` (comando, texto, vitais, delta de mana). |
| `automato/runtime/transcript_dia155_…82c3eb.jsonl`, `…dia156_…08e293`, `…9eb61a`, `…1a4abb`, `…2cb7a0` | 189 KB – 4,3 MB | Idem. |
| `automato/README.md`, `DECISOES.md`, `CHANGELOG.md`, `nucleo/guarda.py`, `camadas/{vigia,prepara,cuidar}.py`, `rotinas/mercado.py`, `nucleo/config.py` | pequenos | Lidos/varridos como registro de comportamento observado em produção. |
| `docs/circlemud/00-afirmacoes-e-validacao.md` | 5,7 KB | Lido; define os níveis de confiança que este documento usa. |
| `docs/expedicao_comandos.md`, `docs/rotinas.md`, `docs/expedicao_modular.md`, `docs/expedicao_esgotos_dia95.md` | 2,5–19 KB | Varridos. |

### Fontes que **não** consegui varrer por inteiro

- **`scripts/local/` como um todo (476 arquivos, ~27,6 MB)** — não foi lido arquivo por arquivo. Usei
  `grep` dirigido e extração programática apenas dos `transcript_*.jsonl`. Os `session_*.log` e
  `session_*.txt` (alguns de 1 a 8 MB, ex.: `transcript_dia111_20261016_013534_fcd6da.jsonl`, 8,9 MB;
  `session_live_dia111_*.log`, 5,5 MB) só foram tocados por padrões específicos. **Achados possíveis
  foram perdidos.**
- **`automato/runtime/transcript_dia156_20261016_123921_2cb7a0.jsonl` (4,3 MB)** — durante parte da
  varredura o arquivo estava **travado pelo daemon ao vivo** (`The process cannot access the file …`);
  só consegui lê-lo via `grep` e por shell read. As linhas citadas dele foram confirmadas por `grep`.
- **`data/heroes/grebolius/evolucao.md` (155 KB)** — varredura por padrões apenas; é narrativa, não
  transcrição, e portanto não gera linha **Testado**.
- **`data/heroes/grebolius/mapa.json`, `mapa_vivo.json`, `posts.json`, `state.json`, `ciclos.json`,
  `capitulos.json`, `events.json`** — varridos por padrões pontuais (relaxado, inanição, choque, magia).
- **Nada em `scripts/test_fixtures/`** foi usado como evidência: são dados de teste.

---

## Tabela principal — fatos já observados no DeBo

Confiança: **Testado (resposta real registrada)** · **Provável (relato/documentação do projeto, sem transcrição)** · **Dúvida (divergência ou ambíguo)**.

| # | Fato observado no DeBo | Fonte da evidência (arquivo:linha) | Comando/resposta literal (trecho) | Confiança |
| --- | --- | --- | --- | --- |
| 1 | `term <linhas> <colunas>` configura o terminal e responde em português | `maquina/evidencias/consulta_2026-10-15.json:411-415` | `term 22 80` → `Muito bem, agora seu terminal está configurado para 22 linhas e 80 colunas.` | **Testado** |
| 2 | A linha de paginação tem forma fixa, com `S` de saída e número de página | `data/heroes/grebolius/evidence/dia92.json:382`; `dia91.json:285` | `[ Aperte ENTER para continuar, S para sair ou número da página ( 1 de 2 )     ]` | **Testado** |
| 3 | A paginação existe de fato e varia por comando | `automato/runtime/transcript_dia156_20261016_121159_9eb61a.jsonl:116`; `…102159_08e293.jsonl:5958` | `spells` → `( 1 de 3 )`; `commands` → `( 1 de 3 )`; `help autoquest` → `( 1 de 5 )` | **Testado** |
| 4 | A linha do paginador vem **colada no prompt**, sem quebra de linha antes do `>` | `data/heroes/grebolius/evidence/dia92.json:382` | `… 19) Ilimitado Um peitoral 18.000 0 1` `\n` `[ Aperte ENTER … ( 1 de 2 )     ] 67hp 170mn 101mv >` | **Testado** |
| 5 | `commands` é paginado e anuncia o idioma da lista | `automato/runtime/transcript_dia156_20261016_102159_08e293.jsonl:5958` | `Os seguintes comandos estão disponíveis em INGLÊS para você:` — inclui `autoexit`, `autogold`, `autoquest`, `balance`, `deposit`, `identify` | **Testado** |
| 6 | Não há evidência de resposta visivelmente **cortada por largura** (80 colunas): o servidor quebra as linhas | `data/heroes/grebolius/evidence/dia92.json:382` | A tabela de `list` quebra em 80 colunas e continua na página 2 | **Dúvida** (há relato de `exits` cortado — ver #26) |
| 7 | `term` **não existe** na ajuda importada do CircleMUD, mas funciona no DeBo | `maquina/commands.md` (índice, linhas 15-113, não contém TERM); `maquina/evidencias/consulta_2026-10-15.json:411` | índice de verbetes sem `TERM` × resposta real aceitando `term 22 80` | **Dúvida** (extensão do DeBo) |
| 8 | `score tudo` / `pontos` tem formato fixo com seções em colchetes | `maquina/evidencias/consulta_2026-10-15.json:292-296` | `[Pontos e atributos]`, `[Ouro e equipamentos]`, `[Situação atual]`, `[ Duração ]` | **Testado** |
| 9 | O contador de mortes aparece no início do `score` | `maquina/evidencias/consulta_2026-10-15.json:296`; `scripts/local/transcript_dia100_20261016_000913_acc661.jsonl:134` | `Você morreu 3 vezes e não caiu em nenhuma armadilha de morte.` → depois `Você morreu 4 vezes e caiu em 1 armadilha de morte.` | **Testado** |
| 10 | `score` mostra `[Autoquests em andamento]` quando há missão ativa | `data/heroes/grebolius/evidence/dia91.json:235`; `dia156.json:30` | `Problemas Agrícolas: Você deve matar criaturas.` | **Testado** |
| 11 | A seção `[ Duração ]` lista efeitos ativos com horas restantes e magnitude | `maquina/evidencias/consulta_2026-10-15.json:296`; `dia95.json:335` | `armor                 (   5 horas ) +25 em ARMADURA` / `poison                (   9 horas ) -2 em FORÇA` | **Testado** |
| 12 | `exits` devolve bloco nomeado por direção, alinhado por coluna | `data/heroes/grebolius/evidence/dia91.json:33`; `automato/runtime/transcript_dia156_20261016_113245_1a4abb.jsonl:13` | `Saídas:\nNorte - O Altar do Templo\nLeste - A Sala de Doações de Midgaard\nSul   - A Praça do Templo\nOeste - A Sala de Leitura\nCima  - O Panteão dos Centenários\nBaixo - A Praça do Templo` | **Testado** |
| 13 | O `look` traz a linha de colchetes, que é fonte independente do `exits` | `data/heroes/grebolius/evidence/dia92.json:121` | `[ Saídas: norte, leste, sul, oeste, cima e baixo ]` | **Testado** |
| 14 | Porta fechada/trancada aparece com `!` **antes** do nome da direção | `data/heroes/grebolius/evidence/dia92.json:976`; `dia95.json:245` | `[ Saídas: norte, sul e !oeste ]` · `[ Saídas: leste, sul e !baixo ]` | **Testado** |
| 15 | `consider` devolve tabela de cinco eixos, sem nomear o alvo | `data/heroes/grebolius/evidence/dia93.json:665`; `scripts/local/transcript_dia100_20261016_000913_acc661.jsonl:110` | `Você  Oponente` / `Nível: 11   Fácil!` / `Vida: 87   É uma perda de tempo` / `Poder: 25   É uma perda de tempo` / `Precisão: 18   Fácil!` / `Armadura: 50   Perfeito!` | **Testado** |
| 16 | `consider` **recusa** quando o alvo é objeto | `data/heroes/grebolius/conhecimento.md:665` (prosa, com a frase citada) | `Comparar sua força com a de quem?` | **Provável** |
| 17 | `inventory` abre sempre com `Você está carregando:` | `maquina/evidencias/consulta_2026-10-15.json:373`; `automato/runtime/transcript_dia156_20261016_102159_08e293.jsonl:21` | `Você está carregando:\num cantil\n(x3) um pão recheado …` | **Testado** |
| 18 | `equipment` abre com `Você está usando:` e usa setas `->` | `automato/runtime/transcript_dia156_20261016_121159_9eb61a.jsonl:17` | `Você está usando:\n  no corpo           -> a Armadura da Torre Negra ..Isso tem uma pequena aura! (novo)` | **Testado** |
| 19 | `wimpy <n>` responde em português e aceita número | `data/heroes/grebolius/evidence/dia91.json:40`; `automato/runtime/transcript_dia155_20261016_092432_82c3eb.jsonl:5` | `Certo, você irá se acovardar se você ficar abaixo de 17 pontos de vida.` → depois `… abaixo de 30 pontos de vida.` | **Testado** |
| 20 | `wimpy` **não aceita** valor acima da metade da vida máxima | `data/heroes/grebolius/evidence/dia113b.json:10` (com os literais registrados) | `wimpy 45` recusado; `wimpy 43` aceito (`Você irá se acovardar abaixo de 43 pontos de vida`) | **Provável** (relato de evidência, sem transcrição crua no workspace) |
| 21 | `save` responde sempre a mesma frase | `maquina/evidencias/consulta_2026-10-15.json:432-437`; `automato/runtime/transcript_dia155_20261016_092432_82c3eb.jsonl:832` | `save` → `Salvando os seus atalhos.` | **Testado** |
| 22 | `alias <nome>` apaga o atalho e confirma | `maquina/evidencias/consulta_2026-10-15.json:404-408` | `alias cxhelp_1817` → `Atalho apagado.` | **Testado** |
| 23 | `alias` **criação** não foi observada | — | — | **Dúvida** (lacuna) |
| 24 | `tips` é alternância e responde nas duas direções | `maquina/evidencias/consulta_2026-10-15.json:299-303, 390-394, 397-401` | liga: `Você verá as dicas do jogo.` / desliga: `Você não verá mais as dicas do jogo.` | **Testado** |
| 25 | As dicas chegam como linha prefixada por `DICA:` | `data/heroes/grebolius/evidence/dia92.json:157, 265, 310` | `DICA: Para recitar um pergaminho, utilize o comando RECITAR.` | **Testado** |
| 26 | O `exits` pode devolver resposta **desalinhada** (descrição de sala, dica, evento ou nada) no lugar da lista | `automato/runtime/transcript_dia156_20261016_102159_08e293.jsonl:2117, 2161, 2382`; `automato/runtime/transcript_dia156_20261016_123921_2cb7a0.jsonl:1615` | `cmd: "exits"` → `Valgren tagarela: 'pelo menos deu pra fugir'` · `→ Você não pode ir por aí...` · `→ O Sol, vagarosamente, se põe no oeste.` · `cmd: "look"` → `Saídas: Norte - O Escritório dos Correios …` | **Testado** |
| 27 | Leitura curta de `exits` em sala de seis portas (1 linha só) | `data/heroes/grebolius/conhecimento.md:573-586` | “Uma delas trouxe **uma linha numa sala de seis portas**”; a regra passou a ser *“ler `exits`, mas acrescentar o que a linha de colchetes anuncia”* | **Provável** (medido segundo o projeto, sem literal preservado) |
| 28 | `autoquest` sozinho pede subcomando | `data/heroes/grebolius/evidence/dia91.json:264-265` | `Certo, mas qual comando de autoquest?\nDigite AJUDA AUTOQUEST para ver as opções.` | **Testado** |
| 29 | `autoquest todas` lista catálogo com status e requisitos | `data/heroes/grebolius/evidence/dia156.json:29`; `scripts/local/transcript_dia101_20261016_003804_cd4a79.jsonl:88` | `Autoquests do DeBo MUD` … `Problemas Agrícolas            Em andamento` / `Uma Lição em Gargamel          Não feita` | **Testado** |
| 30 | `identify <item>` responde com bloco `Você se sente informado:` | `maquina/evidencias/consulta_2026-10-15.json:324`; `scripts/local/transcript_dia101_20261016_003804_cd4a79.jsonl:35-37` | `Objeto: 'a Espada do Peão Negro' Tipo: ARMA` / `O item é: ANTI-BOM NOBITS` / `Peso: 10, Valor: 100, Aluguel: 1, Nível: 11, Encarnação: 1` | **Testado** |
| 31 | O verbo em português `identificar` é recusado com o perfil em inglês | `maquina/evidencias/consulta_2026-10-15.json:306-310` | `identificar anel` → `Barlow vai para oeste.` `\n\n` `Como?!?` | **Testado** |
| 32 | `recall` é gratuito até o nível 70 e leva ao Templo de Midgaard | `automato/runtime/transcript_dia156_20261016_123921_2cb7a0.jsonl:14` | `Retornando para sua cidade natal...\nLembre-se, você só poderá retornar gratuitamente até o nível 70. Depois disso lance magias de retorno e use pergaminhos.\n\nO Templo de Midgaard` | **Testado** |
| 33 | `sleep` / `wake` / `stand` / `rest` têm respostas fixas | `consulta_2026-10-15.json:334-338, 439-443`; `dia156.json:31`; `transcript_dia155_…82c3eb.jsonl:2-3`; `transcript_dia111_…fcd6da.jsonl:9954` | `Você se deita e dorme.` · `Você já está dormindo profundamente.` · `Você já está acordado...` · `Você já está em pé.` · `Você se senta e descansa seus ossos cansados.` | **Testado** |
| 34 | Ações físicas são recusadas dormindo | `automato/runtime/transcript_dia156_20261016_102159_08e293.jsonl:1145` | `fill cantil fonte` dormindo → `Você não pode fazer isso dormindo.` | **Testado** |
| 35 | `eat` / `drink` / `fill` respondem em português | `consulta_2026-10-15.json:341-345, 348-352`; `transcript_dia156_…08e293.jsonl:22-26, 1157` | `Você come um pão recheado.` · `Você bebe água cristalina.\nVocê não sente mais sede.` · `Você enche um cantil a partir de a grande fonte com agua cristalina.` | **Testado** |
| 36 | `eat` erra a palavra quando o item não existe com aquele nome | `automato/runtime/transcript_dia156_20261016_102159_08e293.jsonl:24` | `Você não tem nenhum pao.` (sem acento, casando a palavra digitada) | **Testado** |
| 37 | `practice` sem argumento lista magias e proficiências em % | `automato/runtime/transcript_dia156_20261016_121159_9eb61a.jsonl:62`; `scripts/local/transcript_dia98_…ca2c00.jsonl:132` | `Você tem 24 sessões de treino sobrando.\nVocê conhece as seguintes magias e habilidades:\narmor  99%:   (perfeito)` | **Testado** |
| 38 | `practice <magia>` fora da guilda é recusado | `automato/runtime/transcript_dia156_20261016_121159_9eb61a.jsonl:92` | `Você pode praticar somente em sua guilda.` | **Testado** |
| 39 | Um treino leva de 10% a 95% e não repete | `automato/runtime/transcript_dia156_20261016_121159_9eb61a.jsonl:124-130` | `Você pratica por um tempo...` → `Você agora está instruído nessa área.` → `Você já está instruído nessa área.` | **Testado** |
| 40 | `spells` lista a progressão numerada de magias do mago | `automato/runtime/transcript_dia156_20261016_121159_9eb61a.jsonl:116` | `Uma maga aprende as seguintes magias:` … `20 -> lightning bolt` … `33 -> charm person` + `( 1 de 3 )` | **Testado** |
| 41 | `skills` foi lido no jogo (nadar, blast, mix, second attack, magic extension) | `data/heroes/grebolius/evidence/dia156b.json:16` | `1 swim, 22 blast, 40 mix, 50 second attack, 60 magic extension` | **Provável** (relato, sem transcrição do bloco) |
| 42 | `deposit <valor>` funciona no Templo e confirma em português | `automato/runtime/transcript_dia156_20261016_102159_08e293.jsonl:31` | `Você deposita 232 moedas.` | **Testado** |
| 43 | `balance` existe e responde em português | `scripts/local/transcript_dia141_20261016_072801_5a9f49.jsonl:1331` | `Você possui 7.032 moedas no banco.` | **Testado** |
| 44 | O `score` exibe `Banco:` e `Carregando:`/`Total:` separados | `data/heroes/grebolius/evidence/dia156.json:30`; `scripts/local/transcript_dia141_…5a9f49.jsonl:1332` | `Banco: 7.528 | Carregando: 300 - Total: 7.828` / `Banco: {<<<<<>>>>>} 7.032` | **Testado** |
| 45 | `list` devolve tabela com cabeçalho e colunas de preço/nível/encarnação | `data/heroes/grebolius/evidence/dia92.json:382`; `automato/runtime/transcript_dia156_20261016_123921_2cb7a0.jsonl:5498` | ` ##   Disponível   Item                                         Preço Nível Enc.` | **Testado** |
| 46 | `buy` cobra, entrega e confirma com dois blocos | `data/heroes/grebolius/evidence/dia93.json:215` | `O padeiro falou por telepatia com você: 'São 18 moedas.'\nVocê comprou um pão recheado (x 3).` | **Testado** |
| 47 | `sell` negocia por telepatia e recusa quando o caixa do NPC não cobre | `automato/runtime/transcript_dia156_20261016_121159_9eb61a.jsonl:256, 217` | `O armeiro falou por telepatia com você: 'Você receberá 500 moedas por isso!'\nO lojista agora possui um anel arcano.` · recusa: `'Isso é caro demais para mim - Tente um feiticeiro!'` | **Testado** |
| 48 | `value <item>` responde pelo NPC, com recusa tipada | `automato/runtime/transcript_dia156_20261016_121159_9eb61a.jsonl:33-35` | `O feiticeiro falou por telepatia com você: 'Eu não compro esse tipo de coisa.'` · `'Você não parece ter isso.'` | **Testado** |
| 49 | `get` recusa quando o peso estoura | `automato/runtime/transcript_dia156_20261016_121159_9eb61a.jsonl:47` | `Você já está carregando muito peso e não pode pegar a bainha de Excalibur.` | **Testado** |
| 50 | `wear` valida dono e nível do item | `scripts/local/transcript_dia100_20261016_000913_acc661.jsonl:4` | `Você já está usando algo sobre o corpo.` · `Você não tem experiência para usar a bainha de Excalibur.` · `Você não pode usar um colar com uma pedra púrpura porque não é o dono do item.` | **Testado** |
| 51 | `remove` confirma a peça retirada | `scripts/local/transcript_dia101_20261016_003804_cd4a79.jsonl:60, 64` | `Você pára de usar os chifres do Minotauro.` | **Testado** |
| 52 | `quit` responde e imprime a mensagem de aventuras não concluídas | `data/heroes/grebolius/evidence/dia156.json:31` | `quit` → `Adeus e volte sempre!\n*Você falhou em suas aventuras! Se quiser concluí-las deverá recomeçá-las!*` | **Testado** |
| 53 | O **mesmo** aviso de aventuras falhadas aparece na **morte**, não só no `quit` | `scripts/local/transcript_dia100_20261016_000913_acc661.jsonl:126` | `… golpe que esmaga seu crânio!\nVocê está morto!\nVocê perdeu 1.435 pontos de experiência pela sua morte.\n*Você falhou em suas aventuras! Se quiser concluí-las deverá recomeçá-las!*` | **Testado** |
| 54 | `prompt` como comando **nunca** aparece nos registros; o prompt observado é `hp mn mv >` | `maquina/evidencias/consulta_2026-10-15.json:296`; `automato/nucleo/driver/debo_bot.py:619` | prompt literal: `67hp 170mn 101mv >`; regex do driver: `(-?\d+)\s*hp\s+(-?\d+)\s*mn\s+(-?\d+)\s*mv\s*>` | **Dúvida** (comando não testado; formato do prompt sim) |
| 55 | `display hv / display all / display auto` está documentado no manual importado | `maquina/commands.md:475-488` | `Usage: display < H | M | V | all | auto | off >` | **Provável** (documentado, não executado) |
| 56 | `autogold` existe na lista de comandos do DeBo, mas nenhuma resposta foi capturada | `automato/runtime/transcript_dia156_20261016_102159_08e293.jsonl:5958` (nome na lista) | `autogold` presente na página 1 de `commands`; sem transcrição de execução | **Dúvida** |
| 57 | `offer` no DeBo é **OFERENDA de cadáver**, não cotação de aluguel | `maquina/evidencias/consulta_2026-10-15.json:262-266` | `OFERENDA OFFERING` … `cada corpo dado em oferta é recompensado com 50 pontos de experiência` | **Provável** (ajuda consultada; não executado) |
| 58 | `sacrifice` não funciona; `sacrificar`/`queimar`/`burn` não existem | `data/heroes/grebolius/evidence/dia156b.json:18` | `'sacrifice' responde 'Voce nao tem ideia de como fazer isso'. 'sacrificar', 'queimar' e 'burn' respondem 'Como?!?': nao existem.` | **Provável** |
| 59 | `l` é `look` e `o` é `order` — **não** são direções | `data/heroes/grebolius/evidence/dia156b.json:18`; `dia156.json:12` | `O servidor MUD interpreta 'l' como 'look' (olhar), e nao como o token direcional 'e' (leste)` | **Testado** (relatado como medido ao vivo, com o comando em `dia156.json`) |
| 60 | `diagnose` / `train` / `time` / `where` / `weather` / `gold` / `donate` / `junk` / `quaff` não têm execução registrada nos transcripts varridos | varredura de `scripts/local/*.jsonl` e `automato/runtime/*.jsonl` | — (nenhuma entrada `cmd` com esses verbos) | **Dúvida** (lacuna de teste) |

---

## 1. Terminal e paginação

**Fato #1 — `term` funciona e responde em português.**

```text
> term 22 80
Muito bem, agora seu terminal está configurado para 22 linhas e 80 colunas.
```
`maquina/evidencias/consulta_2026-10-15.json:411-415` (`source_file: maquina_tip_identify_20261015_184005.jsonl`, `source_line: 79`).

**Fato #2 — o texto exato da linha de paginação.**

```text
[ Aperte ENTER para continuar, S para sair ou número da página ( 1 de 2 )     ]
```
`data/heroes/grebolius/evidence/dia92.json:382` — aparece **colada no prompt** na mesma linha:
`… ( 1 de 2 )     ] 67hp 170mn 101mv >`. A mesma forma reaparece com `( 1 de 3 )` em
`automato/runtime/transcript_dia156_20261016_121159_9eb61a.jsonl:116` (`spells`) e `( 1 de 5 )` em
`data/heroes/grebolius/evidence/dia91.json:285` (`help autoquest`).

**Fato #3 — o terminal é 80 colunas, e o servidor quebra as linhas em vez de cortar.** A tabela do
`list` em `dia92.json:382` quebra alinhamento em 80 colunas e continua na página seguinte; não há
linha truncada no meio de palavra. **Não achei, em nenhum log varrido, uma resposta com corte por
largura.** O `docs/circlemud/00-afirmacoes-e-validacao.md:34-40` ainda lista esse teste como aberto.

**Fato #4 — o DeBo tem `term`, o manual importado não.** O índice de `maquina/commands.md:15-113`
não tem `TERM`; a única ocorrência de `PAGE`/`pagelength` no projeto é a própria palavra inglesa em
prosa. `docs/circlemud/00-afirmacoes-e-validacao.md:37` sugere testar `term 60 200` — **isso ainda não
tem resposta registrada**, é lacuna.

**Fato #5 — paginação existe em `list`, `help`, `commands`, `spells`, `autoquest`, `help caixa`.**
Exemplos literais:
- `commands` → `"Os seguintes comandos estão disponíveis em INGLÊS para você:"` + `( 1 de 3 )`
  (`automato/runtime/transcript_dia156_20261016_102159_08e293.jsonl:5958`).
- `list` do armeiro → `( 1 de 2 )` (`…123921_2cb7a0.jsonl:5498`).
- `help caixa` → `( 1 de 5 )` (`scripts/local/transcript_dia141_20261016_072801_5a9f49.jsonl:1272`).
- `data/heroes/grebolius/evidence/dia142.json:9`: *“‘autoquest todas’ e ‘help autoquest’ usam
  paginador; a listagem completa exige avancar as paginas.”* — **Provável**.

**Fato #6 — `config`/`pagelength` não aparecem em nenhum registro.** Busquei `pagelength`, `page
length`, `linhas de`, `ENTER`, `Pressione`, `config`, `colunas` em todo o workspace: as únicas
ocorrências reais são `term 22 80` (acima), a linha do paginador e o `\u0007`-aviso de DT. **Lacuna.**

---

## 2. Comandos — trechos literais

### 2.1 `score tudo` (formato completo observado)

`maquina/evidencias/consulta_2026-10-15.json:292-296`:

```text
Você é Grebolius, o Aprendiz de Mago.
 Você está em sua 1ª encarnação, como um Mago Elfo, nível 11.
 Você tem 17 anos, 2 meses, 19 dias e 4 horas.
 Você esteve jogando durante 0 dias e 15 horas.
 Você pesa 61,68kg e mede 1,39m.
 Você morreu 3 vezes e não caiu em nenhuma armadilha de morte.

[Pontos e atributos]------------------------------------------------------------
          Vida: {<<<<<>>>>>}  67 de 67
          Mana: {<<<<<>>>>>} 170 de 170
     Movimento: {<<<<<>>>>>} 101 de 101
   Experiência: {<<<<<>>>--} 152.098
 Próximo nível: {<<<<<>>>>>}  47.902           Pontos de aventura: 0
   Alinhamento: {<<<<<>----}   222 - Você é um pouco bom.
[Ouro e equipamentos]-----------------------------------------------------------
         Banco: {----------}   0
    Carregando: {<<<<<>>>>>} 612 - Total: 612
[Situação atual]----------------------------------------------------------------
 Você está em pé.
 Você se sente protegido.
[ Duração ]
 armor                 (   5 horas ) +25 em ARMADURA
```

Note que `help score` lista variantes (`pontos vida`, `pontos mana`, `pontos mov`, `pontos ouro`,
`pontos alinhamento`, `pontos estado`, `pontos autoquest`) em `docs/expedicao_comandos.md:53-89` —
**documentado, e a execução não foi registrada por variante**.

### 2.2 `exits` (formato exato em português)

```text
Saídas:
Norte - O Altar do Templo
Leste - A Sala de Doações de Midgaard
Sul   - A Praça do Templo
Oeste - A Sala de Leitura
Cima  - O Panteão dos Centenários
Baixo - A Praça do Templo
```
`automato/runtime/transcript_dia156_20261016_113245_1a4abb.jsonl:13`;
`data/heroes/grebolius/evidence/dia91.json:33` (quatro saídas); `dia95.json:137`.

Observação de campo: `Sul   -` traz **três espaços** (padding para 5 caracteres) e `Cima  -` dois.
Nas salas visitadas do Templo o `exits` veio **completo**, com as seis direções.

### 2.3 `consider`

`data/heroes/grebolius/evidence/dia93.json:665`:

```text
             Você  Oponente
   Nível:     11   Fácil!
    Vida:     87   É uma perda de tempo
   Poder:     25   É uma perda de tempo
Precisão:     18   Fácil!
Armadura:     50   Perfeito!
```

`scripts/local/transcript_dia100_20261016_000913_acc661.jsonl:110` traz a mesma tabela no nível 14
(`Vida: 75   Você é louco?` / `Armadura: 76   Perfeito!`). A escala de veredictos é qualitativa e
**não** coincide com o manual importado (`maquina/commands.md:438-452`: *“compare your Level with the
monsters level … does not take hitpoints … into account”*): no DeBo a resposta cobre **cinco** eixos.

### 2.4 `inventory` / `equipment`

```text
Você está carregando:
um cantil
um pão recheado
um bracelete de conchas (novo)(+44L)
(x3) um pergaminho de sabedoria
```
`maquina/evidencias/consulta_2026-10-15.json:369-373`. O formato de quantidade é `(x3) um …`, com o
`x` **antes** do número — confirmado também em `conhecimento.md:588-592`.

```text
Você está usando:
  na cabeça          -> a Coroa da Rainha Branca ..Isso emite um som estridente! (novo)
  no corpo           -> a Armadura da Torre Negra ..Isso tem uma pequena aura! (novo)
```
`automato/runtime/transcript_dia156_20261016_121159_9eb61a.jsonl:17`.

### 2.5 `wimpy`

```text
Certo, você irá se acovardar se você ficar abaixo de 17 pontos de vida.
```
`data/heroes/grebolius/evidence/dia91.json:40`. Depois da morte #4 o valor subiu: `… abaixo de 30
pontos de vida.` (`automato/runtime/transcript_dia155_20261016_092432_82c3eb.jsonl:5`). A recusa
acima da metade da vida só está registrada como relato (`dia113b.json:10`) — **Provável**.

### 2.6 `save`, `alias`, `tips`, `autoquest`

```text
save    -> Salvando os seus atalhos.
alias cxhelp_1817 -> Atalho apagado.
tips    -> Você verá as dicas do jogo.   (liga)
tips    -> Você não verá mais as dicas do jogo.   (desliga)
autoquest -> Certo, mas qual comando de autoquest?
             Digite AJUDA AUTOQUEST para ver as opções.
autoquest todas -> Autoquests do DeBo MUD
                   Problemas Agrícolas            Em andamento
```
Fontes: `maquina/evidencias/consulta_2026-10-15.json:432-437`, `:404-408`, `:299-303`, `:390-394`,
`:397-401`; `data/heroes/grebolius/evidence/dia91.json:264-265`; `dia156.json:29`.

A regra do `help save` (**Provável**, documentado pelo servidor) é importante para a crônica:
`maquina/evidencias/consulta_2026-10-15.json:280-288` — *“Você NÃO PODE carregar uma versão salva se
você morrer — seu personagem ainda existe, mas você irá perder pontos de experiência, e todos seus
objetos continuarão no jogo, em seu corpo.”*

### 2.7 `practice` / treino

```text
Você tem 40 sessões de treino sobrando.
Você conhece as seguintes magias e habilidades:
armor                 99%:   (perfeito)
burning hands         99%:   (perfeito)
lightning bolt        99%:   (perfeito)
```
`automato/runtime/transcript_dia156_20261016_121159_9eb61a.jsonl:62`. Fora da guilda:
`Você pode praticar somente em sua guilda.` (`:92`). Sequência de treino (`:124-130`):
`Você pratica por um tempo...` → `Você agora está instruído nessa área.` → `Você já está instruído
nessa área.`

### 2.8 Banco e lojas

```text
deposit 232   -> Você deposita 232 moedas.
balance       -> Você possui 7.032 moedas no banco.
list          ->  ##   Disponível   Item            Preço Nível Enc.
buy           -> O padeiro falou por telepatia com você: 'São 18 moedas.'
                 Você comprou um pão recheado (x 3).
sell          -> O armeiro falou por telepatia com você: 'Você receberá 500 moedas por isso!'
                 O lojista agora possui um anel arcano.
sell (recusa) -> O armeiro falou por telepatia com você: 'Isso é caro demais para mim - Tente um feiticeiro!'
value         -> O feiticeiro falou por telepatia com você: 'Eu não compro esse tipo de coisa.'
```
Fontes: `automato/runtime/transcript_dia156_20261016_102159_08e293.jsonl:31`;
`scripts/local/transcript_dia141_20261016_072801_5a9f49.jsonl:1331`;
`data/heroes/grebolius/evidence/dia92.json:382`; `dia93.json:215`;
`automato/runtime/transcript_dia156_20261016_121159_9eb61a.jsonl:256, 217, 33-35`.

Detalhe de comportamento do `buy` (**Testado**, relatado com o literal): `'buy pao de viagem' cobra 6
e entrega pao recheado - a loja casa so a primeira palavra; a palavra distintiva e necessaria.`
(`data/heroes/grebolius/evidence/dia156b.json:17`).

---

## 3. Movimento

### 3.1 Recusas de movimento

| Recusa | Literal | Fonte |
| --- | --- | --- |
| Sala bloqueada | `Você não pode ir por aí...` | `data/heroes/grebolius/evidence/dia91.json:103`; `dia94.json:1685`; `dia95.json:317`; `automato/runtime/transcript_dia156_20261016_102159_08e293.jsonl:2161` |
| Peso | `Você já está carregando muito peso e não pode pegar a bainha de Excalibur.` | `automato/runtime/transcript_dia156_20261016_121159_9eb61a.jsonl:47` |
| Dormindo | `Você não pode fazer isso dormindo.` | `automato/runtime/transcript_dia156_20261016_102159_08e293.jsonl:1145` |
| Postura "relaxado" | `Nah... você está muito relaxado..` | **Provável** — ver abaixo |
| Guarda de NPC | `O guarda te humilha e não deixa você passar.` | **Provável** — `conhecimento.md:607` |

**O caso "relaxado" é Provável, não Testado.** A frase
`Nah... você está muito relaxado..` existe apenas em **prosa e código**, nunca como transcrição:
- `data/heroes/grebolius/diretiva_de_jogo.md:67, 88, 110`
- `automato/README.md:160`
- `data/heroes/grebolius/evidence/dia123.json:7` (campo `stand_fix`, relato de causa-raiz)
- `automato/nucleo/guarda.py:21` (`FALHAS`), `automato/camadas/vigia.py:128`

Rodei `grep "relax"` em todo o workspace: **nenhuma ocorrência em `.log`/`.jsonl` de sessão**. A
causa-raiz está registrada como observada no Dia 123 e a correção (`wake; stand` antes de andar) está
em produção, mas o texto cru do servidor não sobreviveu no repositório.

### 3.2 Custo de movimento

Cada deslocamento em sala comum consome **1 ponto** de movimento, e a regeneração devolve o ponto
alguns segundos depois. Evidência por prompt consecutivo:

```text
87hp 170mn 100mv >  (após andar)
87hp 170mn 101mv >  (pouco depois)
```
`data/heroes/grebolius/evidence/dia91.json:33`; `automato/runtime/transcript_dia156_20261016_123921_2cb7a0.jsonl:37-38`
mostra o mesmo em sequência (`114mv` → `113mv` → `112mv`). **Provável** como valor *por setor*: nunca
fizemos um par isolado comando→mv com o setor anotado; o que existe é a leitura do prompt.

### 3.3 Água e natação

**Sem evidência de execução.** O que existe:
- `data/heroes/grebolius/ficha.md:78` — perícia `swim` (Nadar) em 95% (**Testado** como dado de ficha
  lida no jogo; ver `transcript_dia98_…ca2c00.jsonl:132`).
- Descrição de sala observada: `data/heroes/grebolius/mapa.json:5358` — *“O rio aparenta ser muito
  fundo, impossibilitando a entrada nele sem alguma embarcação (ou sem saber nadar).”*
- **Nenhuma** mensagem de "Você começa a nadar", afogamento, ou recusa por não saber nadar foi
  capturada. **Lacuna.**

### 3.4 Fugas

Testado, com o bloco completo em `data/heroes/grebolius/evidence/dia95.json:317`:

```text
Uma cobra te picou!
Você se sente muito doente!
…
Você sente que está muito fraco e tenta fugir!
O Canto Nordeste da Borda
[ Saídas: sul, oeste e !baixo ]
Você consegue fugir para o leste.
Você perdeu 1 ponto de experiência na sua fuga.
```

Três fatos encadeados e observados: (1) o **wimpy dispara sozinho** e anuncia
`Você sente que está muito fraco e tenta fugir!`; (2) a fuga pode ter sucesso
(`Você consegue fugir para o leste.`); (3) **fugir custa 1 ponto de experiência**
(`Você perdeu 1 ponto de experiência na sua fuga.`). Também `evolucao.md:1224` registra o mesmo
custo (195.201 XP). O veneno entrou como efeito visível no `score`
(`Você está envenenado!` + `poison ( 9 horas ) -2 em FORÇA`, `dia95.json:335`).

O manual importado (`maquina/commands.md:641-655`) fala que FUGIR funciona "SE existir uma saída
próxima viável" — e o custo em XP **não** está lá. A ajuda do DeBo
(`maquina/evidencias/consulta_2026-10-15.json:192-196`) também não menciona o custo.

---

## 4. Magias

### 4.1 Tabela de dano e mana observados

| Magia | Mensagem de acerto (literal) | Dano observado | Mana por conjuração | Fonte |
| --- | --- | --- | --- | --- |
| `magic missile` | `Certo.\nVocê observa com orgulho seu míssil mágico atingir o monstro novato! [2]` | 2, 4, 5, 6, 8, 9, 10, 11, 12, 13, 14, 15, 17 | **10** | `dia92.json:544`; `dia94.json:1145, 1208, 1217, 1289, 1487, 1568, 1595, 2063, 2090, 2135`; `scripts/local/transcript_dia97_…e1d2ac.jsonl:44, 64` |
| `magic missile` (erro) | `O míssil mágico voa pelos ares passando milhas distantes do monstro novato.` | 0 | 10 | `dia94.json:1208, 1496, 3269` |
| `burning hands` | `Certo.\nVocê queima um monstro agressivo com suas pequenas mãos quentes!   [33]` | 15, 18, 22, 30, 33, 36, 40 | **12–15** | `scripts/local/transcript_dia97_…e1d2ac.jsonl:48`; `transcript_dia100_…acc661.jsonl:116`; `transcript_dia98_…ca2c00.jsonl:146, 185` |
| `burning hands` (golpe fatal) | `Você queimou um monstro esfomeado até morte!` | — | 24 (leitura contaminada por regen) | `scripts/local/transcript_dia100_…acc661.jsonl:117` |
| `lightning bolt` | `O raio acerta um monstro esfomeado com impacto total! [48]` | 48, 53, 64, 68, **80** | **30** | `scripts/local/transcript_dia141_…5a9f49.jsonl:5479, 5483, 5491`; `automato/runtime/transcript_dia155_…82c3eb.jsonl:1849, 1856, 1881` |
| `lightning bolt` (golpe fatal) | `Seu raio transforma um monstro esfomeado em pedaços!` | — | 30 | `automato/runtime/transcript_dia155_…82c3eb.jsonl:1862` |
| `lightning bolt` (erro) | `Sua pontaria vai de mal a pior... seu raio erra um monstro agressivo!` | 0 | 15 (registro parcial) | `automato/runtime/transcript_dia155_…82c3eb.jsonl` |
| `armor` (sucesso) | `Certo.\nVocê sente alguém te protegendo.` | +25 a +30 de ARMADURA | **15** | `dia93.json:512` (170→152); `transcript_dia156_…123921_2cb7a0.jsonl:1537, 1591, 1603` |
| `invisibility` (sucesso) | `Você desaparece.` | — | ~15–25 | **Provável** — `conhecimento.md:561` |
| `visible` | `Você se torna visível novamente.` / `Você já está visível.` | — | 0 | `transcript_dia156_…123921_2cb7a0.jsonl:5292, 5633` |

Detalhes úteis, todos **Testado**:
- O **aperfeiçoamento por uso** é anunciado: `Você sente seu 'lightning bolt' melhorar.`
  (`scripts/local/transcript_dia141_20261016_072801_5a9f49.jsonl:5479`).
- O alvo inexistente é recusado com `Em que você deseja lançar a magia?` (milhares de ocorrências;
  ex.: `scripts/local/transcript_dia97_…e1d2ac.jsonl`, `automato/runtime/transcript_dia156_…08e293.jsonl`).
  Esse é um dos gatilhos da guarda de repetição (`data/heroes/grebolius/diretiva_de_jogo.md:110, 125`).
- Um nível ganho anuncia magia nova: `Você aprendeu a magia shocking grasp!`
  (`scripts/local/transcript_dia104_20261016_005512_d958b4.jsonl:202`).

### 4.2 `chill touch` e `shocking grasp`

**Não há dano observado registrado para nenhuma das duas** nos transcripts varridos.
- `chill touch`: só **Provável** — `maquina/aprendizados-cacada-92-93.md:9`: *“**Toque gélido** — Errou
  o zumbi e gastou 5 de mana. Resultado inconclusivo…”*
- `shocking grasp`: só **Provável/Dúvida** — entrou a 10% e subiu a 95% por treino
  (`dia156b.json:15`; `transcript_dia156_…9eb61a.jsonl:124-130`), e o projeto decidiu **não usar**
  (`data/heroes/grebolius/plano_aventureira.md:132`: *“`shocking grasp` está a 10% — não usar”*).

### 4.3 `sanctuary`

Só **Provável**. Não há conjuração registrada. O que existe é via **bastão**:
`scripts/local/transcript_dia101_20261016_003804_cd4a79.jsonl:154`:

```text
Objeto: 'o Cetro do Bispo Negro' Tipo: BASTAO
Este BASTAO conjura:  sanctuary
Cargas: 5 de 5.
```
e o mesmo cetro depois com `Cargas: 0 de 5` (`transcript_dia141_…5a9f49.jsonl:2516`). O manual
importado (`maquina/spells.md`) serve só de referência.

### 4.4 "Área sem magia": o Templo de Midgaard — **Testado**

`automato/runtime/transcript_dia156_20261016_123921_2cb7a0.jsonl` traz o par limpo:

```text
:91  look  -> "O Templo de Midgaard
              [ Saídas: norte, leste, sul, oeste, cima e baixo ]"
:96  cast 'armor'       -> "Certo.\nSua magia falha e desaparece."
:98  cast 'invisibility'-> "Certo.\nSua magia falha e desaparece."
:213 cast 'detect magic'-> "Certo.\nSua magia falha e desaparece."

:104 d     -> "A Praça do Templo"
:1591 cast 'armor' -> "Certo.\nVocê sente alguém te protegendo."   (113hp 245mn)
:1603 cast 'armor' -> "Certo.\nVocê sente alguém te protegendo."   (224mn)
```

O mesmo padrão aparece em `data/heroes/grebolius/evidence/dia113b.json:11`:
*“dentro dele ‘cast armor’ e ‘cast detect magic’ respondem ‘Sua magia falha e desaparece’. Na Praca do
Templo a armadura funcionou de primeira.”* E em `scripts/local/transcript_dia100_…acc661.jsonl:12`
(ao entrar no Paraíso / Templo, `cast 'armor'` falha com mana intacta: `mana_delta=0`).

**Caveat de confiabilidade:** como essa falha também acontece **fora** do Templo em outros registros
(`transcript_dia111_…fcd6da.jsonl:905-930`, ainda em outra sala), a leitura correta é: *"a falha
`Sua magia falha e desaparece` ocorre dentro do Templo de Midgaard, e a mesma magia funciona na Praça
do Templo, um passo abaixo"* — o que é **Testado** — sem concluir que a falha *só* ocorre lá.

### 4.5 Sala sem magia na **Loja de Magias** — **Testado**

```text
Você não consegue ler o pergaminho. As paredes desta sala parecem impedir você.
```
`scripts/local/transcript_dia106_20261016_010916_019cdd.jsonl:70`. Recitado **do lado de fora**:
```text
Você recita um pergaminho de remover maldições, que dissolve.
A Armadura da Torre Negra brilha em azul.
```
`:74`. Consistente com `data/heroes/grebolius/evidence/dia106.json:12` e `conhecimento.md:684-685`.

### 4.6 Invisibilidade bloqueia comércio — **Testado**

`automato/runtime/transcript_dia156_20261016_123921_2cb7a0.jsonl`:

```text
:5290  list  -> "O balconista do bar exclama: 'Não negocio com quem não vejo!'"
:5292  visible -> "Você se torna visível novamente."
:5498  list  -> " ##   Disponível   Item                                         Preço Nível Enc. …
                 1) 1  Um par de braçadeiras de novato  400  0  1
                 3) 2  A Armadura da Torre Negra      17.000 17 1
                 [ Aperte ENTER para continuar, S para sair ou número da página ( 1 de 2 ) ]"
```

Ou seja: a recusa, o comando de saída (`visible`) e a lista funcionando **depois** de ficar visível
estão todos em transcrição crua. `visible` num estado já visível responde
`Você já está visível.` (`:5633, 5679, 5685, 5845, 5991, 6056`).

### 4.7 Custo de mana — divergência interna do projeto (**Dúvida**)

- `data/heroes/grebolius/conhecimento.md:569` diz: *“Cada magia custa **~25 de mana** (260 → 245 → 220
  com armadura + invisibilidade).”*
- As transcrições mostram **15** por `armor`: `260 → 245` (`transcript_dia156_…123921_2cb7a0.jsonl:1537`,
  `:1603` mede `239 → 224`, também 15) e `200 → 185` (`scripts/local/transcript_dia100_…acc661.jsonl`).
- `data/heroes/grebolius/ficha.md:110` repete o número errado: *“Armadura e invisibilidade custam ~25
  de mana cada”*.

São **duas fontes do projeto divergindo do registro**: a prosa arredonda para ~25 enquanto o próprio
par de prompts citado na mesma frase (260→245→220) implica 15. O número observado é **15** para
`armor`; `magic missile` 10; `burning hands` 12–15; `lightning bolt` 30. Fica como **Dúvida** no que
diz respeito a `invisibility` (não isolei um par limpo antes/depois).

### 4.8 Duração percebida de `armor` / `invisibility` / `sanctuary`

- **Provável.** A duração de `armor` (25→30 h de jogo) foi cronometrada indiretamente pela seção
  `[ Duração ]` do `score`, que decresce: `5 horas` → `4 horas` → `3 horas` na mesma sessão
  (`maquina/evidencias/consulta_2026-10-15.json:296, 317, 331`) e até `51 horas`
  (`data/heroes/grebolius/evidence/dia95.json:335`).
- A escala do relógio de jogo — **~75 s reais por hora de jogo**, medida com `time` (61 s e ~78 s em
  duas transições) — está em `conhecimento.md:641`, mas **o comando `time` não aparece em nenhuma
  transcrição varrida**. **Provável.**
- **A mensagem de expiração de `armor`/`invisibility`/`sanctuary` não existe em nenhum registro**
  (`conhecimento.md:652-654` declara explicitamente essa lacuna). O `cuidar.py` re-conjura a cada 25
  minutos justamente por não haver mensagem. **Lacuna.**
- O manual de `armor` no DeBo (`maquina/evidencias/consulta_2026-10-15.json:234-238`) diz
  `Efeito : -20 - nível(conjurador)/2`, `Duração: 24 horas`, `Nível: Clérigo 9, Mago 7, Paladino 1`:
  o **sinal negativo** no cabeçalho contradiz a prosa (“aumenta a classe de armadura”) e o
  `+25 em ARMADURA` observado. `maquina/comparacao_commands.md:10` já registra essa divergência.
- O `help invisibility` local (`consulta_2026-10-15.json:248-252`) diz `Mago nível 6`,
  `Duração: (6 + nível/4) h`, `+40 AC`, e que **atacar quebra o efeito** — todos **Prováveis**
  (documentado, não medido).

---

## 5. Morte e ressurreição

### 5.1 Bloco literal da morte #4 (Dia 100) — **Testado**

`scripts/local/transcript_dia100_20261016_000913_acc661.jsonl:126`:

```text
Um monstro agressivo acerta sua cabeça com um golpe que esmaga seu crânio!
Você está morto!
Você perdeu 1.435 pontos de experiência pela sua morte.
*Você falhou em suas aventuras! Se quiser concluí-las deverá recomeçá-las!*
                            B o b  d o  D i a c h o
                                 Menu Principal
          Você é Grebolius, Mago Elfo, nível 14
   .-.     Tecla
 __|=|__   [ 1 ] Entrar no jogo
(_/`-`\_)  [ 2 ] Ler a história do mundo de Devil's Bob
…
< Faça a sua escolha >
```

Isso resolve três coisas de uma vez: (a) a mensagem exata da morte; (b) a **perda de 1.435 de
experiência** — o número que `observacoes/morte-04-dia-100.md:25` só registrava em prosa; (c) a
mensagem *“Você falhou em suas aventuras!…”* **pertence à morte**, e o mesmo texto reaparece no `quit`
(`data/heroes/grebolius/evidence/dia156.json:31`). `data/heroes/grebolius/missoes.md:46` atribui a
frase corretamente à morte, mas quem consultar o `dia156.json` pode ler como mensagem de saída —
**as duas leituras são verdadeiras**, e isso fica registrado aqui para evitar ambiguidade futura.

### 5.2 O que a morte faz com a personagem — **Testado**

`scripts/local/transcript_dia100_20261016_000913_acc661.jsonl:132`: após escolher `1` no menu:
```text
Seja bem vindo!

* Para obter ajuda sobre como ressussitar, digite AJUDA MORTE. *

 * Você morreu pois caiu em uma armadilha mortal, digite AJUDA ARMADILHA para saber mais. *

O Paraíso
   Magníficos campos verdes estendem-se por uma eterna imensidão…
[ Saídas: norte, leste, sul e oeste ]
Conecte-se novamente em 9 horas, 9 minutos e 42 segundos para progredir na missão Todo Dia um Pouco.

< Morto >
```
Observações **Testadas** deste bloco: (1) após a morte o jogador cai no **Menu Principal** e precisa
digitar `1`; (2) existe um **cooldown expresso em horas/minutos/segundos** exibido ao entrar;
(3) a personagem renasce no **Paraíso** com o prefixo `< Morto >` na sala; (4) a mensagem de
armadilha mortal é exibida nesse retorno.

Outras leituras na mesma sessão, todas no Paraíso:
- `:134` — `score tudo`: `Você morreu 4 vezes e caiu em 1 armadilha de morte.` e, em
  `[Situação atual]`, `Você está morto!`.
- `:138` — `n` → a descrição traz `Uma curiosa energia mágica, muito viva e tenaz, chama sua atenção
  para o oeste.`
- `:140` — `exits` → `Oeste - Um Portal Escondido no Paraíso`.
- `:141` — `w` → `Um Portal Escondido no Paraíso` … `Um brilhante portal foi aberto aqui.`
- `:137`/`:143` — `exits` antes/depois mostra as quatro direções do Paraíso apontando para si mesmo.

A etapa seguinte (portal → Caminho no Vazio → Fonte da Vida → `drink fonte` → renascer no Templo com
metade da vida) está em `conhecimento.md:474` e em `scripts/local/exit_paraiso_log.txt:10-60`
(`O Paraíso` → `Um Portal Escondido no Paraíso`), mas **sem a linha final de renascimento isolada**:
**Provável**.

### 5.3 Aviso de armadilha mortal (DT) — **Testado**

`data/heroes/grebolius/evidence/dia95.json:23`:
```text
A Borda Estreita
   … Há uma outra saída daqui, mas leva diretamente para o meio-ar …
\u0007Você percebe que há algo perigoso por perto!
[ Saídas: norte, leste e sul ]
```
O `\u0007` (BEL) **precede** o aviso — é o alerta sonoro da DT. Confirmado como a única defesa em
`conhecimento.md:471-472` (*“DT mata direto, sem wimpy”*, com `help death`) e
`data/heroes/grebolius/diretiva_de_jogo.md:51-55`.

### 5.4 O inventário **não** é perdido na morte

Testado por ausência + relato. `observacoes/morte-04-dia-100.md:25` diz que o equipamento foi
**desequipado** (não perdido) e recuperado com `wear all`; o `help save` do servidor
(`consulta_2026-10-15.json:280-288`) diz que os objetos **continuam no jogo, em seu corpo**. Não
encontrei o `score`/`inventory` imediatamente pós-morte em transcrição para provar item a item:
**Provável**.

### 5.5 Contagem de mortes

`3` (Dia 91) → `4` (Dia 100, com 1 DT) → `5`, `6`, `7` (resumos dos Dias 113, 118, 126) e
`Você morreu 7 vezes e caiu em 1 armadilha de morte.` em
`automato/runtime/transcript_dia156_20261016_102159_08e293.jsonl:2333`. **Testado** como valor de
`score`; a atribuição de cada morte a um Dia vem das evidências de dia (**Provável** no detalhe).

---

## 6. Regras do DeBo × CircleMUD importado

| Tema | Manual importado (CircleMUD) | DeBo observado | Confiança |
| --- | --- | --- | --- |
| Idioma dos verbos | Exemplos em inglês | `identificar anel` → `Como?!?`; `identify anel` funciona | **Testado** (`consulta_2026-10-15.json:306-310, 320-324`) |
| Comando `term` | **Não existe** em `commands.hlp` | `term 22 80` funciona e responde | **Testado / Dúvida** de origem |
| Comando `term`/paginação | Sem verbete | `[ Aperte ENTER para continuar, S para sair ou número da página ( 1 de N )     ]` | **Testado** |
| `consider` | Compara só nível | Compara nível, vida, poder, precisão e armadura | **Testado** (`dia93.json:665`) |
| `offer` | Cotação de hospedagem (`OFFER RENT`) | `help offer` devolve `OFERENDA` (sacrifício de cadáver, 50 XP) | **Provável** (`consulta_2026-10-15.json:262-266`) |
| `circle` | Tópico sobre o CircleMUD em `info.hlp` | `help circle` devolve a habilidade `CIRCLE AROUND` | **Provável** (`comparacao_commands.md:15`) |
| `sacrifice` | Existe no mundo padrão | `'Voce nao tem ideia de como fazer isso'` | **Provável** (`dia156b.json:18`) |
| `autogold` | Comando de toggle do engine | Existe na lista (`commands`), sem execução capturada | **Dúvida** |
| AC | Escala negativa, menor é melhor | `A cada 10 pontos de armadura, o dano recebido é reduzido em um ponto`; `armor +25`, AC 44 sem armor | **Testado** (ajuda + `score`) |
| `quit`/`save` | Descreve necessidade de rent para guardar equipamento | `help quit` diz que os itens permanecem com você; `save` → `Salvando os seus atalhos.` | **Testado** |
| Fuga | Descreve só a condição de saída viável | Fugir **custa 1 XP** | **Testado** (`dia95.json:317`) |
| Ajuda `autoquest` | Ausente no `commands.hlp` | `help autoquest` funciona; `ajuda autoquest` é recusado com `Como?!?`-like/`Certo, mas qual comando…` | **Testado/Provável** (`dia91.json:264-285`) |

A camada de regras **específicas do DeBo** que apareceu com resposta real:
`help armor` (`consulta_2026-10-15.json:234-238`), `help invisibility` (`:248-252`),
`help identify`/`IDENTIFICAR` (`:59-64`, `:241-245`), `help offer`/`OFERENDA` (`:262-266`),
`help tip` (`:122-126`), `help look` (`:24-28`), `help exits` (`:31-35`), `help score`/variantes
(`docs/expedicao_comandos.md:53-89`), `help autoquest` (`dia91.json:284-285`).

As regras **importadas do CircleMUD** continuam sendo `maquina/commands.md` (99 verbetes),
`maquina/info.md` (19 verbetes) e `maquina/spells.md` (44 verbetes) — ver `maquina/fontes.json` para os
hashes. Nenhum deles certifica comportamento no DeBo.

---

## 7. Contradições e incertezas encontradas

1. **Custo de mana por magia.** `conhecimento.md:569` e `ficha.md:110` dizem ~25 por `armor`;
   as transcrições medem **15**. Registrado como **Dúvida** em §4.7.
2. **`Você falhou em suas aventuras!…`** aparece **na morte** (`transcript_dia100_…acc661.jsonl:126`)
   e **no `quit`** (`dia156.json:31`). Quem ler apenas um dos dois pode atribuir a frase ao gatilho
   errado. **Dúvida resolvida** — o texto serve aos dois.
3. **`term` vs. `commands.hlp`.** O comando existe no DeBo e não existe no manual importado:
   confirma que `commands.md` é referência de engine, não catálogo do servidor. **Dúvida de origem.**
4. **`exits` desalinhado.** Há leituras em que o `exits` devolve dica, evento, recusa ou a descrição
   de outra sala (`08e293.jsonl:2117, 2161, 2382`; `123921_…jsonl:1615`). O projeto tratava isso como
   "resposta cortada"; a evidência mostra que é **resposta deslocada/errada**, não truncada por
   largura. **Dúvida** entre as duas leituras — a regra prática (cruzar com a linha de colchetes do
   `look`) continua válida.
5. **`Nah... você está muito relaxado..`** é dado como resposta observada em
   `diretiva_de_jogo.md:67, 88` e `dia123.json:7`, mas **não existe em nenhum log/transcrição** do
   workspace. Ou o registro bruto foi perdido, ou a frase foi parafraseada. **Dúvida.**
6. **Sala sem magia não é privilégio do Templo** (`conhecimento.md:684`): a Loja de Magias também
   bloqueia. E `cast armor` falhou também fora do Templo em `transcript_dia111_…fcd6da.jsonl:905-930`.
   Não confundir "o Templo bloqueia" (Testado) com "só o Templo bloqueia" (não provado).
7. **`maquina/tips.md:5`** afirma que os Dias 90 e 91 não registraram linhas `DICA:` — mas
   `data/heroes/grebolius/evidence/dia91.json` **contém** ao menos uma
   (`DICA: Atalhos são de grande ajuda…`, `dia93.json:341` e `dia92.json:157, 265, 310, 364, 454,
   517, 634, 715, 850, 976, 1048, 1138, 1228, 1300, 1372, 1453, 1534, 1651`). A afirmação é sobre os
   registros consultados à época e pode ter sido feita sobre outro recorte — mas a divergência entre
   `maquina/tips.md:5` e as evidências do dia é **real** e fica marcada como **Dúvida**.
8. **Morte #6/#7 e `armadilha de morte` = 1.** `evolucao.md` e `capitulos.json` dizem que as mortes
   #5, #6 e #7 foram por armadilha mortal, mas o `score` do Dia 156 mostra
   `caiu em 1 armadilha de morte` (`08e293.jsonl:2333`). Ou o contador não incrementa como o projeto
   supõe, ou as mortes #6/#7 tiveram outra causa. **Dúvida.** (`conhecimento.md:471` já havia notado
   que, na morte #5, *“a contagem de armadilhas do servidor continuou em 1”*.)

---

## 8. Lacunas — o que **não** tem evidência registrada e precisa de teste ao vivo

Complementa e atualiza o protocolo de `docs/circlemud/00-afirmacoes-e-validacao.md:30-67`.

**Terminal**
1. `term` **sem argumento** — mostra o tamanho atual? (nunca executado)
2. `term 60 200` — aceito? reduz páginas? (nunca executado; é o teste nº 2 de `00-…md:37`)
3. Qualquer resposta **cortada por largura** de 80 colunas (nenhum caso encontrado)
4. `config`, `pagelength`, `page` — não existem em nenhum registro

**Comandos**
5. `prompt` / `prompt <formato>` — o comando nunca foi enviado; só temos o prompt padrão
   `NNhp NNmn NNmv >` (o teste nº 5 de `00-…md:40` continua aberto)
6. `display hv | all | auto | off` — documentado, nunca executado
7. `alias <nome> <comando>` **criando** atalho (só apagar foi testado)
8. `autogold` — existe na lista, nunca executado
9. `diagnose`, `train`, `time`, `where`, `weather`, `gold`, `donate`, `junk`, `quaff` — zero execuções
   registradas nos transcripts varridos
10. `offerenda` / `oferenda <corpo>` — nunca executado; o texto de ajuda promete 50 XP por corpo
11. `sit` — não há resposta isolada de `sit` (só `rest`, `sleep`, `wake`, `stand`)
12. Variantes de `score` (`pontos vida`, `pontos ouro`, `pontos autoquest`) — nenhuma registrada
13. `exits` repetido N vezes na mesma sala para medir a taxa de resposta desalinhada (§7.4)

**Movimento**
14. A frase exata da recusa por postura "relaxado" (e se ela é mesmo `Nah... você está muito
    relaxado..`) — **nenhuma transcrição no workspace**
15. Custo de movimento **por setor** (estrada, esgoto, floresta) com par comando→`mv` isolado
16. Natação: `swim`, "Você começa a nadar", afogamento, recusa por não saber nadar
17. Esgotamento de movimento ("você está exausto") — nenhuma mensagem capturada
18. Portas: `open`/`close`/`lock`/`unlock` e a recusa literal de porta trancada (só vimos o `!` na
    linha de saídas e a recusa genérica `Você não pode ir por aí...`)
19. `flee` explícito (o que existe é a fuga automática do wimpy e um "Você consegue fugir para o
    leste.")

**Magias**
20. `chill touch` — dano, custo e mensagem (só "errou e gastou 5 de mana", em prosa)
21. `shocking grasp` — dano e custo (nunca conjurado em combate registrado)
22. `sanctuary` — conjuração direta, custo, duração e mensagem (só via bastão com cargas)
23. `invisibility` — par limpo antes/depois de mana; e a mensagem de **expiração**
24. `armor` — mensagem de expiração (declaradamente inexistente em `conhecimento.md:652-654`)
25. Mensagem de **resistência** de monstro a magia (nenhum caso capturado)
26. `cast` contra objeto (só contra criaturas)
27. Dano de `burning hands`/`magic missile` em série controlada (10 conjurações no mesmo alvo) —
    a faixa atual vem de alvos mistos e níveis diferentes
28. Se a falha `Sua magia falha e desaparece` ocorre **fora** de salas sem magia (há indício de sim em
    `transcript_dia111_…fcd6da.jsonl:905-930`)

**Morte**
29. O que exatamente acontece com **itens equipados vs. carregados** na morte (item a item)
30. `AJUDA MORTE` e `AJUDA ARMADILHA` — citados pelo servidor na tela de retorno, nunca consultados
31. A tela completa de renascimento (`drink fonte` até "renasceu no Templo com metade da vida")
32. Se o cooldown de reconexão (`9 horas, 9 minutos e 42 segundos`) é regra fixa ou variável
33. Contador de armadilhas: por que ficou em `1` apesar de várias mortes descritas como DT

**Servidor / crônica**
34. `help death` e `help diretrizes` — o texto integral das regras declaradas pelo DeBo
35. `bug`/`typo`/`idea`/`errata`/`md`/`quem`/`autoexit`/`brief`/`compact`/`toggle` — existem nos
    registros de ajuda/dica, sem execução capturada
36. `identify` no **nível 80 exato** da primeira encarnação (o limite entre o comando e a magia)
37. Qualquer mensagem de `identify` recusando item **vestido** — o relato
    (`maquina/verificacoes.md:27`: *“recusou itens ainda vestidos (‘Você não tem nenhum…’)”*) não tem
    transcrição localizada

---

## 9. Como usar este documento

- Para a crônica: só as linhas **Testado** podem ser afirmadas como fato de servidor; as **Provável**
  entram como entendimento da máquina, nunca na voz da personagem.
- Para o próximo teste autorizado: a seção **Lacunas** é a fila de trabalho; o protocolo de
  `docs/circlemud/00-afirmacoes-e-validacao.md:30-67` continua sendo o roteiro.
- Para corrigir: quando uma resposta real divergir daqui, registrar data, comando, alvo, condição,
  resposta literal e fonte, e corrigir apenas a linha afetada — mantendo as citações `arquivo:linha`.
