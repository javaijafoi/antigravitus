# Plano do Capítulo 03 — "Três Ofícios"

**Goal do capítulo:** concluir **três missões quaisquer**, sem repetir nenhuma já feita.
**Estado:** em curso (aberto no Dia 141). **Nenhuma das três concluída ainda.**
**Onde estamos:** Dia 155.

---

## 1. O que NÃO pode ser repetido (já concluídas — conferido no servidor)
| Missão | Como se confirma |
|---|---|
| **Limpando Monstros** | `autoquest todas` → *Concluída* |
| **Ninguém Segura Esse Bebê** | `autoquest todas` → *Concluída* (estava sem registro; concluída antes do Dia 98) |
| `coleira-dragao` e `altruismo` | missões antigas, não-autoquest, registradas como concluídas |

**Como conferir de novo:** `python automato/nucleo/driver/play.py "autoquest todas"` e ler o log em `automato/runtime/`.

## 2. As três missões candidatas (em ordem de viabilidade)

### A) Problemas Agrícolas — oficial, nível 10-40 · **a mais perto**
- **Objetivo:** eliminar os monstros invasores do milharal.
- **Onde:** fazenda, a oeste de Jareth (rota completa na seção 3).
- **Estado:** **aceita** (Pacificador, Dia 147). Já foram abatidos **4 invasores** (1 no Dia 153 e **3 no Dia 155**).
- **Como entregar:** falar com o **Pacificador** (Praça do Templo) e/ou o **fazendeiro** (na casa da fazenda).
  No Dia 99 o fazendeiro não respondeu aos gatilhos — testar `say sim`, `ask fazendeiro` e, se preciso, voltar ao Pacificador.
- **Ferramenta:** rotina `milharal` do automato (já chega e caça).
- **Cuidado:** o milharal tem **tipos diferentes** de monstro (esfomeado, agressivo, …) e uma sala com armadilha mortal ("Adentro do Milharal").

### B) Dicas Mágicas — oficial, até nível 29 · **travada num gatilho**
- **Objetivo:** seguir as instruções do **mago aventureiro** (Bar dos Magos).
- **Estado:** em andamento. O servidor diz *"Você deve responder 'sim'"*; responder limpa a instrução, mas **ela volta**.
  O mago já disse *"Vamos lá, então. Preste muita atenção."*
- **Hipóteses (testar uma por vez):**
  1. a resposta certa a alguma pergunta pode ser **"não"**, não "sim" (`help autoquest`: *"a maioria… apenas sim ou não"*);
  2. o passo pode exigir **uma magia específica** conjurada na sala certa (`detect magic`, `identify`, `invisibility`);
  3. pode exigir **estar no Laboratório** (a leste do Bar) com a magia ativa.

### C) Novela dos Novatos — oficial, nível 1-30
- **Objetivo:** iniciar o encadeamento com **"o novato esperto"**, que "habita as praças e encruzilhadas civis".
- **Estado:** descoberta (Dia 83). Varridas as Praças do Templo, Comércio e Comum sem encontrá-lo.
- **Próximo passo:** procurar em **outras encruzilhadas** (Rua Principal, Praça Comum a leste/oeste, becos) com `mapear.py`.

### D) Uma Lição em Gargamel — oficial, nível 20-80 · **missão não catalogada antes do Dia 142**
- **Objetivo:** iniciar com **"o smurf minerador"**.
- **Estado:** descoberta (via `autoquest todas`). **Sem pista de onde fica** — candidatos: minas, colinas, arredores de Midgaard/Jareth.

## 3. Rotas que já estão resolvidas (não redescobrir)
**Templo → Milharal** (confirmada ao vivo; detalhe no `conhecimento.md` §23-24 e no mapa):
```
Templo -n5-> Grande Campo -n,e,n-> O Começo da Estrada -n6-> Aclive
      -l6-> Portão Oeste de Jareth - Centro - Portão Leste -> A Entrada da Floresta
      -n,n,l,l-> labirinto do bosque (buscar a sala com "O Pequeno Bosque" a LESTE)
      -n,n-> A Entrada da Fazenda -o-> Pequena Estrada -o-> Fim da Estrada -o-> MILHARAL
```
**Volta:** `recall` (grátis até o nível 70) — é o que a rotina faz.

## 4. Ferramentas do automato para este capítulo
| Comando | Para quê |
|---|---|
| `python automato/nucleo/driver/live_daemon.py` | subir a sessão viva (obrigatório antes de tudo) |
| `python automato/acoes/mapear.py "n,n,l,s"` | **mapear à mão** uma sequência, vendo cada sala |
| `python automato/acoes/mapear.py --buscar "marca"` | procurar uma sala/saída pelo nome, gravando o caminho |
| `python automato/camadas/vigia.py` | diagnóstico do estado (fome, sede, morte, travamento) |
| `python automato/camadas/prepara.py` | alimentar, hidratar, guardar ouro no banco, dormir |
| `python automato/rotinas/milharal.py` via `trabalhar.py --rotina milharal` | caçar os invasores |

## 5. Regras permanentes (do autor)
- **Proibido vender armaduras** (Torre Negra ou peão) — prejuízo comprovado;
- **Nada de metajogo** nas descrições dos capítulos (o detalhe técnico fica nas descrições dos dias);
- **Nunca** rodar robô sem supervisão; ler o log a cada minuto e matar o job se algo piorar.

## 6. Decisão pendente do autor
**Armadura da Torre Negra** (60 kg, amaldiçoada, presa ao corpo): continuar carregando (custo zero, mas quase sem espaço para espólio)
ou pagar **8.509** para desamaldiçoar e doar (libera 60 kg, custo puro).

---

## 7. O plano de execução (o que o agente deve fazer, em ordem)
1. **Fechar Problemas Agrícolas:** rodar a rotina `milharal` (agora funcional) com supervisão até os abates bastarem,
   depois **falar com o Pacificador e com o fazendeiro** para confirmar a entrega. **Contar como missão 1.**
2. **Destravar Dicas Mágicas:** testar as três hipóteses da seção 2-B, uma por vez, registrando o que o servidor responde.
3. **Abrir Novela dos Novatos:** procurar "o novato esperto" nas encruzilhadas com o mapeador. **Missão 2 ou 3.**
4. **Gargamel:** procurar "o smurf minerador" (minas/colinas). **Missão 2 ou 3.**
5. **Ao concluir a terceira:** escrever a crônica de fechamento, fechar o capítulo no `add_chapter.py` e publicar.
