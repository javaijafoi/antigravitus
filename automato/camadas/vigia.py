# -*- coding: utf-8 -*-
"""vigia.py - o vigia da personagem.

Le a cauda do log do daemon (leitura pura: nao manda comando nenhum ao MUD,
portanto NAO interfere no motor que estiver rodando) e devolve um diagnostico:

    OK | FOME | SEDE | VIDA_BAIXA | MANA_BAIXA | MORTA | TRAVADO | SEM_SESSAO

Uso:
    python automato/camadas/vigia.py            # texto legivel
    python automato/camadas/vigia.py --json     # para uso por outros robos

Quem RODA o vigia em laco e' o turno.py (a cada 60 s). Sozinho ele e' um
retrato do agora: se ninguem chamar, ninguem ve.
"""
import json
import re
import socket
import sys
from pathlib import Path

import sys
from pathlib import Path as _P
sys.path.insert(0, str(_P(__file__).resolve().parents[1] / 'nucleo'))
import config
LOCAL = config.DIR_LOGS
LIMITE_VIDA = 0.45
LIMITE_MANA = 0.15
LINHAS = 12000          # varredura de estado: o sinal de fome pode ficar longe do fim
JANELA_CURTA = 40       # vitais e morte: so' o que acabou de acontecer
JANELA_MEDIA = 300      # travamento e guarda: recente, mas com folga


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


def fome_e_sede(linhas):
    """Decide fome e sede pelo evento MAIS RECENTE, nao por janela fixa.

    Antes o vigia so' olhava as ultimas 120 linhas. Numa sessao real a ultima
    rajada de 'morrendo de fome' ficou a 546 linhas do fim, e nesse vao ele
    respondia OK com a personagem morrendo de fome. Agora vale o bloco
    '[Situacao atual]' mais recente - que diz o AGORA - ou, se houver, uma
    rajada posterior a ele.
    """
    idx_sit = max((i for i, l in enumerate(linhas) if re.search(r'situa..o atual', l, re.I)), default=-1)
    idx_fome = max((i for i, l in enumerate(linhas) if 'morrendo de fome' in l.lower()), default=-1)
    idx_sede = max((i for i, l in enumerate(linhas) if 'morrendo de sede' in l.lower()), default=-1)
    if idx_sit == -1:
        return idx_fome != -1, idx_sede != -1
    bloco = '\n'.join(linhas[idx_sit:idx_sit + 30]).lower()
    return ('fome' in bloco) or (idx_fome > idx_sit), ('sede' in bloco) or (idx_sede > idx_sit)


def vitais(texto):
    m = re.findall(r'(\d+)hp (\d+)mn (\d+)mv', texto)
    return tuple(int(x) for x in m[-1]) if m else None


def do_driver(timeout=2.0):
    """Pergunta ao driver pelo _STATUS. IPC local: NAO manda comando ao MUD.

    O log pode estar desatualizado, e foi assim que a personagem chegou a
    "morrendo de fome" com o vigia respondendo OK: o texto tinha saido da janela.
    O driver sabe o agora - fome, sede, combate e estado. Devolve None se o
    daemon nao estiver no ar.
    """
    try:
        lock = json.loads(config.LOCK.read_text(encoding='utf-8'))
        token = lock.get('token', '')
    except Exception:
        token = ''
    try:
        s = socket.socket()
        s.settimeout(timeout)
        s.connect((config.HOST, config.PORT))
        s.sendall((token + '\n_STATUS\n').encode('utf-8'))
        dados = b''
        while True:
            pedaco = s.recv(65536)
            if not pedaco:
                break
            dados += pedaco
        s.close()
        return json.loads(dados.decode('utf-8', 'replace'))
    except Exception:
        return None


