# Plano 034 — Capítulo 12: o tomo de Lemin, com a biblioteca de Jareth achada e vazia

| | |
|---|---|
| **Criado em** | 2026-10-19 · Dia 157 |
| **Por** | Claude Opus 5.5 (claude-opus-5-5) |
| **Herói** | grebolius |
| **Objetivo** | Concluir Ajuda Mágica: achar o tomo e entregá-lo a Lemin só com a etapa confirmada. |
| **Sessão encerrada?** | sim — Templo de Midgaard; `_CLOSE sleep` com save_confirmed=True e sleep_confirmed=True; daemon finalizado com código 0; sem quit. Encerrada por decisão do autor, com a missão aberta. |

Este plano continua o 033 (não editado). Onde divergirem, vale este. Os bloqueios do 032/033 sobre o Beco Escuro e a porta da Vovó **perderam o sentido**: a biblioteca que se procurava atrás deles foi achada em outro lugar.

## 1. Onde o objetivo está

`score tudo`, na abertura e no fechamento: **`Ajuda Mágica: Você deve entregar objeto ao personagem.`** O pedido de Lemin segue sendo "um tomo de pergaminho bem grosso. Pode ser usado mesmo." **O tomo não foi achado.** Nenhum give. A Biblioteca da cidade de Jareth foi achada, mas não tem tomo. Paris, as alas escondidas da catedral, a capela e as casas de Lyon também não têm.

## 2. Estado exato

- Templo de Midgaard, dormindo. Vida 199/199, mana 430/430, movimento 145/145. Nível 32, EXP 7.225.093.
- **Alinhamento 393** (era 412; ver §4). 9 mortes e 1 DT, sem mudança.
- Ouro 15.920: 220 na mão, 15.700 no banco. Peso 69/115 kg.
- Inventário: cantil (cheio), rosário, mochila de Pellinore (3 pães recheados, manto de pano, colar com pedra púrpura, bainha de Excalibur, Cruz Ansada, Cetro do Bispo Negro), pergaminho de sabedoria ("A Lenda de Nambor") e **um rolo de pergaminho** comprado agora (NOTA, peso 1 — não é o tomo; guardado).
- armor +36 com 29 horas no score final; invisibility não está ativa.
- Evidência: `evidence/dia157-biblioteca-paris.json`. Transcript: `automato/runtime/transcript_dia158_20261019_152259_a5c65c.jsonl` (o "dia158" no nome foi engano meu no `MUD_DAY`; a data é a mesma do Dia 157).

## 3. O que já foi descoberto

- **A Biblioteca de Jareth** (`jr_biblioteca` no mapa): de Uma Praça (`lb013`), `n,n,n,n,e,e,e,e,e,n,w,w,s` — Rua do Rio ao norte, ponte, margem até a curva, Caminho de Tábuas a oeste duas vezes, sul. Já constava em `help mapa 2`. Tem a assistente (convite de *Arrumando a Biblioteca*, nível 60+, "Pode me ajudar? Sim?" — **não responder**) e a bibliotecária. Nada no chão, sem `list`. **Não tem o tomo.**
- **Lojas de Jareth:** Pergaminhos e Afins (sul da Praça, oeste) vende só um rolo de pergaminho (nota) e, mais baratos que Midgaard, retorno 6.209 e remover maldições 4.369. Dalston: malas, mochila, lanterna, tocha.
- **Champs Elysées → Paris:** norte da Entrada Para a França; `open norte` no portão; rota do aviso **N L N O S O N O** até O Centro Histórico da França; volta **L S L N L S O** e **S**. Paris: praça 3×3, hotel fechado, QG dos Mosqueteiros com porta **trancada** (guarda dormindo; não é alvo).
- **Catedral:** do Átrio, leste/oeste são átrios fechados; do Corredor Central, leste e oeste abrem as naves laterais. Corredor Oriental norte → leste Sala de Espera → `open leste` → **A Pequena Capela** (padre Tintoreto). **O Campanário da Catedral existe** (`where corcunda`), entrada não achada pela catedral, pela Rua Notre Dame nem pelo Fim da Rua.
- **Lyon:** casa, parque, cabana (comerciante; `list` recusado), outra casa, Estação de Carruagens (centro de Lyon 50, **centro da cidade de Paris 85**; não usada), Túnel Escuro (rato agressivo).
- **`where <nome>` revela salas fora do mapa** (achou a capela e o campanário). **`help mapa <n>`** dá rota de 33 regiões.
- Tudo no `mapa.json` (+50 salas) e no conhecimento §66.

## 4. Os bloqueios, e o que já foi tentado

