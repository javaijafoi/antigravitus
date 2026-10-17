# Plano 015 — Capítulo 09: Reta Final do Farm de Ouro (7.189/9.800), Poção de Clariss e Rumo ao Nível 50

| | |
|---|---|
| **Criado em** | 2026-10-17 · Dia 156 (sessão 2) |
| **Por** | **`Gemini 3.8 Flash (High)`** |
| **Herói** | `grebolius` |
| **Capítulo** | **09 — "O Preço Não Se Mata com Raio"**, `em_curso` em `capitulos.json` (`id=9`), `continues_chapter: 8` |
| **Objetivo** | **Completar as 2.611 moedas restantes no Milharal, comprar a poção aquosa em Clariss, entregar ao Alquimista/Minerador e avançar ao Nível 50** |
| **Sessão encerrada?** | **Sim** — 8 rodadas de caça executadas no Milharal (57 abates); ouro elevado de 4.229 para 7.189 moedas; desconexão por socket EOF pelo servidor DeBo; processo live_daemon finalizado |

> **Leia o [`LEIA.md`](LEIA.md) primeiro.** **Este arquivo não se edita** — quem vier cria o **`plano016.md`**.
>
> **Antes de encerrar sua sessão, rode `python scripts/devolutiva.py`** — obrigatório (0 falhas).

---

## 0. Diretiva do Autor: O Escopo do Capítulo 09

> **Diretiva do autor:** *"o capitulo nove é terminar a missão e chegar no level 50"*

O Plano 014 iniciou a execução ao vivo da diretiva:
1. **Fase 1 (Em andamento avançado):** Levantadas 7.189 moedas de ouro (saltando de 4.229 para 7.189 em 57 abates). Faltam apenas **2.611 moedas** para atingir a meta de 9.800 (9.750 da poção de Clariss + 50 de margem). Em seguida, troca do jarro brilhante com o Novato Alquimista e entrega ao smurf minerador.
2. **Fase 2:** Investimento das 68 sessões de treino acumuladas na Guilda dos Magos e transição para zonas de caça pós-nível 30 rumo ao Nível 50.

---

## 1. Onde os dois pilares estão

### Pilar A — A Missão `Uma Lição em Gargamel` (ATIVA)
```
[Autoquests em andamento]
Uma Lição em Gargamel: Você deve entregar objeto ao personagem.
```

- **Estado da cadeia:**
  1. Minerador pediu o `jarro brilhante` sem machucar ninguém.
  2. O Novato Alquimista quer `uma poção aquosa` de Clariss em troca do jarro.
  3. Clariss (Avenida Floris, Jareth) vende por **9.750 moedas**.
  4. Grebolius possui **7.189 moedas** vivas no bolso (faltam **2.611 moedas**, ~5 rodadas de caça).
  5. Atrás da porta trancada do Covil de Gargamel está **Papai Smurf** (`where smurf`).

### Pilar B — A Escalada rumo ao Nível 50
- Grebolius está no **Nível 28** com **4.191.978 EXP** (faltam apenas **308.022 EXP** para o Nível 29).
- Possui **68 sessões de treino** acumuladas na Mestre dos Feiticeiros.
- Atingir o Nível 50 exige planejar a rota de EXP pós-nível 30 (onde a Área dos Novatos deixa de pontuar).

---

## 2. Estado exato

| Atributo | Valor verificado |
|---|---|
| **Personagem** | Grebolius, Mago Elfo (1ª encarnação) |
| **Nível** | **28** |
| **Vida / Mana / Movimento** | **178/178 · 340/340 · 141/141** |
| **Experiência** | **4.191.978** (meta Nv 29: 4.500.000, faltam 308.022) |
| **Ouro** | **7.189 na mão · 0 no banco** (faltam 2.611 para os 9.800) |
| **Mortes** | **8** (nenhuma nova nesta sessão) |
| **Classe de Armadura** | **137** (103 base + 34 de `armor`, 24h restantes) |
| **`wimpy`** | **45** |
| **Treinos** | **68 sessões acumuladas** |
| **Local** | **O Templo de Midgaard** (save confirmado antes da desconexão) |
| **Provisões** | **3 pães recheados na mochila de Pellinore**, **3 pães na mão**, cantil cheio de água cristalina |

---

## 3. O que já foi descoberto e resolvido

1. **Rendimento comprovado do Milharal:**
   - Em 8 rodadas, foram 57 abates confirmados de invasores, esfomeados, agressivos e 2 abates do líder dos monstros.
   - Rendimento líquido de +2.960 moedas e +191.977 EXP.
   - O servidor DeBo/CircleMUD recolhe moedas automaticamente ao morrer o mob (`autoloot`: 50 moedas em mobs comuns, 120 no líder).
2. **Motor `milharal.py` aprimorado e robusto:**
   - Contra-ataque a emboscadas no percurso: ao encontrar monstro hostil a caminho da fazenda, o bot conjura `lightning bolt` imediatamente, elimina a criatura e retoma a rota sem travar em "Não dá! Você está muito ocupado, lutando!".
   - Recuperação limpa de trânsito: adicionado `run('recall'); run('stand')` entre tentativas falhas de percurso.
3. **Concorrência de autoquests no Alquimista resolvida:**
   - `Limpando Monstros` foi entregue com sucesso no Dia 156 sem `quit`.
   - A janela para a entrega da poção aquosa a `O Novato Alquimista` está livre. **NÃO reinicie Limpando Monstros.**

