# Plano 014 — Capítulo 09: Concluir 'Uma Lição em Gargamel' e Atingir o Nível 50

| | |
|---|---|
| **Criado em** | 2026-10-17 · Dia 156 |
| **Por** | **`Gemini 3.8 Flash (High)`** |
| **Herói** | `grebolius` |
| **Capítulo** | **09 — "O Preço Não Se Mata com Raio"**, `em_curso` em `capitulos.json` (`id=9`), `continues_chapter: 8` |
| **Objetivo** | **Concluir a missão 'Uma Lição em Gargamel' E avançar até o Nível 50** |
| **Sessão encerrada?** | **Sim** — Plano e metadados de capítulo ajustados conforme diretiva expressa do autor; personagem em repouso seguro no Templo |

> **Leia o [`LEIA.md`](LEIA.md) primeiro.** **Este arquivo não se edita** — quem vier cria o **`plano015.md`**.
>
> **Antes de encerrar sua sessão, rode `python scripts/devolutiva.py`** — obrigatório (0 falhas).

---

## 0. Diretiva do Autor: O Escopo do Capítulo 09

> **Diretiva do autor:** *"o capitulo nove é terminar a missão e chegar no level 50"*

O Plano 013 tratava o Capítulo 09 apenas como o término burocrático da poção e do minerador. A diretiva do autor unifica a narrativa da expedição com o grande salto de poder de Grebolius:
1. **Conclusão integral de `Uma Lição em Gargamel`:** farmar o ouro restante, comprar a poção de Clariss, receber o jarro brilhante com o Alquimista, entregá-lo ao minerador e desvendar o mistério de Papai Smurf no Covil de Gargamel.
2. **Escalada até o Nível 50:** transição da faixa de novato/aprendiz para o patamar veterano, investindo os 68 treinos acumulados e migrando de zonas de caça conforme o teto de nível.

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
  4. Grebolius tem **4.229 moedas** na mão (faltam **5.521 moedas**).
  5. Atrás da porta trancada do Covil de Gargamel está **Papai Smurf** (`where smurf`).

### Pilar B — A Escalada rumo ao Nível 50
- Grebolius está no **Nível 28** com **4.000.001 EXP** (próximo nível em 4.500.000).
- Possui **68 sessões de treino** acumuladas na Mestre dos Feiticeiros.
- Atingir o Nível 50 exige planejar a rota de EXP pós-nível 30 (onde a Área dos Novatos deixa de pontuar).

---

## 2. Estado exato

| Atributo | Valor verificado |
|---|---|
| **Personagem** | Grebolius, Mago Elfo (1ª encarnação) |
| **Nível** | **28** |
| **Vida / Mana / Movimento** | **178/178 · 340/340 · 141/141** |
| **Experiência** | **4.000.001** (meta Nv 29: 4.500.000) |
| **Ouro** | **4.229 na mão · 0 no banco** (faltam 5.521 para a poção) |
| **Mortes** | **8** (nenhuma nova) |
| **Classe de Armadura** | **137** (103 base + 34 de `armor`) |
| **`wimpy`** | **45** |
| **Treinos** | **68 sessões acumuladas** |
| **Local** | **O Templo de Midgaard** (sono e save confirmados) |
| **Provisões** | **5 pães recheados** dentro da *mochila de Pellinore*, cantil cheio |

> 💡 **Nota sobre a fome (correção do Plano 013):** O Plano 013 alertava sobre fome sem comida; a fotografia documental de `dia156j.json` comprova que Grebolius comprou **5 pães recheados** (guardados dentro da mochila de Pellinore) antes de dormir. Ao acordar, basta `get pao mochila` e `eat pao`.

---

## 3. O que já foi descoberto e resolvido

1. **Concorrência de autoquests no Alquimista resolvida:** O Alquimista não troca o jarro se `Limpando Monstros` estiver ativa. Como o ciclo foi entregue no Nível 28 (com ganho de 94.227 EXP e manto), **a janela está livre**. **NÃO reinicie Limpando Monstros.**
2. **Rotas consolidadas:**
   - **Vila dos Smurfs:** Templo -> sul, sul (Praça do Comércio) -> 8x leste -> norte -> Entrada Para a Vila dos Smurfs.
   - **Clariss em Jareth:** Templo -> portão oeste -> Jareth -> Avenida Floris -> *As Misturas de Clariss*.
   - **Milharal (Farm):** Rota testada no Capítulo 07/08 via floresta e fazenda (`conhecimento.md` §16).
3. **Economia de farm comprovada:** Os monstros do milharal rendem 50 a 120 moedas por abate (`autoloot`). ~110 abates cobrem com folga as 5.521 moedas que faltam e já adiantam o Nível 29.

---

## 4. Roteiro de Execução em Duas Fases

