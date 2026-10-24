# -*- coding: utf-8 -*-
"""Testes da regra de moral (diretiva do autor, 2026-10-22, diretiva_de_jogo.md §27), sem driver.

Nada que abaixe o alinhamento e' abatido, mesmo hostil; `consider` so' para bicho novo.
"""
import sys
import unittest
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ / 'scripts'))
for sub in ('nucleo', 'camadas'):
    sys.path.insert(0, str(RAIZ / 'automato' / sub))
import auditar_sessao as A  # noqa: E402
import config as C  # noqa: E402
import turno as T  # noqa: E402

SCORE = ("   Alinhamento: {<<<<<>>---}   312 - Você é bom.\n"
         "         Força: 11       Constituição: 9                   Acerto: 11\n")


class TestRotinasBanidas(unittest.TestCase):
    def test_milharal_esta_banido_por_moral(self):
        for nome in ('milharal_v2', 'milharal'):
            self.assertIn(nome, C.ROTINAS_BANIDAS_POR_MORAL)
            self.assertTrue(T.rotina_banida(nome))
        self.assertIn('415 para 312', T.rotina_banida('milharal_v2'))

    def test_outra_rotina_nao_e_banida(self):
        self.assertIsNone(T.rotina_banida('novatos'))

    def test_turno_recusa_rotina_banida_com_codigo_6(self):
        from unittest import mock
        with mock.patch.object(sys, 'argv', ['turno.py', '--rotina', 'milharal_v2']):
            self.assertEqual(T.main(), T.CODIGO_BANIDA)
        self.assertEqual(T.CODIGO_BANIDA, 6)


class TestAlinhamento(unittest.TestCase):
    def test_le_o_numero_do_score(self):
        self.assertEqual(T.alinhamento_do_score(SCORE), 312)
        self.assertEqual(T.alinhamento_do_score("Alinhamento: {<<<<<>>>>>}   -40 - Você é mau."), -40)

    def test_sem_score_devolve_none(self):
        self.assertIsNone(T.alinhamento_do_score(''))
        self.assertIsNone(T.alinhamento_do_score(None))
        self.assertIsNone(T.alinhamento_do_score('Menu Principal'))

    def test_codigos_distintos(self):
        self.assertNotEqual(T.CODIGO_BANIDA, T.CODIGO_MORAL)


def _reg(cmd, texto=''):
    return {'kind': 'command', 'cmd': cmd, 'text': texto, 'origem': 'play'}


class TestConsiderSoParaBichoNovo(unittest.TestCase):
    def regras(self, comandos):
        return [a['regra'] for a in A.auditar([_reg(c) for c in comandos])]

    def test_pecas_do_tabuleiro_nao_pedem_consider(self):
        for alvo in ('rei', 'rainha', 'bispo', 'cavaleiro', 'torre', 'peao'):
            regras = self.regras(["cast 'sleep' %s" % alvo])
            self.assertFalse(any(r.startswith('ataque-sem-consider') for r in regras), alvo)

    def test_bicho_novo_continua_pedindo_consider(self):
        regras = self.regras(["cast 'lightning bolt' dragaozinho"])
        self.assertTrue(any(r.startswith('ataque-sem-consider') for r in regras))

    def test_bicho_novo_com_consider_passa(self):
        regras = self.regras(['consider dragaozinho', "cast 'lightning bolt' dragaozinho"])
        self.assertFalse(any(r.startswith('ataque-sem-consider') for r in regras))

    def test_conhecidos_sao_so_as_pecas(self):
        self.assertEqual(A.CONHECIDOS, {'peao', 'peão', 'bispo', 'cavaleiro', 'cavalo', 'torre', 'rainha', 'rei'})


if __name__ == '__main__':
    unittest.main()
