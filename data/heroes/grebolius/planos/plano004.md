# Plano 004 — Capítulo 05 publicado; a lição do transcript

| | |
|---|---|
| **Criado em** | 2026-10-16 · Dia 156 |
| **Por** | **`deepseek-flash`** |
| **Herói** | `grebolius` |
| **Objetivo** | **O Capítulo 05 está fechado, corrigido e publicado.** Falta escolher o próximo |
| **Sessão encerrada?** | **Sim** — nada rodando, personagem salva no Templo |

> **Leia o [`LEIA.md`](LEIA.md) primeiro.** **Este arquivo não se edita** — quem vier cria o
> **`plano005.md`**. Os planos 001, 002 e 003 **ficam como estão**: cada um é o retrato de um momento,
> inclusive dos erros. O 003, do `GPT-6 / Codex`, **corrige o 002** — e a correção dele é a peça mais
> importante desta pasta.

---

## 1. O capítulo está fechado — e agora está **certo**

`capitulos.json` → capítulo 5 `concluido`, `closed_on_day: 156`. **As duas autoquests concluídas:**

```
Novela dos Novatos             Concluída
Limpando Monstros              Concluída
```

**A narrativa publicada é a do `GPT-6 / Codex`**, não a minha. A minha contava o **fim** de uma cadeia
longa como se fosse o começo; a dele tem a cadeia real. **O commit `1ecce4d` é dele** e foi empurrado
por mim, com a autoria sinalizada — ele está proibido de publicar (diretiva do autor, `AGENTS.md` §12).

**Evidência:** `evidence/dia156d.json` (meu, **parcialmente superado**) e **`evidence/dia156e.json`**
(dele, 7.024 linhas, a fonte da revisão).

---

## 2. A cadeia real das duas missões — o que o plano 002 não sabia

**Novela dos Novatos** não fechou "ao falar com a tagarela". Foi uma cadeia:

| Novato | O que ele queria ouvir |
|---|---|
| o **perdido** | **`say ajuda mapas`** |
| o **perturbador** | **`say diretrizes`** e, quando ele pediu, `say sim` |
| a **tagarela** | receber **a veste** |
| o **confuso** | **`say retornar`** ← **`say recall` NÃO funcionou** |
| o **esperto** | **`say ajuda remortar`** |

**Limpando Monstros** não fechou "ao fazer o mico fugir". Foi a cadeia do Alquimista:

```
inseto rastejante → dois monstros de veste → dois zumbis
                  → ESPECTRO NEGRO INVISÍVEL → o Minotauro
```

**Voltando ao Alquimista entre cada etapa.** O mico foi defesa incidental. **Não é preciso entregar
chifres** — abate e retorno bastaram.

---

## 3. ⚠️ A lição — e ela é sobre MÉTODO, não sobre sorte

**Dois agentes jogaram o mesmo capítulo e chegaram a resultados opostos.** A diferença não foi
habilidade: foi **como cada um leu a fonte**.

| `deepseek-flash` (eu) | `GPT-6 / Codex` |
|---|---|
| Tratou *"dizer algo ao personagem"* como **enigma** | Leu o **transcript** |
| Inventou ~35 frases, 9 tópicos, 3 entregas | Achou a fala que o novato **já tinha dito** |
| **`ajuda mapas`, gravado na linha 5562 do transcript que eu tinha aberto** | **Leu a linha 5562** |

### As três regras que saem disso (estão no `automato/DECISOES.md` §9)

1. **O diálogo de missão é literal.** O NPC diz a palavra e você repete **a palavra dele**, não o seu
   sinônimo. `retornar` funcionou; `recall` não. `ajuda remortar` funcionou; `ajuda encarnação` não.
2. **Ler o transcript, não a síntese.** Fala de NPC não se perde: está gravada. **Resumo é
   interpretação; transcript é fonte.**
3. **`score tudo` antes de cada fala e cada entrega.** O objetivo **muda** com a etapa, e ação antes da
   hora **não conta** — a veste entregue cedo saiu do inventário sem avançar.

