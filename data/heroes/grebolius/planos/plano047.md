# Plano 047 — Tesouro Negro em ciclo e a exceção do Rei Branco: abrir o Tesouro Branco (e depois a Ajuda Mágica)

| | |
|---|---|
| **Criado em** | 2026-10-22 · Dia 157 (sessão marcada Dias 161 a 163 nos registros) |
| **Por** | Claude Sonnet 5.5 (claude-sonnet-5-5) |
| **Herói** | grebolius |
| **Objetivo** | Matar o Rei Branco **uma vez** (exceção de moralidade do autor, `DECISOES.md` §17), pegar as chaves e abrir o **Tesouro Branco** (porta `!baixo` de D1); depois, a Ajuda Mágica (`observacoes/ajuda-magica-padroes-2026-10-22.md` §4) |
| **Sessão encerrada?** | sim — Templo de Midgaard, `save` e `sleep` confirmados (`_CLOSE sleep`), driver fechado, sem `quit` |

Substitui o plano 046 (meu antecessor, não é editado). Esta sessão teve várias ordens do autor: Tesouraria Negra, nível 35, identificar todos os itens, detect sempre ligado, a meta de pegar o tesouro mais 5 vezes (feitas 3 pela rotina, mais 2 manuais antes), e por fim a exceção do Rei Branco.

## 1. Onde o objetivo está
O **Tesouro Negro** virou rotina (`acoes/tesouro_negro.py`): 3 tomadas (+60.000) e período de reset medido (~13 min). **O Rei Branco ainda não foi enfrentado** (nenhum raio nele; o marcador `rei_branco_morto.json` não existe). Falta rodar o lado branco, que está pronto e testado. Depois, a Ajuda Mágica: a ordem de testes está escrita e nenhuma foi executada.

## 2. Estado exato
- **Local:** Templo de Midgaard (`templo_midgaard`), dormindo. **Nível 35** · EXP 10.114.484 (próximo nível em 11.000.000, faltam 885.516) · vida 232/232 · mana 510/510 · MV 149.
- **Alinhamento 394** (as mortes do Rei Negro o subiram de 312). **Mortes:** 16 + 1 DT. Wimpy 45.
- **CA:** 87 sem magias, 124 com `armor`, 164 com `armor` e `invisibility`. Buffs no fechamento: `armor` 25 h, `detect invisibility` 13 h.
- **Ouro:** 144.548 (144.248 banco + 300 mão). Diretriz: nenhuma compra acima de 5% do ouro total (~7.200) sem pedir ao autor.
- **Vestido (18 peças):** coroa da Rainha Branca, brinco de novato, colar com pedra púrpura, coleira do dragão, mochila de Pellinore, veste de escamas, braçadeiras, luvas, bracelete, rosário, anel de rubi, anel dourado, escudo de aço, cinturão de rodeio, calça, botas negras, lâmina de ferro, cajado (`sleep`, 3 cargas; o login o solta da mão: `hold cajado`).
- **Inventário:** cantil, 2 pães, tomo druídico. **Na mochila (guardado pela rotina):** túnica dourada, Cruz Ansada (voltou a servir com o alinhamento 394), manto, Lança do Cavaleiro Negro (amaldiçoada), Cetro do Bispo Negro, Armadura do Peão Negro, Cetro do Rei Negro, bainha de Excalibur, Armadura da Torre Branca, colar e rosário reservas. **Sem chave** do Tesouro no inventário.
- **Autoquests:** Xeque-mate Concluída; Ajuda Mágica não ativa. Fonte: `state.json`; conferir com `score tudo`.

