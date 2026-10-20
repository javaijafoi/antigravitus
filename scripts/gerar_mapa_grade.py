#!/usr/bin/env python3
"""gerar_mapa_grade.py - o mapa.json desenhado em grade, como mapa de masmorra, num HTML só.

Por que existe (pedido do autor, 2026-10-20): ver o mundo como um mapa de salas quadradas
numeradas, com corredores e legenda, e clicar numa sala para ver o que o mapa.json sabe dela.
O mapa.html do site é um grafo de pontos e só desenha as salas com `coords`; aqui a posição
de cada sala sai das próprias saídas (n/s/e/w), zona por zona.

O MUD não é euclidiano: duas salas podem "querer" a mesma casa. Quando isso acontece, a
segunda vai para a casa livre mais próxima e o corredor sai torto (tracejado). Cada colisão,
saída não recíproca, destino inexistente, saída pendente e duplicata vira um AVISO na aba
"Avisos" do HTML: é a lista para validar o mapa.

O HTML é autocontido (dados, estilo e script embutidos; nada de fetch nem biblioteca externa)
e abre direto do disco.

Uso:
    python scripts/gerar_mapa_grade.py                       # grebolius -> mapa_grade.html
    python scripts/gerar_mapa_grade.py --hero grebolius --saida caminho.html
"""
import argparse
import json
import math
import sys
from collections import deque
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

DIRS = {'n': (0, -1), 's': (0, 1), 'e': (1, 0), 'w': (-1, 0)}
OPOSTA = {'n': 's', 's': 'n', 'e': 'w', 'w': 'e', 'u': 'd', 'd': 'u'}
ORDEM = 'nesw'
CAMPOS = ('id', 'name', 'zone', 'layer', 'risk', 'risk_code', 'icon', 'exits', 'npcs', 'npcs_confirmados',
          'notes', 'discovered_in', 'visitas_registradas', 'fontes', 'source', 'aliases',
          'unresolved_exits', 'duplicata_de')
TEMPLATE = Path(__file__).with_name('mapa_grade_template.html')


# --------------------------------------------------------------------------- #
# layout (puro)
# --------------------------------------------------------------------------- #

def adjacencia(salas, ids):
    """Vizinhos n/s/e/w dentro do conjunto `ids`, nos dois sentidos, em ordem estável."""
    adj = {i: set() for i in ids}
    for i in sorted(ids):
        for d, b in (salas[i].get('exits') or {}).items():
            if d in DIRS and b in ids and b != i:
                adj[i].add((d, b))
                adj[b].add((OPOSTA[d], i))
    return {i: sorted(v, key=lambda t: (ORDEM.index(t[0]), t[1])) for i, v in adj.items()}


def _anel(centro, r):
    """Casas à distância de Chebyshev r de `centro`, das mais próximas (Manhattan) às mais longe."""
    cx, cy = centro
    casas = [(cx + dx, cy + dy) for dx in range(-r, r + 1) for dy in range(-r, r + 1)
             if max(abs(dx), abs(dy)) == r]
    return sorted(casas, key=lambda p: (abs(p[0] - cx) + abs(p[1] - cy), p[1], p[0]))


def casa_livre(ocupadas, origem, d):
    """A casa ideal (origem + d); se ocupada, até 3 passos na mesma direção; depois, em espiral."""
    dx, dy = DIRS[d]
    for k in (1, 2, 3):
        p = (origem[0] + dx * k, origem[1] + dy * k)
        if p not in ocupadas:
            return p
    alvo = (origem[0] + dx, origem[1] + dy)
    r = 1
    while True:
        for p in _anel(alvo, r):
            if p not in ocupadas:
                return p
        r += 1


