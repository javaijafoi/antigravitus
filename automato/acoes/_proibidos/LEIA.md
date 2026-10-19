# _proibidos — NÃO EXECUTAR

Estes oito scripts automatizam fala, entrega ou compra de missão (`say`, `ask`, `give`, `buy`). São
anteriores às diretivas do autor do Dia 156 e as violam:

- **AGENTS #13**: entregar ou comprar só com a sub-etapa confirmada em `score tudo`;
- **AGENTS #14**: falar com NPC de missão nunca é automatizado.

Ficam no repositório só como histórico, porque evidências antigas (`dia156l/m/o.json`) citam os
caminhos originais em `automato/acoes/`. Daqui eles **não rodam**: a primeira linha de cada um é
`raise SystemExit('PROIBIDO …')` (e o `sys.path` deles já não acha o `nucleo/`). O
`scripts/check_project.py` dá **erro**
(`automato.import_proibido`) se qualquer código fora desta pasta os importar ou chamar.

O que fazer no lugar: `automato/camadas/navegar.py` leva até o NPC. A fala, o `give` e a compra são
feitos à mão, linha a linha (PROTOCOLO §2).
