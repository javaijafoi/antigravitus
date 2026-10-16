# Rotinas de trabalho (a partir do Dia 148)

## A ideia (proposta do autor)
O herói não tem "um robô": tem **rotinas** que ele sabe executar de ponta a ponta.
Cada rotina é aprendida, ajustável com o tempo, e protegida por camadas de segurança.

## As camadas
| Camada | Arquivo | Papel |
|---|---|---|
| **Vigia** | `scripts/local/vigia.py` | Lê a **cauda do log do daemon** (leitura pura: não manda comando, não interfere) e devolve um diagnóstico: `OK / FOME / SEDE / VIDA_BAIXA / MORTA / TRAVADO / SEM_SESSAO`. |
| **Prepara** | `scripts/local/prepara.py` | O arrumador: come, bebe, **deposita o ouro no banco do Templo**, dorme para recompor e volta ao Templo. |
| **Trabalhar** | `scripts/local/trabalhar.py` | O despachante: `--rotina X` carrega `rotinas/X.py` e chama `executar()`. `--listar` mostra o catálogo. |
| **Turno** | `scripts/local/turno.py` | O encarregado: roda o vigia, manda o prepara consertar quando precisa, sobe a rotina em segundo plano e **pergunta ao vigia a cada minuto**; se houver problema, **mata a rotina** e recomeça. |

## O contrato de uma rotina
```python
NOME = 'milharal'
DESCRICAO = '...'
def executar() -> bool:
    run('wake'); run('stand')
    ...
    voltar_ao_templo(); run('save')
    return True
```
Ela **sempre parte do Templo** (o ponto de encontro) e **sempre volta para lá**, salvando no fim.
É isso que torna as rotinas reiniciáveis: qualquer interrupção é recuperável com `prepara.py`.

## Rotinas registradas
| Rotina | O que faz | Estado |
|---|---|---|
| **milharal** | Caça os monstros invasores (missão *Problemas Agrícolas*) e traz espólio. Trajeto: checkpoints + rota gravada do bosque. | funcional (herdada do motor.py) |
| ~~**xadrez**~~ | ~~Coleta armaduras de peão e vende (150 cada)~~ | **SUSPENSA no Dia 150 por diretiva do autor: "perdemos mais dinheiro do que ganhamos com elas". Guardada em `rotinas/_suspensas/`. Não reativar sem ordem expressa.** |
| **esgoto** | Reconhece os esgotos sob o Laboratório com cuidado, sem entrar em luta desfavorável. | em teste |

## Proteções ativas
1. **Guarda de repetição** (`guarda.py`, dentro de `base.run`): mesma resposta 3× seguidas → `recall` + `save` + saída (código 9). Ignora comandos benignos (buy/eat/drink/look/score...).
2. **Vigia de minuto em minuto** (`turno.py`): lê o log sem interferir e derruba a rotina se algo piorar.
3. **Banco**: o ouro fica depositado no Templo (`deposit`), com reserva de 300 na mão — a morte não leva o que está guardado.
