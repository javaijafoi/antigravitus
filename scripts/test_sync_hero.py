import json
from pathlib import Path
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / 'scripts'))

from scripts import sync_hero

FIXTURES_DIR = Path(__file__).resolve().parent / 'test_fixtures'

class SyncHeroTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        for relative in ['data/heroes.json'] + [f'data/heroes/grebolius/{name}' for name in ['state.json','hero.json','missoes.json','posts.json','ficha.md']]:
            target = self.root / relative
            target.parent.mkdir(parents=True,exist_ok=True)
            target.write_bytes((FIXTURES_DIR / relative).read_bytes())

    def tearDown(self):
        self.temp.cleanup()

    def update_state(self,change):
        path = self.root/'data/heroes/grebolius/state.json'
        state = json.loads(path.read_text(encoding='utf-8'))
        change(state)
        path.write_text(json.dumps(state,ensure_ascii=False),encoding='utf-8')

    def test_one_state_updates_both_catalogs_and_ficha(self):
        self.update_state(lambda s:s['vitals']['hp'].update(current=30))
        outputs = sync_hero.expected_outputs(self.root,'grebolius')
        local = json.loads(outputs['data/heroes/grebolius/hero.json'])
        central = next(h for h in json.loads(outputs['data/heroes.json']) if h['id']=='grebolius')
        self.assertEqual(local,central)
        self.assertEqual(local['quick_stats']['hp'],'30 / 52')
        self.assertIn('| **Pontos de Vida (HP)** | 30 | 52 |',outputs['data/heroes/grebolius/ficha.md'])

    def test_mapa_em_grade_e_derivado_do_mapa_json(self):
        outputs = sync_hero.expected_outputs(self.root,'grebolius')
        self.assertNotIn('data/heroes/grebolius/mapa_grade.json',outputs)   # sem mapa.json, sem derivado
        mapa = {'hero_name':'Grebolius','rooms':[{'id':'a','name':'A','zone':'Z','exits':{'e':'b'}},
                                                 {'id':'b','name':'B','zone':'Z','exits':{'w':'a'}}]}
        (self.root/'data/heroes/grebolius/mapa.json').write_text(json.dumps(mapa),encoding='utf-8')
        grade = json.loads(sync_hero.expected_outputs(self.root,'grebolius')['data/heroes/grebolius/mapa_grade.json'])
        self.assertEqual(grade['total'],2)
        self.assertEqual([s['id'] for s in grade['zonas'][0]['salas']],['a','b'])

    def test_invalid_resource_stops_before_any_write(self):
        self.update_state(lambda s:s['vitals']['hp'].update(current=999))
        path = self.root/'data/heroes/grebolius/ficha.md'
        before = path.read_bytes()
        self.assertEqual(sync_hero.main(['--hero','grebolius','--root',str(self.root)]),1)
        self.assertEqual(before,path.read_bytes())

    def test_future_state_is_rejected(self):
        posts = json.loads((self.root/'data/heroes/grebolius/posts.json').read_text(encoding='utf-8'))
        future_day = max(p['id'] for p in posts if isinstance(p.get('id'), int)) + 1
        self.update_state(lambda s:s['as_of'].update(day=future_day))
        with self.assertRaises(ValueError):
            sync_hero.expected_outputs(self.root,'grebolius')

    def test_documental_source_cannot_claim_live_verification(self):
        self.update_state(lambda s:s['as_of'].update(verification='documental', live_verified=True))
        with self.assertRaises(ValueError):
            sync_hero.expected_outputs(self.root,'grebolius')

    def test_check_detects_stale_without_rewriting_chronicles(self):
        post_path = self.root/'data/heroes/grebolius/posts.json'
        before = post_path.read_bytes()
        self.update_state(lambda s:s['vitals']['mv'].update(current=80))
        args = ['--hero','grebolius','--root',str(self.root)]
        self.assertEqual(sync_hero.main(args+['--check']),1)
        self.assertEqual(sync_hero.main(args),0)
        self.assertEqual(sync_hero.main(args+['--check']),0)
        self.assertEqual(post_path.read_bytes(),before)

    def test_pending_ring_is_not_added_as_confirmed_inventory(self):
        text = sync_hero.expected_outputs(self.root,'grebolius')['data/heroes/grebolius/ficha.md']
        recorded,pending = text.split('### Pendências de inventário')
        recorded = recorded.split('## ✦ Inventário e Suprimentos')[1]
        self.assertNotIn('anel arcano',recorded)
        self.assertIn('anel arcano',pending)
        self.assertIn('não confirmados',pending)

if __name__ == '__main__':
    unittest.main()
