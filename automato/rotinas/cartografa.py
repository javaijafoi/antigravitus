# -*- coding: utf-8 -*-
"""cartografa.py - o modo batedor: levantar salas novas sem travar um combate.

Doutrina (registrada em state.json, perfil `batedor`):
  - mapeamento em invisibilidade;
  - evasao total de combate: fuga imediata no primeiro turno;
  - zero engajamento.

Regras duras deste arquivo, cada uma com o motivo:

  1. So anda por direcao que o comando `exits` ANUNCIOU. Sondar no escuro
     devolve "nao pode ir", que esta na lista FALHAS da guarda de repeticao:
     tres seguidas e a guarda mata a sessao.
  2. Fuga do wimpy ABORTA o dia naquela regiao. A fuga joga a personagem numa
     sala adjacente aleatoria, e num mundo onde 61% das salas tem texto
     identico a posicao nao se recupera por observacao.
  3. Fome ou sede ABORTAM a saida. O proprio servidor avisa: "Voce nao ira
     recuperar sua saude enquanto estiver com fome ou com sede". Sem isto,
     nao ha regeneracao e a reserva de vida e' falsa.
  4. Nenhuma magia de dano. A lista MAGIA_DANO existe para ser conferida.
  5. Termina sempre no Templo, com `save`.

O que ela grava: um fato JSONL por sala, em automato/runtime/cartografa.jsonl.
E' esse arquivo que o digestor consome depois. A rotina NAO reescreve o
mapa.json: separar observacao de consolidacao evita corromper o mapa curado.
"""
import collections
import json
import os
import re
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'camadas'))
from base import *          # noqa: F401,F403  (run, sala, andar, voltar_ao_templo, estourou, vida_frac, suprimentos)
import base
import config
import cuidar                # o cuidado continuo: comer, beber, armadura, invisibilidade

NOME = 'cartografa'
DESCRICAO = 'Levanta salas novas em invisibilidade, marca perigos e volta ao Templo sem lutar.'

DIR = {'norte': 'n', 'sul': 's', 'leste': 'e', 'oeste': 'w', 'cima': 'u', 'baixo': 'd'}
OPOSTO = {'n': 's', 's': 'n', 'e': 'w', 'w': 'e', 'u': 'd', 'd': 'u'}
RE_EXIT = re.compile(r'^\s*(Norte|Sul|Leste|Oeste|Cima|Baixo)\s*-\s*(.+?)\s*$', re.I)
RE_VITAIS = re.compile(r'(-?\d+)\s*hp\s+(-?\d+)\s*mn\s+(-?\d+)\s*mv')

# Salas homonimas ja' conhecidas no levantamento. Nelas o TITULO nao identifica
# a sala - so' a posicao identifica. Entrar nelas em excesso e' o que faz o
# robo girar em falso, entao elas tem teto proprio.
# Titulos que se repetem em salas diferentes: a identidade ali e' a posicao, nao
# o nome. A lista vive no config porque a mesclagem tambem precisa dela - para
# dar a essas salas um id proprio (`lb###`) em vez do `lv###` comum.
LABIRINTO = config.TITULOS_LABIRINTO

MAGIA_DANO = ('magic missile', 'burning hands', 'chill touch', 'lightning bolt',
              'shocking grasp', 'curse', 'poison', 'blindness')

CHECAR_CUIDADO_A_CADA = 12      # passos entre passadas do cuidar.py
RECONJURAR_A_CADA = 36          # passos entre re-conjuracoes (duracao nao medida)

PERIGO = ('massacra', 'louco', 'suicid', 'mataria', 'sem chance', 'muito superior',
          'arriscad', 'sorte')

FATOS = config.RUNTIME / 'cartografa.jsonl'


def sem_acento(texto):
    import unicodedata
    t = unicodedata.normalize('NFKD', (texto or '').lower())
    return ''.join(c for c in t if not unicodedata.combining(c))


