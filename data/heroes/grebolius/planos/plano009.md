# Plano 009 — Capítulo 08: `Uma Lição em Gargamel` (na Vila dos Smurfs)

| | |
|---|---|
| **Criado em** | 2026-10-16 · Dia 156 |
| **Por** | **`Gemini 4 Argon`** |
| **Herói** | `grebolius` |
| **Objetivo** | **Concluir `Uma Lição em Gargamel`** — a autoquest de nível 20–80 iniciada com `o smurf minerador` na Vila dos Smurfs |
| **Sessão encerrada?** | **Sim** — personagem no Templo de Midgaard, salva (`save`, sem `quit`); daemon no ar |

> **Leia o [`LEIA.md`](LEIA.md) primeiro.** **Este arquivo não se edita** — quem vier cria o
> **`plano010.md`**.
>
> **Antes de encerrar, rode `python scripts/devolutiva.py`** — é obrigatório desde o Dia 156 e
> **reprova** quem promete no plano e não grava no artefato (§8).

---

## 1. Onde o objetivo está

**O Capítulo 07 ("O Que Eu Deixei no Meio") foi CONCLUÍDO.** `Problemas Agrícolas` está marcada como **`Concluída`** em `autoquest todas` e saiu de `autoquest listar` (não é repetível nesta encarnação).

**Diretriz do autor para o Capítulo 08:** fazer a nova missão disponível para o nível dela — **`Uma Lição em Gargamel`**:
- **Catálogo (`autoquest todas`):** `Níveis: 20-80, encarnações: 1-4, qualquer alinhamento, todas as classes, todas as raças.`
- **Iniciador (`autoquest listar`):** **`o smurf minerador`** (`Até o nível 80, iniciada com: o smurf minerador.`).
- **Endereço descoberto nesta sessão (`help vila dos smurfs` / `MAPA 33`):**
  > *"A partir do Templo de Midgaard, siga para o sul em direção à famosa Praça do Comércio. De lá, siga para o leste pela Rua Principal, até chegar ao centro da grande Estrada do Rei. Nesse ponto, haverá um caminho ao norte, onde se encontra a Entrada Para a Vila dos Smurfs."*

---

## 2. Estado exato

| | |
|---|---|
| Personagem | **Nível 22**, Mago Elfo, 1ª encarnação |
| Vida / mana / movimento | **141/141 · 280/280 · 133/133** *(cheios)* |
| Experiência | **1.572.738** (próximo nível em **1.600.000** — restam apenas **27.262 EXP** para o Nível 23) |
| Ouro | **300 na mão + 3.999 no banco** (**4.299** total; +2.648 depositados nesta sessão) |
| Mortes | **8** (0 nesta sessão) e **1** armadilha mortal histórica |
| Atributos | `FOR 11 · INT 19 · SAB 17 · DES 16 · CON 10 · CAR 12` |
| Combate | **CA 134** (base 103 + `armor` 31 por 51h) · **Acerto 10** · **Dano 7** · `wimpy 45` |
| Magias ativas | `armor` (51h) |
| Magias aprendidas | `burning hands` 99% · `lightning bolt` 99% · `magic missile` 99% · `detect invisibility` 97% · `armor` 99% · `invisibility` 99% · `chill touch` 95% · `shocking grasp` 95% · `curse` 10% |
| Autoquests concluídas | `A Coleira do Dragão`, `Altruísmo`, `Ninguém Segura Esse Bebê`, `Novela dos Novatos`, `Limpando Monstros`, **`Problemas Agrícolas`** |
| Local | **O Templo de Midgaard** (`save` executado) |
| Mapa | **381 salas / 793 arestas** |

---

## 3. O que já foi descoberto nesta sessão

