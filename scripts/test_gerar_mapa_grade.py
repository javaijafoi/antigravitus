#!/usr/bin/env python3
"""Testes do scripts/gerar_mapa_grade.py: layout em grade, avisos de validação e o HTML autocontido."""
import json
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import gerar_mapa_grade as G  # noqa: E402


def sala(i, exits, zona='Z', **kw):
    return dict({'id': i, 'name': i.upper(), 'zone': zona, 'layer': 'l', 'risk': '', 'risk_code': 'unknown',
                 'icon': '', 'exits': exits, 'npcs': [], 'notes': '', 'discovered_in': ''}, **kw)


def mapa(*salas, **kw):
    return dict({'hero_name': 'Teste', 'rooms': list(salas), 'zones': ['Z']}, **kw)


class TestLayout(unittest.TestCase):
    def test_cruz_fica_nas_direcoes(self):
        m = mapa(sala('c', {'n': 'n1', 's': 's1', 'e': 'e1', 'w': 'w1'}),
                 sala('n1', {'s': 'c'}), sala('s1', {'n': 'c'}), sala('e1', {'w': 'c'}), sala('w1', {'e': 'c'}))
        salas = {r['id']: r for r in m['rooms']}
        pos, num, desl = G.layout_zona(list(salas), salas, ['c'])
        x, y = pos['c']
        self.assertEqual(pos['n1'], (x, y - 1))
        self.assertEqual(pos['s1'], (x, y + 1))
        self.assertEqual(pos['e1'], (x + 1, y))
        self.assertEqual(pos['w1'], (x - 1, y))
        self.assertEqual(num['c'], 1)
        self.assertEqual(desl, [])

    def test_colisao_desloca_e_entorta(self):
        # a -e-> b -n-> c ; a -n-> d -e-> c' : c e d querem a mesma casa que "x"
        m = mapa(sala('a', {'e': 'b', 'n': 'd'}), sala('b', {'w': 'a', 'n': 'x'}), sala('d', {'s': 'a', 'e': 'y'}),
                 sala('x', {'s': 'b'}), sala('y', {'w': 'd'}))
        dados = G.montar(m)
        z = dados['zonas'][0]
        casas = [(s['x'], s['y']) for s in z['salas']]
        self.assertEqual(len(casas), len(set(casas)), 'duas salas na mesma casa')
        self.assertTrue(any(e['torta'] for e in z['arestas']))
        self.assertTrue(any(a['tipo'] == 'colisao' for a in dados['avisos']))

    def test_ilhas_nao_se_sobrepoem(self):
        m = mapa(sala('a', {'e': 'b'}), sala('b', {'w': 'a'}), sala('c', {'e': 'd'}), sala('d', {'w': 'c'}), sala('e', {}))
        z = G.montar(m)['zonas'][0]
        casas = [(s['x'], s['y']) for s in z['salas']]
        self.assertEqual(len(casas), 5)
        self.assertEqual(len(set(casas)), 5)

    def test_saida_so_de_ida_tambem_conecta(self):
        m = mapa(sala('a', {'e': 'b'}), sala('b', {}))
        salas = {r['id']: r for r in m['rooms']}
        pos, _, _ = G.layout_zona(['a', 'b'], salas, ['a'])
        self.assertEqual(pos['b'][0] - pos['a'][0], 1)


class TestAvisos(unittest.TestCase):
    def test_nao_reciproca_inexistente_pendente_duplicata(self):
        m = mapa(sala('a', {'e': 'b', 'n': 'fantasma'}, unresolved_exits=['oeste']), sala('b', {'w': 'c'}),
                 sala('c', {'e': 'b'}, duplicata_de='b'))
        tipos = {a['tipo'] for a in G.montar(m)['avisos']}
        self.assertTrue({'nao_reciproca', 'destino_inexistente', 'saida_pendente', 'duplicata'} <= tipos)


class TestHTML(unittest.TestCase):
    TEMPLATE = '<title>__HEROI__</title><script id="dados" type="application/json">__DADOS_JSON__</script>'

    def test_dados_embutidos_e_seguro_para_script(self):
        m = mapa(sala('a', {}, notes='</script><b>x</b>'))
        texto = G.html(G.montar(m), self.TEMPLATE)
        self.assertIn('<title>Teste</title>', texto)
        self.assertNotIn('</script><b>', texto)
        blob = texto.split('type="application/json">')[1].rsplit('</script>', 1)[0]
        self.assertEqual(json.loads(blob)['zonas'][0]['salas'][0]['notes'], '</script><b>x</b>')

    def test_deterministico(self):
        m = mapa(sala('a', {'e': 'b'}), sala('b', {'w': 'a'}))
        self.assertEqual(G.html(G.montar(m), self.TEMPLATE), G.html(G.montar(m), self.TEMPLATE))

    def test_template_real_sem_rede(self):
        t = G.TEMPLATE.read_text(encoding='utf-8')
        self.assertIn('__DADOS_JSON__', t)
        self.assertNotIn('fetch(', t)
        self.assertNotIn('<script src', t)
        self.assertNotIn('<link rel="stylesheet"', t)


class TestMapaReal(unittest.TestCase):
    def setUp(self):
        self.mapa = json.loads((G.ROOT / 'data' / 'heroes' / 'grebolius' / 'mapa.json').read_text(encoding='utf-8'))
        self.dados = G.montar(self.mapa)

    def test_todas_as_salas_uma_aba_por_zona(self):
        self.assertEqual(sum(z['n'] for z in self.dados['zonas']), len(self.mapa['rooms']))
        self.assertEqual(len(self.dados['zonas']), len({r.get('zone') for r in self.mapa['rooms']}))
        for z in self.dados['zonas']:
            casas = [(s['x'], s['y']) for s in z['salas']]
            self.assertEqual(len(casas), len(set(casas)), z['nome'])

    def test_tabuleiro_em_grade_8x8(self):
        z = next(z for z in self.dados['zonas'] if 'Tabuleiro' in z['nome'])
        pos = {s['id']: (s['x'], s['y']) for s in z['salas']}
        a1 = pos['xadrez_A1']
        for c, col in enumerate('ABCDEFGH'):
            for f in range(1, 9):
                self.assertEqual(pos['xadrez_%s%d' % (col, f)], (a1[0] + c, a1[1] - (f - 1)), '%s%d' % (col, f))


if __name__ == '__main__':
    unittest.main()
