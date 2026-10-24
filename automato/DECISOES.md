# Por que mudamos, o que mudamos, e os próximos desafios

Cada entrada responde a três perguntas: **por que** (o problema real), **o que** (a mudança) e
**o custo** (o que se perdeu). A intenção é que outro agente entenda a decisão sem repetir a dor.

---

## 1. A guarda de repetição (v0.2, Dia 143)
- **Por que**: as mortes #5, #6 e #7 vieram de scripts **insistindo** num estado travado — sala bloqueada,
  alvo que não existia, personagem descansando. O robô não sabia desistir.
- **O que**: mesma resposta **3× seguidas** → imprime o texto repetido, `recall` + `save`, sai (código 9).
  Correção posterior: comandos **benignos** (comprar, comer, beber, olhar, score) não disparam.
- **Custo**: o robô para antes de "insistir" — exige que **alguém olhe** o motivo. É de propósito.
- **Próximo desafio**: distinguir repetição **útil** (meditar) de **travada**.

## 2. O ouro dorme no banco (v0.4, Dia 148)
- **Por que**: as mortes levavam ouro; ela carregava 7.000+ no bolso por dias.
- **O que**: o `prepara.py` deposita tudo acima de **300** (`deposit` no Templo).
- **Custo**: sacar de novo dá trabalho quando surge uma compra grande (ex.: pergaminho de 8.509).
- **Próximo desafio**: calcular automaticamente **quanto guardar** conforme o próximo objetivo.

## 3. O vigia lê o log, não o jogo (v0.4, Dia 148)
- **Por que**: monitorar mandando `score` enquanto a rotina roda **desincroniza a sessão** — foi assim que
  perdi rodadas achando que a rota estava errada.
- **O que**: o vigia lê a **cauda do log do driver** (leitura pura) e devolve um diagnóstico simples.
- **Custo**: só vê o que o driver já registrou (não pergunta nada novo).
- **Próximo desafio**: sinais mais finos — "preso na mesma sala há N minutos".

