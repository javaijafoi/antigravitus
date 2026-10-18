# Plano 019 — Capítulo 10: Dez Cabeças Inéditas e Caçadas Criativas

| | |
|---|---|
| **Criado em** | 2026-10-18 · Dia 156 |
| **Por** | Gemini 3.8 Flash (High) |
| **Herói** | grebolius |
| **Objetivo** | Capítulo 10 ("Dez Cabeças Inéditas") — Abater 10 criaturas ou monstros que Grebolius ainda não matou no MUD, executando planos criativos e arrojados de reconhecimento, armadilha e caça |
| **Sessão encerrada?** | sim — personagem em total segurança no Templo de Midgaard; HP 196/196, Mana 420/420, MV 144/144, CA 148, wimpy 45, Nível 31 consolidado, save e sono confirmados; live_daemon finalizado |

---

## 1. Onde o objetivo está

O **Capítulo 09 ("O Preço Não Se Mata com Raio") foi CONCLUÍDO com êxito absoluto**:
1. A autoquest **`Uma Lição em Gargamel` foi 100% finalizada**: poção aquosa comprada em Clariss (9.750 moedas), entregue ao Alquimista recebendo o jarro brilhante, jarro entregue ao Smurf Minerador.
2. Infiltração em *O Covil de Gargamel*: `cast 'sleep' gargamel` (95%) neutralizou Gargamel imediatamente (+1.200 EXP) e um único `cast 'lightning bolt' gargamel` eliminou o vilão (+1.080 EXP), saqueando 2.000 moedas e a `chave quadrada`.
3. Chave entregue ao minerador; tocha comprada no Armazém de Midgaard (15 moedas) e entregue ao minerador.
4. O Smurf Minerador premiou Grebolius com **`um colar com uma pedra púrpura`** (Anti-DT, Abençoado, Armadura +10, Acerto +1, Dano +1, Destreza +1, Máx-Mana +25), equipado com sucesso no segundo slot de pescoço.

O autor Peter definiu a nova diretriz para a próxima sessão:
> *"a missão de amanhã vai ser diferente a missão a próxima missão vai ser matar 10 bichos que ela ainda não matou mesmo que ela tenha que fazer planos malucos e ser muito criativa"*

O **Capítulo 10 ("Dez Cabeças Inéditas")** está formalmente aberto em `capitulos.json`. A meta é identificar, rastrear e abater 10 criaturas ou monstros que jamais constaram como abatidos no bestiário de Grebolius (`data/heroes/grebolius/monstros.md`).

---

## 2. Estado exato

- **Nível:** 31 (Mago Elfo, 1ª encarnação).
- **EXP:** 6.840.487 (próximo nível: 7.000.000 — faltam apenas 159.513 EXP para Nível 32!).
- **Vitals:** HP 196/196, Mana 420/420 (aumentada de 370 para 420 pelo colar), MV 144/144.
- **Wimpy:** 45 (estritamente mantido).
- **Armadura:** CA 148 (magia `armor` ativa + colar de pedra púrpura +10).
- **Ouro:** 2.110 moedas na mão (lucro líquido de 2.000 de Gargamel - 15 da tocha + moedas residuais; 0 no banco).
- **Local:** O Templo de Midgaard (repousando / dormindo).
- **Autoquests em andamento:** Nenhuma ativa (todas as elegíveis concluídas, exceto `Dicas Mágicas` no Templo).
- **Equipamentos vestidos:**
  - na cabeça: `a Coroa da Rainha Branca`
  - na orelha direita: `um diminuto brinco de novato`
  - no pescoço (1): `a coleira do dragão de estimação`
  - no pescoço (2): `um colar com uma pedra púrpura` (NOVO: Anti-DT, Abençoado, CA +10, Acerto +1, Dano +1, Des +1, Mana +25)
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
- **Inventário:** `um cantil` (cheio de água cristalina), `a mochila de Pellinore`, `um pergaminho de sabedoria`.
- **Dentro da Mochila:** 2 pães recheados, 1 manto de pano, 1 colar púrpuro sobressalente, a bainha de Excalibur, uma Cruz Ansada, o Cetro do Bispo Negro.

---

## 3. O que já foi descoberto

1. **Bestiário de Abates Confirmados (monstros que NÃO contam para os 10 inéditos):**
   - `monstro invasor` (50 abates)
   - `monstro esfomeado` (36 abates)
   - `monstro agressivo` (18 abates)
   - `líder dos monstros` (3 abates)
   - `monstro novato` (1 abate)
   - `Gargamel` (1 abate, Dia 156)
2. **Magia Sleep de Nível 31 é a Chave para Planos Malucos:**
   - Com 95% de proficiência, `sleep` neutralizou Gargamel instantaneamente. Mobs que caem no sono não reagem, não conjuram e não fogem, permitindo rajadas seguras de `lightning bolt` mesmo contra alvos de alto poder.
3. **Item Anti-DT:**
   - O `colar com uma pedra púrpura` possui a flag ANTI-DT, conferindo proteção contra armadilhas de morte instantânea.

---

## 4. Candidatos a bichos inéditos e ideias criativas

