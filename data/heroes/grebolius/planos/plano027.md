# Plano 027 — Capítulo 12 (Tomo II): Expedição a Notre Dame ou Xeque-mate no Rei Negro

| | |
|---|---|
| **Criado em** | 2026-10-18 · Dia 156 |
| **Por** | Gemini 3.8 Flash (Medium) |
| **Herói** | grebolius |
| **Objetivo** | Capítulo 12 (Tomo II — As Chaves do Tabuleiro) — Preparar e conduzir expedição de batedor (com invisibilidade e armadura) rumo a Notre Dame/França para localizar Lemin e iniciar Ajuda Mágica (ou reiniciar Xeque-mate no Tabuleiro de Xadrez com abordagem tática à distância contra o Rei Negro) |
| **Sessão encerrada?** | sim — personagem em total segurança no Templo de Midgaard; HP 199/199, Mana 430/430, MV 145/145, CA 89, wimpy 45, Alinhamento 412 (Bom), Nível 32 consolidado (7.225.102 EXP), 16.059 moedas de ouro (15.700 no banco, 359 na mão), 6 pães recheados e cantil saciado de água fresca na mochila de Pellinore; save, sono e _CLOSE confirmados; live_daemon finalizado |

---

## 1. Onde o objetivo está

O **Plano 026 foi integralmente cumprido com êxito**:
1. **Comércio Mercantil de Alto Valor Concluído:**
   - A `Coroa da Rainha Negra` (ANTI-GOOD, valor 3.000 moedas) foi retirada da mochila, cotada no Armeiro de Midgaard (`value coroa` -> 1.500 moedas) e vendida com sucesso (`sell coroa`).
   - 4 kg de peso morto foram aliviados e o perigo de choque elétrico/zap por restrição moral foi 100% eliminado sem nunca vestir o item.
2. **Saúde Financeira e Bancária Consolidada:**
   - Depósito de 1.700 moedas no Banco do Templo, elevando a reserva bancária para **15.700 moedas** e o patrimônio total para **16.059 moedas** (mantendo 359 moedas na mão, respeitando com precisão a margem operacional de `RESERVA_OURO = 300`).
3. **Reconstituição de Estoque de Suprimentos:**
   - Cantil 100% abastecido com água cristalina na grande fonte de mármore azul da Praça do Templo.
   - Compra de 5 pães recheados na Padaria de Midgaard por 30 moedas, elevando o estoque para **6 pães recheados** na mochila de Pellinore (cumprindo com folga a regra `LIMIAR_PAO = 2`).
4. **Descoberta Documental Crítica sobre `Ajuda Mágica`:**
   - Auditoria in-game através de `help autoquest` e `help notre dame` comprovou que o patrono `Lemin` **NÃO está em Midgaard**: pertence à zona de **Notre Dame/França** (`44) Ajuda Mágica: Lemin (Notre Dame)`).
   - Rota terrestre completa até a França extraída e documentada em `conhecimento.md` §60.

Para o **Capítulo 12**, as duas opções de avanço tático estruturadas são:
- **Opção A (Ajuda Mágica):** Despachar expedição de batedor com salvaguardas arcanas (invisibilidade e armadura) rumo a oeste para desbravar o caminho até Notre Dame e localizar Lemin.
- **Opção B (Xeque-mate):** Retornar a F1 no Tabuleiro de Xadrez, reativar a cadeia no Bispo Branco e aplicar estratégia de combate à distância com raios (`lightning bolt`) sem engajamento corpo a corpo contra o Rei Negro.

---

## 2. Estado exato

- **Nível:** 32 (Mago Elfo, 1ª encarnação).
- **EXP:** 7.225.102 (próximo nível: 8.000.000 — faltam 774.898 EXP para o Nível 33).
- **Vitals:** HP 199/199, Mana 430/430, MV 145/145.
- **Wimpy:** 45 (estritamente calibrado).
- **Alinhamento:** 412 (Bom — `{<<<<<>>---} Você é bom`).
- **Armadura:** CA 89 (base equipado).
- **Ouro:** 16.059 moedas de ouro (15.700 depositadas no Banco do Templo, 359 na mão).
- **Local:** O Templo de Midgaard (dormindo com save confirmado).
- **Suprimentos:** Cantil saciado com água cristalina, 6 pães recheados na mochila de Pellinore.
- **Equipamentos vestidos:**
  - na cabeça: `a Coroa da Rainha Branca`
  - na orelha direita: `um diminuto brinco de novato`
  - no pescoço (1): `a coleira do dragão de estimação`
  - no pescoço (2): `um colar com uma pedra púrpura` (Anti-DT, Abençoado, CA +10, Acerto +1, Dano +1, Des +1, Mana +25)
  - sobre o corpo: `um manto de pano`
  - nos braços: `um par de braçadeiras de novato`
  - nas mãos: `um par de luvas de couro`
  - no pulso esquerdo: `um rosário`
  - no pulso direito: `um bracelete de prata e ouro`
  - como escudo: `um escudo`
  - na cintura: `um belo cinturão de rodeio`
  - nas pernas: `uma calça de couro`
  - empunhando: `uma espada curta`
