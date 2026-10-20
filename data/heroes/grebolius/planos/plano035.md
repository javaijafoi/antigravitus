# Plano 035 — Capítulo 12: Ajuda Mágica, reativar com Lemin antes do tomo

| | |
|---|---|
| **Criado em** | 2026-10-19 · Dia 157 |
| **Por** | Claude Haiku 5.5 (claude-haiku-5-5) |
| **Herói** | grebolius |
| **Objetivo** | Concluir Ajuda Mágica: reabrir a missão com Lemin, achar o tomo e entregá-lo só com a etapa de entrega confirmada. |
| **Sessão encerrada?** | sim — Templo de Midgaard; `_CLOSE sleep` com save_confirmed=True e sleep_confirmed=True; driver fechado; sem quit. |

Este plano continua o 034 (não editado). Onde divergirem, vale este.

## 1. Onde o objetivo está

O plano 034 dizia que Ajuda Mágica estava em andamento, na etapa `Você deve entregar objeto ao personagem`. **Não está.** Verificado nesta sessão: `autoquest listar` mostra Ajuda Mágica como *disponível* (iniciada com Lemin), e o `score tudo` não tem seção `[Autoquests em andamento]`. A missão precisa ser reaberta com Lemin antes de qualquer entrega. O tomo não foi achado.

## 2. Estado exato

- **Local:** O Templo de Midgaard (`templo_midgaard`), dormindo após `_CLOSE sleep`.
- **Vida/mana/MV:** 199/199 · 430/430 · 145/145 (MV 145 após o `drink`).
- **Nível:** 32 · EXP 7.225.093 · próximo nível em 774.907.
- **Alinhamento:** 393 (Bom) · wimpy 45.
- **Ouro:** 15.920 (15.700 banco + 220 mão). Peso 70/115 kg.
- **Inventário:** cantil (bebido no Templo, sem sede), livro "Equipamentos para Primeira Encarnação", de Jooh (pego na Sala de Doações), rolo de pergaminho (NOTA, não é o tomo), rosário, mochila de Pellinore, pergaminho de sabedoria.
- **Fome:** nenhuma (`fome=nao`). **Não há pão** no inventário: o plano 034 falava em 3 pães na mochila, e não aparecem.
- Armor +36 com 23 horas restantes no `score tudo`.
- Alinhamento caiu de 412 para 393 no Túnel Escuro de Lyon (rato preto, ver §4). Túnel banido.

## 3. O que já foi descoberto

- **Rota até Lyon, verificada à mão:** Templo → `d` (Praça do Templo) → `s` (Praça do Comércio) → `w` (Rua Principal) → `w` (Dentro do Portão Oeste) → `w` (Fora do Portão) → `w` (Estrada) → `w` (Estrada) → `w` (Borda da Floresta) → `w` (Trilha) → `n` → `n` → `w` → `n` → `w` → `n` → `n` → `e` (**Entrada Para a França**, cap12_012) → `s` ×4 (**O Centro da Cidade**, cap12_026, em Lyon). `navegar.py --de cap12_012 --para cap12_026` confirma os quatro `s`.
- **Lemin** está em O Centro da Cidade (Lyon). O `look rapaz` mostra "Lemin está com saúde perfeita" e descreve um jovem aflito.
- **Lyon centro:** loja de magia a leste; loja de produtos variados a oeste; fonte de vinho de mesa.
- **Sala de Doações (`sala_doacoes`):** o livro de Jooh está no chão (o guia de equipamentos, não NOTA). `cast 'identify' livro` falhou duas vezes na sala, com a mesma mensagem "Sua magia falha e desaparece" do Templo: a sala aparenta bloquear magia.
- Lemin ainda não tem a palavra de abertura da missão. `ask lemin ajuda` não gerou resposta.

## 4. Os bloqueios, e o que já foi tentado

