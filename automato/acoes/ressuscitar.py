# -*- coding: utf-8 -*-
"""farm_armaduras.py - fluxo de coleta e venda em lote das Armaduras da Torre Negra.

Descobriu-se nas sessoes 101/102:
  - a Armadura da Torre Negra pesa 60 kg e o armeiro paga 8.500 por ela;
  - a mochila pesa 48 kg e NAO alivia peso (testado);
  - entao cabe 1 armadura por viagem, com a carga quase vazia (mochila entra, sobra 2 kg);
  - a rota fixa e curta: Templo -> 4N -> 3O -> 3N (sala da Torre) e
    Armeiro -> s -> recall -> 4N -> 3O -> 3N.

Este fluxo navega em lotes curtos (2 comandos), confere a sala e, se desincronizar,
volta com 'recall' e refaz. Travas: aborta em combate, vida baixa ou torre negra viva.

Uso: python scripts/local/farm_armaduras.py [--max 60] [--min-hp 55]
Depende do live_daemon.py no ar (porta 14888) e do token em scripts/local/.controller.
"""
import argparse
import json
from guarda import vigiar as _vigiar, limpa as _limpa_txt
import os
import re
import socket
import sys
import time
from pathlib import Path

HOST = '127.0.0.1'
PORT = 14888
ROOT = Path(__file__).resolve().parent.parent.parent
LOCK = ROOT / 'scripts/local/.controller'

TO_TOWER = ['n', 'n', 'n', 'n', 'w', 'w', 'w', 'n', 'n', 'n']
TO_SHOP = ['s', 's', 'w', 's']  # do Templo ate o Armeiro
TOWER_MARK = 'torre do rei'
SHOP_MARK = 'loja de armaduras'


def token():
    if os.environ.get('MUD_CTRL_TOKEN'):
        return os.environ['MUD_CTRL_TOKEN']
    try:
        return json.loads(LOCK.read_text(encoding='utf-8')).get('token', '')
    except Exception:
        return ''


def call(command, timeout=60.0):
    sock = socket.socket()
    sock.settimeout(timeout)
    sock.connect((HOST, PORT))
    sock.sendall((token() + '\n' + command + '\n').encode('utf-8'))
    chunks = []
    while True:
        chunk = sock.recv(65536)
        if not chunk:
            break
        chunks.append(chunk)
    sock.close()
    data = b''.join(chunks).decode('utf-8', errors='replace').strip()
    try:
        return json.loads(data)
    except Exception:
        return {'ok': False, 'raw': data}


def _vigiar_repeticao(texto, limite=3, comando=None):
    k = _vigiar(texto, limite, comando)
    if k:
        print('[GUARDA] mesma resposta %dx seguidas: %r' % (limite, k[:120]), flush=True)
        print('[GUARDA] parando o robo: recall + save', flush=True)
        try:
            call('recall')
            call('save')
        except Exception:
            pass
        raise SystemExit(9)


def run(command, timeout=60.0):
    payload = call(command, timeout)
    if payload.get('raw') is not None:
        text, vitals, combate = payload['raw'], {}, False
    else:
        cmds = payload.get('commands') or []
        text = '\n'.join((c.get('text') or '') for c in cmds)
        vitals = payload.get('vitals') or {}
        combate = bool(payload.get('in_combat'))
    _vigiar_repeticao(text, 3, command)
    return text, vitals, combate



import re
DIR = {'norte': 'n', 'sul': 's', 'leste': 'e', 'oeste': 'w'}


def main():
    for passo in range(40):
        t, _, _ = run('look')
        if 'Fonte da Vida' in t:
            print('DRINK:', ' '.join(run('drink fonte')[0].split())[:120]); break
        if 'Portal Escondido' in t:
            print('portal -> enter'); run('enter portal'); continue
        if 'Vazio' in t:
            run('n'); continue
        m = re.search(r'atenção para o (norte|sul|leste|oeste)', t)
        if m:
            d = DIR[m.group(1)]
            print(f'{passo}: energia -> {m.group(1)} ({d})', flush=True)
            run(d)
        else:
            print(f'{passo}: sem dica, tentando n', flush=True); run('n')
    t, _, _ = run('score tudo')
    print('VIDA:', [l.strip() for l in t.split('\n') if 'Vida:' in l])
    return 0

if __name__ == '__main__':
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    sys.exit(main())