### E as descobertas operacionais que eu não fiz

- **`where <nome>` localiza monstro/jogador DENTRO DA SUA ÁREA.** Eu varri o mundo a pé por rodadas.
  `where` sozinho lista **os jogadores** da área.
- **`autoquest todas` é HISTÓRICO**, não estado atual: marcava *Limpando Monstros* concluída enquanto o
  ciclo reiniciado ainda pedia o Minotauro. **O catálogo não é prova de conclusão; o `score` é.** Eu usei
  o catálogo como prova no `dia156d.json` — **está corrigido no `maquina/verificacoes.md`**.
- **`buy 6 pao`** compra em lote; **`put all.punhal mochila`** guarda em lote (`all.<item>`).
- **O `help` pode mentir:** ele documenta `Uso: onde <monstro ou jogador>`, e **`onde` responde
  `Como?!?`**. Só `where` funciona. **(Essa eu peguei, testando o que ele tinha lido na ajuda.)**

**A conclusão que interessa ao projeto:** os dois juntos valem mais que cada um. Ele leu o transcript
que eu não li; eu testei o `onde` que ele tirou da ajuda. **É o argumento a favor dos planos numerados**
— e a razão de o 003 dele **não** apagar o 002 meu.

---

## 4. Estado exato

| | |
|---|---|
| Personagem | **Nível 21**, Mago Elfo, 1ª encarnação |
| Vida / mana / movimento | **135/135 · 270/270 · 131/131** |
| Experiência | **1.200.001** (próximo em 1.400.000) |
| Ouro | **300 na mão + 1.351 no banco** (1.651) |
| Mortes | **7** (nenhuma nova) |
| Alinhamento | **181 — um pouco bom** |
| Acerto / Dano / CA | **4 / 2 / 110** |
| `wimpy` | **45** |
| Sessões de treino | **40** |
| Pontos de Aventura | **0** |
| Local | **O Templo de Midgaard**, dormindo |
| Mapa | **381 salas / 793 arestas** |

**Equipamento novo:** `um diminuto brinco de novato` (**ANTI-DT**; +15 vida máx, +15 movimento máx,
+1 acerto, +1 dano) e `um manto de pano` (armadura +30). Magia nova: **`curse` a 10%**.

**⚠️ O ANTI-DT do brinco é uma flag do ITEM — não é prova de que a personagem esteja imune a armadilha
mortal.** Não foi testado. Não presuma.

---

## 5. Os bloqueios

**Nenhum.** As duas missões fecharam, o capítulo está publicado, e não há tarefa pendente.

**O que falta é DECISÃO:** o objetivo do próximo capítulo. **Não abrir outra autoquest para preencher
tempo** — foi o que o Dia 156 ensinou.

**Candidatos, em ordem de valor:**
1. **As 33 portas nomeadas** do Capítulo 04 — nunca abertas, contornadas duas vezes.
2. **Jareth e a Avenida Floris** — rota verificada, **nunca percorridas**. Menor risco.
3. **Pontos de Aventura → a loja dos deuses** — ANTI-DT e IMUNE-DT.
4. **Uma Lição em Gargamel** — o smurf minerador, sem pista. **Comece pelos `docs/circlemud/` e pelo
   `where`, não varrendo o mundo.**

---

## 6. NÃO REPITA

1. **Tratar o diálogo de missão como enigma.** Ele é **literal** — o NPC diz a palavra.
2. **Ler o resumo no lugar do transcript.** Custou **seis rodadas** (o novato esperto estava nos
   `docs/circlemud/`) e **uma crônica publicada errada**.
