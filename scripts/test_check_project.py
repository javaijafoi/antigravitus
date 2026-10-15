"""Regressões para inconsistências reais, preservação histórica e escrita/publicação explícitas."""
import contextlib
import copy
import io
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
import add_day
import create_hero
import publish_daily
from scripts import check_project as check


def post(day=1):
    return {"id": day, "day": f"Dia {day}", "title": "Uma observação", "date": "Data registrada",
            "in_game_time": "Tempo registrado", "excerpt": "O caminho foi observado.",
            "tags": ["Jornada"], "content": ["A porta estava fechada; decidi esperar."]}


def dump(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def sample_map():
    return {"hero_id": "teste", "total_rooms": 2, "layers": [{"id": "solo"}], "sanctuary_id": "a",
            "last_updated_day": 10, "rooms": [
                {"id": "a", "layer": "solo", "exits": {"n": "b"}},
                {"id": "b", "layer": "solo", "exits": {}}]}


class ValidatorTests(unittest.TestCase):
    def test_markdown_bold_hp_and_wimpy_are_parsed(self):
        result = check.parse_ficha("| **Pontos de Vida (HP)** | **52** | **52** | 100% |\n* **Configuração de Fuga (Wimpy):** **13 HP**\n* **Sessões de Treino Disponíveis:** **6 sessões de treino acumuladas**")
        self.assertEqual(result["hp"], (52, 52))
        self.assertEqual(result["wimpy"], 13)
        self.assertEqual(result["training_sessions"], 6)

    def test_absent_parse_is_explicit_not_zero(self):
        values = check.parse_ficha("Nível: 8\nOuro: 1.051")
        self.assertIsNone(values["hp"])
        self.assertIsNone(values["wimpy"])
        self.assertIsNone(values["training_sessions"])

    def test_empty_posts_require_explicit_draft(self):
        self.assertTrue(check.validate_posts("teste", [])[0])
        self.assertFalse(check.validate_posts("teste", [], allow_empty=True)[0])

    def test_malformed_posts_report_errors_without_crashing(self):
        for value in (None, {}, [None], [1], [{"id": []}], [{"id": True}], [post(), "texto"]):
            with self.subTest(value=value):
                self.assertTrue(check.validate_posts("teste", value)[0])

    def test_order_duplicate_and_placeholder_are_invalid(self):
        invalid = post()
        invalid["content"] = ["Conteúdo registrado via CLI."]
        self.assertTrue(check.validate_posts("teste", [post(2), post(1), invalid])[0])

    def test_legacy_metagame_is_warning_and_not_rewritten(self):
        value = post()
        value["content"] = ["Restaram 30 HP e quarenta pontos de couraça."]
        original = copy.deepcopy(value)
        errors, warnings = check.validate_posts("teste", [value])
        self.assertFalse(errors)
        self.assertTrue(any("metajogo" in warning for warning in warnings))
        self.assertEqual(value, original)

    def test_manual_new_day_cannot_bypass_evidence_policy(self):
        errors, _ = check.validate_posts("teste", [post(1), post(2)], legacy_through_day=1)
        self.assertTrue(any("posterior ao legado" in error for error in errors))
        self.assertFalse(check.validate_posts("teste", [post(1)], legacy_through_day=1)[0])

    def test_new_post_future_or_missing_evidence_fails(self):
        value = post()
        value.update(source_kind="live", evidence=[{"document": "observacoes.md", "day": 2}])
        with tempfile.TemporaryDirectory() as temp:
            errors, _ = check.validate_posts("teste", [value], hero_dir=temp)
        self.assertTrue(any("futuro" in error for error in errors))
        self.assertTrue(any("não encontrada" in error for error in errors))

    def test_evidence_cannot_escape_hero_directory(self):
        for path in ("../senhas.txt", "C:/dados.txt", "notas\\sessao.md"):
            self.assertTrue(check.validate_evidence([{"document": path}], "fonte", 1))

    def test_map_allows_one_way_connections(self):
        self.assertFalse(check.validate_map("teste", sample_map(), 10)[0])

    def test_map_rejects_broken_targets_duplicates_totals(self):
        value = sample_map()
        value["rooms"][1]["id"] = "a"
        value["total_rooms"] = 50
        errors, _ = check.validate_map("teste", value, 10)
        self.assertTrue(any("duplicado" in error for error in errors))
        self.assertTrue(any("inexistente" in error for error in errors))
        self.assertTrue(any("total_rooms" in error for error in errors))

    def test_map_accepts_legacy_day_interval_and_warns_staleness(self):
        value = sample_map()
        del value["last_updated_day"]
        value["last_updated_cycle"] = "Ciclo V (Dias 41–50)"
        self.assertFalse(check.validate_map("teste", value, 50)[0])
        self.assertTrue(check.validate_map("teste", value, 60)[1])

    def test_map_state_distinguishes_camp_and_sanctuary(self):
        state = {"camp": {"room_id": "b"}, "sanctuary": {"room_id": "a"}}
        value = sample_map()
        value["camp_id"] = "a"
        self.assertTrue(any("camp_id" in error for error in check.validate_map("teste", value, 10, state)[0]))

    def test_future_cycle_and_bad_limits_are_errors(self):
        future = {"cycle": 7, "start_day": 61, "end_day": 70, "title": "Plano", "summary": "Ainda vai ocorrer."}
        self.assertTrue(check.validate_cycles("teste", [future], 60)[0])
        future.update(cycle=1, start_day=2, end_day=10)
        self.assertTrue(check.validate_cycles("teste", [future], 60)[0])

    def test_nested_malformed_data_reports_errors(self):
        for value in (None, [], {"skills": [None]}, {"as_of": []}, {"vitals": {"hp": []}}):
            with self.subTest(value=value):
                self.assertTrue(check.validate_state("teste", value, 1)[0])
        for value in (None, {"items": [None]}, {"items": [{"id": "m", "accepted_day": []}]}):
            self.assertTrue(check.validate_missions("teste", value, 1)[0])

    def test_full_catalog_metadata_and_unparsed_vitals_fail(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            hero_dir = root / "data/heroes/teste"
            local = {"id": "teste", "subtitle": "Vigente", "quick_stats": {"hp": "52 / 52"}}
            dump(hero_dir / "hero.json", local)
            (hero_dir / "ficha.md").write_text("Não há tabela interpretável.", encoding="utf-8")
            errors, _ = check.validate_hero_sync(dict(local, subtitle="Antigo"), root, 1)
            self.assertTrue(any("subtitle" in error for error in errors))
            self.assertTrue(any("não foi possível interpretar hp" in error for error in errors))


class WritingTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.hero = self.root / "data/heroes/teste"
        self.hero.mkdir(parents=True)
        dump(self.hero / "posts.json", [post()])
        (self.hero / "observacao.md").write_text("Porta fechada observada.", encoding="utf-8")
        self.patches = [patch.object(add_day, "HEROES_DIR", self.root / "data/heroes"), patch.object(add_day, "BASE_DIR", self.root)]
        for item in self.patches:
            item.start()

    def tearDown(self):
        for item in self.patches:
            item.stop()
        self.temp.cleanup()

    def add(self, day=2, **kwargs):
        return add_day.add_chronicle(day, "Porta", "Data observada", "Tempo observado", "Porta fechada", ["Jornada"],
                                     ["A porta permaneceu fechada."], hero_id="teste", source_kind="documental",
                                     evidence=[{"document": "observacao.md", "day": day}], **kwargs)

    def test_existing_day_requires_explicit_replace_and_preserves_bytes(self):
        before = (self.hero / "posts.json").read_bytes()
        with self.assertRaises(ValueError):
            self.add(1)
        self.assertEqual((self.hero / "posts.json").read_bytes(), before)
        with contextlib.redirect_stdout(io.StringIO()):
            self.add(1, replace=True)
        self.assertEqual(len(json.loads((self.hero / "posts.json").read_text(encoding="utf-8"))), 1)

    def test_unknown_hero_never_falls_back_to_other_character(self):
        with self.assertRaises(ValueError):
            add_day.get_posts_path("desconhecido")

    def test_recorded_post_keeps_real_content_and_origin(self):
        with contextlib.redirect_stdout(io.StringIO()):
            result = self.add()
        self.assertEqual(result["content"], ["A porta permaneceu fechada."])
        self.assertEqual(result["source_kind"], "documental")
        self.assertIn("evidence", result)

    def test_future_cycle_does_not_overwrite_file(self):
        dump(self.hero / "ciclos.json", [])
        before = (self.hero / "ciclos.json").read_bytes()
        with self.assertRaises(ValueError):
            add_day.add_cycle_summary(1, "Ainda não ocorreu.", hero_id="teste")
        self.assertEqual((self.hero / "ciclos.json").read_bytes(), before)

    def test_cli_requires_real_content_and_evidence(self):
        result = subprocess.run([sys.executable, "-B", str(ROOT / "add_day.py"), "--hero", "teste", "--day", "2", "--title", "Porta"], capture_output=True, text=True)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("--content-file", result.stderr)

    def test_create_hero_is_draft_without_invented_day_or_numbers(self):
        templates = self.root / "data/heroes/_template"
        shutil.copytree(ROOT / "data/heroes/_template", templates)
        dump(self.root / "data/heroes.json", [])
        with patch.object(create_hero, "HEROES_DIR", self.root / "data/heroes"), patch.object(create_hero, "HEROES_JSON", self.root / "data/heroes.json"), contextlib.redirect_stdout(io.StringIO()):
            create_hero.create_hero("novo", 'Nome "com aspas"')
        directory = self.root / "data/heroes/novo"
        self.assertEqual(json.loads((directory / "posts.json").read_text()), [])
        self.assertEqual(json.loads((directory / "mapa.json").read_text(encoding="utf-8"))["total_rooms"], 0)
        meta = json.loads((directory / "hero.json").read_text(encoding="utf-8"))
        self.assertEqual(meta["record_status"], "draft")
        self.assertEqual(meta["quick_stats"]["hp"], "Não verificado")
        dump(self.root / "data/heroes.json", [meta])
        self.assertFalse(check.validate_project(self.root)[0])


class PublishTests(unittest.TestCase):
    def test_default_without_checkout_is_dry_run(self):
        with tempfile.TemporaryDirectory() as temp, patch.object(publish_daily, "validate_project", return_value=([], [])), patch.object(publish_daily, "git", side_effect=subprocess.CalledProcessError(128, "git")) as command, contextlib.redirect_stdout(io.StringIO()):
            self.assertTrue(publish_daily.sync_all(temp))
        self.assertEqual(command.call_count, 1)

    def test_push_requires_publish_and_validation_blocks_commit(self):
        with self.assertRaises(ValueError):
            publish_daily.sync_all(push=True)
        with patch.object(publish_daily, "validate_project", return_value=(["Erro real"], [])), patch.object(publish_daily, "git") as command, contextlib.redirect_stdout(io.StringIO()):
            self.assertFalse(publish_daily.sync_all(publish=True))
        command.assert_not_called()

    def test_publication_excludes_local_and_sensitive_paths(self):
        for value in (".env", "data/heroes/teste/session_1.txt", "scripts/local/coletor.py", "data/secrets.json", "audio/test_samples/a.mp3", "work/notas.md", "logs.txt"):
            self.assertFalse(publish_daily.public_path(value), value)
        self.assertTrue(publish_daily.public_path("data/heroes/teste/state.json"))

    @unittest.skipUnless(shutil.which("git"), "Git indisponível")
    def test_commit_is_single_local_revision_and_does_not_stage_unrelated_files(self):
        with tempfile.TemporaryDirectory() as temp, patch.object(publish_daily, "validate_project", return_value=([], [])), contextlib.redirect_stdout(io.StringIO()):
            root = Path(temp)
            subprocess.run(["git", "init", str(root)], check=True, capture_output=True)
            # Identidade restrita a este repositório de teste temporário.
            publish_daily.git(root, "config", "user.name", "Teste local")
            publish_daily.git(root, "config", "user.email", "teste@example.invalid")
            (root / "README.md").write_text("Inicial", encoding="utf-8")
            publish_daily.git(root, "add", "README.md")
            publish_daily.git(root, "commit", "-m", "Inicial")
            (root / "README.md").write_text("Revisado", encoding="utf-8")
            (root / ".env").write_text("NAO_PUBLICAR=teste", encoding="utf-8")
            before = publish_daily.git(root, "rev-parse", "HEAD")
            self.assertTrue(publish_daily.sync_all(root))
            self.assertEqual(publish_daily.git(root, "rev-parse", "HEAD"), before)
            self.assertTrue(publish_daily.sync_all(root, publish=True))
            self.assertEqual(publish_daily.git(root, "rev-list", "--count", "HEAD").strip(), "2")
            self.assertEqual(publish_daily.git(root, "show", "--format=", "--name-only", "HEAD").strip(), "README.md")
            self.assertIn(".env", publish_daily.git(root, "ls-files", "--others"))
            self.assertEqual(publish_daily.git(root, "remote"), "")


if __name__ == "__main__":
    unittest.main()
