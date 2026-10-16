# -*- coding: utf-8 -*-
"""digerir_mapa.py - reconstroi o mapa do mundo a partir dos registros, sem logar.

Le os transcript_*.jsonl (registro fiel das sessoes ja jogadas) e monta um mapa
com identidade de sala vinda da POSICAO NO GRAFO, nao do texto.

Por que nao do texto: o bosque e o milharal sao labirintos de salas
textualmente identicas. Mover 'e' numa sala de "Num Bosque Iluminado" devolve
exatamente o mesmo titulo, a mesma descricao e as mesmas saidas - 1549
movimentos observados assim. Nenhum fingerprint separa essas salas. O que
separa e a sequencia de movimentos: se voce andou, voce saiu de onde estava.

O texto ainda serve para duas coisas: achar um candidato quando nao ha aresta
conhecida, e conferir a chegada. Nunca para decidir sozinho.

Regras de identidade:
  1. se ja existe aresta (atual, direcao), ela manda - e o caminho ja andado;
  2. senao, se existe UM candidato com a mesma assinatura cuja volta
     (candidato, oposta) aponta para a sala atual, e ele;
  3. senao, se existe um unico candidato com a mesma assinatura, e ele;
  4. senao - varias salas identicas e nenhuma prova - nasce uma sala nova.
     Em labirinto isso e o certo: fundir seria inventar caminho.

Nada aqui abre socket, le arquivo de jogo ou depende do daemon no ar. Uso:
    python automato/acoes/digerir_mapa.py
    python automato/acoes/digerir_mapa.py --mostrar-ruido
    python automato/acoes/digerir_mapa.py --validar-midgaard

Le os transcripts das sessoes vivas, em automato/runtime/. Mora aqui, e nao em
scripts/local/, porque aquela pasta esta no .gitignore: ferramenta que produz o
dado do capitulo precisa ser versionada.
"""
import argparse
import collections
import glob
import hashlib
import json
import re
import sys
from pathlib import Path
from types import SimpleNamespace

ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT / 'scripts'))
from expedition.observations import (  # noqa: E402
    DIRECTIONS, parse_room, named_exits, norm, plain,
)

CFG = SimpleNamespace(item_catalog=[], known_entities=[])
PROMPT = re.compile(r'(-?\d+)\s*hp\s+(-?\d+)\s*mn\s+(-?\d+)\s*mv\s*>', re.I)
DANO = re.compile(r'\[\s*-?\d+\s*\]')
SAIDAS = re.compile(r'\[\s*Sa[ií]das\s*:', re.I)

# Tokens de movimento ACEITOS pelo servidor. Medido nos proprios transcripts:
#   'e' 3985x -> sala   | 'w' 1469x -> sala        (movimento real)
#   'l'    2x -> sala   | mas a sala e a MESMA: 'l' e o comando look
#   'o'    2x -> "Ordenar quem e o que?"           'o' e o comando order
#   'oeste' 2x -> "Como?!?"                        palavra em portugues e recusada
# Por isso 'l' e 'o' NAO entram aqui, e as palavras em portugues tambem nao.
# O mapa curado (data/heroes/grebolius/mapa.json) usa 'l'/'o' como CHAVE de dado;
# isso e convencao de arquivo, nunca comando a enviar.
MOVE = {'n': 'n', 's': 's', 'e': 'e', 'w': 'w', 'u': 'u', 'd': 'd',
        'north': 'n', 'south': 's', 'east': 'e', 'west': 'w',
        'up': 'u', 'down': 'd'}
OPP = {'n': 's', 's': 'n', 'e': 'w', 'w': 'e', 'u': 'd', 'd': 'u'}

# Comandos que mudam de sala sem serem passo: recall, fuga, portais.
TELEPORTE = {'recall', 'flee', 'fugir', 'enter', 'entrar', 'portal', 'sair', 'quit'}
# Comandos cuja resposta pode trazer uma sala que ainda esta valendo.
POSICIONA = set(MOVE) | TELEPORTE | {'look', 'exits'}

# Recusa de movimento. Se aparece no texto, o passo NAO aconteceu mesmo que a
# sala venha junto - por isso estas frases curtas e especificas.
RECUSA = ('nao pode ir por ai', 'nao da! voce esta muito ocupado, lutando',
          'voce esta muito ocupado, lutando', 'voce esta muito relaxado',
          'esta escuro', 'voce nao consegue sair')

