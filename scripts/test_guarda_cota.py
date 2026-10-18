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
        mock_handoff.assert_called_once_with(0.04, tipo="semanal", reset_fmt="120h 00m", modelo="gemini-3.8-flash")

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
        mock_handoff.assert_called_once_with(0.09, tipo="diario", reset_fmt="4h 00m", modelo="gemini-3.8-flash")

    @patch("guarda_cota.urllib.request.urlopen")
    def test_ignora_outro_modelo_esgotado(self, mock_urlopen):
        import json
        # Simula resposta do server onde Argon está em 0.6% (crítico), mas Flash está em 18% (seguro)
        mock_resp = MagicMock()
        mock_resp.read.return_value = json.dumps({
            "userStatus": {
                "cascadeModelConfigData": {
                    "clientModelConfigs": [
                        {
                            "modelId": "gemini-4-argon-high",
                            "label": "Gemini 4 Argon (High)",
                            "quotaInfo": {
                                "remainingFraction": 0.006,  # 0.6% - CRÍTICO!
                                "resetTime": "2026-10-24T00:00:00Z"
                            }
                        },
                        {
                            "modelId": "gemini-3.8-flash-high",
                            "label": "Gemini 3.8 Flash (High)",
                            "quotaInfo": {
                                "remainingFraction": 0.18,  # 18% - SEGURO!
                                "resetTime": "2026-10-24T00:00:00Z"
                            }
                        }
                    ]
                }
            }
        }).encode("utf-8")
        mock_resp.__enter__.return_value = mock_resp
        mock_urlopen.return_value = mock_resp

        # Quando checar o modelo ativo (3.8 Flash), NÃO deve cortar mesmo que o Argon esteja esgotado!
        detalhes = guarda_cota.consultar_detalhes_cota("gemini-3.8-flash")
        self.assertIsNotNone(detalhes)
        self.assertEqual(detalhes["modelo"], "Gemini 3.8 Flash (High)")
        self.assertEqual(detalhes["frac"], 0.18)
        self.assertTrue(guarda_cota.checar_guarda(modelo_alvo="gemini-3.8-flash", forcar=True))


if __name__ == "__main__":
    unittest.main()

