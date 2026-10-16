# Briefing — Capítulo 05 (para o agente que assume)

> ## ⛔ **OBSOLETO — NÃO USE ESTE ARQUIVO**
>
> **Aviso acrescentado depois, por `deepseek-flash`.** Este briefing foi escrito para **quem fosse
> assumir o Capítulo 05**. O capítulo **fechou** (as duas autoquests concluídas, `status: concluido`), e
> ele foi **substituído pelo esquema de planos numerados**:
>
> ```bash
> python scripts/mandabala.py      # a ordem de leitura + o plano vigente, inteiro
> ```
>
> **Além de obsoleto, ele está errado no ponto principal:** o *"próximo passo"* dizia
> *"vigiar os novatos até um deles FALAR"*. **Nenhum precisava falar** — o esperto **já tinha falado**, e
> a instrução (`ajuda mapas`) estava gravada nas **linhas 5535–5562** de um transcript já aberto.
>
> **O que vale hoje:** [`planos/plano004.md`](planos/plano004.md) e
> [`../../../../automato/DECISOES.md`](../../../../automato/DECISOES.md) §9.
>
> **Fica no repositório como registro** — o erro visível ensina mais que o erro apagado.

## Comece lendo, nesta ordem

1. **`AGENTS.md`** (raiz) — como trabalhar aqui. Regra zero: diga seu modelo/versão no relatório, na
   evidência e no commit (`[agente: ...]`), e registre sua mudança em
   `docs/agentes/registro_de_evolucao.md`.
2. **`docs/agentes/registro_de_evolucao.md` §9** — **o handoff do Capítulo 05.** É o mais importante:
   estado real, bloqueios, rotas verificadas e o que **não** repetir.
3. **`data/heroes/grebolius/diretiva_de_jogo.md`** — as regras de jogo. **Leia antes de jogar.**
4. **`data/heroes/grebolius/plano_capitulo_05.md`** — o que o capítulo é.
5. **`data/heroes/grebolius/andarilho_e_novatos.md`** — todos os textos das duas missões, literais.

---

## O objetivo, em uma linha

**Fechar as duas autoquests**, que **já estão ativas**:

```
[Autoquests em andamento]
Novela dos Novatos: Você deve dizer algo ao personagem.
Limpando Monstros: Você deve matar criatura.
```

**Não precisa iniciá-las.** Isso já foi feito.

---

## Os dois bloqueios

| Missão | O que falta |
|---|---|
| **Limpando Monstros** | **Abates.** A zona 186 seca e repovoa devagar. Ronda boa **esvazia** a masmorra |
| **Novela dos Novatos** | **Achar o que dispara o `say`.** Cobertos 4 dos 5 novatos, com ~35 frases — nenhum reagiu |

**A pista mais forte:** em **toda** autoquest do DeBo, **o NPC fala primeiro** e a personagem responde
`sim`. Nenhum novato **falou** em sessão alguma.

➡️ **Próximo passo sugerido: vigiar os novatos até um deles FALAR.** Não falar no vácuo.

---

## Três coisas que economizam rodadas

1. **`docs/circlemud/`** — a Zona dos Novatos **é o `186.wld` do CircleMUD padrão**. Os docs dão
   **mob por mob, sala por sala**, com o item que cada um carrega. Foi o que resolveu seis rodadas de
   busca. **Antes de varrer o mundo à mão, olhe os docs.**
2. **`diretiva_de_jogo.md`** — `burning hands` é o dano principal; **corpo a corpo está desligado**
   (`allow_verified_melee = False`); `wimpy 45`.
3. **`save`, nunca `quit`** — `quit` com missão em andamento **zera o progresso**. Queda de conexão
   **não** zera (verificado).

---

## Não persiga

- **A coleira do dragão** — o autor confirmou: **a missão do dragão já foi feita.** Pista falsa.
- **O Andarilho Misterioso** (*"Energias obscuras… Uma Cela de Prisão"*) — é **evento de mundo**
  (`help andarilho`), não pista da missão.
- **Vender armaduras** — diretiva do autor, proibido.

---

## Estado no momento da passagem

Nível 20, Mago Elfo. **113/113 hp, 260/260 mana.** Ouro: 340 na mão + 1.142 no banco. **7 mortes.**
Mapa: **381 salas.** As duas missões ativas. Daemon do driver na porta 14888 (runtime fora do git).

**Publicação:** `check_project.py` (0 erros) → `sync_hero.py` → `publish_daily.py --publish --push`.
A árvore é **compartilhada com outras conversas do mesmo agente** — confira `git status` antes e depois.
