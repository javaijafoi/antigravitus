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
| **Mestre da Guilda dos Magos** | `laboratorio_magos` | Treinadora Suprema da Guilda de Magos | `practice` (abre lista de magias conhecidas e disponíveis para treino com sessões). | Auditado Dia 82 (15 treinos em estoque). Protegida por barreira de luz. |
| **Mago Aventureiro** | `bar_magos` | Mentor / Doador de Autoquest (*Dicas Mágicas*) | `autoquest`, `'sim`, `'não`, `give pergaminho mago`. Pede a entrega de um *pergaminho de retorno*. | Auditado Dia 82. Missão ativa. |
| **Winkan, o Engenheiro do Caos** | `sala_leitura` | Veterano Lendário de Midgaard | Em meditação profunda sob aura de poder e serenidade na Sala de Leitura. | Auditado ao vivo no Dia 82 na Sala de Leitura. |
| **Losilly, a Urdidura** | `sala_leitura` | Heroína Lendária de Midgaard | Equipada com raio de luz (+4E), coleiras de dragão, armadura de cristal (+1E) e bolsa de Pellinore. | Auditada ao vivo no Dia 82 na Sala de Leitura. |
| **Clérigo Guardião** | `guilda_clerigos_entrada` | Sentinela do Enclave Sagrado | Cota de malha prateada e maça polida; vigia o portal de alabastro dos clérigos. | Auditado Dia 82. |
| **Zelador de Midgaard** | `praca_templo` / `entrada_javali` | Auxiliar Cívico e Zelador da Cidade | Varrendo pacientemente as lajes ao redor da Fonte de Mármore Azul. | Auditado Dia 82. |
| **Carecacabeludo, o Preservador**| `templo_midgaard` | Guardião Sagrado da Nave Central | Sentinela cerimonial. Vigilância pacífica. | Auditado historicamente. Neutro. |
| **Aiko, a Instruída** | `corredor_sujo` (Masmorra dos Novatos) | Aventureira Observadora / Guia | Presente no corredor das catacumbas. Diálogos informativos a conferir. | Auditada Dia 51. Neutra e pacífica. |

---

## 🛒 2. Mercadores, Artesãos e Lojas

> **Preços e estoques estão consolidados em [itens.md](itens.md)** — a tabela de itens com ID por
> item e por oferta, referenciando o NPC. Este arquivo descreve **quem é** cada mercador; aquele
> diz **o que ele vende e por quanto**. Onde os dois discordarem, vale o `list` ao vivo.
>
> ⚠️ **Invisibilidade bloqueia comércio.** O balconista responde *"Não negocio com quem não vejo!"* e
> o `list` não devolve nada. Rodar **`visible`** antes de `list`, `buy` ou `sell`.

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

### F. O Bar do Javali Roncador
* **NPC Responsável:** O Taverneiro do Javali (`bar_javali` — Ala Leste da Praça do Templo, dentro da Estalagem).
* **Função:** Fornecimento de bebidas tradicionais, cerveja ale, cospefogo e recipientes maiores de cerveja.
* **Comandos:** `list`, `buy <item>`.
* **Catálogo de Preços (Auditado no Dia 82):**
  | Item | Preço | Nível | Utilidade / Observação |
  | :--- | :---: | :---: | :--- |
  | **Uma garrafa de especialidade local** | 22 ouros | Nv 0 | Bebida regional da estalagem. |
  | **Uma garrafa de cospefogo** | 55 ouros | Nv 0 | Aguardente forte e destilada. |
  | **Uma garrafa de cerveja ale** | 11 ouros | Nv 0 | Bebida de cevada de baixo custo. |
  | **Uma garrafa de cerveja** | 22 ouros | Nv 0 | Cerveja comum de taberna. |
  | **Um barril de cerveja** | 330 ouros | Nv 0 | **Recipiente massivo de líquido.** Maior reservatório comercial da cidade. |

---

### G. A Loja de Animais
* **NPC Responsável:** O Garoto da Loja de Animais (`loja_animais` — Rua Principal Leste I, 1 sul).
* **Função:** Venda de mascotes, guardas caninos e montarias treinadas; funciona também como estábulo.
* **Comandos:** `list`, `buy <animal>`.
* **Catálogo de Animais (Auditado no Dia 82):**
  | Animal | Preço | Porte / Função |
  | :--- | :---: | :--- |
  | **Um gatinho** | 300 ouros | Pequeno felino doméstico. |
  | **Um cachorrinho** | 300 ouros | Filhote de guarda. |
  | **Um beagle** | 300 ouros | Cão rastreador de pequeno porte. |
  | **Um rottweiler** | 900 ouros | Cão de guarda robusto e musculoso. |
  | **Um lobo** | 1.800 ouros | Predador treinado de grande porte para combate e patrulha. |

