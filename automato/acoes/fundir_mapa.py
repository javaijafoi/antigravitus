# -*- coding: utf-8 -*-
"""fundir_mapa.py - absorve o levantamento no mapa curado, de forma repetivel.

O problema que isto resolve: a primeira mesclagem foi feita a mao, num script
solto. Rodar de novo ia empilhar sala sobre sala e contar visita duas vezes.

A separacao que torna repetivel:

    CURADO     o que um humano escreveu: nome, camada, zona, risco, coords,
               notas, descoberta. NUNCA e' removido nem sobrescrito.
    LEVANTAMENTO  o que as sessoes observaram. E' DERIVADO: a cada rodada ele e'
               apagado e refeito do zero a partir do digerido.

Como o derivado e' identificado:
    - salas que ESTE script criou vivem na camada `levantamento`;
    - arestas que ESTE script acrescentou a salas curadas ficam registradas em
      `arestas_do_levantamento`, entao a rodada seguinte sabe o que tirar antes
      de repor.

Uso:
    python automato/acoes/fundir_mapa.py                  # funde e grava
    python automato/acoes/fundir_mapa.py --seco           # so' relata, nao grava
    python automato/acoes/fundir_mapa.py --mapa X --levantamento Y

Antes de gravar, confere: id unico, toda saida aponta para sala existente, e toda
sala numa camada declarada. Falhando a conferencia, nada e' escrito.
"""
import argparse
import difflib
import json
import re
import sys
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT / 'automato' / 'nucleo'))
import config  # noqa: E402

# Titulos que se repetem em salas diferentes. A identidade ali e' a POSICAO, e o
# id precisa denunciar isso: por isso labirinto ganha `lb###` em vez de `lv###`.
LABIRINTO = config.TITULOS_LABIRINTO

# Identidades provadas PELA CAMINHADA (Dia 156).
#
# A rota ate' o id da esquerda termina na sala que o jogo chama pelo nome da
# direita: sao a MESMA sala, e o mapa ficou com dois nos porque curadoria e
# levantamento batizaram o lugar de formas diferentes. Semelhanca de nome nao
# pega esses casos - sao nomes genuinamente distintos - mas a caminhada prova.
#
# E O NOME DO JOGO VENCE, porque e' ele que a rotina le' no `look` ao chegar.
# Sem bater o nome, a rotina nao reconhece onde esta' e a rota falha - foi assim
# que a auditoria de mercado errou 11 de 17 lojas. O nome antigo fica em
# `aliases`, para nao perder o que a curadoria escreveu.
ALIAS_CAMINHADA = {
    'correio_midgaard': 'O Escritório dos Correios',
    'bar_javali': 'O Bar da Estalagem Javali Roncador',
    # Terceiro caso, achado ao ir pegar doacao no Dia 156: o mapa dizia "A Sala
    # de Doacoes" e o jogo diz "A Sala de Doacoes de Midgaard". A rotina nao
    # reconhecia onde estava e nao conseguia rotear para la'.
    'sala_doacoes': 'A Sala de Doações de Midgaard',
}

# --- Arestas corrigidas por verificacao AO VIVO (Dia 156) ---
#
# O merge mantem o valor CURADO nos conflitos. Isso esta' certo para dado de
# curadoria - mas errado quando a curadoria simplesmente observou mal. Aqui a
# OBSERVACAO vence, e cada linha tem a prova.
#
# `None` = o jogo RECUSA a direcao ("Você não pode ir por aí...").
# nome    = destino que o jogo ANUNCIA mas ainda nao foi visitado (fica como
#           sala nova, sem coordenada - e' fronteira).
#
# Caso que originou isto: "A Entrada da Guilda dos Clérigos" tinha 3 das 4
# arestas erradas, incluindo um `s` para a Loja de Armaduras que nao existe. Era
# o que fazia o BFS achar uma rota de 3 passos ate' o armeiro e terminar na
# Praca do Templo - a rota real e' `d,s,w,s` (4 passos).
ARESTAS_VERIFICADAS = {
    'guilda_clerigos_entrada': {
        'e': 'A Praça do Templo',
        'n': 'O Bar dos Clérigos',   # anunciado no `exits`; o guarda barra a passagem
        's': None,                   # recusado: "Você não pode ir por aí..."
        'w': None,                   # recusado
    },
}