3. **Usar `autoquest todas` como prova de conclusão.** É histórico. Use o `score`.
4. **Entregar ou falar antes de o `score` pedir.** Não conta.
5. **Pedir `onde`** — o `help` documenta, o servidor recusa. **`where`.**
6. **Varrer o mundo atrás de NPC** sem tentar `where <nome>` antes.
7. **Presumir que ANTI-DT no item imuniza a personagem.**
8. **A coleira do dragão** — a missão do dragão já foi feita. Pista falsa.
9. **O Andarilho Misterioso** — evento de mundo, não missão.
10. **Vender armaduras**, usar **`quit`** com missão em andamento, digerir **corpus parcial**, e navegar
    pelo **título** no Grande Campo.

---

## 7. Ferramentas e comandos

| Ferramenta | Para quê |
|---|---|
| **`docs/circlemud/`** | A Zona dos Novatos **é o `186.wld` padrão**: mob por mob, sala por sala. **A fonte que mais rendeu** |
| **`evidence/dia156e.json`** | A cadeia real das duas missões, com as falas |
| `data/heroes/grebolius/conhecimento.md` §Retomada do Dia 156 | O resumo operacional dele |
| `automato/DECISOES.md` **§9** | **A lição de método**, com o custo medido |
| `maquina/verificacoes.md` | Os achados técnicos (`where`, `buy`, `all.<item>`, o `onde` que não existe) |

```
python automato/nucleo/driver/play.py "<comando>"     # comando avulso
python scripts/mandabala.py                           # retomar: o plano vigente
python automato/camadas/cuidar.py                     # come, bebe, magias (exit 0/1/2)
python automato/camadas/prepara.py --forcar           # padaria, fonte, banco, doações
python automato/verificar.py                          # 18/18
python scripts/check_project.py                       # 0 erros
python scripts/sync_hero.py --hero grebolius          # regenera ficha.md / hero.json
```

**Combate:** `consider` antes; **`burning hands`** a 99% mata de primeira o novato; **`lightning bolt`**
para o que é grande — **de longe, com o alvo isolado** (dois raios abateram o Minotauro; o primeiro deu
71). **Corpo a corpo DESLIGADO** — **nunca use a adaga**.

---

## 8. Como encerrar a sua sessão (a mesma obrigação que gerou este plano)

1. `cuidar.py` até `exit 0`.
2. **`save`** — **nunca `quit`**.
3. **Criar `planos/plano005.md`.** **Não edite este nem os anteriores.**
4. Se fechou capítulo: `capitulos.json` com `parts` contendo **`source_kind`**, **`date`** e
   **`evidence`** — sem isso o `check_project.py` falha.
5. `sync_hero.py --hero grebolius` **e** `--check`.
6. `automato/verificar.py` (18/18), `check_project.py` (**0 erros**),
   `python -B -m unittest discover -s scripts -p "test_*.py"` (**116 testes**).
7. Bloco em `docs/agentes/registro_de_evolucao.md` (**append-only**) com **modelo/versão**.
8. Mudança de motor → `automato/CHANGELOG.md` (+ `DECISOES.md`, que **é onde mora a lição deste dia**).
9. Publicar **só se pedido** — e **sinalizar quem fez** cada parte. **A árvore é compartilhada**: confira
   `git status` antes e depois, e **leia o `AGENTS.md` §12** (há agente proibido de publicar).

---

## 9. Fios soltos

- **33 portas nomeadas** por abrir — a promessa contornada duas vezes.
- **Jareth** e a **Avenida Floris** nunca percorridas.
- **40 sessões de treino** sobrando; **`curse` a 10%** (aprendida agora, quase inútil até treinar).
- **Armadura da Torre Negra** amaldiçoada e vestida: desamaldiçoar custa **8.509**.
- A **coleira do dragão** continua na mochila — pode ser descartada (`junk`).
- **`evidence/dia156d.json` (meu) está parcialmente superado** pelo `dia156e.json` (dele). **Fica** como
  registro do erro — apagar apagaria a lição.
- **O driver tem bug:** ele marcou `dead_or_menu` com a personagem viva, respondendo e com HP cheio.
  **Registrado, não corrigido** — e isso foi a decisão certa: `maquina/verificacoes.md` guarda o sintoma.
