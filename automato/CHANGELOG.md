# Controle de versão do automato

Versionamento semântico adaptado a um jogo: **MAIOR** muda o contrato das rotinas,
**MENOR** acrescenta camada/rotina, **CORREÇÃO** conserta comportamento.
As datas usam o **dia de jogo**.

## v1.1 — Dia 155 · automato autossuficiente
- **MUDOU**: o **driver inteiro** (debo_bot.py, parsers.py, live_daemon.py, play.py) passou a viver em `automato/nucleo/driver/`.
- **MUDOU**: token, senha e logs foram para `automato/runtime/` — **fora do git** (`.gitignore`).
- **NOVO**: `automato/acoes/ressuscitar.py` (a ressurreição virou ação do automato).
- **NOVO**: `config.py` aponta os documentos do herói (`conhecimento.md`, `diretiva_de_jogo.md`, `mapa.json`) — referenciados, não copiados.
- **REQUISITO**: subir o driver antes de qualquer camada.

## v1.0 — Dia 155 · empacotamento
- **NOVO**: pasta `automato/` com núcleo, camadas, rotinas e documentação (README, CHANGELOG, DECISOES).
- **NOVO**: `nucleo/config.py` — um único ponto de configuração (caminhos, limites, magias).
- **MUDOU**: as rotinas leem `config` em vez de ter caminhos fixos; o automato roda fora de `scripts/local/`.
- **NÃO MUDOU**: o contrato das rotinas (partir do Templo, voltar, salvar).

## v0.6 — Dias 152-154 · trajeto determinístico
- **CORREÇÃO**: `base.py` apontava o token para o caminho errado — todas as rotinas liam vazio.
- **CORREÇÃO**: a rota da fazenda é **oeste, oeste, oeste** (Entrada da Fazenda → Pequena Estrada → Fim da Estrada → Milharal).
- **NOVO**: rota completa Templo→Milharal documentada no `conhecimento.md` §24: n5 → n,e,n → n6 → l6 → n,n,l,l,s → o3.
- **NOVO**: o caçador usa **LIGHTNING BOLT** (48-64 de dano) e mira o **nome exato** do monstro.

## v0.5 — Dia 150 · diretiva do autor
- **REMOVIDO**: venda de armaduras (rotina `xadrez` **suspensa** para `rotinas/_suspensas/`).
- **MOTIVO**: "perdemos mais dinheiro do que ganhamos com elas" — caixa finito do armeiro + armadura amaldiçoada (60 kg) + pergaminho de 8.509 para vender por 8.500.

## v0.4 — Dias 148-149 · camadas de decisão
- **NOVO**: `vigia.py` (diagnóstico pelo log), `prepara.py` (arrumador + banco), `trabalhar.py` (despachante), `turno.py` (encarregado).
- **NOVO**: **banco do Templo** no prepara (`deposit`), com reserva de 300 na mão.
- **NOVO**: hidratação na **fonte de mármore azul** da Praça do Templo (`fill cantil fonte` / `drink fonte`).
- **CORREÇÃO**: o prepara só compra pão se não tiver (ela acumulou 10 e ficou em 130/115 kg).

## v0.3 — Dia 147 · higiene e alvo
- **NOVO**: `abastecer()` — comer e beber **antes** de dormir/viajar (dormir faminto consumia vida e mana).
- **CORREÇÃO**: caçador com **plano B de alvo** quando a magia pergunta "em que?".

## v0.2 — Dia 143 · guarda de repetição
- **NOVO**: `guarda.py` — mesma resposta **3× seguidas** → `recall` + `save` + saída (código 9).
- **NOVO**: injeção da guarda no `run()` de **33 robôs**.
- **CORREÇÃO**: a guarda passou a **ignorar comandos benignos** (buy/eat/drink/look/score/rest/sleep) — compras legítimas a disparavam.

## v0.1 — Dia 141 · método
- **NOVO**: o método "mapear à mão → testar em trechos → só então automatizar".
- **NOVO**: `wake; stand` obrigatório antes de qualquer deslocamento.
- **MOTIVO**: 7 mortes, das quais **4 causadas por script sem supervisão**.

## Próximas versões (planejado)
- **v1.1**: rotina `dicas-magicas` (descobrir o gatilho do ciclo do "sim").
- **v1.2**: rotina `esgoto` de verdade (reconhecimento com mapa incremental).
- **v1.3**: o turno relançar a rotina sozinho quando o vigia voltar a OK.
