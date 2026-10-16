#!/usr/bin/env python3
"""Testes do scripts/mandabala.py — descoberta do plano vigente e ordem de leitura."""
import shutil
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

sys.path.insert(0, str(Path(__file__).resolve().parent))

import mandabala  # noqa: E402


PLANO_MODELO = """\
# Plano 001 — teste

| | |
|---|---|
| **Criado em** | 2026-10-16 · Dia 156 |
| **Por** | `modelo-de-teste` |
| **Herói** | `heroi_teste` |
| **Objetivo** | Fazer o teste passar |
| **Sessão encerrada?** | Sim |

Corpo do plano.
"""


class BasePlanos(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, self.tmp, True)
        self.heroes = self.tmp / "data" / "heroes"
        self.heroes.mkdir(parents=True)
        self._p_heroes = mock.patch.object(mandabala, "HEROES_DIR", self.heroes)
        self._p_root = mock.patch.object(mandabala, "ROOT_DIR", self.tmp)
        self._p_heroes.start()
        self._p_root.start()
        self.addCleanup(self._p_heroes.stop)
        self.addCleanup(self._p_root.stop)

    def criar(self, heroi, numero, texto=PLANO_MODELO):
        pasta = self.heroes / heroi / "planos"
        pasta.mkdir(parents=True, exist_ok=True)
        arq = pasta / f"plano{numero:03d}.md"
        arq.write_text(texto, encoding="utf-8")
        return arq


class TestDescoberta(BasePlanos):
    def test_herois_com_planos_so_lista_quem_tem_pasta(self):
        self.criar("com_plano", 1)
        (self.heroes / "sem_plano").mkdir()
        self.assertEqual(mandabala.heroes_com_planos(), ["com_plano"])

    def test_planos_de_ordena_por_numero(self):
        self.criar("h", 2)
        self.criar("h", 10)
        self.criar("h", 1)
        self.assertEqual([n for n, _ in mandabala.planos_de("h")], [1, 2, 10])

    def test_ignora_arquivo_fora_do_padrao(self):
        self.criar("h", 1)
        (self.heroes / "h" / "planos" / "LEIA.md").write_text("x", encoding="utf-8")
        (self.heroes / "h" / "planos" / "plano1.md").write_text("x", encoding="utf-8")
        self.assertEqual([n for n, _ in mandabala.planos_de("h")], [1])

    def test_heroi_sem_pasta_devolve_vazio(self):
        self.assertEqual(mandabala.planos_de("nao_existe"), [])


class TestResolucaoDeHeroi(BasePlanos):
    def test_sem_planos_nenhum_devolve_erro(self):
        heroi, erro = mandabala.resolver_heroi(None)
        self.assertIsNone(heroi)
        self.assertIn("planos", erro)

    def test_um_heroi_e_escolhido_sozinho(self):
        self.criar("unico", 1)
        self.assertEqual(mandabala.resolver_heroi(None), ("unico", None))

    def test_varios_herois_escolhe_o_do_plano_mais_alto(self):
        self.criar("a", 1)
        self.criar("b", 7)
        self.assertEqual(mandabala.resolver_heroi(None)[0], "b")

    def test_heroi_pedido_sem_planos_da_erro_claro(self):
        self.criar("tem", 1)
        heroi, erro = mandabala.resolver_heroi("nao_tem")
        self.assertIsNone(heroi)
        self.assertIn("tem", erro)


class TestCabecalho(unittest.TestCase):
    def test_extrai_os_campos_da_tabela(self):
        campos = mandabala.cabecalho_do_plano(PLANO_MODELO)
        self.assertEqual(campos["Por"], "modelo-de-teste")
        self.assertEqual(campos["Objetivo"], "Fazer o teste passar")
        self.assertIn("2026-10-16", campos["Criado em"])

    def test_sem_tabela_devolve_vazio(self):
        self.assertEqual(mandabala.cabecalho_do_plano("# nada aqui"), {})


class TestLacunas(unittest.TestCase):
    def test_sem_lacuna(self):
        self.assertEqual(mandabala.lacunas([1, 2, 3]), [])

    def test_com_lacuna(self):
        self.assertEqual(mandabala.lacunas([1, 3, 5]), [2, 4])

    def test_vazio(self):
        self.assertEqual(mandabala.lacunas([]), [])


