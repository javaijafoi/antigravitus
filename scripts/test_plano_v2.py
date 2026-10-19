#!/usr/bin/env python3
"""Testes do modelo de plano v2: autossuficiente, §2 em números, §5 executável.

Os casos vêm de planos reais: o 033 remetia ao 032 em sete seções; o 032/033 terminavam em
"decidir com o autor"; o 026 (Gemini) era autossuficiente.
"""
import sys
import unittest
from pathlib import Path
from unittest import mock

sys.path.insert(0, str(Path(__file__).resolve().parent))

import devolutiva  # noqa: E402
import mandabala  # noqa: E402
from test_devolutiva import BaseTmp  # noqa: E402

CABECALHO = """\
# Plano {n:03d} — teste

| | |
|---|---|
| **Criado em** | 2026-10-19 · Dia 157 |
| **Por** | `modelo-de-teste` |
| **Objetivo** | Testar |

"""

BOM = """\
## 1. Onde o objetivo está
Missão ativa na etapa de entrega; falta o tomo.

## 2. Estado exato
Templo; 199/199 de vida, 430/430 de mana, 145/145 MV; ouro 16.059.

## 5. O próximo passo, e só ele
`score tudo`; depois ir à biblioteca de Paris por `navegar.py --para paris_biblioteca`.

## 8. Devolutiva técnica

| Descobri | Registrei em | O quê |
|---|---|---|
| mapa | nada | sem caminhada nova nesta sessão |
"""


class TestChecarPlanoV2(unittest.TestCase):
    def ids(self, texto):
        return [i for i, _ in mandabala.checar_plano_v2(texto)]

    def test_plano_bom_passa(self):
        self.assertEqual(self.ids(BOM), [])

    def test_igual_ao_plano_e_acusado(self):
        texto = BOM.replace("Missão ativa", "Igual ao Plano 032: missão ativa")
        self.assertIn("plano.autossuficiente", self.ids(texto))

    def test_le_lo_inteiro_e_acusado(self):
        texto = BOM.replace("falta o tomo.", "O Plano 028 guarda o percurso; lê-lo inteiro.")
        self.assertIn("plano.autossuficiente", self.ids(texto))

    def test_palavra_que_termina_em_os_nao_e_remissao(self):
        texto = BOM.replace("falta o tomo.", "os passos do Plano 031 foram refeitos aqui: n, n, e.")
        self.assertNotIn("plano.autossuficiente", self.ids(texto))

    def test_estado_sem_numeros(self):
        texto = BOM.replace("Templo; 199/199 de vida, 430/430 de mana, 145/145 MV; ouro 16.059.",
                            "Sem mudança relevante.")
        self.assertIn("plano.estado_numerico", self.ids(texto))

    def test_delegar_ao_autor_e_acusado(self):
        texto = BOM.replace("`score tudo`; depois", "Decidir, com o autor, a porta da Vovó; depois")
        self.assertIn("plano.proximo_passo_executavel", self.ids(texto))

    def test_delegar_com_invariante_citada_e_legitimo(self):
        texto = BOM.replace("`score tudo`; depois",
                            "Confirmar com o autor a compra de 9.750 (AGENTS #13); depois")
        self.assertNotIn("plano.proximo_passo_executavel", self.ids(texto))

    def test_sem_secao_5(self):
        texto = BOM.split("## 5.")[0]
        self.assertIn("plano.proximo_passo_executavel", self.ids(texto))

    def test_sequencia_traz_o_paragrafo_5(self):
        saida = mandabala.sequencia_abertura(BOM, "h")
        self.assertIn("SUA PRIMEIRA AÇÃO", saida)
        self.assertIn("navegar.py --para paris_biblioteca", saida)

    def test_plano_real_026_do_gemini_passa(self):
        arq = Path(mandabala.ROOT_DIR) / "data" / "heroes" / "grebolius" / "planos" / "plano026.md"
        if not arq.is_file():
            self.skipTest("plano026 ausente")
        self.assertEqual(self.ids(arq.read_text(encoding="utf-8")), [])


class TestLimiarNoDevolutiva(BaseTmp):
    """FALHA a partir do PLANO_V2_DESDE; aviso nos anteriores (append-only, não se corrigem)."""

    def _chamadas(self, numero):
        texto = CABECALHO.format(n=numero) + BOM.replace("Missão ativa", "Igual ao Plano 032: missão")
        self.plano(numero, texto)
        with mock.patch.object(devolutiva, "falha") as m_falha, \
             mock.patch.object(devolutiva, "aviso") as m_aviso, mock.patch.object(devolutiva, "ok"):
            devolutiva.checar_plano("h")
        return str(m_falha.call_args_list), str(m_aviso.call_args_list)

    def test_plano_novo_falha(self):
        falhas, _ = self._chamadas(mandabala.PLANO_V2_DESDE)
        self.assertIn("plano.autossuficiente", falhas)

    def test_plano_antigo_so_avisa(self):
        falhas, avisos = self._chamadas(mandabala.PLANO_V2_DESDE - 1)
        self.assertNotIn("plano.autossuficiente", falhas)
        self.assertIn("plano.autossuficiente", avisos)


if __name__ == "__main__":
    unittest.main(verbosity=2)
