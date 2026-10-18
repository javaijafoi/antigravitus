# Plano 017 — Ativação Oficial de Gargamel, Proteção da Sala do Alquimista e Caminho ao Nível 50

| | |
|---|---|
| **Criado em** | 2026-10-17 · Dia 156 |
| **Por** | Gemini 3.8 Flash (High) |
| **Herói** | grebolius |
| **Objetivo** | Concluir integralmente `Uma Lição em Gargamel` (obter o jarro brilhante, entregar ao minerador, desvendar Papai Smurf no Covil de Gargamel) e escalar ao Nível 50 |
| **Sessão encerrada?** | sim — personagem em segurança no Templo de Midgaard; HP 188/188, Mana 360/360, MV 143/143, wimpy 45, save confirmado; live_daemon ativo |

---

## 1. Onde o objetivo está

A autoquest **`Uma Lição em Gargamel`** está **OFICIALMENTE ATIVA** sob `[Autoquests em andamento]` no `score tudo` (ativada via diálogo canônico com o Smurf Minerador em *O Fim Do Túnel*). O Nível 30 de Grebolius está consolidado (**5.759.762 EXP** acumulados).

A causa raiz da falha anterior na entrega foi diagnosticada e remediada:
1. Ao abrir a porta de *A Sala do Alquimista*, um mob hostil (*o novato zumbi*) engajou combate instantâneo, bloqueando a interação pacífica.
2. O Alquimista exige o diálogo de identificação prévia (**`say Grebolius`** seguido de **`say sim`** à pergunta *"Deixe-me adivinhar: você quer um jarro brilhante, certo?"*). Emitir `give aquosa alquimista` durante o combate sem esse diálogo fez o NPC absorver a poção sem entregar o jarro.
3. O script `entregar_alquimista.py` foi corrigido para abater qualquer ameaça na sala antes de falar e executar o protocolo canônico de diálogo antes da entrega.

Falta apenas acumular as moedas para recomprar a poção aquosa (9.750 moedas na loja de Clariss em Jareth), entregá-la ao Alquimista pelo jarro brilhante, levar o jarro ao Minerador e resgatar Papai Smurf no Covil de Gargamel.

---

## 2. Estado exato

- **Nível:** 30 (Mago Elfo, 1ª encarnação).
- **EXP:** 5.759.762 (restam apenas 240.238 EXP para Nível 31).
- **Vitals:** HP 188/188, Mana 360/360, MV 143/143.
- **Wimpy:** 45 (estritamente mantido).
- **Armadura:** CA 138 (magia `armor` ativa com 44 horas de jogo restantes).
- **Ouro:** 301 moedas na mão (0 no banco).
- **Local:** Templo de Midgaard (ponto seguro de retorno).
- **Autoquests em andamento:** `Uma Lição em Gargamel` (ativa e confirmada no `score tudo`).
- **Equipamentos:** Coroa da Rainha Branca, Armadura da Torre Negra, Espada Curta, Escudo, Manto de Pano, Cinturão de Rodeio, Rosário, Luvas e Calça de Couro, Mochila de Pellinore.
- **Suprimentos:** Mochila de Pellinore com pão recheado e espadas de reserva; cantil com água cristalina; pergaminho de sabedoria no inventário.

---

## 3. O que já foi descoberto

1. **Ativação Canônica do Smurf Minerador (`conhecimento.md` §47):**
   - Templo -> `s,s` (Praça do Comércio) -> `8x e` (Rua Principal/Portão Leste/Estrada do Rei) -> `n` (Entrada Para a Vila dos Smurfs) -> `3x n` (O Poço Smurf) -> `d` (Dentro do Poço) -> `e` (O Fim Do Túnel).
   - Sequência exata: aguardar *"Olá, alguém poderia me ajudar?"* -> `say sim` -> `say Grebolius` -> `say sim`. O servidor confirma *"Você começa a participar da aventura."*.
2. **Protocolo Estrito do Alquimista (`conhecimento.md` §48):**
   - Na Sala do Alquimista, abater qualquer `novato zumbi` antes de falar.
   - Dizer `say Grebolius`, aguardar a pergunta sobre o jarro, responder `say sim`, e só depois emitir `give aquosa alquimista`.
3. **Compra da Poção em Jareth:**
   - Preço exato: 9.750 moedas em *As Misturas de Clariss*.
   - Comando obrigatório: `buy aquosa` (nunca `buy pocao`).
   - Rota: Templo -> Floresta -> Portão Leste de Jareth -> ~10 passos a oeste pela Avenida Floris -> loja ao sul.
4. **Motor de Grind Híbrido (`cacador_hibrido.py`):**
   - Alterna Milharal V2 (50 moedas diretas no corpo do mob) com Masmorra dos Novatos (abates rápidos e espólios leves), com recarga automática de sono e hidratação no Templo.

---

