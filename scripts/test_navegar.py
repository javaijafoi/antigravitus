# -*- coding: utf-8 -*-
"""Testes do navegar.py: sufixo de curadoria, origem homônima e a rota que veio do nav.py.

Sem conexão com o MUD. Os casos vêm do primeiro uso ao vivo (registro_de_evolucao.md,
Dia 157, Plano 033): o navegador parou em "A Rua Principal" contra "A Rua Principal (Oeste)"
e não deduziu a origem em "A Praça do Templo", que tem duas salas no mapa.
"""
import sys
import unittest
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ / 'automato' / 'camadas'))
sys.path.insert(0, str(RAIZ / 'automato' / 'rotas'))

import navegar as N  # noqa: E402

MAPA = {
    'praca': {'id': 'praca', 'name': 'A Praça do Comércio', 'layer': 'superficie', 'exits': {'w': 'rua_o'}},
    'rua_o': {'id': 'rua_o', 'name': 'A Rua Principal (Oeste)', 'layer': 'superficie', 'exits': {'e': 'praca', 'n': 'sala'}},
    'sala': {'id': 'sala', 'name': 'A Sala de Doações de Midgaard', 'aliases': ['A Sala de Doações'],
             'layer': 'superficie', 'exits': {'s': 'rua_o'}},
    'templo': {'id': 'templo', 'name': 'A Praça do Templo', 'layer': 'superficie', 'exits': {}},
    'lv1': {'id': 'lv1', 'name': 'A Praça do Templo', 'layer': 'levantamento', 'exits': {}},
    'beco1': {'id': 'beco1', 'name': 'O Beco Escuro', 'layer': 'jareth_fazenda', 'exits': {}},
    'beco2': {'id': 'beco2', 'name': 'O Beco Escuro', 'layer': 'jareth_fazenda', 'exits': {}},
}

# A rota fixa do antigo automato/rotas/nav.py (andada ao vivo no Dia 157 sem desvio):
# (direção, nome esperado da sala de chegada), como o jogo mostra o título.
TEMPLO_A_PRACA_JARETH = (
    [('n', 'O Altar do Templo'), ('n', 'Atrás do Altar')]
    + [('n', 'O Grande Campo de Midgaard')] * 3
    + [('n', 'Um Caminho Dentre os Campos'), ('e', 'Um Caminho Dentre os Campos'),
       ('n', 'O Começo da Estrada'), ('n', 'A Estrada Midgaard-Jareth'), ('n', 'A Estrada Midgaard-Jareth'),
       ('n', 'Um Posto de Guarda na Estrada'), ('n', 'Numa Pequena Vila'), ('n', 'O Centro do Vilarejo'),
       ('n', 'Numa Pequena Vila'), ('n', 'Um Posto de Guarda na Estrada'),
       ('n', 'A Estrada Midgaard-Jareth'), ('n', 'A Estrada Midgaard-Jareth')]
    + [('e', 'A Estrada Midgaard-Jareth')] * 5
    + [('e', 'Nas Proximidades da Cidade'), ('e', 'O Portão Oeste'), ('e', 'Avenida Floris'), ('e', 'Uma Praça')]
)


class FalsoMUD:
    def __init__(self, respostas):
        self.respostas, self.enviados = list(respostas), []

    def __call__(self, c):
        self.enviados.append(c)
        return self.respostas.pop(0), {'hp': 199}, False


class TestSufixoDeCuradoria(unittest.TestCase):
    def test_titulo_real_bate_com_nome_curado(self):
        self.assertTrue(N.confere(MAPA['rua_o'], 'A Rua Principal'))
        self.assertTrue(N.confere(MAPA['rua_o'], 'A Rua Principal (Oeste)'))
        self.assertTrue(N.confere(MAPA['sala'], 'A Sala de Doações'))  # alias

    def test_titulo_diferente_continua_parando(self):
        self.assertFalse(N.confere(MAPA['rua_o'], 'Rua Principal'))
        self.assertFalse(N.confere(MAPA['rua_o'], 'A Rua Principal Leste'))

    def test_navegar_nao_para_no_sufixo(self):
        mud = FalsoMUD(['A Rua Principal\n[ Saídas: norte, leste ]', 'A Sala de Doações\n[ Saídas: sul ]'])
        feitos = N.navegar(MAPA, 'praca', 'sala', mud, log=lambda *_: None)
        self.assertEqual(mud.enviados, ['w', 'n'])
        self.assertEqual([i for _, i in feitos], ['rua_o', 'sala'])

    def test_navegar_ainda_para_em_sala_errada(self):
        with self.assertRaises(N.Parada) as ctx:
            N.navegar(MAPA, 'praca', 'sala', FalsoMUD(['A Praça do Templo\n']), log=lambda *_: None)
        self.assertEqual(ctx.exception.codigo, 3)


