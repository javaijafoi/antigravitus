---
name: mud-capitulo
description: "Conduzir a Season 02+ por capítulos: abrir um capítulo com objetivo, salvar partes a cada sessão e fechar o capítulo quando a meta for cumprida. Substitui o fluxo por dia; o sono encerra a sessão, não o capítulo."
---

# Ciclo por capítulo (Season 02+)

A partir do Dia 101 a unidade de trabalho e de publicação é o **capítulo**, não o dia. Um capítulo pode atravessar muitas sessões e muitas noites de sono. Ele **não fecha quando se dorme**: fecha quando o **objetivo** dele for resolvido.

Referência completa do modelo: [docs/season_capitulos.md](../../docs/season_capitulos.md). Dados do herói: `data/heroes/<id>/temporadas.json` e `data/heroes/<id>/capitulos.json`.

## Escopo típico de um capítulo
Definido pelo autor no pedido do capítulo. Normalmente: **duas missões** mais o que houver no meio — treinar, melhorar equipamento, vender espólio, repor provisões.

## Fluxo
1. **Abrir** o capítulo (uma vez), com título e objetivo:
   ```bash
   python add_chapter.py --hero grebolius --chapter 1 --tomo 1 --title "TÍTULO" --goal "META VERIFICÁVEL" --kind missao
   ```
2. **Salvar uma parte** ao fim de cada sessão/dia (o capítulo continua aberto):
   ```bash
   python add_chapter.py --hero grebolius --chapter 1 --part --day 102 --date "2026-10-16" --summary "O que realmente aconteceu" --evidence-file scripts/local/fontes.json --source-kind live
   ```
3. Ao cumprir a meta, **fechar** com a crônica do capítulo:
   ```bash
   python add_chapter.py --hero grebolius --chapter 1 --close --day 104 --content-file scripts/local/cap01.txt --excerpt "..." --tags "Missão,Treino" --source-kind live --evidence-file scripts/local/fontes.json
   ```
4. Validar e publicar **o capítulo**:
   ```bash
   python scripts/check_project.py
   python publish_daily.py --publish --push --message "feat(grebolius): capitulo 1 - ..."
   ```

## Regras
- O `goal` é o critério. Sem meta resolvida, o capítulo não fecha — mesmo depois de dormir, salvar e acordar em outro dia.
- Partes podem ser salvas sem publicar. A publicação é do capítulo fechado.
- A doutrina de evidência continua valendo: cada parte e cada capítulo declaram `source_kind` e fontes; nada é narrado sem base na sessão.
- As regras de segurança do jogo são as do [post-mortem da morte #04](../../data/heroes/grebolius/observacoes/morte-04-dia-100.md): **parada dura em 60% da vida**, um comando por vez sob ameaça, fuga é emergência e não licença para lutar, nunca lutar em sala com 2+ monstros.
- Se o capítulo envolver a origem da personagem (Season 02, Tomo I), valem as ressalvas de [notas_editoriais.md](../../data/heroes/grebolius/notas_editoriais.md): só afirmar revelação quando o servidor entregar o gatilho.


## Método de automação (obrigatório desde o Capítulo 2)

**O motor só anda sozinho depois de provar que anda.** A ordem é sempre:

1. **Mapear à mão primeiro** — ir e voltar observando sala a sala; só então escrever o trajeto.
2. **Ler `exits`** para os nomes das saídas (o `look` não traz destino).
3. **Andar por marco** ("até a sala X"), nunca por contagem de passos.
4. **Testar em trechos curtos**, lendo o retorno de cada um, antes de juntar.
5. **Teto de passos e de tempo dentro do script**: ao estourar, `recall` + `save` e sair.
6. **Nunca** rodar caçada em segundo plano — script solto já causou as mortes #5, #6 e #7.
7. **Higiene antes de sair**: `wake; stand` (o jogo recusa andar "relaxado"), `sleep` para encher a mana, comida e água em ordem (`score tudo` confere).
8. **Limite do mundo não é falha da personagem**: quando o gargalo é o caixa de um NPC, registrar e parar.
9. **Não fechar o capítulo antes dos alvos cumpridos** — o sistema devolve para `em_curso` (aconteceu no Dia 136).
