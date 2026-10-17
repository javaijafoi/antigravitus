# Plano 007 — Capítulo 06 fechado; a devolutiva técnica virou obrigatória

| | |
|---|---|
| **Criado em** | 2026-10-16 · Dia 156 |
| **Por** | **`deepseek-flash`** |
| **Herói** | `grebolius` |
| **Objetivo** | **Nenhum capítulo em curso.** Os sete estão fechados. Falta escolher o 07 e cobrar a devolutiva |
| **Sessão encerrada?** | **Sim** — personagem no Templo, salva; daemon no ar |

> **Leia o [`LEIA.md`](LEIA.md) primeiro.** **Este arquivo não se edita** — quem vier cria o
> **`plano008.md`**.
>
> **Antes de encerrar a sua sessão, rode `python scripts/devolutiva.py`.** Ele é obrigatório desde o
> Dia 156 e **reprova** o que passar despercebido — inclusive *"a devolutiva prometeu o mapa e o
> `mapa.json` não mudou"*.

---

## 1. Onde o objetivo está

**Os SETE capítulos estão `concluido`.** O 06 fechou com a limpeza dos esgotos executada pelo
`Gemini 3.8 Flash` e a narrativa escrita por mim. **Não há capítulo em curso.**

**O 07 já tem assunto e endereço:** a **Serpente dos Esgotos**, o **Aligátor** e o **Dragão Vermelho**
— os três ficaram vivos, e dois deles **mataram ela antes**.

---

## 2. Estado exato

| | |
|---|---|
| Personagem | **Nível 21**, Mago Elfo |
| Vida / mana / movimento | **135/135 · 270/270 · 131/131** |
| Experiência | **1.219.294** (próximo em 1.400.000) |
| Ouro | **300 na mão + 1.351 no banco** (1.651) |
| Mortes | **8** (a 8ª no Covil do Dragão) |
| Classe de Armadura | **111** (81 + 30 de `armor`) |
| Acerto / Dano | 4 / 2 |
| `wimpy` | **45** |
| Sessões de treino | **40** — decidir o que treinar conforme o objetivo |
| Pontos de Aventura | **0** |
| Local | **O Templo de Midgaard**, em pé, salva |
| Mapa | **381 salas / 793 arestas** |

**Equipamento:** `a Armadura da Torre Negra` (amaldiçoada), `a Coroa da Rainha Branca`,
`um diminuto brinco de novato` (**ANTI-DT**), `um manto de pano` (+30), `um escudo`, espada curta.
**Magias:** `burning hands` 99%, `lightning bolt` 99%, `magic missile` 99%, `detect invisibility` 97%,
`armor` 99%, `curse` 10%.

---

## 3. O que já foi descoberto (não redescubra)

1. **A rota de mão dupla dos esgotos:** `A Praça Comum` → `n` → `O Depósito de Lixo` → **`d`** → *A
   Junção Quádrupla Abaixo do Depósito* → **`u`** volta. **NUNCA descer pelo buraco do Laboratório dos
   Magos** — mão única.
2. **`Passo-Em-Falso` é armadilha mortal — e o SERVIDOR AVISA:** *"Você percebe que há algo perigoso
   por perto!"*. Fica a oeste da borda oriental e ao norte da larga borda. **Recuar, sempre.**
3. **`consider` tem um rótulo acima de `danger`: `Você é LOUCO!`** — Clodoaldison e os 3 besouros
   gigantes dormindo. **Não calibrado.**
4. **O Dragão Vermelho abate 135 HP em um turno** — a vida máxima dela. **Não é alvo de nível 21.**
   Habita `A Borda Estreita (Covil do Dragão)`, tem aura multicolorida.
5. **O inventário SOBREVIVE à morte** — ela revestiu tudo com `wear all` no Templo depois da Morte #8.
   **A morte custa experiência, não equipamento.**
6. **`where <nome>` localiza monstro/jogador DENTRO DA SUA ÁREA; `where` sozinho lista os JOGADORES.**
   **`onde` NÃO existe**, apesar de o `help where` o documentar.
7. **O diálogo de missão é LITERAL:** `retornar`, `diretrizes`, `ajuda remortar`, `ajuda mapas`.
   (`automato/DECISOES.md` §9)
8. **A coleira do dragão não é de missão** — a missão do dragão já foi feita.
9. **Os anéis do esgoto existem** — o `Gemini 3.8 Flash` andou e descobriu que salas registradas como
   becos são circuitos de mão dupla. **O mapa ainda não foi corrigido** (ver §8).

---

## 4. Os bloqueios

**Nenhum de execução.** O que há é **trabalho de verificação pendente** — está na devolutiva (§8).

---

## 5. O próximo passo, e só ele

> **Escolher o objetivo do Capítulo 07 com o autor** — e, se for voltar aos esgotos, **corrigir o
> `mapa.json` primeiro** (§8), porque navegar com o mapa errado é andar às cegas.

**Ordem sugerida, se for o esgoto:**
1. `cuidar.py` até `exit 0`; `prepara.py --forcar`.
2. **Corrigir as 4 arestas dos anéis** (§8) — descendo, conferindo o `exits` real e gravando.
3. **Serpente** e **Aligátor** — os alvos que ficaram. De longe, magia, alvo isolado.
4. **O Dragão** fica para quando houver resposta para 135 de dano em um turno.
5. **Não testar o `Passo-Em-Falso`** sem decidir antes se vale o risco (é a pergunta aberta que vale
   mais que ouro: **o brinco ANTI-DT anula a DT?**).

