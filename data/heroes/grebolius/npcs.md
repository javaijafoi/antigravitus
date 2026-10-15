# 👥 Catálogo Oficial de NPCs de Midgaard e Masmorras — Grebolius

> Este documento é o compêndio estruturado de todas as figuras, comerciantes, mestres e sentinelas encontrados por Grebolius no mundo de Devil's Bob MUD.  
> Sua finalidade é subsidiar o herói no **Modo Padrão** com informações consolidadas de comércio, diálogos, requisitos de quests e controle de auditoria cíclica (uma verificação maleável por ciclo). No Modo Aventura, o herói não dispersa e foca exclusivamente na quest ativa.

---

## ✦ Regra Operacional de Sondagem e Auditoria (Modo Padrão)

1. **Sondagem no Primeiro Contato:**
   - Ao encontrar um NPC pela primeira vez, o herói não ataca. Executa `look <npc>` e comandos diagnósticos contextuais:
     - Se parecer comerciante: executa `list` (ou `listar`) para mapear itens, preços e níveis.
     - Se parecer mentor/mestre: executa `practice` para verificar opções de treino.
     - Se parecer dador de tarefas: executa `autoquest`, `'sim` ou `'não`.
2. **Cadência de Manutenção e Auditoria:**
   - **Atualização Diária:** Se a sessão diária revelar qualquer novo NPC, novo item à venda, alteração de preço ou diálogo inédito, o registro deve ser inserido neste documento no encerramento do dia.
   - **Pendência Maleável por Ciclo:** A checagem de estoques e novidades não exige desvios artificiais forçados; é tratada como uma pendência contínua que é sanada organicamente conforme as expedições passarem próximas aos NPCs durante o ciclo.

---

## 🏛️ 1. Mestres, Guias e Mentores

| NPC | Localização (`room_id`) | Função / Serviço | Interações & Comandos | Status / Última Auditoria |
| :--- | :--- | :--- | :--- | :--- |
| **Mestre da Guilda dos Magos** | `laboratorio_magos` | Treinadora Suprema da Guilda de Magos | `practice` (abre lista de magias conhecidas e disponíveis para treino com sessões). | Auditado Dia 81 (15 treinos em estoque). Protegida por barreira de luz. |
| **Mago Aventureiro** | `bar_magos` | Mentor / Doador de Autoquest (*Dicas Mágicas*) | `autoquest`, `'sim`, `'não`. Pede a entrega de um *pergaminho de retorno*. | Auditado Dia 80. Missão ativa aguardando 9.202 moedas. |
| **Winkan, o Engenheiro do Caos** | `templo_midgaard` | Veterano Lendário de Midgaard | Em meditação profunda sob luz ofuscante. Não oferece diálogo mecânico ativo. | Auditado historicamente. Figura de respeito. |
| **Carecacabeludo, o Preservador**| `templo_midgaard` | Guardião Sagrado da Nave Central | Sentinela cerimonial. Vigilância pacífica. | Auditado historicamente. Neutro. |
| **Aiko, a Instruída** | `corredor_sujo` (Masmorra dos Novatos) | Aventureira Observadora / Guia | Presente no corredor das catacumbas. Diálogos informativos a conferir. | Auditada Dia 51. Neutra e pacífica. |

---

## 🛒 2. Mercadores, Artesãos e Lojas

### A. Padaria de Midgaard
* **NPC Responsável:** O Padeiro (`padaria` — Rua Principal Oeste, 1 norte).
* **Função:** Fornecimento de rações e pães de alto rendimento calórico e baixo peso.
* **Comandos:** `list`, `buy <item>`.
* **Catálogo de Preços (Auditado no Dia 81):**
  | Item | Preço | Peso Estimado | Custo-Benefício |
  | :--- | :---: | :---: | :--- |
  | **Pão Recheado** | 6 ouros | ~1 lb | **Excelente (Ração Primária Oficial)**. Sacia fome prolongada por custo quase nulo. |
  | **Broa de Milho** | 13 ouros | ~1-2 lbs | Bom. Reserva calórica padrão. |
  | **Rosquinha Malhada** | 151 ouros | ~1 lb | Luxo. Rendimento idêntico ao pão por custo desproporcional. |