- **Missão não ativa (diverge do 034 §2):** `score tudo` sem seção de autoquest; `autoquest listar` mostra Ajuda Mágica como disponível. Tentado: `ask lemin ajuda` — sem resposta. Não testei outras palavras para não aceitar missão errada.
- **Identify na Sala de Doações:** falhou 2 de 2 com "Sua magia falha e desaparece". Pegou-se o livro sem identify (exceção do próprio 034 §5 para sala que bloqueia magia). Registrado.
- **Navegação:** `navegar.py` parou no passo 5 da rota para Lyon ("Término da Rua Principal" x "Rua Principal") e de novo em `--de portao_oeste` (nome curado com sufixo "de Midgaard"). Andei à mão nesses trechos. É o erro de motor já descrito no 034 §8, ainda não corrigido.
- **Túnel Escuro de Lyon:** rato preto atacou primeiro; o contra-ataque automático causou queda de alinhamento 412 → 393. Túnel fora de rota, não voltar.

## 5. O próximo passo, e só ele

**Reabrir Ajuda Mágica com Lemin, à mão.** Ir ao Centro da Cidade de Lyon (rota do §3), ler toda fala de Lemin sem cortar, e responder uma palavra por vez, confirmando com `score tudo` depois de cada resposta, até aparecer `Ajuda Mágica: Você deve entregar objeto ao personagem.` Só então `give livro lemin`, sem nenhuma outra fala antes (AGENTS #13 e #14).
- Se Lemin pedir outra coisa que não o livro, registrar a fala e parar; não entregar.
- Opção padrão, se nenhuma palavra abrir a missão em duas tentativas: parar e perguntar ao autor a palavra de abertura.

## 6. NÃO REPITA

- Não responder a Lemin em rajada ou com palavras chutadas.
- Não usar `identify` na Sala de Doações: a sala bloqueia magia (2 de 2 falhas).
- Não entrar no Túnel Escuro de Lyon (rato agressivo; matar custa alinhamento).
- Não entregar o rolo de pergaminho (é NOTA) nem o livro sem a etapa de entrega no `score tudo`.
- Não procurar o tomo de novo nas lojas de Midgaard, Lyon e Jareth, na Biblioteca de Jareth, em Paris, na catedral, na capela nem nas casas de Lyon.
- Não usar `quit`; não editar planos antigos.
- Não contar com pães: não há no inventário.

## 7. Ferramentas e comandos

Python: `C:\Users\peter\AppData\Local\Programs\Python\Python312\python.exe` (o `python` do PATH não funciona nesta máquina). Driver: `$env:MUD_DAY='157'; $env:MUD_WIMPY='45'; python automato\nucleo\driver\live_daemon.py` em segundo plano. Comandos: `automato\nucleo\driver\play.py "<cmd>"`. Fechar: `play.py "_CLOSE sleep"`. Navegação: `automato\camadas\navegar.py --de <id> --para <id> [--seco]`, sempre com `--de`; quando parar em nome curado, ande à mão. Auditor: `python scripts/auditar_sessao.py`.

## 8. Devolutiva técnica

| Descobri | Registrei em | O quê |
|---|---|---|
| mapa | `mapa.json` | nada (a rota Templo→Lyon já estava no mapa; nada novo gravado nesta sessão) |
| referência do servidor | `maquina/verificacoes.md` | PENDENTE: `where`/`autoquest listar` mostram missão disponível sem `score` de autoquest; identify falha em Sala de Doações |
| fato do mundo | `conhecimento.md` §NN | PENDENTE: Lemin em Lyon centro; livro de Jooh na Sala de Doações; Ajuda Mágica não ativa no Dia 157 |
| erro do motor | `automato/CHANGELOG.md` | PENDENTE: `navegar.py` para em nome curado com sufixo e não deduz origem (já descrito no 034 §8) |

## 9. Como encerrar a sua sessão

Siga `docs/agentes/PROTOCOLO.md` §3. Próximo passo de encerramento: `python scripts/encerrar.py --agente "Claude Haiku 5.5 (claude-haiku-5-5)" --fechar --avanco nao` (avanço não: a missão não foi concluída). Antes, registrar a evidência e as pendências da §8.
