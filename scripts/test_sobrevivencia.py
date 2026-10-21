# -*- coding: utf-8 -*-
"""Testes da diretiva §26: fome, sede, armadura, alvo do sono e portão do navegar.

Sem conexão com o MUD: o auditor lê registros na memória, o `minutos_de_sono` é
puro e o portão tem o `subprocess` trocado por um falso.
"""
import sys
import unittest
from pathlib import Path
from unittest import mock

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ / 'scripts'))
sys.path.insert(0, str(RAIZ / 'automato' / 'camadas'))
sys.path.insert(0, str(RAIZ / 'automato' / 'nucleo'))

import auditar_sessao as A  # noqa: E402
import navegar as N  # noqa: E402
import prepara as P  # noqa: E402


def cmd(c, texto='', hp=199, combate=False):
    return {'kind': 'command', 'cmd': c, 'text': texto, 'vitals': {'hp': hp},
            'in_combat': combate, 'at': '2026-10-20T15:00:00-03:00'}


def regras(regs):
    return {a['regra'].split(' ')[0] for a in A.auditar(regs)}


class TestSobrevivenciaNoAuditor(unittest.TestCase):
    def test_fome_em_sessao(self):
        self.assertIn('fome-em-sessao', regras([cmd('look', 'Você está morrendo de fome!')]))
        self.assertNotIn('fome-em-sessao', regras([cmd('look', 'Você está com fome.')]))

    def test_fome_e_uma_falha_por_sessao(self):
        seq = [cmd('look', 'Você está morrendo de fome! (-3hp)')] * 4
        self.assertEqual(sum(1 for a in A.auditar(seq) if a['regra'].startswith('fome-em-sessao')), 1)

    def test_sede_em_sessao(self):
        self.assertIn('sede-em-sessao', regras([cmd('look', 'Você está morrendo de sede!')]))

    def test_ataque_com_ca_sem_armor(self):
        seq = [cmd('score tudo', 'Classe de Armadura: 112'),
               cmd("cast 'lightning bolt' peao")]
        self.assertIn('armadura-ausente', regras(seq))

    def test_ataque_com_ca_de_armor_nao_falha(self):
        seq = [cmd('score tudo', 'Classe de Armadura: 148'),
               cmd("cast 'lightning bolt' peao")]
        self.assertNotIn('armadura-ausente', regras(seq))

    def test_sem_ca_no_transcript_nao_inventa_falha(self):
        self.assertNotIn('armadura-ausente', regras([cmd('kill peao')]))


class TestAlvoDoSono(unittest.TestCase):
    def test_vida_cheia_nao_dorme_por_tempo(self):
        self.assertEqual(P.minutos_de_sono(226, 226), 0)

    def test_deficit_vira_minutos_na_taxa_medida(self):
        # 176/226: falta 45 de vida; a ~5 hp/min da' 9 min
        self.assertEqual(P.minutos_de_sono(176, 226), 9)

    def test_respeita_o_teto_e_o_piso(self):
        self.assertEqual(P.minutos_de_sono(1, 1000), P.SONO_MINUTOS_MAX)
        # déficit pequeno não vira 0: o piso é o sono curto de mana/movimento
        self.assertEqual(P.minutos_de_sono(220, 226), P.SONO_MINUTOS_MIN)

    def test_le_a_vida_do_score(self):
        self.assertEqual(P.hp_do_score('Vida: {<<<<<>>>>>} 180 de 226'), (180, 226))
        self.assertEqual(P.hp_do_score('\nVida:  211 de 211'), (211, 211))
        self.assertEqual(P.hp_do_score('nada'), (None, None))

    def test_sem_leitura_nao_dorme(self):
        self.assertEqual(P.minutos_de_sono(None, None), 0)


class TestPortaoDoNavegar(unittest.TestCase):
    def test_portao_libera_quando_o_cuidar_esta_ok(self):
        with mock.patch('subprocess.run') as r:
            r.return_value = mock.Mock(returncode=0, stdout='[CUIDAR] ok', stderr='')
            self.assertEqual(N.cuidado_antes(), 0)

    def test_portao_devolve_o_pedido_de_recarga(self):
        with mock.patch('subprocess.run') as r:
            r.return_value = mock.Mock(returncode=2, stdout='[CUIDAR] precisa_repor=True', stderr='')
            self.assertEqual(N.cuidado_antes(), 2)

    def test_portao_devolve_falha_do_cuidado(self):
        with mock.patch('subprocess.run') as r:
            r.return_value = mock.Mock(returncode=1, stdout='', stderr='')
            self.assertEqual(N.cuidado_antes(), 1)


if __name__ == '__main__':
    unittest.main()
