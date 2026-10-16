# -*- coding: utf-8 -*-
"""play.py - cliente IPC do live_daemon.py (driver V2) com trava de controlador unico.

Uso: python scripts/local/play.py "look" [--json]
Para comandar, defina MUD_CTRL_TOKEN com o token de automato/runtime/.controller.
"""
import argparse
import json
import os
import socket
import sys
from pathlib import Path

HOST = '127.0.0.1'
PORT = 14888
ROOT = Path(__file__).resolve().parents[3]
LOCK = ROOT / 'automato' / 'runtime' / '.controller'


def controller_ok():
    if not LOCK.is_file():
        return True
    try:
        lock = json.loads(LOCK.read_text(encoding='utf-8'))
    except Exception:
        return True
    token = lock.get('token')
    if not token:
        return True
    if os.environ.get('MUD_CTRL_TOKEN') == token:
        return True
    print('[BLOQUEADO] O controle da sessao viva pertence a ' + str(lock.get('owner')) + '. '
          'Comandos concorrentes podem matar a personagem. Encerre o loop concorrente ou defina '
          'MUD_CTRL_TOKEN correto para reassumir.')
    return False


def call(command, timeout=60.0):
    token = os.environ.get('MUD_CTRL_TOKEN', '')
    sock = socket.socket()
    sock.settimeout(timeout)
    sock.connect((HOST, PORT))
    sock.sendall((token + '\n' + command + '\n').encode('utf-8'))
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


def render(payload):
    if payload.get('raw') is not None:
        return payload['raw']
    parts = []
    for item in payload.get('commands', []):
        parts.append(f">>> {item.get('cmd')}")
        parts.append((item.get('text') or '').rstrip())
        flags = []
        if item.get('timeout'):
            flags.append('TIMEOUT')
        if not item.get('prompt'):
            flags.append('SEM_PROMPT')
        if item.get('in_combat'):
            flags.append('EM_COMBATE')
        if flags:
            parts.append('[' + ' | '.join(flags) + ']')
    resync = payload.get('resync') or {}
    for label, item in resync.items():
        parts.append(f">>> [{label}] {('' if item.get('prompt') else '(sem prompt) ')}{(item.get('text') or '').strip()}")
    steps = payload.get('steps') or {}
    for label, text in steps.items():
        parts.append(f">>> [{label}] {text}")
    if payload.get('closed'):
        parts.append(f"[FECHADO] save_confirmed={payload.get('save_confirmed')} sleep_confirmed={payload.get('sleep_confirmed')}")
    if payload.get('error'):
        parts.append(f"[ERRO] {payload['error']}")
    vitals = payload.get('vitals') or {}
    if vitals:
        sup = payload.get('supplies') or {}
        def _sup(v):
            return {True: 'SIM', False: 'nao', None: '?'}[v]
        parts.append(
            f"[vitais hp={vitals.get('hp')} mn={vitals.get('mana')} mv={vitals.get('mv')}"
            f" | fome={_sup(sup.get('fome'))} sede={_sup(sup.get('sede'))}"
            f" | combate={payload.get('in_combat')} | estado={payload.get('state')} | sala={payload.get('room')}]")
    return '\n'.join(parts)


def main():
    parser = argparse.ArgumentParser(description='Cliente IPC do live_daemon.py')
    parser.add_argument('command', nargs='*')
    parser.add_argument('--json', action='store_true')
    parser.add_argument('--timeout', type=float, default=90.0)
    args = parser.parse_args()
    if not controller_ok():
        sys.exit(9)
    payload = call(' '.join(args.command), args.timeout)
    if args.json:
        print(json.dumps(payload, ensure_ascii=False, indent=1))
    else:
        print(render(payload))


if __name__ == '__main__':
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    main()
