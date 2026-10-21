# -*- coding: utf-8 -*-
"""Testes do aproveitar_tempo: empilhamento por orcamento e execucao sem MUD."""
import sys
import unittest
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ / 'automato' / 'acoes'))
import aproveitar_tempo as A


def nomes(tarefas):
    return [t.nome for t in tarefas]


class TestSelecao(unittest.TestCase):
    def test_dois_minutos_empilham_ate_o_limite(self):
        escolhidas, planejado, restante = A.selecionar(2, A.padrao())
        self.assertEqual(nomes(escolhidas),
                         ['comer_beber', 'cuidar', 'guardar_ouro', 'vender_espolio'])
        self.assertEqual(planejado, 120)
        self.assertEqual(restante, 0)

    def test_quatro_minutos_empilham_mais(self):
        escolhidas, planejado, restante = A.selecionar(4, A.padrao())
        self.assertIn('encher_cantil', nomes(escolhidas))
        self.assertIn('descansar', nomes(escolhidas))
        self.assertLessEqual(planejado, 240)
        self.assertGreaterEqual(restante, 0)

    def test_orcamento_minusculo_nao_escolhe_nada(self):
        escolhidas, planejado, restante = A.selecionar(0.1, A.padrao())
        self.assertEqual(escolhidas, [])
        self.assertEqual(planejado, 0)
        self.assertEqual(restante, 6)

    def test_varre_peoes_so_com_pedido_explicito(self):
        self.assertNotIn('varrer_peoes', nomes(A.padrao()))
        escolhidas, _p, _r = A.selecionar(5, A.por_nome(['varrer_peoes']))
        self.assertEqual(nomes(escolhidas), ['varrer_peoes'])

    def test_ordem_e_por_prioridade(self):
        escolhidas, _p, _r = A.selecionar(4, A.padrao())
        prioridades = [t.prioridade for t in escolhidas]
        self.assertEqual(prioridades, sorted(prioridades))


class TestExecucao(unittest.TestCase):
    def _tarefa(self, nome, custo, prioridade, executar, pode=None):
        return A.Tarefa(nome, custo, prioridade, pode, executar)

    def test_executa_na_ordem_e_para_no_orcamento(self):
        vistos = []

        def faz(n):
            def _f(ctx=None):
                vistos.append(n)
                return True
            return _f

        tarefas = [self._tarefa('a', 10, 10, faz('a')),
                   self._tarefa('b', 10, 20, faz('b')),
                   self._tarefa('c', 999, 30, faz('c'))]
        rel = A.aproveitar(1, tarefas, log=lambda *_: None)
        self.assertEqual(vistos, ['a', 'b'])
        self.assertEqual(rel['feitas'][0]['nome'], 'a')
        self.assertEqual(len(rel['feitas']), 2)

    def test_falha_de_uma_nao_aborta_a_outra(self):
        def explode(ctx=None):
            raise RuntimeError('boom')

        tarefas = [self._tarefa('ruim', 10, 10, explode),
                   self._tarefa('boa', 10, 20, lambda ctx=None: True)]
        rel = A.aproveitar(1, tarefas, log=lambda *_: None)
        self.assertEqual([f['nome'] for f in rel['feitas']], ['ruim', 'boa'])
        self.assertFalse(rel['feitas'][0]['ok'])

    def test_pre_condicao_falsa_pula_e_registra(self):
        tarefas = [self._tarefa('pulada', 10, 10, lambda ctx=None: True, pode=lambda ctx=None: False),
                   self._tarefa('feita', 10, 20, lambda ctx=None: True)]
        rel = A.aproveitar(1, tarefas, log=lambda *_: None)
        self.assertEqual([p['nome'] for p in rel['puladas']], ['pulada'])
        self.assertEqual([f['nome'] for f in rel['feitas']], ['feita'])

    def test_relatorio_tem_os_campos(self):
        rel = A.aproveitar(1, [], log=lambda *_: None)
        for campo in ('pedido_s', 'planejado_s', 'usado_s', 'feitas', 'puladas', 'restante_s'):
            self.assertIn(campo, rel)


if __name__ == '__main__':
    unittest.main()
