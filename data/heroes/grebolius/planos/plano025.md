# Plano 025 — Capítulo 11 (Tomo II): Autoquests Xeque-Mate e Ajuda Mágica (+ Bateria Completa de Mecânicas Inéditas)

| | |
|---|---|
| **Criado em** | 2026-10-18 · Dia 156 |
| **Por** | Gemini 3.8 Flash (High) |
| **Herói** | grebolius |
| **Objetivo** | Capítulo 11 (Tomo II — As Chaves do Tabuleiro) — Iniciar e executar a autoquest Xeque-mate no Grande Tabuleiro de Xadrez; se concluída em menos de 3 horas de tempo real, executar também a autoquest Ajuda Mágica. Concomitantemente, testar em campo a lista completa de mecânicas e comandos inéditos de CircleMUD/DeBo, cabendo exclusivamente a quem estiver jogando avaliar a viabilidade em tempo real e descartar o que não fizer sentido ou for impraticável |
| **Sessão encerrada?** | sim — personagem em total segurança no Templo de Midgaard; HP 196/196, Mana 420/420, MV 144/144, CA 143 (sem armor), wimpy 45, Alinhamento 311 (Bom), Nível 31 consolidado, save e sono confirmados; live_daemon finalizado |

---

## 1. Onde o objetivo está

O **Capítulo 11 do Tomo II ("As Chaves do Tabuleiro")** possui duas missões centrais com uma diretiva de enriquecimento operacional:
1. **Missões do Tomo II (Eixo Primário):**
   - Iniciar e executar a autoquest `Xeque-mate` no Grande Tabuleiro de Xadrez (nível 30+).
   - Se concluída com facilidade (**menos de 3 horas de tempo real no relógio**), emendar imediatamente com a autoquest `Ajuda Mágica` em Midgaard.
2. **Bateria Completa de Mecânicas Inéditas (Sem Pré-Filtro do Planejador):**
   - O autor Peter determinou: **não fazer pré-filtro de esforço no plano**. Toda a lista de mecânicas, comandos e eventos descobertos no CircleMUD/DeBo é entregue integralmente a quem estiver jogando.
   - O jogador/agente em tempo real deve buscar testar tudo aquilo que foi descoberto. Se durante a sessão perceber que determinado teste não faz sentido, é inviável, perigoso demais ou exige esforço desproporcional, **o próprio jogador exclui o item na hora**, registra o motivo da recusa e segue adiante.

---

## 2. Estado exato

- **Nível:** 31 (Mago Elfo, 1ª encarnação).
- **EXP:** 6.933.216 (próximo nível: 7.000.000 — faltam apenas **66.784 EXP** para o Nível 32).
- **Vitals:** HP 196/196, Mana 420/420, MV 144/144.
- **Wimpy:** 45 (estritamente calibrado).
- **Alinhamento:** 311 (Bom — `{<<<<<>>---} Você é bom`).
- **Armadura:** CA 143 (sem armor arcana) / CA 148 (com armor arcana).
- **Ouro:** 1.719 moedas na mão (0 no banco).
- **Local:** O Templo de Midgaard (dormindo com save confirmado).
- **Suprimentos:** Cantil saciado de água cristalina, comida pronta.
- **Equipamentos vestidos:**
  - na cabeça: `a Coroa da Rainha Branca`
  - na orelha direita: `um diminuto brinco de novato`
  - no pescoço (1): `a coleira do dragão de estimação`
  - no pescoço (2): `um colar com uma pedra púrpura` (Anti-DT, Abençoado, CA +10, Acerto +1, Dano +1, Des +1, Mana +25)
  - sobre o corpo: `um manto de pano`
  - no corpo: `a Armadura da Torre Negra`
  - nos braços: `um par de braçadeiras de novato`
  - nas mãos: `um par de luvas de couro`
  - no pulso esquerdo: `um bracelete de prata e ouro`
  - no pulso direito: `um rosário`
  - como escudo: `um escudo`
  - na cintura: `um belo cinturão de rodeio`
  - nas pernas: `uma calça de couro`
  - empunhando: `uma espada curta`

---

## 3. O que já foi descoberto

### Autoquests de Nível 30+
- `Xeque-mate`: ativa no Tabuleiro de Xadrez (requisito Nível 30+, qualquer alinhamento).
- `Ajuda Mágica`: ativa em Midgaard (requisito Nível 30+, qualquer alinhamento).

### Catálogo Completo de Mecânicas Inéditas a Testar
Entregue integralmente para execução e validação de quem estiver jogando:

