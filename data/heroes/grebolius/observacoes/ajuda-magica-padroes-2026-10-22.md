# Ajuda Mágica: o passado, os padrões e o que testar (2026-10-22)

Agente: Claude Sonnet 5.5 (claude-sonnet-5-5). Pedido do autor: "vamos tentar descobrir como terminar a missão que temos; olha o passado, olha os padrões". Leitura de `conhecimento.md` §56 a §82 e §88/§89, `missoes.json`, planos 041 a 046 e evidências `dia157-*`, `dia158-campanario`. Nenhuma conexão ao jogo.

## 1. O que a missão pede
- Patrono: **Lemin**, no Centro da Cidade de Lyon (região de Notre Dame). Nível 30 a 45, só magos. A cadeia leva ~6 minutos à mão: `say sim`, esperar a pergunta, `say Merlin`, `say sim`, `say sim`.
- Pedido literal: **"Primeiro, preciso de um tomo de pergaminho bem grosso. Pode ser usado mesmo."** O "Primeiro" indica mais materiais depois. Lemin repete o pedido a cada ~30 s.
- Recusados com a mesma frase ("não é o item correto ou você não é o dono original"): tomo da sabedoria druídica (SPELLBOOK REMORT, NÃO-DOAR, nível 37, vindo da Sala de Doações), pergaminho de sabedoria ("A Lenda de Nambor"), rolo de pergaminho (nota), livro de Jooh.
- A missão caiu 3 vezes (reconexão do driver e `_CLOSE`), sempre depois de ativada.

## 2. Padrões que se repetem nas quests concluídas
1. **Só o item exato passa, e vem da fonte do roteiro.** Gargamel: poção aquosa da loja de Clariss. Dicas Mágicas: pergaminho de retorno da Loja de Magias de Midgaard (comprado no Dia 28 e aceito no Dia 83, então o item pode ser anterior à etapa). Xeque-mate: o Cetro do Rei Negro passou; o Cetro do Bispo, da loja, foi recusado com a MESMA frase. Essa frase é o teste "item certo", não prova de que falta a fonte.
2. **Item de quest pode ser invisível.** Passamos 3 dias achando que o cetro e a chave não existiam; estavam no chão, invisíveis (§88). Toda a busca do tomo (Dias 157 e 158) é anterior a essa descoberta. Não há registro de varredura com `detect invisibility` e `detect magic` em Lyon, Notre Dame e Paris.
3. **Porta trancada ou saída oculta pede chave do roteiro** (a Tesouraria pediu a chave do Rei). Portas fechadas na região do Lemin: QG dos Mosqueteiros em Paris (porta norte, guarda dormindo).
4. **NPC de quest fala sozinho quando a personagem chega** (Lemin, Alquimista, Bispo Branco, Mago Aventureiro). NPCs calados e protegidos por luz (corcunda, comerciante francês da cabana de Lyon, padre Tintoreto) são candidatos a gancho, não confirmados. O servidor diz haver 5 autoquests secretas.
5. **O patrono e os itens ficam na mesma região** (Gargamel em Midgaard e Jareth; Dicas Mágicas em Midgaard). Lemin é da França: Lyon, Notre Dame, Paris, labirinto de Champs Élysées.
6. **A missão ativa cai por reconexão.** A busca deve ser feita SEM a missão ativa; abrir a cadeia só com o item na mão.

## 3. O que já foi descartado
Pierre e Toulouse (Lyon, de dia, sem tomo), Campanário e segundo andar de Notre Dame, Sala de Doações, lojas e biblioteca de Jareth, Armazém de Midgaard, mural da Praça do Comércio, Sala de Leitura e Laboratório dos Magos (sem material acessível), pergaminhos de identificação (dissolvem ao `recite`).

## 4. Ordem de testes, do mais barato ao mais caro
1. **`where tomo`, `where livro`, `where pergaminho`** (nunca testado; `where <NPC>` funciona). Custo zero.
2. **`cast 'locate object' tomo`** (e `livro`, `pergaminho`). A magia foi aprendida no nível 34 e só o texto do `help` fala em espelho localizador; ninguém tentou conjurar depois do 34. Anotar a resposta exata. Itens ANTI-LOCATE não aparecem.
3. **Varredura com `detect invisibility` e `detect magic`** (sem missão ativa) em: Centro de Lyon e Rua Principal, Notre Dame (átrio, naves, capela, campanário, segundo andar), Paris (praças, entrada do QG), cabana do comerciante. `look` de cada sala e de cada NPC.
4. **QG dos Mosqueteiros:** `look`, `exits`, `open norte`; descobrir quem carrega a chave (`consider` e `look` dos mobs de Paris com detect ligado). O mosqueteiro é guarda: não atacar (moral, diretiva §27).
5. **NPCs calados:** Degas (eremita do labirinto de Champs Élysées), comerciante francês, padre Tintoreto, recepcionista do hotel. Falar à mão, uma vez cada, depois de `autoquest listar` (cuidado: só há uma autoquest ativa por vez).
6. **Silverthorne (Loja do Escriba, Albernathy)** e **Torre da Magia** (`help mapa 29`, a leste de Jareth, nunca tentada). Rota até Silverthorne desconhecida; o livro 2533 da Torre é cenário no mundo-base. Prior baixo.

## 5. Dúvida aberta
"Pode ser usado mesmo" pode significar que um item em estado gasto, "(muito gasto)", serve. Nenhuma observação confirma isso.