## 4. Proibido vender armaduras (v0.5, Dia 150 — diretiva do autor)
- **Por que**: a conta não fechava. O armeiro tem **caixa finito** (`3 armaduras de 8.500 e seca), a armadura
  da Torre pesa **60 kg** e é **amaldiçoada**, e desamaldiçoar custa **8.509** para vender por **8.500**.
- **O que**: nenhuma rotina de armaduras; a `xadrez` foi **suspensa** para `rotinas/_suspensas/` com LEIA-ME.
  O ouro passa a vir de **espólio de combate, recompensa de missão e do banco**.
- **Custo**: perde-se a única renda "garantida" conhecida.
- **Próximo desafio**: achar **outra** fonte de ouro.

## 5. Rota determinística em vez de sorteio (v0.6, Dias 152-154)
- **Por que**: gastei `6 rodadas com o bosque culpando o parser, quando o erro era **meu**: eu usava
  `norte, norte, leste, leste` onde o mapa dizia **`norte, norte, leste, sul`**, e
  `oeste, sul, oeste, oeste, oeste` onde eram **três oestes**.
- **O que**: a rota Templo→Milharal foi extraída **do mapa** e escrita no `conhecimento.md` §24; a rotina
  passou a andar por **marco de sala**, nunca por contagem.
- **Custo**: a rota depende do mapa — e ele **não está** atualizado em pelo menos um ponto
  (a Divisão da Trilha leva a *Uma Parte Densa*, não direto ao Bosque).
- **Próximo desafio**: **revalidar o mapa** sala a sala enquanto se joga, anotando as divergências.

## 6. Magia certa, alvo certo (v0.6, Dia 153)
- **Por que**: as mãos flamejantes faziam `25 de dano e os monstros fugiam antes de morrer; o alvo
  genérico ("monstro") falhava contra "monstro agressivo".
- **O que**: **lightning bolt** (95%) como magia principal (48-64 de dano, e a habilidade ainda sobe
  com o uso) e **nome exato** do monstro como alvo, com plano B.
- **Custo**: 40+ de mana por golpe — exige a recarga por sono antes de cada saída.
- **Próximo desafio**: medir **mana por abate** e decidir quando usar a magia de reserva.

---

## 7. O automato passou a ser autossuficiente (v1.1, Dia 155)
- **Por que**: o automato dependia de arquivos fora dele (o driver, os parsers, a ressurreição), então
  outro agente não conseguia rodá-lo "pegando a pasta" — e as rotinas liam texto vazio quando o token
  estava em outro caminho.
- **O que**: o **driver completo** foi para `automato/nucleo/driver/` (debo_bot, parsers, live_daemon, play);
  os **segredos e logs** para `automato/runtime/` (fora do git); a ressurreição para `automato/acoes/`; e
  `config.py` passou a apontar os **documentos do herói** (`conhecimento.md`, `diretiva_de_jogo.md`, `mapa.json`)
  como conhecimento **referenciado** — não copiado.
- **Custo**: subir o driver virou um passo obrigatório antes de qualquer camada, e reiniciá-lo abre uma
  sessão nova no MUD.
- **Próximo desafio**: um `automato/setup.py` que valide ambiente (Python, rede, token, senha) e suba o driver sozinho.


## 8. Todo agente se identifica (v1.3, Dia 155)
- **Por que**: o automato agora é feito para **outros agentes** usarem e ajustarem. Com mais de um
  mexendo no mesmo jogo, não dá para saber quem mudou o quê — nem comparar modelos.
- **O que**: obrigatório declarar **modelo e versão** no começo do relatório, no campo `agent` dos
  arquivos de evidência e na mensagem do commit (`[agente: <modelo/versao>]`).
- **Custo**: uma linha a mais em cada registro.
- **Próximo desafio**: uma tabela comparando o desempenho de cada modelo nas mesmas rotinas.


## 9. A missão fala a palavra dela — e a fonte é o transcript (Dia 156)

- **Por que**: no Dia 156, **dois agentes jogaram o mesmo capítulo e chegaram a resultados opostos**, e a
  diferença não foi de habilidade — foi de **método de leitura**.
  - O `deepseek-flash` tratou o objetivo *"Você deve dizer algo ao personagem"* como **enigma**: inventou
    ~35 frases (`say novela`, `say oi novato`, `say conte sua historia`…), 9 tópicos de `ask`, 3 itens com
    `give`, em 4 dos 5 novatos. **Nenhuma funcionou**, e ele concluiu que faltava "o NPC falar primeiro".
  - O `GPT-6 / Codex` **leu o transcript** e achou a fala que o novato **já tinha dito**: a instrução
    **`ajuda mapas`**, gravada nas **linhas 5535–5562 do transcript da sessão anterior**. A cadeia real era
    `ajuda mapas` → `diretrizes` → *levar a veste à tagarela* → `retornar` → **`ajuda remortar`**.
  - **O primeiro agente tinha o arquivo aberto. Não leu.** É a diferença entre *ajuda* e *teste executado*
    que o `AGENTS.md` §4.1 já exigia — agora com custo medido.
- **O que**: a doutrina de leitura entra no método, em três regras:
  1. **O diálogo de missão é literal.** O NPC diz a palavra, e você repete **a palavra dele** — não o seu
     sinônimo. `say retornar` foi reconhecido pelo confuso; `say recall` **não**. `ajuda remortar` foi
     reconhecido; `ajuda encarnação` **não**.
  2. **Ler o transcript, não a síntese.** Fala espontânea de NPC não se perde: ela está gravada. Resumo é
     interpretação; transcript é fonte.
  3. **`score tudo` antes de cada fala e cada entrega.** O objetivo **muda** conforme a etapa, e ação antes
     da hora **não conta** — uma veste entregue cedo demais saiu do inventário sem avançar; a segunda
     entrega, com a etapa pedindo, gerou *"Você atingiu seu objetivo"*.
- **Custo**: ler transcript é lento e chato, e o método "tentar frases" é mais divertido de escrever. O
  custo real já foi pago: **seis rodadas** procurando o novato esperto cuja sala (**18645**) estava nos
  `docs/circlemud/` desde o começo, e uma **crônica publicada errada** que outro agente teve de corrigir.
- **Ganho colateral**: `where <nome>` localiza monstro/jogador **dentro da sua área** — comando que existia
  e que o primeiro agente nunca procurou, porque nunca leu `help` de forma ampla. E `autoquest todas` é
  **histórico**: marcava *Limpando Monstros* concluída enquanto o ciclo reiniciado ainda pedia o Minotauro.
  **O catálogo não é prova de conclusão; o `score` é.**
- **Próximo desafio**: uma camada que **extraia as falas de NPC do transcript automaticamente** e as
  apresente antes da sessão — para que "ler a fonte" deixe de depender de disciplina e vire ferramenta.


## Os próximos desafios (revisados no Dia 156)

> A lista anterior pedia *"localizar os NPCs de Novela dos Novatos (o novato esperto, nas praças)"* — e
> **estava errada**: ele não anda pelas praças, ele é o **`Smart Newbie` (18615)**, na sala **18645 = A
> Sacada**, e os `docs/circlemud/` diziam isso desde o começo. A Novela está **concluída**.
> **CORREÇÃO (Dia 156, mesma data):** a linha abaixo dizia que *"Problemas Agrícolas"* estava **vetada**.
> **O veto CAIU.** O autor deu a missão ao próximo agente — *"vamos dar a missão para o próximo agente e
> ver se ele consegue fazer a do Problemas Agrícolas"*. Ela é o objetivo do **Capítulo 07**, e o plano é
> o **`planos/plano008.md`**. **Onde ainda se ler "vetada", está desatualizado.**
>
> *"Problemas Agrícolas"* foi **vetada pelo autor** e saiu da lista. *(VETO REVOGADO — ver acima.)*

1. **Abrir as 33 portas nomeadas** do Capítulo 04 — nunca abertas, e o Capítulo 05 as contornou duas vezes.
2. **Jareth e a Avenida Floris** — rota conhecida e verificada, **nunca percorridas**.
3. **Pontos de Aventura → a loja dos deuses** (`autoquest loja`): as proteções **ANTI-DT** e **IMUNE-DT**
   são a única defesa contra a armadilha que o `wimpy` não segura.
4. **Uma Lição em Gargamel** (*o smurf minerador*, sem pista) — a única iniciadora ainda não localizada.
   **Comece pelos `docs/circlemud/` e pelo `where`**, não varrendo o mundo.
5. **Decidir o destino da Armadura da Torre Negra** (amaldiçoada): carregar (grátis, mas sem espaço) ou
   pagar **8.509** para desamaldiçoar e doar (libera 60 kg).
6. **Extrair as falas de NPC do transcript automaticamente** (ver §9) — para que ler a fonte deixe de
   depender de disciplina.

## Como outro agente deve continuar
- Leia o `README.md` primeiro (a arquitetura e o contrato);
- Mude **só** `nucleo/config.py` para adaptar a outro projeto/heroi;
- **Nunca** rode rotina sem vigia e sem supervisão (ver os invariantes no README);
- Registre cada mudança aqui e no `CHANGELOG.md` — o próximo agente continua de onde você parou.


## 2026-10-17 — retomada011: confirmar contexto antes de agir

Agente: GPT-6 / Codex (versão específica não informada); fonte: data/heroes/grebolius/evidence/dia156j.json. Decisão: cruzar resposta com sala-marco,vitais,objetivo e falas em idle/preroll; não confiar em prompt isolado ou palavra morte em histórico como morte vigente. Exemplo: recompensa sob eat pao e saídas sob n no transcript72663a. Alertas/guardas temporários são de worker no workspace; nenhum reparo geral do motor foi aplicado. Custo: consultas adicionais e interrupção manual em ambiguidade. Seguir AGENTS§13 para retirada/handoff ao atingir10% da janela5h.


---

## 10. Diálogos de missão NUNCA automatizados — resposta direta do agente ao vivo (Dia 156 — diretiva do autor)

- **Por que**: Scripts que automatizam conversas com NPCs (`say sim`, `say Grebolius`, `give`) com tempos arbitrários de espera (`time.sleep`) repetidamente causaram falhas graves: atropelam falas longas de NPCs antes do término, ativam quests concorrentes na mesma sala (ex.: ativar *Limpando Monstros* ao invés de avançar *Gargamel*) e entregam itens antes de o NPC registrar o diálogo correto, consumindo itens raros e ouro sem conceder a recompensa.
- **O que**: Fica expressamente **proibido** automatizar falas e entregas de missão em scripts em lote (`automato/acoes/` ou `automato/rotinas/`). O motor apenas navega até a sala do NPC e garante a segurança física. A conversa, a leitura atenta da fala do NPC, a conferência de `score tudo` e a entrega de itens devem ser feitas **diretamente pelo agente consciente em resposta ao contexto em tempo real**.
- **Custo**: Exige que o agente conduza pessoalmente a interação social passo a passo em cada etapa de missão, impedindo a execução autônoma "às cegas" durante conversas e entregas.
- **Próximo desafio**: Adaptar scripts de apoio em `automato/acoes/` para atuarem apenas como navegadores/posicionadores e limpadores de sala, deixando comandos de `say` e `give` para o terminal ao vivo do agente.


---

## 11. Guarda de Cota Inteligente e Handoff Automatizado (v1.6.7, Dia 156 — diretiva do autor)
- **Por que**: A diretiva do AGENTS.md §13 determina que o agente interrompa ações e faça handoff ao atingir 10% da janela de 5 horas. Porém, checar a cota manualmente a cada 5 minutos pelo operador consome foco, e checagens excessivas por script geram tráfego desnecessário no language server.
- **O que**: Criado o módulo `automato/camadas/guarda_cota.py` que consulta o endpoint local RPC do Antigravity com frequência adaptativa (a cada 35 min se cota > 40%; a cada 10-15 min se entre 20%-40%; a cada 1-5 min se próxima de 10%). Ao bater <= 10% (tolerância 5%-10%), o automato aborta a caça, recolhe a personagem com segurança no Templo, alimenta, hidrata, salva, deita, fecha a conexão e gera o próximo plano numerado de handoff.
- **Custo**: Uma consulta local HTTP a cada 10-35 minutos; em falha de conexão com o server, o script registra aviso e não interrompe bruscamente o bot.
- **Próximo desafio**: Monitorar a taxa de consumo por ciclo (burn rate de tokens/hora) para prever o momento exato do corte.

---

## 12. Monitoramento de Weekly Limit (< 5%) além do Diário (< 10%) na Guarda de Cota (v1.6.13, Dia 156 — diretiva do autor)
- **Por que**: Modelos como Gemini possuem limites com janelas semanais (~7 dias / ~130h de reset) além ou no lugar de janelas curtas de 5 horas. Se o corte fosse fixado rigidamente em 10% para uma janela semanal, o bot pararia prematuramente quando ainda restava considerável volume de requisições utilizáveis; ao mesmo tempo, se a cota semanal chegasse a zero, o agente ficaria travado por dias. A diretiva do autor estabeleceu: *"se tiver abaixo de 5%, faz o mesmo que faz hoje quando o diário está acabando"*.
- **O que**: Atualizado `automato/camadas/guarda_cota.py` e `scripts/checar_cota.py` para distinguir automaticamente janelas semanais (> 24h até o reset) de janelas curtas/diárias (<= 24h). Para janelas semanais, o corte crítico de handoff é acionado em `<= 5%` (0.05); para diárias, mantém-se em `<= 10%` (0.10). O handoff executa o mesmo protocolo seguro (recall, pão, cantil, save, sleep, fechamento de socket e plano numerado documentando se foi semanal ou diário).
- **Custo**: Nenhum. Melhora o aproveitamento seguro do saldo do modelo e protege contra esgotamento semanal.


---

## 13. Catraca do padrão entre modelos (v1.7.0, Dia 157 — pedido do autor, Claude Opus 5.5)
- **Por que**: Vários modelos trabalham na mesma campanha e o padrão variava com o modelo. Nos planos 001–033: planos que remetiam ao anterior em vez de trazer o conteúdo (033 → 032 em sete seções; 029 → "ler o 028 inteiro"), próximo passo devolvido ao autor (032, 033), seis planos num só dia com pouco avanço, duas ferramentas para a mesma função (`rotas/nav.py` × `camadas/navegar.py`) e oito scripts em `acoes/` que ainda automatizam `say`/`give`/`buy` de missão. Toda regra estava em prosa, espalhada por AGENTS, LEIA, diretiva e planos, e só era cumprida quando algum script cobrava.
- **O que**: o padrão sai da prosa e vai para comandos e verificações. `docs/agentes/PROTOCOLO.md` é o roteiro único. O `mandabala.py` imprime a sequência de abertura e a primeira ação (§5 do plano). O `encerrar.py` gera o próximo plano a partir do `state.json` e grava o boletim. O plano v2 (autossuficiente, §5 executável) vira FALHA a partir do plano 034. `docs/agentes/catraca.json` lista as verificações em vigor e `scripts/test_catraca.py` reprova quem remover uma. A tabela "Ferramentas" do `automato/README.md` marca cada script como canônico, legado, pontual ou PROIBIDO, e o `check_project.py` avisa quando surge script fora dela.
- **Custo**: mais um passo no fim da sessão (`encerrar.py` em duas etapas). Planos mais longos, porque copiam o que segue valendo. Remover ou afrouxar uma verificação passa a exigir a aprovação do autor citada aqui.
- **Como afrouxar uma regra**: nova seção neste arquivo, com a frase do autor, e edição de `docs/agentes/catraca.json` no mesmo commit.


---

## 14. `consider` só para bicho novo, e nada que abaixe a moral é abatido (v1.7.28, Dia 161 — diretiva do autor, 2026-10-22, Claude Sonnet 5.5)
- **Frases do autor:** *"vc já conhece todos os bixos do tabuleiro, para que dar consider?"* · *"consider é importante quando achamos bixos novos, mas pode usar o que estavamos abatendo no milharal? não podemos matar nada que abaixe nossa moral, mesmo que for hostil"*.
- **Por que:** o auditor dava FALHA `ataque-sem-consider` até para o `sleep` na Rainha, que já foi medida muitas vezes. E o `milharal_v2` rendeu 43 mil de EXP em 10 minutos, mas o alinhamento caiu de 415 para 312 em 17 abates de alvos hostis; o autor proíbe qualquer abate que derrube a moral, hostil ou não.
- **O que:** (1) `scripts/auditar_sessao.py` ganha `CONHECIDOS` (peão, bispo, cavaleiro/cavalo, torre, rainha, rei): essas peças não exigem `consider` prévio; bicho novo continua exigindo. (2) `automato/nucleo/config.py` ganha `ROTINAS_BANIDAS_POR_MORAL` (`milharal_v2` e `milharal`); `turno.py` e `trabalhar.py` se recusam a rodá-las (código 6). (3) `turno.py` lê o alinhamento entre turnos, com o motor parado, e para com código 7 se ele cair (diretiva §22 aplicada como parada, não só como aviso). (4) `diretiva_de_jogo.md` §27 e três IDs na catraca.
- **Custo:** o milharal, a fonte de XP mais rápida conhecida (~2,5 mil por abate), fica fora até o autor liberar ou aparecer alvo que não derrube a moral. A isenção do `consider` é uma lista fixa: bicho novo que entre nela sem ser medido escapa do auditor.
- **Como desfazer:** tirar o nome de `ROTINAS_BANIDAS_POR_MORAL` (só com nova frase do autor registrada aqui) ou o bicho de `CONHECIDOS`.


---

## 15. Detect invisibility sempre ligado e identify de todos os itens (v1.7.29, Dia 161 — diretivas do autor, 2026-10-22, Claude Sonnet 5.5)
- **Frases do autor:** *"detect invisibility sempre ligado"* · *"obrigação sempre identificar todos os itens que temos"*.
- **Por que:** o espólio do Rei Negro (Cetro e Chave) é invisível e levou 3 dias para aparecer (§88); e sem `identify` o item errado é vestido, vendido ou largado (Dia 161: botas e túnica ficaram para trás sem registro do que faziam).
- **O que:** (1) `config.MANTER_DETECT_INVISIBILITY = True`; o `cuidar.py` lê as horas do `score` e relança abaixo de 4 h, confirmando pelo `score` (a mensagem de sucesso ainda não foi medida). A regex de duração passou a casar "detect invisibility" inteiro: antes as horas do detect eram lidas como as da invisibilidade. (2) `acoes/identificar_itens.py` identifica inventário e vestidos e grava `itens.json`; `devolutiva.py` (`itens.identificados`) exige o registro de todo item do `state.json`; diretiva §29.
- **Custo:** ~16 de mana a cada ~20 horas de jogo (~25 min reais); uma ida a mais à Praça do Templo, porque o Templo bloqueia magia. A ferramenta gasta ~2 a 4 comandos por item.
- **Limite:** item dentro da mochila vestida exige tirar a mochila (peso).


---

## 16. Rotina do Tesouro Negro: pegar o tesouro 5 vezes sem ficar parado (v1.7.31, Dia 161 — meta do autor, 2026-10-22, Claude Sonnet 5.5)
- **Frase do autor:** *"pegar o tesouro do bau mais 5x, não fique parado esperando muito tempo, utilize rotinas ou crie novas"*.
- **Por quê:** o Tesouro Negro da Realeza (20.000 moedas) reaparece e a porta tranca de novo quando a zona do tabuleiro reinicia, mas o período não estava medido; esperar parado desperdiçava a sessão.
- **O que:** `acoes/tesouro_negro.py` repete a ida (Templo, H5, D5, D7, D8, `cast 'sleep' rainha`, `unlock`/`open` se `!baixo`, `down`, `get moedas`, `up`, `recall`), nunca por E8. A porta fica aberta: ver `!baixo` de novo é o sinal do reset. Mede o intervalo entre tomadas (mediana) e sonda 1,5 min antes dele; antes de medir, 1ª sonda aos 6 min e depois a cada 3. Entre as sondas empilha tarefas do `aproveitar_tempo` (sem `vender_espolio`) e dorme o resto. Para se faltar a chave, 3 idas seguidas falharem, ou passar do teto de minutos.
- **Custo:** cada sonda é uma ida de ~1 min (14 passos pelo tabuleiro); o periodo real do reset decide a duração total; a chave deteriora com o tempo e pode acabar no meio.
- **Limite:** `cast 'sleep' rainha` rende ~750 de EXP por lance (observado 3 vezes); não afeta o alinhamento nas medições feitas (312 antes e depois).


---

## 17. EXCEÇÃO de moralidade: o Rei Branco morre uma vez, para abrir o Tesouro Branco (v1.7.35, Dia 163 — decisão do autor, 2026-10-22, Claude Sonnet 5.5)
- **Frases do autor:** *"vamos tentar matar o rei branco, abrindo uma exceção na política de moralidade"* · justificativa *"todo rei é um tirano, e nossa personagem é rebelde"* · *"e pegar o tesouro dos brancos"* · *"se algum personagem o defende, é tirano como ele!"* · *"deve ser um espelho da tesouraria negra"* · *"mataremos ele só uma vez"*.
- **O que a exceção cobre (e só isto):** (1) **uma** morte do Rei Branco (E1), pelo kite de 1 raio com recall imediato; (2) combate **de defesa** contra peças NPC do lado branco que o defendam e ataquem a personagem; (3) o Tesouro Branco (porta `!baixo` de D1, espelho do negro), com as chaves que o Rei largar.
- **O que NÃO cobre:** jogadores reais (o Keen e os demais: PvP fica fora), animais, camponeses e NPCs neutros ou pacíficos (§22 e §27 seguem valendo para tudo o mais), e nenhuma segunda morte do Rei Branco.
- **Custo esperado, medido antes:** abater peça branca (alvo bom) derruba o alinhamento (Cavaleiro Branco: 455 para 402; o Rei Negro, ao contrário, SOBE a moral: 312 para 394 em três mortes). O alinhamento hoje é 394; abaixo de ~350 a Cruz Ansada (ANTI-NEUTRO) volta a pular do corpo. O Rei Branco nunca foi medido: `consider` obrigatório (bicho novo) e a 1ª ida é medição.
- **Como:** `xadrez_cascata.py --etapa rei --rei --lado branco --excecao-rei-branco` e `tesouro_negro.py --lado branco --excecao-rei-branco`. A trava `automato/runtime/rei_branco_morto.json` impede um segundo kill. O alinhamento é conferido antes e depois e registrado no plano.
- **Como desfazer:** apagar este item e o `--excecao-rei-branco`; sem a flag as duas ferramentas recusam o lado branco.

