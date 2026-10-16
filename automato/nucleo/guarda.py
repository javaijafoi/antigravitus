"""Guarda de repeticao para os robos do DeBoMUD.

Ideia (do autor): se a MESMA resposta vier 3x seguidas, o robo nao deve insistir —
ele para, salva e devolve o controle para o agente consertar.

Motivo pratico: as mortes #5, #6 e #7 vieram de scripts insistindo em um estado
travado (sala bloqueada, alvo inexistente, personagem descansando). A repeticao
e o sinal mais barato de "isto nao vai andar".
"""
import re

LIMITE = 3
# Comandos cuja repeticao e' legitima (comprar, comer, beber, olhar...). Nao disparam a guarda.
BENIGNOS = ('buy', 'eat', 'drink', 'deposit', 'withdraw', 'balance', 'practice', 'score',
            'inventory', 'equipment', 'i', 'save', 'rest', 'sleep', 'wake', 'stand', 'look',
            'exits', 'who', 'help', 'ajuda', 'consider', 'identify', 'value')
_ESTADO = {'chave': None, 'n': 0, 'historico': []}


def limpa(texto):
    t = re.sub(r'\s+', ' ', (texto or '')).strip()
    t = re.sub(r'\d+hp \d+mn \d+mv', '', t)
    return t[:180]


def vigiar(texto, limite=LIMITE, comando=None):
    """Registra a resposta. Devolve a mensagem repetida quando atinge o limite."""
    base = (comando or '').strip().split(' ')[0].lower()
    if base in BENIGNOS:
        _ESTADO['chave'] = None
        _ESTADO['n'] = 0
        return None
    k = limpa(texto)
    if not k:
        _ESTADO['chave'] = None
        _ESTADO['n'] = 0
        return None
    if k == _ESTADO['chave']:
        _ESTADO['n'] += 1
    else:
        _ESTADO['chave'] = k
        _ESTADO['n'] = 1
        _ESTADO['historico'].append(k)
        _ESTADO['historico'] = _ESTADO['historico'][-20:]
    return k if _ESTADO['n'] >= limite else None


def historico():
    return list(_ESTADO['historico'])
