# Plano 043 — Xeque-mate: matar o Rei Negro (o cetro é o fim da missão)

| | |
|---|---|
| **Criado em** | 2026-10-21 · Dia 158 (sessão marcada Dia 159 nos registros) |
| **Por** | DeepSeek deepseek-flash (dsh) |
| **Herói** | grebolius |
| **Objetivo** | **Terminar a Xeque-mate**: matar o Rei Negro em E8 e entregar o cetro ao Bispo Branco |
| **Sessão encerrada?** | sim — Templo, `save` e `sleep` confirmados, driver fechado, sem `quit` |

Substitui o plano 042 (não editado). **Orientação do autor (2026-10-21):** *"não importa se morrermos; o que importa é ficar mais forte no processo e tentar novas ideias contra o Rei"*.

## 1. Onde o objetivo está
A cascata já foi feita até a Rainha em sessões anteriores, mas **a missão caiu** (reconexões e mortes) e o Rei Negro nunca morreu: 1.500–2.200 de vida, 80–173 de dano por rodada, Santuário, e o kite de 1–2 raios por ida não fecha a conta (seriam 25–35 raios). O que muda agora: **cajado com 3 cargas de `sleep`**, `charm person` treinado (pega nível ≤ 33), e a certeza de que **em combate não se anda** e o `recall` custa ~552 EXP.

## 2. Estado exato
- **Local:** Templo de Midgaard, dormindo. **Vida/mana/MV:** 211/211 · 500/500 · 146/146.
- **Nível 33** · EXP **8.575.839** (faltam ~424k para o 34) · alinhamento 462 (Bom) · wimpy 45.
- **Ouro: 13.922** (12.565 banco + 1.357 mão). **Piso de emergência: 10.000 — não descer disso.**
- **Na mão:** cajado retorcido (BASTÃO MÁGICO, **3 cargas de `sleep`**, NOBITS) — não é de cura, é controle.
- **Equipado:** mochila de Pellinore (sobre o corpo), Coroa da Rainha Branca, túnica dourada, colar anti-DT, Cruz Ansada, cinto de rodeio, escudo de aço, anel de rubi; CA 147 (com `armor`).
- **Na mochila:** lanças e armaduras de peão do tabuleiro (vendáveis — `vender_espolio`).
- **Fonte:** `state.json` (as_of Dia 158, live). Conferir com `score tudo` ao conectar.

## 3. O que já foi descoberto (não redescobrir)
- **Tabuleiro (colunas A–H de oeste a leste, fileiras 1–8 de sul a norte):** entrada em H5; F1 Bispo Branco; E1 Rei Branco (mata quem entra); fileira 8: A8 torre, B8 cavalo, C8 bispo, **D8 Rainha** (saída oculta `baixo`), **E8 Rei**, F8 bispo, G8 cavalo, H8 torre.
- **Rei Negro:** ~1.500–2.200 de vida com regeneração entre idas; **Santuário** corta o dano pela metade; 2–3 golpes de 54–72 por rodada; `sleep`, `blindness` e `curse` pegam nele; o primeiro raio o acorda; **morrer cancela a missão** (§59) e custa EXP.
- **Movimento em combate é bloqueado** ("muito ocupado"): sair é `recall` (~552 EXP, 0,7 s) ou `flee` (aleatório, mesmo custo — pode cair em E8).
- **Regeneração:** barra de 211 cheia em ~20 s (medido); dormir é desperdício.
- **Cajado:** 3 cargas de `sleep` — `use cajado` em combate **nunca foi testado**; se funcionar, dorme o alvo sem "tempo de se concentrar".
- **Charm person:** funciona em nível ≤ 33 (Cavaleiro e Bispo Negro seguem); a Rainha e o Rei têm Santuário e não encantam.
- **Ferramentas novas:** `aproveitar_tempo.py` (espera útil), `vender_espolio.py` (venda com `value`), `preparar.dormir` com teto de 90 s.

