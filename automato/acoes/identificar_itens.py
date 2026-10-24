# -*- coding: utf-8 -*-
"""identificar_itens.py - identifica TODOS os itens que a personagem tem e grava o catalogo.

Ordem do autor (2026-10-22): "obrigacao sempre identificar todos os itens que temos"
(diretiva_de_jogo.md §29). O `identify <item>` como comando e' gratuito (nao gasta mana) e mostra
tipo, flags (maldicao, NODROP, ANTI-*), peso, valor, nivel e o que o item afeta.

O que faz: le `inventory` e `equipment`, identifica um item por vez (conferindo pelo NOME que a resposta
devolve que e' o item certo e nao um homonimo) e grava `data/heroes/<heroi>/itens.json`. Item de dentro da
mochila de Pellinore nao entra aqui: tire-o (`remove mochila`, `get X mochila`), rode de novo e guarde.

Fala com o driver por `base.run` (token e origem no transcript). Nao compra, nao vende, nao larga nada.

Uso:  python automato/acoes/identificar_itens.py [--hero grebolius] [--sem-gravar]
"""
import argparse
import json
import re
import sys
import unicodedata
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'nucleo'))

ROOT = Path(__file__).resolve().parents[2]
ARTIGOS = ('o ', 'a ', 'os ', 'as ', 'um ', 'uma ', 'uns ', 'umas ')
STOP = {'um', 'uma', 'uns', 'umas', 'o', 'a', 'os', 'as', 'de', 'da', 'do', 'dos', 'das', 'par', 'belo', 'bela',
        'e', 'com', 'em', 'para', 'que', 'no', 'na', 'resistentes', 'grande', 'pequeno', 'pequena'}
_PROMPT = re.compile(r'^\s*\d+hp\s+\d+mn\s+\d+mv')
_MARCAS = re.compile(r'\s*(?:\.\.[^!\n]*!?|\(\+\d+[LE]\)|\(novo\)|\(muito gasto\)|\(gasto\)|\(invis[ií]vel\))\s*', re.I)
_QTD = re.compile(r'^\s*\(x(\d+)\)\s*')


def sem_acento(texto):
    return ''.join(c for c in unicodedata.normalize('NFD', texto or '') if unicodedata.category(c) != 'Mn').lower()


def normalizar(nome):
    """Chave estavel do item: sem acento, sem artigo, sem marcas do inventario. Pura."""
    t = _QTD.sub('', nome or '')
    t = _MARCAS.sub(' ', t)
    t = sem_acento(t).strip(" .,'\"")
    t = re.sub(r'\s+', ' ', t)
    for a in ARTIGOS:
        if t.startswith(a):
            t = t[len(a):]
            break
    return t.strip()


def limpar_linha(linha):
    """(nome_sem_marcas, quantidade, marcas_do_jogo) de uma linha do `inventory`. Pura."""
    m = _QTD.match(linha or '')
    qtd = int(m.group(1)) if m else 1
    marcas = re.findall(r'\(\+\d+[LE]\)|\(novo\)|\(muito gasto\)|\(gasto\)|\(invis[ií]vel\)|\.\.[^!\n]*!?', linha or '', re.I)
    nome = _MARCAS.sub(' ', _QTD.sub('', linha or '')).strip()
    return nome, qtd, [x.strip() for x in marcas]


def itens_do_inventario(texto):
    """[(nome, quantidade, marcas)] das linhas depois de 'Voce esta carregando:'. Pura."""
    out, dentro = [], False
    for linha in (texto or '').splitlines():
        if 'carregando' in sem_acento(linha) and linha.strip().endswith(':'):
            dentro = True
            continue
        if not dentro:
            continue
        if not linha.strip() or _PROMPT.match(linha) or linha.lstrip().startswith(('[', '>>>')):
            if out:
                break
            continue
        if sem_acento(linha).strip() in ('nada.', 'nada'):
            break
        out.append(limpar_linha(linha))
    return out


def itens_do_equipamento(texto):
    """[(slot, nome, marcas)] das linhas 'slot -> item' do `equipment`. Pura."""
    out = []
    for linha in (texto or '').splitlines():
        m = re.match(r'^\s*(.+?)\s*->\s*(.+?)\s*$', linha)
        if not m or _PROMPT.match(linha):
            continue
        nome, _q, marcas = limpar_linha(m.group(2))
        out.append((m.group(1).strip(), nome, marcas))
    return out


def palavras_chave(nome):
    """Palavras para tentar no `identify`, da mais especifica a menos. Pura."""
    toks = [t for t in re.findall(r"[a-z0-9]+", normalizar(nome)) if t not in STOP and len(t) >= 3]
    return toks