def saidas(conhecidas=None, tentativas=3):
    """Todas as direcoes anunciadas, inclusive cima e baixo.

    O `pex` do base.py so' cobre norte/sul/leste/oeste; cima e baixo ficariam
    de fora de um mapa que precisa deles.

    Le ATE' TRES vezes e fica com a resposta MAIS COMPLETA. Medido em sessao
    real: 20 leituras de `exits` voltaram cortadas pela latencia - uma delas com
    UMA linha numa sala de SEIS portas. A rotina entao acreditava que havia uma
    porta, tentava direcoes que nao via, e ficava presa.

    `conhecidas` e' o que ja' se sabe daquela sala: se a resposta trouxer menos
    portas que isso, e' resposta cortada e vale insistir.
    """
    alvo = len(conhecidas or {})
    melhor = {}
    for _ in range(tentativas):
        t, _, _ = run('exits')
        achadas = {}
        for linha in t.split('\n'):
            m = RE_EXIT.match(linha.strip())
            if m:
                achadas[DIR[sem_acento(m.group(1)).strip()]] = m.group(2).strip()
        if len(achadas) > len(melhor):
            melhor = achadas
        if alvo and len(melhor) >= alvo:
            break                       # ja' alcancou o que se sabia: para
        if not alvo and achadas and 'saidas' in sem_acento(t):
            break                       # sem referencia: a primeira valida serve
        time.sleep(0.4)
    return melhor


def olhar():
    t, _, combate = run('look')
    return t, combate


RE_PROMPT = re.compile(r'^-?\d+\s*hp\s+-?\d+\s*mn\s+-?\d+\s*mv\s*>\s*')
RE_DIRETOES = re.compile(r'\[\s*sa[ií]das\s*:\s*([^\]]+)\]', re.I)


def direcoes_do_look(texto):
    """As saidas tambem aparecem entre colchetes no proprio `look`.

    Fonte INDEPENDENTE do comando `exits`, e de graca: o `look` ja' roda todo
    passo. Quando o `exits` volta truncado pela latencia - ja' voltou com uma
    linha numa sala de seis portas - e' aqui que as portas perdidas reaparecem.

    So' devolve direcoes (o nome do destino nao esta' nessa linha), por isso o
    valor e' '?': basta saber que a porta existe.
    """
    m = RE_DIRETOES.search(texto or '')
    if not m:
        return {}
    achadas = {}
    corpo = sem_acento(m.group(1))
    for pedaco in re.split(r'\s*,\s*|\s+e\s+', corpo):
        p = pedaco.strip()
        if p in DIR:
            achadas.setdefault(DIR[p], '?')
    return achadas
RE_CABECALHO = re.compile(r'^\[?\s*sa[ií]das\s*:?\s*$', re.I)
RE_DESTINO = re.compile(r'^(Norte|Sul|Leste|Oeste|Cima|Baixo)\s*[-:]', re.I)
# "Vida: {<<<<<>>>>>} 113 de 113", "Banco: ...", "Proximo nivel: ..." - rotulo
# curto seguido de dois-pontos. Nenhum titulo real tem essa forma.
RE_ROTULO = re.compile(r'^[a-z ]{3,24}:')

# Linhas de ficha que a latencia do driver pode entregar dentro do `look`.
# Conferido no levantamento: nenhum dos 209 titulos reais comeca com "voce".
NAO_TITULO = (
    'voce e ', 'voce esta', 'voce tem ', 'voce esteve', 'voce pesa', 'voce morreu',
    'voce nao', 'voce conhece', 'voce pode', 'pontos de atributos', 'ouro e equipamentos',
    'situacao atual', 'encarnacao', 'proximo nivel', 'alinhamento', 'classe de armadura',
    # ultima linha do score, que ja' vazou como titulo de sala num ensaio real
    'digite pontos', 'digite ', 'pontos de aventura',
)


def titulo(texto):
    """Titulo da sala, ignorando o que nao e' titulo.

    Duas fontes de sujeira, ambas medidas em ensaio real: a resposta do `exits`
    vazando para dentro do `look` (a primeira linha vira "Saídas:") e a resposta
    do `score` chegando atrasada (a primeira linha vira "Você é Grebolius...").
    Cada uma delas ja' fez a rotina encerrar sozinha. Devolve '?' quando nao ha
    titulo nenhum: quem chama deve reler.
    """
    for linha in (texto or '').split('\n'):
        limpa = RE_PROMPT.sub('', linha.strip()).strip()
        if not limpa or limpa.startswith('['):
            continue
        if RE_CABECALHO.match(limpa) or RE_DESTINO.match(limpa) or limpa.endswith(':'):
            continue
        baixo = sem_acento(limpa)
        if any(baixo.startswith(p) for p in NAO_TITULO):
            continue
        if RE_ROTULO.match(baixo):
            continue
        if re.fullmatch(r'[-=]{5,}.*', limpa):
            continue
        return limpa
    return '?'


