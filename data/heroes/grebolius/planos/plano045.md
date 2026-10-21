# Plano 045 — Xeque-mate: terminar a cascata e entregar o Cetro do Rei Negro (que já temos, invisível)

| | |
|---|---|
| **Criado em** | 2026-10-21 · Dia 159 (sessão marcada Dia 160 nos registros) |
| **Por** | Claude Sonnet 5.5 (claude-sonnet-5-5) |
| **Herói** | grebolius |
| **Objetivo** | **Terminar a Xeque-mate**: entregar o Cetro do Rei Negro ao Bispo Branco, no passo "entregar objeto" |
| **Sessão encerrada?** | sim — Templo de Midgaard, `save` e `sleep` confirmados, driver parado, sem `quit`; a Xeque-mate está ativa em "matar criaturas" |

Substitui o plano 044 (meu antecessor, não é editado).

## 1. Onde o objetivo está
**O enigma do cetro está resolvido.** O espólio do Rei Negro (Cetro e Chave do Tesouro Negro) é **invisível**: com `detect invisibility` ligado, a sala E8 mostra no chão 9 Cetros do Rei Negro e 4 Chaves. Eu **tenho 2 cetros e 2 chaves** no inventário. O Bispo Branco aceitou a entrega de um cetro, mas com a missão cancelada (passei por E1, o que a derruba); reaceitei com `say sim` ×2 e a missão está em **"Você deve matar criaturas"** (peões: 6 de 9). Falta refazer a cascata (peões, bispos, cavalos, torres, Rainha, ~25 a 45 min) e, no passo "entregar objeto", dar o cetro.

## 2. Estado exato
- **Local:** Templo de Midgaard, dormindo. **Nível 34** · EXP 9.411.382 (faltam 588.618 para o 35) · HP 214/214 · mana 510 · MV 148 · alinhamento 510 (Bom) · CA 111 sem `armor` (mais ~37 com ela). Morreu 13 vezes e 1 DT.
- **Atributos:** FOR 11, CON 9, SAB 17, INT 19, DES 17, CAR 12; acerto 11, dano 5.
- **Ouro:** 38.490 (38.190 banco + 300 mão). Diretriz: nenhuma compra acima de 5% do ouro total (~1.920) sem pedir ao autor.
- **Inventário:** 2 Cetros do Rei Negro e 2 Chaves do Tesouro Negro (**invisíveis**: só aparecem no `inventory` com `detect invisibility`), cantil, 2 pães, tomo druídico, cajado retorcido (3 cargas de sleep), uma lança. Equipamento todo vestido (CA 111 sem buffs). Os buffs (`armor`, `invisibility`, `detect invisibility`) **expiraram**: relançar com `cuidar.py`.
- **Autoquests:** Xeque-mate ativa ("matar criaturas"). Ajuda Mágica: não ativa (sem tomo). Fonte: `state.json`; conferir com `score tudo`.

## 3. O que já foi descoberto
- **Itens do Rei (invisíveis):** `conhecimento.md` §88. `give cetro bispo` é aceito. A Chave do Tesouro Negro deteriora; abre o `baixo` de D8 (Tesouraria Negra), que está trancado ("Parece estar trancado") e ainda não foi aberto. A Rainha reaparece em ~20 min e atrapalha D8.
- **Missão cancelada por E1:** nunca entrar em E1 (Rei Branco) com a Xeque-mate ativa, nem invisível. O `PROIBIDAS` do módulo já proíbe E1 no caminho.
- **Cascata (`xadrez_cascata.py`):** `--etapa f1` (reaceitar à mão com `say sim` ×2 se o convite aparecer; `say sim` sozinho abriu a missão), `peoes` (várias varreduras até 9 mortes; reaparecem devagar), `bispos`, `cavalos`, `torres`, `rainha`, com `f1` entre elas e ~80 s de espera pela ordem. `cadeia4.ps1` (scratchpad) encadeia tudo e para na entrega; refazer se preciso (20 tentativas por etapa).
- **Kite do Rei** (`--etapa rei --rei`): funciona (1 raio e `recall` imediato; ~30 idas), agora com `detect invisibility` e `get` do chão; não é necessário neste plano porque já temos o cetro.
- **Doação e venda:** o ferreiro e o armeiro seguem sem caixa; `donate` funciona de qualquer lugar; `autogold` alterna o ouro automático (hoje ligado). `detect invisibility` custa ~16 de mana e dura 12 h (§88).

