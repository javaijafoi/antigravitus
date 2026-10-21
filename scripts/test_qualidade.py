# -*- coding: utf-8 -*-
"""Testes do radar de uso (vigia.uso_do_transcript + quality_run).

Sem MUD: os transcripts são arquivos temporários com `at` e `origem` de verdade.
"""
import json
import sys
import tempfile
import unittest
from datetime import datetime, timedelta
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ / 'automato' / 'camadas'))
sys.path.insert(0, str(RAIZ / 'scripts'))

import quality_run  # noqa: E402
import vigia  # noqa: E402


def escrever(caminho, comandos):
    """comandos: [(cmd, origem, minutos_atras)]"""
    agora = datetime.now().astimezone()
    with open(caminho, 'w', encoding='utf-8') as fh:
        for cmd, origem, minutos in comandos:
            at = (agora - timedelta(minutes=minutos)).isoformat()
            fh.write(json.dumps({'kind': 'command', 'cmd': cmd, 'origem': origem,
                                 'at': at, 'text': ''}) + '\n')


class TestUsoDoTranscript(unittest.TestCase):
    def test_conta_passos_e_ataques_a_mao(self):
        with tempfile.TemporaryDirectory() as t:
            p = Path(t) / 'tr.jsonl'
            escrever(p, [('n', 'play', 1)] * 5 + [("cast 'lightning bolt' peao", 'play', 1)])
            u = vigia.uso_do_transcript(p, janela_min=30)
        self.assertEqual(u['comandos'], 6)
        self.assertEqual(u['passos_mao'], 5)
        self.assertEqual(u['ataques_mao'], 1)
        self.assertEqual(u['por_origem'], {'play': 6})

    def test_script_nao_conta_como_mao(self):
        with tempfile.TemporaryDirectory() as t:
            p = Path(t) / 'tr.jsonl'
            escrever(p, [('n', 'navegar', 1)] * 9 + [('kill peao', 'turno:milharal', 1)])
            u = vigia.uso_do_transcript(p, janela_min=30)
        self.assertEqual(u['passos_mao'], 0)
        self.assertEqual(u['ataques_mao'], 0)
        self.assertEqual(u['por_origem'], {'navegar': 9, 'turno:milharal': 1})

    def test_janela_corta_o_que_e_antigo(self):
        with tempfile.TemporaryDirectory() as t:
            p = Path(t) / 'tr.jsonl'
            escrever(p, [('n', 'play', 200)] * 10 + [('s', 'play', 2)] * 2)
            u = vigia.uso_do_transcript(p, janela_min=30)
        self.assertEqual(u['comandos'], 2)
        self.assertEqual(u['passos_mao'], 2)

    def test_dormindo_quando_o_ultimo_comando_foi_sleep(self):
        with tempfile.TemporaryDirectory() as t:
            p = Path(t) / 'tr.jsonl'
            escrever(p, [('sleep', 'play', 5)])
            u = vigia.uso_do_transcript(p, janela_min=30)
        self.assertTrue(u['dormindo'])

    def test_sem_transcript_e_sem_sessao(self):
        u = vigia.uso_do_transcript(Path('nao_existe.jsonl'))
        self.assertEqual(u['comandos'], 0)
        self.assertEqual(vigia.diagnostico_de_uso(u)['estado'], 'SEM_SESSAO')


class TestDiagnosticoDeUso(unittest.TestCase):
    def uso(self, passos=0, ataques=0, dormindo=False, comandos=None):
        return {'comandos': comandos if comandos is not None else max(passos + ataques, 1),
                'passos_mao': passos, 'ataques_mao': ataques, 'dormindo': dormindo,
                'janela_min': 30, 'por_origem': {'play': passos + ataques}, 'ultimo_ha_min': 1}

    def test_passos_demais_e_anomalia(self):
        d = vigia.diagnostico_de_uso(self.uso(passos=vigia.LIMITE_PASSOS_MAO))
        self.assertEqual(d['estado'], 'USO_ANOMALO')
        self.assertIn('navegar.py', d['motivos'][0])

    def test_um_passo_a_menos_nao_alerta(self):
        d = vigia.diagnostico_de_uso(self.uso(passos=vigia.LIMITE_PASSOS_MAO - 1))
        self.assertEqual(d['estado'], 'OK')

    def test_ataques_demais_e_anomalia(self):
        d = vigia.diagnostico_de_uso(self.uso(ataques=vigia.LIMITE_ATAQUES_MAO))
        self.assertEqual(d['estado'], 'USO_ANOMALO')
        self.assertIn('turno.py', d['motivos'][0])

    def test_dormindo_nao_alerta(self):
        d = vigia.diagnostico_de_uso(self.uso(passos=999, dormindo=True))
        self.assertEqual(d['estado'], 'OK')
        self.assertIn('silencio', d['motivos'][0])

    def test_rotina_rodando_nao_alerta(self):
        d = vigia.diagnostico_de_uso(self.uso(passos=999), supervisionado=True)
        self.assertEqual(d['estado'], 'OK')


class TestRadar(unittest.TestCase):
    def test_registro_leva_o_que_importa(self):
        d = vigia.diagnostico_de_uso(TestDiagnosticoDeUso().uso(passos=70))
        linha = quality_run.linha_do_registro(d)
        self.assertEqual(linha['estado'], 'USO_ANOMALO')
        self.assertEqual(linha['passos_mao'], 70)
        self.assertTrue(linha['at'])

    def test_verificar_devolve_codigo_por_estado(self):
        self.assertEqual({'OK': 0, 'SEM_SESSAO': 2, 'USO_ANOMALO': 1}['USO_ANOMALO'], 1)


if __name__ == '__main__':
    unittest.main()
