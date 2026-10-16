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



import re, random, time
OP = {'n': 's', 's': 'n', 'e': 'w', 'w': 'e'}
RESERVA = config.RESERVA_OURO


def andar(d):
    r, _, _ = run(d)
    return 'não pode ir' not in r


def situacao():
    t, _, _ = run('score tudo')
    low = t.lower()
    d = {'texto': t,
         'fome': 'morrendo de fome' in low or 'com fome' in low or 'ficando com fome' in low,
         'sede': 'morrendo de sede' in low or 'com sede' in low or 'ficando com sede' in low}
    m = re.search(r'peso total de (\d+) kg', t)
    d['peso'] = int(m.group(1)) if m else None
    m = re.search(r'm\u00e1ximo (\d+) itens e um peso total de (\d+) kg', t)
    d['peso_max'] = int(m.group(2)) if m else None
    m = re.search(r'Carregando:\s*\{[^}]*\}\s*([\d.]+)', t)
    d['ouro'] = int(m.group(1).replace('.', '')) if m else None
    m = re.search(r'Banco:\s*\{[^}]*\}\s*([\d.]+)', t)
    d['banco'] = int(m.group(1).replace('.', '')) if m else None
    return d


def abastecer():
    s = situacao()
    if not (s['fome'] or s['sede']):
        return
    for m in ['s', 's', 'w', 'n']:
        andar(m)
    t, _, _ = run('look')
    if 'Padaria' not in t:
        print('[PREPARA] padaria nao encontrada', flush=True)
        return
    conv = run('inventory')[0].lower()
    tem_pao = 'p\u00e3o' in conv or 'pao' in conv
    if not tem_pao:
        for _ in range(3):
            run('buy pao')
    for _ in range(3):
        run('eat pao')
    run('drink cantil')
    run('drink cantil')
    print('[PREPARA] alimentada e hidratada', flush=True)


def hidratar():
    """A sede se resolve na FONTE da Praca do Templo; o cantil pode estar vazio."""
    s = situacao()
    if not s['sede']:
        return
    run('recall'); run('stand')
    andar('s')  # Praca do Templo
    run('fill cantil fonte')
    for _ in range(4):
        run('drink fonte')
    s2 = situacao()
    print(f"[PREPARA] hidratada na fonte (sede agora: {s2['sede']})", flush=True)


def guardar_ouro():
    s = situacao()
    ouro = s['ouro'] or 0
    if ouro <= RESERVA + 100:
        return
    deposito = ouro - RESERVA
    run(f'deposit {deposito}')
    print(f'[PREPARA] depositadas {deposito} moedas (reserva de {RESERVA} na mao)', flush=True)


def recompor():
    run('recall'); run('stand')
    run('sleep')
    time.sleep(75)
    run('wake'); run('stand')
    s = situacao()
    print(f"[PREPARA] apos o sono: {s['peso']}/{s['peso_max']} kg, fome={s['fome']}, sede={s['sede']}", flush=True)


def main():
    run('wake'); run('stand')
    run('recall')
    print('[PREPARA] inicio no Templo', flush=True)
    abastecer()
    run('recall'); run('stand')
    hidratar()
    guardar_ouro()
    recompor()
    run('recall'); run('stand')
    print('[PREPARA] pronta: no Templo, alimentada, hidratada, ouro guardado', flush=True)
    return 0


if __name__ == '__main__':
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    sys.exit(main())
