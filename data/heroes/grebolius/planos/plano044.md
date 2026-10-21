# Plano 044 — Xeque-mate: o Rei já cai por kite; falta achar o Cetro do Rei Negro (locate object)

| | |
|---|---|
| **Criado em** | 2026-10-21 · Dia 158 (sessão marcada Dia 159 nos registros) |
| **Por** | Claude Sonnet 5.5 (claude-sonnet-5-5) |
| **Herói** | grebolius |
| **Objetivo** | **Terminar a Xeque-mate**: entregar o cetro do Rei Negro ao Bispo Branco |
| **Sessão encerrada?** | sim — Templo de Midgaard, `save` e `sleep` confirmados, `live_daemon` parado, sem `quit`; a autoquest caiu no fechamento |

Substitui o plano 043 (meu antecessor, não é editado).

## 1. Onde o objetivo está
A parte difícil está resolvida: **o Rei Negro foi morto por mim** (kite de 1 raio com recall imediato, ~30 idas, vida da personagem intacta), com +36.846 EXP e nível 34. Mas **o Rei nasce sem cetro**: `look rei` mostra "o Rei usa: NADA" em dois reis seguidos e o corpo só tinha ouro; o servidor recusa cetros de outros mobs ("não é o item correto ou você não é o dono original"). A hipótese forte é que o Cetro do Rei Negro seja item único e já exista em outro lugar (jogador, loja, chão), o que impede a carga. A missão caiu no fechamento: reaceitar e refazer a cascata custa ~25 min.

## 2. Estado exato
- **Local:** Templo de Midgaard, dormindo. **Nível 34** · EXP 9.015.232 (faltam 984.768 para o 35) · HP 214/214 · mana 510 · MV 148 · alinhamento 512 (Bom). Morreu 13 vezes e 1 DT.
- **Ouro:** 27.186 (21.486 banco + 5.700 mão). **Piso de emergência: 10.000.** Diretiva: **nenhuma compra acima de 5% do ouro total (~1.360) sem pedir ao autor** (`diretiva_de_jogo.md` §25).
- **Vestido:** coroa da Rainha Branca, brinco de novato, Cruz Ansada, colar anti-DT, túnica dourada, braçadeiras, luvas, bracelete, rosário, anéis, escudo de aço, cinturão de rodeio, calça, botas negras, lâmina de ferro, cajado retorcido na mão (3 cargas de sleep), mochila de Pellinore. CA 147 com `armor`.
- **Mochila:** lanças e coroas da Rainha Negra (revenda quando ferreiro/armeiro tiverem caixa), Armadura da Torre Branca, veste de escamas (opção de +20 vida), bainha de Excalibur (nível 85), rosário e manto de reserva. Na mão: tomo druídico (não doa/vende).
- **Fonte:** `state.json` (live). Conferir com `score tudo`.

## 3. O que já foi descoberto
- **Kite do Rei (funciona):** `python automato/acoes/xadrez_cascata.py --etapa rei --rei --idas 60`: por ida, entra em E8 invisível, `consider`, `sleep`, **1 `lightning bolt` e `recall` imediato** (sem esperar). Lê a barra do Rei (`{------>>>>}`: `-` perdido). Barra vazia + "mortalmente ferido" = ele não luta mais, **ficar e rematar** (senão morre sem crédito). Detalhes e armadilhas no `conhecimento.md` §83.
- **Cascata (a missão cai ao fechar):** `--etapa f1`, reaceitar com o Bispo Branco (`say sim` ao convite e ao "Entendido?", à mão), `--etapa peoes` (2 a 4 varreduras até 9 mortes), `--etapa bispos`, `cavalos`, `torres`, `rainha`, com `--etapa f1` entre elas (a ordem demora ~75 s). Um script encadeia isso (`cadeia.ps1` no scratchpad da sessão; refazer se preciso).
- **O Rei sem cetro:** §84. Tesourarias do tabuleiro (3665/3666) têm ouro e chaves, não cetro (docs/circlemud §96).
- **locate object:** aprendida no nível 34; só conjura de um **espelho localizador**, vendido por Albernathy em **Silverthorne** (preço desconhecido) ou achado no mundo. Silverthorne tem a Loja do Escriba e teletransporte para Midgaard/Jareth/Sundhaven; **nenhum `help mapa` dá a rota de Midgaard** (copiados em `automato/runtime/help_mapas_dia158.txt`).
- **Infra:** `score tudo` mostra `[ Duração ]` das magias; `prepara.py --forcar --sem-doacoes` reabastece; depois de morte o equipamento volta ao inventário (`wear all`, `wield ferro`, `hold cajado`); `donate` funciona de qualquer lugar; Ajuda Mágica segue sem tomo (plano 041).