---

## 6. NÃO REPITA

1. **Descer pelo buraco do Laboratório dos Magos** — mão única.
2. **Entrar no Covil do Dragão** despreparada — 135 HP em um turno.
3. **Pisar no `Passo-Em-Falso`** por curiosidade.
4. **Tratar diálogo de missão como enigma** — é literal.
5. **Ler resumo no lugar do transcript.**
6. **Usar `autoquest todas` como prova de conclusão** — é histórico; a prova é o `score`.
7. **Pedir `onde`** — só `where`.
8. **Presumir imunidade** por causa da flag ANTI-DT do brinco.
9. **Vender armaduras**, **`quit`** com missão em andamento, digerir **corpus parcial**, navegar pelo
   **título** no Grande Campo.
10. **Numerar seção do `conhecimento.md` sem conferir o próximo livre** — a do Dia 156 colidiu (§29).

---

## 7. Ferramentas e comandos

| Ferramenta | Para quê |
|---|---|
| **`python scripts/devolutiva.py`** | **OBRIGATÓRIO no fim da sessão** — verifica o protocolo inteiro |
| `python scripts/mandabala.py` | retomar: o plano vigente + a ordem de leitura |
| **`docs/circlemud/`** | a fonte que mais rendeu |
| `maquina/verificacoes.md` | onde vai **correção de referência do servidor** |
| `data/heroes/grebolius/conhecimento.md` | onde vai **fato do mundo** (§38 é o último número) |

```
python automato/nucleo/driver/play.py "<comando>"
python automato/camadas/cuidar.py                     # exit 0/1/2
python automato/camadas/prepara.py --forcar
python scripts/check_project.py                       # 0 erros
python automato/verificar.py                          # 18/18
```

**Combate:** `consider` antes; **`burning hands`** mata o novato de primeira; **`lightning bolt`** para
o grande, **de longe e com o alvo isolado**. **Corpo a corpo DESLIGADO** — nunca a adaga.

---

## 8. Devolutiva técnica

> **Esta seção é obrigatória** (LEIA.md §8) e é **cobrada** pelo `scripts/devolutiva.py`.

| Descobri | Registrei em | O quê |
|---|---|---|
| **mapa** | **`mapa.json` — PENDENTE** | **Quatro arestas que o Gemini andou e provou serem de mão dupla continuam registradas como becos:** `esgotos_entrada --w--> sala_paredes_lisas`, `esgoto_poco --d--> abaixo_do_poco`, `sala_paredes_lisas --d--> estranha_intersecao`, `canto_noroeste_borda --e--> estreita_borda_leste_oeste`. **Não gravei porque não verifiquei ao vivo — gravar sem andar seria inventar** (AGENTS.md §4.1). **É a primeira tarefa do próximo que for ao esgoto.** |
| **referência do servidor** | **`maquina/verificacoes.md`** ✅ | O **aviso prévio de armadilha mortal** (*"Você percebe que há algo perigoso por perto!"*); o rótulo novo de `consider`, **`Você é LOUCO!`**; e o **Dragão que abate 135 HP em um turno**. Mais a confirmação de que **o inventário sobrevive à morte**. **Coleta do `Gemini 3.8 Flash`; registro meu**, porque ele não tocou neste arquivo. |
| **fato do mundo** | **`conhecimento.md` §38** ✅ | A incursão aos esgotos: abates, topologia dos anéis, Clodoaldino, os besouros, o Dragão, a Morte #8. **A seção era §29** (colidindo com a minha) — **renumerada por mim para §38**, com nota de correção. |
| **erro do motor** | **nada** | O motor não atrapalhou nesta sessão. *(A limitação conhecida continua: o `check_project.py` confere **estrutura**, não **cobertura** — é por isso que este script existe.)* |

### O que esta devolutiva está registrando, e por quê

**Duas sessões seguidas falharam do mesmo jeito, no mesmo dia:**

1. **A minha** publicou uma crônica errada — leu o fim de uma cadeia e narrou como começo.
2. **A do `Gemini 3.8 Flash`** andou os esgotos, **descobriu os anéis**, escreveu o achado em prosa
   **numa seção chamada "fechando os anéis do esgoto"** — e **não tocou no `mapa.json`**.

**Nos dois casos ninguém percebeu, porque o validador confere estrutura e não cobertura.** Ele não sabe
que uma caminhada aconteceu. **É por isso que `scripts/devolutiva.py` existe**, e é por isso que esta
tabela é conferida contra o `git diff`: **se ela diz "mapa", o `mapa.json` tem de ter mudado.**

> **⚠️ Nesta sessão, a linha "mapa" diz PENDENTE de propósito** — é a única honesta. **O script vai
> acusar aviso nela**, e deve mesmo: **a pendência é real e fica visível.**

---

## 9. Como encerrar a sua sessão

1. `cuidar.py` até `exit 0`; **`save`** — **nunca `quit`**.
2. **Criar `planos/plano008.md`** com o modelo do `LEIA.md`, **incluindo a §8 Devolutiva técnica**.
3. **Rodar `python scripts/devolutiva.py` e resolver as FALHAS.** Só encerre com **0 falhas**.
4. `sync_hero.py --hero grebolius` **e** `--check`.
5. Bloco em `docs/agentes/registro_de_evolucao.md` (**append-only**) com **modelo/versão**.
6. Publicar **só se pedido**, **sinalizando quem fez** — e ler o **`AGENTS.md` §12**.