# Linhas que o servidor injeta no meio da descricao. Todas foram observadas em
# varias salas diferentes, prova de que nao descrevem a sala.
TRANSIENTES = (
    'voce esta com muita fome', 'voce esta com muita sede',
    'voce esta com fome', 'voce esta com sede',
    'voce esta morrendo de fome', 'voce esta morrendo de sede',
    'voce solta um gemido agudo', 'sua garganta parece secar',
    'voce sente que esta muito fraco e tenta fugir',
    'voce nao pode ir por ai', 'nao da! voce esta muito ocupado, lutando',
    'voce esta muito ocupado, lutando',
)


def eh_ruido(linha):
    if PROMPT.search(linha) or DANO.search(linha):
        return True
    v = norm(linha).strip()
    if v in ('saidas:', 'saidas'):
        return True
    return any(t in v for t in TRANSIENTES)


def assinatura(texto, titulo):
    """(codigos de saida, descricao limpa) ou (None, None) se nao ha sala."""
    linhas = [s.strip() for s in plain(texto).split('\n') if s.strip()]
    idx = next((i for i, s in enumerate(linhas) if SAIDAS.search(s)), None)
    if idx is None:
        return None, None
    codigos = tuple(sorted({c for w, c in DIRECTIONS.items()
                            if re.search(r'\b' + w + r'\b', norm(linhas[idx]))}))
    corpo = linhas[:idx]
    for i, s in enumerate(corpo):
        if s == titulo:
            corpo = corpo[i + 1:]
            break
    return codigos, sorted({s for s in corpo if not eh_ruido(s)})


def sig_hash(titulo, codigos, descricao):
    bruto = '%s|%s|%s' % (norm(titulo), ','.join(codigos), '\n'.join(norm(s) for s in descricao))
    return hashlib.sha256(bruto.encode()).hexdigest()[:20]


def eventos(path):
    with open(path, encoding='utf-8', errors='replace') as fh:
        for linha in fh:
            try:
                d = json.loads(linha)
            except Exception:
                continue
            if d.get('kind') == 'command':
                yield (d.get('cmd') or '').strip().lower(), d.get('text') or ''


class Mapa:
    def __init__(self):
        self.nos = {}                                    # id -> dados
        self.por_sig = collections.defaultdict(list)     # assinatura -> [ids]
        self.arestas = {}                                # (id, dir) -> id  VERIFICADAS
        self.declaradas = collections.defaultdict(collections.Counter)
        self.ruido = collections.Counter()
        self.criados_ambiguos = 0
        self.aliases = 0
        self.recusas = self.parados = self.saltos = 0

    def novo(self, sig, titulo, descricao, codigos):
        nid = 'r%04d' % (len(self.nos) + 1)
        self.nos[nid] = {'id': nid, 'sig': sig, 'sigs': {sig},
                         'titulos': collections.Counter([titulo]),
                         'descricao': ' '.join(descricao)[:300], 'saidas': codigos,
                         'visitas': 0, 'ambiguo': False,
                         'npcs': collections.Counter()}
        self.por_sig[sig].append(nid)
        return nid

    def alias(self, nid, sig):
        """Descricao instavel na mesma posicao: guarda a variacao sem criar sala."""
        if sig in self.nos[nid]['sigs']:
            return
        self.nos[nid]['sigs'].add(sig)
        self.por_sig[sig].append(nid)
        self.aliases += 1

    def candidato(self, sig, origem, d):
        cands = [n for n in self.por_sig.get(sig, []) if n != origem]
        if not cands:
            return None
        for c in cands:                       # prova de ida e volta
            if self.arestas.get((c, OPP[d])) == origem:
                return c
        if len(cands) == 1:
            return cands[0]
        return None

    def melhor(self, sig):
        cands = self.por_sig.get(sig)
        if not cands:
            return None
        if len(cands) == 1:
            return cands[0]
        return max(cands, key=lambda n: self.nos[n]['visitas'])

    def localizar(self, sig, titulo, descricao, codigos):
        """Onde o heroi esta, e se da para confiar nessa posicao.

        Confiavel = assinatura que so existe numa sala. Se varias salas tem o
        mesmo texto, a posicao e um chute; e chute nao pode virar aresta.
        """
        cands = self.por_sig.get(sig) or []
        if len(cands) == 1:
            return cands[0], True
        if cands:
            return max(cands, key=lambda n: self.nos[n]['visitas']), False
        return self.novo(sig, titulo, descricao, codigos), True

    def andar(self, atual, d, titulo, descricao, codigos, sig, confiavel):
        if atual is None:
            alvo, conf = self.localizar(sig, titulo, descricao, codigos)
            return alvo, False, conf
        alvo = self.arestas.get((atual, d))
        if alvo is not None:
            return alvo, False, True
        alvo = self.candidato(sig, atual, d)
        if alvo is not None:
            if confiavel:
                self.arestas[(atual, d)] = alvo
                self.arestas.setdefault((alvo, OPP[d]), atual)
            return alvo, True, True
        if not confiavel:
            # Origem incerta: reaproveita uma sala conhecida e NAO grava aresta.
            return self.melhor(sig) or self.novo(sig, titulo, descricao, codigos), False, False
        alvo = self.novo(sig, titulo, descricao, codigos)
        self.nos[alvo]['ambiguo'] = len(self.por_sig[sig]) > 1
        self.criados_ambiguos += 1
        self.arestas[(atual, d)] = alvo
        self.arestas.setdefault((alvo, OPP[d]), atual)
        return alvo, True, True

    def resolve_salto(self, atual, titulo, descricao, codigos, sig):
        """sala mudou sem comando de movimento: recall, fuga, portal.

        Sem passo nao ha posicao a seguir, entao o texto volta a ser a unica
        prova. Devolve tambem se a posicao e confiavel.
        """
        return self.localizar(sig, titulo, descricao, codigos)


