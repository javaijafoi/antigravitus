# -*- coding: utf-8 -*-
"""vender_espolio.py - rotina de venda de espolio nos dois comerciantes de Midgaard. ID: vender_espolio

Por que existe (2026-10-21): o autor perguntou "o caixa do comerciante ja' voltou?" e nao havia
rotina para responder. As vendas estavam espalhadas em `xadrez_v2/v3` (legado, que pega espolio
antes da triagem) e em `novatos.vender_espolios`. Aqui a venda e' uma rotina propria:

  * **`value <item>` antes do `sell`**: o Armeiro informa a oferta (validado no Dia 156); so'
    vende acima de `minimo`;
  * **whitelist explicita** de tipos (arma/armadura/escudo). Todo o resto do inventario - tomo,
    cetro, coroa, mochila, cantil, joias, equipamento vestido - nunca e' tocado;
  * **para quando o caixa seca**: "Eu nao posso pagar por uma arma dessas!" encerra aquele
    comerciante e a rotina segue para o outro, sem laco de `sell`;
  * **relatorio** com o que vendeu, por quanto, e o estado do caixa de cada um.

Uso:
    python automato/camadas/trabalhar.py --rotina vender_espolio
    from vender_espolio import executar; executar(max_itens=2, minimo=1000)
"""
import re
import sys
import time
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]
for _p in ('nucleo', 'camadas', 'rotinas', 'acoes'):
    sys.path.insert(0, str(RAIZ / 'automato' / _p))

import base                      # noqa: E402
from base import run             # noqa: E402

# tipos que os dois comerciantes compram (whitelist: fora daqui nada e' vendido)
VENDAVEIS = ('espada', 'escudo', 'armadura', 'lan\u00e7a', 'lanca', 'machado', 'adaga', 'clava')
# nunca tocar, mesmo que o nome contenha uma palavra da whitelist
PROTEGIDOS = ('tomo', 'cetro', 'coroa', 'mochila', 'cantil', 'rosario', 'ros\u00e1rio', 'colar',
              'anel', 'bota', 'luva', 'cinto', 'veste', 'tunica', 't\u00fanica', 'pao', 'p\u00e3o',
              'pergaminho', 'pocao', 'po\u00e7\u00e3o', 'chave', 'lamina', 'l\u00e2mina')

RECUSAS = ('nao posso pagar', 'n\u00e3o posso pagar', 'nao compro', 'n\u00e3o compro',
           'nao quero', 'n\u00e3o quero', 'nao estou interessado', 'n\u00e3o estou interessado')

ARMEIRO = ('loja_armaduras', ('armadura', 'escudo'))
FERREIRO = ('loja_armas', ('espada', 'lan\u00e7a', 'lanca', 'machado', 'adaga', 'clava'))


def sem_acento(texto):
    return (texto or '').lower()


def inventario():
    """Nomes dos itens carregados, do `inventory`. Lista vazia se nao deu para ler."""
    t, _v, _c = run('inventory')
    itens, dentro = [], False
    for linha in (t or '').split('\n'):
        crua = linha.strip()
        if not crua or crua.startswith('Voc'):
            if dentro and not crua:
                continue
            continue
        if 'carregando' in sem_acento(crua):
            dentro = True
            continue
        if dentro and crua:
            nome = re.sub(r'^\(x\d+\)\s*', '', crua).strip(' .')
            if nome:
                itens.append(nome)
    return itens


def vendavel(nome):
    a = sem_acento(nome)
    if any(p in a for p in PROTEGIDOS):
        return False
    return any(v in a for v in VENDAVEIS)


def oferta(item):
    """Valor que o comerciante oferece (int) ou None. Aceita '1.500' e '1500'."""
    t, _v, _c = run('value %s' % item)
    m = re.search(r'(\d[\d.]*)\s*(?:moedas|coins?)', sem_acento(t) or '')
    if not m:
        m = re.search(r'(\d[\d.]{2,})', t or '')
    if not m:
        return None
    try:
        return int(m.group(1).replace('.', ''))
    except ValueError:
        return None


def ouro():
    t, _v, _c = run('gold')
    m = re.search(r'(\d[\d.]*)', t or '')
    return int(m.group(1).replace('.', '')) if m else None


def _ir(destino):
    import navegar
    try:
        mapa = navegar.carregar_mapa()
        navegar.navegar(mapa, 'templo_midgaard', destino, run)
        return True
    except Exception as e:      # noqa: BLE001 - rota e' o unico caminho conhecido
        print('[VENDER] ATENCAO: nao cheguei em %s (%s)' % (destino, e), flush=True)
        return False


def _vender_no(local, tipos, max_itens, minimo, caixa, ouro0):
    """Vende, num comerciante, os itens do inventario que casam com `tipos`."""
    if not _ir(local):
        caixa[local] = 'sem rota'
        return
    for item in inventario():
        if len(caixa.get('vendidos', [])) >= max_itens:
            break
        a = sem_acento(item)
        if not any(t in a for t in tipos) or not vendavel(item):
            continue
        valor = oferta(item)
        if valor is None:
            caixa.setdefault('pulados', []).append({'item': item, 'motivo': 'sem oferta legivel'})
            continue
        if valor < minimo:
            caixa.setdefault('pulados', []).append({'item': item, 'motivo': 'oferta %d < minimo %d' % (valor, minimo)})
            continue
        t, _v, _c = run('sell %s' % item)
        if any(r in sem_acento(t) for r in RECUSAS):
            caixa['esgotado'] = True
            caixa.setdefault('recusas', []).append({'item': item, 'texto': (t or '').strip()[:120]})
            print('[VENDER] caixa esgotado em %s: %s' % (local, (t or '').strip()[:80]), flush=True)
            return
        caixa['vendidos'].append({'item': item, 'oferta': valor})
        print('[VENDER] %s por %d' % (item, valor), flush=True)


def executar(max_itens=6, max_s=150, minimo=200):
    """Vende o espolio vendavel nos dois comerciantes e devolve o relatorio."""
    t0 = time.time()
    ouro0 = ouro()
    rel = {'vendidos': [], 'recusas': [], 'pulados': [], 'caixa': {}, 'ouro_antes': ouro0,
           'ouro_depois': None, 'usados_s': 0.0}
    print('[VENDER] inicio: %d itens carregados' % len(inventario()), flush=True)
    run('recall')
    run('stand')
    try:
        import cuidar
        cuidar.cuidar()
    except Exception as e:      # noqa: BLE001 - sem magia ainda da' para vender
        print('[VENDER] aviso: cuidar falhou (%s)' % e, flush=True)

    for local, tipos in (ARMEIRO, FERREIRO):
        if time.time() - t0 > max_s:
            rel['caixa'][local] = 'tempo esgotado'
            break
        caixa = {'vendidos': []}
        _vender_no(local, tipos, max_itens - len(rel['vendidos']), minimo, caixa, ouro0)
        rel['vendidos'].extend(caixa.get('vendidos') or [])
        rel['pulados'].extend(caixa.get('pulados') or [])
        rel['recusas'].extend(caixa.get('recusas') or [])
        rel['caixa'][local] = 'esgotado' if caixa.get('esgotado') else 'aberto'

    rel['ouro_depois'] = ouro()
    rel['usados_s'] = round(time.time() - t0, 1)
    print('[VENDER] fim: %d vendidos, ouro %s -> %s (%.0fs)'
          % (len(rel['vendidos']), rel['ouro_antes'], rel['ouro_depois'], rel['usados_s']), flush=True)
    return rel


if __name__ == '__main__':
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    print(executar())
