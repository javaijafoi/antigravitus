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
import base as B  # noqa: E402
import config as C  # noqa: E402
import cuidar as CU  # noqa: E402
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
        self.assertEqual(P.minutos_de_sono(1, 1000), P.SONO_MINUTOS_REAIS_MAX)
        # déficit pequeno não vira 0: o piso é o sono curto de mana/movimento
        self.assertEqual(P.minutos_de_sono(220, 226), P.SONO_MINUTOS_REAIS_MIN)

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


class TestModoBreve(unittest.TestCase):
    """O `brief` corta a descrição da sala; quem liga tem de restaurar."""

    def test_le_o_estado_do_toggle(self):
        with mock.patch.object(B, 'run', return_value=('Modo breve: NAO', {}, False)):
            self.assertFalse(B.display_breve())
        with mock.patch.object(B, 'run', return_value=('Modo breve: SIM', {}, False)):
            self.assertTrue(B.display_breve())

    def test_nao_manda_brief_quando_ja_esta_ligado(self):
        enviados = []

        def falso(c, timeout=60.0):
            enviados.append(c)
            return ('Modo breve: SIM', {}, False)

        with mock.patch.object(B, 'run', side_effect=falso):
            self.assertTrue(B.brief(True))
        self.assertEqual(enviados, ['toggle'])

    def test_liga_e_devolve_o_estado_anterior_para_restaurar(self):
        enviados = []

        def falso(c, timeout=60.0):
            enviados.append(c)
            return ('Modo breve: NAO', {}, False) if c == 'toggle' else ('', {}, False)

        with mock.patch.object(B, 'run', side_effect=falso):
            self.assertFalse(B.brief(True))
        self.assertEqual(enviados, ['toggle', 'brief'])


MAPA = {
    'a': {'id': 'a', 'name': 'Praça', 'exits': {'e': 'b'}},
    'b': {'id': 'b', 'name': 'Rua Larga', 'exits': {'w': 'a', 'e': 'c'}},
    'c': {'id': 'c', 'name': 'Biblioteca', 'exits': {'w': 'b'}},
}


class FalsoMUD:
    def __init__(self, respostas):
        self.respostas, self.i, self.enviados = respostas, 0, []

    def __call__(self, c):
        self.enviados.append(c)
        if c in ('wake', 'stand'):
            return 'Você já está em pé.', {'hp': 199}, False
        t = self.respostas[min(self.i, len(self.respostas) - 1)]
        self.i += 1
        return t, {'hp': 199}, False


class TestGuardaDeArmadilha(unittest.TestCase):
    """§6: o aviso de armadilha mortal aborta em qualquer script, não só no milharal."""

    def test_andar_aborta_no_aviso(self):
        with mock.patch.object(B, 'run', return_value=('Você percebe que há algo perigoso por perto!', {}, False)):
            with self.assertRaises(B.PerigoMortal):
                B.andar('n')

    def test_navegar_para_com_codigo_7(self):
        mud = FalsoMUD(['Você percebe que há algo perigoso por perto!'])
        with self.assertRaises(N.Parada) as ctx:
            N.navegar(MAPA, 'a', 'c', mud, log=lambda *_: None)
        self.assertEqual(ctx.exception.codigo, 7)

    def test_passos_normais_nao_acionam(self):
        with mock.patch.object(B, 'run', return_value=('Rua Larga', {}, False)):
            self.assertTrue(B.andar('n'))


