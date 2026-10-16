# automato — como este projeto joga

> **Antes de mexer:** leia [`AGENTS.md`](../AGENTS.md) (regra de identificação, invariantes, checklists e
> mapa de consulta) e registre sua mudança em
> [`docs/agentes/registro_de_evolucao.md`](../docs/agentes/registro_de_evolucao.md). Este README explica
> **como o motor funciona**; o guia de agentes explica **como trabalhar no projeto**.

O **automato** é a forma de jogar deste projeto, empacotada para que **outros agentes** possam
usar, entender e ajustar. Ele não é um "bot que joga sozinho": é um **sistema de camadas** onde
cada peça tem uma responsabilidade e a segurança vem antes da produtividade.

## A ideia em uma frase
> O herói tem **rotinas** (trabalhos que sabe fazer de ponta a ponta). As rotinas são
> **observadas por um vigia**, **arrumadas por um preparador** e **supervisionadas por um turno**.
> Toda rotina **parte do Templo e volta para lá** — é isso que a torna reiniciável.

## As camadas

Três camadas com um trabalho cada — **observar, cuidar, recarregar**. Misturar as três foi o que
fez a rotina parar no meio do mato e voltar para a padaria por fome, com seis pães na mochila.

\`\`\`
turno.py      o encarregado: vigia -> cuidar -> (prepara, se o cuidar pedir) -> rotina -> vigia/min
   |
   +-- vigia.py        OBSERVA. Le o log E o driver (por IPC _STATUS, sem falar com o MUD).
   |                   diagnostico: OK / FOME / SEDE / VIDA_BAIXA / MORTA / TRAVADO / EM_COMBATE
   +-- cuidar.py       CUIDA, em campo. Come, bebe, veste armadura e invisibilidade. NUNCA vai
   |                   a cidade; o unico passo que da' e' sair da area sem magia (o Templo).
   |                   saida: 0 resolvido | 2 precisa recarregar | 1 nao resolveu
   +-- prepara.py      RECARREGA. A ida a cidade: padaria, fonte, banco e sono. So' entra quando
   |                   o cuidar devolve 2, ou com --forcar. Decide por ESTOQUE, nunca por fome.
   +-- trabalhar.py    o despachante: --rotina X carrega rotinas/X.py e chama executar()
         |
         +-- rotinas/milharal.py    caca os invasores do milharal (missao Problemas Agricolas)
         +-- rotinas/esgoto.py      reconhece os esgotos com cuidado
         +-- rotinas/cartografa.py  modo batedor: levanta salas novas sem travar combate
         +-- rotinas/_suspensas/    rotinas proibidas por diretiva (nao reativar)
\`\`\`

**Regra de ouro:** *fome pede comida; a cidade entra quando a comida acaba.* O piso é
\`LIMIAR_PAO = 2\` — mínimo para partir; abaixo disso, recarrega.

O **núcleo** (\`nucleo/\`) sustenta tudo:
- \`config.py\` — **o único lugar** onde se aponta caminho e limite (driver, token, logs, tempo, magias);
- \`base.py\` — \`run()\` (conversa com o driver), navegação por **checkpoints**, \`voltar_ao_templo()\`;
- \`guarda.py\` — a **guarda de repetição**.

## O contrato de uma rotina
\`\`\`python
from base import *

NOME = 'minha-rotina'
DESCRICAO = 'o que ela faz, em uma linha'

def executar() -> bool:
    run('wake'); run('stand')          # o jogo recusa andar "relaxado"
    if not ir_ao_lugar():              # trajeto SEMPRE verificado por marco de sala
        return False
    ...                                # laco de trabalho
    voltar_ao_templo(); run('save')    # SEMPRE termina no Templo e salva
    return True
\`\`\`

**Regras do contrato:**
1. parte do Templo e volta para lá; 2. verifica a sala por **marco**, não por contagem de passos;
3. nunca luta abaixo de \`VIDA_MINIMA\`; 4. termina com \`save\`; 5. pode ser interrompida a
qualquer momento — o \`prepara.py\` conserta o resto.


## O que está DENTRO e o que é REFERENCIADO

Nada essencial vive fora desta pasta: o driver foi migrado para dentro do automato.

### Dentro (o core)
```
automato/
├── nucleo/
│   ├── config.py              <-- O UNICO lugar de configuracao
│   ├── base.py                <-- run(), navegacao, contrato
│   ├── guarda.py              <-- guarda de repeticao
│   └── driver/                <-- O DRIVER COMPLETO (nada fica em scripts/local)
│       ├── debo_bot.py        <-- cliente do MUD
│       ├── parsers.py         <-- parsers das respostas do MUD
│       ├── live_daemon.py     <-- sessao viva unica (127.0.0.1:14888)
│       └── play.py            <-- cliente IPC de linha de comando
├── camadas/                   <-- vigia, prepara, trabalhar, turno
├── rotinas/                   <-- milharal, esgoto, _suspensas/
├── acoes/                     <-- ressuscitar e outras acoes pontuais
└── runtime/                   <-- SEGREDOS E LOGS (fora do git)
    ├── .controller            <-- token do driver
    ├── .mud_pass              <-- senha do MUD
    └── session_live_*.log     <-- os logs que o vigia le
