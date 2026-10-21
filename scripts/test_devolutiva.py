#!/usr/bin/env python3
"""Testes do scripts/devolutiva.py — o verificador de fim de sessão."""
import shutil
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

sys.path.insert(0, str(Path(__file__).resolve().parent))

import devolutiva  # noqa: E402
import mandabala  # noqa: E402


PLANO_BOM = """\
# Plano 002 — teste

| | |
|---|---|
| **Criado em** | 2026-10-16 · Dia 156 |
| **Por** | `modelo-de-teste` |
| **Herói** | `h` |
| **Objetivo** | Testar |

## 8. Devolutiva técnica

| Descobri | Registrei em | O quê |
|---|---|---|
| mapa | `mapa.json` | corrigi 4 arestas |
| referência do servidor | `maquina/verificacoes.md` | o aviso de DT |

## 9. Como encerrar
nada
"""


class BaseTmp(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, self.tmp, True)
        (self.tmp / "data" / "heroes").mkdir(parents=True)
        # `devolutiva` só tem ROOT; os planos são descobertos pelo `mandabala`, que tem HEROES_DIR
        # e ROOT_DIR. Patchear o módulo errado foi erro meu — `does not have the attribute`.
        alvos = (
            (devolutiva, "ROOT", self.tmp),
            (mandabala, "ROOT_DIR", self.tmp),
            (mandabala, "HEROES_DIR", self.tmp / "data" / "heroes"),
        )
        for modulo, nome, valor in alvos:
            p = mock.patch.object(modulo, nome, valor)
            p.start()
            self.addCleanup(p.stop)

    def plano(self, numero, texto=PLANO_BOM):
        pasta = self.tmp / "data" / "heroes" / "h" / "planos"
        pasta.mkdir(parents=True, exist_ok=True)
        (pasta / f"plano{numero:03d}.md").write_text(texto, encoding="utf-8")


class TestPendente(unittest.TestCase):
    """Declarar o que NÃO se fez é o comportamento certo — vira aviso, não falha."""

    def test_reconhece_pendente(self):
        for t in ("PENDENTE", "pendente", "a fazer", "nada", "não fiz", "falta"):
            self.assertTrue(devolutiva.PENDENTE.search(t), t)

    def test_nao_marca_texto_normal(self):
        self.assertIsNone(devolutiva.PENDENTE.search("corrigi as quatro arestas do mapa"))


class TestCoerencia(BaseTmp):
    def _rodar(self, texto, mudou_retorno):
        with mock.patch.object(devolutiva, "mudou", return_value=mudou_retorno), \
             mock.patch.object(devolutiva, "ok") as m_ok, \
             mock.patch.object(devolutiva, "falha") as m_falha, \
             mock.patch.object(devolutiva, "aviso") as m_aviso:
            devolutiva.checar_coerencia_da_devolutiva("h", texto, "HEAD")
        return m_ok, m_falha, m_aviso

    def test_promete_mapa_e_mapa_mudou_passa(self):
        _, falha, _ = self._rodar(PLANO_BOM, True)
        self.assertEqual(falha.call_count, 0)

    def test_promete_mapa_e_mapa_nao_mudou_falha(self):
        _, falha, _ = self._rodar(PLANO_BOM, False)
        self.assertEqual(falha.call_count, 2)          # mapa e maquina/verificacoes.md

    def test_pendente_vira_aviso_nao_falha(self):
        texto = PLANO_BOM.replace("| corrigi 4 arestas |", "| **PENDENTE** |")
        _, falha, aviso = self._rodar(texto, False)
        self.assertEqual(falha.call_count, 1)          # só a de maquina/
        self.assertTrue(any("PENDENTE" in str(c) for c in aviso.call_args_list))

    def test_prosa_ao_redor_nao_conta_como_promessa(self):
        """A explicação cita os mesmos arquivos; só as LINHAS DE TABELA são promessa."""
        texto = PLANO_BOM.replace(
            "## 9. Como encerrar",
            "> nota: o `mapa.json` não foi tocado, e conhecimento.md também não.\n\n## 9. Como encerrar")
        _, falha, _ = self._rodar(texto, True)
        self.assertEqual(falha.call_count, 0)

    def test_sem_tabela_avisa(self):
        texto = "# Plano\n\n## 8. Devolutiva técnica\n\nsó texto solto\n"
        _, _, aviso = self._rodar(texto, True)
        self.assertTrue(any("não tem tabela" in str(c) for c in aviso.call_args_list))

    def test_cabecalho_da_tabela_nao_e_promessa(self):
        texto = ("# P\n\n## 8. Devolutiva técnica\n\n"
                 "| Descobri | Registrei em | O quê |\n|---|---|---|\n")
        _, falha, _ = self._rodar(texto, False)
        self.assertEqual(falha.call_count, 0)


