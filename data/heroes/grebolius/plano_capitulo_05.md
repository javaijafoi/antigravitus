# Plano do Capítulo 05 — "Amanhã Eu Começo por Elas"

> **Título escolhido pelo autor.** É a última linha do fecho do Capítulo 04 — *"Amanhã eu começo por
> elas"* — e amarra os dois capítulos: o 04 descobriu as portas, o 05 as abre.

**Natureza do capítulo:** continuação do **desafio pessoal** de mapeamento. `kind`: **`marco`**.
Não é missão de ninguém; ninguém está esperando resposta.

**Goal:** abrir as **trinta portas nomeadas e nunca visitadas** do levantamento, começando pela
**Avenida Floris**, e catalogar cada lugar novo — o que vende, por quanto e quem atende. Sem travar
combate. `id` no `capitulos.json`: **5**.

---

## 1. O placar: as trinta portas

São destinos que o servidor **anuncia pelo nome** e que ela **nunca atravessou**. Cada um é uma porta
fechada com placa — o levantamento registrou o nome, não a sala.

### A Avenida Floris — 12 portas (a prioridade do capítulo)

Uma rua inteira que ela nunca andou. **Quase metade das portas do capítulo abre aqui**, e o padrão
dos nomes diz que é um distrito comercial:

| Porta | Sentido a partir da Avenida |
|---|---|
| A Delegacia | norte |
| A Loja de Arcos | norte |
| A Loja de Armas de Maris | norte |
| A Sapataria | norte |
| Estábulos | norte |
| O Banco de Jareth | norte |
| Uma Rua de Pedra Esburacada | norte |
| A Loja de Carriolas | sul |
| A Loja de Montarias | sul |
| A Loja de Provisões | sul |
| A Recepção do Clube Kitty-Kat | sul |
| A Via da Veneração | sul |

> **Repare no que essa lista é:** uma delegacia, um banco, estábulos, uma sapataria, uma loja de
> arcos, uma loja de armas, uma loja de carriolas, uma loja de montarias, uma loja de provisões, um
> clube e uma via de veneração. É outro centro urbano. **E "A Loja de Armas de Maris" implica uma
> Maris** — pode ser outra cidade, não um bairro de Midgaard.

### As outras 18

| Porta | Vista de | Sentido |
|---|---|---|
| A Construtora M&M | Uma Rua Larga | sul |
| A Rua das Glórias | Uma Rua Larga | oeste |
| Grottas - A Loja de Móveis | Uma Rua Larga | norte |
| A Rua do Rio | Uma Praça | norte e sul |
| Rua Bourbon | O Centro da Cidade de Jareth | norte e sul |
| O Caminho Para as Planícies Nobres | O Centro do Vilarejo | oeste |
| Um Casebre | Numa Pequena Vila | leste e oeste |
| A Entrada Para o Bosque Sombrio | O Pequeno Bosque | norte |
| As Planícies | O Pequeno Bosque | leste |
| Na Margem do Lago | Em Meio as Árvores | norte |
| Uma Densa Floresta | Em Meio as Árvores | oeste |
| Na Porta da Caverna | O Fim da Trilha | oeste |
| Caminhando no Fosso | Um Fosso Gramado | leste |
| O Labirinto | A Entrada do Labirinto | sul |
| Uma Curva no Cano de Esgoto | A Junção Regular | oeste |
| O Final Leste do Beco | O Beco Escuro | leste |
| O Bar dos Guerreiros | A Entrada da Guilda dos Guerreiros | leste |
| O Bar dos Paladinos | A Entrada da Guilda dos Paladinos | leste |

**Três exigem ressalva antes de tentar** — não são portas, são guardas:

- **O Bar dos Paladinos** e **O Bar dos Guerreiros**: o guarda da entrada já recusou passagem
  (*"O guarda te humilha e não deixa você passar."*). Só se entra sendo da guilda.
- **O Labirinto** e **O Final Leste do Beco**: labirinto tem teto de visitas por segurança
  (`MAX_VISITAS_LABIRINTO = 3`), e o Beco Escuro tem guarda no `e`.

---

## 2. O método

O que funcionou no Capítulo 04 e continua valendo:

1. **Rota pelo mapa, não de ouvido.** A origem é sempre a sala onde ela **está** — não onde se supõe.
   Aplicar rota de origem errada é o que faz um `d` responder *"Você não pode ir por aí..."*.
2. **Conferir a chegada por marco de sala**, nunca por contagem de passos.
3. **Desviar do perigo.** As 20 salas de `risk_code` alto (`RISCO_A_EVITAR`) ficam fora da rota. Se
   não houver caminho limpo, vai pela direta **e registra** que passou por perigo.
4. **`visible` antes de qualquer comércio.** Invisibilidade bloqueia troca: *"Não negocio com quem
   não vejo!"*.
5. **Não lutar.** Fugir é vitória. `wimpy` fica em **48**.
6. **Voltar ao Templo e salvar** ao fim de cada rodada.

**Ao entrar em cada lugar novo, anotar:** nome da sala, saídas, NPC que atende, o que a loja vende
(`list`) e o preço. Item novo entra na tabela de [itens.md](itens.md) com ID próprio.

---

## 3. Diretivas que continuam valendo

- **PROIBIDO vender armaduras** da Torre Negra ou de peão: *"perdemos mais dinheiro do que ganhamos"*.
- **Saque do prepara: 300** na mão (`config.SAQUE_PARA_COMPRAR`). O banco não é tocado além disso.
- **Teto de 10 conexões**, com 3 preferidas.
- **Nada de metajogo** nas descrições dos capítulos.
- **Coordenadas são só da superfície.** Para labirinto vale o `id`, com `lb###`.

---

## 4. Quando o capítulo fecha

Quando **as trinta portas tiverem sido abertas ou justificadas** — uma porta guardada, um labirinto no
teto de visitas ou uma região de risco fatal não é falha do capítulo, é resposta. O que não se admite
é porta fechada por não ter ido.

**E o que o capítulo deixa:** um mapa do mundo além de Midgaard, com o comércio de lá catalogado.

---

## 5. Riscos conhecidos

| Risco | Estado |
|---|---|
| **Avenida Floris pode ser cidade hostil** | desconhecido — o distrito nunca foi visitado. Ir com vida e mana cheias e rota de volta conhecida. |
| **O Banco de Jareth** | pode render acesso a mais um banco; útil, mas exige ouro para testar. |
| **Na Porta da Caverna / Uma Densa Floresta** | podem ser zona de caça; não é para lutar. |
| **Guildas (Paladinos, Guerreiros)** | barradas por guarda. Registrar como resposta, não insistir. |
