# -*- coding: utf-8 -*-
"""vigia.py - o vigia da personagem.

Le a cauda do log do daemon (leitura pura: nao manda comando nenhum ao MUD,
portanto NAO interfere no motor que estiver rodando) e devolve um diagnostico:

    OK | FOME | SEDE | VIDA_BAIXA | MANA_BAIXA | MORTA | TRAVADO | SEM_SESSAO

Uso:
    python scripts/local/vigia.py            # texto legivel
    python scripts/local/vigia.py --json     # para uso por outros robos
"""
import json
import re
import sys
from pathlib import Path

import sys
from pathlib import Path as _P
sys.path.insert(0, str(_P(__file__).resolve().parents[1] / 'nucleo'))
import config
LOCAL = config.DIR_LOGS
LIMITE_VIDA = 0.45
LIMITE_MANA = 0.15
LINHAS = 120
JANELA_CURTA = 40


def log_mais_recente():
    logs = [p for p in LOCAL.glob('session_live_*.log') if p.is_file()]
    if not logs:
        return None
    return max(logs, key=lambda p: p.stat().st_mtime)


def cauda(linhas=LINHAS):
    p = log_mais_recente()
    if p is None:
        return []
    with open(p, encoding='utf-8', errors='replace') as fh:
        return [l.rstrip('\n').rstrip('\r') for l in fh.readlines()[-linhas:]]


def vitais(texto):
    m = re.findall(r'(\d+)hp (\d+)mn (\d+)mv', texto)
    return tuple(int(x) for x in m[-1]) if m else None


def diagnosticar():
    t = cauda()
    texto = '\n'.join(t)
    d = {'estado': 'OK', 'motivos': [], 'ultimas': t[-3:]}
    if not t:
        d['estado'] = 'SEM_SESSAO'
        d['motivos'].append('nenhum log de sessao encontrado')
        return d
    # morte / menu
    curto = '\n'.join(t[-JANELA_CURTA:])
    if re.search(r'Menu Principal|< Morto >|Digite o nome de seu personagem|Voc[eê] est[aá] morto', curto):
        d['estado'] = 'MORTA'
        d['motivos'].append('sinal de morte ou menu principal no log')
    # personagem descansando (o jogo recusa andar)
    if texto.count('muito relaxado') >= 3:
        d['estado'] = 'TRAVADO'
        d['motivos'].append('varias recusas por estar relaxado (descansando)')
    # fome e sede
    if 'morrendo de fome' in texto:
        d['estado'] = 'FOME'
        d['motivos'].append('morrendo de fome (perde vida e mana por ciclo)')
    if 'morrendo de sede' in texto:
        if d['estado'] == 'OK':
            d['estado'] = 'SEDE'
        d['motivos'].append('morrendo de sede (perde vida e mana por ciclo)')
    # guarda de repeticao
    if '[GUARDA]' in texto:
        d['estado'] = 'TRAVADO' if d['estado'] == 'OK' else d['estado']
        d['motivos'].append('guarda de repeticao disparou: o robo parou')
    # vitais
    v = vitais(curto)
    if v:
        hp, mn, mv = v
        d['vitais'] = {'hp': hp, 'mn': mn, 'mv': mv}
    return d


def main():
    d = diagnosticar()
    if '--json' in sys.argv:
        print(json.dumps(d, ensure_ascii=False))
    else:
        print('VIGIA:', d['estado'])
        for m in d['motivos']:
            print('  -', m)
        if 'vitais' in d:
            v = d['vitais']
            print(f"  vitais: {v['hp']}hp {v['mn']}mn {v['mv']}mv")
        print('  ultimas linhas:', ' | '.join(x.strip()[:80] for x in d['ultimas'] if x.strip()))
    return 0 if d['estado'] == 'OK' else 1


if __name__ == '__main__':
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    sys.exit(main())
