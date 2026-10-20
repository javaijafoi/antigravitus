# -*- coding: utf-8 -*-
"""Testes do automato/acoes/ressuscitar.py (sem driver). Textos reais dos logs do Dia 156."""
import sys
import unittest
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ / 'automato' / 'acoes'))
import ressuscitar as R  # noqa: E402


class TestProximoComando(unittest.TestCase):
    def test_dica_de_energia_em_cada_direcao(self):
        for nome, d in (('leste', 'e'), ('norte', 'n'), ('oeste', 'w')):
            t = 'O Paraíso\nUma curiosa energia mágica, muito viva e tenaz, chama sua atenção para o %s.' % nome
            self.assertEqual(R.proximo_comando(t), d)

    def test_dica_de_saida_para_cima(self):
        t = 'Uma curiosa saída, para cima, chama sua atenção.\n[ Saídas: leste, oeste e cima ]'
        self.assertEqual(R.proximo_comando(t), 'u')

    def test_dica_quebrada_de_linha(self):
        self.assertEqual(R.proximo_comando('chama sua atenção\npara o oeste.'), 'w')

    def test_portal_fonte_e_vazio(self):
        self.assertEqual(R.proximo_comando('Um Portal Escondido no Paraíso\nVocê segue essa estranha energia'), 'enter portal')
        self.assertEqual(R.proximo_comando('226hp 490mn 146mv > A Fonte da Vida'), 'drink fonte')
        self.assertEqual(R.proximo_comando('O Vazio\nNada ao redor.'), 'n')

    def test_menu_de_morte_manda_raw_1(self):
        self.assertEqual(R.proximo_comando('Escolha uma das opções do menu!\nB o b  d o  D i a c h o'), '_RAW 1')
        self.assertEqual(R.proximo_comando('...\n  Menu Principal  \n'), '_RAW 1')

    def test_sem_dica_vai_ao_norte(self):
        self.assertEqual(R.proximo_comando('O Paraíso\nMagníficos campos verdes.'), 'n')


class TestUsaABase(unittest.TestCase):
    """Fala com o driver só por base.run: token certo, origem no transcript e guarda de repetição."""

    def test_sem_cliente_proprio(self):
        src = (RAIZ / 'automato' / 'acoes' / 'ressuscitar.py').read_text(encoding='utf-8')
        self.assertIn('from base import run', src)
        self.assertNotIn('import socket', src)
        self.assertNotIn('scripts/local/.controller', src)
        self.assertNotIn('farm_armaduras', src)


if __name__ == '__main__':
    unittest.main()