CAMADA_DERIVADA = 'levantamento'
ZONA_DERIVADA = 'Levantamento (Dias 96-141)'
FONTE = 'levantamento_sessoes'
# A primeira mesclagem foi feita a mao e usou outro rotulo. Aceitar os dois evita
# que uma rodada sobre arquivo legado deixe etiqueta orfa para tras.
FONTES_ANTIGAS = ('levantamento_sessoes', 'levantamento_dias_96_141')
LIMIAR_NOME = 0.82


def base(texto):
    t = unicodedata.normalize('NFKD', (texto or '').lower())
    return ' '.join(''.join(c for c in t if not unicodedata.combining(c)).split())


def chave(texto):
    """Nome normalizado, sem o sufixo de desambiguacao do curador.

    O humano escreve "O Grande Campo (Sul)" para separar salas homonimas; o
    jogo chama todas de "O Grande Campo de Midgaard". Sem tirar os parenteses,
    as duas viram salas diferentes e o mapa ganha duplicata.
    """
    return ' '.join(re.sub(r'\([^)]*\)', ' ', base(texto)).split())


def compativel(a, b):
    a, b = chave(a), chave(b)
    if not a or not b:
        return False
    if a in b or b in a:
        return True
    return difflib.SequenceMatcher(None, a, b).ratio() >= LIMIAR_NOME


def carregar(caminho):
    return json.loads(Path(caminho).read_text(encoding='utf-8'))


def novo_id(nome, mapa_id):
    """Id da sala derivada. Labirinto ganha prefixo proprio.

    Onde o titulo se repete, o nome nao identifica a sala - a posicao identifica.
    Usar o mesmo `lv###` para tudo esconde isso de quem le o mapa depois, e a
    confusao e' exatamente o que se quer evitar. `lb###` diz "aqui o titulo nao
    serve" na propria etiqueta.
    """
    prefixo = 'lb' if chave(nome) in LABIRINTO else 'lv'
    n = 1 + sum(1 for x in mapa_id.values() if x and x.startswith(prefixo))
    return '%s%03d' % (prefixo, n)


def normalizar_saidas(salas):
    """l/o -> e/w. No servidor 'l' e' look e 'o' e' order; nunca direcao."""
    trocas = colisoes = 0
    for sala in salas:
        novo = {}
        for d, alvo in (sala.get('exits') or {}).items():
            dd = {'l': 'e', 'o': 'w'}.get(d, d)
            if dd in novo:
                colisoes += 1
            novo[dd] = alvo
            trocas += dd != d
        sala['exits'] = novo
    return trocas, colisoes


def limpar_derivado(curadas):
    """Tira o que a rodada ANTERIOR deste script tinha posto."""
    removidas = 0
    for sala in curadas:
        for d in sala.pop('arestas_do_levantamento', []):
            if d in (sala.get('exits') or {}):
                del sala['exits'][d]
                removidas += 1
        sala.pop('visitas_registradas', None)
        fontes = sala.get('fontes')
        if isinstance(fontes, list):
            for antiga in FONTES_ANTIGAS:
                if antiga in fontes:
                    fontes.remove(antiga)
            if not fontes:
                sala.pop('fontes', None)
    return removidas