- **Fonte do tomo:** descartados, com observação, as lojas de Midgaard, Lyon e Jareth, a biblioteca do Lorde, a Biblioteca de Jareth, Paris, a catedral visível, a capela e as casas de Lyon.
- **Abertos, sem tentativa:** (a) os **livros-guia da Sala de Doações** (o guia de equipamentos de Jooh é longo e "usado"; nunca identificados); (b) a **Torre da Magia** (`help mapa 29`, a leste de Jareth; zona provavelmente acima do nível 32); (c) o **Campanário** (entrada escondida); (d) a **carruagem** de Lyon para o "centro da cidade de Paris" (pode ser outra área); (e) o QG trancado dos Mosqueteiros (não forçar).
- **FALHA do auditor (diretiva §22), justificada:** no Túnel Escuro de Lyon, "um rato preto" atacou primeiro ("Um rato preto tenta te morder, mas erra"); o contra-ataque automático o matou e o alinhamento caiu **412 → 393**. Parei, conferi a causa no log e **bani o túnel**. Não segui para O Beco Sem Saída.
- **Erro de método meu:** três `cast 'armor'` e três `cast 'invisibility'` dentro do Templo, que bloqueia magia (diretiva §7). O autor cobrou estudar os documentos antes. Corrigido conjurando na Praça do Templo.

## 5. O próximo passo, e só ele

**Testar a pista (a), a mais barata: o guia de Jooh da Sala de Doações.** Abrir o driver e rodar `score tudo` (precisa mostrar `Ajuda Mágica: Você deve entregar objeto ao personagem.`). Templo → `e` (Sala de Doações) → `look livro` para confirmar que é o guia de equipamentos → `cast 'identify' livro` ainda no chão (o auditor cobra identify antes de get; se a sala bloquear magia como o Templo, registrar a resposta e só então `get livro`, que é doação) → `get livro`. Se o tipo for livro (não NOTA), levar a Lemin por `navegar.py --de praca_templo` até a Entrada Para a França e a pé até O Centro da Cidade de Lyon; lá, `score tudo` de novo e **só então** `give livro lemin`, à mão, sem nenhuma outra fala antes (AGENTS #13 e #14). Se o identify mostrar NOTA ou Lemin recusar, voltar ao §4 e seguir a pista (d), a carruagem de Lyon para o centro de Paris (85 moedas).

## 6. NÃO REPITA

- Não conjurar no Templo nem na Loja de Magias.
- Não procurar o tomo de novo: nas lojas de Midgaard, Lyon e Jareth; na Biblioteca de Jareth; na biblioteca do Lorde; em Paris; na catedral e na capela; nas casas de Lyon.
- **Não entrar no Túnel Escuro de Lyon** (rato agressivo; matar custa alinhamento).
- Não responder à assistente de bibliotecária nem a nenhum convite de outra missão com Ajuda Mágica ativa.
- Não entregar o rolo de pergaminho a Lemin (é nota, não tomo).
- Não forçar portas trancadas (QG dos Mosqueteiros, Vovó, cadeia).
- Não mandar dois comandos de movimento no mesmo processo em segundo plano (mandei um `e` a mais em Jareth assim).
- Não usar `quit`; não editar planos antigos.

## 7. Ferramentas e comandos

Python: `C:\Users\peter\AppData\Local\Programs\Python\Python312\python.exe`. Driver: `MUD_DAY=157 MUD_WIMPY=45 python automato/nucleo/driver/live_daemon.py` em segundo plano; `play.py "<cmd>"`; fechar com `play.py "_CLOSE sleep"`. Navegação: `automato/camadas/navegar.py --de <id> --para <id>` — **passe sempre `--de`**, e saiba que ele para em nome curado com sufixo, como "A Rua Principal (Oeste)"; nesses trechos, ande por marco à mão. Auditor: `python scripts/auditar_sessao.py`. Rotas novas: `navegar.py --de lb013 --para jr_biblioteca`, `--de cap12_012 --para nd_capela`, `--de cap12_012 --para ly_estacao`.

## 8. Devolutiva técnica

| Descobri | Registrei em | O quê |
|---|---|---|
| mapa | `mapa.json` | +50 salas: Rua do Rio, margem, Caminho de Tábuas e Biblioteca de Jareth; Champs Elysées (rota em nota) e Paris; alas da catedral e capela; casas, estação e túnel de Lyon. |
| referência do servidor | `maquina/verificacoes.md` | `help mapa <n>`; `list <n>` em loja comum não inspeciona; `list` fora de loja; `look <npc>` dispara fala de missão; `where` revela salas. |
| fato do mundo | `conhecimento.md` §66 | Biblioteca de Jareth sem tomo; Paris e a catedral; rato de Lyon custa alinhamento; pistas que restam. |
| erro do motor | PENDENTE | `navegar.py` para em nome curado com sufixo e não deduz origem homônima (descrito no registro de evolução; não corrigido). |

## 9. Como encerrar a sua sessão

Templo, comer e beber, `_CLOSE sleep` com `sleep_confirmed=True`, evidência com autoria, plano 035, `auditar_sessao.py` sobre o transcript e `devolutiva.py` (ou o `encerrar.py`, se a outra sessão já o tiver publicado).