def digerir(arquivos):
    mapa = Mapa()
    dias, sessoes, comandos, looks, looks_falhos = set(), 0, 0, 0, 0
    movimentos = movimentos_recusados = movimentos_sem_sala = 0
    seguiram_aresta = abriram_aresta = 0
    trocas_sem_movimento = ignoradas = aliases = 0

    for path in arquivos:
        m = re.search(r'dia(\d+)', Path(path).name)
        if m:
            dias.add(int(m.group(1)))
        sessoes += 1
        atual = None
        confiavel = False
        for cmd, texto in eventos(path):
            comandos += 1
            base = cmd.split()[0] if cmd else ''
            d = MOVE.get(base)
            room = parse_room(texto, CFG) if texto else None
            recusado = any(t in norm(texto) for t in RECUSA)

            if base == 'look':
                looks += 1
                if room is None:
                    looks_falhos += 1

            if room is not None:
                # Comando que nao posiciona: uma sala no texto e sobra de buffer
                # do servidor, nao a sala onde o heroi esta. Descartar.
                if not d and base not in POSICIONA:
                    ignoradas += 1
                    continue
                codigos, descricao = assinatura(texto, room.title)
                if descricao is None:
                    continue
                linhas = [s.strip() for s in plain(texto).split('\n') if s.strip()]
                idx = next((i for i, s in enumerate(linhas) if SAIDAS.search(s)), None)
                if idx is not None:
                    for s in linhas[:idx]:
                        if eh_ruido(s):
                            mapa.ruido[s] += 1
                sig = sig_hash(room.title, codigos, descricao)

                if d:
                    movimentos += 1
                    if recusado:
                        movimentos_recusados += 1
                        continue                      # nao saiu do lugar
                    alvo, nova, confiavel = mapa.andar(
                        atual, d, room.title, descricao, codigos, sig, confiavel)
                    mapa.nos[alvo]['visitas'] += 1
                    if nova:
                        abriram_aresta += 1
                    else:
                        seguiram_aresta += 1
                    atual = alvo
                elif atual is None:
                    atual, confiavel = mapa.localizar(sig, room.title, descricao, codigos)
                    mapa.nos[atual]['visitas'] += 1
                elif sig in mapa.nos[atual]['sigs']:
                    mapa.nos[atual]['visitas'] += 1
                elif base in TELEPORTE:
                    trocas_sem_movimento += 1
                    atual, confiavel = mapa.resolve_salto(
                        atual, room.title, descricao, codigos, sig)
                    mapa.nos[atual]['visitas'] += 1
                else:
                    # Sem comando de passo e sem teleporte. Se o titulo e o mesmo,
                    # a descricao apenas variou - apelido, nunca sala nova. Se o
                    # titulo mudou, o heroi saiu dalgum jeito: resolver de verdade.
                    titulo_atual = mapa.nos[atual]['titulos'].most_common(1)[0][0]
                    if norm(room.title) == norm(titulo_atual):
                        mapa.alias(atual, sig)
                        aliases += 1
                        mapa.nos[atual]['visitas'] += 1
                    else:
                        trocas_sem_movimento += 1
                        atual, confiavel = mapa.resolve_salto(
                            atual, room.title, descricao, codigos, sig)
                        mapa.nos[atual]['visitas'] += 1
            elif d:
                movimentos += 1
                movimentos_sem_sala += 1

            if base == 'exits' and atual is not None:
                for dd, nome in named_exits(texto).items():
                    if nome.strip():
                        mapa.declaradas[(atual, dd)][nome.strip()] += 1

            # NPC: `consider X` ACEITO prova que X e' criatura. O nome do alvo nao
            # vem na resposta - ela traz "Você  Oponente" e a tabela comparativa -
            # entao o nome sai do proprio comando.
            #
            # Foi `consider` que separou criatura de objeto, porque a frase do
            # `look` NAO separa: "Um brilho punhal de novato esta' aqui, procurando
            # alguem para apunhalar" tem exatamente a forma de "Um cachorro esta'
            # procurando no lixo alguma coisa para comer". Objeto o jogo recusa com
            # "Comparar sua forca com a de quem?" - 382 recusas contra 92 aceites.
            if base == 'consider' and atual is not None:
                partes = cmd.split(None, 1)
                if len(partes) > 1:
                    alvo_mob = partes[1].strip().lower()
                    if alvo_mob and 'oponente' in norm(texto):
                        mapa.nos[atual]['npcs'][alvo_mob] += 1

    return mapa, dict(dias=dias, sessoes=sessoes, comandos=comandos, looks=looks,
                      looks_falhos=looks_falhos, movimentos=movimentos,
                      seguiram_aresta=seguiram_aresta, abriram_aresta=abriram_aresta,
                      movimentos_recusados=movimentos_recusados,
                      movimentos_sem_sala=movimentos_sem_sala,
                      trocas_sem_movimento=trocas_sem_movimento,
                      ignoradas=ignoradas, aliases=aliases)