_RX_OBJ = re.compile(r"Objeto:\s*'([^']+)'[,\s]*Tipo:\s*([^\r\n]+)")
_RX_FLAGS = re.compile(r'O item [eé]:\s*([^\r\n]*)')
_RX_PESO = re.compile(r'Peso:\s*(-?\d+),\s*Valor:\s*(-?[\d\.]+)(?:,\s*Aluguel:\s*(-?[\d\.]+))?'
                      r'(?:,\s*N[ií]vel:\s*(-?\d+))?(?:,\s*Encarna[cç][aã]o:\s*(-?\d+))?')
_RX_VESTIR = re.compile(r'Pode ser vestido em:\s*([^\r\n]*)')


def _num(v):
    return int(v.replace('.', '')) if v else None


def parse_identify(texto):
    """Dicionario da resposta do `identify`; `identificado` False se nao houver 'Objeto:'. Pura."""
    t = texto or ''
    d = {'identificado': False, 'nome': None, 'tipo': None, 'flags': [], 'peso': None, 'valor': None,
         'aluguel': None, 'nivel': None, 'encarnacao': None, 'vestir_em': [], 'efeitos': [], 'linhas': []}
    m = _RX_OBJ.search(t)
    if not m:
        return d
    d.update(identificado=True, nome=m.group(1).strip(), tipo=m.group(2).strip())
    f = _RX_FLAGS.search(t)
    if f:
        d['flags'] = f.group(1).split()
    p = _RX_PESO.search(t)
    if p:
        d.update(peso=int(p.group(1)), valor=_num(p.group(2)), aluguel=_num(p.group(3)),
                 nivel=int(p.group(4)) if p.group(4) else None, encarnacao=int(p.group(5)) if p.group(5) else None)
    v = _RX_VESTIR.search(t)
    if v:
        d['vestir_em'] = v.group(1).split()
    for linha in t.splitlines():
        s = linha.strip()
        if not s or _PROMPT.match(s) or s.startswith(('Objeto:', 'O item', 'Peso:', 'Pode ser vestido', '>>>')):
            continue
        d['linhas'].append(s)
        if re.match(r'^(Modifica|Afeta|Melhora|A CA aplicada)', s, re.I):
            d['efeitos'].append(s)
    return d


def amaldicoado(d):
    """True se as flags indicam item preso ao corpo (amaldicoado ou NODROP). Pura."""
    f = ' '.join(d.get('flags') or []).upper()
    return 'AMALDI' in f or 'NODROP' in f or 'NÃO-LARGAR' in f or 'NAO-LARGAR' in f


def identificar(nome, run):
    """Tenta `identify <palavra>` ate a resposta devolver o MESMO nome; devolve (dict, comandos). `run` injetavel."""
    alvo = normalizar(nome)
    usados = []
    for kw in palavras_chave(nome):
        for prefixo in ('', '2.', '3.'):
            cmd = f'identify {prefixo}{kw}'
            d = None
            for _tentativa in range(2):     # o driver as vezes devolve a resposta do comando anterior (Dia 161)
                usados.append(cmd)
                d = parse_identify(run(cmd)[0])
                if d['identificado']:
                    break
            if d['identificado'] and normalizar(d['nome']) == alvo:
                return d, usados
            if not d['identificado']:
                break               # a palavra nao existe: proxima
    return None, usados


COMANDO_DO_SLOT = {'empunhando': 'wield', 'segurando': 'hold'}      # o resto e' `wear`


def tirou(texto):
    """True se a resposta do `remove` diz que a peca saiu. Pura."""
    return 'para de usar' in sem_acento(texto)


def identificar_vestido(slot, nome, run):
    """Item VESTIDO: o `identify` (comando e magia) so' enxerga o inventario, entao tira, identifica e veste de novo.

    Devolve (dict|None, estado) com estado 'ok', 'preso' (nao saiu: maldito ou NODROP) ou 'nao_identificado'.
    Se identificou mas nao conseguiu vestir de volta, o estado e' 'ok' e o chamador ve a peca no inventario.
    """
    usada = None
    verbo = COMANDO_DO_SLOT.get(sem_acento(slot).split()[0], 'wear')
    alvo = normalizar(nome)
    for kw in sorted(palavras_chave(nome), key=lambda k: -len(k)):     # a mais longa e' a mais especifica ("cardeal", "dourado")
        for _tentativa in range(2):
            texto = run(f'remove {kw}')[0]
            if tirou(texto):
                if alvo in sem_acento(texto):
                    usada = kw
                else:                       # saiu OUTRO item com a mesma palavra (dois aneis): veste de volta e tenta a proxima
                    run(f'{verbo} {kw}')
                break
        if usada:
            break
    if not usada:
        return None, 'preso'
    d, _cmds = identificar(nome, run)
    run(f'{verbo} {usada}')
    return d, ('ok' if d else 'nao_identificado')