def layout_ilha(ancora, adj):
    """BFS a partir da âncora. Devolve (posições, ordem, deslocadas[(sala, de, direção)])."""
    pos, ocup, ordem, deslocadas = {ancora: (0, 0)}, {(0, 0): ancora}, [ancora], []
    fila = deque([ancora])
    while fila:
        a = fila.popleft()
        for d, b in adj[a]:
            if b in pos:
                continue
            ideal = (pos[a][0] + DIRS[d][0], pos[a][1] + DIRS[d][1])
            p = ideal if ideal not in ocup else casa_livre(ocup, pos[a], d)
            if p != ideal:
                deslocadas.append((b, a, d))
            pos[b], ocup[p] = p, b
            ordem.append(b)
            fila.append(b)
    return pos, ordem, deslocadas


def _ancora(ids, salas, preferidas):
    for p in preferidas:
        if p in ids:
            return p
    return sorted(ids, key=lambda i: (-(salas[i].get('visitas_registradas') or 0), i))[0]


def layout_zona(ids, salas, preferidas=()):
    """Posição (x, y) e número de cada sala da zona; ilhas lado a lado. Devolve (pos, num, deslocadas)."""
    adj = adjacencia(salas, set(ids))
    restantes, ilhas, deslocadas = set(ids), [], []
    while restantes:
        ancora = _ancora(restantes, salas, preferidas)
        pos, ordem, desl = layout_ilha(ancora, {k: v for k, v in adj.items()})
        restantes -= set(pos)
        mx, my = min(x for x, _ in pos.values()), min(y for _, y in pos.values())
        pos = {k: (x - mx, y - my) for k, (x, y) in pos.items()}
        ilhas.append((pos, ordem))
        deslocadas += desl
    # prateleiras: maiores ilhas primeiro, da esquerda para a direita; nova fileira quando passa
    # da largura (a mais larga das ilhas ou ~1,6 x raiz da área ocupada, o que for maior)
    primeira = ilhas[0][1][0]                       # a ilha da âncora (santuário/mais visitada) abre a zona
    ilhas.sort(key=lambda il: (il[1][0] != primeira, -len(il[0]), il[1][0]))
    caixas = [(max(x for x, _ in p.values()) + 1, max(y for _, y in p.values()) + 1) for p, _ in ilhas]
    area = sum((w + 1) * (h + 1) for w, h in caixas)
    largura = max(max(w for w, _ in caixas), 12, int(math.sqrt(area) * 1.6))
    final, numero, cx, cy, altura_fila, n = {}, {}, 0, 0, 0, 1
    for (pos, ordem), (w, h) in zip(ilhas, caixas):
        if cx and cx + w > largura:
            cx, cy, altura_fila = 0, cy + altura_fila + 1, 0
        for k in ordem:
            final[k] = (pos[k][0] + cx, pos[k][1] + cy)
            numero[k] = n
            n += 1
        cx += w + 1
        altura_fila = max(altura_fila, h)
    return final, numero, deslocadas


# --------------------------------------------------------------------------- #
# avisos de validação (puro)
# --------------------------------------------------------------------------- #

def avisos_do_mapa(salas, deslocadas):
    av = []
    for b, a, d in deslocadas:
        av.append({'tipo': 'colisao', 'sala': b,
                   'texto': 'sem casa livre a %s de %s: desenhada fora do lugar (corredor torto)' % (d, a)})
    for i in sorted(salas):
        r = salas[i]
        for d, b in sorted((r.get('exits') or {}).items()):
            if b not in salas:
                av.append({'tipo': 'destino_inexistente', 'sala': i, 'texto': 'saída %s aponta para "%s", que não está no mapa' % (d, b)})
            elif d in OPOSTA and (salas[b].get('exits') or {}).get(OPOSTA[d]) != i:
                volta = (salas[b].get('exits') or {}).get(OPOSTA[d])
                av.append({'tipo': 'nao_reciproca', 'sala': i,
                           'texto': '%s → %s, mas %s %s → %s' % (d, b, b, OPOSTA[d], volta or 'nada')})
        for u in r.get('unresolved_exits') or []:
            av.append({'tipo': 'saida_pendente', 'sala': i, 'texto': 'saída sem destino conhecido: %s' % u})
        if r.get('duplicata_de'):
            av.append({'tipo': 'duplicata', 'sala': i, 'texto': 'duplicata de %s' % r['duplicata_de']})
    return av