## 3. O que já foi descoberto
- **`conhecimento.md` §91, §92 e §93**; evidências `dia161-tesouraria-negra-nivel35.json`, `dia161-itens-identificados.json` e `dia163-tesouro-negro-rotina.json`; catálogo `itens.json`; ficha `observacoes/ficha_rpg_dia161.html` (nível 35).
- **Tesouro Negro:** reset ~13 min; porta `!baixo` = reiniciou. **Cada `unlock` gasta uma chave**; o Rei Negro deixa 3 a 4; `get all.chave` pega todas. As chaves somem entre sessões.
- **Exceção do Rei Branco (`DECISOES.md` §17, diretiva §27):** uma morte, "todo rei é um tirano"; vale também a defesa contra peças NPC brancas; **jogadores (Keen etc.) ficam fora**. O Rei Branco nunca foi medido; abater peça branca derruba o alinhamento (Cavaleiro Branco: 455 para 402).
- **Rei Negro acordado ataca até invisível** (morte #16: -90, -91, -59 em duas rodadas). A rotina agora o dorme antes de pegar a chave do chão de E8.
- **Jogadores:** só "Darkay diz: oi grebolius"; o canal `tagarela` é público; o Keen (nível 55) rouba golpes finais no tabuleiro.
- **Pão e água** vão pelo `prepara`/`cuidar` (`aproveitar_tempo`), e o espólio vai para a mochila com `base.guardar_na_mochila` (diretiva §29).

## 4. Os bloqueios, e o que já foi tentado
- **Auditor da sessão (`auditar_sessao.py`): FALHAs desta parte, cada uma tratada com código:**
  - morte #16 e a conferência do chão de E8 com o Rei acordado: **tratada com código: `automato/acoes/tesouro_negro.py` dorme o Rei antes de pegar a chave** e sai se ele não dormir (`scripts/test_tesouro_negro.py`).
  - fome e peso no kite longo: **tratadas com código: `automato/acoes/xadrez_cascata.py` repõe pão e água pelo `aproveitar_tempo`** e **`tesouro_negro.py` guarda o espólio na mochila**.
  - confusão do menu de morte com queda de conexão: **tratada com documentação em `conhecimento.md` §92/§93**; o reinício do daemon só vale com `_STATUS` e o log conferidos.
- **Rei Branco:** sem medição de vida, dano ou barra; a primeira ida do kite é a medição. A trava `automato/runtime/rei_branco_morto.json` impede um segundo kill.
- **Tesouro Branco:** a sala atrás de D1 é só hipótese (espelho do negro); o nome da chave e da sala não estão confirmados. A rotina aceita qualquer "chave do tesouro" e "tesouro".
- **Driver:** cai a cada ~1 h; reiniciar só o `live_daemon` pelo PID.
- **Pendente (código):** `prepara.ir_fonte` anda `s` (é `down`).

## 5. O próximo passo, e só ele
Conectar (`mandabala.py`; `get_usage` e `cota_claude.py --registrar`; subir o `live_daemon` com `MUD_DAY=164 MUD_WIMPY=45`), `score tudo` (anotar o **alinhamento antes: 394**), `python automato/acoes/identificar_itens.py` (diretiva §29), `prepara.py --forcar --sem-doacoes`, `cuidar.py`. **Depois:** `python automato/acoes/tesouro_negro.py --lado branco --excecao-rei-branco --tomadas 2`, com monitor a cada tomada e a cada 5 minutos (o autor pediu avisos assim). Na 1ª ida ao Rei Branco registrar o `consider`, a barra de vida e o dano dele; se a rodada dele passar de ~200, parar e mostrar os números ao autor. Depois da morte, conferir o alinhamento e anotar. **Se o Tesouro Branco não existir ou não abrir, voltar à Ajuda Mágica** (`observacoes/ajuda-magica-padroes-2026-10-22.md` §4).

## 6. NÃO REPITA
- Não matar o Rei Branco uma segunda vez; não atacar jogadores (Keen etc.), animais nem NPCs pacíficos (exceção só para o Rei Branco e a defesa contra peças brancas).
- Não entrar em E8 nem em E1 sem dormir o Rei antes; vida abaixo de 100 só `recall`; `kite` só com a personagem inteira.
- Não matar `turno.py`/`navegar.py` à força sem restaurar o `brief` (`base.brief(False)`); não reiniciar o daemon sem ler `_STATUS` e o log (o "menu" pode ser o de morte).
- Não recolher "tudo do corpo": só chaves; o resto vai para a mochila (§29). Não vestir nem empunhar a Lança do Cavaleiro Negro.
- Não abrir a cadeia do Lemin antes de ter o item; nenhuma compra acima de 5% do ouro sem pedir; não derrubar todos os Python.

## 7. Ferramentas e comandos
Python 3.10 (`python`). `play.py "<cmd>"` (`_CLOSE sleep`; `MUD_CTRL_TOKEN` do `.controller` local). `tesouro_negro.py --lado negro|branco [--excecao-rei-branco] --tomadas N` (rotina do tesouro), `xadrez_cascata.py --etapa rei --rei [--lado branco --excecao-rei-branco]`, `identificar_itens.py`, `cuidar.py` (armor e detect), `prepara.py`, `navegar.py --de <id> --para <id>`, `ressuscitar.py` (reequipa e come), `aproveitar_tempo.py`, `mandabala.py --sobre <termo>`, `cota_claude.py`, `quality_run.py --loop`.

## 8. Devolutiva técnica
| Descobri | Registrei em | O quê |
|---|---|---|
| mapa | `mapa.json` | nada novo nesta parte (a sala `xadrez_tesouro_negro` é da parte anterior) |
| referência do servidor | `maquina/verificacoes.md` | nada: tudo no conhecimento §93 |
| fato do mundo | `conhecimento.md` §93 | reset de ~13 min, `unlock` gasta chave, `get all.chave`, Rei Negro sobe a moral, jogadores, exceção do Rei Branco |
| erro do motor | `automato/CHANGELOG.md` | v1.7.31 a v1.7.36: rotina do tesouro, `get all.chave`, padrão para pão, água e mochila, lado branco, sleep antes do chão de E8 |

## 9. Como encerrar a sua sessão
Siga `docs/agentes/PROTOCOLO.md` §3: `_CLOSE sleep` no Templo, evidência com `agent`, `python scripts/encerrar.py --agente "<modelo/versão>"`, preencher o plano 048, `python scripts/encerrar.py --agente "<modelo/versão>" --fechar --avanco sim|nao`.