Para atingir a cota de 10 monstros inéditos exigida pelo autor, aqui estão os alvos mais viáveis no mundo já mapeado:

1. **Azrael** (em *O Covil de Gargamel*):
   - Ficou vivo no covil. Consider: Nível: Muito fácil, Vida: É uma perda de tempo, Poder: Fácil. Abate trivial com 1 raio.
2. **Kobold** (em *Uma Divisão da Trilha*, na Floresta a caminho da fazenda):
   - Já verificado no consider como "É uma perda de tempo". Nunca foi abatido.
3. **Zumbi** (em *O Começo Da Passagem* ou *O Corredor Sujo*, na Masmorra dos Novatos):
   - Já catalogado como "É uma perda de tempo".
4. **Diabinho saltitante** (em *Uma Grande Sala*, Masmorra dos Novatos):
   - Presente na área subterrânea da escola de noviços.
5. **Rato gigante / Rato dos esgotos** (em *A Junção no Esgoto*):
   - Veredito anterior assustava ("Você é LOUCO!"), mas com `sleep` a 95% e raio de 66 de dano, pode ser neutralizado de longe sem retaliação.
6. **Cobra dos esgotos** (em *A Junção no Esgoto* ou canais):
   - Veredito "Você é louco?". Com sono arcano prévio, torna-se caçável.
7. **Lobo** (em *A Loja de Animais*, Midgaard, ou nos ermos):
   - Veredito "É uma perda de tempo".
8. **Peão Branco / Peão Negro** (no Grande Tabuleiro de Xadrez):
   - Peão negro já foi testado e morto por scripts de teste, mas não está registrado na tabela de abates do bestiário.
9. **Cavalo ou Bispo do Xadrez** (peças de apoio):
   - Com `sleep` prévio, é possível derrubar uma peça de valor sem perigo de contra-ataque.
10. **Criatura do Milharal** (na borda ou pastagens):
    - Diferente dos 4 invasores da cota do fazendeiro.
11. **Barney ou criatura da Terra das Brincadeiras** (próximo à Vila dos Smurfs):
    - Área mapeada em `fundir_mapa.py`.

---

## 5. O próximo passo, e só ele

1. Acordar no Templo (`wake; stand`).
2. Definir o primeiro alvo da lista de 10 inéditos (recomendado: **Azrael** no Covil de Gargamel ou **Kobold** na Trilha da Floresta).
3. Viajar até o local, aplicar `consider <alvo>`, conjurar `cast 'sleep' <alvo>` e abater com `cast 'lightning bolt' <alvo>`.
4. Registrar o abate formalmente no bestiário e prosseguir para os próximos da contagem até completar 10.

---

## 6. NÃO REPITA

1. **NÃO ataque sem sono prévio (`sleep`) alvos com veredito "Você é louco?" ou superior.**
2. **NÃO pegue armaduras amaldiçoadas (`ITEM_NODROP`).** Se houver espólio no chão de mobs perigosos, usar `identify <item>` antes de pegar.
3. **NÃO desative o wimpy 45.**
4. **NÃO automatize diálogos verbais com NPCs.**

---

## 7. Ferramentas e comandos

- Lançar daemon viva: `$env:MUD_WIMPY="45"; $env:MUD_DAY="156"; python automato/nucleo/driver/live_daemon.py`
- Executar comandos via base: `python -c "import sys; sys.path.insert(0, 'automato/nucleo'); from base import run; print(run('look')[0])"`
- Encerrar sessão com sono e save: `python -c "import sys; sys.path.insert(0, 'automato/nucleo'); from base import call; call('_CLOSE sleep')"`
- Sincronizar herói: `python scripts/sync_hero.py --hero grebolius`
- Validadores: `python scripts/check_project.py` e `python scripts/devolutiva.py`

---

## 8. Devolutiva técnica

| Descobri | Registrei em | O quê |
|---|---|---|
| mapa | `nada` | Salas do Castelo de Gargamel, Armazém e Vila dos Smurfs já constavam consolidadas no mapa.json |
| referência do servidor | `maquina/verificacoes.md` | `identify` gratuito como comando; veredito consider Gargamel/Azrael; sleep funcional no chefe; atributos do colar |
| fato do mundo | `data/heroes/grebolius/conhecimento.md` §52 | Conclusão integral de Uma Lição em Gargamel, compra da poção aquosa (9.750), jarro, chave, tocha e colar púrpuro Anti-DT |
| erro do motor | `nada` | Nenhum erro de motor ocorrido nesta sessão; scripts e camadas operaram de forma estável |

---

## 9. Como encerrar a sua sessão

Ao terminar a sua vez:
1. Retornar ao Templo de Midgaard (`recall; stand`).
2. Beber do cantil se sede, comer se fome.
3. Salvar e deitar: `call('_CLOSE sleep')`.
4. Atualizar `evidence/dia156p.json`, `state.json`, `capitulos.json` e `monstros.md`.
5. Executar `python scripts/sync_hero.py --hero grebolius`.
6. Rodar `python scripts/check_project.py` e `python scripts/devolutiva.py`.
7. Criar o próximo plano numerado (`planos/plano020.md`).
