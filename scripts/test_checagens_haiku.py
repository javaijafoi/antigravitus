#!/usr/bin/env python3
"""Testes das checagens nascidas da auditoria da sessão do Haiku (Plano 035, Dia 157).

1. brecha do #13: citar #13 numa frase não libera a delegação ao autor em outra (DELEGA_MESMA_FRASE);
2. o que o repositório já sabe sobre os nomes do §5 aparece na abertura (abertura.conhecimento_do_npc);
3. conexão ao jogo sem state.json atualizado reprova (state.desatualizado);
4. conexão deixada aberta reprova e avisa na abertura (sessao.aberta).
"""
import json
import os
import shutil
import sys
import tempfile
import time
import unittest
from pathlib import Path
from unittest import mock

sys.path.insert(0, str(Path(__file__).resolve().parent))

import devolutiva  # noqa: E402
import mandabala  # noqa: E402


class TestBrechaDo13(unittest.TestCase):
    def test_citacao_em_outra_frase_nao_libera(self):
        passo = ("Só então `give livro lemin`, sem outra fala (AGENTS #13 e #14).\n"
                 "- Opção padrão: parar e perguntar ao autor a palavra de abertura.")
        self.assertIn("perguntar ao autor", mandabala.delegacao_sem_motivo(passo))

    def test_citacao_na_mesma_frase_libera(self):
        passo = "Confirmar com o autor a compra de 9.750 moedas (AGENTS #13) antes de comprar."
        self.assertIsNone(mandabala.delegacao_sem_motivo(passo))

    def test_sem_delegacao(self):
        self.assertIsNone(mandabala.delegacao_sem_motivo("Ir a Lyon e falar com Lemin, à mão."))

    def test_plano_real_035_e_acusado(self):
        arq = Path(mandabala.ROOT_DIR) / "data" / "heroes" / "grebolius" / "planos" / "plano035.md"
        if not arq.is_file():
            self.skipTest("plano035 ausente")
        ids = [i for i, _ in mandabala.checar_plano_v2(arq.read_text(encoding="utf-8"))]
        self.assertIn("plano.proximo_passo_executavel", ids)


class TestConhecimentoNaAbertura(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, self.tmp, True)
        pasta = self.tmp / "data" / "heroes" / "h"
        pasta.mkdir(parents=True)
        (pasta / "conhecimento.md").write_text(
            "# K\n\n## 61. Ajuda Mágica: Lemin em Lyon\n"
            "- **Cadeia observada:** olhar Lemin aciona convite; responder Merlin após o fim da fala.\n",
            encoding="utf-8")
        p = mock.patch.object(mandabala, "HEROES_DIR", self.tmp / "data" / "heroes")
        p.start()
        self.addCleanup(p.stop)

    def test_termos_ignoram_verbo_e_palavras_comuns(self):
        self.assertEqual(mandabala.termos_do_passo("**Reabrir Ajuda Mágica com Lemin.** Ir a Lyon."),
                         ["Lemin", "Lyon"])

    def test_sobre_traz_secao_e_linha(self):
        secoes, linhas, total = mandabala.sobre("lemin", "h")
        self.assertEqual(total, 2)
        self.assertIn("61. Ajuda Mágica: Lemin em Lyon", secoes)
        self.assertTrue(any("responder Merlin" in l for l in linhas))

    def test_abertura_mostra_o_que_ja_se_sabe(self):
        plano = "## 5. O próximo passo\nReabrir a missão com Lemin, à mão.\n"
        saida = mandabala.sequencia_abertura(plano, "h")
        self.assertIn("O QUE O REPOSITÓRIO JÁ SABE", saida)
        self.assertIn("responder Merlin", saida)

    def test_main_sobre(self):
        with mock.patch.object(mandabala, "resolver_heroi", return_value=("h", None)), \
             mock.patch("sys.stdout"):
            self.assertEqual(mandabala.main(["--sobre", "Merlin"]), 0)


class TestSessaoAoVivo(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, self.tmp, True)
        self.runtime = self.tmp / "runtime"
        self.runtime.mkdir()
        p = mock.patch.object(mandabala, "RUNTIME_DIR", self.runtime)
        p.start()
        self.addCleanup(p.stop)

    def transcript(self, nome, tipos):
        arq = self.runtime / nome
        arq.write_text("\n".join(json.dumps({"kind": k}) for k in tipos) + "\n", encoding="utf-8")
        return arq

    def rodar(self, state_mudou):
        with mock.patch.object(devolutiva, "falha") as m_falha, mock.patch.object(devolutiva, "ok"), \
             mock.patch.object(devolutiva, "aviso"), \
             mock.patch.object(devolutiva, "momento_do_commit", return_value=0.0), \
             mock.patch.object(devolutiva, "mudou", return_value=state_mudou):
            devolutiva.checar_sessao_ao_vivo("h", "abc")
        return str(m_falha.call_args_list)

    def test_aberta_e_fechada(self):
        self.assertTrue(mandabala.sessao_aberta(self.transcript("transcript_a.jsonl", ["open", "command"])))
        self.assertFalse(mandabala.sessao_aberta(
            self.transcript("transcript_b.jsonl", ["open", "command", "close", "shutdown"])))
        self.assertFalse(mandabala.sessao_aberta(self.transcript("transcript_c.jsonl", ["open", "idle"])))

    def test_jogou_sem_state_reprova(self):
        self.transcript("transcript_1.jsonl", ["open", "command", "close", "shutdown"])
        falhas = self.rodar(state_mudou=False)
        self.assertIn("state.desatualizado", falhas)
        self.assertNotIn("sessao.aberta", falhas)

    def test_jogou_com_state_passa(self):
        self.transcript("transcript_1.jsonl", ["open", "command", "close", "shutdown"])
        self.assertEqual(self.rodar(state_mudou=True), "[]")

    def test_ultima_conexao_aberta_reprova(self):
        self.transcript("transcript_1.jsonl", ["open", "command", "close", "shutdown"])
        tarde = self.transcript("transcript_2.jsonl", ["open", "command", "idle"])
        agora = time.time() + 5
        os.utime(tarde, (agora, agora))
        self.assertIn("sessao.aberta", self.rodar(state_mudou=True))

    def test_sem_jogo_nao_cobra_state(self):
        self.assertEqual(self.rodar(state_mudou=False), "[]")


if __name__ == "__main__":
    unittest.main(verbosity=2)
