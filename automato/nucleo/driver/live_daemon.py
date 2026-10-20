# -*- coding: utf-8 -*-
"""
live_daemon.py - sessao viva persistente com debomud.org:4000 (driver V2.1).

Garantias:
- Instancia unica: o socket IPC e reservado ANTES do login; se a porta 14888 estiver
  em uso, o processo sai sem abrir uma segunda sessao no MUD.
- Token obrigatorio: todo comando precisa vir precedido do token de
  automato/runtime/.controller; clientes sem token sao recusados sem executar nada.
- Sem segredo embutido: a senha vem de MUD_PASS ou automato/runtime/.mud_pass.
- Leitura por prompt (send_prompt): resposta correlacionada ao comando.
- Log de sessao nomeado por dia + carimbo e transcricao JSONL de evidencia.
- _RESYNC reafirma wake/stand/wear all/wimpy; _CLOSE confirma save (e sleep).

Protocolo: uma conexao TCP em 127.0.0.1:14888, payload = "<token>[\t<origem>]\n<comando>".
  A origem (play, navegar, trabalhar...) vai para cada comando do transcript (campo "origem").
  _PING | _STATUS | _RESYNC [wimpy] | _CLOSE [sleep] | _RAW <cmd> | <cmd[;cmd...]>
"""
import json
import os
import re
import socket
import sys
import time
import uuid
from datetime import datetime
from pathlib import Path

AQUI = Path(__file__).resolve().parent          # automato/nucleo/driver
AUTOMATO = AQUI.parents[1]                       # automato/
ROOT = AQUI.parents[2]                           # raiz do projeto
RUNTIME = AUTOMATO / 'runtime'                   # token, senha e logs
RUNTIME.mkdir(parents=True, exist_ok=True)
sys.path.insert(0, str(AQUI))

from debo_bot import DeboClient

HOST = '127.0.0.1'
PORT = 14888
DAY = int(os.environ.get('MUD_DAY', '97'))
WIMPY = int(os.environ.get('MUD_WIMPY', '30'))
STAMP = datetime.now().strftime('%Y%m%d_%H%M%S')
SESSION_ID = uuid.uuid4().hex[:6]
LOG_FILE = RUNTIME / f'session_live_dia{DAY}_{STAMP}_{SESSION_ID}.log'
TRANSCRIPT = RUNTIME / f'transcript_dia{DAY}_{STAMP}_{SESSION_ID}.jsonl'
CONTROLLER = RUNTIME / '.controller'
SAVE_RE = re.compile(r'salv', re.I)
SLEEP_RE = re.compile(r'(dorm|deita|adormec|acorda)', re.I)


def controller_token():
    if CONTROLLER.is_file():
        try:
            return (json.loads(CONTROLLER.read_text(encoding='utf-8')) or {}).get('token', '') or ''
        except Exception:
            return ''
    return ''


def credential():
    value = os.environ.get('MUD_PASS')
    if value:
        return value.strip()
    local = RUNTIME / '.mud_pass'
    if local.is_file():
        return local.read_text(encoding='utf-8').strip()
    raise SystemExit('[DAEMON] Credencial ausente: defina MUD_PASS ou crie scripts/local/.mud_pass')


class Session:
    def __init__(self, client):
        self.client = client
        self.transcript = TRANSCRIPT.open('a', encoding='utf-8')
        self.alive = True

    def record(self, kind, **data):
        entry = {'at': datetime.now().astimezone().isoformat(timespec='seconds'), 'kind': kind}
        entry.update(data)
        self.transcript.write(json.dumps(entry, ensure_ascii=False) + '\n')
        self.transcript.flush()

    def status(self):
        c = self.client
        return {
            'vitals': dict(c.vitals),
            'supplies': dict(c.supplies),
            'in_combat': bool(c.in_combat),
            'state': c.current_state,
            'last_move': c.last_move,
            'room': (c.last_room_info or {}).get('title'),
            'day': DAY, 'wimpy': WIMPY,
            'log': LOG_FILE.name, 'transcript': TRANSCRIPT.name,
        }

    def drain(self, kind='spontaneous'):
        text = self.client.recv_chunk()
        if text.strip():
            self.record(kind, text=text.strip(), vitals=dict(self.client.vitals),
                        in_combat=bool(self.client.in_combat), state=self.client.current_state)
        return text

    def run(self, command, timeout=8.0, origem=None):
        pre = self.drain('preroll')
        result = self.client.send_prompt(command, timeout=timeout)
        result['preroll'] = pre.strip()
        if origem:
            # quem mandou (play, navegar, trabalhar...): o auditar_sessao.py separa jogo a mao de rotina
            result['origem'] = origem
        self.record('command', **result)
        return result

    def resync(self, wimpy=None):
        w = WIMPY if wimpy is None else int(wimpy)
        results = {}
        for label, command in (('wake', 'wake'), ('stand', 'stand'), ('wear', 'wear all'), ('wimpy', f'wimpy {w}')):
            results[label] = self.run(command, timeout=5.0)
        return results

    def close_session(self, sleep=False):
        steps = {}
        steps['stand'] = self.run('stand', timeout=5.0)
        steps['save'] = self.run('save', timeout=6.0)
        steps['save_confirmed'] = bool(SAVE_RE.search(steps['save'].get('text', '')))
        if sleep:
            steps['sleep'] = self.run('sleep', timeout=6.0)
            steps['sleep_confirmed'] = bool(SLEEP_RE.search(steps['sleep'].get('text', '')))
        self.drain('tail')
        self.record('close', sleep=sleep, save_confirmed=steps.get('save_confirmed'),
                    sleep_confirmed=steps.get('sleep_confirmed'), state=self.client.current_state)
        return steps