## 4. Os bloqueios, e o que já foi tentado

- **Bloqueio:** Saldo atual em 301 moedas após a compra da primeira poção; são necessárias 9.750 moedas para nova poção aquosa.
- **Solução implementada:** `cacador_hibrido.py` já testado e validado ao vivo (rendeu 1.210 moedas em poucos minutos na sessão anterior). O próximo operador pode rodar ciclos controlados até atingir 9.800 moedas.
- **Atenção Invariante 8:** **NUNCA dar `quit`** enquanto `Uma Lição em Gargamel` estiver ativa, pois o comando zera as autoquests em andamento. Encerrar sempre com `save` e sono no Templo.

---

## 5. O próximo passo, e só ele

Executar o acúmulo de saldo e a entrega canônica:
1. Rodar `python automato/acoes/cacador_hibrido.py --ciclos 4 --meta-ouro 9800` até atingir ≥ 9.750 moedas.
2. Executar `python automato/acoes/comprar_pocao.py` para comprar `uma poção aquosa` em Clariss (Jareth).
3. Conduzir até a Sala do Alquimista e eliminar qualquer `novato zumbi` hostil.
4. **Interação manual pelo agente ao vivo (Invariante 14 / Diretiva 20 — PROIBIDO AUTOMATIZAR):**
   - Conferir `score tudo` (confirmar que a autoquest pede a entrega);
   - Emitir `say Grebolius` no terminal interativo e ler a resposta do NPC;
   - Responder `say sim` e ler a reação do NPC;
   - Emitir `give aquosa alquimista` e verificar o recebimento de `o jarro brilhante` no `inventory`.
5. Ir ao Smurf Minerador em *O Fim Do Túnel* e fazer a entrega manualmente (`give jarro minerador`).
6. Seguir para o norte do Poço Smurf, desvendar Papai Smurf no Covil de Gargamel e avançar rumo ao Nível 50.

---

## 6. NÃO REPITA

1. **NÃO automatizar diálogos de missão por script (Invariante 14 / Diretiva 20):** Falar com NPCs de missão é exclusivo do agente ao vivo no terminal ("para evitar dar merda").
2. **NÃO dar `quit`:** `Uma Lição em Gargamel` está ativa no `score tudo`; `quit` apagaria a missão.
3. **NÃO emitir `give` sem diálogo prévio e sem checar `score tudo`:** O Alquimista engole itens se não ouvir `say Grebolius` -> `say sim` antes.
4. **NÃO ignorar mobs na Sala do Alquimista:** Mate o novato zumbi antes de tentar interagir com o NPC.
5. **NÃO comprar 'pocao' em Clariss:** Sempre usar `buy aquosa`.
6. **NÃO vender armaduras amaldiçoadas:** Descartar qualquer item com flag `amaldiçoado` ou da Torre Negra.

---

## 7. Ferramentas e comandos

- **Caçador Híbrido:** `python automato/acoes/cacador_hibrido.py --ciclos 4 --meta-ouro 9800`
- **Comprar Poção:** `python automato/acoes/comprar_pocao.py`
- **Terminal Interativo para Diálogo:** `python automato/nucleo/driver/play.py` (ou comandos diretos via live_daemon)
- **Verificar Devolutiva:** `python scripts/devolutiva.py`

---

## 8. Devolutiva técnica

| Descobri | Registrei em | O quê |
|---|---|---|
| mapa | `mapa.json` | PENDENTE: 4 arestas de anéis de mão dupla dos esgotos documentadas em prosa no Dia 156 aguardam fundição |
| referência do servidor | `maquina/verificacoes.md` | PENDENTE: Nenhuma mensagem nova de servidor; comportamento de bolsas locais fixado |
| fato do mundo | `conhecimento.md` | §47 (Ativação de Gargamel no Minerador), §48 (Protocolo Estrito na Sala do Alquimista), §49 (Diretiva: Diálogos de Missão Sempre Manuais) e §50 (Guarda de Cota Inteligente e Handoff Automatizado) |
| erro do motor | `CHANGELOG.md` | v1.6.5 (caçador híbrido), v1.6.6 (Invariante 14: proibição de diálogos automatizados) e v1.6.7 (Guarda de cota adaptativa e handoff automatizado) |

---

## 9. Como encerrar a sua sessão

1. Conduzir Grebolius ao Templo de Midgaard e garantir vitais cheios (HP/Mana).
2. Alimentar, hidratar, salvar (`save`) e deitar (`sleep`).
3. Registrar evidência em `data/heroes/grebolius/evidence/` com autoria declarada.
4. Atualizar `state.json` e sincronizar derivados via `python scripts/sync_hero.py --hero grebolius`.
5. Criar o próximo plano numerado append-only (`planos/plano018.md`) **somente ao encerrar a sessão para handoff**.
6. Rodar `python scripts/devolutiva.py` e conferir 0 falhas.
