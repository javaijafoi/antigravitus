# Plano 028 — Capítulo 12: encontrar o tomo pedido por Lemin

| | |
|---|---|
| **Criado em** | 2026-10-19 · Dia 157 |
| **Por** | GPT-6 / Codex (versão específica não informada) |
| **Herói** | grebolius |
| **Objetivo** | Concluir Ajuda Mágica; capítulo 12 segue em curso. Xeque-mate permanece opcional, condicionado a estratégia viável. |
| **Sessão encerrada?** | sim — Templo de Midgaard; save e sleep confirmados; driver finalizado com código 0, sem quit. |

## 1. Onde o objetivo está

Plano 027 executado parcialmente: França e Lyon alcançadas, Lemin encontrado, missão aceita e pergunta sobre Merlin respondida corretamente. A primeira entrega está formalmente ativa: `Ajuda Mágica: Você deve entregar objeto ao personagem.` O pedido literal é **um tomo de pergaminho bem grosso, podendo ser usado**. Nenhum give foi feito. Capítulo 12 aberto e parte do Dia 157 salva; NÃO está concluído.

## 2. Estado exato

- Templo de Midgaard, dormindo; HP 199/199, mana 430/430, MV 145/145.
- Nível 32, EXP 7.225.102; faltam 774.898 para 33. Alinhamento 412, bom.
- Ouro 16.059: banco 15.700, mão 359. Nenhum gasto nesta sessão.
- Wimpy 45; peso 74/115 kg. CON real no score: 9, corrigida no estado.
- CA 165 no último score, com **armor +36 (2 horas restantes)** e **invisibility +40 (9 horas)**. Revalidar e renovar antes de sair. Base registrada: 89.
- 3 pães na mochila; cantil reabastecido e utilizado no encerramento. Sem fome nem sede.
- 9 mortes e 1 DT históricas; nenhum combate, morte ou queda de alinhamento no Dia 157.
- Inventário e equipamento conferidos: mesmos itens, exceto 3 pães consumidos. Mochila de Pellinore preservada.
- Evidência: `evidence/dia157-cap12.json`; transcript `automato/runtime/transcript_dia157_20261019_110528_01cfdc.jsonl`.

## 3. O que já foi descoberto

**Lemin está no Centro da Cidade de Lyon**, na região Notre Dame. Não fica dentro da catedral. `where Lemin` localiza o NPC na área. `look lemin` iniciou o convite; `say sim` aceitou. Pergunta sobre o mago que confeccionou a mochila: Merlin. Ouvir até a linha em que espera a resposta; resposta antecipada não avançou. Depois há monólogo longo sobre o livro destruído e dois pedidos sucessivos de confirmação; conferir score antes de responder cada um.

Rota percorrida e gravada em `mapa.json`: Templo → Praça do Templo → Praça do Comércio → Rua Principal oeste → portão oeste → estrada das planícies → borda da floresta → trilha iluminada → caminho sombreado ao norte → primeira passagem oeste → bifurcação → norte → oeste → norte até colinas → leste para França. Da Entrada Para a França: sul pela ponte e Entrada de Lyon, depois Rua Principal, até Centro da Cidade. Cada marco foi observado. **Não executar a sequência por contagem cega.** Na França, o ramo leste leva à catedral, não ao patrono.

`locate object` foi recusada ao nível 32. `help locate` informa Mago nível 34 e espelho localizador, vendido por Albernathy em Silverthorne ou encontrado no mundo. Ajuda não comprova compra, posse ou sucesso da magia.

## 4. Os bloqueios, e o que já foi tentado