## 4. Os bloqueios, e o que já foi tentado
- **Peões:** reaparecem devagar; cada varredura rende 1 a 3 mortes. Tentado: encadear até 20 varreduras (a cadeia faz sozinha).
- **Driver:** cai a cada ~1 h; reiniciar só o `live_daemon` por PID mantém a missão (conferido 4 vezes).
- **Falhas do auditor da sessão** (`fome-em-sessao`, `sede-em-sessao`, registro 6): a personagem reconectou com fome e sede depois de um reinício do driver, antes de rodar o `cuidar`. Evitadas no código por `cuidar.py` (mudou nesta sessão: `situacao()` volta a devolver o `texto`, e o `navegar.py` exige pão, água e armor antes de sair) e por `Ctx.comer_beber` em `automato/acoes/xadrez_cascata.py`, que roda a cada ida.

## 5. O próximo passo, e só ele
Conectar (`mandabala.py`; `cota_claude.py --registrar` com `get_usage`; subir o `live_daemon` com `MUD_DAY=160 MUD_WIMPY=45`), `score tudo` (confirmar "Xeque-mate: Você deve matar criaturas"; se a missão tiver caído, reaceitar com o Bispo em F1 com `say sim` ×2), `prepara.py --forcar --sem-doacoes`, `cuidar.py` e `cast 'detect invisibility'` (para listar os cetros). Em seguida lançar a cascata (`cadeia4.ps1` ou `--etapa peoes`, `f1`, `bispos`, `cavalos`, `torres`, `rainha`, `f1`) e, **só quando o `score tudo` mostrar "Você deve entregar objeto ao personagem"**, dar `give cetro bispo` em F1 e conferir o `score tudo`, a EXP e o `autoquest todas`. Se o primeiro cetro for recusado, tentar o segundo; se ambos, ir a E8 (invisível, com `detect invisibility`, sem passar por E1) e pegar outros do chão.

## 6. NÃO REPITA
- Não entrar em E1 (nem invisível) com a missão ativa; vida abaixo de 100 só `recall`; não esperar entre raio e `recall` no Rei.
- Não dar `give` fora do passo (a entrega só conclui no passo "entregar objeto"); não fechar a conexão desnecessariamente.
- Não concluir que um corpo ou sala está vazio sem `detect invisibility`.
- Não comprar acima de 5% do ouro sem pedir; não passar pela fileira 1 do lado branco (a Rainha Branca engaja).
- Não pegar a Armadura da Torre Negra (maldita) em H8.

## 7. Ferramentas e comandos
Python: `C:\Users\peter\AppData\Local\Programs\Python\Python312\python.exe`. `play.py "<cmd>"` (`_CLOSE sleep`, `_RAW 1` no menu de morte). `navegar.py`, `prepara.py`, `cuidar.py`, `xadrez_cascata.py` (`--etapa peoes|bispos|cavalos|torres|rainha|f1|rei`), `ressuscitar.py`, `mandabala.py --sobre <termo>`, `cota_claude.py`. Scripts de apoio no scratchpad da sessão (`cadeia4.ps1`, `olha_pecas.py`, `mapeia_tabuleiro.py`, `limpa_tabuleiro.py`, `espera_rei.py`); o mapa do tabuleiro está em `automato/runtime/tabuleiro_dia159.json`.

## 8. Devolutiva técnica
| Descobri | Registrei em | O quê |
|---|---|---|
| mapa | `mapa.json` | nada novo nesta parte |
| referência do servidor | `maquina/verificacoes.md` | nada: tudo no conhecimento §83 a §88 |
| fato do mundo | `conhecimento.md` §88 | espólio do Rei invisível; `detect invisibility` ~16 de mana, 12 h; E1 cancela a missão |
| erro do motor | `automato/CHANGELOG.md` | v1.7.26: `detect invisibility` no kite e `get` do chão; `cuidar.situacao()` com `texto` |

## 9. Como encerrar a sua sessão
Siga `docs/agentes/PROTOCOLO.md` §3: `_CLOSE sleep` no Templo, evidência com `agent`, `python scripts/encerrar.py --agente "<modelo/versão>"`, preencher o plano 046, `python scripts/encerrar.py --agente "<modelo/versão>" --fechar --avanco sim|nao`.
