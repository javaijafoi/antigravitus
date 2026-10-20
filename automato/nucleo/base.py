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


def origem():
    """Quem manda o comando, para o transcript: MUD_ORIGEM ou o nome do script (navegar, trabalhar,
    xadrez_cascata...). O auditar_sessao.py so' conta como jogo a mao o que vem do play.py."""
    return (os.environ.get('MUD_ORIGEM') or Path(sys.argv[0] or 'automato').stem or 'automato')[:40]


def call(command, timeout=60.0):
    sock = socket.socket()
    sock.settimeout(timeout)
    sock.connect((HOST, PORT))
    sock.sendall((token() + '\t' + origem() + '\n' + command + '\n').encode('utf-8'))
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
        # Fome e sede vem do driver; o ultimo valor vale para quem perguntar depois.
        sup = payload.get('supplies')
        if isinstance(sup, dict):
            for chave in ('fome', 'sede'):
                if sup.get(chave) is not None:
                    _SUPRIMENTOS[chave] = sup[chave]
    _vigiar_repeticao(text, 3, command)
    return text, vitals, combate


_SUPRIMENTOS = {'fome': None, 'sede': None}


def suprimentos():
    """Fome e sede mais recentes, como o driver reportou. None = ainda nao visto.

    Existe porque `run` devolve tres valores e mudar a assinatura quebraria
    todas as rotinas. Antes disto, nenhuma rotina sabia que a personagem
    estava morrendo de fome.
    """
    return dict(_SUPRIMENTOS)


LINHA = re.compile('^(Norte|Sul|Leste|Oeste|Cima|Baixo)\\s*-\\s*(.+)$')
D = {'Norte': 'n', 'Sul': 's', 'Leste': 'e', 'Oeste': 'w', 'Cima': 'u', 'Baixo': 'd'}
OP = {'n': 's', 's': 'n', 'e': 'w', 'w': 'e', 'u': 'd', 'd': 'u'}
INICIO = time.time()


def reiniciar_relogio():
    global INICIO
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


# --- mochila de Pellinore ---------------------------------------------------
# Ela so' reduz o peso do que guarda quando esta VESTIDA (slot "sobre o corpo",
# o mesmo do manto de pano); na mao, o conteudo pesa cheio. O `put` nao enxerga a
# mochila vestida ("Nao ha nenhuma mochila aqui"). Medido ao vivo, conhecimento
# par.68: 4 lancas na mochila na mao = 123 kg (acima do teto de 115); vestida = 50.
def guardar_na_mochila(*seletores):
    """Guarda itens na mochila e a deixa VESTIDA: tira -> put -> veste.

    `seletores` sao os alvos do put (ex.: 'all.lanca', 'coroa'). Devolve a lista
    de (seletor, texto). Se o slot estiver ocupado pelo manto, tira o manto antes.
    """
    resultados = []
    run('remove %s' % config.MOCHILA)
    for sel in seletores:
        t, _, _ = run('put %s %s' % (sel, config.MOCHILA))
        resultados.append((sel, t))
    t, _, _ = run('wear %s' % config.MOCHILA)
    if 'já está usando' in t or 'ja esta usando' in t.lower():
        run('remove manto')
        run('wear %s' % config.MOCHILA)
    return resultados


def espolio_proibido(nome_ou_identify):
    """True se o texto (nome do item ou saida do identify) indica item proibido."""
    t = (nome_ou_identify or '').lower()
    if any(p in t for p in config.ESPOLIOS_PROIBIDOS):
        return True
    return any(f in t for f in config.FLAGS_DE_MALDICAO)


# --- consider antes de atacar (diretiva §2) --------------------------------
# Revisao de 16 a 20/10: 1 consider em 589 magias no dia das tres mortes do tabuleiro. O consider
# fica no script porque, a mao, ele nao acontece. O auditar_sessao.py da FALHA no primeiro ataque a
# um alvo sem consider na sessao.
PERIGO_DURO = ('suicid', 'mataria', 'menor chance', 'muito superior', 'sem chance', 'massacrad')
_CONSIDERADOS = {}


def _sem_acento(texto):
    import unicodedata
    t = unicodedata.normalize('NFKD', texto or '')
    return ''.join(c for c in t if not unicodedata.combining(c)).lower()


def perigo_duro(texto_do_consider):
    """O primeiro sinal de perigo duro na resposta do consider, ou None (diretiva §2: nao atacar)."""
    t = _sem_acento(texto_do_consider)
    return next((p for p in PERIGO_DURO if p in t), None)


def considerar(alvo):
    """`consider <alvo>` uma vez por alvo e por processo. Devolve o perigo duro achado ou None.

    Sem o alvo na sala ("Comparar sua forca com a de quem?") nada fica guardado: tenta de novo
    no proximo encontro.
    """
    chave = re.sub(r'^\d+\.', '', (alvo or '').strip().lower().split(' ')[0])
    if chave in _CONSIDERADOS:
        return _CONSIDERADOS[chave]
    t, _, _ = run('consider %s' % alvo)
    if 'oponente' not in _sem_acento(t):
        return None
    _CONSIDERADOS[chave] = perigo_duro(t)
    return _CONSIDERADOS[chave]