1. **Tradições Arcanas e Percepção Mágica (Grebolius Nv 31 / 420 Mana):**
   - `cast 'detect alignment'`: revelar aura moral visual de NPCs (vermelha/azul/branca) para proteger a postura heroica (Invariante 15).
   - `cast 'detect invisibility'`: revelar objetos invisíveis e presenças ocultas.
   - `cast 'sense life'`: detectar formas de vida em salas escuras ou escondidas (`hide`).
   - `cast 'locate object' <item>`: radar global para descobrir sala ou mob portador de itens do mundo.
   - `cast 'sleep' <alvo>`: adormecer oponentes para controle de duplas (dano físico $1{,}5\times$ no alvo que dorme).
   - `cast 'blindness' <alvo>`: cegar inimigo (-4 AC e hitroll).
   - `cast 'infravision'`: enxergar no escuro sem tocha.
   - `cast 'ventriloquate' <alvo> <mensagem>`: projetar voz arcana.

2. **Sobrevivência, Alquimia e Rastreamento:**
   - `sip <recipiente|fonte>`: bebericar pequenos goles sem gastar todo o cantil.
   - `taste <recipiente|comida>`: degustar para identificar sabores ou detectar venenos.
   - `pour <origem> <destino>` e `pour <recipiente> out`: transferir líquidos ou esvaziar frascos.
   - `track <monstro>`: farejar rastro e receber indicação direcional da bússola (`You sense a trail south from here!`).
   - `diagnose [alvo]`: diagnóstico clínico com relatório textual preciso dos ferimentos em combate.

3. **Economia, Banco Portátil e Descarte:**
   - `cashcard` (Banco Portátil, item 3036 no Empório *The Grocer*): comprar e testar `balance`, `deposit <n>` e `withdraw <n>` em qualquer lugar do mundo fora do Templo.
   - `donate <item>`: doação remota direta para a sala de doações do Templo de Midgaard.
   - `junk <item>`: descarte destrutivo que recompensa na hora com ouro ou EXP.
   - `value <item>`: cotar preço de venda com lojista antes de fechar negócio.

4. **Comunicação, Murais e Correios:**
   - Correios MMS (sala 3062): testar `check` (cartas na fila), `receive` (receber carta) e `mail <jogador>` (enviar carta por 150 moedas).
   - Murais Públicos (`gen_board`): testar `read <n>` e `write <título>` na Praça do Comércio e guildas.
   - Escrita de bilhetes portáteis: `write <papel> com <pena>`.
   - `whisper <alvo> <mensagem>` e `ask <alvo> <pergunta>`.
   - `reply <mensagem>`: responder diretamente ao último tell.
   - `norepeat`: toggle de supressão do eco de falas.

5. **Eventos Cênicos e Easter Eggs Vivos (Verificação de Relógio `time`):**
   - **O Prefeito de Midgaard:** verificar às 6h e às 20h do jogo se abre/fecha o portão do bazar com as falas clássicas.
   - **A Corte do Rei Welmar (Castelo de Welmar, zona 150):**
     - Monólogo latino de 4 estrofes do Rei Welmar às 12h do jogo na sala do trono.
     - Broncas do Capitão Peter na guarda (*"limpe essas botas!"*, *"cota enferrujada!"*).
     - Jogatina de dados de Jerry no alojamento.
     - Guarda dos gêmeos Tim e Tom.
   - **Fido de Midgaard:** verificar se devora cadáveres na rua e cospe os itens contidos limpos na calçada.
   - **Recepcionista da Estalagem:** verificar se executa emotes sociais aleatórios a cada tick (`smile, sigh, yawn, dance`).

---

## 4. Os bloqueios, e o que já foi tentado

- **Identificação do NPC Patrono de Xeque-mate:** Localizar no Tabuleiro de Xadrez o iniciador formal da quest sem agredir peças brancas (preservando o alinhamento 311).
- **Controle de Tempo (< 3h):** Medir o tempo de relógio do mundo real desde o primeiro comando para decidir o encadeamento de `Ajuda Mágica`.
- **Filtro em Tempo Real pelo Operador:** Nenhum comando da lista acima foi pré-excluído. O operador deve tentar cobrir o máximo possível, descartando na hora aquilo que se mostrar inviável ou sem sentido no contexto prático.

---

## 5. O próximo passo, e só ele

O agente operador deve seguir este fluxo integrado:

### 1. Início e Testes Arcanos/Sobrevivência Imediatos (Templo de Midgaard)
1. Acordar (`wake; stand`).
2. Testar de imediato os comandos de percepção no Templo:
   - `cast 'detect alignment'` (verificar se a visualização de auras auxilia na identificação de peças/patronos);
   - `cast 'detect invisibility'`;
   - `cast 'sense life'`.
3. Testar `sip cantil`, `taste cantil` e provar a água da fonte. Testar `pour`.

### 2. Marcha para o Xadrez e Autoquest `Xeque-mate` (Missão Principal)
4. Deslocar-se ao Grande Tabuleiro de Xadrez via rota segura (`go_xadrez`).
5. No caminho ou na entrada do tabuleiro, testar `track peao` ou `track cavaleiro`.
6. Testar `cast 'locate object'` buscando peças ou armas conhecidas.
7. Localizar o NPC patrono de `Xeque-mate`, ouvir o diálogo integral sem cortar falas e confirmar o objetivo em `score tudo`.
8. Durante as lutas contra peças negras da missão:
   - Rodar `diagnose` durante o combate para registrar a resposta clínica de ferimentos.
   - Testar `cast 'sleep'` para neutralizar alvos ou conter múltiplos inimigos.
   - Testar `cast 'blindness'`.