class TestFalhaJustificada(unittest.TestCase):
    """plano.falha_justificada: FALHA do auditor se corrige com código, não com parágrafo (planos 037-039)."""

    # linha real do plano 039 §4
    REAL = ("- **Auditor:** as FALHAS de `auditar_sessao.py` deste dia (repetição de recusa por clientes "
            "simultâneos) estão explicadas nos planos 037 e 038 e no conhecimento §68 a §71.")
    CORRIGIDA = ("- **Auditor:** a FALHA de recuo-a-pe do auditar_sessao.py está justificada e corrigida em "
                 "`automato/acoes/xadrez_cascata.py` (piso de vida antes de cada lance).")

    def _rodar(self, numero, texto, mudou_retorno=False):
        with mock.patch.object(devolutiva, "mudou", return_value=mudou_retorno), \
             mock.patch.object(devolutiva, "ok") as m_ok, \
             mock.patch.object(devolutiva, "falha") as m_falha, \
             mock.patch.object(devolutiva, "aviso") as m_aviso:
            devolutiva.checar_falhas_justificadas(numero, texto, "HEAD")
        return m_ok, m_falha, m_aviso

    def test_acha_a_linha_real_sem_codigo(self):
        self.assertEqual(devolutiva.falhas_justificadas(self.REAL), [(self.REAL, [])])
        self.assertEqual(devolutiva.falhas_justificadas("o auditor passou limpo"), [])

    def test_sem_codigo_e_falha_a_partir_do_041(self):
        _, falha, aviso = self._rodar(41, self.REAL)
        self.assertEqual((falha.call_count, aviso.call_count), (1, 0))
        _, falha, aviso = self._rodar(40, self.REAL)          # planos antigos não se corrigem: só aviso
        self.assertEqual((falha.call_count, aviso.call_count), (0, 1))

    def test_codigo_citado_tem_de_ter_mudado(self):
        self.assertEqual(devolutiva.falhas_justificadas(self.CORRIGIDA)[0][1], ["automato/acoes/xadrez_cascata.py"])
        _, falha, _ = self._rodar(41, self.CORRIGIDA, mudou_retorno=False)
        self.assertEqual(falha.call_count, 1)
        _, falha, _ = self._rodar(41, self.CORRIGIDA, mudou_retorno=True)
        self.assertEqual(falha.call_count, 0)


class TestJanelaDaSessao(BaseTmp):
    def test_sem_plano_anterior_usa_head(self):
        self.plano(1)
        self.assertEqual(devolutiva.desde_da_sessao("h", None), "HEAD")

    def test_explicito_vence(self):
        self.plano(1)
        self.assertEqual(devolutiva.desde_da_sessao("h", "abc123"), "abc123")

    def test_usa_o_commit_que_adicionou_o_penultimo_plano(self):
        self.plano(1)
        self.plano(2)
        with mock.patch.object(devolutiva, "git", return_value=(0, "deadbeef")):
            self.assertEqual(devolutiva.desde_da_sessao("h", None), "deadbeef")


class TestChecarPlano(BaseTmp):
    def test_plano_sem_devolutiva_falha(self):
        self.plano(1, PLANO_BOM.split("## 8.")[0])
        with mock.patch.object(devolutiva, "falha") as m_falha, \
             mock.patch.object(devolutiva, "ok"), mock.patch.object(devolutiva, "aviso"):
            devolutiva.checar_plano("h")
        self.assertTrue(any("não tem a seção" in str(c) for c in m_falha.call_args_list))

    def test_plano_completo_passa(self):
        self.plano(1)
        with mock.patch.object(devolutiva, "falha") as m_falha, \
             mock.patch.object(devolutiva, "ok"), mock.patch.object(devolutiva, "aviso"):
            devolutiva.checar_plano("h")
        self.assertEqual(m_falha.call_count, 0)

    def test_numero_inesperado_falha(self):
        self.plano(1)
        with mock.patch.object(devolutiva, "falha") as m_falha, \
             mock.patch.object(devolutiva, "ok"), mock.patch.object(devolutiva, "aviso"):
            devolutiva.checar_plano("h", numero_esperado=2)
        self.assertTrue(any("esperado era 002" in str(c) for c in m_falha.call_args_list))


class TestCapitulos(BaseTmp):
    def _cap(self, payload):
        arq = self.tmp / "data" / "heroes" / "h" / "capitulos.json"
        arq.parent.mkdir(parents=True, exist_ok=True)
        arq.write_text(payload, encoding="utf-8")

    def test_parte_sem_source_kind_falha(self):
        self._cap('{"chapters":[{"id":1,"status":"concluido","parts":[{"day":1,"date":"x","evidence":[{}]}]}]}')
        with mock.patch.object(devolutiva, "falha") as m_falha, \
             mock.patch.object(devolutiva, "ok"), mock.patch.object(devolutiva, "aviso"):
            devolutiva.checar_capitulos("h")
        self.assertTrue(any("source_kind" in str(c) for c in m_falha.call_args_list))

    def test_parte_completa_passa(self):
        self._cap('{"chapters":[{"id":1,"status":"concluido","parts":'
                  '[{"day":1,"date":"x","source_kind":"live","evidence":[{"document":"d"}]}]}]}')
        with mock.patch.object(devolutiva, "falha") as m_falha, \
             mock.patch.object(devolutiva, "ok"), mock.patch.object(devolutiva, "aviso"):
            devolutiva.checar_capitulos("h")
        self.assertEqual(m_falha.call_count, 0)


