# -*- coding: utf-8 -*-
"""inventario.py - ler a bolsa e o cantil sem acreditar em resposta corrompida.

A latencia do driver mistura respostas: `inventory` pode voltar com o texto do
`score`, com um evento da sala, ou vazio. Uma leitura dessas devolvia ZERO paes,
o `cuidar` concluia "estoque acabou" e disparava uma viagem a cidade que nao era
necessaria. E' o mesmo erro que o autor apontou - parar por fome com a mochila
cheia - chegando por outro caminho.

Duas regras aqui:

   1. A resposta tem que se identificar. `inventory` sempre abre com
      "Voce esta carregando:" (ou diz que nao carrega nada). Sem esse marcador,
      leia de novo;
   2. Se mesmo assim nao vier, devolve None. **None nao e' zero**: quem chama
      deve tratar "nao sei" como "nao sei", nunca como "acabou".

Formato real medido nos registros (o MUD usa `(x3)`, nao `(3x)`):

    Voce esta carregando:
    um cantil
    uma broa
    (x3) um pao recheado
    ...
"""
import re
import time

from base import run

TENTATIVAS = 3
ESPERA = 0.4


def sem_acento(texto):
    import unicodedata
    t = unicodedata.normalize('NFKD', (texto or '').lower())
    return ''.join(c for c in t if not unicodedata.combining(c))


def ler_bolsa(tentativas=TENTATIVAS):
    """Texto do inventario, ou None se a resposta nao se identificar."""
    for _ in range(tentativas):
        t, _, _ = run('inventory')
        if 'carregando' in sem_acento(t):
            return t
        time.sleep(ESPERA)
    return None


def contar_comida(tentativas=TENTATIVAS):
    """Unidades de comida na bolsa. **None = nao consegui ler, e nao zero.**"""
    t = ler_bolsa(tentativas)
    if t is None:
        return None
    total = 0
    for linha in t.split('\n'):
        b = sem_acento(linha)
        if 'pao' in b or 'broa' in b or 'carne' in b:
            m = re.search(r'\(x(\d+)\)', linha)
            total += int(m.group(1)) if m else 1
    return total


def agua_no_cantil(tentativas=TENTATIVAS):
    """0.0 vazio .. 1.0 cheio. **None = nao consegui ler.**"""
    for _ in range(tentativas):
        t, _, _ = run('look in cantil')
        b = sem_acento(t)
        if 'nao tem' in b or 'nao esta carregando' in b:
            return None
        if 'vazio' in b or 'vazia' in b:
            return 0.0
        if 'quase cheio' in b:
            return 0.8
        if 'metade' in b:
            return 0.5
        if 'cheio' in b or 'cheia' in b:
            return 1.0
        time.sleep(ESPERA)
    return None
