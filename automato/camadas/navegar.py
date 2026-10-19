# -*- coding: utf-8 -*-
"""navegar.py - leva a personagem de uma sala a outra pelo mapa.json, conferindo cada sala.

Por que existe: andar sala a sala "à mão" por rota que o mapa já conhece gasta contexto
e, pior, dispensa a conferência (diretiva de jogo §9: andar por MARCO, em trecho curto,
com teto de passos e tempo). Este script faz o trajeto e PARA no destino.

O que ele NÃO faz (de propósito):
  - nunca fala, pergunta, entrega, compra, pega nem ataca. Só envia direções, `look` e
    `exits`. Diálogo de missão é manual (AGENTS #14, diretiva §20). Ao chegar ele devolve
    o controle a quem joga;
  - nunca atravessa sala marcada como perigosa (config.RISCO_A_EVITAR) sem --permitir-risco;
  - nunca insiste: sala diferente da esperada, combate, vida baixa, porta fechada ou
    recusa de movimento => para e explica.

Códigos de saída: 0 chegou | 2 sem caminho ou dado ruim | 3 sala inesperada |
4 combate ou vida baixa | 5 recusa de movimento ou porta | 6 teto de passos ou de tempo.

Uso:
    python automato/camadas/navegar.py --listar lyon
    python automato/camadas/navegar.py --seco --de templo_midgaard --para cap12_026
    python automato/camadas/navegar.py --para cap12_026            # parte de onde está
"""
import argparse
import collections
import json
import re
import sys
import time
import unicodedata
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'nucleo'))
import config  # noqa: E402

DIRECOES = ('n', 's', 'e', 'w', 'u', 'd')
PROMPT = re.compile(r'^\s*\d+hp\s+\d+mn\s+\d+mv\s*>\s*')
RECUSAS = ('não pode ir', 'a porta está fechada', 'muito relaxado', 'está muito ocupado',
           'você está muito ocupado', 'trancad')


def normalizar(texto):
    t = unicodedata.normalize('NFKD', texto or '')
    t = ''.join(c for c in t if not unicodedata.combining(c))
    return ' '.join(re.sub(r'[^a-z0-9 ]+', ' ', t.lower()).split())


def carregar_mapa(caminho=None):
    caminho = Path(caminho) if caminho else config.DOC_MAPA
    dados = json.loads(caminho.read_text(encoding='utf-8'))
    return {r['id']: r for r in dados['rooms']}


def vizinhos(salas, id_, permitir_risco=False):
    sala = salas[id_]
    for d, destino in (sala.get('exits') or {}).items():
        if d not in DIRECOES or destino not in salas:
            continue
        if not permitir_risco and salas[destino].get('risk_code') in config.RISCO_A_EVITAR:
            continue
        yield d, destino


def caminho(salas, origem, destino, permitir_risco=False):
    """Menor caminho como lista de (direcao, id). None se não houver."""
    if origem not in salas or destino not in salas:
        return None
    if origem == destino:
        return []
    anterior = {origem: None}
    fila = collections.deque([origem])
    while fila:
        atual = fila.popleft()
        for d, prox in vizinhos(salas, atual, permitir_risco):
            if prox in anterior:
                continue
            anterior[prox] = (atual, d)
            if prox == destino:
                return _reconstruir(anterior, destino)
            fila.append(prox)
    return None


def _reconstruir(anterior, destino):
    passos, c = [], destino
    while anterior[c]:
        pai, d = anterior[c]
        passos.append((d, c))
        c = pai
    passos.reverse()
    return passos


def titulo(texto):
    """Primeira linha útil de uma resposta de movimento ou look (o nome da sala)."""
    for linha in (texto or '').splitlines():
        limpa = PROMPT.sub('', linha).strip()
        if not limpa or limpa.startswith('DICA') or limpa.startswith('>>>'):
            continue
        return limpa
    return ''


def candidatos_por_titulo(salas, t):
    n = normalizar(t)
    return [i for i, r in salas.items() if normalizar(r['name']) == n]


def buscar(salas, consulta):
    n = normalizar(consulta)
    achados = []
    for i, r in salas.items():
        if n in normalizar(i) or n in normalizar(r['name']):
            achados.append((i, r['name'], r.get('zone', ''), r.get('risk_code', '')))
    return achados


class Parada(Exception):
    def __init__(self, codigo, motivo):
        super().__init__(motivo)
        self.codigo, self.motivo = codigo, motivo


