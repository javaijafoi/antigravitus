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


class TestDevolutivaTecnica(unittest.TestCase):
    """A devolutiva técnica é obrigatória desde o Dia 156 — o sintoma é a descoberta
    existir em prosa e não no artefato (os anéis do esgoto fora do mapa.json)."""

    def test_sem_secao(self):
        self.assertEqual(mandabala.devolutiva_tecnica("# Plano 001\n\n## 1. Onde\nnada\n"),
                         (False, False))

    def test_secao_com_conteudo_real(self):
        texto = ("# Plano\n\n## 8. Devolutiva técnica\n\n"
                 "| Descobri | Registrei em | O quê |\n|---|---|---|\n"
                 "| mapa | `mapa.json` | 4 arestas reversas dos aneis do esgoto |\n")
        self.assertEqual(mandabala.devolutiva_tecnica(texto), (True, True))

    def test_secao_so_com_placeholders(self):
        texto = ("# Plano\n\n## 8. Devolutiva técnica\n\n"
                 "| Descobri | Registrei em | O quê |\n|---|---|---|\n"
                 "| mapa | `mapa.json` | <salas/arestas corrigidas, ou \"nada\"> |\n")
        self.assertEqual(mandabala.devolutiva_tecnica(texto), (True, False))

    def test_aceita_acento_e_variacao_de_nivel(self):
        self.assertTrue(mandabala.devolutiva_tecnica("### Devolutiva tecnica\nmapa: nada\n")[0])
        self.assertTrue(mandabala.devolutiva_tecnica("## 8. DEVOLUTIVA TÉCNICA\n" + "x" * 20 + "\n")[0])

    def test_avisa_quando_falta_a_secao(self):
        self.criar_em_tmp = None  # marcador de leitura
        with tempfile.TemporaryDirectory() as tmp:
            heroi = Path(tmp) / "data" / "heroes" / "h" / "planos"
            heroi.mkdir(parents=True)
            (heroi / "plano001.md").write_text(
                "# Plano 001\n\n| **Por** | `m` |\n| **Objetivo** | testar |\n\n## 1. Onde\nnada\n",
                encoding="utf-8")
            with mock.patch.object(mandabala, "HEROES_DIR", Path(tmp) / "data" / "heroes"), \
                 mock.patch.object(mandabala, "ROOT_DIR", Path(tmp)), \
                 mock.patch("sys.stdout") as out:
                mandabala.main(["--hero", "h"])
                texto = "".join(c.args[0] for c in out.write.call_args_list)
        self.assertIn("NÃO tem a seção 'Devolutiva técnica'", texto)


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



class TestHistoricoDeCombate(unittest.TestCase):
    """historico.combate: o --sobre traz o que os transcripts já mediram contra o alvo (conhecimento §76)."""

    # textos reais de transcript_dia156_20261018_124258_79991b.jsonl (13:35)
    RAIO = ("Certo.\r\nO raio acerta o Rei Negro com impacto total! [79]\r\n"
            "{-<<<<>>>>>} o Rei Negro                                  Grebolius {<<<<<>>>>>}\r\n\r\n199hp 329mn 145mv > ")
    MORTE = "O Rei Negro acerta você com um golpe que quebra sua espinha!\r\nVocê está morto!\r\n"

    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, self.tmp, True)

    def transcript(self, nome, registros):
        import json
        arq = self.tmp / f"transcript_{nome}.jsonl"
        arq.write_text("\n".join(json.dumps(r, ensure_ascii=False) for r in registros), encoding="utf-8")
        return arq

    @staticmethod
    def cmd(c, texto="", hp=199, at="2026-10-18T13:35:00-03:00"):
        return {"kind": "command", "cmd": c, "text": texto, "vitals": {"hp": hp}, "at": at}

    def test_lances_vida_dano_barra_e_morte(self):
        self.transcript("a", [
            self.cmd("look", hp=199),
            self.cmd("consider rei", "Você  Oponente", hp=199),
            self.cmd("cast 'lightning bolt' rei", self.RAIO, hp=119, at="2026-10-18T13:35:27-03:00"),
            self.cmd("cast 'lightning bolt' peao", "[30]", hp=110),      # outro alvo: fora do histórico
            {"kind": "idle", "text": self.MORTE},
        ])
        sessoes = mandabala.historico_de_combate("Rei Negro", pasta=self.tmp)
        self.assertEqual(len(sessoes), 1)
        s = sessoes[0]
        self.assertEqual([l["cmd"] for l in s["lances"]], ["consider rei", "cast 'lightning bolt' rei"])
        raio = s["lances"][1]
        self.assertEqual((raio["vida_antes"], raio["vida_depois"], raio["dano"]), (199, 119, 79))
        self.assertEqual(raio["barra"], "{-<<<<>>>>>}")       # a barra do Rei, não a dela
        self.assertTrue(s["morte"])
        self.assertEqual(s["dano"], 79)

    def test_sem_lance_contra_o_alvo_nao_vira_sessao(self):
        self.transcript("b", [self.cmd("say rei"), self.cmd("cast 'armor'"), self.cmd("look", "o Rei Negro está aqui")])
        self.assertEqual(mandabala.historico_de_combate("Rei Negro", pasta=self.tmp), [])
        self.assertEqual(mandabala.linhas_do_historico([]), ["  nenhum lance contra esse alvo nos transcripts."])

    def test_alvo_numerado_e_acento(self):
        self.transcript("c", [self.cmd("cast 'sleep' 2.torre", hp=200), self.cmd("kill peao", hp=200)])
        self.assertEqual(len(mandabala.historico_de_combate("Torre", pasta=self.tmp)[0]["lances"]), 1)
        self.assertEqual(len(mandabala.historico_de_combate("Peão Negro", pasta=self.tmp)[0]["lances"]), 1)

    def test_linhas_trazem_resumo_e_barra(self):
        self.transcript("d", [self.cmd("look", hp=199), self.cmd("cast 'lightning bolt' rei", self.RAIO, hp=119)])
        texto = "\n".join(mandabala.linhas_do_historico(mandabala.historico_de_combate("rei", pasta=self.tmp)))
        self.assertIn("1 lance(s), dano 79, vida 199 -> 119", texto)
        self.assertIn("{-<<<<>>>>>}", texto)


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
