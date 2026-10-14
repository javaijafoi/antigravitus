---
name: mud-ciclo-diario
description: Protocolo completo de jogabilidade e encerramento para cada dia no Devil's Bob MUD. Define ritmo narrativo rico (dias longos), 3 ações diárias obrigatórias, combate/treino frequente, reflexão decenal, ausência total de metajogo, ficha viva sincronizada, doutrina de aço e magia, e deploy contínuo em produção.
---

# ⚔️ Skill: Modus Operandi Completo do Devil's Bob MUD

Esta skill formaliza todas as regras de jogo, liturgia de encerramento e diretrizes operacionais para qualquer agente que continue a campanha no Devil's Bob MUD (`debomud.org:4000`), inclusive em outros computadores.

---

## 🗡️ 1. Doutrina do Personagem (Grebolius — Ladra Arcana)
* **Aço e Magia Inseparáveis:** Estudar magia com voracidade para obter vantagens à distância e emboscadas, mas **NUNCA largar a adaga**. O punhal na cintura e as lâminas secundárias continuam sendo a extensão primordial de seu instinto de sobrevivência.
* **Aproveitamento Total de Recursos:** Se a guilda dos ladrões fechou as portas e os guardas a humilham, ela **não lamenta**: ela usurpa e domina todo e qualquer poder que conseguir (guilda dos magos, venenos, artefatos e magia proibida) para se fortalecer e esmagar quem a desprezou.
* **Disfarce Ativo:** Manter a postura dura de guerreiro novato para proteger sua identidade de mulher goblin até que seu poder militar seja incontestável.

---

## 🏹 2. Diretrizes Narrativas e de Jogabilidade
1. **Extensão e Profundidade (Dias 5x mais longos):**
   * As crônicas devem ser densas, detalhadas, exploratórias e imersivas (cerca de 5 vezes maiores que relatos básicos).
2. **Três Ações Importantes por Dia (Obrigatório):**
   * Cada dia jogado DEVE conter pelo menos **3 ações de peso**:
     - Lutar ou treinar (obrigatório pelo menos uma destas duas por dia);
     - Descobrir algo novo (salas desconhecidas, passagens secretas, rotas);
     - Conhecer alguém ou obter diálogos (NPCs, mestres, mercadores, lendas);
     - Conseguir ou fabricar novos itens (equipamentos, provisões, armas, chaves);
     - Surrupiar ou pilhar recursos.
3. **Frequência de Combate e Treino:**
   * **NUNCA passar mais de 3 dias sem lutar.**
   * **NUNCA passar mais de 1 dia sem treinar** (visitar guildas/mestres, usar `practice`, refinar feitiços ou movimentos).
   * Aprender sempre algo novo no mundo a cada ciclo.
4. **Gestão de Estamina (Limiar do Movimento):**
   * O dia de exploração deve ir até quase o esgotamento total dos pontos de movimento (`MV`), deixando apenas a margem estritamente suficiente para retornar a um santuário seguro.
5. **Zero Metajogo (Imersão Total):**
   * **NUNCA** mencionar nomes de arquivos técnicos como `mapa.md`, `posts.json`, `evolucao.md`, `ficha.md`.
   * **NUNCA** citar termos de sistema como "Level 30", "XP", "Hitpoints", "DikuMUD" ou atributos numéricos nos relatos em prosa.
   * Substitutos literários:
     - "Level 30" -> *o ápice da força dos mortais*, *o domínio supremo dos mestres*, *o limiar da soberania*.
     - "Level / Nível" -> *círculo de poder*, *grau de maestria*, *posto entre os grandes*.
     - "XP" -> *maturidade em batalha*, *experiência de sangue*, *vigor acumulado*.
     - "HP" -> *vitalidade*, *integridade física*, *fôlego vital*.

---

## 📜 3. Gestão da Ficha Viva da Personagem
* Em `data/heroes/<slug>/ficha.md` e na aba `/ficha.html` do site:
  - Manter sempre a **ficha viva** da personagem refletindo o estado real do MUD (HP, Mana, MV, Atributos, Perícias conhecidas, Sessões de treino pendentes, Equipamentos em uso e Inventário).
  - **Sem histórico de versões passadas**: o arquivo reflete unicamente o estado presente e vivo do herói.

---

## ⏳ 4. Ciclo Decenal (A cada 10 dias)
* A cada 10 dias de jornada (Dias 10, 20, 30...):
  1. O herói faz uma **pausa reflexiva profunda** em seu diário, avaliando friamente se sua rota e escolhas estão acelerando sua chegada ao topo.
  2. Modificar de forma **sutil** o arquivo `data/heroes/<slug>/identidade.md`, incorporando as fissuras, aprendizados e novas táticas consolidadas.
  3. Aplicar as novas táticas imediatamente no ciclo decenal seguinte.

---

## 📌 5. Liturgia Obrigatória de Encerramento Diário
NENHUM dia jogado é encerrado sem cumprir esta sequência de 5 passos:

