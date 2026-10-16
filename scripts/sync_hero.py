#!/usr/bin/env python3
"""Gera ficha e catálogo a partir do último estado documentado, sem jogar ou publicar."""
import argparse
import json
from pathlib import Path
import re
import sys

for _stream in (sys.stdout, sys.stderr):
    if hasattr(_stream, "reconfigure"):
        _stream.reconfigure(encoding="utf-8", errors="replace")

ROOT_DIR = Path(__file__).resolve().parents[1]
STATUS = {'discovered':'Descoberta', 'active':'Ativa', 'completed':'Concluída', 'blocked':'Bloqueada', 'deferred':'Adiada', 'abandoned':'Abandonada'}

def read_json(path):
    return json.loads(path.read_text(encoding='utf-8'))

def json_text(value):
    return json.dumps(value, ensure_ascii=False, indent=2) + '\n'

def number(value):
    return f'{value:,}'.replace(',', '.')

def validate_state(state, hero_id, posts, extra_max=0):
    if state.get('hero_id') != hero_id or state.get('schema_version') != 1:
        raise ValueError('state.json deve identificar o herói e a versão 1 do esquema.')
    day = state.get('as_of', {}).get('day')
    post_ids = [p['id'] for p in posts if isinstance(p, dict) and type(p.get('id')) is int]
    limite = max(post_ids) if post_ids else 0
    # A Season 02 corre por capítulos: os dias do capítulo também são jornada documentada.
    limite = max(limite, extra_max)
    if type(day) is not int or day < 1 or limite <= 0 or day > limite:
        raise ValueError('O estado precisa referir-se a uma jornada documentada, não futura.')
    for key in ('hp','mana','mv'):
        resource = state['vitals'][key]
        if any(type(resource.get(k)) is not int for k in ('current','max')) or not 0 <= resource['current'] <= resource['max'] or resource['max'] <= 0:
            raise ValueError(f'Recurso inválido: {key}.')
    for key in ('level', 'gold', 'wimpy', 'training_sessions'):
        if type(state.get(key)) is not int or state[key] < (1 if key == 'level' else 0):
            raise ValueError(f'Campo numérico inválido: {key}.')
    if state['wimpy'] > state['vitals']['hp']['max']:
        raise ValueError('Wimpy não pode exceder HP máximo.')
    if not state['as_of'].get('source') or state['as_of'].get('verification') not in ('documental','live') or type(state['as_of'].get('live_verified')) is not bool:
        raise ValueError('Informe a origem e a natureza documental ou de sessão do estado.')
    if state['as_of']['live_verified'] != (state['as_of']['verification'] == 'live'):
        raise ValueError('Origem documental não pode alegar verificação ao vivo; origem live exige confirmação de sessão.')
    for skill in state['skills']:
        if type(skill.get('proficiency')) is not int or not 0 <= skill['proficiency'] <= 100:
            raise ValueError('Proficiência fora da faixa 0–100.')

def quick_stats(state):
    def pair(key):
        item = state['vitals'][key]
        return f"{item['current']} / {item['max']}"
    class_label = state['mechanical_class'].split(' (')[0]
    style = f"; estilo {state['narrative_style']}" if state.get('narrative_style') else ''
    weapon = state.get('weapon_summary') or next((item['name'] for item in state['equipment'] if item['slot'] == 'Empunhado (Arma Principal)'), 'Não registrado')
    return {
        'level_badge': f"(Grau {state['level']} • {class_label}{style})",
        'hp': pair('hp'), 'mana': pair('mana'), 'mv': pair('mv'),
        'ac': f"AC {state['armor']['base']} ({state['armor']['with_armor']} com armor; registro)",
        'weapon': weapon, 'weapon_icon':'🗡️',
        'sanctuary':state['sanctuary']['name'],
        'location':state['location']['name'], 'camp':state['camp']['name'],
        'as_of_day':state['as_of']['day'], 'verification':state['as_of']['verification']
    }