## 4. Os bloqueios e o que já foi tentado
- **Kite de 1–2 raios por ida:** sempre caiu a missão (mortes #10, #12, #13). Não repetir sem tática nova.
- **Andar para sair de E8:** custa uma rodada inteira e pode matar (§76). Só `recall`.
- **Reconexão/morte derruba a autoquest:** conferir `score tudo` logo no login; se estiver inativa, reaceitar com o Bispo em F1.
- **3 FALHAs do auditor na sessão de 2026-10-21** (não repetir): fome/sede registradas no início (o `prepara` rodou depois de sair) e `cast 'sleep' rainha` **sem `consider`** — entrar com `prepara --forcar` **antes** de sair e `consider` antes de qualquer magia no alvo.
- **Caixa dos comerciantes:** finito; a venda para quando seca (`vender_espolio` registra).

## 5. O próximo passo, e só ele
Conectar, `prepara.py --forcar` **antes de sair**, `score tudo` (conferir se a Xeque-mate está ativa; se não, reaceitar com o Bispo em F1), `navegar.py --para xadrez_D7` e **`consider rainha`** — se a Rainha estiver viva, matá-la com `sleep` (cajado ou magia) + 3–4 raios, **recall com vida ≥ 190** (margem nova), e só então ir ao Rei.

**No Rei (E8), nesta ordem de ideias:**
1. **Charm de apoio:** `cast 'charm person' bispo` (C8/F8) ou `cavalo` (B8/G8) e `ordenar` o mob a atacar o rei, se o comando existir; medir o dano que o aliado faz por rodada.
2. **Mercenário:** testar se dá para contratar (taverna de Midgaard: `list`/`say`; registrar se não existe).
3. **Cajado:** `use cajado` no Rei para testar `sleep` sem concentração; se dormir, 2 raios seguidos e `recall`.
4. **Kite com margem 190:** 1 raio por ida, `recall` a 190 (não a 150), regenerar 20 s, voltar (17 s) — ciclo medido de ~40 s.
5. **Só se 1–4 falharem:** tentar `flee` a partir de E8 (risco de cair em E8/D8/C8) — decisão do autor na hora.

## 6. NÃO REPITA
- Não entrar em E8 com vida < 190; não andar em combate; não usar `sleep` (magia) em combate — o cajado é a exceção a testar.
- Não atacar sem `consider` (FALHA do auditor); não sair sem `prepara` (fome/sede = FALHA e a vida não sobe).
- Não repetir o kite de 25–35 raios: se uma ida inteira não tirar um segmento da barra do Rei, parar e replanejar.
- Não dar `give` fora da etapa; não `quit`; não deixar a personagem parada em E1/B1/G1.
- **Dinheiro:** não gastar abaixo de **10.000** de reserva; só gastar o que a sessão render (pão e água sempre liberados).

## 7. Ferramentas e comandos
`mandabala.py --sobre "Rei Negro"` antes da luta; `navegar.py --para xadrez_E7`; `xadrez_cascata.py --etapa rei --rei --idas N` (kite pronto, mas com `LIMITE_VIDA = 150` — subir a margem antes de usar); `aproveitar_tempo.py --minutos 2` durante espera de repop; `vender_espolio.py` para o caixa; `prepara.py --forcar` **antes** de sair; `cuidar.py` para `armor`/`invisibility`.

## 8. Devolutiva técnica
| Descobri | Registrei em | O quê |
|---|---|---|
| mapa | `mapa.json` | nada novo nesta sessão (D8/D7 já estavam) |
| referência do servidor | `maquina/verificacoes.md` | andar em combate bloqueado; `recall` custa 552 EXP; `sleep` não pega em combate |
| fato do mundo | `conhecimento.md` §89 | regeneração ~20 s e o cajado de `sleep` |
| erro do motor | `automato/CHANGELOG.md` | v1.7.23 e v1.7.24 (sono/descanso por vitais; `aproveitar_tempo` e `vender_espolio`) |

## 9. Como encerrar a sua sessão
`recall` → Templo, comer/beber, `_CLOSE sleep`; `python scripts/encerrar.py --agente "<modelo/versão>"`, preencher o plano 044, `--fechar --avanco sim|nao --tipo chefe`.

## 10. Orçamento de ouro (orientação do autor, não regra)
- **Pão e água:** livres, sempre.
- **Resto:** só com o ouro **ganho na própria sessão** (vendas, espólios, doação de sangue).
- **Piso:** nunca menos de **10.000** no total (banco + mão).
- Hoje: 13.922 disponíveis; margem livre acima do piso = **3.922**.