1. **Salvar no Jogo:** Executar o comando `save` no MUD.
2. **Repousar com Segurança:** Retornar a um santuário protegido (Templo de Midgaard ou Panteão dos Centenários) e emitir `sleep`.
3. **Atualizar Registros do Herói:**
   - Adicionar o novo dia em `data/heroes/<slug>/posts.json` (mantendo a ordem estritamente crescente).
   - Atualizar `data/heroes/<slug>/mapa.md` com novos cômodos e conexões.
   - Atualizar `data/heroes/<slug>/evolucao.md` com as mutações de comportamento e combates.
   - Atualizar `data/heroes/<slug>/conhecimento.md` com criaturas, perigos e rotas decifradas.
   - Atualizar `data/heroes/<slug>/ficha.md` com os status vitais e inventário atuais.
4. **Atualizar Feed Geral e Index:**
   - Manter `data/posts.json` ou feed integrado sincronizado.
5. **Subir em Produção Imediatamente (Git & Vercel):**
   - Executar commit e push para `origin main`:
     ```powershell
     git add .
     git commit -m "cronica: Dia X - <Titulo> (<Heroi>)"
     git push origin main
     ```
   - Respeitar estritamente o isolamento de credenciais locais (nunca alterar configs globais de git).

---

## 🛡️ 6. Heurística Avançada de Combate, Carga e Sobrevivência (CircleMUD / DeBo)
Para destravar o avanço de nível sem loop de morte:

1. **Configuração de Fuga de Emergência (Wimpy 10):**
   - Com Constituição 9 e Vida 23, qualquer crítico de mob nível 2 tira 8 a 10 de vida. Rodar `wimpy 10` imediatamente para forçar fuga antes de sofrer hit kill.
2. **Gerenciamento de Carga com Força 10 (Descarte de Peso Morto):**
   - Com STR 10, carregar itens pesados (como picareta +10L, espadas militares pesadas, lâminas improvisadas e gorros reservas) drena os 84 MV velozmente e trava a esquiva.
   - Vender sucata nos comerciantes certos de Midgaard:
     * Loja de Armas / Ferreiro (Rua Leste II): espada longa, lâmina improvisada, adaga extra, picareta.
     * Loja de Armaduras (Rua Oeste): gorro de couro reserva.
     * Loja de Magias (Término da Rua Oeste): bastões e itens arcanos excedentes.
   - Usar sacolas/mochilas (`backpack`, `bag`) para driblar o limite de itens soltos nas mãos.
3. **Otimização de Equipamento em Uso:**
   - Conferir sempre itens melhores na mochila: remover gorro comum (`remove gorro`) e vestir o elmo encantado de novato (`wear elmo`) para maximizar Classe de Armadura e auras místicas.
4. **Avaliação Obrigatória com `con <alvo>`:**
   - **NUNCA** executar `kill` ou lançar feitiço ofensivo sem antes rodar `con <alvo>`.
   - Ler rigorosamente o quadro comparativo:
     * Se a Vida do oponente for *"Você é louco?"* ou *"Precisaria de muita sorte"*: **Fugir / ignorar imediatamente (ex: bebê dragão)**.
     * Se Poder for *"perda de tempo"* e Precisão for *"Fácil!"*: **Atacar**.
5. **O Combo de 'Ladra Arcana' (Abertura Mágica + Finalização no Aço):**
   - Abrir o combate à distância com `cast 'magic missile' <alvo>` (10 de dano instantâneo com 95%+ de acerto).
   - Deixar o punhal novato empunhado e o escudo apararem o contra-ataque e finalizarem a presa no combate corpo a corpo para economizar mana.
6. **Regra dos 50% de Mana / 15 HP:**
   - Se a Mana cair abaixo de 50 MP ou o HP abaixo de 15 HP, interromper a caça imediatamente, retornar ao Santuário (Panteão ou Templo) e usar `sleep` até recuperação completa (23/23 HP e 100/100 MP).
7. **Varredura e Portas de Fuga Abertas:**
   - Checar saídas e salas adjacentes com `look <direcao>` antes de entrar.
   - Manter portas destrancadas e abertas nas costas para que o comando `flee` não falhe em pânico.
8. **Auto-Saque e Sacrifício aos Deuses:**
   - Ativar `autogold` e `autoloot` (ou conferir em `config`).
   - Após saquear (`get all corpo`), usar `sac corpo` para oferecer o cadáver aos deuses em troca de moedas de ouro ou bônus de XP.
9. **Monitoramento de Luz, Hidratação e Suprimentos:**
   - Vigiar alertas da tocha para não lutar cego no escuro (inviabiliza conjuração).
   - Beber nos cantis assim que a sede surgir.
   - Passar na Sala de Doações do Templo para checar itens e pergaminhos gratuitos deixados por veteranos antes de comprar.
10. **O Pavor e Ódio da Morte:**
    - Grebolius sentiu o Vazio entre os mundos e a perda de fragmentos de memória. A morte é uma mutilação existencial e um horror absoluto que ela jamais aceitará reviver.