def faltando(esperados, catalogo):
    """Nomes de `esperados` que nao estao no catalogo (por chave normalizada). Pura."""
    ja = {normalizar(i.get('nome')) for i in (catalogo or {}).get('itens', [])}
    vistos, falta = set(), []
    for n in esperados:
        k = normalizar(n)
        if k and k not in ja and k not in vistos:
            vistos.add(k)
            falta.append(n)
    return falta


def caminho_catalogo(heroi):
    return ROOT / 'data' / 'heroes' / heroi / 'itens.json'


def carregar_catalogo(heroi):
    p = caminho_catalogo(heroi)
    if p.is_file():
        return json.loads(p.read_text(encoding='utf-8'))
    return {'schema_version': 1, 'hero_id': heroi, 'itens': []}


def gravar_item(catalogo, d, onde, quando, agente):
    """Insere/atualiza `d` (de parse_identify) pela chave normalizada. Pura (altera `catalogo`)."""
    chave = normalizar(d['nome'])
    reg = {'nome': d['nome'], 'chave': chave, 'tipo': d['tipo'], 'flags': d['flags'], 'peso': d['peso'],
           'valor': d['valor'], 'aluguel': d['aluguel'], 'nivel': d['nivel'], 'encarnacao': d['encarnacao'],
           'vestir_em': d['vestir_em'], 'efeitos': d['efeitos'], 'linhas': d['linhas'],
           'amaldicoado': amaldicoado(d), 'onde': onde, 'identificado_em': quando, 'agente': agente}
    for i, antigo in enumerate(catalogo['itens']):
        if antigo.get('chave') == chave:
            catalogo['itens'][i] = reg
            return reg
    catalogo['itens'].append(reg)
    return reg


def main(argv=None):
    ap = argparse.ArgumentParser(description='Identifica todos os itens (inventario e vestidos) e grava o catalogo.')
    ap.add_argument('--hero', default='grebolius')
    ap.add_argument('--agente', default='Claude Sonnet 5.5 (claude-sonnet-5-5)')
    ap.add_argument('--quando', default=None, help='data AAAA-MM-DD (padrao: hoje)')
    ap.add_argument('--sem-gravar', action='store_true')
    args = ap.parse_args(argv)
    import time
    from base import run
    quando = args.quando or time.strftime('%Y-%m-%d')

    inventario, vestidos = [], []
    for _tentativa in range(3):             # leitura vazia = resposta atrasada, nao "nada vestido"
        inventario = itens_do_inventario(run('inventory')[0])
        vestidos = itens_do_equipamento(run('equipment')[0])
        if inventario and vestidos:
            break
    if not inventario and not vestidos:
        print('[IDENTIFICAR] nao consegui ler inventory nem equipment (driver atrasado?): nada identificado', flush=True)
        return 1
    alvos = [(n, 'inventario', None) for n, _q, _m in inventario] + [(n, f'vestido: {s}', s) for s, n, _m in vestidos]
    print(f'[IDENTIFICAR] {len(inventario)} no inventario, {len(vestidos)} vestidos', flush=True)

    cat = carregar_catalogo(args.hero)
    nao, presos, feitos = [], [], 0
    vistos = set()
    for nome, onde, slot in alvos:
        k = normalizar(nome)
        if k in vistos:
            continue
        vistos.add(k)
        if slot is None:
            d, cmds = identificar(nome, run)
            estado = 'ok' if d else 'nao_identificado'
        else:
            d, estado = identificar_vestido(slot, nome, run)
            cmds = []
        if estado == 'preso':
            presos.append(nome)
            print(f'[IDENTIFICAR] PRESO AO CORPO (nao saiu): {nome}', flush=True)
            continue
        if d is None:
            nao.append(nome)
            print(f'[IDENTIFICAR] NAO IDENTIFICADO: {nome} (tentativas: {len(cmds)})', flush=True)
            continue
        gravar_item(cat, d, onde, quando, args.agente)
        feitos += 1
        if amaldicoado(d):
            presos.append(nome)
        print(f"[IDENTIFICAR] {d['nome']} | {d['tipo']} | {' '.join(d['flags'])} | nivel {d['nivel']} | "
              f"{'; '.join(d['efeitos'])[:90]}", flush=True)
    if not args.sem_gravar:
        p = caminho_catalogo(args.hero)
        p.write_text(json.dumps(cat, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
        print(f'[IDENTIFICAR] catalogo gravado: {p} ({len(cat["itens"])} itens)', flush=True)
    print(f'[IDENTIFICAR] feitos={feitos} sem_identificar={len(nao)} presos_ao_corpo={presos}', flush=True)
    return 1 if nao else 0


if __name__ == '__main__':
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    sys.exit(main())
