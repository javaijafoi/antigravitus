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


## Os próximos desafios (em ordem de valor para o capítulo)
1. **Fechar o trajeto do milharal** (falta confirmar *Uma Parte Densa → Bosque → sul*) e **entregar
   Problemas Agrícolas** — é a missão mais perto de concluir (1 invasor já abatido).
2. **Descobrir o gatilho de Dicas Mágicas** — o ciclo do "sim" limpa a instrução e ela volta;
   a hipótese é que exija **uma magia específica** no lugar certo.
3. **Localizar os NPCs** de Novela dos Novatos (*o novato esperto*, nas praças) e de
   Uma Lição em Gargamel (*o smurf minerador*, sem pista).
4. **Decidir o destino da Armadura da Torre Negra** (60 kg presos, amaldiçoada): carregar (grátis,
   mas sem espaço para espólio) ou pagar **8.509** para desamaldiçoar e doar (libera 60 kg).
5. **Revalidar o mapa** — consolidado no Dia 100 e já divergente em pelo menos um ponto.

## Como outro agente deve continuar
- Leia o `README.md` primeiro (a arquitetura e o contrato);
- Mude **só** `nucleo/config.py` para adaptar a outro projeto/heroi;
- **Nunca** rode rotina sem vigia e sem supervisão (ver os invariantes no README);
- Registre cada mudança aqui e no `CHANGELOG.md` — o próximo agente continua de onde você parou.
