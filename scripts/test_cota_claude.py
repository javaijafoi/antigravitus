# -*- coding: utf-8 -*-
"""Testes do vigia de cota do Claude Code (AGENTS.md §13)."""
import sys
import tempfile
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import cota_claude

AGORA = datetime(2026, 10, 20, 12, 0, tzinfo=timezone.utc)


def snap(u5, us, minutos=1):
    return {"registrado_em": (AGORA - timedelta(minutes=minutos)).isoformat(),
            "usado_5h_pct": u5, "usado_semanal_pct": us}


class TestCotaClaude(unittest.TestCase):
    def test_ok(self):
        cod, _ = cota_claude.avaliar(snap(40, 20), AGORA)
        self.assertEqual(cod, 0)

    def test_corte_5h_restando_10_ou_menos(self):
        cod, msgs = cota_claude.avaliar(snap(90, 20), AGORA)
        self.assertEqual(cod, 1)
        self.assertTrue(any("CRÍTICO" in m for m in msgs))

    def test_corte_semanal_restando_5_ou_menos(self):
        cod, _ = cota_claude.avaliar(snap(10, 95), AGORA)
        self.assertEqual(cod, 1)

    def test_semanal_6_por_cento_nao_corta(self):
        cod, _ = cota_claude.avaliar(snap(10, 94), AGORA)
        self.assertEqual(cod, 2)  # só atenção

    def test_atencao_5h(self):
        cod, _ = cota_claude.avaliar(snap(85, 20), AGORA)
        self.assertEqual(cod, 2)

    def test_snapshot_velho_falha(self):
        cod, msgs = cota_claude.avaliar(snap(10, 10, minutos=60), AGORA)
        self.assertEqual(cod, 1)
        self.assertIn("min", msgs[0])

    def test_sem_snapshot_falha(self):
        self.assertEqual(cota_claude.avaliar(None, AGORA)[0], 1)

    def test_registrar_e_ler(self):
        with tempfile.TemporaryDirectory() as d:
            alvo = Path(d) / "c.json"
            cota_claude.registrar(93, 7, caminho=alvo)
            lido = cota_claude.carregar(alvo)
            self.assertEqual(lido["usado_5h_pct"], 93.0)
            self.assertEqual(cota_claude.avaliar(lido)[0], 1)


if __name__ == "__main__":
    unittest.main()