1. **Onde o jogo marca que `Problemas Agrícolas` foi feita:** `autoquest todas` exibe `Problemas Agrícolas            Concluída`, e `autoquest listar` a **remove** de `Autoquests Disponíveis Agora:` (provando que é missão única nesta encarnação, ao contrário de `Limpando Monstros`).
2. **Onde fica a Vila dos Smurfs (`Uma Lição em Gargamel`):** planos anteriores diziam *"o smurf minerador, sem pista"*, mas `help mapas` lista **`33. VILA DOS SMURFS`** e `help vila dos smurfs` dá a rota exata a partir do Templo: sul até a Praça do Comércio → leste pela Rua Principal (cruzando o Portão Leste) até o centro da Estrada do Rei → norte para **`A Entrada Para a Vila dos Smurfs`**.
3. **Três regras de autoquest medidas em `Problemas Agrícolas` que valem para `Uma Lição em Gargamel`:**
   - **Nunca saia da sala antes da última fala do NPC:** `O Pacificador` falou 13 linhas espaçadas; sair antes da 13ª travou o gatilho seguinte. Espere ~15s de silêncio após a fala antes de andar.
   - **Em missões de abate por ondas, o `score tudo` pode manter `Você deve matar criaturas.` mesmo com a cota cheia:** volte à sala do NPC ao completar a contagem do log para que o *mobprog* dele avance a etapa.
   - **Confira a descrição exata do mob com `look`:** nem todo mob usa `'está aqui'` na descrição da sala.
4. **Ficha técnica de `um belo cinturão de rodeio`:** nível 15, peso 5, valor 1.250, slot `CINTURA`, `CA -12` (+22 CA no `score` do DeBo), `Acerto +5`, `Dano +5`, `Destreza +1`, `Carisma +1`.

---

## 4. Os bloqueios, e o que já foi tentado

- **`Problemas Agrícolas`:** **RESOLVIDO E ENTREGUE.**
- **`Uma Lição em Gargamel`:** **NENHUM BLOQUEIO.** A Vila dos Smurfs ainda não foi mapeada no `mapa.json` — a primeira ida será mapeamento à mão + início e conclusão da autoquest.

---

## 5. O próximo passo, e só ele

**Executar o Capítulo 08 — Concluir `Uma Lição em Gargamel`:**

1. **Preparar no Templo:** rodar `python automato/camadas/prepara.py --forcar` e `python automato/camadas/cuidar.py` (para repor pães na Padaria e conjurar `detect invisibility`).
2. **Ir até a Vila dos Smurfs (`help vila dos smurfs`):**
   - Do Templo de Midgaard: `s, s` até `A Praça do Comércio`.
   - Seguir `e` pela `Rua Principal`, passar pelo `Portão Leste de Midgaard` (`open portao leste` se fechado) e avançar `e` pela `Estrada do Rei` conferindo `exits` a cada sala até ver ao **norte** `A Entrada Para a Vila dos Smurfs`.
3. **Mapear a Vila dos Smurfs e localizar `o smurf minerador`:**
   - Entrar ao norte e usar `where minerador` / `where smurf`.
   - Ao encontrar `o smurf minerador`, aguardar a fala dele, responder `say sim` e **permanecer na sala até o briefing inteiro terminar** (usar `historico dizer` para confirmar todas as instruções).
4. **Cumprir todas as etapas de `Uma Lição em Gargamel`:**
   - Usar `consider` antes de cada novo tipo de mob (incluindo Gargamel/Azrael).
   - Combater à distância com `lightning bolt` e `wimpy 45`.
   - Atualizar `mapa.json` com as salas da Vila dos Smurfs (fundindo com `digerir_mapa.py` sobre o **corpus inteiro** + `fundir_mapa.py`).

---

## 6. NÃO REPITA

