# -*- coding: utf-8 -*-
"""test_guarda_cota.py - Testes unitários para a guarda de cota diária e semanal."""

import unittest
from unittest.mock import patch, MagicMock
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "automato" / "camadas"))

import guarda_cota


class TestGuardaCota(unittest.TestCase):

    def test_constantes_threshold(self):
        self.assertEqual(guarda_cota.THRESHOLD_DIARIO, 0.10)
        self.assertEqual(guarda_cota.THRESHOLD_SEMANAL, 0.05)
        self.assertEqual(guarda_cota.THRESHOLD_CRITICO, 0.10)

    def test_intervalo_recomendado_diario(self):
        self.assertEqual(guarda_cota.intervalo_recomendado(0.50, is_weekly=False), 2100.0)
        self.assertEqual(guarda_cota.intervalo_recomendado(0.25, is_weekly=False), 900.0)
        self.assertEqual(guarda_cota.intervalo_recomendado(0.15, is_weekly=False), 300.0)
        self.assertEqual(guarda_cota.intervalo_recomendado(0.08, is_weekly=False), 60.0)

    def test_intervalo_recomendado_semanal(self):
        self.assertEqual(guarda_cota.intervalo_recomendado(0.25, is_weekly=True), 2100.0)
        self.assertEqual(guarda_cota.intervalo_recomendado(0.15, is_weekly=True), 900.0)
        self.assertEqual(guarda_cota.intervalo_recomendado(0.08, is_weekly=True), 300.0)
        self.assertEqual(guarda_cota.intervalo_recomendado(0.04, is_weekly=True), 60.0)

    @patch("guarda_cota.consultar_detalhes_cota")
    def test_checar_guarda_semanal_seguro(self, mock_detalhes):
        mock_detalhes.return_value = {
            "frac": 0.18,
            "reset_str": "2026-10-24T00:00:00Z",
            "horas_restantes": 120.0,
            "is_weekly": True,
            "tipo": "semanal",
            "threshold": 0.05,
            "reset_formatado": "120h 00m",
        }
        # Cota de 18% em limite semanal (corte 5%) -> deve retornar True (seguro)
        self.assertTrue(guarda_cota.checar_guarda(forcar=True))

    @patch("guarda_cota.executar_handoff_completo")
    @patch("guarda_cota.consultar_detalhes_cota")
    def test_checar_guarda_semanal_critico(self, mock_detalhes, mock_handoff):
        mock_detalhes.return_value = {
            "frac": 0.04,
            "reset_str": "2026-10-24T00:00:00Z",
            "horas_restantes": 120.0,
            "is_weekly": True,
            "tipo": "semanal",
            "threshold": 0.05,
            "reset_formatado": "120h 00m",
        }
        # Cota de 4% em limite semanal (corte 5%) -> deve disparar handoff e retornar False
        self.assertFalse(guarda_cota.checar_guarda(forcar=True))
        mock_handoff.assert_called_once_with(0.04, tipo="semanal", reset_fmt="120h 00m")

    @patch("guarda_cota.executar_handoff_completo")
    @patch("guarda_cota.consultar_detalhes_cota")
    def test_checar_guarda_diario_critico(self, mock_detalhes, mock_handoff):
        mock_detalhes.return_value = {
            "frac": 0.09,
            "reset_str": "2026-10-18T16:00:00Z",
            "horas_restantes": 4.0,
            "is_weekly": False,
            "tipo": "diario",
            "threshold": 0.10,
            "reset_formatado": "4h 00m",
        }
        # Cota de 9% em limite diário (corte 10%) -> deve disparar handoff e retornar False
        self.assertFalse(guarda_cota.checar_guarda(forcar=True))
        mock_handoff.assert_called_once_with(0.09, tipo="diario", reset_fmt="4h 00m")


if __name__ == "__main__":
    unittest.main()
