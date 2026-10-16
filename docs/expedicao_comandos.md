# Comandos essenciais da expedição modular

Recorte técnico das consultas de 15/10/2026, para uso quando o dicionário completo ainda estiver no formato de tabela. A máquina conhece esta referência; isso não concede habilidades à personagem. Listado significa presença em `commands`, e não execução prática aprovada de todas as variações. A lista completa e as correções pertencem a `maquina/`.

## `look`

**Listado:** sim. **Consulta:** `help look`. Fonte: consultas locais preservadas; ajuda pode ser parcial.

```text
1.1.2 3.1.5 4.3.3 VER LOOK

Uso: ver
     ver <item>
     ver <em | no | na | dentro | in> <item>
     ver <o | a | at> <item>
     ver <direção>

Use este comando para observar os arredores.

Exemplos:

  > ver
  > ver o anjo
  > ver dentro da mochila
  > ver sul

Observe que se você VER O CORPO você não verá o conteúdo dele. Para ver
o que está dentro de um contêiner (por exemplo, um corpo) use VER EM <objeto>.

Veja também: EXAMINAR, PEGAR, LER
```

## `exits`

**Listado:** sim. **Consulta:** `help exits`. Fonte: consultas locais preservadas; ajuda pode ser parcial.

```text
1.1.3 SAÍDAS SAIDAS EXITS

Uso: saídas

Fornece uma lista das saídas diretas de sua localidade. Obviamente, as menos
visíveis (como portas secretas) não serão exibidas por este comando - você
tem que PENSAR para que possa localizar estas! =P

Veja também: AUTOSAÍDAS
```

## `score`

**Listado:** sim. **Consulta:** `help score`. Fonte: consultas locais preservadas; ajuda pode ser parcial.

```text
4.2.2 PONTOS SCORE INFLUÊNCIAS INFLUENCIAS AFFECTS

Uso: pontos
         pontos tudo
         pontos vida
         pontos mana
         pontos mov
         pontos ouro
         pontos alinhamento
         pontos estado
         pontos autoquest

Provê informações úteis sobre seu estado, como idade, pontos de vida, mana,
pontos de movimento, classe de armadura, alinhamento, pontos de experiência,
quantidade de ouro sendo carregado, quanto tempo você esteve jogando, número
de mortes, armadilhas de morte, vitórias na arena, sobre quais influências
seu personagem está no momento, entre outras.

Use PONTOS TUDO para obter um relatório completo, e não apenas as
informações principais sobre seu personagem.

O comando PONTOS (SCORE) também pode exibir informações específicas sobre o seu 
personagem para agilizar a leitura e entendimento das informações. Para isso, 
basta adicionar ao final do comando PONTOS a informação que você deseja obter
separadamente. As opções individuais são: 

pontos vida - exibe em quantidade e porcentagem a vida do seu personagem.
pontos mana - exibe em quantidade e porcentagem a mana do seu personagem.
pontos mov - exibe em quantidade e porcentagem os movimentos do seu personagem.
pontos ouro - exibe a quantidade de ouro que seu personagem carrega e em sua conta bancária.
pontos alinhamento - exibe o alinhamento do seu personagem.
pontos estado - exibe os estados e condições do seu personagem.
pontos aventura - exibe informações sobre aventuras em andamento pelo seu personagem.

Veja também: AC, EXPERIÊNCIA, BARRALUTA, REGENERAÇÃO, ACESSIBILIDADE
```

## `inventory`

**Listado:** sim. **Consulta:** `help inventory`. Fonte: consultas locais preservadas; ajuda pode ser parcial.

```text
3.1.1 INVENTÁRIO INVENTARIO INVENTORY

Uso: inventário 

Use este comando se você não tem certeza do que está carregando, ou caso queira
simplesmente checar se nenhum ladrão furtou sua mochila sem que você tenha
percebido.

Veja também: EQUIPAMENTOS, SEGURAR, REMOVER, VESTIR
```

## `consider`

**Listado:** sim. **Consulta:** `help consider`. Fonte: consultas locais preservadas; ajuda pode ser parcial.

```text
4.3.6 CONSIDERAR CONSIDERE

Uso: considerar <criatura>

Este comando efetua uma comparação de forças entre você e seu alvo.

Entretanto, tal comparação não passa de uma rude estimativa numérica; cada
aventureiro conhece bem o próprio poder!

Exemplo:

  > considerar cachorro

See also: GOLPEAR, MATAR
```