---

### B. Loja de Magias de Midgaard
* **NPC Responsável:** O Feiticeiro Mercador (`loja_magias` — Fim da Rua Principal Oeste, 1 norte).
* **Função:** Artefatos arcanos, poções, varinhas e pergaminhos sagrados.
* **Comandos:** `list`, `buy <item>`.
* **Catálogo de Preços (Auditado nos Dias 42 e 80):**
  | Item | Preço | Nível Mín. | Enc. | Utilidade Estratégica |
  | :--- | :---: | :---: | :---: | :--- |
  | **Pergaminho de Retorno** | 9.202 ouros | Nv 0 | 1 | **Meta da Quest 'Dicas Mágicas'** e fuga de emergência absoluta. |
  | **Pergaminho de Identificação** | 4.601 ouros | Nv 0 | 1 | Identifica propriedades, bônus e requisitos de itens (como o Anel +2E). |
  | **Poção Amarela de Detectar Invisibilidade** | 5.370 ouros | Nv 0 | 1 | Concede visão arcana de seres invisíveis em campo. |
  | **Pergaminho de Remover Maldições** | 8.509 ouros | Nv 0 | 1 | Quebra maldições de equipamentos presos. |
  | **Cajado Retorcido** | 14.570 ouros | Nv 38 | 1 | Equipamento de combate arcano de alto grau. |
  | **Bastão Cinza de Invisibilidade** | 92.233 ouros | Nv 29 | 1 | Camuflagem mecânica sem gasto de mana. |
  | **Pergaminho Portador de Tempestades** | 574.999 ouros | Nv 1 | 1 | Destruição elemental massiva em área. |

---

### C. Loja de Armaduras de Midgaard
* **NPC Responsável:** O Armeiro (`loja_armaduras` — Rua Principal Oeste, 1 sul).
* **Função:** Forjamento e venda de proteções corporais; compra de sucatas de armaduras.
* **Comandos:** `list`, `buy <item>`, `sell <item>`.
* **Catálogo de Preços de Bronze e Aço (Auditado no Dia 80):**
  | Peça de Armadura | Preço | Slot Corporal | AC Estimada |
  | :--- | :---: | :---: | :---: |
  | **Um par de braçadeiras de bronze** | 1.750 ouros | Braços | Média |
  | **Um par de manoplas de bronze** | 1.750 ouros | Mãos | Média |
  | **Uma cota de malha de bronze** | 2.500 ouros | Corpo | Alta |
  | **Um par de perneiras de bronze** | 3.500 ouros | Pernas | Média-Alta |
  | **Um elmo de bronze** | 3.500 ouros | Cabeça | Média-Alta |
  | **Um peitoral de bronze** | 7.000 ouros | Peito | Alta |
  | **Um peitoral reforçado de bronze** | 18.000 ouros | Peito | Superior |
* **Cotações de Compra de Sucata (Histórico):**
  - Gorro de couro simples: 75 ouros.

---

### D. Loja de Armas de Midgaard
* **NPC Responsável:** O Ferreiro Armeiro (`loja_armas` — Rua Principal Leste II, 1 norte).
* **Função:** Armamento marcial e lâminas; principal comprador de armas descartadas.
* **Comandos:** `list`, `buy <item>`, `sell <item>`.
* **Cotações de Compra de Sucata (Auditadas até Dia 60):**
  | Arma Descartada | Cotação Paga | Custo-Benefício de Venda |
  | :--- | :---: | :--- |
  | **Espada Longa Militar** | 240 ouros | Excelente (carregar apenas se estiver a poucos passos da loja). |
  | **Picareta Pesada (+10L)** | 120 ouros | Péssimo (peso excessivo esgota estamina; não compensa carregar). |
  | **Lâmina Improvisada (+3L)** | 120 ouros | Bom (peso leve). |
  | **Adaga Comum / Punhal de Novato** | 4 a 10 ouros | Regular (vender apenas em pacotes de limpeza de inventário). |

---