class TestOrigemHomonima(unittest.TestCase):
    def test_prefere_a_unica_sala_curada(self):
        self.assertEqual(N.deduzir_origem(MAPA, 'A Praça do Templo'), 'templo')

    def test_titulo_com_sufixo_tem_candidato_unico(self):
        self.assertEqual(N.deduzir_origem(MAPA, 'A Rua Principal'), 'rua_o')

    def test_varias_curadas_pede_de_com_os_ids(self):
        with self.assertRaises(N.Parada) as ctx:
            N.deduzir_origem(MAPA, 'O Beco Escuro')
        self.assertEqual(ctx.exception.codigo, 2)
        self.assertIn('--de', ctx.exception.motivo)
        self.assertIn('beco1, beco2', ctx.exception.motivo)

    def test_sem_candidato_pede_de(self):
        with self.assertRaises(N.Parada) as ctx:
            N.deduzir_origem(MAPA, 'Uma Sala Que Não Existe')
        self.assertIn('--de', ctx.exception.motivo)

    def test_de_explicito_desempata_e_confere_o_look(self):
        self.assertEqual(N.deduzir_origem(MAPA, 'O Beco Escuro', de='beco2'), 'beco2')
        self.assertEqual(N.deduzir_origem(MAPA, 'A Praça do Templo', de='lv1'), 'lv1')
        with self.assertRaises(N.Parada) as c1:
            N.deduzir_origem(MAPA, 'A Praça do Comércio', de='beco2')
        self.assertEqual(c1.exception.codigo, 3)
        with self.assertRaises(N.Parada) as c2:
            N.deduzir_origem(MAPA, 'O Beco Escuro', de='nao_existe')
        self.assertEqual(c2.exception.codigo, 2)

    def test_mapa_real_praca_do_templo(self):
        salas = N.carregar_mapa()
        self.assertGreater(len(N.candidatos_por_titulo(salas, 'A Praça do Templo')), 1)
        self.assertEqual(N.deduzir_origem(salas, 'A Praça do Templo'), 'praca_templo')
        self.assertEqual(N.deduzir_origem(salas, 'A Rua Principal'), 'rua_oeste_1')


class TestRotaDoNavPy(unittest.TestCase):
    """A rota do nav.py virou arestas do mapa.json: o navegar.py faz o mesmo trajeto."""

    def setUp(self):
        self.salas = N.carregar_mapa()

    def test_templo_a_praca_de_jareth_igual_ao_nav_py(self):
        p = N.caminho(self.salas, 'templo_midgaard', 'lb013')
        self.assertEqual([d for d, _ in p], [d for d, _ in TEMPLO_A_PRACA_JARETH])
        for k, ((_, sala), (_, nome)) in enumerate(zip(p, TEMPLO_A_PRACA_JARETH), 1):
            self.assertTrue(N.confere(self.salas[sala], nome), 'passo %d: %s não aceita "%s"' % (k, sala, nome))

    def test_jareth_centro_fica_tres_passos_a_leste_da_praca(self):
        p = N.caminho(self.salas, 'templo_midgaard', 'jareth_centro')
        self.assertEqual([d for d, _ in p], [d for d, _ in TEMPLO_A_PRACA_JARETH] + ['e', 'e', 'e'])
        self.assertEqual([i for _, i in p[-4:]], ['lb013', 'lb014', 'lb015', 'jareth_centro'])

    def test_falso_mud_anda_a_rota_inteira(self):
        mud = FalsoMUD(['%s\n[ Saídas: ... ]' % nome for _, nome in TEMPLO_A_PRACA_JARETH])
        feitos = N.navegar(self.salas, 'templo_midgaard', 'lb013', mud, log=lambda *_: None)
        self.assertEqual(len(feitos), 26)

    def test_nav_py_so_repassa(self):
        import nav
        self.assertEqual(nav.ROTAS['templo-praca-jareth'], 'lb013')
        for destino in nav.ROTAS.values():
            self.assertIn(destino, self.salas)
        self.assertEqual(nav.main(['templo-praca-jareth', '--de', '3']), 2)
        self.assertEqual(nav.main(['rota-que-nao-existe']), 2)


if __name__ == '__main__':
    unittest.main()