def presencas(texto):
    """Linhas de criatura na sala, segundo as marcas do proprio servidor."""
    marcas = ('esta aqui', 'esta andando', 'zanza', 'rastej', 'espreita',
              'esta procurando', 'esta chorando', 'esta gritando', 'esta perdido',
              'questiona:', 'exclama:', 'esta dormindo', 'esta em pe aqui')
    achadas = []
    for linha in (texto or '').split('\n'):
        limpa = linha.strip()
        if limpa and any(m in sem_acento(limpa) for m in marcas):
            achadas.append(limpa)
    return achadas


def alvo_de(linha):
    """Palpite de palavra-chave para 'consider', a partir da linha de presenca."""
    palavras = [p for p in re.findall(r'[a-zà-ú]+', sem_acento(linha))
                if len(p) > 3 and p not in ('esta', 'aqui', 'andando', 'procurando',
                                            'chorando', 'gritando', 'perdido', 'dormindo')]
    return palavras[-1] if palavras else None


def avaliar_perigo(linha):
    """`consider` no alvo. NUNCA ataca: so' le' o veredito."""
    alvo = alvo_de(linha)
    if not alvo:
        return None
    t, _, _ = run('consider ' + alvo)
    baixo = sem_acento(t)
    if 'como?!' in baixo or 'nao esta vendo' in baixo or 'ninguem aqui' in baixo:
        return None
    for marca in PERIGO:
        if marca in baixo:
            return {'alvo': alvo, 'veredito': marca, 'linha': linha}
    return {'alvo': alvo, 'veredito': 'tranquilo', 'linha': linha}


def registrar(reg):
    reg = dict(reg)
    reg['dia'] = os.environ.get('MUD_DAY')
    reg['em'] = time.strftime('%Y-%m-%dT%H:%M:%S')
    try:
        FATOS.parent.mkdir(parents=True, exist_ok=True)
        with open(FATOS, 'a', encoding='utf-8') as fh:
            fh.write(json.dumps(reg, ensure_ascii=False) + '\n')
    except OSError as erro:
        print('[CARTOGRAFA] nao consegui gravar o fato: %s' % erro, flush=True)


def mana_atual():
    t, _, _ = run('score')
    m = RE_VITAIS.search(t)
    return int(m.group(2)) if m else None


def provisions_ok():
    """Provisao e magias: delegado ao cuidar.py.

    A rotina nao decide mais sobre fome, sede, armadura ou invisibilidade. Ela
    pergunta ao `cuidar` se esta' pronta para partir e se o estoque ainda da'.
    Comer, beber e vestir as magias sao cuidado continuo, nao preparacao; a
    viagem a cidade e' do `prepara.py`.
    """
    r = cuidar.cuidar(forcar_magias=True)
    if r['precisa_repor']:
        print('[CARTOGRAFA] estoque no fim (%s): rode prepara.py'
              % '; '.join(r['motivos']), flush=True)
        return False
    if not r['ok']:
        print('[CARTOGRAFA] nao estou pronta para partir: %s'
              % '; '.join(r['motivos']), flush=True)
        return False
    mana = mana_atual()
    if mana is not None and mana < config.MANA_MINIMA_BATEDOR:
        print('[CARTOGRAFA] mana %s abaixo do piso; nao parto' % mana, flush=True)
        return False
    print('[CARTOGRAFA] pronta: %s' % ', '.join(r['acoes']), flush=True)
    return True