class TestMain(BasePlanos):
    def test_padrao_imprime_ordem_e_plano_integral(self):
        self.criar("h", 1)
        with mock.patch("sys.stdout") as out:
            self.assertEqual(mandabala.main(["--hero", "h"]), 0)
            texto = "".join(c.args[0] for c in out.write.call_args_list)
        self.assertIn("PLANO 001", texto)
        self.assertIn("AGENTS.md", texto)
        self.assertIn("Corpo do plano.", texto)
        self.assertIn("CRIE o plano 002", texto)

    def test_escolhe_o_mais_alto_por_padrao(self):
        self.criar("h", 1)
        self.criar("h", 2, PLANO_MODELO.replace("Fazer o teste passar", "Objetivo do dois"))
        with mock.patch("sys.stdout") as out:
            mandabala.main(["--hero", "h"])
            texto = "".join(c.args[0] for c in out.write.call_args_list)
        self.assertIn("PLANO 002", texto)
        self.assertIn("Objetivo do dois", texto)

    def test_so_caminho_imprime_apenas_o_caminho(self):
        self.criar("h", 1)
        with mock.patch("sys.stdout") as out:
            self.assertEqual(mandabala.main(["--hero", "h", "--so-caminho"]), 0)
            texto = "".join(c.args[0] for c in out.write.call_args_list)
        self.assertEqual(texto.strip(), "data/heroes/h/planos/plano001.md")

    def test_numero_inexistente_falha(self):
        self.criar("h", 1)
        with mock.patch("sys.stderr"):
            self.assertEqual(mandabala.main(["--hero", "h", "--numero", "99"]), 1)

    def test_avisa_quando_o_plano_nao_e_o_mais_recente(self):
        self.criar("h", 1)
        self.criar("h", 2)
        with mock.patch("sys.stdout") as out:
            mandabala.main(["--hero", "h", "--numero", 1])
            texto = "".join(c.args[0] for c in out.write.call_args_list)
        self.assertIn("NÃO é o plano mais recente", texto)

    def test_avisa_lacuna_de_numeracao(self):
        self.criar("h", 1)
        self.criar("h", 3)
        with mock.patch("sys.stdout") as out:
            mandabala.main(["--hero", "h"])
            texto = "".join(c.args[0] for c in out.write.call_args_list)
        self.assertIn("lacuna", texto)
        self.assertIn("002", texto)

    def test_avisa_plano_sem_autoria(self):
        self.criar("h", 1, "# Plano 001\n\nsem tabela\n")
        with mock.patch("sys.stdout") as out:
            mandabala.main(["--hero", "h"])
            texto = "".join(c.args[0] for c in out.write.call_args_list)
        self.assertIn("não declara autoria", texto)

    def test_listar_mostra_heroi_e_resumo(self):
        self.criar("h", 1)
        with mock.patch("sys.stdout") as out:
            self.assertEqual(mandabala.main(["--listar"]), 0)
            texto = "".join(c.args[0] for c in out.write.call_args_list)
        self.assertIn("h", texto)
        self.assertIn("plano001", texto)
        self.assertIn("Fazer o teste passar", texto)

    def test_listar_sem_planos_falha(self):
        with mock.patch("sys.stderr"):
            self.assertEqual(mandabala.main(["--listar"]), 1)

    def test_heroi_sem_planos_falha(self):
        self.criar("outro", 1)
        with mock.patch("sys.stderr"):
            self.assertEqual(mandabala.main(["--hero", "nao_tem"]), 1)


class TestRepositorioReal(unittest.TestCase):
    """O repositório precisa ter o plano 001 do grebolius legível e com autoria."""

    def test_plano001_do_grebolius_existe_e_tem_autoria(self):
        plano = mandabala.ROOT_DIR / "data" / "heroes" / "grebolius" / "planos" / "plano001.md"
        if not plano.is_file():
            self.skipTest("plano001.md ainda não existe")
        campos = mandabala.cabecalho_do_plano(plano.read_text(encoding="utf-8"))
        self.assertTrue(campos.get("Por"), "o plano 001 precisa declarar autoria")
        self.assertTrue(campos.get("Objetivo"))

    def test_leia_existe_na_pasta_de_planos(self):
        leia = mandabala.ROOT_DIR / "data" / "heroes" / "grebolius" / "planos" / "LEIA.md"
        if not leia.is_file():
            self.skipTest("LEIA.md ainda não existe")
        texto = leia.read_text(encoding="utf-8")
        self.assertIn("append-only", texto)
        self.assertIn("Nunca edite um plano antigo", texto)


if __name__ == "__main__":
    unittest.main(verbosity=2)
