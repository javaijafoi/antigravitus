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
        # o mesmo id pode valer em dois scripts (ex.: sessao.aberta na abertura e no fechamento)
        pares = [(v["id"], v["arquivo"]) for v in dados["verificacoes"]]
        self.assertEqual(len(pares), len(set(pares)), "par (id, arquivo) repetido na catraca")
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


class _BaseTmp(unittest.TestCase):
    """Raiz temporária com automato/camadas/navegar.py, e o check_project importado."""

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


class TestTabelaFerramentas(_BaseTmp):
    """automato.ferramenta_fora_da_tabela: script novo sem linha na tabela do README é avisado."""

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


class TestImportProibido(_BaseTmp):
    """automato.import_proibido: código que importa ou chama acoes/_proibidos/ é ERRO."""

    def escrever(self, rel, texto):
        arq = self.tmp / rel
        arq.parent.mkdir(parents=True, exist_ok=True)
        arq.write_text(texto, encoding="utf-8")

    def test_import_e_erro(self):
        self.escrever("automato/rotinas/x.py", "from acoes._proibidos import falar_minerador\n")
        erros = self.check.validate_forbidden_imports(self.tmp)
        self.assertEqual(len(erros), 1)
        self.assertIn("rotinas/x.py:1", erros[0])

    def test_subprocess_e_erro(self):
        self.escrever("scripts/y.py", "run(['python', 'automato/acoes/_proibidos/comprar_pocao.py'])\n")
        self.assertEqual(len(self.check.validate_forbidden_imports(self.tmp)), 1)

    def test_comentario_e_a_propria_pasta_nao_contam(self):
        self.escrever("automato/rotinas/x.py", "# nada de acoes/_proibidos aqui\n")
        self.escrever("automato/acoes/_proibidos/z.py", "import _proibidos\n")
        self.assertEqual(self.check.validate_forbidden_imports(self.tmp), [])

    def test_repositorio_real_limpo(self):
        self.assertEqual(self.check.validate_forbidden_imports(ROOT), [])

    def test_scripts_proibidos_tem_trava(self):
        for arq in (ROOT / "automato" / "acoes" / "_proibidos").glob("*.py"):
            self.assertIn("raise SystemExit('PROIBIDO", arq.read_text(encoding="utf-8"), arq.name)


if __name__ == "__main__":
    unittest.main(verbosity=2)