---

### H. O Correio de Midgaard
* **NPC Responsável:** O Carteiro de Midgaard (`correio_midgaard` — Entrada do Javali Roncador, 1 norte).
* **Função:** Sistema postal oficial do reino; envio e recebimento de correspondência entre jogadores.
* **Comandos:** `mail <destinatário>`, `check`.
* **Status:** Auditado no Dia 82. O Carteiro veste uniforme rústico com teias-de-aranha; avisa prontamente quando não há correspondência pendente.

---

### I. A Recepção da Estalagem Javali Roncador
* **NPC Responsável:** A Recepcionista (`recepcao_javali` — Entrada do Javali Roncador, 1 cima).
* **Função:** Aluguel de quartos e leitos para aventureiros sem guilda ou santuário garantido salvarem seus pertences.
* **Comandos:** `look`, diálogo sobre quartos.

---

### J. O Bar dos Magos
* **NPC Responsável:** O Garçom dos Magos (`bar_magos` — Entrada da Guilda dos Magos, 1 sul).
* **Função:** Bebidas para aprendizes e mestres arcanos em ambiente com ilusões flutuantes.
* **Catálogo (Auditado no Dia 82):** Garrafa de cerveja ale (10 ouros), Garrafa de cospefogo (50 ouros). Garçom empunha adaga amolada.

---

### K. A Taverna Encardida
* **NPC Responsável:** Filthy (`taverna_encardida` — Sul do Fim do Beco Pobre).
* **Função:** Ponto de encontro de renegados e marinheiros no submundo de Midgaard; ambiente fétido e imundo.
* **Comandos:** `list`, `buy <item>`.
* **Catálogo (Auditado no Dia 82):**
  | Item | Preço | Nível | Utilidade / Observação |
  | :--- | :---: | :---: | :--- |
  | **Uma garrafa de especialidade local** | 20 ouros | Nv 0 | Bebida regional barata. |
  | **Uma garrafa de cospefogo** | 50 ouros | Nv 0 | Aguardente pura do submundo. |
* **Outros Habitantes:** Dois mendigos pedindo esmolas e cães farejando entulho.

---

### L. Outras Figuras Notáveis e Autoridades de Midgaard
* **O Prefeito de Midgaard** (`praca_comercio`): Autoridade máxima cívica; transita pela praça central fiscalizando o comércio e os murais.
* **Negelok, o Super Uper Duper** (`templo_midgaard`): Veterano supremo voando montado em O Grifo Real, cercado por uma aura multicolorida.
* **O Pranteador da Cidade** (`beco_escuro`): Figura trágica chorando silenciosamente na viela leste.
* **Mercenários Urbanos** (`beco_escuro`): Guerreiros de aluguel reunidos junto a espadas curtas e portais mágicos.
* **Guarda da Guilda dos Necromantes** (`guilda_necromantes`): Sentinela temível protegido por enormes ossos; humilha e proíbe terminantemente a entrada de não-necromantes ao Bar dos Necromantes ("Só necromantes entram aqui").

---

## 📜 3. NPCs de Missões e Alianças

| NPC | Localização (`room_id`) | Missão Vinculada | Diálogos & Condições | Histórico e Desfecho |
| :--- | :--- | :--- | :--- | :--- |
| **Guarda Novato** | `pequena_sala` (Masmorra dos Novatos) | *A Coleira do Dragão* | Recebe a coleira perdida do bebê dragão. | **Concluída no Dia 31**. Recompensa concedida: 5.000 EXP. |
| **Novato Alquimista** | `sala_alquimista` (Masmorra dos Novatos) | *Limpando Monstros* | Diálogos: `'sim`, `'não`, `autoquest`. Recompensa por insetos e chifres de minotauro. | **Ativa**. Entregas recorrentes devem ser tratadas de forma calejada e rotineira. |
| **O Pacificador** | `praca_templo` / `termino_rua_oeste` / `portao_oeste` | Ordem Urbana / Aliança Cívica | Diálogo pacífico; vigia colossal das muralhas e praças. | Aliado neutro garantidor da paz pública. |
| **Mago Aventureiro** | `bar_magos` | *Dicas Mágicas* (Autoquest exclusiva) | Diálogo de instruções para jovens magos. | Disponível para o nível de Grebolius (1-29). |

---

## ⚔️ 4. Sentinelas, Guardas e Barreiras