## `diagnose`

**Listado:** sim. **Consulta:** `help diagnose`. Fonte: consultas locais preservadas; ajuda pode ser parcial.

```text
DIAGNOSTICAR DIAGNOSTIQUE DIAGNOSE

Uso: diagnosticar
     diagnosticar <vítima>

O comando DIAGNOSTICAR lhe mostra o quão ferido um personagem aparenta.
Caso esteja lutando contra alguém, você pode usar DIAGNOSTICAR para
diagnosticar a pessoa com quem você estiver lutando.

Exemplos: 

  > diagnosticar
  > diagnosticar rasmussen

Veja também: CONSIDERAR
```

## `cast`

**Listado:** sim. **Consulta:** `help cast`. Fonte: consultas locais preservadas; ajuda pode ser parcial.

```text
6.1.1 LANÇAR LANCAR LANCE CAST

Uso: lançar '<nome da magia>'
     lançar '<nome da magia>' <alvo>

Este é o comando utilizado para lançar magias. Utilize-o para lançar magias,
em alguém, ou em algum objeto.

Exemplo:

  > lançar 'burning hands' <alvo>
  Note que o nome da magia precisa estar entre aspas "'".

Veja também: AJUDA MAGIA <nome de uma magia>

Exemplos:

  > ajuda magia cure ligh
  > ajuda magia energy drain
```

## `flee`

**Listado:** sim. **Consulta:** `help flee`. Fonte: consultas locais preservadas; ajuda pode ser parcial.

```text
5.1.2 FUGIR FUJA FLEE

Uso: fugir

Se você está numa luta e as coisas estão começando a ficar um pouco
desfavoráveis (talvez você esteja morrendo), apenas digite FUGIR, e pronto!
Você evitou o perigo - isto é, SE existir uma saída próxima viável, e SE essa
saída não levar você simplesmente da brasa para o fogo... no entanto, quem quer
mesmo viver pra sempre?

Veja também: COVARDE
```

## `save`

**Listado:** sim. **Consulta:** `help save`. Fonte: consultas locais preservadas; ajuda pode ser parcial.

```text
SALVAR SAVE

Uso: salvar

Salva seu personagem. Isso inclui pontos de experiência, força, ouro, etc.
Seu equipamento é tambem salvo no (improvável?) caso de uma pane do jogo.
O jogo periodicamente salva automaticamente você e seu equipamento; então
não é necessário fazer com que seu cliente (o programa pelo qual você
conecta no jogo) salve automaticamente para você.

Você NÃO PODE carregar uma versão salva se você morrer -- seu personagem ainda
existe, mas você irá perder pontos de experiência, e todos seus objetos
continuarão no jogo, em seu corpo.

Veja também: SAIR
```

## `sleep`

**Listado:** sim. **Consulta:** `help sleep`. Fonte: consultas locais preservadas; ajuda pode ser parcial.

```text
1.3.1 ACORDAR ACORDE DORMIR DURMA DESCANSAR DESCANSE SENTAR SENTE LEVANTAR LEVANTE WAKE SLEEPING REST SIT STAND

Utilize esses comandos para mudar de posição. Caso se sinta cansado, talvez
seja uma boa idéia sentar e descansar por um tempo, ou mesmo tirar um cochilo,
com o comando DORMIR.

Veja também: DIREÇÕES, MAGIA SLEEP
```

## `wake`

**Listado:** sim. **Consulta:** `help wake`. Fonte: consultas locais preservadas; ajuda pode ser parcial.

```text
1.3.1 ACORDAR ACORDE DORMIR DURMA DESCANSAR DESCANSE SENTAR SENTE LEVANTAR LEVANTE WAKE SLEEPING REST SIT STAND

Utilize esses comandos para mudar de posição. Caso se sinta cansado, talvez
seja uma boa idéia sentar e descansar por um tempo, ou mesmo tirar um cochilo,
com o comando DORMIR.

Veja também: DIREÇÕES, MAGIA SLEEP
```

## `sit`

**Listado:** sim. **Consulta:** `help sit`. Fonte: consultas locais preservadas; ajuda pode ser parcial.

```text
1.3.1 ACORDAR ACORDE DORMIR DURMA DESCANSAR DESCANSE SENTAR SENTE LEVANTAR LEVANTE WAKE SLEEPING REST SIT STAND

Utilize esses comandos para mudar de posição. Caso se sinta cansado, talvez
seja uma boa idéia sentar e descansar por um tempo, ou mesmo tirar um cochilo,
com o comando DORMIR.

Veja também: DIREÇÕES, MAGIA SLEEP
```