9. Concluir todos os passos de `Xeque-mate` respeitando a validação de etapas (Invariante 13).

### 3. Avaliação Temporal (< 3h) e Autoquest `Ajuda Mágica`
10. Checar o tempo decorrido desde o início da sessão:
    - Se `Xeque-mate` foi concluída em **menos de 3 horas de relógio real**:
      - Retornar a Midgaard (`recall`).
      - Localizar o patrono e iniciar imediatamente a autoquest `Ajuda Mágica`.
      - Concluir seus objetivos.

### 4. Circuito Urbano: Economia, Comunicação e Easter Eggs
11. Em Midgaard (no retorno ou trânsito):
    - Ir ao Empório (*The Grocer*, sala 3013), comprar o `cashcard` (item 3036) e testar `balance`, `deposit` e `withdraw` na rua.
    - Testar `donate` e `junk` em itens dispensáveis.
    - Visitar os Correios (sala 3062) e testar `check`, `receive` e `mail`.
    - Testar `read 1` no mural da Praça do Comércio.
    - Testar `norepeat`, `reply`, `whisper` e `ask`.
    - Checar o relógio (`time`): se perto das 6h/20h, observar o Prefeito de Midgaard; se perto das 12h, verificar a corte do Rei Welmar no Castelo.

*(Lembrete ao operador: se qualquer um dos testes urbanos ou cênicos se mostrar excessivamente trabalhoso, demorado ou impraticável no momento, exclua-o na hora sem prejuízo da missão).*

---

## 6. NÃO REPITA

1. **NÃO priorize testes secundários em detrimento das autoquests — a missão primária é Xeque-mate (e Ajuda Mágica se < 3h).**
2. **NÃO ataque peças brancas no Tabuleiro de Xadrez — Grebolius é de alinhamento bom (311).**
3. **NÃO pegue armaduras ou itens amaldiçoados (NODROP).**
4. **NÃO entregue itens sem validar a sub-etapa exata em `score tudo` (Invariante 13).**
5. **NÃO automatize diálogos verbais com NPCs (Invariante 14).**
6. **NÃO machuque seres inocentes ou pacíficos (Invariante 15).**
7. **NÃO dê `quit` com autoquest em andamento (Invariante 8) — encerre sempre com `save` e sono no Templo.**

---

## 7. Ferramentas e comandos (Checklist Geral)

- **Missão:** `score tudo`, `look`, `exits`, `say`, `give`, `autoquest listar`.
- **Arcanos:** `cast 'detect alignment'`, `cast 'detect invisibility'`, `cast 'sense life'`, `cast 'locate object' <item>`, `cast 'sleep'`, `cast 'blindness'`, `cast 'infravision'`, `cast 'ventriloquate'`.
- **Sobrevivência:** `sip`, `taste`, `pour`, `diagnose`, `track <alvo>`.
- **Economia:** `cashcard` (`balance`, `deposit`, `withdraw`), `donate <item>`, `junk <item>`, `value <item>`.
- **Comunicação/Murais:** `mail`, `check`, `receive`, `read <n>`, `write`, `whisper`, `ask`, `reply`, `norepeat`.
- **Cênicos/Mundo:** `time` (horários do Prefeito 6h/20h e Rei Welmar 12h), observação do Fido e Recepcionista.

---

## 8. Devolutiva técnica

| Descobri | Registrei em | O quê |
|---|---|---|
| mapa | `mapa.json` | PENDENTE (rotas urbanas mapeadas; novas salas do Xadrez e Castelo entrarão ao explorar) |
| referência do servidor | `maquina/verificacoes.md` | Protocolo integral dos 27 comandos e mecânicas inéditas documentado |
| fato do mundo | `conhecimento.md` | §57 catalogando o compêndio completo de mecânicas a testar |
| erro do motor | `automato/CHANGELOG.md` | v1.6.14 documentando incorporação das autoquests + checklist integral ao Capítulo 11 |

---

## 9. Como encerrar a sua sessão

1. Retornar ao Templo de Midgaard (`recall`).
2. Sancionar alimentação e água.
3. Executar `save` e `sleep`.
4. Registrar as respostas literais dos comandos testados (e os motivos dos descartados) em `maquina/verificacoes.md` e na nova evidência `evidence/dia156*.json`.
5. Criar o Plano 026 detalhando os avanços nas autoquests e nas descobertas de comandos.
6. Rodar `python scripts/sync_hero.py --hero grebolius`, `python scripts/check_project.py` e `python scripts/devolutiva.py`.