| NPC | Localização (`room_id`) | Postura | Regra de Interação |
| :--- | :--- | :--- | :--- |
| **Pelotão de Guardas Municipais (8x)** | `portao_leste` / `portao_oeste` | Defesa Militar Máxima | **Não provocar sob nenhuma hipótese.** Barram novatos com lâminas mortais. |
| **Mago Guardião** | `entrada_guilda_magos` | Sentinela Protetor | Protegido por luz ofuscante; permite passagem para o Laboratório e Bar. |
| **Sentinela dos Ladrões** | `entrada_guilda_ladroes` | Hostil / Bloqueador | Vigia sombrio; desdenha de magos e novatos. Não forçar entrada. |
| **Sentinela dos Guerreiros** | `entrada_guilda_guerreiros` | Hostil / Bloqueador | Brutamontes armado; barra novatos sem treinamento marcial. |
| **Guarda Necromante** | `entrada_guilda_necromantes` | Bloqueador Opressor | Protegido por ossos; barra e humilha invasores. |

---

## 📅 5. Registro de Auditorias por Ciclo

| Ciclo | Marco | NPCs Auditados | Descobertas e Mudanças |
| :---: | :---: | :--- | :--- |
| **Ciclo 5** | Dia 42 | Feiticeiro (Loja de Magias) | Mapeamento completo de pergaminhos, poções e varinhas. |
| **Ciclo 6** | Dia 51 | Merceeiro (Armazém Geral) | Mapeamento de recipientes e confirmação de ausência de odres/barris. |
| **Ciclo 8** | Dia 80 | Armeiro (Loja de Armaduras) e Mago Aventureiro | Mapeamento de peças de bronze (1.750 a 18.000) e requisitos de Dicas Mágicas. |
| **Ciclo 9** | Dia 81 | Padeiro (Padaria) e Mestre da Guilda | Reconfirmação de pães a 6 moedas e 15 sessões de treino acumuladas. |
| **Ciclo 9** | Dia 82 | Auditoria Urbana Geral Completa (100% Midgaard) | Taverneiro do Javali (barris de cerveja 330 ouros), Carteiro (serviço postal), Garoto dos Animais (lobos e cães), Winkan e Losilly (Sala de Leitura), Clérigo Guardião, Filthy (Taverna Encardida), Prefeito de Midgaard, Negelok em Grifo Real, Pranteador, Mercenários, Guarda Necromante (ossos), Odin (Hugin, Munin, Gere, Freke), 12 heróis do Panteão e Matriz Completa de Autoquests (`autoquest todas`). |
| **Ciclo 9** | Dia 90+ | *Aguardando próxima auditoria* | Checagem programada para início do Ciclo 10. |

## Dia 91 — Família da fazenda e ameaça no milharal

Fonte: [dossiê primário](evidence/dia91.json).

| Personagem | Local observado | Confirmação / pendência |
| :--- | :--- | :--- |
| O fazendeiro | Entrada da Casa (`fazenda_entrada_casa`) | Perguntou sobre ajuda e pediu exterminar 10 invasores do milharal. Sem recompensa ou conclusão confirmada. |
| Mulher desesperada | Sala de Estar e Quarto | Encontrada chorando de medo; pode circular. Nenhuma fala ou aliança acrescentada. |
| Criança | Quarto | Encontrada gritando; resgate não confirmado. |
| Líder dos monstros | Região do Milharal Destruído | Pelagem azul e clava; avaliação de vida desfavorável. Não atribuir posição fixa nem abate. |

O Padeiro voltou a vender pão recheado por seis moedas; três compras foram confirmadas na continuação do Dia 91.

## Dia 94 — Armeiro e catalogação no Modo Expandir Horizontes

Fonte: [dossiê primário do Dia 94](evidence/dia94.json).

| Personagem / Comerciante | Local observado | Confirmação / interação |
| :--- | :--- | :--- |
| **O Armeiro** | Loja de Armaduras (`loja_armaduras`) | Comprou `os chifres do Minotauro` por **50 moedas** cada (3 vendidos = 150 moedas) e `a fedida pele do Minotauro` por **50 moedas** cada (2 vendidas = 100 moedas). |
| **Um velho porteiro** | A Entrada da Vila Residencial (`vila_residencial_entrada`) | Guarda o grande portão de ferro com emblema `"M"` na entrada murada da Vila Residencial. Nota técnica: a palavra-chave de alvo não é `velho` (`look velho` recusado); usar substantivo `porteiro`. |
| **Um apressado aventureiro** | Um Caminho Dentre os Campos (`caminho_campos_jareth`) | Transita pelo entroncamento dos campos em busca de desafios. Nota técnica: a palavra-chave de alvo não é `apressado` (`look apressado` recusado); usar substantivo `aventureiro`. |

