# Expedição modular V2 — Grebolius

O Dungeon anterior permanece disponível como legado. Este modo tem uma entrada separada: `scripts/expedition_runner.py`. Nenhum runner antigo, registro de campanha ou crônica é substituído.

## Como as peças se encaixam

```text
Localizar → preparar no local atual → trânsito até o destino
                                         ↓
                       explorar uma sala por vez → recuperar → continuar
                                         ↓
                           escolher repouso próximo → salvar → dormir

Vigilância durante toda a conexão: ataque inesperado → tentar fuga →
conferir resultado → relocalizar → invalidar plano → decisão do modelo.
```

| Peça | O que faz | Quando interrompe |
| --- | --- | --- |
| Localize | Lê atributos, sala e saídas atuais. | Localização ou atributos incompletos. |
| Prepare | Confere ficha, inventário, equipamento, fome, sede e cantil; abastece somente se necessário. | Recipiente ausente, preço, saldo, capacidade ou rota desconhecidos. |
| Scout | Olha ao redor e na direção antes de cada passo. | Saída desapareceu, combate ou perigo explícito. Olhar adiante pode não revelar a próxima sala. |
| Move | Executa um passo, verifica a chegada e chama Ambient. | Recusa, fuga, posição inesperada ou mudança antes do comando. |
| Travel | Vai do ponto A ao B, validando os passos do roteiro. | Divergência do mapa ou encontro que exija decisão. Não inicia limpeza oportunista. |
| Ambient/transit | Avalia a presença na chegada durante um percurso. | Hostil, jogador ou entidade desconhecida exigem avaliação. |
| Ambient/clear | Resolve encontros e espólios antes de sair da sala explorada. | Alvo desconhecido, confronto inviável ou reaparecimentos sem fim. |
| Fight | Avalia adversário; usa magia aprendida; relê recursos a cada turno. | Reserva atingida, recusa, fuga, morte ou desfecho não comprovado. |
| Loot | Decide preservar, coletar, examinar, deixar ou destruir. | Alvo ambíguo ou alteração do inventário não confirmada. |
| Recover | Recupera recursos na própria região e volta a avaliar. | Dano, ataque, fome/sede ou espera sem recuperação suficiente. |
| Camp | Escolhe o repouso adequado mais próximo entre caminhos observados; confirma save e sono. | Local desconhecido, ameaça, trajeto inviável, save/sono não confirmado. |
| ReactionGuard | Monitora mensagens entre ações e enquanto o modelo pensa. | Ataque inesperado ou vida crítica interrompe o plano; fuga malsucedida exige intervenção. |

Cada peça devolve resultado explícito: concluída, pausada, recusada, fuga ou repouso confirmado. Os perfis alteram a política das peças; não duplicam o roteiro. Existe um leitor de socket; o executor e a vigilância compartilham um bloqueio para não enviarem comandos concorrentes. A vigilância recebe mensagens enquanto o executor espera uma resposta, mas a reação aguarda a liberação desse comando, cujo timeout é de seis segundos. Isso não garante reação anterior a todo golpe.

## Recursos e autonomia

- Trabalhar enquanto houver ações úteis e recursos suficientes; recuperar na região e continuar quando houver recuperação comprovada. Não contar passos para forçar um dia “produtivo”.
- Preservar vida para novos golpes e movimento para retirada/repouso. As reservas crescem com o dano observado, custo dos passos e distância do repouso conhecido. Valores iniciais são estimativas conservadoras configuráveis, não mecânicas descobertas no servidor.
- O perfil `dungeon_corajoso` admite mais risco que `exploracao`. `batedor` não inicia luta. Nenhum perfil autoriza atacar um alvo não classificado nem ignora `consider` desfavorável.
- Fim de mana não muda automaticamente para punhal. Corpo a corpo exige configuração explícita e orçamento de golpes medido.
- O estoque inicial padrão é quatro pães e cantil com pelo menos 75% do volume estimado pela descrição. Comprar só depois de preço, ouro e capacidade conferidos. A implementação inicial trata pão e cantil; recipientes e alimentos diferentes exigem adaptação orientada pela ajuda.
- Retorno à cidade ocorre por comida/água; mochila cheia ou pouca vida não disparam viagem de venda ou cura. Após abastecer, tentar retomar a frente anterior se houver identificação individualizada e rota verificável.
- Repouso “mais próximo” significa menor número de passos por ligações efetivamente observadas entre candidatos conhecidos. Três observações sem ameaça e abrigo conhecido ou sala sem passagem são critérios operacionais; não comprovam imunidade a reaparecimentos. Sem candidato adequado, o controle pausa para o modelo.
- Tempo e comandos limitam sessões sem fim: padrão 30 minutos/400 comandos, com margem de encerramento. Os limites são configuráveis e não são metas de consumo.