### Fase 1: Desfecho da Missão dos Smurfs
1. **Acordar e comer:** `wake`, `stand`, `get pao mochila`, `eat pao`.
2. **Levantar 5.521 moedas:**
   - **Opção recomendada:** Farm controlado no Milharal via `automato/rotinas/milharal.py` (ou missões ativas liberadas de nível alto: *Cuidado Com o Chacal* Nv 22+, *QuizBo!* Nv 25+).
   - Manter cautela estrita: não entrar em `Adentro do Milharal Destruído` (DT).
3. **Comprar a poção:** Ir a *As Misturas de Clariss* em Jareth com 9.800 moedas e executar `buy pocao`.
4. **Troca do Jarro:** Ir a *A Sala do Alquimista* (Escola de Midgaard), conferir `score tudo` (verificar se objetivo é entregar objeto), `give pocao alquimista` e aguardar o diálogo completo até receber `o jarro brilhante`.
5. **Entrega ao Minerador:** Levar o jarro a `o smurf minerador` no Fim do Túnel sob o Poço Smurf (`give jarro minerador`).
6. **Investigação do Covil de Gargamel:** Ir ao castelo ao norte da Vila dos Smurfs e investigar a porta trancada de Papai Smurf (`where smurf`). *Cuidado: Gargamel e Azrael estão lá; não atacar de frente sem consider.*

### Fase 2: A Rota rumo ao Nível 50
1. **Investimento das 68 sessões de treino:**
   - Visitar a Mestre dos Feiticeiros no Laboratório dos Magos.
   - Treinar as magias disponíveis para 95%+ (fortalecer feitiços de dano direto e utilitários).
2. **Transição de Zonas de Caça por Faixa de Nível:**
   - **Nível 28–35:** Milharal Destruído (mobs de nível 10 a 40 continuam rendendo EXP rápida e ouro abundante).
   - **Nível 35–45:** Esgotos intermediários (verificar com `consider` alvos viáveis, evitando cobras mortais e o Dragão Vermelho do Covil do Dragão) e arredores da Floresta de Jareth.
   - **Nível 45–50:** Zonas periféricas e masmorras de nível veterano catalogadas no `mapa.json` (511 salas).
3. **Protocolo de Sobrevivência Veterana:**
   - `wimpy 45` sempre ativo.
   - `armor` (+34) e `detect invisibility` sempre renovados.
   - Monitoramento contínuo de mana: recarga por sono (`sleep`) de ~80s quando mana < 80.
   - Uso imediato de `word of recall` / poção de retorno em emboscadas.

---

## 5. O próximo passo imediato, e só ele

> **Acordar no Templo, alimentar-se com o pão da mochila, deslocar-se ao Milharal e farmar as 5.521 moedas restantes para atingir 9.800 de ouro vivo.**

---

## 6. NÃO REPITA

1. **Não reiniciar `Limpando Monstros`** enquanto a poção não estiver trocada pelo jarro.
2. **Não vender armaduras** (Diretiva do autor §15: Torre Negra e armaduras de peão são proibidas de vender).
3. **Não usar `quit` com missão em andamento** (apaga o progresso; encerramento é sempre `save` e `sleep`).
4. **Não inventar comandos em português** (`where`, não `onde`; direções `n, s, e, w`).
5. **Não abrir a porta do Covil de Gargamel sem `consider`** (Azrael e Gargamel são perigosos; um dragão já abateu 135 HP em um turno).
6. **Não caçar com fome ou sede** (bloqueia regeneração e causa perda de HP).

---

## 7. Ferramentas e Comandos

- `python scripts/mandabala.py` — exibe o plano vigente e status.
- `automato/rotinas/milharal.py` — rotina supervisionada de caça no milharal.
- `python scripts/check_project.py` — validação de integridade documental.
- `python scripts/devolutiva.py` — conferência obrigatória antes de encerrar.

---

## 8. Devolutiva técnica

| Descobri | Registrei em | O quê |
|---|---|---|
| **mapa** | `mapa.json` | PENDENTE: 4 arestas de anéis de mão dupla dos esgotos documentadas em prosa no Dia 156 aguardam consolidação no JSON. |
| **referência do servidor** | `maquina/verificacoes.md` | PENDENTE: Nenhuma nova mensagem bruta de servidor nesta sessão de alinhamento de plano. |
| **fato do mundo** | `capitulos.json` id=9 ✅ | **Atualizado o Capítulo 09** com a diretiva do autor: meta expandida para concluir `Uma Lição em Gargamel` e atingir o Nível 50. |
| **erro do motor** | `automato/DECISOES.md` | Nada nesta sessão; motor permaneceu offline e estável. |

---

## 9. Como encerrar a sua sessão

1. `cuidar.py` até `exit 0`; confirmar `save` e `sleep` no Templo.
2. Criar `planos/plano015.md` mantendo o histórico append-only.
3. Executar `python scripts/devolutiva.py` e resolver eventuais falhas.
4. Rodar `python scripts/check_project.py` e testes unitários.
5. Registrar o bloco no livro-razão (`docs/agentes/registro_de_evolucao.md`).