def navegar(salas, origem, destino, run, permitir_risco=False, hp_min=0.60,
            max_passos=80, max_segundos=300, log=print):
    """Executa o caminho com `run(cmd) -> (texto, vitals, combate)`. Devolve a lista de passos feitos."""
    plano = caminho(salas, origem, destino, permitir_risco)
    if plano is None:
        raise Parada(2, 'sem caminho entre %s e %s (rotas por sala perigosa excluídas)' % (origem, destino))
    if len(plano) > max_passos:
        raise Parada(6, 'caminho de %d passos passa do teto de %d' % (len(plano), max_passos))
    inicio, hp_max, feitos = time.time(), 0, []
    for i, (d, esperado) in enumerate(plano, 1):
        if time.time() - inicio > max_segundos:
            raise Parada(6, 'teto de tempo (%ds) no passo %d de %d' % (max_segundos, i, len(plano)))
        texto, vitals, combate = run(d)
        baixo = texto.lower()
        if any(r in baixo for r in RECUSAS):
            raise Parada(5, 'passo %d (%s para %s) recusado: %r' % (i, d, salas[esperado]['name'], titulo(texto)[:80]))
        hp = (vitals or {}).get('hp')
        if isinstance(hp, int):
            hp_max = max(hp_max, hp)
        if combate:
            raise Parada(4, 'combate no passo %d; use recall ao primeiro risco, não ande de volta' % i)
        if isinstance(hp, int) and hp_max and hp / hp_max < hp_min:
            raise Parada(4, 'vida %d de %d (<%d%%) no passo %d' % (hp, hp_max, int(hp_min * 100), i))
        t = titulo(texto)
        if normalizar(t) != normalizar(salas[esperado]['name']):
            raise Parada(3, 'passo %d: esperava "%s", cheguei em "%s"' % (i, salas[esperado]['name'], t))
        feitos.append((d, esperado))
        log('[%02d/%02d] %s -> %s' % (i, len(plano), d, t))
    return feitos


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    ap.add_argument('--para', help='id da sala de destino (use --listar para achar)')
    ap.add_argument('--de', help='id da sala atual; se omitido, deduz pelo look')
    ap.add_argument('--listar', metavar='TEXTO', help='procura salas por id ou nome e sai')
    ap.add_argument('--seco', action='store_true', help='só imprime o caminho, sem conectar')
    ap.add_argument('--permitir-risco', action='store_true')
    ap.add_argument('--hp-min', type=float, default=0.60)
    ap.add_argument('--max-passos', type=int, default=80)
    ap.add_argument('--max-segundos', type=int, default=300)
    a = ap.parse_args(argv)
    salas = carregar_mapa()
    if a.listar:
        for i, nome, zona, risco in buscar(salas, a.listar):
            print('%-24s %-40s %-24s %s' % (i, nome, zona, risco))
        return 0
    if not a.para or a.para not in salas:
        print('destino ausente ou desconhecido; use --listar', file=sys.stderr)
        return 2
    if a.seco:
        if not a.de or a.de not in salas:
            print('--seco exige --de com id conhecido', file=sys.stderr)
            return 2
        p = caminho(salas, a.de, a.para, a.permitir_risco)
        if p is None:
            print('SEM CAMINHO', file=sys.stderr)
            return 2
        print(' '.join(d for d, _ in p))
        for d, i in p:
            print('  %s -> %s (%s)' % (d, salas[i]['name'], i))
        return 0
    from base import run  # importa só aqui: precisa do driver no ar
    origem = a.de
    if not origem:
        texto, _, _ = run('look')
        cands = candidatos_por_titulo(salas, titulo(texto))
        if len(cands) != 1:
            print('não deduzi a sala atual (%r tem %d candidatos); passe --de' % (titulo(texto), len(cands)), file=sys.stderr)
            return 2
        origem = cands[0]
    try:
        navegar(salas, origem, a.para, run, a.permitir_risco, a.hp_min, a.max_passos, a.max_segundos)
    except Parada as p:
        print('PAROU (código %d): %s' % (p.codigo, p.motivo), file=sys.stderr)
        return p.codigo
    print('CHEGOU: %s. Daqui em diante é manual: fala de missão, give e compras (AGENTS #14, #13).'
          % salas[a.para]['name'])
    return 0


if __name__ == '__main__':
    sys.exit(main())