## `rest`

**Listado:** sim. **Consulta:** `help rest`. Fonte: consultas locais preservadas; ajuda pode ser parcial.

```text
1.3.1 ACORDAR ACORDE DORMIR DURMA DESCANSAR DESCANSE SENTAR SENTE LEVANTAR LEVANTE WAKE SLEEPING REST SIT STAND

Utilize esses comandos para mudar de posição. Caso se sinta cansado, talvez
seja uma boa idéia sentar e descansar por um tempo, ou mesmo tirar um cochilo,
com o comando DORMIR.

Veja também: DIREÇÕES, MAGIA SLEEP
```

## `stand`

**Listado:** sim. **Consulta:** `help stand`. Fonte: consultas locais preservadas; ajuda pode ser parcial.

```text
1.3.1 ACORDAR ACORDE DORMIR DURMA DESCANSAR DESCANSE SENTAR SENTE LEVANTAR LEVANTE WAKE SLEEPING REST SIT STAND

Utilize esses comandos para mudar de posição. Caso se sinta cansado, talvez
seja uma boa idéia sentar e descansar por um tempo, ou mesmo tirar um cochilo,
com o comando DORMIR.

Veja também: DIREÇÕES, MAGIA SLEEP
```

## `north`

**Listado:** sim. **Consulta:** `help north`. Fonte: consultas locais preservadas; ajuda pode ser parcial.

```text
1.1.1 NORTE SUL LESTE OESTE CIMA BAIXO SUBIR DESCER SUBA DESÇA ANDAR ANDANDO NORTH SOUTH EAST WEST UP DOWN

Uso: norte
     sul
     leste
     oeste
     cima
     baixo

Use um desses comandos para andar na direção desejada.
```

## `south`

**Listado:** sim. **Consulta:** `help south`. Fonte: consultas locais preservadas; ajuda pode ser parcial.

```text
1.1.1 NORTE SUL LESTE OESTE CIMA BAIXO SUBIR DESCER SUBA DESÇA ANDAR ANDANDO NORTH SOUTH EAST WEST UP DOWN

Uso: norte
     sul
     leste
     oeste
     cima
     baixo

Use um desses comandos para andar na direção desejada.
```

## `east`

**Listado:** sim. **Consulta:** `help east`. Fonte: consultas locais preservadas; ajuda pode ser parcial.

```text
1.1.1 NORTE SUL LESTE OESTE CIMA BAIXO SUBIR DESCER SUBA DESÇA ANDAR ANDANDO NORTH SOUTH EAST WEST UP DOWN

Uso: norte
     sul
     leste
     oeste
     cima
     baixo

Use um desses comandos para andar na direção desejada.
```

## `west`

**Listado:** sim. **Consulta:** `help west`. Fonte: consultas locais preservadas; ajuda pode ser parcial.

```text
1.1.1 NORTE SUL LESTE OESTE CIMA BAIXO SUBIR DESCER SUBA DESÇA ANDAR ANDANDO NORTH SOUTH EAST WEST UP DOWN

Uso: norte
     sul
     leste
     oeste
     cima
     baixo

Use um desses comandos para andar na direção desejada.
```

## `up`

**Listado:** sim. **Consulta:** `help up`. Fonte: consultas locais preservadas; ajuda pode ser parcial.

```text
1.1.1 NORTE SUL LESTE OESTE CIMA BAIXO SUBIR DESCER SUBA DESÇA ANDAR ANDANDO NORTH SOUTH EAST WEST UP DOWN

Uso: norte
     sul
     leste
     oeste
     cima
     baixo

Use um desses comandos para andar na direção desejada.
```

## `down`

**Listado:** sim. **Consulta:** `help down`. Fonte: consultas locais preservadas; ajuda pode ser parcial.

```text
1.1.1 NORTE SUL LESTE OESTE CIMA BAIXO SUBIR DESCER SUBA DESÇA ANDAR ANDANDO NORTH SOUTH EAST WEST UP DOWN

Uso: norte
     sul
     leste
     oeste
     cima
     baixo

Use um desses comandos para andar na direção desejada.
```

## `buy`