## Dia 95 — Criaturas da Borda do Abismo nos Esgotos

Fonte: [dossiê primário do Dia 95](evidence/dia95.json).

| Criatura / Monstro | Local observado | Comportamento e Periculosidade |
| :--- | :--- | :--- |
| **Um ameaçador dragão vermelho** | A Borda Estreita (`borda_estreita_sul`) | **LETAL / CRÍTICO.** Dragão colossal cercado por aura multicolorida mística. Encarou a aventureira com fúria. Deve ser contornado a todo custo, sem qualquer engajamento direto. |
| **Cobras venenosas (múltiplas)** | A Estreita Borda Indo de Leste a Oeste (`estreita_borda_leste_oeste`) | **HOSTIS / VENENOSAS.** Grupo emboscador atacando em bando com mordidas lacerantes. Picada inocula peçonha grave (`poison`, -2 FOR, 9h de duração, -10 HP por pulso de dano). O protocolo Wimpy 30 disparou a fuga tática imediata salvando a vida da personagem. |

## Dia 96 — NPCs de Jareth, Rodovia e Novas Cotações de Comércio

Fonte: [dossiê primário do Dia 96](evidence/dia96.json).

### Figuras e Autoridades Encontradas

| Personagem | Local observado | Interação / Comportamento |
| :--- | :--- | :--- |
| **Novato Alquimista** | Sala do Alquimista (`sala_alquimista`) | Relatado o triunfo sobre a masmorra. Missão *Limpando Monstros* concluída com louvor (+75.482 EXP e manto de pano). |
| **Mago Aventureiro** | Bar dos Magos (`bar_magos`) | Etapa 1 de *Dicas Mágicas* concluída (+30.000 EXP recebidos). Etapa 2 ativada (solicitou pergaminho de retorno). |
| **O Pacificador** | Praça do Templo (`praca_templo`) | Despachou Grebolius para socorrer os colonos na fazenda a leste de Jareth (*Problemas Agrícolas*). |
| **Comerciante Sorridente** | A Estrada Midgaard-Jareth | Mercador itinerante exibindo produtos na margem da rodovia. |
| **Guardas Particulares** | Postos de Guarda da Estrada | Operadores de grandes cancelas nos trechos afunilados da rodovia entre Midgaard e Jareth. |
| **Membros da Guarda da Cidade** | Avenida Floris (Jareth) | Sentinelas urbanas fortemente armadas patrulhando a via principal da Cidade Livre. Diálogos observados: *"Paladinos seriam de grande ajuda por aqui..."* e *"Jareth precisa de alguém experiente para uma importante missão"*. |
| **Arius, o Abastecedor** | Loja de Provisões (Jareth) | Mercador de víveres e produtos gerais atendendo no balcão da loja. |
| **Dono do Estábulo** | Estábulos de Jareth | Cuidador encarregado de abrigar e alimentar montarias de viajantes. |
| **Proprietário do Clube Kitty-Kat** | Recepção do Clube Kitty-Kat (Jareth) | Homem careca administrando as reservas e contando as vendas diárias na mesa lustrosa. |
| **Garçonetes do Kitty-Kat** | O Clube Kitty-Kat (`jareth_clube_kitty_kat`) | Atendentes loira e morena servindo mesas, entregando cardápio e acolhendo aventureiros no salão refinado. |

### Novas Cotações de Venda Comprovadas (Midgaard)

| Mercador / Loja | Item Vendido | Cotação Paga | Custo-Benefício |
| :--- | :--- | :---: | :--- |
| **O Armeiro** | `a coroa da Rainha Branca` | **1.500 moedas de ouro** | **Extremo (Ouro puro)**. Peça leve de xadrez com retorno colossal. |
| **O Armeiro** | `a armadura do Peão Preto` | **150 moedas de ouro** | Muito bom para armadura de novato. |
| **O Armeiro** | `um escudo` | **200 moedas de ouro** | Excelente para proteção padrão. |
| **O Armeiro** | Peças de couro (`perneiras`, `jaqueta`, `botas`) | **37 a 75 moedas** | Regular. Bom para descarte de sucata leve. |
| **O Ferreiro** | `a espada do Peão Preto` | **40 moedas de ouro** | Bom rendimento para lâmina de mob. |
| **O Ferreiro** | `uma espada longa` militar | **240 moedas de ouro** | Excelente cotação de armamento marcial. |




## Capítulo 1 (Dias 101 a 111) — Vendas, quests e a armadura amaldiçoada

