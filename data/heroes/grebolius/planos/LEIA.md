# Planos — como funciona

> **O que é.** Cada sessão de agente deixa **um plano numerado**. O autor chega, diz
> **"executa o plano 98"**, e quem pegar continua **exatamente de onde o anterior parou** — sem
> redescobrir nada, sem repetir caminho errado, sem perder conquista.

## As três regras

1. **Nunca edite um plano antigo.** Eles são **append-only**. Errou? Crie o próximo e diga no que o
   anterior falhava. *(Mesma regra do `docs/agentes/registro_de_evolucao.md`.)*
2. **Sempre crie um novo, com o próximo número.** Não existe "atualizar o plano" — existe
   **plano 002**.
3. **Todo plano diz quem o fez.** Modelo/versão no cabeçalho. Sem isso não se sabe a quem perguntar, nem
   se compara desempenho entre modelos.

## Numeração e nome

```
data/heroes/<heroi>/planos/plano001.md
                          plano002.md
                          ...
                          plano098.md
```

**Três dígitos, com zeros à esquerda** — para a ordem alfabética ser a ordem cronológica, e para caber
até 999 planos sem renomear nada.

**Herói diferente, pasta diferente:** `data/heroes/antigravitus/planos/plano001.md` é o plano 1 **do
outro herói**. O número é local ao herói.

## Ordem de leitura de quem chega

**O autor diz "mandabala" e roda:**

```bash
python scripts/mandabala.py
```

O script acha o **plano mais alto**, confere a numeração e a autoria, e imprime **num bloco só**: a
ordem de leitura, as regras que não se negociam e o **conteúdo integral do plano**. Não edita nada, não
joga, não publica — só lê e mostra.

| Comando | O que faz |
|---|---|
| `python scripts/mandabala.py` | o plano vigente, com a ordem de leitura |
| `python scripts/mandabala.py --listar` | todos os planos, de todos os heróis, com autor e objetivo |
| `python scripts/mandabala.py --numero 3` | um plano específico (avisa se não for o mais recente) |
| `python scripts/mandabala.py --hero <id>` | escolhe o herói |
| `python scripts/mandabala.py --so-caminho` | imprime só o caminho, para usar em script |

**Ele avisa sozinho** quando: a numeração tem **lacuna** (plano removido ou renomeado), o plano pedido
**não é o mais recente**, ou o plano **não declara autoria**.

**Sem o script, a ordem é esta:**

1. `AGENTS.md` (raiz) — como trabalhar neste repositório
2. **O plano mais alto da pasta `planos/`** — é o seu ponto de partida
3. `docs/agentes/registro_de_evolucao.md` — o que mudou na ferramenta e por quê
4. `data/heroes/<heroi>/diretiva_de_jogo.md` — **as regras de jogo. Antes de jogar**

## Modelo do plano

Copie isto. O que **não** pode faltar: número, data, **autor**, estado exato, o **próximo passo único**,
e o que **não** repetir.

> ## ⚠️ A **DEVOLUTIVA TÉCNICA** é obrigatória — e é cobrada
>
> **Um capítulo jogado com a devolutiva técnica incompleta é um capítulo pela metade.** O
> `AGENTS.md` §5 diz **onde** cada descoberta vai; o que faltava era **alguém cobrar**. Agora cobra:
> o `scripts/mandabala.py` **avisa** se o plano vigente não tiver a seção
> **`## Devolutiva técnica`**.
>
> **Toda sessão de jogo responde a estas quatro perguntas, mesmo que a resposta seja "nada":**
>
> | Descoberta | Vai para | Pergunta |
> |---|---|---|
> | **Sala, saída, atalho** | **`mapa.json`** | Andei por onde o mapa não sabia? O mapa está errado? |
> | **Comando, magia, mensagem do servidor** | **`maquina/verificacoes.md`** | Vi o servidor responder algo que a referência não tem? |
> | **NPC, item, preço, perigo do mundo** | **`conhecimento.md`** | Descobri um fato do mundo que ninguém registrou? |
> | **Como o motor erra** | **`automato/DECISOES.md`** / `CHANGELOG.md` | O motor me atrapalhou de um jeito novo? |
>
> **O sintoma de que isto foi ignorado:** a descoberta existe **em prosa** ("*o mapa revelado: fechando
> os anéis*") e **não existe no artefato** (`mapa.json` sem as arestas). Aconteceu no Dia 156 — o
> agente andou, descobriu que quatro salas eram anéis de mão dupla, escreveu o achado no
> `conhecimento.md`, **e não tocou no mapa.**
>
> **Nenhum validador pega isso:** o `check_project.py` confere **estrutura**, não **cobertura**. Ele não
> sabe que uma caminhada aconteceu. **Por isso a cobrança tem de ser explícita, e está aqui.**

```markdown
# Plano NNN — <capítulo ou objetivo>

| | |
|---|---|
| **Criado em** | AAAA-MM-DD · Dia <n> |
| **Por** | <modelo/versão> |
| **Herói** | <id> |
| **Objetivo** | <uma frase> |
| **Sessão encerrada?** | sim/não — o que ficou rodando |

## 1. Onde o objetivo está
<o que está feito, o que falta, e as duas ou três frases que resumem>

## 2. Estado exato
<vida/mana/ouro/mortes/local/mapa — números, não adjetivos>

## 3. O que já foi descoberto
<rotas verificadas, endereços, padrões — o que o próximo NÃO precisa redescobrir>

## 4. Os bloqueios, e o que já foi tentado
<com o resultado de cada tentativa>

## 5. O próximo passo, e só ele
<uma ação concreta>

## 6. NÃO REPITA
<caminhos já provados errados>

## 7. Ferramentas e comandos
<o que existe e como se usa>

## 8. Devolutiva técnica  ← OBRIGATÓRIA (o mandabala.py avisa se faltar)
| Descobri | Registrei em | O quê |
|---|---|---|
| mapa | `mapa.json` | <salas/arestas corrigidas, ou "nada"> |
| referência do servidor | `maquina/verificacoes.md` | <comando/mensagem nova, ou "nada"> |
| fato do mundo | `conhecimento.md` §NN | <NPC/item/perigo, ou "nada"> |
| erro do motor | `automato/DECISOES.md` | <o que travou, ou "nada"> |

## 9. Como encerrar a sua sessão
<a obrigação, igual à que gerou este plano>
```

## Por que assim

- **Numerado**: o autor pede "o plano 98" e todos sabem qual é. Sem ambiguidade de "o plano atual".
- **Append-only**: o histórico não se perde. Dá para ver **quando** uma abordagem foi abandonada e
  **por quem** — e cobrar o mesmo erro duas vezes fica visível.
- **Com autoria**: com vários agentes na mesma árvore, saber quem escreveu é o que permite perguntar.
- **Um por sessão**: se cada um editasse o mesmo arquivo, a informação do anterior sumiria — e é
  exatamente essa informação que evita refazer seis rodadas de busca.