def semear_do_levantamento(caminho=None):
    """Conhecimento das sessoes anteriores: o grafo e as portas por abrir.

    Sem isto cada execucao comeca do zero: redescobre o mesmo bolsao a partir do
    Templo e so' depois comeca a expandir. Das sete salas que a sessao do Round 2
    alcancou, seis ja' eram conhecidas - o trabalho foi quase todo redescobrir.

    Com o levantamento digerido em maos, a rotina ja' nasce sabendo onde estao as
    portas que ninguem abriu, e o BFS leva direto ate' a mais proxima atravessando
    terreno conhecido sem gastar passo.

    Devolve (saidas_vistas, fronteira); vazio se nao houver levantamento.
    """
    caminho = Path(caminho or config.DOC_MAPA_VIVO)
    if not caminho.is_file():
        return {}, set()
    try:
        dados = json.loads(caminho.read_text(encoding='utf-8'))
    except Exception as e:
        print('[CARTOGRAFA] levantamento ilegivel (%s): partindo sem semente' % e, flush=True)
        return {}, set()

    saidas_vistas, fronteira = {}, set()
    for sala in dados.get('rooms', []):
        titulo = sem_acento(sala.get('name'))
        if not titulo:
            continue
        saidas = {}
        for d, nome in (sala.get('exits_por_nome') or {}).items():
            if d.endswith('_id') or d not in OPOSTO:
                continue
            saidas[d] = sem_acento(nome)
        if saidas:
            # Titulos repetidos sao salas diferentes (homonimas); a rotina so'
            # consegue representar a uniao. O digerido separa por posicao depois.
            saidas_vistas.setdefault(titulo, {}).update(saidas)
        for d in (sala.get('fronteira') or {}):
            if d in OPOSTO:
                fronteira.add((titulo, d))
    return saidas_vistas, fronteira


def escolher(ex, visitadas, ultima, voltar, perigosas, bloqueadas, sala_atual):
    """Proxima direcao, entre os vizinhos DA SALA ATUAL. Regra de reserva.

    O criterio e' a ULTIMA visita, nao a contagem: contar produz ciclo fechado
    quando os contadores empatam.

    Isto sozinho NAO da' cobertura, e foi medido: com 25 salas alcancaveis, esta
    regra cobre 7 em 300 passos, porque ela so' olha os vizinhos daqui e nunca
    sente falta das portas deixadas por abrir noutro lugar. Quem cobre e' a
    navegacao por fronteira, em `primeiro_passo_para_fronteira`; esta funcao e'
    o ultimo recurso, quando nao ha' fronteira alcancavel.

    Uma tentativa anterior pos um BONUS de fronteira aqui dentro. Piorou (7 -> 4
    salas): o bonus premiava o vizinho que tem porta por abrir, entao a rotina
    pingava entre duas salas em vez de caminhar. Fronteira se resolve com
    CAMINHO, nao com peso local.
    """
    candidatos = []
    for d, nome in ex.items():
        if d not in OPOSTO:
            continue
        if (sala_atual, d) in bloqueadas:
            continue
        chave = sem_acento(nome)
        if chave in perigosas:
            continue
        n = visitadas.get(chave, 0)
        if n and chave in LABIRINTO and n >= config.MAX_VISITAS_LABIRINTO:
            continue
        peso = ultima.get(chave, -1)        # -1 = nunca vista: prioridade maxima
        if d == voltar:
            peso += 100000                  # voltar por onde veio e' o ultimo recurso
        candidatos.append((peso, d))
    if not candidatos:
        return None
    return min(candidatos)[1]


def porta_por_abrir(sala, ex, fronteira, bloqueadas):
    """A sala onde estou tem alguma saida que nunca tomei?"""
    for d in sorted(ex):
        if d in OPOSTO and (sala, d) in fronteira and (sala, d) not in bloqueadas:
            return d
    return None


def primeiro_passo_para_fronteira(sala, saidas_vistas, fronteira, bloqueadas, primeiros=None):
    """BFS no grafo ja' conhecido: primeiro passo ate' a fronteira mais proxima.

    E' isto que da' cobertura. A regra gulosa so' enxerga os vizinhos daqui; esta
    enxerga o mapa inteiro que ja' foi levantado e volta para terminar o servico
    inacabado. Devolve None se nenhuma fronteira for alcancavel pelo que se
    conhece - e ai' o chamador cai na regra de reserva.

    `primeiros` sao as portas CONFIRMADAS AO VIVO nesta sala. O primeiro passo
    tem que sair delas: o caminho depois pode usar o levantamento, mas tentar
    como primeiro passo uma porta que so' a semente conhece gasta o passo e marca
    bloqueio falso - medido, a rotina tentou `s` numa sala que so' tem cima e
    leste.
    """
    alvos = {s for (s, d) in fronteira if (s, d) not in bloqueadas}
    if not alvos:
        return None
    vistos = {sala}
    fila = collections.deque([(sala, None)])
    while fila:
        atual, primeiro = fila.popleft()
        for d, alvo in sorted(saidas_vistas.get(atual, {}).items()):
            if d not in OPOSTO or alvo in vistos or (atual, d) in bloqueadas:
                continue
            if atual == sala and primeiros is not None and d not in primeiros:
                continue                # porta nao confirmada agora: nao arrisco
            passo = d if primeiro is None else primeiro
            if alvo in alvos:
                return passo
            vistos.add(alvo)
            fila.append((alvo, passo))
    return None