### Armeiro de Midgaard (Loja de Armaduras) — corrigido
- **Compra apenas armaduras**: "Eu compro apenas armaduras... Vá embora!" (recusa espadas e afins).
- Paga **8.500** pela **Armadura da Torre Negra** e **150** pela armadura de peão.
- **Tem caixa finito**: depois de pagar cerca de três armaduras (≈25.500), passa a responder "Isso é caro demais para mim - Tente um feiticeiro!". **É limite de dinheiro, não o item** — testado e confirmado no Dia 108 (comprou a armadura de peão normalmente).
- **`sell [#] <item>`** vende vários; **`value <item>`** cota antes.

### Feiticeiro (Loja de Magias) — corrigido
- **Não compra armaduras**: "Eu não compro esse tipo de coisa." Compra **bastões/cajados**.
- Vende pergaminhos: retorno (9.202), **remover maldições (8.509)**, identificação (4.601).
- **As paredes da loja bloqueiam magia**: recitar pergaminho lá dentro falha ("As paredes desta sala parecem impedir você"). Recitar **do lado de fora**.

### Mago Aventureiro e Mestre da Guilda dos Magos
- O **Mago Aventureiro** (Bar dos Magos) inicia/reinicia **Dicas Mágicas** com `say sim`; depois da entrega do pergaminho só dá falas de sabor.
- A **Mestre da Guilda** (Laboratório dos Magos) estuda um livro e não deu instrução. O laboratório tem **escada para baixo → esgotos**.

### Pacificador (Praça do Templo)
- Inicia/reinicia **Problemas Agrícolas**. Ele **fala sozinho quando o personagem permanece na sala**; responder `say sim` engata a missão.

---

## Dia 156 — NPCs confirmados pelo COMPORTAMENTO (levantamento das sessões)

Este bloco não é curadoria: sai da varredura de **26 sessões gravadas** (Dias 96–156, 31.874
comandos). O critério é comportamento observado, não suposição.

### Por que o critério é o comportamento, e não o `consider`

Tentei usar o `consider` para separar NPC de monstro e **não funciona** — ele mede força relativa:

```
consider zumbi     -> "É uma perda de tempo"    (monstro, fácil)
consider rato      -> "Você é LOUCO!"           (monstro, mortal)
consider ferreiro  -> "Você é LOUCO!"           (NPC, mortal)
```

A separação vem de **falar** (`diz`, `pergunta`, `responde`, `tagarela`) e de **vender**. O bestiário
e a tabela de sinais estão em **[monstros.md](monstros.md)**.

### Confirmados por fala

| NPC | Onde | Falas registradas |
|---|---|---|
| **Um Membro da Guarda da Cidade** | Midgaard (rondas) | 24 |
| **Um feiticeiro** | atrás do balcão da Loja de Magias | 23 |
| **Uma pequena criança** | Midgaard | 27 |
| **O Pacificador** | Praça do Templo | 7 |
| **Yurit** | — | 4 |

### Confirmados por chegada (andam pelo mundo)

**O zelador** (8×) e **O Pacificador** (3×) chegam andando e falam — NPC.
Os **monstros do milharal** também chegam andando, mas atacam — monstro. A distinção é o que fazem
ao chegar, não o fato de andarem.

### O cruzamento que valida o método

O levantamento confirmou pelo jogo NPCs que a curadoria já tinha escrito à mão — **com outro
vocabulário**, o que é a prova de que os dois olhares concordam:

| Sala | Curadoria (nome) | Confirmado pelo jogo (palavra-chave) |
|---|---|---|
| A Loja de Armas | Ferreiro | `ferreiro` |
| Rua Principal (Leste I) | Guarda Municipal | `prefeito` |
| Uma Casa Branca | Peões Caídos | `peao`, `peão` |
| A Loja de Animais | Vendedor | `lobo` ⚠️ o lobo está **dentro** da loja |

> ⚠️ **`A Loja de Animais` tem um lobo dentro.** O `consider` aceitou `lobo` naquela sala. Não
> confundir o lobo com o vendedor.

### Pendência que este levantamento NÃO resolve

O campo `npcs` das salas do levantamento mistura o que o `consider` aceitou — criatura — sem
distinguir NPC de monstro. Ele é **matéria-prima**, não veredito. Quem decide é o comportamento, e a
tabela de monstros é [monstros.md](monstros.md).

### Reforço sobre sala sem magia

O `conhecimento.md` §25.1 registra que **o Templo de Midgaard é área sem magia**. Este arquivo já
trazia o mesmo fenômeno noutro lugar, e vale repetir aqui: **as paredes da Loja de Magias também
bloqueiam conjuração** (*"As paredes desta sala parecem impedir você"*). Não é privilégio do Templo —
**conferir o local antes de conjurar**.