**Listado:** sim. **Consulta:** `help buy`. Fonte: consultas locais preservadas; ajuda pode ser parcial.

```text
COMPRAR COMPRE BUY

Uso: comprar <nome do item>
     comprar #<número>
     comprar n.<nome do item>
     comprar n <compre do item>
     comprar n #<número>

Se você gostaria de adquirir um item de uma loja e tem o dinheiro, você pode
comprá-lo. Itens podem ser comprados pelo nome ou pelo número na lista da loja.
Também podem ser comprados em quantidades.
 
Exemplos:
 
  > comprar espada    (compra a primeira espada na lista)
  > comprar #3        (compra o terceiro item na lista)
  > comprar 4.espada  (compra a quarta espada na lista)
  > comprar 10 pão    (compra 10 unidades de pão)
  > comprar 10 #2     (compra 10 unidades do segundo item na lista)
 
Veja também: LISTAR, VENDER, LOJAS, VALOR
```

## `eat`

**Listado:** sim. **Consulta:** `help eat`. Fonte: consultas locais preservadas; ajuda pode ser parcial.

```text
3.3.1 FOME COMER COMA SEDE BEBER BEBA BEBERICAR BEBERIQUE PROVAR PROVE EAT DRINK SIP TASTE

Uso: comer <item>
     provar <item>
     beber [do] <item>
     bebericar [do] <item>

Se você está com fome ou sede, esses comandos são para você!

  > comer pão
  > provar pão
  > beber copo
  > beber do cantil
  > bebericar da fonte
```

## `drink`

**Listado:** sim. **Consulta:** `help drink`. Fonte: consultas locais preservadas; ajuda pode ser parcial.

```text
3.3.1 FOME COMER COMA SEDE BEBER BEBA BEBERICAR BEBERIQUE PROVAR PROVE EAT DRINK SIP TASTE

Uso: comer <item>
     provar <item>
     beber [do] <item>
     bebericar [do] <item>

Se você está com fome ou sede, esses comandos são para você!

  > comer pão
  > provar pão
  > beber copo
  > beber do cantil
  > bebericar da fonte

DICA: Os deuses são os responsáveis pela criação e manutenção de nosso jogo. Respeite-os, pois é graças a eles que este mundo existe.
```

## `fill`

**Listado:** sim. **Consulta:** `help fill`. Fonte: consultas locais preservadas; ajuda pode ser parcial.

```text
ENCHER ENCHA FILL

Uso: encher <recipiente> <recipiente de onde irá encher>

Utilize este comando para encher, com um líquido de uma fonte à sua frente,
um recipiente que você esteja segurando.

Exemplo:

  > encher cantil fonte

Veja também: DESPEJAR
```

## `list`

**Listado:** sim. **Consulta:** `help list`. Fonte: consultas locais preservadas; ajuda pode ser parcial.

```text
LISTAR LISTE

Uso: listar
     listar <tipo do objeto>

Se você gostaria de ver quais itens de uma loja estão à venda, dê uma olhada
na lista. A lista contém todos os itens à venda no momento, assim como a
quantidade em estoque. O preço para cada item também será listado. Caso você
tenha interesse num tipo particular de item, você pode especificar quais itens
listar.
 
Exemplos:
 
  > listar            (lista todos itens à venda)
  > listar espada     (lista todas espadas à venda)
 
Veja também: COMPRAR, VENDER, LOJAS, VALOR
```

## `examine`

**Listado:** sim. **Consulta:** `help examine`. Fonte: consultas locais preservadas; ajuda pode ser parcial.

```text
3.1.7 4.3.4 EXAMINAR EXAMINE

Uso: examinar <alvo a ser examinado>

Com este comando você poderá obter informações valiosas sobre um objeto
ou um monstro.

Veja também: VER
```

## `identify`

**Listado:** sim. **Consulta:** `help identify`. Fonte: consultas locais preservadas; ajuda pode ser parcial.

```text
"MAGIA IDENTIFY"

Uso    : lançar 'identify' <indivíduos | objeto>
Efeito : Descreve o alvo
Duração: Instantânea
Acumula: Não
Nível  : Mago nível 22

A magia IDENTIFY permite que o conjurador identifique as propriedades de um objeto, 
como tipo, dano, bônus, etc.
Seu funcionamento é idêntico ao comando IDENTIFICAR, que, contudo, só pode ser
utilizado por jogadores abaixo do nível 80 da primeira encarnação. Após essa
marca, só é possível identificar objetos através da magia IDENTIFY.

Veja também: IDENTIFICAR, CREATURE KNOWLEDGE
```