class TestPosturaAntesDeAndar(unittest.TestCase):
    """§8: recusa por postura custa um `wake; stand` e uma nova tentativa."""

    def test_andar_levanta_e_repete(self):
        enviados = []

        def falso(c, timeout=60.0):
            enviados.append(c)
            if c == 'n' and enviados.count('n') == 1:
                return ('Nah... você está muito relaxado..', {}, False)
            return ('Rua Larga', {}, False)

        with mock.patch.object(B, 'run', side_effect=falso):
            self.assertTrue(B.andar('n'))
        self.assertEqual(enviados, ['n', 'wake', 'stand', 'n'])

    def test_recusa_de_rota_continua_falsa(self):
        with mock.patch.object(B, 'run', return_value=('Você não pode ir por aí...', {}, False)):
            self.assertFalse(B.andar('n'))

    def test_navegar_levanta_uma_vez_e_segue(self):
        mud = FalsoMUD(['Nah... você está muito relaxado..',
                        'Rua Larga\n[ Saídas: oeste, leste ]',
                        'Biblioteca\n[ Saídas: oeste ]'])
        N.navegar(MAPA, 'a', 'c', mud, log=lambda *_: None)
        self.assertEqual(mud.enviados, ['e', 'wake', 'stand', 'e', 'e'])


class TestSonoObservado(unittest.TestCase):
    """O sono consulta o vigia durante a dormida (diretiva §13; vigia.do_driver é IPC, sem comando)."""

    def _rodar(self, estados):
        """Roda P.dormir() com relógio falso e o vigia devolvendo `estados` em ordem."""
        enviados, relogio = [], {'t': 0.0}

        class Tempo:
            @staticmethod
            def time():
                relogio['t'] += 10
                return relogio['t']

            @staticmethod
            def sleep(s):
                relogio['t'] += s

        def driver():
            if estados:
                return estados.pop(0)
            return {'supplies': {}, 'vitals': {'hp': 999}}

        with mock.patch.object(P, 'time', Tempo), \
             mock.patch.object(P, 'SONO_FATIA_S', 1), \
             mock.patch.object(P, 'minutos_de_sono', return_value=2), \
             mock.patch.object(P, 'voltar_ao_templo'), \
             mock.patch.object(P, 'situacao', return_value={'texto': 'Vida: 150 de 200'}): 
            with mock.patch.object(P, 'run', side_effect=lambda c, timeout=60.0: enviados.append(c) or ('', {}, False)), \
                 mock.patch.object(P, 'vigia') as v, \
                 mock.patch.object(P, 'comer_beber', return_value=['comeu']) as comeu:
                v.do_driver.side_effect = driver
                P.dormir()
        return enviados, comeu

    def test_fome_no_meio_acorda_e_come(self):
        enviados, comeu = self._rodar([
            {'supplies': {'fome': True}, 'vitals': {'hp': 150}},
            {'supplies': {'fome': False}, 'vitals': {'hp': 160}},
            {'supplies': {'fome': False}, 'vitals': {'hp': 170}},
            {'supplies': {'fome': False}, 'vitals': {'hp': 180}},
        ])
        self.assertTrue(comeu.called, 'com fome no meio do sono, tem de comer')
        self.assertIn('wake', enviados)
        self.assertIn('sleep', enviados)

    def test_vida_parada_para_o_sono(self):
        enviados, comeu = self._rodar([
            {'supplies': {}, 'vitals': {'hp': 150}},
            {'supplies': {}, 'vitals': {'hp': 150}},
            {'supplies': {}, 'vitals': {'hp': 150}},
            {'supplies': {}, 'vitals': {'hp': 150}},
        ])
        self.assertFalse(comeu.called)
        self.assertLessEqual(enviados.count('sleep'), 3, 'não pode dormir sem ganho')


    def test_sono_avisa_o_agente_quando_nao_enchE(self):
        """Diretiva 2026-10-21: passou do teto sem encher -> False + aviso, não silêncio."""
        enviados, relogio = [], {'t': 0.0}

        class Tempo:
            @staticmethod
            def time():
                relogio['t'] += 10
                return relogio['t']

            @staticmethod
            def sleep(s):
                relogio['t'] += s

        with mock.patch.object(P, 'time', Tempo), \
             mock.patch.object(P, 'SONO_FATIA_S', 1), \
             mock.patch.object(P, 'minutos_de_sono', return_value=2), \
             mock.patch.object(P, 'voltar_ao_templo'), \
             mock.patch.object(P, 'situacao', return_value={'texto': 'Vida: 150 de 200'}), \
             mock.patch.object(P, 'run', side_effect=lambda c, timeout=60.0: enviados.append(c) or ('', {}, False)), \
             mock.patch('sys.stdout') as saida:
            with mock.patch.object(P, 'vigia') as v:
                v.do_driver.return_value = {'supplies': {}, 'vitals': {'hp': 150}}
                resultado = P.dormir()
        self.assertFalse(resultado, 'sem encher, o sono tem de devolver False')
        texto = ''.join(str(c) for c in saida.write.call_args_list)
        self.assertIn('ATENCAO', texto)


