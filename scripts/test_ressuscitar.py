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


INVENTARIO_APOS_MORTE = """Você está carregando:
um diminuto brinco de novato ..Isso tem uma pequena aura! (novo)
um cajado retorcido
uma lâmina de ferro (novo)
um bracelete de prata e ouro ..Isso emite um som estridente!
um rosário ..Isso tem uma pequena aura!
um belo cinturão de rodeio ..Isso tem uma pequena aura! (novo)
a mochila de Pellinore
um escudo de aço (novo)
um par de braçadeiras de novato (novo)
um par de luvas de couro (muito gasto)
uma calça de couro (muito gasto)
resistentes botas negras (novo)
uma veste de escamas de metal ..Isso tem uma pequena aura! (novo)
a coleira do dragão de estimação (novo)
a Coroa da Rainha Branca ..Isso emite um som estridente! (novo)
uma Cruz Ansada ..Isso tem uma pequena aura!
um colar com uma pedra púrpura ..Isso tem uma pequena aura! (novo)
o anel de rubi do Cardeal ..Isso tem uma pequena aura! (novo)
um anel dourado
um tomo da sabedoria druídica(+3L)
um cantil
(x4) um pão recheado
um manto de pano (novo)
a Lança do Cavaleiro Negro ..Isso emite um som estridente! (novo)
"""


class TestPosMorte(unittest.TestCase):
    """Dia 161: a morte devolve o equipamento desvestido; a ressurreicao tem de reequipar e alimentar."""

    def test_come_bebe_e_reequipa_item_a_item(self):
        cmds = R.comandos_pos_morte(INVENTARIO_APOS_MORTE)
        self.assertEqual(cmds[:2], ['eat pao', 'drink cantil'])
        for esperado in ('wear coroa', 'wear brinco', 'wear colar', 'wear cruz', 'wear mochila', 'wear bracadeiras',
                         'wear luvas', 'wear rosario', 'wear bracelete', 'wear escudo', 'wear cinturao',
                         'wear calca', 'wear dourado', 'wear rubi', 'wear veste', 'wear botas', 'wear coleira', 'wield ferro', 'hold cajado'):
            self.assertIn(esperado, cmds)

    def test_nunca_wear_all_nem_toca_na_lanca_maldita_ou_no_manto(self):
        cmds = ' '.join(R.comandos_pos_morte(INVENTARIO_APOS_MORTE))
        self.assertNotIn('all', cmds)
        self.assertNotIn('lanca', cmds)
        self.assertNotIn('manto', cmds)   # a mochila ocupa o corpo; o manto fica no inventario

    def test_duas_coroas_no_inventario_nao_veste_nenhuma(self):
        inv = INVENTARIO_APOS_MORTE + 'a Coroa da Rainha Negra ..Isso emite um som estridente!\n'
        self.assertNotIn('wear coroa', R.comandos_pos_morte(inv))

    def test_inventario_vazio_nao_manda_nada(self):
        self.assertEqual(R.comandos_pos_morte(''), [])
        self.assertEqual(R.comandos_pos_morte(None), [])


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