```

### Referenciado (conhecimento do heroi, nao copiado)
Apontado por `nucleo/config.py` em `DIR_HEROI`:

| Arquivo | Para que serve |
|---|---|
| `data/heroes/<heroi>/conhecimento.md` | rotas, economia, armadilhas, tudo o que foi aprendido |
| `data/heroes/<heroi>/diretiva_de_jogo.md` | as regras de como jogar (inclui as diretivas do autor) |
| `data/heroes/<heroi>/mapa.json` | o mapa vivo das salas (fonte das rotas) |
| `data/heroes/<heroi>/missoes.json` | o estado das missoes |

### Requisitos de ambiente
- Python 3.10+;
- rede liberada para `debomud.org:4000` (o MUD) e o driver escutando em `127.0.0.1:14888` (local);
- a senha vem de `MUD_PASS` ou de `automato/runtime/.mud_pass` (nunca versionada).

## Como rodar
\`\`\`powershell
# 1. subir o driver (uma unica sessao viva com o MUD):
python automato/nucleo/driver/live_daemon.py
# 2. conferir se esta tudo no lugar:
python automato/verificar.py
# 3. usar as camadas:
python automato/camadas/trabalhar.py --listar              # catalogo de rotinas
python automato/camadas/vigia.py                           # diagnostico agora
python automato/camadas/prepara.py                         # arruma a personagem
python automato/camadas/trabalhar.py --rotina milharal     # roda uma rotina
python automato/camadas/turno.py --rotina milharal --turnos 2   # turno completo, supervisionado
\`\`\`

## Identifique-se (regra para qualquer agente)
Todo agente que operar este automato deve **dizer quem é** — nome e versão do modelo — no
**começo do relatório** e nos **registros** que gravar:
- no arquivo de evidência, no campo `"agent"`: `{"agent": "<modelo/versao>", "via": "automato"}`;
- na mensagem do commit, no fim: `[agente: <modelo/versao>]`.

Motivo: quando dois agentes (ou o mesmo, meses depois) mexem no mesmo jogo, saber **quem** mudou
o quê evita creditar a um a trapalhada do outro — e torna possível comparar o desempenho entre modelos.

## Invariantes de segurança (não quebrar)
1. **Guarda de repetição**: mesma resposta 3× seguidas → \`recall\` + \`save\` + saída (código 9).
   Ela **ignora comandos benignos** (buy/eat/drink/look/score/rest/sleep...) para não disparar em compras.
2. **O vigia lê o log, não o jogo**: mandar \`score\` enquanto a rotina roda **desincroniza** a sessão.
3. **Nunca deixar rotina sem supervisão**: rodar como job e **ler o log a cada ~60 s**; se o vigia
   acusar problema, **matar o job**.
4. **O ouro dorme no banco**: \`deposit\` no Templo; a morte não leva o que está guardado.
5. **Fome e sede consomem vida e mana por ciclo — e sem comer não há regeneração.** A resposta é
   **comer da bolsa, no lugar**. A cidade só entra quando o **estoque** acaba: `LIMIAR_PAO = 2` é o
   mínimo para partir; abaixo disso, repõe. Sentir fome com seis pães na mochila **não** é motivo
   de caminhada — isso já fez a rotina parar no meio do mato e voltar para a padaria à toa.
   Regra de ouro: **fome pede comida; a cidade entra quando a comida acaba.** **Dormir faminto é o pior caso.**
6. **O Templo é a âncora**: a vida dela é barata de recuperar a partir dali (\`recall\` é grátis até o nível 70).
7. **\`vigia.py\` sozinho não vigia nada.** Ele é um retrato do agora; quem pergunta em laço, a cada
   60 s, é o \`turno.py\`. Conduzir a sessão à mão com \`play.py\` deixa a personagem **sem vigia** — foi
   assim que ela chegou a "morrendo de fome" com o vigia tendo respondido \`OK\` no começo. Toda
   sessão viva passa pelo \`turno.py\`, ou por um laço equivalente.

## Lições de campo (custaram caro — não repetir)

### Ler o servidor sem acreditar na primeira resposta

| Sintoma | Causa | Regra |
|---|---|---|
| `exits` com menos portas que a sala tem | resposta **cortada pela latência** — 20 leituras curtas numa sessão, uma delas com **1 linha numa sala de 6 portas** | **acrescentar a linha de colchetes do `look`** e insistir até o número já conhecido |
| `inventory` devolvendo zero pão | a resposta veio com o texto do `score` | **a resposta tem que se identificar; `None` não é zero** (`nucleo/inventario.py`) |
| O vigia declarando MORTA com ela inteira | "Menu Principal" casou dentro de uma **DICA do servidor** | **sinal de morte exige a linha inteira** (`^\s*Menu Principal\s*$`) |
| Magia "que não funciona" | o **Templo de Midgaard é área sem magia**; e a falha diz "…falha e **desaparece**", palavra que também está no sucesso da invisibilidade | **conjurar na Praça do Templo e conferir a FALHA antes do sucesso** |
| Viagem "quebrada" | nomes de saída lidos do `look` | os nomes vêm do comando **`exits`** |
| Magia no alvo errado | nome genérico | mirar o **nome exato** do monstro |
| Loja não responde ao `list` | **invisibilidade bloqueia comércio** — *"Não negocio com quem não vejo!"* | **`visible` antes de `list`/`buy`/`sell`** |
| Falso MORTA outra vez | o **paginador do `commands`** deixa o driver em `dead_or_menu` | **`term 200 80` no login** (já aplicado em `debo_bot.py`); nunca rodar `commands` no meio de uma rotina |
| Missão "Em andamento" tratada como presa | `autoquest todas` mostra **49 missões, todas "Não feita", zero em andamento** | **não há como abandonar autoquest** (`help abandon` é para a montaria) — e "Em andamento" não é estado durável sem reconferir |
| **Progresso de missão zerado de um dia para o outro** | **`quit` com missão em andamento**: *"Você falhou em suas aventuras! Se quiser concluí-las deverá recomeçá-las!"* — e **não foi a morte** (as missões sobreviveram às 7 mortes) | **encerrar a sessão com `save` e deixar a conexão cair**; nunca `quit` no meio de missão |
| **Concluir que um alvo é invencível** | atacou o Grande Minotauro **de adaga**: *"quase nem sente o golpe"* — mas ela **já o havia matado** nos Dias 85-89 | **ela é maga: `consider` e depois `cast 'magic missile'`**. Corpo a corpo está DESLIGADO (`allow_verified_melee: False` na config). **Ler a doutrina do modo v2 antes de concluir que algo é impossível** |
| Fome com ouro no banco | a padaria cobra da **mão** e o `prepara` só depositava | **`sacar_para_comprar()`** — saca até `SAQUE_PARA_COMPRAR` e **avisa** quando o banco não cobre |
| Rota aplicada da sala errada | o caminho foi calculado a partir do Templo, mas ela estava na Praça | **a origem da rota é a sala onde ela ESTÁ** (`sala_atual()`), não onde se supõe |
| *"Nah... você está muito relaxado"* | a personagem está descansando | `wake; stand` antes de andar |

### Andar sem girar em círculo

| Sintoma | Causa | Regra |
|---|---|---|
| Laços no labirinto | trajeto por **contagem** de passos | andar por **marco de sala** |
| Robô girando na mesma sala | recusa lida como sucesso (`andar` só vê "não pode ir") | **conferir a chegada pela sala ter mudado** |
| Robô que não cobre o mapa | a escolha só olha os vizinhos daqui e esquece as portas deixadas por abrir | **fronteira: abrir a porta onde está; senão BFS até a mais próxima** |
| Porta negada vira ímã | o guarda barra, a rotina marca bloqueio — e continua mirando a mesma sala | **porta recusada sai da fronteira** |
| BFS devolve `None` sem motivo aparente | destinos gravados com o **nome cru** do servidor enquanto o grafo usa normalizado; e o `?` da linha de colchetes sobrescrevendo nome real | **normalizar todo destino ao gravar; `setdefault`, nunca `update`** |

### Cuidar de si em campo

| Sintoma | Causa | Regra |
|---|---|---|
| Volta à cidade sem motivo | fome tratada como gatilho de viagem | **comer da bolsa; repor só com estoque < 2** |
| Muitos *"inconclusivo"* na caçada | **mana seca** | `sleep` ~80 s antes de sair |
| Morte por script | robô solto | **teto de tempo + guarda + supervisão** |

### Método — os erros que custaram rounds inteiros

| Sintoma | Causa | Regra |
|---|---|---|
| "A melhoria piorou" sem prova | bônus de fronteira como peso local (mediu 7 → 4 salas) | **medir antes de acreditar**; fronteira se resolve com caminho, não com peso |
| Avaliar navegação por replay | o grafo gravado só tem saídas de salas **correntes** — trava e mente | **política de navegação só se avalia com sessão real instrumentada** |
| Ensaio que usa o código anterior | editar o arquivo e rodar a sessão **no mesmo bloco de ferramentas**: elas correm em paralelo | **editar, conferir o arquivo, e só então executar** — em chamadas separadas |
| Bug invisível por dois rounds | a variável do título foi **sombreada** por um `for ... in do_look.items()` dentro da própria correção | **depois de editar, varrer o AST** procurando reatribuição de variável de estado |

## Diretivas do autor (valem para outros agentes)
- **PROIBIDO vender armaduras** (Torre Negra ou peão): *"perdemos mais dinheiro do que ganhamos"*.
- **Nada de metajogo nas descrições dos capítulos** — o detalhe técnico fica nas descrições dos dias.
- A **âncora do Dia 100** (a personagem é uma elfa; o nome goblin foi um engano de 99 dias) é
  **âncora do autor**, sem evidência de servidor, e **não reescreve** crônicas antigas.

## Como acrescentar uma rotina (o padrão)
1. **Mapeie à mão primeiro**, sala a sala, e anote o trajeto (de preferência no \`mapa.json\` do herói);
2. Escreva \`rotinas/nova.py\` seguindo o contrato acima;
3. Teste **em trechos curtos**, lendo o retorno de cada um;
4. Só então rode via \`turno.py\` — e **sempre supervisionado**;
5. Se a rotina for proibida/suspensa, mova para \`rotinas/_suspensas/\` com um LEIA-ME explicando.