# --------------------------------------------------------------------------- #
# dados para o HTML
# --------------------------------------------------------------------------- #

def montar(mapa):
    salas = {r['id']: r for r in mapa['rooms']}
    por_zona = {}
    for r in mapa['rooms']:
        por_zona.setdefault(r.get('zone') or 'Sem zona', []).append(r['id'])
    ordem_oficial = [z for z in (mapa.get('zones') or []) if z in por_zona]
    zonas = ordem_oficial + sorted((z for z in por_zona if z not in ordem_oficial), key=lambda z: (-len(por_zona[z]), z))
    preferidas = [mapa.get('sanctuary_id'), mapa.get('current_location_id'), mapa.get('camp_id')]
    saida_zonas, deslocadas_todas = [], []
    for zi, z in enumerate(zonas):
        pos, num, desl = layout_zona(por_zona[z], salas, [p for p in preferidas if p])
        deslocadas_todas += desl
        ids = set(pos)
        arestas, vistos = [], set()
        for a in sorted(ids, key=lambda k: num[k]):
            for d, b in sorted((salas[a].get('exits') or {}).items()):
                if d not in DIRS or b not in ids:
                    continue
                chave = tuple(sorted((a, b)))
                if chave in vistos:
                    continue
                vistos.add(chave)
                ideal = (pos[a][0] + DIRS[d][0], pos[a][1] + DIRS[d][1])
                arestas.append({'a': a, 'b': b, 'torta': pos[b] != ideal})
        saida_zonas.append({
            'id': 'z%d' % zi, 'nome': z, 'n': len(ids),
            'largura': max(x for x, _ in pos.values()) + 1, 'altura': max(y for _, y in pos.values()) + 1,
            'salas': [dict({k: salas[i][k] for k in CAMPOS if k in salas[i]}, num=num[i], x=pos[i][0], y=pos[i][1])
                      for i in sorted(ids, key=lambda k: num[k])],
            'arestas': arestas,
        })
    return {
        'heroi': mapa.get('hero_name') or mapa.get('hero_id'),
        'dia': mapa.get('last_updated_day'),
        'santuario': mapa.get('sanctuary_id'),
        'atual': mapa.get('current_location_id'),
        'total': len(salas),
        'zonas': saida_zonas,
        'avisos': avisos_do_mapa(salas, deslocadas_todas),
    }


def html(dados, template=None):
    texto = (template or TEMPLATE.read_text(encoding='utf-8'))
    blob = json.dumps(dados, ensure_ascii=False, separators=(',', ':'), sort_keys=True).replace('</', '<\\/')
    return texto.replace('__DADOS_JSON__', blob).replace('__HEROI__', str(dados['heroi']))


def main(argv=None):
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    ap = argparse.ArgumentParser(description='Desenha o mapa.json em grade num HTML autocontido.')
    ap.add_argument('--hero', default='grebolius')
    ap.add_argument('--saida', default=str(ROOT / 'mapa_grade.html'))
    a = ap.parse_args(argv)
    mapa = json.loads((ROOT / 'data' / 'heroes' / a.hero / 'mapa.json').read_text(encoding='utf-8'))
    dados = montar(mapa)
    Path(a.saida).write_text(html(dados), encoding='utf-8')
    print('%d salas em %d zonas -> %s' % (dados['total'], len(dados['zonas']), a.saida))
    for z in dados['zonas']:
        tortas = sum(e['torta'] for e in z['arestas'])
        print('  %-45s %4d salas  %3d corredores tortos' % (z['nome'], z['n'], tortas))
    tipos = {}
    for av in dados['avisos']:
        tipos[av['tipo']] = tipos.get(av['tipo'], 0) + 1
    print('avisos: ' + (', '.join('%s=%d' % kv for kv in sorted(tipos.items())) or 'nenhum'))
    return 0


if __name__ == '__main__':
    sys.exit(main())