class TestEscalaDoTempo(unittest.TestCase):
    """Hora de JOGO x hora real: o `score` fala em horas de jogo (ID: horas_de_jogo_para_segundos_reais)."""

    def test_24_horas_de_jogo_sao_30_minutos_reais(self):
        self.assertEqual(C.horas_de_jogo_para_segundos_reais(24), 1800)
        self.assertEqual(C.segundos_reais_para_horas_de_jogo(1800), 24)

    def test_2_horas_de_jogo_sao_2_minutos_e_meio(self):
        self.assertEqual(C.horas_de_jogo_para_segundos_reais(2), 150)

    def test_validade_da_magia_vem_da_escala_e_tem_margem(self):
        self.assertLess(C.VALIDADE_MAGIAS_SEGUNDOS, C.horas_de_jogo_para_segundos_reais(24))
        self.assertGreater(C.VALIDADE_MAGIAS_SEGUNDOS, 20 * 60)

    def test_escala_customizada(self):
        self.assertEqual(C.horas_de_jogo_para_segundos_reais(3, escala=60), 180)


class TestMagiaPorDado(unittest.TestCase):
    """Recastar é decisão por DADO (horas no `score`), não por timer (ID: horas_restantes)."""

    def test_le_as_horas_de_jogo_do_score(self):
        texto = ('armor                 (  24 horas ) +30 em ARMADURA\n'
                 'invisibility          (  12 horas ) +40 em ARMADURA')
        self.assertEqual(CU.horas_restantes(texto, 'armor'), 24)
        self.assertEqual(CU.horas_restantes(texto, 'invisibility'), 12)

    def test_magia_ausente_do_score_e_none(self):
        self.assertIsNone(CU.horas_restantes('nada de magia aqui', 'armor'))

    def test_abaixo_do_minimo_manda_reconjurar(self):
        self.assertLess(CU.horas_restantes('armor ( 2 horas )', 'armor'), CU.HORAS_MINIMAS_MAGIA)

    def test_com_horas_de_sobra_nao_reconjura(self):
        texto = 'armor ( 24 horas )\ninvisibility ( 12 horas )'
        with mock.patch.object(CU, 'situacao', return_value={'texto': texto}), \
             mock.patch.object(CU, 'config') as cfg, \
             mock.patch.object(CU, '_conjurar') as conj:
            cfg.USAR_INVISIBILIDADE = True
            r = CU.manter_magias()
        self.assertFalse(conj.called)
        self.assertTrue(r['cache'])

    def test_so_reconjura_o_que_esta_baixo(self):
        texto = 'armor ( 2 horas )\ninvisibility ( 12 horas )'
        with mock.patch.object(CU, 'situacao', return_value={'texto': texto}), \
             mock.patch.object(CU, 'sala_atual', return_value='praca do templo'), \
             mock.patch.object(CU, 'vida_frac', return_value=0.9), \
             mock.patch.object(CU, 'config') as cfg, \
             mock.patch.object(CU, '_conjurar', return_value=(True, 'sente alguem te protegendo')) as conj:
            cfg.USAR_INVISIBILIDADE = True
            CU.manter_magias()
        self.assertEqual([c.args[0] for c in conj.call_args_list], ['armor'])


if __name__ == '__main__':
    unittest.main()
