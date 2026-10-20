# -*- coding: utf-8 -*-
"""Testes do mapeamento do tabuleiro de xadrez (grade 8x8 da zona 36)."""
import copy
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import mapear_tabuleiro as mt


class TestTabuleiro(unittest.TestCase):
    def setUp(self):
        self.salas = {s['id']: s for s in mt.casas()}

    def test_64_casas(self):
        self.assertEqual(len(self.salas), 64)

    def test_cantos_bordas_interior(self):
        self.assertEqual(len(self.salas['xadrez_A1']['exits']), 2)   # canto
        self.assertEqual(len(self.salas['xadrez_H8']['exits']), 2)
        self.assertEqual(len(self.salas['xadrez_D1']['exits']), 3)   # borda
        self.assertEqual(len(self.salas['xadrez_D4']['exits']), 4)   # interior
        # H5 tem a saida extra do portao a leste: 4 saidas (n, s, w, e)
        self.assertEqual(self.salas['xadrez_H5']['exits']['e'], 'grande_tabuleiro_portao')
        self.assertEqual(len(self.salas['xadrez_H5']['exits']), 4)

    def test_cores_como_vistas_ao_vivo(self):
        self.assertEqual(self.salas['xadrez_H1']['name'], 'Uma Casa Branca')   # Torre do Rei Branco
        self.assertEqual(self.salas['xadrez_F1']['name'], 'Uma Casa Branca')   # Bispo Branco
        self.assertEqual(self.salas['xadrez_A1']['name'], 'Uma Casa Preta')    # Torre da Rainha Branca
        self.assertEqual(self.salas['xadrez_E8']['name'], 'Uma Casa Branca')   # Rei Negro
        self.assertEqual(self.salas['xadrez_D8']['name'], 'Uma Casa Preta')    # Rainha Negra
        self.assertEqual(self.salas['xadrez_A8']['name'], 'Uma Casa Branca')   # Torre da Rainha
        self.assertEqual(self.salas['xadrez_H5']['name'], 'Uma Casa Branca')   # entrada

    def test_arestas_simetricas(self):
        oposto = mt.OPOSTO
        for sala in self.salas.values():
            for d, destino in sala['exits'].items():
                if destino in self.salas:
                    self.assertEqual(self.salas[destino]['exits'][oposto[d]], sala['id'])

    def test_riscos_do_rei(self):
        self.assertEqual(self.salas['xadrez_E8']['risk_code'], 'danger')
        self.assertEqual(self.salas['xadrez_E8']['risk'], 'Extremo')

    def test_aplicar_e_idempotente(self):
        mapa = {'rooms': [{'id': 'grande_tabuleiro_portao', 'exits': {}, 'notes': ''}], 'total_rooms': 1}
        n1, a1 = mt.aplicar(mapa)
        copia = copy.deepcopy(mapa)
        n2, a2 = mt.aplicar(mapa)
        self.assertEqual((n1, a1), (64, 0))
        self.assertEqual((n2, a2), (0, 64))
        self.assertEqual(mapa['rooms'][1:], copia['rooms'][1:])
        self.assertEqual(mapa['rooms'][0]['exits']['w'], 'xadrez_H5')
        self.assertEqual(mapa['total_rooms'], 65)
        self.assertEqual(mapa['rooms'][0]['risk_code'], 'medium')


if __name__ == '__main__':
    unittest.main()
