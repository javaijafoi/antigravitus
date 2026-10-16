# -*- coding: utf-8 -*-
"""base.py - infraestrutura compartilhada das ROTINAS.

Uma ROTINA e um trabalho que o heroi sabe fazer de ponta a ponta:
  - sabe partir do Templo e voltar para la (o Templo e o ponto de encontro);
  - tem um laco de trabalho proprio;
  - declara seus limites (vida minima, tempo maximo);
  - e protegida pela guarda de repeticao (aqui dentro) e pelo vigia.py (fora).

Cada rotina vive em rotinas/<nome>.py e expoe:
    NOME, DESCRICAO e a funcao executar() -> bool
"""
import json
import os
import random
import re
import socket
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import config  # noqa: E402
from guarda import vigiar as _vigiar  # noqa: E402

HOST = config.HOST
PORT = config.PORT
LOCK = config.LOCK


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


LINHA = re.compile('^(Norte|Sul|Leste|Oeste)\\s*-\\s*(.+)$')
D = {'Norte': 'n', 'Sul': 's', 'Leste': 'e', 'Oeste': 'w'}
OP = {'n': 's', 's': 'n', 'e': 'w', 'w': 'e'}
INICIO = time.time()


def estourou(segundos=config.LIMITE_TEMPO):
    return time.time() - INICIO > segundos


def pex(txt):
    ex = {}
    for line in txt.split('\n'):
        m = LINHA.match(line.strip())
        if m:
            ex[D[m.group(1)]] = m.group(2).strip()
    return ex


def sala():
    e_txt, _, _ = run('exits')
    ex = pex(e_txt)
    t, _, _ = run('look')
    return ex, t


def andar(d):
    r, _, _ = run(d)
    return 'não pode ir' not in r


def ate(d, marca, lim=32):
    for _ in range(lim):
        ex, t = sala()
        if marca.lower() in t.lower():
            return True
        r, _, _ = run(d)
        if 'não pode ir' in r:
            return False
    return False


def voltar_ao_templo():
    run('recall')
    run('stand')
    return True


def hp_frac(text):
    m = re.findall('Vida:\\s*\\{[^}]*\\}\\s*(\\d+) de (\\d+)', text)
    if m:
        cur, mx = int(m[-1][0]), int(m[-1][1])
        return cur / mx if mx else 1.0
    return 1.0


def mana_baixa():
    t, _, _ = run('score')
    m = re.search('(\\d+)mn', t)
    return int(m.group(1)) < 30 if m else False


def vida_frac():
    t, _, _ = run('score')
    return hp_frac(t)
