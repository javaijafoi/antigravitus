# automato — como este projeto joga

O **automato** é a forma de jogar deste projeto, empacotada para que **outros agentes** possam
usar, entender e ajustar. Ele não é um "bot que joga sozinho": é um **sistema de camadas** onde
cada peça tem uma responsabilidade e a segurança vem antes da produtividade.

## A ideia em uma frase
> O herói tem **rotinas** (trabalhos que sabe fazer de ponta a ponta). As rotinas são
> **observadas por um vigia**, **arrumadas por um preparador** e **supervisionadas por um turno**.
> Toda rotina **parte do Templo e volta para lá** — é isso que a torna reiniciável.

## As camadas
\`\`\`
turno.py      o encarregado: vigia -> prepara (se preciso) -> rotina -> vigia a cada minuto
   |
   +-- vigia.py        le a CAUDA DO LOG do driver (leitura pura: nao manda comando, nao interfere)
   |                   diagnostico: OK / FOME / SEDE / VIDA_BAIXA / MORTA / TRAVADO / SEM_SESSAO
   +-- prepara.py      o arrumador: come, bebe, DEPOSITA O OURO NO BANCO, dorme, volta ao Templo
   +-- trabalhar.py    o despachante: --rotina X carrega rotinas/X.py e chama executar()
         |
         +-- rotinas/milharal.py   caca os invasores do milharal (missao Problemas Agricolas)
         +-- rotinas/esgoto.py     reconhece os esgotos com cuidado
         +-- rotinas/_suspensas/   rotinas proibidas por diretiva (nao reativar)
\`\`\`

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
5. **Fome e sede consomem vida e mana por ciclo.** O prepara resolve — e **dormir faminto é o pior caso**.
6. **O Templo é a âncora**: a vida dela é barata de recuperar a partir dali (\`recall\` é grátis até o nível 70).

## Lições de campo (custaram caro — não repetir)
| Sintoma | Causa | Regra |
|---|---|---|
| *"Nah... você está muito relaxado"* | a personagem está descansando | \`wake; stand\` antes de andar |
| Muitos *"inconclusivo"* na caçada | **mana seca** | \`sleep\` ~80 s antes de sair |
| Viagem "quebrada" | nomes de saída lidos do \`look\` | os nomes vêm do comando **\`exits\`** |
| Laços no labirinto | trajeto por **contagem** de passos | andar por **marco de sala** |
| Morte por script | robô solto | **teto de tempo + guarda + supervisão** |
| Magia no alvo errado | nome genérico | mirar o **nome exato** do monstro |

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
