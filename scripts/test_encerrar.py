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


def cmd(c, texto="", hp=200, at="2026-10-20T15:00:00-03:00"):
    return {"kind": "command", "cmd": c, "text": texto, "vitals": {"hp": hp}, "at": at}


class TestMetricas(unittest.TestCase):
    """O placar só vale se o número vier do transcript, não da opinião."""

    def test_conta_o_basico(self):
        regs = [
            {"kind": "open"},
            cmd("consider peao", "", at="2026-10-20T15:00:00-03:00"),
            cmd("cast 'lightning bolt' peao", "Você está morto!", at="2026-10-20T15:10:00-03:00"),
            cmd("cast 'armor'", "", at="2026-10-20T15:20:00-03:00"),
            cmd("recall", "Você está morrendo de fome! (-3hp)", at="2026-10-20T15:30:00-03:00"),
            cmd("score tudo", "Vida: {<<<<<>>>>>} 180 de 200", at="2026-10-20T16:00:00-03:00"),
        ]
        m = encerrar.metricas_do_transcript(regs)
        self.assertEqual(m["comandos"], 5)
        self.assertEqual(m["minutos"], 60)
        self.assertEqual(m["consider"], 1)
        self.assertEqual(m["casts"], 2)
        self.assertEqual(m["armor"], 1)
        self.assertEqual(m["recalls"], 1)
        self.assertEqual(m["fome"], 1)
        self.assertEqual(m["mortes"], 1)
        self.assertEqual(m["consider_por_100_magias"], 50.0)

    def test_vida_inicial_em_porcento(self):
        m = encerrar.metricas_do_transcript([cmd("look", hp=150)])
        self.assertEqual(m["vida_inicio_pct"], 100)      # só hp conhecido: max = 150

    def test_transcript_vazio_nao_quebra(self):
        m = encerrar.metricas_do_transcript([])
        self.assertEqual(m["comandos"], 0)
        self.assertEqual(m["minutos"], 0)
        self.assertIsNone(m["consider_por_100_magias"])

    def test_linha_do_boletim_leva_tipo_e_metricas(self):
        linha = encerrar.linha_boletim("2026-10-20", "m", "h", "plano041", {"fechou": True},
                                       (0, 1), (0, 0), "sim", [], metricas={"comandos": 10},
                                       tipo="chefe")
        self.assertEqual(linha["tipo"], "chefe")
        self.assertEqual(linha["metricas"], {"comandos": 10})


class TestPlacar(unittest.TestCase):
    def test_le_o_boletim_e_agrupa_por_modelo(self):
        import json
        import tempfile
        with tempfile.TemporaryDirectory() as temp:
            caminho = Path(temp) / "boletim.jsonl"
            caminho.write_text("\n".join(json.dumps(l) for l in [
                {"agente": "A", "devolutiva": {"falhas": 1}, "auditor": {"falhas": 2},
                 "avanco_declarado": "sim", "metricas": {"comandos": 100, "minutos": 50,
                                                         "consider_por_100_magias": 4.0}},
                {"agente": "A", "devolutiva": {"falhas": 0}, "auditor": {"falhas": 0},
                 "avanco_declarado": "nao", "metricas": {"comandos": 200, "minutos": 70}},
                {"agente": "B", "devolutiva": {"falhas": 0}, "auditor": {"falhas": 0},
                 "avanco_declarado": "sim"},
            ]), encoding="utf-8")
            saida = encerrar.placar(caminho)
        self.assertIn("A", saida)
        self.assertIn("B", saida)
        self.assertIn("150", saida)      # média de comandos: (100+200)/2
        self.assertIn("50%", saida)      # A avançou 1 de 2

    def test_sem_boletim_nao_explode(self):
        self.assertIn("não existe", encerrar.placar(Path("nao_existe.jsonl")))


if __name__ == "__main__":
    unittest.main(verbosity=2)