- **Inventário registrado:**
  - Na mão: `um rosário` (sobressalente), `um cantil` (cheio), `a mochila de Pellinore`, `um pergaminho de sabedoria`.
  - Na mochila de Pellinore:
    - 6 `pão recheado`
    - `um manto de pano`
    - `um colar com uma pedra púrpura` (sobressalente)
    - `a bainha de Excalibur`
    - `uma Cruz Ansada`
    - `o Cetro do Bispo Negro`

---

## 3. O que já foi descoberto

### Geografia de Notre Dame e Autoquests
- `help autoquest`: Lista as 51 missões do servidor com patronos e áreas. A missão #44 é `Ajuda Mágica: Lemin (Notre Dame)`.
- `help notre dame`: Rota terrestre oficial a partir do Templo de Midgaard:
  `s` -> Praça do Templo -> `s` -> Praça do Comércio -> `w` pela Rua Principal até `Trilha em Meio a Floresta` -> `Caminho Sombreado Através da Floresta` -> primeira passagem a oeste (`w`) -> `Bifurcação no Caminho` (`n`, depois `w`) -> `n` pelo Caminho Sombreado até `Densa Floresta Entre as Colinas` -> estrada a leste (`e`) até a `Entrada Para a França`.

### Economia Mercantil
- O Armeiro de Midgaard avalia e compra coroas e elmos mágicos por 50% do valor de face (`value coroa` pagou 1.500 moedas pela Coroa da Rainha Negra).

### Cancelamento de Autoquests
- Morte em combate e desconexão via `quit` cancelam autoquests ativas. `save` e `sleep` preservam a sessão íntegra.

---

## 4. Os bloqueios, e o que já foi tentado

- **Acesso a Notre Dame:** A rota passa por áreas de floresta e colinas fora de Midgaard ainda não registradas no `mapa.json`. Deve ser explorada exclusivamente em Modo Batedor com magias de proteção ativas.
- **Rei Negro (E8):** Desfere 60 a 75 de dano por golpe corpo a corpo. Exige combate à distância com raios (`lightning bolt`) e retirada rápida caso engajado.

---

## 5. O próximo passo, e só ele

1. Acordar (`wake; stand`).
2. Sair da área sem magia do Templo até a Praça do Templo (`s`).
3. Conjurar proteções arcanas: `cast 'armor'` e `cast 'invisibility'`.
4. Decidir entre:
   - **Opção A:** Iniciar reconhecimento em Modo Batedor rumo a oeste pela rota de Notre Dame (`w` pela Rua Principal), mapeando as salas com segurança até encontrar Lemin.
   - **Opção B:** Deslocar-se ao Tabuleiro de Xadrez (`n, n, n, n, w, w, w, w`), falar com o Bispo Branco em F1 para reatar a cadeia de Xeque-mate e avançar com kiting arcano.

---

## 6. NÃO REPITA

1. **NÃO procure Lemin dentro da cidade de Midgaard — comprovado via `help autoquest` que ele está em Notre Dame.**
2. **NÃO entre em áreas florestais ou desconhecidas sem invisibilidade e armadura ativas.**
3. **NÃO tente lutar no corpo a corpo contra o Rei Negro.**
4. **NÃO entregue itens sem confirmação formal da etapa em `score tudo` (Invariante 13).**
5. **NÃO automatize diálogos verbais com NPCs (Invariante 14).**
6. **NÃO ataque inocentes ou animais pacíficos (Invariante 15).**
7. **NÃO dê `quit` com autoquest em andamento (Invariante 8).**

---

## 7. Ferramentas e comandos

- **Navegação e Reconhecimento:** `look`, `exits`, `where`, `flee`, `recall`.
- **Magias:** `cast 'armor'`, `cast 'invisibility'`, `cast 'lightning bolt'`, `cast 'sleep'`, `cast 'blindness'`.
- **Auditoria de Missão:** `score tudo`, `autoquest listar`.

---

## 8. Devolutiva técnica

| Descobri | Registrei em | O quê |
|---|---|---|
| mapa | `mapa.json` | PENDENTE (salas da rota Midgaard-França entrarão na expedição do Modo Batedor) |
| referência do servidor | `maquina/verificacoes.md` | Lista canônica de 51 autoquests via help autoquest, rota help notre dame e cotação comercial de 1.500 moedas |
| fato do mundo | `conhecimento.md` §60 | Desmistificação de Ajuda Mágica em Notre Dame, itinerário terrestre e venda da Coroa da Rainha Negra |
| erro do motor | `automato/CHANGELOG.md` | v1.6.16 documentando execução do Plano 026, reposição de estoque de suprimentos e suporte sem-git em devolutiva.py |

---

## 9. Como encerrar a sua sessão

1. Retornar ao Templo de Midgaard (`recall`).
2. Sancionar alimentação e água.
3. Executar `save` e `sleep`.
4. Gravar evidência com `agent` e registrar derivados via `sync_hero.py`.
5. Criar o Plano 028 e rodar `python scripts/devolutiva.py --sem-git` (0 falhas).