def connect():
    password = credential()
    client = DeboClient(log_path=str(LOG_FILE), password=password)
    last = None
    for attempt in range(1, 4):
        try:
            client.connect()
            client.login('Grebolius', password=password, wimpy=WIMPY)
            return client
        except Exception as error:
            last = error
            print(f'[DAEMON] tentativa {attempt} falhou: {error}', flush=True)
            try:
                client.close()
            except Exception:
                pass
            client = DeboClient(log_path=str(LOG_FILE), password=password)
            time.sleep(5)
    raise SystemExit(f'[DAEMON] Nao foi possivel conectar: {last}')


def ler_cabecalho(linha):
    """Primeira linha do pedido: "<token>" ou "<token>\\t<origem>". Clientes antigos mandam so' o token
    e ficam sem origem; play.py manda "play", as rotinas mandam o nome do script (base.origem())."""
    token, _, origem = linha.strip('\r\n ').partition('\t')
    return token.strip(), (origem.strip()[:40] or None)


def handle(session, cmd, token, origem=None):
    raw = cmd.strip()
    if not raw:
        return {'ok': False, 'error': 'comando vazio'}
    if raw == '_PING':
        return {'ok': True, 'pong': True, **session.status()}
    if raw == '_STATUS':
        session.drain('status_preroll')
        return {'ok': True, **session.status()}
    if raw.startswith('_RESYNC'):
        parts = raw.split()
        results = session.resync(parts[1] if len(parts) > 1 else None)
        return {'ok': True, **session.status(),
                'resync': {k: {'text': v.get('text', '').strip(), 'prompt': v.get('prompt'), 'timeout': v.get('timeout')} for k, v in results.items()}}
    if raw.startswith('_CLOSE'):
        sleep = 'sleep' in raw.split()[1:]
        steps = session.close_session(sleep=sleep)
        return {'ok': True, 'closed': True,
                'save_confirmed': steps.get('save_confirmed'),
                'sleep_confirmed': steps.get('sleep_confirmed'),
                'steps': {k: (v.get('text', '').strip() if isinstance(v, dict) else v) for k, v in steps.items()}}
    if raw.startswith('_RAW '):
        commands = [raw[5:].strip()]
    else:
        commands = [part.strip() for part in raw.split(';') if part.strip()]
    out = [session.run(command, timeout=8.0, origem=origem) for command in commands]
    return {'ok': True, 'commands': out, **session.status()}


def port_in_use():
    """No Windows dois sockets podem dividir a mesma porta com SO_REUSEADDR; por isso o
    teste decisivo e tentar conectar: se alguem responde, ja existe controlador ativo."""
    probe = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    probe.settimeout(0.8)
    try:
        probe.connect((HOST, PORT))
        return True
    except OSError:
        return False
    finally:
        try:
            probe.close()
        except Exception:
            pass


def main():
    expected = controller_token()
    if port_in_use():
        print(f'[DAEMON] ja existe controlador ativo em {HOST}:{PORT}; instancia recusada sem tocar no MUD.', flush=True)
        raise SystemExit(3)
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    try:
        server.bind((HOST, PORT))
    except OSError as error:
        print(f'[DAEMON] porta {PORT} ja ocupada ({error}); instancia unica recusada.', flush=True)
        raise SystemExit(2)
    server.listen(5)
    server.settimeout(1.0)
    print(f'[DAEMON] dia={DAY} wimpy={WIMPY} sessao={SESSION_ID} auth={"on" if expected else "off"}', flush=True)
    print(f'[DAEMON] log={LOG_FILE.name}', flush=True)
    client = connect()
    session = Session(client)
    session.record('open', hero='Grebolius', day=DAY, wimpy=WIMPY, log=LOG_FILE.name)
    session.resync()
    print(f'[DAEMON] pronto em {HOST}:{PORT}', flush=True)
    try:
        while session.alive:
            try:
                conn, _ = server.accept()
            except socket.timeout:
                session.drain('idle')
                continue
            except Exception as error:
                print(f'[DAEMON] accept: {error}', flush=True)
                break
            try:
                conn.settimeout(60.0)
                data = conn.recv(8192).decode('utf-8', errors='replace')
                token, _, cmd = data.partition('\n')
                token, origem = ler_cabecalho(token)
                if expected and token != expected:
                    session.record('rejected', cmd=cmd.strip()[:200])
                    conn.sendall((json.dumps({'ok': False, 'error': 'unauthorized'}) + '\n').encode('utf-8'))
                    continue
                if not cmd.strip():
                    conn.close()
                    continue
                payload = handle(session, cmd, token, origem=origem)
                conn.sendall((json.dumps(payload, ensure_ascii=False) + '\n').encode('utf-8', errors='replace'))
                if payload.get('closed'):
                    session.alive = False
            except Exception as error:
                try:
                    conn.sendall((json.dumps({'ok': False, 'error': str(error)}, ensure_ascii=False) + '\n').encode('utf-8'))
                except Exception:
                    pass
            finally:
                try:
                    conn.close()
                except Exception:
                    pass
    finally:
        try:
            session.record('shutdown', state=client.current_state)
            session.transcript.close()
        except Exception:
            pass
        try:
            client.close()
        except Exception:
            pass
        try:
            server.close()
        except Exception:
            pass
        print('[DAEMON] finalizado', flush=True)


if __name__ == '__main__':
    main()