def fundir(mapa, levantamento, seco=False):
    salas = mapa['rooms']
    ids_antes = {s['id'] for s in salas}
    nome_de = {s['id']: s.get('name', s['id']) for s in salas}
    vivo = {r['id']: r for r in levantamento['rooms']}

    # 1) separa curado de derivado, e tira o derivado antigo
    curadas = [s for s in salas if s.get('layer') != CAMADA_DERIVADA]
    antigas = [s for s in salas if s.get('layer') == CAMADA_DERIVADA]
    removidas = limpar_derivado(curadas)
    trocas, colisoes = normalizar_saidas(curadas)

    # 2) pareia o levantamento novo com o curado, por nome tolerante + vizinhos
    def vizinhos(saidas, tabela):
        return {chave(tabela[t]) for t in saidas if t in tabela}

    nomes_vivo = {i: vivo[i].get('name', '') for i in vivo}
    mapa_id, usados, exatos = {}, set(), 0

    # 2a) PRIMEIRO os pares provados pela caminhada. O nome do JOGO vence: o
    # curado e' renomeado e o nome antigo fica em `aliases`.
    provados = 0
    for curado_id, nome_do_jogo in ALIAS_CAMINHADA.items():
        alvo_curado = next((c for c in curadas if c['id'] == curado_id), None)
        if alvo_curado is None:
            continue
        gemeo = next((v for v in levantamento['rooms']
                      if chave(v.get('name')) == chave(nome_do_jogo)), None)
        if gemeo is None:
            continue
        antigo = alvo_curado.get('name', '')
        if antigo and chave(antigo) != chave(nome_do_jogo):
            alvo_curado.setdefault('aliases', [])
            if antigo not in alvo_curado['aliases']:
                alvo_curado['aliases'].append(antigo)
            alvo_curado['name'] = nome_do_jogo
            nome_de[curado_id] = nome_do_jogo
        usados.add(curado_id)
        mapa_id[gemeo['id']] = curado_id
        provados += 1
    for v in sorted(levantamento['rooms'], key=lambda x: -x.get('visits', 0)):
        # Quem ja' foi pareado pelos ALIAS_CAMINHADA nao entra de novo. Sem isto o
        # `else` abaixo grava None e apaga o pareamento provado, e o gemeo volta
        # como sala derivada - foi o que deixou `lv001` convivendo com
        # `correio_midgaard` mesmo depois do alias.
        if v['id'] in mapa_id:
            continue
        vv = vizinhos(v.get('exits') or {}, nomes_vivo)
        escolhida, melhor, marcou = None, -1.0, False
        for c in curadas:
            if c['id'] in usados or not compativel(v['name'], c['name']):
                continue
            igual = chave(v['name']) == chave(c['name'])
            score = len(vv & vizinhos(c.get('exits') or {}, nome_de)) + (10 if igual else 0)
            if score > melhor:
                escolhida, melhor, marcou = c, score, igual
        if escolhida is not None:
            usados.add(escolhida['id'])
            mapa_id[v['id']] = escolhida['id']
            exatos += bool(marcou)
        else:
            mapa_id[v['id']] = None

    for v in levantamento['rooms']:
        if mapa_id[v['id']] is None:
            mapa_id[v['id']] = novo_id(v['name'], mapa_id)

    # 3) enriquece as curadas e cria as novas
    por_id = {s['id']: s for s in curadas}
    adicionadas = conflitos = 0
    detalhes = []
    for v in levantamento['rooms']:
        alvo = mapa_id[v['id']]
        arestas = {d: mapa_id[t] for d, t in (v.get('exits') or {}).items()
                   if t in mapa_id and mapa_id[t] != alvo}
        if alvo in por_id:
            sala = por_id[alvo]
            sala.setdefault('exits', {})
            sala['visitas_registradas'] = sala.get('visitas_registradas', 0) + v.get('visits', 0)
            sala.setdefault('fontes', [])
            if FONTE not in sala['fontes']:
                sala['fontes'].append(FONTE)
            # NPC confirmado por `consider` entra em campo PROPRIO nas salas
            # autorais: o `npcs` delas foi escrito a mao e usa outro vocabulario
            # ("Estatuas dos Centenarios"); o do levantamento e' a palavra-chave
            # que o jogo aceitou ("zelador"). Misturar os dois apagaria a
            # diferenca entre curadoria e confirmacao.
            if v.get('npcs'):
                sala['npcs_confirmados'] = v['npcs']
            novas = []
            for d, t in arestas.items():
                atual = sala['exits'].get(d)
                if atual is None:
                    sala['exits'][d] = t
                    novas.append(d)
                    adicionadas += 1
                elif atual != t:
                    conflitos += 1
                    if len(detalhes) < 10:
                        detalhes.append((sala['name'], d, nome_de.get(atual, atual),
                                         vivo.get(t, {}).get('name', t)))
            if novas:
                sala['arestas_do_levantamento'] = sorted(set(sala.get('arestas_do_levantamento', [])) | set(novas))

    derivadas = []
    for v in levantamento['rooms']:
        alvo = mapa_id[v['id']]
        if alvo in por_id:
            continue
        arestas = {d: mapa_id[t] for d, t in (v.get('exits') or {}).items()
                   if t in mapa_id and mapa_id[t] != alvo}
        derivadas.append({
            'id': alvo, 'name': v['name'], 'layer': CAMADA_DERIVADA, 'zone': ZONA_DERIVADA,
            'risk': 'Desconhecido', 'risk_code': 'unknown', 'icon': '🗺️',
            'exits': arestas, 'npcs': v.get('npcs', []), 'notes': (v.get('description') or '')[:300],
            'discovered_in': 'Ciclo X (Dias 96-156)',
            'visitas_registradas': v.get('visits', 0), 'fontes': [FONTE],
        })

    mapa['rooms'] = curadas + derivadas

    # Correcoes verificadas AO VIVO: a observacao vence a curadoria.
    todos = {r['id']: r for r in mapa['rooms']}
    por_nome = {}
    for r in mapa['rooms']:
        por_nome.setdefault(chave(r['name']), r['id'])
    novas_por_correcao = []
    for rid, direcoes in ARESTAS_VERIFICADAS.items():
        sala = todos.get(rid)
        if sala is None:
            continue
        sala.setdefault('exits', {})
        for d, destino in direcoes.items():
            if destino is None:
                sala['exits'].pop(d, None)
                continue
            alvo = por_nome.get(chave(destino))
            if alvo is None:
                alvo = novo_id(destino, mapa_id)
                novas_por_correcao.append({
                    'id': alvo, 'name': destino, 'layer': CAMADA_DERIVADA,
                    'zone': ZONA_DERIVADA, 'risk': 'Desconhecido', 'risk_code': 'unknown',
                    'icon': '🗺️', 'exits': {}, 'npcs': [],
                    'notes': 'Destino anunciado no `exits` mas nunca visitado. '
                             'Colocado no mapa por correcao verificada ao vivo.',
                    'discovered_in': 'Ciclo X (Dia 156)', 'fontes': [FONTE]})
                mapa_id[destino] = alvo
                por_nome[chave(destino)] = alvo
            sala['exits'][d] = alvo
            todos[alvo] = sala
    if novas_por_correcao:
        # as novas precisam existir como alvo de aresta
        for nova in novas_por_correcao:
            mapa['rooms'].append(nova)
            todos[nova['id']] = nova
        # a volta: liga a nova sala de volta para quem a anunciou
        for rid, direcoes in ARESTAS_VERIFICADAS.items():
            for d, destino in direcoes.items():
                if destino is None:
                    continue
                alvo = por_nome.get(chave(destino))
                if alvo and alvo != rid:      # nunca auto-laco
                    OPOSTO_D = {'n': 's', 's': 'n', 'e': 'w', 'w': 'e', 'u': 'd', 'd': 'u'}
                    todos[alvo].setdefault('exits', {})
                    if OPOSTO_D.get(d) and OPOSTO_D[d] not in todos[alvo]['exits']:
                        todos[alvo]['exits'][OPOSTO_D[d]] = rid
    # Rede de seguranca: sala que aponta para si mesma e' sempre defeito.
    auto_lacos = 0
    for r in mapa['rooms']:
        for d, a in list((r.get('exits') or {}).items()):
            if a == r['id']:
                del r['exits'][d]
                auto_lacos += 1
    return {'trocas': trocas, 'colisoes': colisoes, 'removidas': removidas,
            'pareadas': len(usados), 'exatas': exatos,
            'novas': len(derivadas), 'adicionadas': adicionadas,
            'conflitos': conflitos, 'detalhes': detalhes,
            'curadas': len(curadas), 'ids_antes': len(ids_antes),
            'corrigidas': len(ARESTAS_VERIFICADAS), 'novas_por_correcao': len(novas_por_correcao)}