def andar_mapeando(semente=None):
    visitadas = {}
    ultima = {}                 # titulo -> passo da ultima visita (o criterio de escolha)
    saidas_vistas = {}          # titulo -> saidas ja' observadas naquela sala
    vistos = set()              # (sala, direcao) ja' vistos
    fronteira = set()           # (sala, direcao) vistos e NUNCA tomados
    if semente:
        # Copia: a semente nao pode ser mutada entre execucoes.
        saidas_vistas = {k: dict(v) for k, v in semente[0].items()}
        fronteira = set(semente[1])
        vistos = {(s, d) for s in saidas_vistas for d in saidas_vistas[s]} - fronteira
    # GRAFO DE NAVEGACAO: comeca igual a' semente, mas quando a rotina PISA numa
    # sala, o que o servidor mostra SUBSTITUI o que a semente dizia. Somar nao
    # serve para navegar: a semente acha que "A Loja de Animais" continua ao
    # norte, o mundo mostra que ela e' beco, e a uniao mantem o norte velho - o
    # BFS segue roteando por uma porta que nao existe e a rotina pinga entre duas
    # salas. Para o que ja' foi visto, vale o que foi visto.
    grafo_nav = {k: dict(v) for k, v in (semente[0] if semente else {}).items()}
    perigosas = set()
    bloqueadas = set()          # (sala, direcao) que o jogo recusou
    avaliados = {}
    passos_sem_nova = 0
    voltar = None
    tentou = None
    anterior = None
    passos = 0
    inicio = time.time()

    while not estourou(config.LIMITE_TEMPO_BATEDOR):
        passos += 1
        # `olhar()` PRIMEIRO: o titulo diz de qual sala se trata, e com isso o
        # `saidas()` ja' sabe quantas portas esperar e insiste se vier cortado.
        texto, combate = olhar()

        if combate:
            print('[CARTOGRAFA] atacada: recuando sem revidar', flush=True)
            registrar({'tipo': 'ataque', 'sala': titulo(texto)})
            run('recall')
            return False

        if vida_frac() < config.VIDA_MINIMA_BATEDOR:
            print('[CARTOGRAFA] vida no piso: encerrando', flush=True)
            return False

        nome = titulo(texto)
        if nome == '?':
            # Sem titulo legivel: reler uma vez antes de concluir qualquer coisa.
            time.sleep(0.4)
            texto2, _ = olhar()
            texto = texto + '\n' + texto2
            nome = titulo(texto)
        chave = sem_acento(nome)
        # PORTAS DE AGORA: so' o que o SERVIDOR acabou de confirmar - o `exits`
        # (com nome do destino) e a linha de colchetes do proprio `look` (so'
        # direcoes, mas vem sempre). O retry mira o que a linha de colchetes
        # anuncia, que e' fonte viva.
        do_look = direcoes_do_look(texto)
        ex = saidas(conhecidas=do_look)
        # ACRESCENTA o que a linha de colchetes anuncia, NUNCA sobrescreve.
        #
        # `do_look` so' traz direcoes - a linha "[ Saídas: norte, leste ]" nao
        # tem nome de destino - entao o valor dele e' '?'. Com `ex.update(do_look)`
        # o nome real virava '?': "a entrada da estalagem javali roncador" virava
        # '?', o BFS ia procurar um no' chamado '?' que nao existe no grafo e
        # devolvia None. Foi ESTA a causa de o BFS nunca engatar, e explica o
        # experimento que me travou dois rounds: grafo vivo e grafo pristino com
        # MESMO tamanho, MESMOS pares de fronteira e MESMAS saidas - porque os
        # TAMANHOS batiam e so' os VALORES estavam envenenados.
        for direcao, destino in do_look.items():
            ex.setdefault(direcao, destino)

        # CHEGADA CONFERIDA. O `andar` do base.py so' reconhece a recusa como
        # "nao pode ir"; qualquer outra - "O guarda te humilha e nao deixa voce
        # passar." - passava por sucesso e o robo girava na mesma sala ate' o
        # detector de perdida. Aqui a prova e' a sala ter mudado.
        recusado = bool(tentou) and anterior is not None and chave == anterior
        if recusado:
            bloqueadas.add((anterior, tentou))
            # Porta recusada sai da fronteira: ela NAO e' mais um alvo. Sem isto
            # o BFS mandava a rotina de volta para a mesma sala para tentar a
            # mesma porta - medido, ela pingou Guilda dos Paladinos <-> Estalagem
            # ate' o detector de perdida, porque a porta `e` da Guilda (a unica
            # de fronteira ali) e' barrada pelo guarda.
            fronteira.discard((anterior, tentou))
            registrar({'tipo': 'bloqueio', 'sala': nome, 'direcao': tentou})
            print('[CARTOGRAFA] %s nao saiu de %r: direcao bloqueada aqui'
                  % (tentou, nome), flush=True)
            voltar = None
        anterior = chave

        novo = chave not in visitadas
        visitadas[chave] = visitadas.get(chave, 0) + 1
        ultima[chave] = passos
        passos_sem_nova = 0 if (novo and not recusado) else passos_sem_nova + 1

        # CONHECIMENTO ACUMULADO (levantamento + historico): serve para PLANEJAR
        # caminho pelo BFS, nunca para escolher a porta de agora. Tentar porta
        # que a sala nao tem gasta passo e marca bloqueio FALSO - medido: a
        # rotina ficou 5 passos parada tentando as saidas que a semente atribuia
        # a "A Sala de Doacoes de Midgaard" e que na verdade eram do Templo.
        # NORMALIZAR OS DESTINOS. `saidas()` devolve o nome como o servidor
        # escreve ("A Entrada da Estalagem Javali Roncador"); todo o resto do
        # grafo - a semente, `fronteira`, `alvos` - usa a forma normalizada
        # ("a entrada da estalagem javali roncador").
        #
        # Sem normalizar aqui, o BFS sai da sala, procura o no' de destino pelo
        # nome CRU, nao acha, e devolve None. Era ESTA a causa de o BFS nunca
        # engatar, e explica o experimento que me travou dois rounds: grafo vivo
        # e grafo pristino com MESMO tamanho, MESMOS pares de fronteira e
        # MESMAS saidas davam resultados diferentes - porque so' o vivo tinha os
        # destinos crus.
        norm_ex = {d: sem_acento(n) for d, n in ex.items()}
        conhecidas = dict(saidas_vistas.get(chave, {}))
        conhecidas.update(norm_ex)
        saidas_vistas[chave] = conhecidas
        grafo_nav[chave] = dict(norm_ex)    # para NAVEGAR, vale o que se viu
        if len(ex) < len(conhecidas):
            registrar({'tipo': 'exits_curto', 'sala': nome, 'passo': passos,
                       'vivas': sorted(ex), 'conhecidas': sorted(conhecidas)})

        # FRONTEIRA MORTA: par de fronteira cuja direcao esta sala NAO tem.
        #
        # Ninguem descarta esse par, porque a rotina nunca "toma" a direcao -
        # nao pode, ela nao existe. O BFS entao segue mirando essa sala e volta
        # para ela eternamente: medido, a rotina pingou Rua Principal <-> Loja
        # de Animais por 14 passos ate' o detector de perdida encerrar o ensaio.
        # Estar aqui e ver as portas reais e' prova suficiente para descartar.
        for par in [p for p in fronteira if p[0] == chave and p[1] not in ex]:
            fronteira.discard(par)
            registrar({'tipo': 'fronteira_morta', 'sala': nome, 'passo': passos,
                       'direcao': par[1], 'portas_reais': sorted(ex)})
        # FRONTEIRA: porta conhecida e nunca tomada. Registra do CONHECIMENTO
        # (levantamento + historico), nao so' do que a leitura viva trouxe: e' o
        # que faz o BFS enxergar o servico inacabado das sessoes anteriores.
        for dd in conhecidas:
            if dd in OPOSTO and (chave, dd) not in vistos:
                vistos.add((chave, dd))
                fronteira.add((chave, dd))

        # `consider` uma vez por sala: repetir na mesma sala so' gasta comando.
        perigos = avaliados.get(chave)
        if perigos is None:
            perigos = []
            for linha in presencas(texto)[:2]:
                r = avaliar_perigo(linha)
                if r and r['veredito'] != 'tranquilo':
                    perigos.append(r)
            avaliados[chave] = perigos

        registrar({'tipo': 'sala', 'sala': nome, 'homonima': chave in LABIRINTO,
                   'saidas': ex, 'perigos': perigos, 'visita': visitadas[chave],
                   'passo': passos})

        if perigos:
            # Sala com presenca hostil: sai da rota e recua. Continuar aqui
            # seria mapear com o corpo, e o corpo e' o que nao se pode repor.
            if chave not in perigosas:
                print('[CARTOGRAFA] perigo em %r: %s -> fora da rota'
                      % (nome, perigos[0]['veredito']), flush=True)
            perigosas.add(chave)
            if voltar:
                run(voltar)
                voltar, tentou = None, None
                continue
            run('recall')
            return False

        if passos_sem_nova >= config.PASSOS_SEM_SALA_NOVA:
            print('[CARTOGRAFA] %d passos sem sala nova: perdida, voltando'
                  % passos_sem_nova, flush=True)
            registrar({'tipo': 'perdida', 'sala': nome, 'passos': passos})
            run('recall')
            return False

        # Cuidado em campo: come da bolsa, bebe do cantil e re-conjura as magias
        # se a validade venceu. Volta so' se o ESTOQUE acabar - fome nao e' motivo.
        if passos % CHECAR_CUIDADO_A_CADA == 0:
            c = cuidar.cuidar(forcar_magias=(passos % RECONJURAR_A_CADA == 0))
            registrar({'tipo': 'cuidado', 'sala': nome, 'passo': passos,
                       'acoes': c['acoes'], 'motivos': c['motivos']})
            if c['precisa_repor']:
                print('[CARTOGRAFA] estoque acabou em campo: voltando para repor', flush=True)
                registrar({'tipo': 'provisao_acabou', 'sala': nome, 'passo': passos,
                           'motivos': c['motivos']})
                run('recall')
                return False
            if not c['magias']['invisibilidade']:
                print('[CARTOGRAFA] sem invisibilidade confirmada: recuando', flush=True)
                registrar({'tipo': 'sem_invisibilidade', 'sala': nome, 'passo': passos,
                           'magias': c['magias']})
                run('recall')
                return False

        # COMO ESCOLHER A DIRECAO, em tres frentes decrescentes de prioridade:
        #   1. a sala onde estou tem porta que nunca abri -> abro agora;
        #   2. senao, caminho ate' a fronteira mais proxima pelo mapa ja' conhecido;
        #   3. senao, regra gulosa entre os vizinhos.
        d = porta_por_abrir(chave, ex, fronteira, bloqueadas)
        via = 'porta'
        if d is None:
            # O BFS roda sobre a copia PRISTINA da semente.
            #
            # NAVEGACAO: `grafo_nav` (semente corrigida pelo que ja' se viu) +
            # `fronteira` (pares por abrir, ja' sem os que o jogo recusou).
            #
            # `ex` = portas CONFIRMADAS AO VIVO nesta sala. O BFS planeja pelo
            # mapa inteiro, mas o PRIMEIRO passo tem que sair daqui.
            #
            # Sem esta restricao o BFS roteia por uma porta que a semente acha
            # que existe e o mundo nao tem: medido, ele mandou a rotina de Rua
            # Principal para A Loja de Animais repetidamente porque o
            # levantamento acha que a Loja continua adiante, e ao vivo ela e' um
            # beco so' com `w` de volta. Resultado: 14 passos pingando entre as
            # duas ate' o detector de perdida.
            #
            # (Numa tentativa anterior eu removi esta restricao porque "quebrou
            # o planejamento". O que quebrou foi outra coisa: eu rodava o ensaio
            # no MESMO bloco da edicao, e as ferramentas correm em paralelo - a
            # sessao usava o codigo velho. Licao anotada no README.)
            d = primeiro_passo_para_fronteira(chave, grafo_nav, fronteira, bloqueadas, ex)
            if d is None:
                # Nenhum caminho COMECA por porta confirmada ao vivo. Antes de
                # desistir, aceita um caminho que comece por porta do
                # levantamento: caminhar para perto da fronteira e' melhor que
                # girar no bolsao. Medido: com a restricao sozinha, `via=bfs` caiu
                # a ZERO e a rotina voltou a pingar Praca <-> Estalagem <-> Correios.
                #
                # O risco de rotear por porta que o mundo nao tem - o caso da Loja
                # de Animais - esta' coberto por `grafo_nav`: assim que a rotina
                # pisa numa sala, o que o servidor mostra SUBSTITUI a semente
                # naquele no', e o BFS deixa de achar a passagem inexistente.
                d = primeiro_passo_para_fronteira(chave, grafo_nav, fronteira, bloqueadas)
            via = 'bfs'
            if d is None and passos <= 2:
                # Argumentos da chamada que falhou, para nao ter que adivinhar.
                #
                # PROXIMO PASSO (Round 6): o que falta aqui e' um DIFF entre
                # `grafo_nav` e uma semente recem-carregada NO MESMO processo:
                # ao vivo, com n_bloqueadas=0, n_fronteira=23 e as mesmas saidas,
                # o BFS devolve None - e a reproducao com a semente limpa devolve
                # 'e'. Os campos abaixo ja' mostraram que a diferenca NAO esta' no
                # tamanho do grafo, nem na fronteira, nem nos bloqueios, nem nas
                # saidas da sala atual. Falta ver o CONTEUDO no a no' de destino.
                registrar({'tipo': 'bfs_args', 'sala': nome, 'passo': passos,
                           'chave': chave,
                           'n_bloqueadas': len(bloqueadas),
                           'bloqueadas': sorted('%s|%s' % par for par in bloqueadas)[:25],
                           'n_fronteira': len(fronteira),
                           'saidas_da_sala': sorted(grafo_nav.get(chave, {})),
                           'destinos_da_sala': sorted(grafo_nav.get(chave, {}).values()),
                           'n_nos': len(grafo_nav),
                           'alvos': sorted({s for (s, _) in fronteira})[:20]})
        if d is None:
            d = escolher(ex, visitadas, ultima, voltar, perigosas, bloqueadas, chave)
            via = 'gulosa'
        if d is None:
            print('[CARTOGRAFA] sem saida util em %r: encerrando' % nome, flush=True)
            break

        # INSTRUMENTACAO: por que esta direcao, e o que foi descartado. Sem isto
        # nao ha' como avaliar a politica - replay sobre os fatos NAO serve, o
        # grafo gravado e' parcial (so' tem saidas de salas que foram correntes).
        registrar({'tipo': 'decisao', 'sala': nome, 'passo': passos, 'escolhida': d, 'via': via,
                   'fronteira_total': len(fronteira),
                   'fronteira_aqui': sorted(dd for dd in ex if (chave, dd) in fronteira),
                   'candidatos': sorted([dd, ultima.get(sem_acento(nome2), -1)]
                                        for dd, nome2 in ex.items() if dd in OPOSTO)})

        fronteira.discard((chave, d))       # esta porta deixou de estar por abrir
        tentou = d
        run(d)                  # a chegada e' conferida no topo da proxima volta
        voltar = OPOSTO[d]

    print('[CARTOGRAFA] fim: %d passos em %ds' % (passos, int(time.time() - inicio)), flush=True)
    return True