1. **Sair da sala de um NPC de autoquest antes da última fala do briefing** — aguarde ~15 segundos de silêncio e confira `historico dizer`.
2. **Confiar que `score tudo` muda ao fim de toda sub-etapa de abate** — volte ao NPC ao atingir a cota pedida.
3. **Entrar em `Adentro do Milharal Destruído` ou `Passo-Em-Falso`** — armadilhas mortais (DT) conhecidas; se aparecer `"Você percebe que há algo perigoso por perto!"`, pare imediatamente.
4. **Usar `onde`** — não existe no servidor; use `where <alvo>`.
5. **Executar `quit` com missão em andamento** — zera o progresso da autoquest; encerre sempre com `save`.
6. **Vender armaduras** (proibido pela diretiva §15) ou **digerir corpus parcial** do mapa.

---

## 7. Ferramentas e comandos

```bash
python scripts/mandabala.py                         # lê o plano vigente
python automato/camadas/prepara.py --forcar         # banco, pão, água e revisão de doações
python automato/camadas/cuidar.py                   # fome, sede, armor e detect invisibility
python automato/acoes/mapear.py                     # mapeamento supervisionado
python scripts/devolutiva.py                        # auditoria de fim de sessão (obrigatória)
```

---

## 8. Devolutiva técnica

> **Obrigatória** (LEIA.md §8), e **cobrada** por `python scripts/devolutiva.py`.

| Descobri | Registrei em | O quê |
|---|---|---|
| **mapa** | **`mapa.json`** ✅ | Atualizadas as salas `fazenda_milharal_borda`, `fazenda_entrada_casa`, `fazenda_sala_estar` e `fazenda_cozinha` com as quatro espécies de monstros do milharal (`invasor`, `esfomeado`, `agressivo`, `lider`) e os três membros da família (`O dono da fazenda`, `Mulher desesperada`, `Um garoto`) confirmados ao vivo em `evidence/dia156g.json`. |
| **referência do servidor** | **`maquina/verificacoes.md`** ✅ | Registrados: (1) a exigência de aguardar a 13ª fala de `O Pacificador` antes de deixar a sala; (2) o comportamento de `score tudo` nas Etapas 1–3; (3) a marcação de missão única em `autoquest todas` (`Concluída`) e remoção de `autoquest listar`; (4) a rota de `help vila dos smurfs` (`MAPA 33`); e (5) a ficha de `um belo cinturão de rodeio`. |
| **fato do mundo** | **`conhecimento.md` §40** ✅ | Documentado o passo a passo completo das 4 etapas de `Problemas Agrícolas`, as falas literais de `O fazendeiro`, os atributos do `belo cinturão de rodeio`, a comprovação de conclusão no catálogo e o endereço da Vila dos Smurfs para o Capítulo 08. Atualizados também `state.json`, `missoes.json` e `capitulos.json` (Capítulo 07). |
| **erro do motor** | **`automato/CHANGELOG.md` v1.6.1** ✅ | Corrigido `count_mobs(text)` em `automato/rotinas/milharal.py`, que filtrava apenas por `'está aqui'` ou `'está jogado'`, ignorando `um monstro invasor` (*"Uma estranha criatura, verde e peluda, está procurando algo."*) e contando corpos no chão. |

---

## 9. Como encerrar a sua sessão

1. `cuidar.py` até `exit 0`; **`save`** no Templo — **nunca `quit`** com missão ativa.
2. **Criar `planos/plano010.md`** com o modelo do `LEIA.md`, **incluindo a §8 Devolutiva técnica**.
3. **Rodar `python scripts/devolutiva.py` e resolver as FALHAS.** Só encerre com **0 falhas**.
4. Se fechar capítulo: `capitulos.json` com `parts` contendo **`source_kind`**, **`date`** e **`evidence`**.
5. `sync_hero.py --hero grebolius` **e** `--check`; `verificar.py` **18/18**; `check_project.py` **0 erros**.
6. Bloco em `docs/agentes/registro_de_evolucao.md` (**append-only**) com **modelo/versão**.
7. Publicar **só se pedido**, **sinalizando quem fez** — e respeitando o **`AGENTS.md` §12**.