---

## 4. Roteiro de Execução em Duas Fases

### Fase 1: Desfecho da Missão dos Smurfs
1. **Conectar o driver:** Iniciar `live_daemon.py` e verificar vitais/posicionamento no Templo de Midgaard.
2. **Completar as 2.611 moedas restantes:**
   - Executar ~5-6 rodadas de `automato/camadas/trabalhar.py --rotina milharal`.
   - Intercalar cada rodada com repouso (`sleep` no Templo por ~60-80s até 340 mana).
   - Manter wimpy 45 e conferir que o ouro atinja ≥9.800 moedas.
3. **Comprar a poção:**
   - Viajar a *As Misturas de Clariss* em Jareth (Avenida Floris) com 9.800 moedas.
   - Executar `buy pocao` (9.750 moedas).
4. **Troca do Jarro:**
   - Ir a *A Sala do Alquimista* (Escola de Midgaard).
   - Conferir `score tudo` (verificar se o objetivo vigente continua sendo "entregar objeto ao personagem").
   - Executar `give pocao alquimista` e aguardar o diálogo completo até receber `o jarro brilhante`.
5. **Entrega ao Minerador:**
   - Levar o jarro a `o smurf minerador` no Fim do Túnel sob o Poço Smurf (`give jarro minerador`).
6. **Investigação do Covil de Gargamel:**
   - Ir ao castelo ao norte da Vila dos Smurfs e investigar a porta trancada de Papai Smurf (`where smurf`).
   - *Cuidado: Gargamel e Azrael estão lá; não atacar de frente sem consider.*

### Fase 2: A Rota rumo ao Nível 50
1. **Investimento das 68 sessões de treino:**
   - Visitar a Mestre dos Feiticeiros no Laboratório dos Magos.
   - Treinar as magias disponíveis para 95%+ (fortalecer feitiços de dano direto e utilitários).
2. **Transição de Zonas de Caça por Faixa de Nível:**
   - **Nível 28–35:** Milharal Destruído (mobs de nível 10 a 40 continuam rendendo EXP rápida e ouro abundante).
   - **Nível 35–45:** Esgotos intermediários (verificar com `consider` alvos viáveis, evitando cobras mortais e o Dragão Vermelho do Covil do Dragão) e arredores da Floresta de Jareth.
   - **Nível 45–50:** Zonas periféricas e masmorras de nível veterano catalogadas no `mapa.json` (511 salas).

---

## 5. O próximo passo imediato, e só ele

> **Conectar o driver no Templo de Midgaard e rodar ~5 rodadas de `automato/camadas/trabalhar.py --rotina milharal` (intercaladas com sono para recarga de mana) até atingir 9.800 moedas de ouro.**

---

## 6. NÃO REPITA

1. **Não reiniciar `Limpando Monstros`** enquanto a poção não estiver trocada pelo jarro.
2. **Não vender armaduras** (Diretiva do autor §15: Torre Negra e armaduras de peão são proibidas de vender).
3. **Não usar `quit` com missão em andamento** (apaga o progresso; encerramento é sempre `save` e `sleep`).
4. **Não entrar em `Adentro do Milharal Destruído`** (Death Trap confirmada, Morte #5).
5. **Não abrir a porta do Covil de Gargamel sem `consider`** (Azrael e Gargamel são perigosos).
6. **Não caçar com fome ou sede** (bloqueia regeneração e causa perda de HP).

---

## 7. Ferramentas e Comandos

- `python scripts/mandabala.py` — exibe o plano vigente e status.
- `python automato/camadas/trabalhar.py --rotina milharal` — rotina supervisionada de caça no milharal.
- `python automato/camadas/vigia.py` — diagnóstico passivo do estado da personagem.
- `python automato/camadas/cuidar.py` — aplicação de alimentação, hidratação e armadura mística.
- `python scripts/check_project.py` — validação de integridade documental.
- `python scripts/devolutiva.py` — conferência obrigatória antes de encerrar.

---

## 8. Devolutiva técnica

| Descobri | Registrei em | O quê |
|---|---|---|
| **mapa** | `mapa.json` | PENDENTE: 4 arestas de anéis de mão dupla dos esgotos documentadas em prosa no Dia 156 aguardam consolidação no JSON. |
| **referência do servidor** | `maquina/verificacoes.md` | PENDENTE: Nenhuma mensagem nova de servidor; autoloot de moedas ao abater criaturas confirmado operacional. |
| **fato do mundo** | `conhecimento.md` | **Registrada a Seção 44** com o rendimento de 57 abates no milharal, saldo elevado a 7.189 moedas, 4.191.978 EXP e autoloot. |
| **erro do motor** | `CHANGELOG.md` | **Versão v1.6.3 registrada**: implementado contra-ataque a emboscadas no trânsito e recall limpo entre tentativas em `milharal.py`. |

---

## 9. Como encerrar a sua sessão

1. `cuidar.py` até `exit 0`; confirmar `save` e `sleep` no Templo.
2. Criar `planos/plano016.md` mantendo o histórico append-only.
3. Executar `python scripts/devolutiva.py` e resolver eventuais falhas.
4. Rodar `python scripts/check_project.py` e testes unitários.
5. Registrar o bloco no livro-razão (`docs/agentes/registro_de_evolucao.md`).