### E. O Armazém Geral
* **NPC Responsável:** O Merceeiro Impaciente (`armazem` — Rua Principal Leste I, 1 norte).
* **Função:** Equipamentos de utilidade, mochilas e iluminação.
* **Comandos:** `list`, `buy <item>`.
* **Catálogo de Preços (Auditado no Dia 51):**
  | Item | Preço | Utilidade |
  | :--- | :---: | :--- |
  | **Uma Mochila de Carga** | 30 ouros | Essencial (recipiente para provisões e itens leves). |
  | **Uma Tocha** | 15 ouros | Iluminação básica para masmorras sem luz. |
  | **Uma Mala** | 75 ouros | Recipiente pesado de viagem. |
  | **Uma Lanterna** | 75 ouros | Fonte de luz duradoura. |
  | **Uma Atadura** | 300 ouros | Curativo emergencial. |
  | **Álbum de Figurinhas** | 15.000 ouros | Item colecionável cívico. |
  | **Cartão de Crédito** | 60.000 ouros | Luxo financeiro. |
* **Aviso de Indisponibilidade:** O Merceeiro **NÃO VENDE** odres, cantis gigantes ou barris portáteis.

---

## 📜 3. NPCs de Missões e Alianças

| NPC | Localização (`room_id`) | Missão Vinculada | Diálogos & Condições | Histórico e Desfecho |
| :--- | :--- | :--- | :--- | :--- |
| **Guarda Novato** | `pequena_sala` (Masmorra dos Novatos) | *A Coleira do Dragão* | Recebe a coleira perdida do bebê dragão. | **Concluída no Dia 31**. Recompensa concedida: 5.000 EXP. |
| **Novato Alquimista** | `sala_alquimista` (Masmorra dos Novatos) | *Limpando Monstros* | Diálogos: `'sim`, `'não`, `autoquest`. Recompensa por insetos e chifres de minotauro. | **Ativa**. Entregas recorrentes devem ser tratadas de forma calejada e rotineira. |
| **O Pacificador** | `praca_templo` / `entrada_estalagem` | Ordem Urbana / Aliança Cívica | Diálogo pacífico; convida Grebolius a prestar auxílio quando estiver mais forte. | Vigia colossal. Aliado neutro em caso de invasão. |

---

## ⚔️ 4. Sentinelas, Guardas e Barreiras

| NPC | Localização (`room_id`) | Postura | Regra de Interação |
| :--- | :--- | :--- | :--- |
| **Pelotão de Guardas Municipais (8x)** | `portao_leste` / `portao_oeste` | Defesa Militar Máxima | **Não provocar sob nenhuma hipótese.** Barram novatos com lâminas mortais. |
| **Mago Guardião** | `entrada_guilda_magos` | Sentinela Protetor | Protegido por luz ofuscante; permite passagem para o Laboratório e Bar. |
| **Sentinela dos Ladrões** | `entrada_guilda_ladroes` | Hostil / Bloqueador | Vigia sombrio; desdenha de magos e novatos. Não forçar entrada. |
| **Sentinela dos Guerreiros** | `entrada_guilda_guerreiros` | Hostil / Bloqueador | Brutamontes armado; barra novatos sem treinamento marcial. |

---

## 📅 5. Registro de Auditorias por Ciclo

| Ciclo | Marco | NPCs Auditados | Descobertas e Mudanças |
| :---: | :---: | :--- | :--- |
| **Ciclo 5** | Dia 42 | Feiticeiro (Loja de Magias) | Mapeamento completo de pergaminhos, poções e varinhas. |
| **Ciclo 6** | Dia 51 | Merceeiro (Armazém Geral) | Mapeamento de recipientes e confirmação de ausência de odres/barris. |
| **Ciclo 8** | Dia 80 | Armeiro (Loja de Armaduras) e Mago Aventureiro | Mapeamento de peças de bronze (1.750 a 18.000) e requisitos de Dicas Mágicas. |
| **Ciclo 9** | Dia 81 | Padeiro (Padaria) e Mestre da Guilda | Reconfirmação de pães a 6 moedas e 15 sessões de treino acumuladas. |
| **Ciclo 9** | Dia 90+ | *Aguardando próxima auditoria* | Checagem programada para início do Ciclo 10. |