def construir(mapa):
    por_titulo = collections.defaultdict(list)
    for nid, dado in mapa.nos.items():
        por_titulo[norm(dado['titulos'].most_common(1)[0][0])].append(nid)

    ambiguos = 0
    salas = []
    for nid, dado in mapa.nos.items():
        saidas, por_nome, fronteira = {}, {}, {}
        for (a, d), b in mapa.arestas.items():
            if a == nid and b != nid:
                saidas[d] = b
        for (a, d), cont in mapa.declaradas.items():
            if a != nid:
                continue
            nome = cont.most_common(1)[0][0]
            conf = mapa.arestas.get((nid, d))
            if conf is not None:
                por_nome[d] = nome
                por_nome[d + '_id'] = conf
                continue
            cand = por_titulo.get(norm(nome), [])
            por_nome[d] = nome
            if len(cand) == 1:
                por_nome[d + '_id'] = cand[0]
            elif len(cand) > 1:
                por_nome[d + '_ambiguo'] = len(cand)
                ambiguos += 1
            else:
                fronteira[d] = nome
        salas.append({
            'id': nid, 'name': dado['titulos'].most_common(1)[0][0],
            'aliases': [t for t, _ in dado['titulos'].most_common()[1:]],
            'sig': dado['sig'], 'visits': dado['visitas'],
            'identidade_ambigua': dado['ambiguo'],
            'exits': dict(sorted(saidas.items())),
            'exits_por_nome': por_nome, 'fronteira': fronteira,
            'npcs': [n for n, _ in dado['npcs'].most_common()],
            'description': dado['descricao'],
        })
    salas.sort(key=lambda s: (-s['visits'], s['name']))
    return salas, ambiguos


def classes_identicas(mapa):
    """Grupos de salas que o texto NAO distingue - so a posicao separa."""
    grupos = [(sig, ids) for sig, ids in mapa.por_sig.items() if len(ids) > 1]
    grupos.sort(key=lambda kv: -len(kv[1]))
    return grupos


