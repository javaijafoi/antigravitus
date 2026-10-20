# -*- coding: utf-8 -*-
"""Testes do prepara.garantir_armor: a magia fica na rotina de preparo, nao no script de ataque (diretiva do autor, Dia 157)."""
import sys
import unittest
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ / 'automato' / 'camadas'))
sys.path.insert(0, str(RAIZ / 'automato' / 'nucleo'))
sys.path.insert(0, str(RAIZ / 'automato'))
import prepara


def score(ca):
    return 'Destreza: 17            Carisma: 12      Classe de Armadura: %d\nVida: 1' % ca


class TestGarantirArmor(unittest.TestCase):
    def setUp(self):
        self.cmds = []
        self.cas = [112, 148]
        self.orig = (prepara.situacao, prepara.run, prepara.andar)
        prepara.situacao = lambda *a, **k: {'texto': score(self.cas.pop(0) if len(self.cas) > 1 else self.cas[0])}
        prepara.run = lambda c, *a, **k: (self.cmds.append(c) or ('', {}, False))
        prepara.andar = lambda d: self.cmds.append('andar ' + d)

    def tearDown(self):
        prepara.situacao, prepara.run, prepara.andar = self.orig

    def test_le_a_ca_do_score(self):
        self.assertEqual(prepara.ca_do_score(score(157)), 157)
        self.assertIsNone(prepara.ca_do_score('sem score'))

    def test_lanca_quando_a_ca_caiu(self):
        self.assertTrue(prepara.garantir_armor())
        self.assertIn("cast 'armor'", self.cmds)
        self.assertEqual(self.cmds[0], 'recall')          # Templo bloqueia magia: sai antes
        self.assertIn('andar s', self.cmds)

    def test_nao_lanca_com_armor_ligada(self):
        self.cas = [157]
        self.assertFalse(prepara.garantir_armor())
        self.assertEqual(self.cmds, [])

    def test_leitura_falha_nao_lanca(self):
        prepara.situacao = lambda *a, **k: {'texto': ''}
        self.assertFalse(prepara.garantir_armor())
        self.assertEqual(self.cmds, [])


if __name__ == '__main__':
    unittest.main()