def render_ficha(hero, state, missions):
    def bullet(label, value):
        return f'* **{label}:** {value}'
    def resource_row(name, key):
        v = state['vitals'][key]
        return f"| **{name}** | {v['current']} | {v['max']} | {v['current'] / v['max']:.0%} |"
    day = state['as_of']['day']
    verification = 'Registro documental; sem conferência ao vivo nesta revisão.' if not state['as_of']['live_verified'] else 'Estado verificado em sessão; consultar a origem registrada.'
    lines = [f"# 🧌 Ficha Atual de {hero['name']} (Último Estado Registrado)", '',
        f"> Referência: Dia {day}. {verification}",
        '> Este documento reúne o último estado e as missões registrados; as incertezas aparecem ao final.', '',
        '## ✦ Identificação e Registro',
        bullet('Nome de Registro no MUD', hero['name']), bullet('Título Honorífico',state['honorific']),
        bullet('Raça / Aparência Narrativa',state['appearance']),
        bullet('Raça Mecânica no MUD', state.get('mechanical_race', 'Não registrada')),
        bullet('Classe Mecânica no MUD',state['mechanical_class']),
        bullet('Grau / Nível Atual',f"**{state['level']}**"),
        bullet('Alinhamento Moral',f"{state['alignment']['value']} ({state['alignment']['label']})"),
        bullet('Localização Atual',state['location']['name'] + f' (último registro: Dia {day})'),
        bullet('Acampamento Registrado',state['camp']['name']), bullet('Santuário de Referência',state['sanctuary']['name']), '',
        'O acampamento indica onde houve repouso; não comprova proteção absoluta contra agressão.', '',
        '## ✦ Status Vitais', '| Recurso | Atual | Máximo | Porcentagem |', '| :--- | :---: | :---: | :---: |',
        resource_row('Pontos de Vida (HP)','hp'),resource_row('Pontos de Mana (MP)','mana'),resource_row('Estamina / Movimento (MV)','mv'), '',
        bullet('Experiência Acumulada',f"**{number(state['experience']['current'])} EXP**"),
        bullet(f"Experiência Necessária p/ Grau {state['level'] + 1}", f"**{number(state['experience']['next_level'] - state['experience']['current'])} EXP** (Meta: {number(state['experience']['next_level'])} EXP)"),
        bullet('Ouro Líquido',f"**{number(state['gold'])} moedas de ouro** (valor documental)"), '',
        '## ✦ Atributos Base']
    labels = {'STR':'Força','DEX':'Destreza','CON':'Constituição','INT':'Inteligência','WIS':'Sabedoria','CHA':'Carisma'}
    lines += [bullet(f'{labels[k]} ({k})',value) for k,value in state['attributes'].items()]
    lines += ['', '### Métricas de Combate',
        bullet('Classe de Armadura (AC)', f"{state['armor']['base']} (base) / **{state['armor']['with_armor']}** (com `armor`, conforme registro)"),
        state['armor']['note'], bullet('Bônus de Acerto (Hitroll)',state['hitroll']), bullet('Bônus de Dano (Damroll)',f"{state['damroll']:+d}"),
        bullet('Configuração de Fuga (Wimpy)',f"**{state['wimpy']} HP** (referência de 25%; não garante fuga antes de golpe letal)"), '',
        '## ✦ Missões e Autoquests Oficiais']
    for mission in missions['items']:
        if mission['type'] == 'official':
            lines.append(f"* **{mission['title']} — {STATUS[mission['status']]}:** {mission['objective']}")
            lines.append(f"  * Próximo passo: {mission['next_step']}")
    lines += ['', 'Objetivos pessoais e investigações ficam separados das autoquests no catálogo de missões.', '',
        '## ✦ Habilidades Conhecidas e Treinos Concluídos',
        bullet('Sessões de Treino Disponíveis', f"**{state['training_sessions']} sessões de treino acumuladas**"),
        'Percentuais são registros de proficiência; não garantem acerto, imunidade ou acesso a guildas.']
    for skill in state['skills']:
        lines.append(f"* `{skill['id']}` ({skill['name']}): **{skill['proficiency']}%**")
    lines += ['', '## ✦ Equipamento em Uso', 'Equipamento conforme os últimos documentos disponíveis; conferir no próximo acesso ao MUD.']
    lines += [bullet(item['slot'],f"`{item['name']}`") for item in state['equipment']]
    lines += ['', '## ✦ Inventário e Suprimentos', 'Itens registrados; disponibilidade e efeitos não foram testados nesta revisão.']
    lines += [f"* `{item['name']}` (x{item['quantity']}) — {item['source']}" for item in state['inventory']['recorded']]
    lines += ['', '### Pendências de inventário']
    lines += [f"* **{item['name']}** — último registro: Dia {item['last_seen_day']}. {item['reason']}" for item in state['inventory']['pending_verification']]
    lines += ['', '## ✦ Condições Registradas'] + ['* ' + item for item in state['conditions']]
    lines += ['', '## ✦ Próximo Objetivo (Plano, ainda não executado)',
        f"**{state['next_objective']['title']}**",state['next_objective']['next_step']]
    lines += ['* ' + item for item in state['next_objective']['missing_preparation']]
    lines += ['', '## ✦ Origem e Incertezas',f"Fonte do estado: {state['as_of']['source']}."]
    lines += ['* ' + item for item in state['uncertainties']]
    return '\n'.join(str(line) for line in lines) + '\n'