class TestRepositorioReal(unittest.TestCase):
    def test_o_script_existe(self):
        alvo = Path(devolutiva.ROOT) / "scripts" / "devolutiva.py"
        self.assertTrue(alvo.is_file())

    def test_guarda_de_recursao_existe(self):
        """O script roda a suíte; sem guarda, chamá-lo DE DENTRO dela trava para sempre.

        Foi um travamento real: `test_devolutiva` chamava `main()`, que roda `unittest discover`,
        que carrega `test_devolutiva`... Sem esta guarda, o teste pendura a suíte inteira.
        """
        fonte = (Path(devolutiva.ROOT) / "scripts" / "devolutiva.py").read_text(encoding="utf-8")
        self.assertIn("DSH_DEVOLUTIVA_RODANDO", fonte)

    def test_main_nao_executa_a_suite_de_verdade(self):
        """`rodar` fica mockado: `main()` não pode disparar subprocesso nenhum dentro do teste.

        O que se prova aqui é que o mock foi usado — ou seja, nenhuma suíte rodou de verdade.
        """
        with mock.patch.object(devolutiva, "rodar") as m_rodar, \
             mock.patch.object(devolutiva, "codigo_mudou", return_value=True), \
             mock.patch.object(devolutiva, "checar_git"), \
             mock.patch.object(devolutiva, "checar_evidencias"), \
             mock.patch.object(devolutiva, "checar_livro_razao"), \
             mock.patch.object(devolutiva, "checar_sessao_ao_vivo"), \
             mock.patch.object(devolutiva, "checar_plano", return_value=(1, None)), \
             mock.patch("sys.stdout"):
            codigo = devolutiva.main(["--hero", "grebolius"])
        self.assertEqual(m_rodar.call_count, 3)        # check_project, verificar, suíte — todos mockados
        self.assertIn(codigo, (0, 1, 2))

    def test_sessao_sem_py_pula_a_suite(self):
        """Sessão que só mexeu em data/ não paga 7 s de suíte."""
        with mock.patch.object(devolutiva, "rodar") as m_rodar, \
             mock.patch.object(devolutiva, "codigo_mudou", return_value=False), \
             mock.patch.object(devolutiva, "checar_git"), \
             mock.patch.object(devolutiva, "checar_evidencias"), \
             mock.patch.object(devolutiva, "checar_livro_razao"), \
             mock.patch.object(devolutiva, "checar_sessao_ao_vivo"), \
             mock.patch.object(devolutiva, "checar_plano", return_value=(1, None)), \
             mock.patch("sys.stdout"):
            devolutiva.main(["--hero", "grebolius"])
        self.assertEqual(m_rodar.call_count, 2)        # check_project e verificar
        rotulos = [c.args[1] for c in m_rodar.call_args_list]
        self.assertNotIn("suíte offline", rotulos)

    def test_leia_exige_a_secao(self):
        leia = Path(devolutiva.ROOT) / "data" / "heroes" / "grebolius" / "planos" / "LEIA.md"
        if not leia.is_file():
            self.skipTest("LEIA.md ainda não existe")
        texto = leia.read_text(encoding="utf-8")
        self.assertIn("Devolutiva técnica", texto)
        self.assertIn("OBRIGATÓRIA", texto.upper())


class TestBypassVisivel(unittest.TestCase):
    """O bypass do autor não pode sumir no JSON (fecho.bypass_visivel)."""

    def test_sem_capitulos_fechados(self):
        self.assertIsNone(devolutiva.bypass_do_ultimo_fecho([]))
        self.assertIsNone(devolutiva.bypass_do_ultimo_fecho([{"id": 12, "status": "em_curso"}]))

    def test_fecho_normal_nao_avisa(self):
        caps = [{"id": 12, "status": "concluido",
                 "closing": {"decision": "cumprido", "confirmed_with_author": True, "at": "2026-10-21"}}]
        self.assertIsNone(devolutiva.bypass_do_ultimo_fecho(caps))

    def test_bypass_do_ultimo_aparece(self):
        caps = [{"id": 11, "status": "concluido", "closing": {"decision": "cumprido"}},
                {"id": 12, "status": "concluido",
                 "closing": {"decision": "bypass", "at": "2026-10-21", "reason": "autor mandou"}}]
        achado = devolutiva.bypass_do_ultimo_fecho(caps)
        self.assertIsNotNone(achado)
        self.assertEqual(achado[0], 12)
        self.assertEqual(achado[1]["reason"], "autor mandou")


if __name__ == "__main__":
    unittest.main(verbosity=2)
