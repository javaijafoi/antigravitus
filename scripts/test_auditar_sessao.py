# -*- coding: utf-8 -*-
"""Testes do auditar_sessao.py e do navegar.py (sem conexão com o MUD)."""
import sys
import unittest
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ / 'scripts'))
sys.path.insert(0, str(RAIZ / 'automato' / 'camadas'))

import auditar_sessao as A  # noqa: E402
import navegar as N  # noqa: E402


def cmd(c, texto='', hp=199, combate=False, at='2026-10-19T14:00:00-03:00'):
    return {'kind': 'command', 'cmd': c, 'text': texto, 'vitals': {'hp': hp}, 'in_combat': combate, 'at': at}


def regras(regs):
    return {a['regra'].split(' ')[0] for a in A.auditar(regs)}


class TestAuditor(unittest.TestCase):
    def test_repeticao_de_recusa(self):
        recusa = 'Você não pode ir por aí...'
        self.assertIn('repeticao-de-recusa', regras([cmd('e', recusa)] * 3))
        self.assertNotIn('repeticao-de-recusa', regras([cmd('e', recusa)] * 2))

    def test_recusa_com_acento_perdido(self):
        self.assertIn('repeticao-de-recusa', regras([cmd('e', 'Voc� n�o pode ir por a�...')] * 3))

    def test_quit(self):
        self.assertIn('quit', regras([cmd('quit')]))

    def test_give_exige_etapa_no_score(self):
        self.assertIn('give-sem-etapa', regras([cmd('give tomo lemin')]))
        ok = [cmd('score tudo', 'Ajuda Mágica: Você deve entregar objeto ao personagem.'), cmd('give tomo lemin')]
        self.assertNotIn('give-sem-etapa', regras(ok))
        sem_instrucao = [cmd('score tudo', 'Ajuda Mágica'), cmd('give tomo lemin')]
        self.assertIn('give-sem-etapa', regras(sem_instrucao))

    def test_give_consome_a_etapa(self):
        seq = [cmd('score tudo', 'x: Você deve entregar objeto ao personagem.'), cmd('give a lemin'), cmd('give b lemin')]
        self.assertEqual(sum(1 for a in A.auditar(seq) if a['regra'].startswith('give-sem-etapa')), 1)

    def test_fala_em_lote(self):
        self.assertIn('fala-em-lote', regras([cmd('say sim;say Merlin')]))

    def test_fala_em_rajada(self):
        a = cmd('say sim', at='2026-10-19T14:00:00-03:00')
        b = cmd('say Merlin', at='2026-10-19T14:00:01-03:00')
        self.assertIn('fala-em-rajada', regras([a, b]))
        c = cmd('say Merlin', at='2026-10-19T14:00:30-03:00')
        self.assertNotIn('fala-em-rajada', regras([a, c]))

    def test_ataque_sem_consider(self):
        self.assertIn('ataque-sem-consider', regras([cmd('kill malandro')]))
        self.assertNotIn('ataque-sem-consider', regras([cmd('consider malandro'), cmd('kill malandro')]))

    def test_get_all_e_get_sem_identify(self):
        self.assertIn('get-all', regras([cmd('get all corpo')]))
        self.assertIn('get-sem-identify', regras([cmd('get armadura')]))
        self.assertNotIn('get-sem-identify', regras([cmd('identify armadura'), cmd('get armadura')]))

    def test_alinhamento_caiu(self):
        a = cmd('score tudo', 'Alinhamento: {<<<<<>>---}   412 - Você é bom.')
        b = cmd('score tudo', 'Alinhamento: {<<<<<>>---}   400 - Você é bom.')
        self.assertIn('alinhamento-caiu', regras([a, b]))
        self.assertNotIn('alinhamento-caiu', regras([a, a]))

    def test_recuo_a_pe_com_vida_baixa(self):
        seq = [cmd('look', hp=199), cmd('s', hp=40, combate=True), cmd('n', hp=40, combate=True)]
        self.assertIn('recuo-a-pe', regras(seq))
        seq2 = [cmd('look', hp=199), cmd('s', hp=40, combate=True), cmd('recall', hp=40)]
        self.assertNotIn('recuo-a-pe', regras(seq2))

    def test_sessao_sem_fecho(self):
        self.assertIn('sessao-sem-fecho', regras([cmd('look')]))
        fechada = [cmd('look'), {'kind': 'close', 'save_confirmed': True}]
        self.assertNotIn('sessao-sem-fecho', regras(fechada))

    def test_sessao_limpa_nao_tem_falha(self):
        seq = [cmd('look'), cmd('n'), cmd('score tudo', 'Alinhamento: {<<<>>}   412')]
        self.assertFalse([a for a in A.auditar(seq) if a['nivel'] == A.FALHA])


