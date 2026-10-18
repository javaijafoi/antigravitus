# Plano 023 — Capítulo 11: Nível 32 e Hipótese de Controle de Grupo com 'sleep' contra Duplas

| | |
|---|---|
| **Criado em** | 2026-10-18 · Dia 156 |
| **Por** | Gemini 3.8 Flash (High) |
| **Herói** | grebolius |
| **Objetivo** | Capítulo 11 — Alcançar o Nível 32 (faltam apenas 66.784 de EXP) e testar a hipótese tática formulada pelo autor Peter: controle de grupo com 'sleep' contra duplas de monstros hostis |
| **Sessão encerrada?** | sim — personagem em total segurança no Templo de Midgaard; HP 196/196, Mana 420/420, MV 144/144, CA 143 (sem armor), wimpy 45, Alinhamento 311 (Bom), Nível 31 consolidado, save e sono confirmados; live_daemon finalizado |

---

## 1. Onde o objetivo está

O **Capítulo 10 ("Dez Cabeças Inéditas") foi CONCLUÍDO e PUBLICADO** com 10 monstros genuinamente malignos, alinhamento moral restaurado para 311 ("Você é bom") e saldo em 1.719 moedas.

O **Capítulo 11** abre com uma meta mecânica e uma hipótese tática de alto valor estratégico formulada pelo autor Peter:
1. **Meta de Nível:** Alcançar o **Nível 32** (faltam apenas **66.784 EXP** para os 7.000.000 necessários).
2. **Hipótese Tática a Testar (Controle de Grupo contra Duplas):**
   - Usar `cast 'sleep' <segundo alvo>` para adormecer um dos monstros em salas com duplas perigosas (ex.: os *dois monstros da lama* na Curva Lamacenta dos Esgotos).
   - Combater o primeiro alvo no 1v1 com feitiços de alvo único (`lightning bolt` e golpes físicos, sem magias de área).
   - Abater o primeiro oponente e, em seguida, finalizar o segundo monstro adormecido.
   - *Precedente:* Testado e validado com louvor no Covil de Gargamel (Gargamel adormecido não reagiu enquanto Azrael foi eliminado, e em seguida Gargamel tombou com um raio).

---

## 2. Estado exato

- **Nível:** 31 (Mago Elfo, 1ª encarnação).
- **EXP:** 6.933.216 (próximo nível: 7.000.000 — faltam apenas 66.784 EXP).
- **Vitals:** HP 196/196, Mana 420/420 (413 no repouso), MV 144/144.
- **Wimpy:** 45 (estritamente calibrado).
- **Alinhamento:** 311 (Bom — `{<<<<<>>---} Você é bom`).
- **Armadura:** CA 143 (sem armor arcana) / CA 148 (com armor arcana).
- **Ouro:** 1.719 moedas na mão (0 no banco).
- **Local:** O Templo de Midgaard (dormindo com save confirmado).
- **Suprimentos:** Cantil saciado de água cristalina, pão consumido.
- **Equipamentos vestidos:**
  - na cabeça: `a Coroa da Rainha Branca`
  - na orelha direita: `um diminuto brinco de novato`
  - no pescoço (1): `a coleira do dragão de estimação`
  - no pescoço (2): `um colar com uma pedra púrpura` (Anti-DT, Abençoado, CA +10, Acerto +1, Dano +1, Des +1, Mana +25)
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

---

## 3. O que já foi descoberto

1. **Dinâmica do Sono Arcano (`sleep`):**
   - Neutraliza o alvo completamente (proficiência 95% em Grebolius).
   - Dura vários minutos/ticks no nível 31.
   - Qualquer dano recebido pelo monstro adormecido acorda-o imediatamente no mesmo turno.
   - Se houver dois monstros, isolar um via sono e focar no outro com feitiços de alvo único preserva o sono do segundo.
2. **Cenário de Teste Identificado:**
   - *Uma Curva Lamacenta no Sistema de Esgoto:* abriga 2 `monstros da lama` (veredito "PROBLEMAS!?"). É o laboratório ideal para o teste de CC em duplas.
3. **Fontes Seguras de EXP para o Nível 32:**
   - 3 Cavaleiros Negros no Xadrez (23.298 EXP cada = 69.894 EXP).
   - Ou 2 Ratos de Esgoto (27.868 EXP cada) + 1 Cavaleiro Negro.

---

## 4. Os bloqueios, e o que já foi tentado

- **Risco de Morte em Teste Prematuro:**
  - Enfrentar os 2 monstros da lama antes de alcançar o Nível 32 acarreta risco de perda de EXP se algo falhar no teste.
  - **Mitigação Tática:** Cravar o Nível 32 primeiro no Xadrez (EXP segura), treinar na guilda e somente depois realizar o teste empírico na Curva Lamacenta.

---

## 5. O próximo passo, e só ele

1. Acordar no Templo (`wake; stand`).
2. Ir ao Tabuleiro de Xadrez e abater 3 Cavaleiros Negros (ou 2 Ratos de Esgoto + 1 peça) para cravar os **66.784 EXP restantes** e atingir o **Nível 32**.
3. Retornar ao Templo de Midgaard (`recall`), visitar a guilda para treinar novas magias ou atributos.
4. Descer aos Esgotos de Midgaard com mana cheia (420) e executar o teste empírico da hipótese na Curva Lamacenta:
   - `cast 'sleep' 2.monstro`
   - `kill monstro` + `cast 'lightning bolt' monstro`
   - Avaliar se o segundo monstro permaneceu adormecido durante todo o combate do primeiro.
5. Retornar ao Templo e registrar os resultados em `maquina/verificacoes.md`.

---

## 6. NÃO REPITA

1. **NÃO use magias de área (como fireball ou color spray) se tentar manter um monstro em sono arcano.**
2. **NÃO ataque o monstro adormecido com golpes fracos se ele possuir barra de vida maciça.**
3. **NÃO mate animais inofensivos, pacíficos ou pets de loja — Grebolius possui alinhamento bom e só caça monstros e seres do mal.**
4. **NÃO reduza o wimpy de 45.**
5. **NÃO entregue itens sem validar a sub-etapa em `score tudo` (Invariante 13).**
6. **NÃO automatize diálogos verbais com NPCs (Invariante 14).**

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
| mapa | `nada` | Salas já mapeadas |
| referência do servidor | `maquina/verificacoes.md` | Hipótese técnica de controle de multidão com 'sleep' contra múltiplos alvos |
| fato do mundo | `data/heroes/grebolius/conhecimento.md` | §55: Hipótese tática a testar formulada pelo autor Peter |
| erro do motor | `nada` | Nenhum erro de motor observado |

---

## 9. Como encerrar a sua sessão

Ao terminar a sua vez:
1. Retornar ao Templo de Midgaard (`recall; stand`).
2. Beber do cantil se sede, comer se fome.
3. Salvar e deitar: `call('_CLOSE sleep')`.
4. Atualizar `evidence/`, `state.json`, `capitulos.json` e `monstros.md`.
5. Executar `python scripts/sync_hero.py --hero grebolius`.
6. Rodar `python scripts/check_project.py` e `python scripts/devolutiva.py`.
7. Criar o próximo plano numerado (`planos/plano024.md`).