## Espólios

Preservar provisões, ferramentas, recursos de emergência, itens de missão, raridades e melhorias identificadas. Destruir apenas lixo conhecido, já carregado, com conteúdo conhecido e sem proteção. Desconhecidos ficam registrados para exame e decisão; não supor preço, peso ou utilidade. Coletar apenas o que cabe, preservando espaço, e cujo valor/utilidade esteja verificado. Preço de venda precisa de avaliação comercial; o campo “valor” de identify não prova o preço do comerciante. Arma reserva tem limite configurável. O catálogo é explícito; não aprende descartabilidade por semelhança de nomes.

## Dicionário e conhecimento

Preferir `maquina/dicionario_comandos.md` quando possuir entradas individuais com `**Listado:** sim`. Enquanto estiver em formato de tabela, usar `docs/expedicao_comandos.md`, um recorte da mesma coleta de ajuda, com 31 verbos listados. `--dictionary` seleciona outra edição compatível. A validação bloqueia comandos não listados e sequências injetadas; sintaxe e políticas das ações são implementadas a partir da ajuda. O executor não interpreta automaticamente qualquer manual como código.

Consultar a entrada correspondente antes de ajustar uma ação. Recusa vira evidência no log e pausa para reavaliação; não corrigir a ajuda automaticamente com uma hipótese. Conhecimento da máquina não equivale a habilidade aprendida: a ficha precisa confirmar a magia. Entidades desconhecidas exigem inspeção e classificação baseada em evidência antes de iniciar combate.

## Uso

Prévia, sem conexão:

```text
python -B scripts/expedition_runner.py --dry-run
python -B scripts/expedition_runner.py --dry-run --mode exploracao --config docs/expedicao_grebolius.json
```

Somente numa sessão de jogo já autorizada, com `MUD_PASS` no ambiente:

```text
python -B scripts/expedition_runner.py --live --day <dia> --config docs/expedicao_grebolius.json --destination <id-no-mapa>
```

Sem `--live`, não abre conexão. Uma tentativa de conexão; não reconecta automaticamente. O perfil wimpy vigente vem de `state.json`. Logs novos e exclusivos ficam em `scripts/local/expedition_*.jsonl`, sem alterar os registros da campanha. O runner não publica, reconcilia nem escreve crônicas; o ciclo diário continua responsável pela documentação fiel das evidências.

Durante uma pausa, a conexão e a vigilância continuam disponíveis. A entrada aceita uma ação JSON por linha:

```json
{"action":"observe"}
{"action":"inspect","target":"zumbi"}
{"action":"classify","description":"<linha exata da presença atual>","target":"zumbi","kind":"hostile","evidence":"<resultado observado e fonte da classificação>"}
{"action":"fight","target":"zumbi"}
{"action":"travel","destination":"<id-no-mapa>"}
{"action":"resume"}
{"action":"camp"}
{"action":"close"}
```

Classificações possíveis: `friendly`, `hostile`, `player`; jogadores não são alvos de limpeza automática. Depois de uma interrupção da vigilância, conferir a posição e usar `resume` antes de outro plano. `close` ou fim da entrada encerra a conexão sem afirmar salvamento/sono. Somente `camp` confirmado representa encerramento com repouso.

O arquivo de configuração oferece catálogos de entidades e itens, destino, reservas e limites. O exemplo começa sem autorizar destruição de qualquer item nem inventar classificação de criaturas. Na primeira sala desconhecida, o modelo deverá examinar e classificar. Para mudar a composição de um modo, reutilizar as classes em `scripts/expedition/`; para alterar só o risco, editar o perfil em `models.py`.

## Validação

```text
python -B -m unittest discover -s scripts -p test_expedition.py
```

Os testes impedem abertura de socket e incluem um fluxo completo de exploração terminando em repouso local, observação por passo, trânsito sem limpeza, combate sem vitória presumida, vigilância, fuga e respostas fragmentadas. Aprovação offline não certifica todas as mensagens possíveis do servidor; a estreia ao vivo permanece pendente de sessão autorizada.
