# Notas Editoriais — Grebolius

Documento de leitura, separado das crônicas. Aqui fica o que é decisão do autor e o que é fato do servidor, para que nada se misture.

## Dia 100 — Âncora de origem (estabelecida pelo autor, sem evidência de servidor)

- **Fato do servidor (Dia 100):** Grebolius morreu pela quarta vez, no Milharal Destruído, atacada por um monstro agressivo. Foi conduzida ao Paraíso, ao Portal Escondido e ao Caminho no Vazio, e renasceu ao beber da Fonte da Vida. Está registrado em `evidence/dia100.json`.
- **Âncora do autor (sem evidência de servidor):** a **primeira morte, no Dia 0**, é a raiz acrescentada pelo autor. O Dia 1 já é cânon publicado e abre com ela se crendo goblin; a proposta é que essa crença foi uma **dedução errada a partir dos cacos de memória** deixados pelo Vazio, e não uma mentira. A origem real é **elfa** (o `state.json` sempre separou `mechanical_race: Elfo` de `appearance: Mulher goblin`).
- **Segunda leitura (não reescrita):** as crônicas dos Dias 1 a 99 permanecem exatamente como foram publicadas. A partir do Dia 100 elas ganham uma segunda leitura: o nome, o disfarce de homem, a raiva nos becos e a rejeição passam a ser vistos como tentativas de dar sentido a uma memória rasgada. Nada foi reescrito, nada foi apagado.
- **Pendências abertas:** reconciliar a `identidade.md` e o item 8 da doutrina com essa leitura; verificar em jogo, quando o servidor entregar o gatilho (um NPC que diga o nome, uma magia de detecção, o olhar do Cavaleiro Branco), e só então afirmar a revelação como acontecimento. Até aí, ela é leitura editorial.

## Ganchos em aberto (para o jogo entregar, não para o autor decidir)

1. O nome **Grebolius**, de sonoridade élfica, nunca explicado.
2. O **colar com uma pedra púrpura**, que o jogo insiste que ela não é dona e não pode usar.
3. O **Cavaleiro Branco**, que a matou no Dia 60 — o que ele viu nela?
4. A distinção `mechanical_race` × `appearance` que o próprio `state.json` carrega.
5. O Dia 100 como marco decenal: a doutrina (item 6) pede quebra de limites conhecidos.

## 17 — Camada de ficção sobre morte e memória (movida da diretiva em 2026-10-21)

> **"estou dando uma camada só de ficção porque na verdade morrer quando tá level baixo 'tirou o passado
> dela', mas agora a gente vai morrer a beça e queria tirar esse peso, e como ela tem muito mais xp,
> agora ela perde algo novo e não algo velho. são adaptações do metajogo"**

**Isto é ADAPTAÇÃO DELIBERADA do metajogo, não fato do servidor.** Serve para tirar o peso narrativo de
um capítulo em que ela **vai morrer muito** — e para que a morte deixe de ser derrota na crônica.

| Mecânica real | Camada de ficção |
|---|---|
| Morrer custa experiência | *"A morte tira o passado dela."* |
| Em nível baixo a XP era escassa — a perda doía proporcionalmente muito | *"Morrer cedo tirou o passado dela"* — perdia-se história acumulada |
| Com muito mais XP acumulada, a mesma perda vira fração pequena | *"Agora ela perde algo novo, e não algo velho."* |
| O aprendizado recente é o que ainda não se consolidou | *"A memória tem ficado mais clara: ela só perde o que aprendeu recentemente, como se não dormisse depois de um aprendizado."* |
| **Não há imunidade a morte no servidor.** O que existe é o **brinco com flag ANTI-DT**, que protege de **armadilha mortal** e **nunca foi testado** | *"O poder que ela tem a protege, pelo menos por enquanto, das mortes."* |

### Como escrever

- **Pode** narrar como **percepção dela**, em primeira pessoa, sem hedge — é a voz do diário.
- **Não** afirmar **imunidade a morte como fato**: o texto mantém o *"por enquanto"* / *"parece"*. A
  promessa de imunidade seria mentira mecânica.
- **Não** usar **número cru** de XP/HP/mana na crônica. **O validador é estreito, então não confie nele
  como rede:** o `META` de `scripts/check_project.py` pega `<número> XP|EXP|HP|MP|MV|%`,
  `mana|armadura|dano|experiência: <número>` e `pontos de mana|couraça|experiência` — mas **deixa passar**
  *"ganhei 67068 de experiencia"* (o número não está colado na unidade). **A regra é a intenção, não o
  regex:** *"subi um grau"* é a forma certa; *"oito mil de experiência"* não é, ainda que escape.
- **Morrer no Capítulo 06 é custo previsto, não falha** — a crônica não trata morte como derrota.

**Registro completo, com os cinco mapeamentos:** `capitulos.json` → capítulo 6 → `directive.fiction_layer`.
