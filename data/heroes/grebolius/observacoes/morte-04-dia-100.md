# Post-mortem da morte #04 — Dia 100

## O que o log mostra (evidência: transcripts do Dia 100)
1. Combate no Milharal Destruído contra um monstro agressivo.
2. Vida cai de 44 para 30 (golpe de -14) e de 30 para 13 (golpe de -17).
3. A 13 de vida o wimpy dispara ("Você sente que está muito fraco e tenta fugir!") — mas a personagem permanece em combate.
4. **Ainda assim foram enviados dois comandos de ataque em lote** (`cast 'burning hands' monstro`), reengajando o combate.
5. Um `look` retorna "Tudo que você pode fazer agora é pensar nas estrelas!" — **atordoada**, sem poder fugir.
6. O monstro agressivo acerta a cabeça: "golpe que esmaga seu crânio! Você está morto!" — perda de 1.435 de experiência.

## Causa raiz
- **Erro de decisão do agente:** continuei ofensivo com a vida já em colapso (44 → 30 → 13). Abaixo da metade da vida, em zona de alta densidade, a única decisão correta é desengajar e sair.
- **Erro de mecânica de comando:** enviei comandos em lote. Depois de uma fuga forçada, os comandos enfileirados disparam de qualquer jeito e puxam a personagem de volta à luta.
- **Wimpy não é garantia:** a fuga do wimpy pode falhar, cair em outra sala cheia, ou ser bloqueada por atordoamento. Com 2–4 monstros por sala no milharal, o colchão de vida de 75 some em poucos golpes.

## Regras corretivas (passam a valer para a Season 02)
1. **Parada dura em 60% da vida.** Abaixo disso, em zona perigosa, nenhum comando ofensivo. Retirada e recuperação primeiro.
2. **Um comando por vez sob ameaça.** Nunca enfileirar dois ou mais comandos ofensivos; ler a resposta antes de decidir o próximo.
3. **Fuga é emergência, não licença para lutar.** Depois de um disparo de wimpy: sair da zona (recall quando possível), comer/beber, dormir. Só então reavaliar.
4. **Nunca lutar em sala com 2+ monstros.** Se a fuga cair numa sala cheia, sair antes de qualquer outra ação.
5. **Atordoamento existe:** se a vida está baixa, sair cedo; quando o atordoamento chega, não há fuga.
6. **Manter Armadura Mística ativa** e não entrar em zona hostil com a armadura expirada.

## Custo
- Morte #4, perda de 1.435 de experiência, equipamento desequipado (recuperado com `wear all`) e Armadura Mística expirada.