def executar() -> bool:
    """Cuida de si, mapeia, e volta.

    Nao existe mais um passo separado de "equipar magias": o cuidado e' do
    cuidar.py e ja' foi feito dentro das provisoes. Duplicar aqui era o que
    deixava a rotina com duas verdades sobre fome, sede e invisibilidade.
    """
    run('wake')
    run('stand')
    print('[CARTOGRAFA] inicio', flush=True)

    if not provisions_ok():
        voltar_ao_templo()
        return False

    semente = None
    if config.SEMEAR_LEVANTAMENTO:
        sv, fr = semear_do_levantamento()
        if fr:
            print('[CARTOGRAFA] semeada: %d salas conhecidas, %d portas por abrir'
                  % (len(sv), len(fr)), flush=True)
            registrar({'tipo': 'semente', 'salas': len(sv), 'portas_por_abrir': len(fr)})
            semente = (sv, fr)
        else:
            print('[CARTOGRAFA] sem levantamento para semear: comeco do zero', flush=True)

    ok = andar_mapeando(semente)
    voltar_ao_templo()
    run('save')
    print('[CARTOGRAFA] encerrada no Templo com save (mapeamento: %s)'
          % ('completo' if ok else 'interrompido'), flush=True)
    return ok


def main():
    ok = executar()
    print('[CARTOGRAFA] resultado:', 'ok' if ok else 'interrompida')
    return 0 if ok else 1


if __name__ == '__main__':
    import sys
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    sys.exit(main())
