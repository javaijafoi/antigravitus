# Plano 024 — Capítulo 11 (Tomo II): Autoquest Xeque-Mate e Ajuda Mágica

| | |
|---|---|
| **Criado em** | 2026-10-18 · Dia 156 |
| **Por** | Gemini 3.8 Flash (High) |
| **Herói** | grebolius |
| **Objetivo** | Capítulo 11 (Tomo II — As Chaves do Tabuleiro) — Iniciar e executar a autoquest Xeque-mate no Grande Tabuleiro de Xadrez; se concluída em menos de 3 horas de tempo real, executar também a autoquest Ajuda Mágica |
| **Sessão encerrada?** | sim — personagem em total segurança no Templo de Midgaard; HP 196/196, Mana 420/420, MV 144/144, CA 143 (sem armor), wimpy 45, Alinhamento 311 (Bom), Nível 31 consolidado, save e sono confirmados; live_daemon finalizado |

---

## 1. Onde o objetivo está

O **Tomo I ("O Nome no Vazio", Capítulos 0 a 10)** foi oficialmente **CONCLUÍDO e SELADO**.
O Capítulo 10 ("Dez Cabeças Inéditas e o Fecho do Primeiro Tomo") foi completado com a narrativa dos dez monstros malignos inéditos, a expiação da censura moral e a reflexão abrangente de toda a trajetória do tomo: da mendicância no lixo até a consagração como maga virtuosa de 420 de mana e colar púrpuro anti-DT.

O **Tomo II ("As Chaves do Tabuleiro")** abre com o **Capítulo 11**, regido pela diretiva expressa do autor Peter:
> *"um cap 11 vai ser fazer xeque mate e se for facil (terminar em menos de 3h do mundo real) fazer tbm ajuda magica."*

1. **Autoquest Xeque-mate:** Desbloqueada no catálogo (`autoquest listar`) a partir do nível 30 para qualquer alinhamento. Passa-se no Grande Tabuleiro de Xadrez, local que Grebolius já conhece e onde caça peões, cavaleiros e bispos.
2. **Autoquest Ajuda Mágica:** Também desbloqueada a partir do nível 30 para qualquer alinhamento. Se a resolução de Xeque-mate for concluída em menos de 3 horas de tempo real, emendar imediatamente com esta missão.

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
- **Suprimentos:** Cantil saciado de água cristalina, pão da sacola consumido.
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

1. **Autoquest Xeque-mate no Catálogo:**
   - Exige nível 30+ (Grebolius está no nível 31).
   - Iniciação: Verificar no Tabuleiro de Xadrez qual NPC entrega a missão (possíveis patronos: o Rei Branco, o Peão Branco ou figuras neutras/espectadores do tabuleiro).
2. **Autoquest Ajuda Mágica no Catálogo:**
   - Exige nível 30+ (Grebolius está no nível 31).
   - Iniciação: Provavelmente ligada a mestres da Guilda dos Magos, magos errantes ou pesquisadores de Midgaard.
3. **Mecânica do Xadrez:**
   - Peões negros são alvos fáceis (raio único os destrói);
   - Cavaleiros e Bispos exigem 3 a 4 raios;
   - Peças brancas não devem ser agredidas para preservar o alinhamento bom (311);
   - Armaduras amaldiçoadas dos peões continuam expressamente proibidas de coleta/posse (Invariante 10).

---

## 4. Os bloqueios, e o que já foi tentado

- **Identificação do NPC Patrono de Xeque-mate:**
  - Na rotina de grind do Xadrez, a caça foca nas casas pretas (peões e nobreza negra).
  - É necessário explorar as casas brancas ou a borda do tabuleiro com cautela para localizar o NPC que inicia a autoquest com diálogo formal.
- **Controle de Tempo Real (< 3h):**
  - O cronômetro de tempo real deve ser monitorado desde o início da primeira ação no MUD. Se Xeque-mate cair rapidamente, avançar imediatamente para Ajuda Mágica.

---

## 5. O próximo passo, e só ele

1. Acordar no Templo (`wake; stand`).
2. Digitar `autoquest listar` para confirmar as informações do iniciador de `Xeque-mate` e `Ajuda Mágica`.
3. Deslocar-se ao Grande Tabuleiro de Xadrez via rota segura (`go_xadrez`).
4. Identificar o NPC patrono de `Xeque-mate` e ouvir o diálogo integral até o fim (sem cortar falas).
5. Confirmar em `score tudo` o início formal da quest sob `[Autoquests em andamento]`.
6. Executar os objetivos da quest no Tabuleiro.
7. Se concluída em menos de 3 horas de relógio, retornar a Midgaard e iniciar `Ajuda Mágica`.

---

## 6. NÃO REPITA

1. **NÃO ataque peças brancas no Tabuleiro de Xadrez — Grebolius é de alinhamento bom (311) e defende o lado da luz.**
2. **NÃO pegue armaduras ou itens amaldiçoados (NODROP).**
3. **NÃO entregue itens sem validar a sub-etapa exata em `score tudo` (Invariante 13).**
4. **NÃO automatize diálogos verbais com NPCs (Invariante 14).**
5. **NÃO machuque seres inocentes ou pacíficos (Invariante 15).**
6. **NÃO dê `quit` com autoquest em andamento (Invariante 8) — encerre sempre com `save` e sono no Templo.**

---

## 7. Ordem de leitura recomendada

1. `AGENTS.md` (regras fundamentais de operação e invariantes).
2. `data/heroes/grebolius/planos/plano024.md` (este documento).
3. `data/heroes/grebolius/capitulos.json` (Capítulo 10 fechado com o Tomo I, Capítulo 11 aberto no Tomo II).
4. `data/heroes/grebolius/state.json` (estado mecânico consolidado).

---

## 8. Devolutiva técnica

| Descobri | Registrei em | O que mudou |
|---|---|---|
| Abertura do Tomo II e Capítulo 11 (Xeque-mate e Ajuda Mágica) | `data/heroes/grebolius/capitulos.json` | Tomo II adicionado em `tomos`; Capítulo 10 expandido com reflexão do Tomo I; Capítulo 11 aberto com diretiva de <3h |
| Requisitos de nível 30+ de Xeque-mate e Ajuda Mágica | `data/heroes/grebolius/conhecimento.md` | Catálogo de autoquests atualizado com as missões abertas no Nível 31 |
| Referência de autoquests de nível 30 no DeBo | `maquina/verificacoes.md` | Documentação de `autoquest listar` para Nível 30+ e encarnação 1 |
| Validação de cota do modelo ativo | `automato/CHANGELOG.md` | v1.6.13 preservada e sem novos erros de motor pendentes |
