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
