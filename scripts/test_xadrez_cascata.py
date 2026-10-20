# -*- coding: utf-8 -*-
"""Testes das partes puras do xadrez_cascata (verificacao de casa, grade e caminho). Textos reais do Dia 157."""
import sys
import unittest
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ / 'automato' / 'acoes'))
import xadrez_cascata as xc

F1 = ("Uma Casa Branca\n   Você está em um quadrado de mármore branco. Esta normalmente é a casa   \n"
      "do Bispo do Rei Branco.   \n[ Saídas: norte, leste e oeste ]\nO Bispo Branco está aqui.\n226hp 490mn 146mv >")
E1 = ("Uma Casa Preta\n   Você está em um quadrado de mármore preto. Esta normalmente é a casa   \n"
      "do Rei Branco.  \n[ Saídas: norte, leste e oeste ]\nO Rei Branco está aqui.\n...ele está protegido por uma luz muito forte!")
H5 = "Uma Casa Branca\nVocê está em um quadrado de mármore branco. Há um grande portao enferrujado a leste.\n[ Saídas: norte, leste, sul e oeste ]"
A7 = ("Uma Casa Preta\n   Você está em um quadrado de mármore preto. Esta normalmente é a casa   \n"
      "de um peão da Rainha Negra.   \n[ Saídas: norte, leste e sul ]")
G7 = ("Uma Casa Preta\nVocê está em um quadrado de mármore preto. Esta normalmente é a\ncasa de um dos peões do Rei Negro. \n"
      "[ Saídas: norte, leste, sul e oeste ]")
MEIO = "Uma Casa Branca\n   Você está em um quadrado de mármore branco.  \n[ Saídas: norte, leste, sul e oeste ]"
D8 = ("Uma Casa Preta\n   Você está em um quadrado de mármore preto. Esta normalmente é a casa   \n"
      "da Rainha Negra.   \n[ Saídas: leste, sul, oeste e !baixo ]")


class TestVerificacao(unittest.TestCase):
    def test_casas_certas_passam(self):
        xc.verificar_casa(F1, *xc.parse_casa('F1'))
        xc.verificar_casa(E1, *xc.parse_casa('E1'))
        xc.verificar_casa(H5, *xc.parse_casa('H5'))
        xc.verificar_casa(A7, *xc.parse_casa('A7'))
        xc.verificar_casa(G7, *xc.parse_casa('G7'))
        xc.verificar_casa(MEIO, *xc.parse_casa('D5'))
        xc.verificar_casa(D8, *xc.parse_casa('D8'))

    def test_o_erro_de_E1_por_F1_e_pego(self):
        """Foi a causa da morte #12: achar que E1 era F1."""
        with self.assertRaises(xc.Perdida):
            xc.verificar_casa(E1, *xc.parse_casa('F1'))
        with self.assertRaises(xc.Perdida):
            xc.verificar_casa(F1, *xc.parse_casa('E1'))

    def test_cor_errada_e_pega(self):
        with self.assertRaises(xc.Perdida):
            xc.verificar_casa(MEIO, *xc.parse_casa('D4'))   # D4 = 4+4 par = Preta, texto Branca

    def test_peao_do_lado_errado(self):
        with self.assertRaises(xc.Perdida):
            xc.verificar_casa(A7, *xc.parse_casa('G7'))

    def test_casa_do_meio_nao_tem_peca(self):
        with self.assertRaises(xc.Perdida):
            xc.verificar_casa(A7, *xc.parse_casa('C5'))

    def test_saidas(self):
        self.assertEqual(xc.contar_saidas(H5), 4)
        self.assertEqual(xc.saidas_esperadas(*xc.parse_casa('H5')), 4)
        self.assertEqual(xc.saidas_esperadas(*xc.parse_casa('A1')), 2)
        self.assertEqual(xc.saidas_esperadas(*xc.parse_casa('D1')), 4)   # borda + !baixo
        self.assertEqual(xc.saidas_esperadas(*xc.parse_casa('C1')), 3)
        self.assertEqual(xc.saidas_esperadas(*xc.parse_casa('D4')), 4)
        with self.assertRaises(xc.Perdida):
            xc.verificar_casa(D8.replace('leste, sul, oeste e !baixo', 'norte'), *xc.parse_casa('D8'))  # saidas erradas

    def test_cores(self):
        self.assertEqual(xc.cor_casa(*xc.parse_casa('H1')), 'Branca')
        self.assertEqual(xc.cor_casa(*xc.parse_casa('A1')), 'Preta')
        self.assertEqual(xc.cor_casa(*xc.parse_casa('E8')), 'Branca')
        self.assertEqual(xc.cor_casa(*xc.parse_casa('D8')), 'Preta')


class TestCaminho(unittest.TestCase):
    def test_nunca_passa_por_casas_proibidas(self):
        for destino in ('F1', 'A8', 'H8', 'D7', 'C8', 'A1', 'H1', 'F8'):
            rota = xc.caminho_grade('H5', destino)
            casa = xc.parse_casa('H5')
            for d in rota:
                dc, df = xc.DIRS[d]
                casa = (casa[0] + dc, casa[1] + df)
                if xc.nome_casa(*casa) != destino:
                    self.assertNotIn(xc.nome_casa(*casa), xc.PROIBIDAS)

    def test_F1_vem_por_F2(self):
        rota = xc.caminho_grade('H5', 'F1')
        casa, vistas = xc.parse_casa('H5'), []
        for d in rota:
            dc, df = xc.DIRS[d]
            casa = (casa[0] + dc, casa[1] + df)
            vistas.append(xc.nome_casa(*casa))
        self.assertNotIn('G1', vistas)
        self.assertEqual(vistas[-1], 'F1')

    def test_proibida_como_destino_explicito_e_permitida(self):
        self.assertIsNotNone(xc.caminho_grade('F7', 'E8'))

    def test_tabuleiro_acompanha_passos(self):
        f7 = G7.replace('mármore preto', 'mármore branco').replace('Uma Casa Preta', 'Uma Casa Branca')
        tab = xc.Tabuleiro('G7', lambda d: (f7, {}, False))
        tab.passo('w')
        self.assertEqual(tab.casa, 'F7')

    def test_passo_para_casa_errada_levanta(self):
        # de F2 vai para F1 mas a resposta e' a de E1 (o erro da morte #12)
        with self.assertRaises(xc.Perdida):
            xc.Tabuleiro('F2', lambda d: (E1, {}, False)).passo('s')

    def test_recusa_levanta(self):
        tab = xc.Tabuleiro('F2', lambda d: ('Nah... você está muito relaxado..', {}, False))
        with self.assertRaises(xc.Perdida):
            tab.passo('s')


if __name__ == '__main__':
    unittest.main()