- Falta fonte atual e identificação exata do tomo solicitado. Não presumir que o tomo druídico é o item certo.
- Pierre (Loja de Magias da França) e Toulouse (Loja de Itens Variados) não vendiam tomo nos catálogos vistos.
- Loja de Magias de Midgaard também não vendia tomo.
- Sala de Doações: `look tomo` ausente; dois livros inspecionados eram guias de equipamento e tiro. Transcrição antiga identifica o tomo anterior como **tomo da sabedoria druídica**, posteriormente descartado com junk em 2026-10-16. Não procurar o mesmo item perdido como se estivesse garantido no chão.
- Sala de Leitura e Laboratório dos Magos sem tomo acessível observado. Não atacar a mestra para obter livro.
- `ask lemin tomo` não deu pista adicional. Não repetir sem novo contexto.
- Castelo de Welmar parcialmente reconhecido: saguão, ala oeste, escadaria e corredores até hóspedes. Nenhuma fonte do tomo nas salas visitadas. Porta leste da Escadaria Principal trancada; não forçada. Porta pequena oeste do Saguão de Entrada abre para Uma Pequena Passagem, não atravessada nesta sessão. Isso é fronteira de exploração, **não prova de fonte do tomo**.
- Ajuda do castelo omite parte do trajeto: o caminho efetivo passa pela saída leste, Entrada da Cidade, Intersecção, Estrada do Rei e Fora do Castelo; então norte para ponte levadiça e portão.

## 5. O próximo passo, e só ele

**Identificar uma fonte verificável do tomo exigido por Lemin**, cruzando o pedido e as pistas já registradas. Uma pergunta ao autor sobre localização ficou pendente no chat; ausência de resposta não é autorização para inventar a fonte. Ao obter o item correto, voltar a Lemin, ouvir tudo e reconfirmar score, pedido e inventory imediatamente antes de give. Continuar Ajuda Mágica até confirmação real de conclusão.

## 6. NÃO REPITA

- Não procurar Lemin em Midgaard ou no altar da catedral.
- Não tratar o pergaminho de sabedoria carregado como o tomo sem evidência.
- Não comprar material caro nem entregar livro por tentativa.
- Não atacar habitantes pacíficos, guardas, magos ou animais para descobrir espólios.
- Não cortar monólogos; não automatizar falas de missão em lote.
- Não usar quit, não fechar o capítulo sem completar Ajuda Mágica, não publicar no GitHub.
- `dead_or_menu` já apareceu com HP pleno por histórico de login ou dica com Menu Principal. PARAR e auditar look/score/log, sem confiar cegamente no rótulo ou descartá-lo sem conferência. Não houve correção do motor.

## 7. Ferramentas e comandos

Python disponível em `C:/Users/peter/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe`; não está no PATH desta sessão. Driver em `automato/nucleo/driver/live_daemon.py`, com `MUD_DAY` e `MUD_WIMPY=45`. Porta local 14888. Estado do driver nesta sessão: auth off por falta de .controller; nenhum controlador concorrente observado. Não expor credenciais.

Leitura de cota Codex disponível pelo app: começo da sessão 93% da janela de 5h e 99% semanal restantes. Reconsultar ao retomar; não confundir com a cota Gemini do language server. Aplicar limites do AGENTS §13.

## 8. Devolutiva técnica

| Descobri | Registrei em | O quê |
|---|---|---|
| mapa | `mapa.json` | Rotas observadas até França, Lyon, catedral e parte do castelo; homônimos separados pelo percurso, sem inventar arestas de retorno. |
| referência do servidor | `maquina/verificacoes.md` | where Lemin, cadeia de aceitação, requisito de locate object e efeitos reais das proteções. |
| fato do mundo | `conhecimento.md` §61 | Lemin em Lyon, primeiro material, catálogos e fontes descartadas. |
| erro do motor | PENDENTE | Falso dead_or_menu com personagem viva auditado; janela textual suspeita, sem correção ou teste de regressão. |

## 9. Como encerrar a sua sessão

Retornar ao Templo quando necessário; alimentar, hidratar, confirmar save e sleep, fechar conexão sem quit. Criar Plano 029, atualizar fonte canônica, evidência, mapa e parte do capítulo; rodar sincronização, conferência e devolutiva. Não fechar capítulo por simples sono.