## 4. Os bloqueios, e o que já foi tentado
- **Cetro do Rei:** não vem do corpo. Tentado: `get cetro corpo`, `look in corpo`, `look rei` em dois reis. Não tentado: `locate object cetro` (falta o espelho), perguntar ao autor se outro jogador tem o item.
- **Rota a Silverthorne:** ausente. Não tentado: Portão Leste de Jareth (floresta), ponta oeste da Estrada Midgaard-Jareth.
- **Falhas do auditor desta sessão** (corrigidas em `automato/acoes/xadrez_cascata.py`, que mudou nesta sessão): `repeticao-de-recusa` (28x `sleep` no Rei ausente: agora `kite_rei` detecta "Em que você deseja" e espera o repop), `ataque-sem-consider` (agora `consider` antes do 1º sleep), `armadura-ausente` (agora `Ctx.armor()` via `prepara.garantir_armor`), `fome/sede-em-sessao` (sleep do descanso deixava dormindo; `wake`+`stand` e `comer_beber`), `alinhamento-caiu` (479 → 450 por abates de peças do tabuleiro, esperado).

## 5. O próximo passo, e só ele
Conectar (`mandabala.py`; `cota_claude.py --registrar` com `get_usage`; subir o `live_daemon` com `MUD_DAY=159 MUD_WIMPY=45`), `prepara.py --forcar --sem-doacoes`, `cuidar.py`. **Não refazer a cascata ainda.** Ir pelo **Portão Leste de Jareth** (`navegar.py --para jareth_portao_leste`) e explorar a floresta com um explorador em Python (origem `MUD_ORIGEM=mapear`, parar em combate ou com vida abaixo de 150, `consider` antes de lutar) procurando a estrada para Silverthorne (Estrada de Paralelepípedos, Grande Muro, Praça Oeste). Ao chegar, ler o `list` de Albernathy **sem comprar**, anotar o preço do espelho e pedir ao autor a compra com o número, citando a diretiva §25 (compra acima de 5%). Com o espelho: `cast 'locate object' cetro` e agir conforme o dono (mob: matar com `consider`; loja: comprar com pedido; jogador: parar e perguntar). Só depois refazer a cascata e o kite.

## 6. NÃO REPITA
- Não esperar entre o raio e o `recall` no Rei; não tentar `sleep` repetido com o Rei acordado; nunca ir embora quando ele estiver "mortalmente ferido" sem rematar.
- Não comprar acima de 5% do ouro sem pedir; não vestir item sem `identify`; vida < 100 só `recall`.
- Não deixar a personagem dormindo ao interromper um laço (`wake;stand`); não descer em `nd2_armadilha` (Notre Dame) nem em E1/E8 fora do kite.
- Não fechar a conexão com a missão ativa sem querer perdê-la; não derrubar todos os Python.
- Não refazer a cascata antes de saber onde está o cetro (25 min).

## 7. Ferramentas e comandos
Python: `C:\Users\peter\AppData\Local\Programs\Python\Python312\python.exe`. `play.py "<cmd>"` (`_RAW 1` no menu de morte; `_CLOSE sleep`). `navegar.py --de <id> --para <id>`; `prepara.py`; `cuidar.py`; `xadrez_cascata.py` (`--etapa peoes|bispos|cavalos|torres|rainha|f1|rei`); `ressuscitar.py` (depois de `_RAW 1`); `mandabala.py --sobre <termo>`; `cota_claude.py`.

## 8. Devolutiva técnica
| Descobri | Registrei em | O quê |
|---|---|---|
| mapa | `mapa.json` | nada novo nesta parte |
| referência do servidor | `maquina/verificacoes.md` | nada: tudo no conhecimento §83 e §84 |
| fato do mundo | `conhecimento.md` §83, §84 | kite que mata o Rei; o Rei sem cetro; locate object |
| erro do motor | `automato/CHANGELOG.md` | v1.7.25: recall imediato, sleep, armor, consider, repop |

## 9. Como encerrar a sua sessão
Siga `docs/agentes/PROTOCOLO.md` §3: `_CLOSE sleep` no Templo, evidência com `agent`, `python scripts/encerrar.py --agente "<modelo/versão>"`, preencher o plano 045, `python scripts/encerrar.py --agente "<modelo/versão>" --fechar --avanco sim|nao`.