def diagnosticar():
    t = cauda()
    medio = '\n'.join(t[-JANELA_MEDIA:])
    d = {'estado': 'OK', 'motivos': [], 'ultimas': t[-3:]}
    if not t:
        d['estado'] = 'SEM_SESSAO'
        d['motivos'].append('nenhum log de sessao encontrado')
        return d
    # morte / menu: so' o que acabou de acontecer, e so' com sinal FORTE.
    #
    # "Menu Principal" sozinho NAO serve: o proprio servidor escreve
    # "...utilize o comando SAIR para ir ate' o Menu Principal, e, la'..." numa
    # DICA. O vigia casava essa dica, declarava MORTA com a personagem inteira e
    # o turno rodava o ressuscitar sem necessidade - medido na linha 82835 da
    # sessao do Dia 156. Os padroes agora exigem a linha inteira.
    curto = '\n'.join(t[-JANELA_CURTA:])
    SINAIS_MORTE = (
        r'^\s*<\s*Morto\s*>',                    # titulo de sala do Paraiso
        r'Voc[eê]\s+est[aá]\s+mort[oa]',
        r'^\s*Menu Principal\s*$',               # a linha do menu, sozinha
        r'^\s*Digite o nome de seu personagem',  # desconexao de verdade
    )
    if any(re.search(padrao, curto, re.M | re.I) for padrao in SINAIS_MORTE):
        d['estado'] = 'MORTA'
        d['motivos'].append('sinal de morte ou menu principal no log')
    # personagem descansando (o jogo recusa andar)
    if medio.count('muito relaxado') >= 3:
        d['estado'] = 'TRAVADO'
        d['motivos'].append('varias recusas por estar relaxado (descansando)')
    # FONTE 1: o driver. Ele sabe o AGORA - fome, sede, combate, estado.
    drv = do_driver()
    if drv:
        d['driver'] = drv
        sup = drv.get('supplies') or {}
        for chave in ('fome', 'sede'):
            if sup.get(chave) is not None:
                d[chave] = sup[chave]
        vit = drv.get('vitals') or {}
        if vit.get('hp') is not None:
            d['vitais'] = {'hp': vit.get('hp'), 'mn': vit.get('mana'), 'mv': vit.get('mv')}
        if drv.get('in_combat'):
            d['estado'] = 'EM_COMBATE'
            d['motivos'].append('em combate agora (o driver viu)')
        if drv.get('state') == 'disconnected':
            d['estado'] = 'SEM_SESSAO'
            d['motivos'].append('driver sem conexao com o MUD')
        # FONTE 2 (reserva): o log, so' para o que o driver nao cobre.
        if 'fome' not in d or 'sede' not in d:
            fome_log, sede_log = fome_e_sede(t)
            d.setdefault('fome', fome_log)
            d.setdefault('sede', sede_log)
    else:
        d['motivos'].append('driver fora do ar; lendo so o log (pode estar vazio de fome/sede)')
        fome, sede = fome_e_sede(t)
        d['fome'], d['sede'] = fome, sede

    if d.get('fome') and d['estado'] not in ('MORTA', 'SEM_SESSAO', 'EM_COMBATE'):
        d['estado'] = 'FOME'
        d['motivos'].append('morrendo de fome (perde vida e mana por ciclo)')
    if d.get('sede') and d['estado'] == 'OK':
        d['estado'] = 'SEDE'
        d['motivos'].append('morrendo de sede (perde vida e mana por ciclo)')
    # guarda de repeticao
    if '[GUARDA]' in medio:
        d['estado'] = 'TRAVADO' if d['estado'] == 'OK' else d['estado']
        d['motivos'].append('guarda de repeticao disparou: o robo parou')
    return d


def main():
    d = diagnosticar()
    if '--json' in sys.argv:
        print(json.dumps(d, ensure_ascii=False))
    else:
        print('VIGIA:', d['estado'])
        for m in d['motivos']:
            print('  -', m)
        print('  fome: %s | sede: %s' % (
            {True: 'SIM', False: 'nao', None: '?'}[d.get('fome')],
            {True: 'SIM', False: 'nao', None: '?'}[d.get('sede')]))
        if 'vitais' in d:
            v = d['vitais']
            print(f"  vitais: {v['hp']}hp {v['mn']}mn {v['mv']}mv")
        print('  ultimas linhas:', ' | '.join(x.strip()[:80] for x in d['ultimas'] if x.strip()))
    return 0 if d['estado'] == 'OK' else 1


if __name__ == '__main__':
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    sys.exit(main())