def compativel(a, b):
    """Nomes do mapa curado e do jogo divergem em detalhe; compara com tolerancia.

    O curador humano desambigua nomes repetidos com sufixo entre parenteses
    ("O Grande Campo (Sul)") porque o jogo da o mesmo titulo a salas diferentes.
    O digest separa essas salas por posicao, sem precisar do sufixo.
    """
    def limpa(v):
        return re.sub(r'\s*\([^)]*\)\s*', ' ', norm(v)).strip()
    a, b = limpa(a), limpa(b)
    if not a or not b:
        return False
    if a == b or a in b or b in a:
        return True
    import difflib
    return difflib.SequenceMatcher(None, a, b).ratio() >= .72


def validar_midgaard(mapa, salas):
    """Confere o mapa digerido contra o mapa curado a mao."""
    alvo = ROOT / 'data/heroes/grebolius/mapa.json'
    if not alvo.is_file():
        alvo = ROOT / 'data/heroes/antigravitus/mapa.json'
    if not alvo.is_file():
        return None
    curado = json.loads(alvo.read_text(encoding='utf-8'))
    nome_por_id = {r['id']: r['name'] for r in curado['rooms']}
    digerido = collections.defaultdict(list)
    for s in salas:
        digerido[norm(s['name'])].append(s)

    print('=== VALIDACAO CONTRA O MAPA CURADO A MAO (%s) ===' % alvo.name)
    print('salas no curado                  :', len(curado['rooms']))
    print('salas digeridas                  :', len(salas))
    com_par = [r for r in curado['rooms'] if norm(r['name']) in digerido]
    print('salas do curado achadas no digerido:', len(com_par))

    traduz = {'l': 'e', 'o': 'w', 'c': 'u', 'b': 'd', 'n': 'n', 's': 's',
              'e': 'e', 'w': 'w', 'u': 'u', 'd': 'd'}
    confirmado = so_nome = divergente = sem_dado = ambigua = 0
    detalhes = []
    for r in curado['rooms']:
        nome = norm(r['name'])
        lista = digerido.get(nome)
        if not lista:
            continue
        if len(lista) > 1:
            ambigua += 1
        s = max(lista, key=lambda x: x['visits'])
        for d, tgt in r.get('exits', {}).items():
            dd = traduz.get(d, d)
            esperado = nome_por_id.get(tgt, tgt)
            real = s['exits'].get(dd)
            if real and real in mapa.nos:
                obtido = mapa.nos[real]['titulos'].most_common(1)[0][0]
                if compativel(obtido, esperado):
                    confirmado += 1
                else:
                    divergente += 1
                    detalhes.append((r['name'], dd, esperado, obtido))
                continue
            declarado = s['exits_por_nome'].get(dd)
            if declarado and compativel(declarado, esperado):
                so_nome += 1
            elif declarado:
                divergente += 1
                detalhes.append((r['name'], dd, esperado, declarado))
            else:
                sem_dado += 1
    print()
    print('saidas confirmadas por passo observado :', confirmado)
    print('saidas que batem so pelo nome declarado:', so_nome)
    print('saidas divergentes                     :', divergente)
    print('saidas sem dado no digerido            :', sem_dado)
    print('salas do curado com nome ambiguo aqui  :', ambigua)
    for x in detalhes[:12]:
        print('   %-32s -%s-> curado=%-30s digerido=%s' % x)
    return dict(confirmado=confirmado, so_nome=so_nome,
                divergente=divergente, sem_dado=sem_dado)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--glob', action='append', default=None,
                    help='padrao de transcripts; pode repetir. Sem isto, le os dois lugares.')
    ap.add_argument('--out', default=None)
    ap.add_argument('--mostrar-ruido', action='store_true')
    ap.add_argument('--validar-midgaard', action='store_true')
    args = ap.parse_args()

    # Duas casas de transcript, e as duas importam: as sessoes vivas escrevem em
    # automato/runtime/, e o corpus historico dos Dias 96-141 ficou em
    # scripts/local/ (que o git ignora). Ler so' uma delas derruba o
    # levantamento de 266 para 105 salas.
    padroes = args.glob or [
        str(ROOT / 'automato/runtime/transcript_*.jsonl'),
        str(ROOT / 'scripts/local/transcript_*.jsonl'),
    ]
    arquivos = sorted({f for padrao in padroes for f in glob.glob(padrao)})
    if not arquivos:
        print('nenhum transcript em', padroes)
        return 1

    mapa, st = digerir(arquivos)
    salas, ambiguos = construir(mapa)
    grupos = classes_identicas(mapa)

    hero = 'grebolius'
    with open(arquivos[0], encoding='utf-8', errors='replace') as fh:
        for linha in fh:
            try:
                d = json.loads(linha)
            except Exception:
                continue
            if d.get('kind') == 'open':
                hero = (d.get('hero') or hero).lower()
                break

    out = args.out or str(ROOT / 'data/heroes' / hero / 'mapa_vivo.json')
    Path(out).parent.mkdir(parents=True, exist_ok=True)
    Path(out).write_text(json.dumps({
        'hero_id': hero, 'fonte': 'transcripts',
        'gerado_por': 'automato/acoes/digerir_mapa.py',
        'metodo': 'identidade por posicao no grafo; texto so como candidato',
        'resumo': {
            'sessoes': st['sessoes'], 'comandos': st['comandos'],
            'dias': sorted(st['dias']), 'salas': len(salas),
            'arestas_verificadas': len(mapa.arestas),
            'salas_de_texto_identico': sum(len(g[1]) for g in grupos),
            'destinos_de_fronteira': sum(len(s['fronteira']) for s in salas),
        },
        'rooms': salas,
    }, ensure_ascii=False, indent=2), encoding='utf-8')

    if args.mostrar_ruido:
        print('=== linhas removidas da assinatura (top 12) ===')
        for s, n in mapa.ruido.most_common(12):
            print('  %5dx  %s' % (n, s[:95]))
        print()

    print('=' * 78)
    print('DIGESTAO DOS REGISTROS')
    print('=' * 78)
    print('sessoes / comandos     : %d / %d' % (st['sessoes'], st['comandos']))
    print('dias cobertos          : %d (%d..%d)' % (len(st['dias']), min(st['dias']), max(st['dias'])))
    print('looks                  : %d (sem sala: %d)' % (st['looks'], st['looks_falhos']))
    print('movimentos             : %d' % st['movimentos'])
    print('   seguiu aresta ja conhecida : %d' % st['seguiram_aresta'])
    print('   abriu aresta nova          : %d' % st['abriram_aresta'])
    print('   recusado pelo jogo         : %d' % st['movimentos_recusados'])
    print('   sem sala no texto          : %d' % st['movimentos_sem_sala'])
    print('   destino era texto identico : %d' % mapa.criados_ambiguos)
    print('sala mudou sem mover   : %d (recall, fuga, portal)' % st['trocas_sem_movimento'])
    print('descricao instavel      : %d (virada em apelido, sem criar sala)' % st['aliases'])
    print('sala ignorada por buffer: %d (texto de cast/consider/save etc.)' % st['ignoradas'])
    print()
    print('SALAS COM IDENTIDADE PROPRIA :', len(salas))
    print('ARESTAS VERIFICADAS          :', len(mapa.arestas))
    print('linhas de ruido removidas    :', sum(mapa.ruido.values()))
    print()
    print('CLASSES DE TEXTO IDENTICO (so a posicao separa):', len(grupos))
    for sig, ids in grupos[:8]:
        nome = mapa.nos[ids[0]]['titulos'].most_common(1)[0][0]
        print('  %3d salas  %-34s saidas=%s' % (
            len(ids), nome[:34], ''.join(mapa.nos[ids[0]]['saidas']) or '-'))
    if len(grupos) > 8:
        print('  ... e mais %d classes' % (len(grupos) - 8))
    print()
    print('vizinhos nomeados e nunca visitados:', sum(len(s['fronteira']) for s in salas))
    print('vizinhos nomeados ambiguos         :', ambiguos)
    print()
    print('MAIORES SALAS')
    for s in salas[:12]:
        marca = ' [texto identico]' if s['identidade_ambigua'] else ''
        print('  %5dx  %-30s saidas=%-6s%s' % (
            s['visits'], s['name'][:30], ''.join(sorted(s['exits'])) or '-', marca))
    print()
    if args.validar_midgaard:
        validar_midgaard(mapa, salas)
        print()
    print('gravado em:', out)
    return 0


if __name__ == '__main__':
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    sys.exit(main())