def conferir(mapa):
    """Falhando aqui, nada e' gravado."""
    problemas = []
    ids = [s['id'] for s in mapa['rooms']]
    if len(ids) != len(set(ids)):
        problemas.append('id de sala duplicado')
    conjunto = set(ids)
    for s in mapa['rooms']:
        for d, t in (s.get('exits') or {}).items():
            if t not in conjunto:
                problemas.append('saida %s/%s aponta para sala inexistente: %s' % (s['id'], d, t))
    camadas = {l['id'] for l in mapa['layers']}
    for s in mapa['rooms']:
        if s.get('layer') not in camadas:
            problemas.append('sala %s em camada inexistente: %s' % (s['id'], s.get('layer')))
    if mapa.get('total_rooms') != len(mapa['rooms']):
        problemas.append('total_rooms diverge da lista')
    for campo in ('sanctuary_id', 'current_location_id', 'camp_id'):
        alvo = mapa.get(campo)
        if alvo is not None and alvo not in conjunto:
            problemas.append('%s aponta para sala inexistente: %s' % (campo, alvo))
    return problemas


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--mapa', default=str(ROOT / 'data/heroes/grebolius/mapa.json'))
    ap.add_argument('--levantamento', default=str(ROOT / 'data/heroes/grebolius/mapa_vivo.json'))
    ap.add_argument('--dia', type=int, default=156)
    ap.add_argument('--seco', action='store_true')
    args = ap.parse_args()

    mapa = carregar(args.mapa)
    levantamento = carregar(args.levantamento)
    antes = len(mapa['rooms'])

    if CAMADA_DERIVADA not in {l['id'] for l in mapa['layers']}:
        mapa['layers'].append({
            'id': CAMADA_DERIVADA, 'name': '🗺️ Levantamento Vivo (Dias 96-156)',
            'description': 'Salas reconstruidas dos registros de sessao. Derivadas: refeitas a cada '
                           'mesclagem. Sem posicao grafica; aparecem como ficha, nao como no do desenho.'})
    if ZONA_DERIVADA not in mapa.get('zones', []):
        mapa.setdefault('zones', []).append(ZONA_DERIVADA)

    r = fundir(mapa, levantamento)
    mapa['total_rooms'] = len(mapa['rooms'])
    mapa['last_updated_day'] = args.dia
    mapa['last_updated_cycle'] = 'Ciclo X (Dia %d; com levantamento das sessoes)' % args.dia
    mapa.setdefault('reconciliation_notes', []).append(
        'Dia %d: levantamento refundido (%d salas digeridas: %d pareadas com o curado, %d novas). '
        "Chaves 'l'/'o' normalizadas para 'e'/'w' - no servidor 'l' e' look e 'o' e' order, nunca "
        'direcao. O derivado e refeito a cada rodada; o curado nunca e sobrescrito. Conflito de '
        'aresta mantem o valor curado.' % (args.dia, len(levantamento['rooms']), r['pareadas'], r['novas']))

    problemas = conferir(mapa)
    print('=' * 70)
    print('MESCLAGEM DO MAPA')
    print('=' * 70)
    print('  curadas (autorais)        : %d' % r['curadas'])
    print("  chaves 'l'/'o' -> 'e'/'w' : %d  (colisoes: %d)" % (r['trocas'], r['colisoes']))
    print('  derivado anterior removido: %d arestas' % r['removidas'])
    print('  pareadas com o curado     : %d  (nome exato: %d)' % (r['pareadas'], r['exatas']))
    print('  salas novas (derivadas)   : %d' % r['novas'])
    print('  arestas novas no curado   : %d' % r['adicionadas'])
    print('  conflitos (curado venceu) : %d' % r['conflitos'])
    print('  correcoes ao vivo aplicadas: %d salas, %d salas novas criadas'
          % (r.get('corrigidas', 0), r.get('novas_por_correcao', 0)))
    for c in r['detalhes']:
        print('     %-34s -%s-> curado=%-28s levantamento=%s' % c)
    print('  TOTAL                     : %d -> %d salas' % (antes, len(mapa['rooms'])))
    print()
    if problemas:
        print('CONFERENCIA FALHOU - nada foi gravado:')
        for p in problemas[:10]:
            print('  -', p)
        return 1
    print('  conferencia interna: OK (id unico, saidas validas, camadas validas)')
    if args.seco:
        print('  --seco: nada gravado')
        return 0
    Path(args.mapa).write_text(json.dumps(mapa, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print('  gravado em:', args.mapa)
    return 0


if __name__ == '__main__':
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    sys.exit(main())
