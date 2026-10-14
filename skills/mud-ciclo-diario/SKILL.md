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