def expected_outputs(root, hero_id):
    root = Path(root)
    if not re.fullmatch(r'[a-z0-9][a-z0-9_-]*', hero_id):
        raise ValueError('Identificador de herói inválido.')
    directory = root / 'data/heroes' / hero_id
    hero = read_json(directory / 'hero.json')
    state = read_json(directory / 'state.json')
    missions = read_json(directory / 'missoes.json')
    posts = read_json(directory / 'posts.json')
    extra = 0
    chapters = directory / 'capitulos.json'
    if chapters.is_file():
        try:
            data = read_json(chapters)
            days = [p['day'] for c in data.get('chapters', []) for p in c.get('parts', [])
                    if isinstance(p, dict) and type(p.get('day')) is int]
            if days:
                extra = max(days)
        except Exception:
            pass
    validate_state(state, hero_id, posts, extra)
    if missions.get('hero_id') != hero_id or missions.get('as_of_day') != state['as_of']['day']:
        raise ValueError('O catálogo de missões deve identificar o mesmo herói e dia do estado.')
    hero['quick_stats'] = quick_stats(state)
    hero['folder'] = f'data/heroes/{hero_id}'
    catalog = read_json(root / 'data/heroes.json')
    if sum(item.get('id') == hero_id for item in catalog) != 1:
        raise ValueError('O herói deve ter uma única entrada no catálogo.')
    catalog = [hero if item.get('id') == hero_id else item for item in catalog]
    return {f'data/heroes/{hero_id}/hero.json':json_text(hero), 'data/heroes.json':json_text(catalog), f'data/heroes/{hero_id}/ficha.md':render_ficha(hero,state,missions)}

def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--hero', required=True)
    parser.add_argument('--root', type=Path, default=ROOT_DIR, help=argparse.SUPPRESS)
    parser.add_argument('--check', action='store_true', help='Conferir os derivados sem gravar.')
    args = parser.parse_args(argv)
    try:
        outputs = expected_outputs(args.root,args.hero)
        stale = [relative for relative,content in outputs.items() if not (args.root / relative).exists() or (args.root / relative).read_text(encoding='utf-8') != content]
        if args.check:
            for relative in stale:
                print('Derivado desatualizado:',relative)
            print('Derivados conferidos.' if not stale else 'Execute sync_hero.py após revisar as fontes.')
            return int(bool(stale))
        for relative in stale:
            (args.root / relative).write_text(outputs[relative],encoding='utf-8')
            print('Atualizado:',relative)
        print('Fontes documentais preservadas; nenhuma ação no MUD ou publicação executada.')
        return 0
    except (ValueError,KeyError,TypeError,OSError) as error:
        print(f'Erro ao sincronizar: {error}',file=sys.stderr)
        return 1

if __name__ == '__main__':
    for _stream in (sys.stdout, sys.stderr):
        if hasattr(_stream, "reconfigure"):
            _stream.reconfigure(encoding="utf-8", errors="replace")
    raise SystemExit(main())
