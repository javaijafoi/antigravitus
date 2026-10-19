#!/usr/bin/env python3
"""Testes da catraca (AGENTS.md §14): nenhuma verificação em vigor some sem decisão registrada.

Se este teste falhou porque você removeu ou renomeou uma verificação: ou a recoloque, ou registre a
aprovação do autor em automato/DECISOES.md e edite docs/agentes/catraca.json no mesmo commit.
"""
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CATRACA = ROOT / "docs" / "agentes" / "catraca.json"


def carregar():
    return json.loads(CATRACA.read_text(encoding="utf-8"))


def ausentes(dados, raiz=ROOT):
    """[(id, arquivo)] cujo id não aparece literalmente no arquivo."""
    faltam = []
    for v in dados["verificacoes"]:
        arq = raiz / v["arquivo"]
        texto = arq.read_text(encoding="utf-8", errors="replace") if arq.is_file() else ""
        if v["id"] not in texto:
            faltam.append((v["id"], v["arquivo"]))
    return faltam


class TestCatraca(unittest.TestCase):
    def test_catraca_bem_formada(self):
        dados = carregar()
        ids = [v["id"] for v in dados["verificacoes"]]
        self.assertEqual(len(ids), len(set(ids)), "id repetido na catraca")
        for v in dados["verificacoes"]:
            for campo in ("id", "arquivo", "desde", "regra"):
                self.assertTrue(v.get(campo), f"{v.get('id')}: falta '{campo}'")

    def test_nenhuma_verificacao_sumiu(self):
        faltam = ausentes(carregar())
        self.assertEqual(faltam, [], "verificação removida sem decisão registrada (AGENTS §14): "
                         + ", ".join(f"{i} em {a}" for i, a in faltam))

    def test_detecta_remocao(self):
        """A catraca tem de morder: um id que não está no arquivo é acusado."""
        dados = {"verificacoes": [{"id": "id.que.nao.existe.em.lugar.nenhum",
                                   "arquivo": "scripts/mandabala.py"}]}
        self.assertEqual(len(ausentes(dados)), 1)


class TestTabelaFerramentas(unittest.TestCase):
    """automato.ferramenta_fora_da_tabela: script novo sem linha na tabela do README é avisado."""

    def setUp(self):
        import shutil
        import sys
        import tempfile
        sys.path.insert(0, str(ROOT / "scripts"))
        import check_project
        self.check = check_project
        self.tmp = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, self.tmp, True)
        (self.tmp / "automato" / "camadas").mkdir(parents=True)
        (self.tmp / "automato" / "camadas" / "navegar.py").write_text("", encoding="utf-8")
        (self.tmp / "automato" / "camadas" / "__init__.py").write_text("", encoding="utf-8")

    def readme(self, tabela):
        (self.tmp / "automato" / "README.md").write_text(
            "# x\n\n## Ferramentas — uma por função\n\n" + tabela + "\n\n## Outra\n`novo.py`\n",
            encoding="utf-8")

    def test_tudo_na_tabela(self):
        self.readme("| Andar | `camadas/navegar.py` | canônica |")
        self.assertEqual(self.check.validate_tool_registry(self.tmp), [])

    def test_script_novo_fora_da_tabela_avisa(self):
        self.readme("| Andar | `camadas/navegar.py` | canônica |")
        (self.tmp / "automato" / "rotas").mkdir()
        (self.tmp / "automato" / "rotas" / "novo.py").write_text("", encoding="utf-8")
        avisos = self.check.validate_tool_registry(self.tmp)
        self.assertEqual(len(avisos), 1)
        self.assertIn("rotas/novo.py", avisos[0])

    def test_repositorio_real_sem_script_fora(self):
        self.assertEqual(self.check.validate_tool_registry(ROOT), [])


if __name__ == "__main__":
    unittest.main(verbosity=2)