MAPA = {
    'a': {'id': 'a', 'name': 'Praça', 'exits': {'e': 'b'}},
    'b': {'id': 'b', 'name': 'Rua Larga', 'exits': {'w': 'a', 'e': 'c', 'n': 'r'}},
    'c': {'id': 'c', 'name': 'Biblioteca', 'exits': {'w': 'b'}},
    'r': {'id': 'r', 'name': 'Beco Escuro', 'risk_code': 'danger', 'exits': {'s': 'b', 'e': 'c'}},
}


class FalsoMUD:
    """Responde como o driver: título da sala de destino na primeira linha."""
    def __init__(self, respostas, vitals=None, combate=False):
        self.respostas, self.i, self.vitals, self.combate, self.enviados = respostas, 0, vitals or {'hp': 199}, combate, []

    def __call__(self, c):
        self.enviados.append(c)
        t = self.respostas[self.i]
        self.i += 1
        return t, self.vitals, self.combate


class TestNavegar(unittest.TestCase):
    def test_caminho_minimo_e_titulo(self):
        self.assertEqual([d for d, _ in N.caminho(MAPA, 'a', 'c')], ['e', 'e'])
        self.assertEqual(N.titulo('199hp 430mn 145mv > Biblioteca\nTexto'), 'Biblioteca')
        self.assertEqual(N.titulo('DICA: x\n\nRua Larga\n'), 'Rua Larga')

    def test_evita_sala_perigosa_por_padrao(self):
        self.assertEqual([i for _, i in N.caminho(MAPA, 'a', 'r')] if N.caminho(MAPA, 'a', 'r') else None, None)
        self.assertEqual([i for _, i in N.caminho(MAPA, 'a', 'r', permitir_risco=True)], ['b', 'r'])

    def test_chega_e_so_envia_direcoes(self):
        mud = FalsoMUD(['Rua Larga\n[ Saídas: oeste ]', 'Biblioteca\n[ Saídas: oeste ]'])
        N.navegar(MAPA, 'a', 'c', mud, log=lambda *_: None)
        self.assertEqual(mud.enviados, ['e', 'e'])

    def test_para_em_sala_inesperada(self):
        mud = FalsoMUD(['Praça\n'])
        with self.assertRaises(N.Parada) as ctx:
            N.navegar(MAPA, 'a', 'c', mud, log=lambda *_: None)
        self.assertEqual(ctx.exception.codigo, 3)

    def test_para_em_recusa_e_em_combate(self):
        with self.assertRaises(N.Parada) as c1:
            N.navegar(MAPA, 'a', 'c', FalsoMUD(['Você não pode ir por aí...']), log=lambda *_: None)
        self.assertEqual(c1.exception.codigo, 5)
        with self.assertRaises(N.Parada) as c2:
            N.navegar(MAPA, 'a', 'c', FalsoMUD(['Rua Larga\n'], combate=True), log=lambda *_: None)
        self.assertEqual(c2.exception.codigo, 4)

    def test_teto_de_passos(self):
        with self.assertRaises(N.Parada) as ctx:
            N.navegar(MAPA, 'a', 'c', FalsoMUD([]), max_passos=1, log=lambda *_: None)
        self.assertEqual(ctx.exception.codigo, 6)

    def test_mapa_real_tem_rota_do_templo_a_lyon(self):
        salas = N.carregar_mapa()
        p = N.caminho(salas, 'templo_midgaard', 'cap12_026')
        self.assertTrue(p)
        self.assertEqual(salas[p[-1][1]]['name'], 'O Centro da Cidade')


if __name__ == '__main__':
    unittest.main()
