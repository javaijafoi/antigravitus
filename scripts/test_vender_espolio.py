# -*- coding: utf-8 -*-
"""Testes do vender_espolio: whitelist, oferta antes do sell e parada quando o caixa seca."""
import sys
import unittest
from pathlib import Path
from unittest import mock

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ / 'automato' / 'rotinas'))
import vender_espolio as V


class TestFiltro(unittest.TestCase):
    def test_arma_e_armadura_sao_vendaveis(self):
        self.assertTrue(V.vendavel('uma espada longa'))
        self.assertTrue(V.vendavel('um escudo de aço'))
        self.assertTrue(V.vendavel('a armadura de um peão negro'))

    def test_protegidos_nunca_entram(self):
        for nome in ('o tomo da sabedoria druídica', 'um cetro do bispo negro',
                     'a Coroa da Rainha Negra', 'a mochila de Pellinore',
                     'um rosário', 'um colar com uma pedra púrpura'):
            self.assertFalse(V.vendavel(nome), nome)

    def test_entulho_nao_entra(self):
        for nome in ('um pão recheado', 'um cantil', 'um pergaminho de retorno'):
            self.assertFalse(V.vendavel(nome), nome)


class TestOferta(unittest.TestCase):
    def test_le_a_oferta_com_e_sem_ponto(self):
        with mock.patch.object(V, 'run', return_value=('Ele oferece 4.000 moedas.', {}, False)):
            self.assertEqual(V.oferta('lança'), 4000)
        with mock.patch.object(V, 'run', return_value=('Ele oferece 150 moedas.', {}, False)):
            self.assertEqual(V.oferta('escudo'), 150)

    def test_sem_oferta_devolve_none(self):
        with mock.patch.object(V, 'run', return_value=('Nao compro isso.', {}, False)):
            self.assertIsNone(V.oferta('x'))


class TestFluxo(unittest.TestCase):
    def _rodar(self, itens, respostas, minimo=200, max_itens=6):
        enviados = []

        def run(cmd, timeout=60.0):
            enviados.append(cmd)
            return respostas.get(cmd, ('', {}, False))

        with mock.patch.object(V, 'run', side_effect=run), \
             mock.patch.object(V, 'inventario', return_value=itens), \
             mock.patch.object(V, '_ir', return_value=True), \
             mock.patch.object(V, 'ouro', return_value=1000), \
             mock.patch.dict(sys.modules, {'cuidar': mock.Mock(cuidar=lambda *a, **k: None)}):
            rel = V.executar(max_itens=max_itens, minimo=minimo)
        return enviados, rel

    def test_vende_so_acima_do_minimo(self):
        itens = ['uma espada longa', 'um escudo de aço']
        respostas = {
            'value uma espada longa': ('Ele oferece 40 moedas.', {}, False),
            'value um escudo de aço': ('Ele oferece 200 moedas.', {}, False),
            'sell um escudo de aço': ('Você vende por 200 moedas.', {}, False),
        }
        enviados, rel = self._rodar(itens, respostas, minimo=200)
        self.assertIn('sell um escudo de aço', enviados)
        self.assertNotIn('sell uma espada longa', enviados)
        self.assertEqual(rel['vendidos'][0]['item'], 'um escudo de aço')

    def test_recusa_para_o_comerciante(self):
        itens = ['uma espada longa', 'uma adaga']
        respostas = {
            'value uma espada longa': ('Ele oferece 500 moedas.', {}, False),
            'sell uma espada longa': ('Eu nao posso pagar por uma arma dessas!', {}, False),
            'value uma adaga': ('Ele oferece 500 moedas.', {}, False),
            'sell uma adaga': ('Você vende por 500 moedas.', {}, False),
        }
        enviados, rel = self._rodar(itens, respostas, minimo=200)
        self.assertIn('sell uma espada longa', enviados)
        self.assertNotIn('sell uma adaga', enviados, 'depois da recusa nao insiste')
        self.assertEqual(rel['recusas'][0]['item'], 'uma espada longa')

    def test_item_protegido_nem_e_consultado(self):
        itens = ['o tomo da sabedoria druídica', 'a Coroa da Rainha Negra']
        enviados, rel = self._rodar(itens, {})
        self.assertFalse([c for c in enviados if c.startswith('value')])
        self.assertEqual(rel['vendidos'], [])


if __name__ == '__main__':
    unittest.main()
