# Roteiro — Banco de Sangue, déficit no Tabuleiro e teste de cura com vida baixa

> **Quando:** próxima sessão. **Modo (§26):** `missão` (sondagem, linha a linha) na fase 1 e 4;
> `moer` **só** se for farmar de verdade — aqui o Tabuleiro é para **tirar vida**, não para XP em série.
> **Teto de gasto:** 5% do ouro (1.572). Nada de compra neste roteiro.
> **Origem:** ordem do autor em 2026-10-21 ("faltou testar o banco de sangue"; "matar umas peças pretas
> e, em vez de dormir, procurar onde se cura").

## 0. O que já está medido (não repetir)

- `give blood` no Banco de Sangue: **211 → 201 hp** na resposta, e **211 de novo** no comando seguinte
  (~6 s). A enfermeira diz *"te dá algumas moedas e você começa a se sentir melhor"*. O que falta é saber
  se a vida **volta sozinha** ou se **é a doação que devolve** — e se a perda se **acumula** em doações
  seguidas. É o teste da fase 1.
- `curar` = `Como?!?` em 6 salas, **todas com 211/211**: Templo de Midgaard, Guilda dos Clérigos,
  Templo de Todos e Ninguém, Banco de Sangue, **Hospital de Jareth** e Meditação/Oração.
  `help curar` diz que o comando existe e serve nesses lugares → falta o teste **com déficit**.
- Nenhuma magia de cura na lista da maga; `heal`/`cure`/`curar` dão o mesmo verbete de ajuda.
- Lojas: a de Magias de Midgaard **não tem** cura; Lyon (Pierre/Toulouse) só abre **de dia**.

## 1. Fase 1 — Banco de Sangue, três medições (5 min, custo zero)

Na sala, **sem sair**:
```
score
give blood
score
give blood
score
```
Leitura do resultado:
- **hp desce e fica (211 → 201 → 191):** o banco tira vida de verdade **e não devolve** → dá para usar
  como fonte de déficit. Vá direto para a **fase 2A** (o Templo fica a 2 salas).
- **hp volta a 211 depois de cada doação:** a enfermeira devolve o sangue → o banco é só dinheiro
  (e possivelmente uma fonte infinita de trocados). Vá para a **fase 2B**.

Anotar: hp antes/depois de cada doação, moedas recebidas (`score` mostra "Carregando"), e se a mensagem
muda na segunda vez.

## 2A. Se o banco drena a vida — testar cura já, com déficit

Do banco: `e` (Via da Veneração) → `s` (Templo de Todos e Ninguém) → `curar` → `score`.
Depois `e` (Salão dos Deuses) → `curar` → `score`, e ficar 1 min parado medindo a vida (é a sala dos
"ventos sagrados").
Se algum responder diferente de `Como?!?`: **medir ouro ÷ HP** na segunda vez (anotar ouro antes/depois).

## 2B. Se o banco não drena — déficit no Tabuleiro (15–20 min)

1. `python automato\camadas\navegar.py --para xadrez_H5` (o `navegar` já vai ao tabuleiro; portão `medium`).
2. **Nunca** entrar em E8, E1, B1, G1 (casas do Rei) e **nunca** andar com vida abaixo de 100 — `recall`.
3. Alvo: **peões pretos** (e, se sobrar vida, um bispo preto). **`consider` antes de cada ataque**
   (o auditor dá FALHA em ataque sem `consider`).
4. Combate à mão, no máximo ~8 rodadas por peça: `cast 'lightning bolt' peao` (2 raios por peão,
   conhecimento §68). Parar ao chegar em **~150 hp** (déficit de ~60) — **não dormir**.
5. Anotar EXP e ouro ganhos (`score` depois de cada abate) — é o XP que o autor pediu.

## 3. Fase 3 — teste de cura com déficit (o que decide)

Com o déficit na mão (hp ~150/211), na ordem de menor custo:

1. **Fonte da Praça do Templo (Midgaard, no caminho de volta):** `score`, `drink fonte`, `score`.
   Nunca foi medido com vida baixa.
2. **Hospital de Jareth** (`jr_hospital`): `score`, `curar`, `score`. Se curar: `score` do ouro antes e
   depois → **ouro ÷ HP**.
3. **Salão dos Deuses (Jareth):** `curar` e 1 min parado, medindo a vida.
4. **Templo de Todos e Ninguém:** `curar` (já deu `Como?!?` cheio; só repete se 2 e 3 falharem).

Se algum funcionar: repetir com déficit conhecido e anotar **preço por HP**; comparar com dormir
(grátis, ~5 hp/min) e decidir se vira método padrão de emergência.

## 4. Fase 4 — fecho

`recall` → Templo de Midgaard, comer/beber (`cuidar.py`), `_CLOSE sleep`. Se `save_confirmed` vier falso,
repetir `_CLOSE sleep` (a resposta "Salvando os seus atalhos." é a confirmação). **Nunca `quit`.**

## 5. Riscos e regras que valem aqui

- **A rota para Jareth passa pelo Altar do Templo** e nesta sessão disparou combate ali: ir com `armor`,
  `consider` em tudo que se mexer e **`recall` ao primeiro golpe grave** (não recuar andando).
- Vida < 100 → **só `recall`**, em qualquer fase.
- Não atacar cidadão, guarda, zelador, animal ou peça **branca** (o autor pediu peças pretas; peça branca
  é do outro lado da quest e não dá o XP que interessa).
- Não comprar nada; não testar magia no Templo nem em loja (`armor` falha lá dentro).
- Máximo ~30 ataques e ~80 passos por `play.py` na sessão inteira (auditor). Se for farmar de verdade,
  é `turno.py --rotina novatos|milharal_v2` — **as rotinas `xadrez_v2/v3` são legado e não podem ser usadas**
  (pegam espólio antes da triagem).

## 6. Registro (copiar para `maquina/verificacoes.md`)

| # | Local | Comando | HP antes→depois | Ouro | Resposta literal | Veredito |
|---|---|---|---|---|---|---|
| 1 | Banco de Sangue | `give blood` (1ª) | | | | |
| 2 | Banco de Sangue | `give blood` (2ª) | | | | |
| 3 | Fonte da Praça do Templo | `drink fonte` | | | | |
| 4 | Hospital de Jareth | `curar` | | | | |
| 5 | Salão dos Deuses | `curar` | | | | |
| 6 | Salão dos Deuses | ficar 1 min | | | | |