## `equipment`

**Listado:** sim. **Consulta:** `help equipment`. Fonte: consultas locais preservadas; ajuda pode ser parcial.

```text
3.2.1 EQUIPAMENTOS EQUIPMENT

Uso: equipamentos

Fornece uma lista de todos os equipamentos que você estiver vestindo, segurando
e empunhando.

Veja também: INVENTÁRIO, REMOVER, VESTIR
```

## `get`

**Listado:** sim. **Consulta:** `help get`. Fonte: consultas locais preservadas; ajuda pode ser parcial.

```text
3.1.2 PEGAR GET TAKE

Uso: pegar <objeto>
     pegar tudo
     pegar tudo dentro de <objeto>
     pegar tudo dentro de todo.<objeto>
     pegar todo.<objeto> dentro de todo.<objeto>

Se você encontrar algo interessante jogado no chão, pode pode PEGAR este
objeto e carregá-lo em seu inventário.  PEGAR também é utilizado para
pegar objetos de dentro de baús, mochilas ou qualquer outro tipo de contêiner.

Exemplos:

  > pegar espada corpo          (uma espada dentro de um corpo)
  > pegar tudo dentro de corpo  (todos itens dentro de um corpo)
  > pegar tudo todas.mochila    (tudo dentro de todas as mochilas)
  > pegar todo.pão toda.mochila (todos os pães dentro de todas as mochilas)

Quando você não usar o objeto após "dentro de", você tentará pegar algo que
estiver no chão.

Note que o uso de "dentro de" é somente cosmético, para entender melhor o que
se faz. Se você estiver acostumado com o comando, poderá omití-lo.

Se ficou um pouco confuso, ao ler troque o ponto "." por "objeto do tipo"; e o
espaço por "dentro de", caso já não esteja na frase. Nesse caso, vamos usar o
"dentro de", então concentre-se apenas em entender o ponto ".".

Exercite um pouco esse raciocínio:

PEGAR ...
                                 "tudo" = "tudo"
                             "todo.pão" = "todo objeto do tipo pão"
         "pegar tudo dentro da mochila" = "pegar tudo dentro da mochila"
 "pegar tudo de dentro de toda.mochila" = "pegar tudo de dentro de todo objeto
                                           do tipo mochila"
     "pegar todo.pão dentro da mochila" = "pegar todo objeto do tipo pão dentro
                                           da mochila"
"pegar todo.pão dentro de toda.mochila" = "pegar todo objeto do tipo pão dentro
                                           de todo objeto do tipo mochila"

Nesse ponto você já deve ter percebido que o uso do termo "tudo" é especial.
Não importa se você usar o termo "tudo", "todas" etc; eles são permutáveis.

Aqui vai a lista completa deles: TUDO, TODA, TODO, TODAS, TODOS e ALL.

Veja também: SOLTAR, PÔR
```

## `junk`

**Listado:** sim. **Consulta:** `help junk`. Fonte: consultas locais preservadas; ajuda pode ser parcial.

```text
3.1.9 DESCARTAR DESCARTE JUNK

Usage: descartar <objeto>
       descartar <número> moedas

Use DESCARTAR, ao invés de SOLTAR, se você quiser manter o mundo um pouco
mais limpo. Ao DESCARTAR algum objeto, ele desaparecerá e você ganhará algumas
moedas ou pontos de experiência, da mesma forma que acontece ao soltar algo no
depósito de lixo.

Exemplos:

  > descartar copo
  > descartar todos.bronze
  > descartar 500 moedas

Veja também: DOAR, SOLTAR
```

## `close`

**Listado:** sim. **Consulta:** `help close`. Fonte: consultas locais preservadas; ajuda pode ser parcial.

```text
1.1.6 ABRIR ABRA FECHAR FECHE TRANCAR TRANQUE DESTRANCAR DESTRANQUE OPEN CLOSE LOCK UNLOCK

Uso:       abrir <porta> [direção]
          fechar <porta> [direção]
         trancar <porta> [direção]
      destrancar <porta> [direção]

São comandos para abrir, fechar, trancar e destrancar aberturas, como portões e alçapões.

Exemplos:

  > abrir grade
  > trancar porta
  > destrancar porta sul
  > fechar portão

Veja também: ENTRAR, DEIXAR
```
