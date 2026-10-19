#!/usr/bin/env python3
"""Testes do scripts/encerrar.py — sem subprocesso, sem git, sem MUD."""
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import encerrar  # noqa: E402
import mandabala  # noqa: E402

STATE = {
    "as_of": {"day": 157, "verification": "live"},
    "level": 32,
    "alignment": {"value": 412, "label": "Bom"},
    "vitals": {"hp": {"current": 199, "max": 199}, "mana": {"current": 430, "max": 430},
               "mv": {"current": 145, "max": 145}},
    "experience": {"current": 7225102, "next_level": 8000000},
    "gold": 16059,
    "wimpy": 45,
    "armor": {"base": 89, "with_armor": 165},
    "location": {"name": "O Templo de Midgaard", "room_id": "templo_midgaard"},
    "conditions": ["Save e sono confirmados no Templo."],
    "next_objective": {"title": "Capítulo 12: reconstruir o livro de Merlin"},
}


class TestFecho(unittest.TestCase):
    def test_sem_close(self):
        self.assertFalse(encerrar.fecho_do_transcript([{"kind": "open"}])["fechou"])

    def test_close_confirmado(self):
        r = encerrar.fecho_do_transcript(
            [{"kind": "open"}, {"kind": "close", "save_confirmed": True, "sleep_confirmed": True}])
        self.assertEqual(r, {"fechou": True, "save": True, "sleep": True})

    def test_vale_o_ultimo_close(self):
        r = encerrar.fecho_do_transcript(
            [{"kind": "close", "save_confirmed": True, "sleep_confirmed": True},
             {"kind": "close", "save_confirmed": True, "sleep_confirmed": False}])
        self.assertFalse(r["sleep"])


class TestEsqueleto(unittest.TestCase):
    def setUp(self):
        self.texto = encerrar.esqueleto_plano(34, "Modelo X 1.0", "grebolius", STATE, "2026-10-20")

    def test_cabecalho_lido_pelo_mandabala(self):
        campos = mandabala.cabecalho_do_plano(self.texto)
        self.assertEqual(campos["Por"], "Modelo X 1.0")
        self.assertIn("Dia 157", campos["Criado em"])

    def test_estado_vem_do_state_em_numeros(self):
        estado = mandabala.secao(self.texto, 2)
        for trecho in ("199/199", "430/430", "16.059", "templo_midgaard", "412"):
            self.assertIn(trecho, estado)
        self.assertNotIn("plano.estado_numerico", [i for i, _ in mandabala.checar_plano_v2(self.texto)])

    def test_tem_devolutiva_e_todas_as_secoes(self):
        for n in range(1, 10):
            self.assertTrue(mandabala.secao(self.texto, n) or n == 9, f"falta §{n}")
        tem, _ = mandabala.devolutiva_tecnica(self.texto)
        self.assertTrue(tem)

    def test_state_vazio_nao_quebra(self):
        texto = encerrar.esqueleto_plano(1, "m", "h", {}, "2026-10-20")
        self.assertIn("# Plano 001", texto)


class TestResumoEBoletim(unittest.TestCase):
    def test_le_resumo_da_devolutiva(self):
        saida = "...\nRESULTADO: 2 falha(s), 3 aviso(s), 20 verificação(ões) ok\n"
        self.assertEqual(encerrar.resumo_saida(saida, encerrar.RX_DEVOLUTIVA), (2, 3))

    def test_le_resumo_do_auditor(self):
        self.assertEqual(encerrar.resumo_saida("Resumo: 5 falha(s), 2 aviso(s)", encerrar.RX_AUDITOR), (5, 2))

    def test_sem_resumo(self):
        self.assertEqual(encerrar.resumo_saida("nada", encerrar.RX_AUDITOR), (None, None))

    def test_linha_do_boletim(self):
        linha = encerrar.linha_boletim("2026-10-20", "m", "h", "plano034", {"fechou": True},
                                       (0, 1), (0, 0), "sim", [("plano.autossuficiente", "x")])
        self.assertEqual(linha["agente"], "m")
        self.assertEqual(linha["avanco_declarado"], "sim")
        self.assertEqual(linha["plano_v2"], ["plano.autossuficiente"])

    def test_agente_obrigatorio_e_real(self):
        self.assertEqual(encerrar.main(["--agente", "<modelo/versão>"]), 1)

    def test_fechar_exige_avanco(self):
        self.assertEqual(encerrar.main(["--agente", "Modelo X", "--fechar"]), 1)


if __name__ == "__main__":
    unittest.main(verbosity=2)
