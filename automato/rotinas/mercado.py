# -*- coding: utf-8 -*-
"""mercado.py - auditoria de comercio: anda ate' cada loja e lista o que ela vende.

O que esta rotina resolve, e que a doutrina exige:

1. **Rota pelo mapa, nao por contagem de passos.** O `mapa.json` ja' tem o grafo;
   a rota sai de um BFS sobre ele, a partir da sala onde ela REALMENTE esta' -
   nao da sala onde a gente acha que ela esta'. Aplicar rota de origem errada foi
   o que fez um `d` responder "Você não pode ir por aí..." com ela ja' na Praca.

2. **Conferir a chegada por marco de sala**, nunca pelo numero de passos. Se a
   sala nao for a esperada, `recall` e segue para a proxima.

3. **`visible` antes de `list`.** Descoberto no Dia 156: **invisibilidade bloqueia
   comercio**. O balconista responde *"Nao negocio com quem nao vejo!"* e o `list`
   nao devolve nada. A invisibilidade serve para mapear; para comprar, atrapalha.

O que ela grava, por loja: a tabela do `list` - Item, Preco, Nivel, Encantamento -
que e' a fonte autoritativa de "quem vende o que, por quanto".
"""
import json
import re
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'nucleo'))
import base           # noqa: E402
import config         # noqa: E402
from base import *    # noqa: F401,F403

FATOS = config.RUNTIME / 'mercado.jsonl'

DIRECOES = 'nsewud'
OPOSTO_D = {'n': 's', 's': 'n', 'e': 'w', 'w': 'e', 'u': 'd', 'd': 'u'}

# Salas de comercio e servico ja' conhecidas, por id do mapa. A lista e' explicita
# de proposito: quem entra aqui foi verificado, e acrescentar e' uma decisao.
LOJAS = [
    'padaria', 'loja_magias', 'loja_armaduras', 'loja_armas', 'armazem',
    'loja_animais', 'correio_midgaard', 'bar_javali', 'recepcao_javali',
    'bar_magos', 'taverna_encardida', 'bar_necromantes', 'laboratorio_magos',
    'bar_ladroes', 'guilda_guerreiros', 'guilda_magos', 'guilda_necromantes',
]

RE_LISTA = re.compile(
    r'^\s*(\d+)\)\s+(.+?)\s{2,}(.+?)\s{2,}(\d+)\s+(\d+)\s+(\d+)\s*$')
RE_TITULO = re.compile(r'^-?\d+\s*hp\s+-?\d+\s*mn\s+-?\d+\s*mv\s*>\s*')


def sem_acento(texto):
    import unicodedata
    t = unicodedata.normalize('NFKD', (texto or '').lower())
    return ''.join(c for c in t if not unicodedata.combining(c)).strip()


def titulo(texto):
    """Primeira linha que e' titulo de sala, ignorando prompt e ficha."""
    for linha in (texto or '').split('\n'):
        limpa = RE_TITULO.sub('', linha.strip()).strip()
        if not limpa or limpa.startswith('['):
            continue
        b = sem_acento(limpa)
        if any(b.startswith(p) for p in (
                'voce ', 'vida:', 'mana:', 'movimento:', 'digite', 'saidas:',
                'experiencia:', 'banco:', 'carregando:', 'nivel ')):
            continue
        if limpa.endswith(':'):
            continue
        return limpa
    return '?'


def sala_atual():
    """Titulo da sala onde ela esta' AGORA. E' a origem de toda rota."""
    for _ in range(3):
        t, _, _ = run('look')
        n = titulo(t)
        if n != '?':
            return n
        time.sleep(0.4)
    return '?'


def carregar_mapa():
    dados = json.loads(config.DOC_MAPA.read_text(encoding='utf-8'))
    por_id = {r['id']: r for r in dados['rooms']}
    viz = {}
    for r in dados['rooms']:
        arestas = [(d, a) for d, a in (r.get('exits') or {}).items()
                   if d in DIRECOES and a in por_id]
        viz[r['id']] = sorted(arestas)
    por_titulo = {}
    for rid, r in por_id.items():
        por_titulo.setdefault(sem_acento(r['name']), []).append(rid)
    # Salas que a rota deve EVITAR. A protecao agora vem daqui, nao da
    # invisibilidade (que alias bloqueia comercio).
    perigosas = {rid for rid, r in por_id.items()
                 if (r.get('risk_code') or '') in config.RISCO_A_EVITAR}
    return por_id, viz, por_titulo, perigosas


def rota(viz, origem, destino, evitar=()):
    """BFS no grafo do mapa, SEM passar pelas salas perigosas.

    Origem e destino sempre valem - se a loja ficasse numa sala de risco, evitar
    a si mesma seria impossivel. Se nao houver caminho limpo, devolve None e quem
    chamou decide se aceita o caminho sujo.
    """
    if origem == destino:
        return []
    bloqueadas = set(evitar) - {origem, destino}
    visto, fila = {origem}, [(origem, [])]
    while fila:
        atual, caminho = fila.pop(0)
        for d, alvo in viz.get(atual, []):
            if alvo in visto or alvo in bloqueadas:
                continue
            if alvo == destino:
                return caminho + [d]
            visto.add(alvo)
            fila.append((alvo, caminho + [d]))
    return None


# Identidades PROVADAS PELA CAMINHADA. Curadoria e levantamento batizaram o mesmo
# lugar de formas diferentes, e o mapa ficou com dois nos para uma sala so':
# aplicar a rota ate' `correio_midgaard` termina em "O Escritorio dos Correios".
# Isso e' prova empirica de que sao a mesma sala - mais forte que semelhanca de
# nome, que nesses casos e' baixa de proposito.
#
# Enquanto a mesclagem nao casar esses pares na origem, a rotina aceita o titulo
# alternativo como chegada. Acrescentar aqui SO' com a caminhada como prova.
ALIAS = {
    'correio_midgaard': 'o escritorio dos correios',
    'bar_javali': 'o bar da estalagem javali roncador',
}


def ir_para(por_id, viz, por_titulo, perigosas, destino_id):
    """Anda ate' a sala e CONFERE a chegada pelo titulo. True se chegou."""
    esperado = sem_acento(por_id[destino_id]['name'])
    alternativo = ALIAS.get(destino_id)
    aqui = sem_acento(sala_atual())
    if aqui == esperado or (alternativo and aqui == alternativo):
        return True
    origem = por_titulo.get(aqui, [None])[0]
    if origem is None:
        print('[MERCADO] nao sei onde estou (%r): recall' % aqui, flush=True)
        run('recall')
        return False
    caminho = rota(viz, origem, destino_id, perigosas)
    passou_perigo = False
    if caminho is None:
        # Sem caminho limpo. O autor autorizou o risco: "se der merda, acontece,
        # aprendemos". Vai pelo caminho direto e REGISTRA que passou por perigo.
        caminho = rota(viz, origem, destino_id)
        passou_perigo = True
        if caminho is not None:
            print('[MERCADO] %s: sem rota limpa, indo pela direta' % destino_id, flush=True)
    if caminho is None:
        print('[MERCADO] sem rota %s -> %s' % (origem, destino_id), flush=True)
        return False
    for d in caminho:
        run(d)
    aqui = sem_acento(sala_atual())
    chegou = aqui == esperado or (alternativo and aqui == alternativo)
    if not chegou:
        print('[MERCADO] %s: esperava %r, cheguei em %r'
              % (destino_id, esperado, aqui), flush=True)
        registrar({'tipo': 'rota_falhou', 'destino': destino_id, 'esperado': esperado,
                   'cheguei': aqui, 'passos': caminho})
        run('recall')
    elif passou_perigo:
        registrar({'tipo': 'rota_com_perigo', 'destino': destino_id,
                   'origem': origem, 'passos': caminho})
    return chegou


def listar():
    """`visible` e depois `list`. Devolve os itens da tabela."""
    invisible = 'nao negocio com quem nao vejo' in sem_acento(run('list')[0])
    if invisible:
        # Descoberto no Dia 156: invisibilidade bloqueia comercio.
        run('visible')
        time.sleep(0.3)
    t, _, _ = run('list')
    itens = []
    for linha in t.split('\n'):
        m = RE_LISTA.match(linha)
        if m:
            itens.append({'n': int(m.group(1)), 'disponivel': m.group(2).strip(),
                          'item': m.group(3).strip(), 'preco': int(m.group(4)),
                          'nivel': int(m.group(5)), 'enc': int(m.group(6))})
    return itens, invisible


def registrar(reg):
    FATOS.parent.mkdir(parents=True, exist_ok=True)
    with open(FATOS, 'a', encoding='utf-8') as f:
        f.write(json.dumps(reg, ensure_ascii=False) + '\n')


def executar() -> bool:
    run('wake')
    run('stand')
    # Sem invisibilidade: ela bloqueia comercio. Garante visibilidade antes de sair.
    if not config.USAR_INVISIBILIDADE:
        run('visible')
    por_id, viz, por_titulo, perigosas = carregar_mapa()
    print('[MERCADO] inicio: %d lojas | %d salas de risco a evitar | estou em %r'
          % (len(LOJAS), len(perigosas), sala_atual()), flush=True)

    resultado = {}
    for lid in LOJAS:
        if lid not in por_id:
            print('[MERCADO] %s nao existe no mapa: pulo' % lid, flush=True)
            continue
        nome = por_id[lid]['name']
        if not ir_para(por_id, viz, por_titulo, perigosas, lid):
            continue
        itens, era_invisivel = listar()
        registrar({'tipo': 'loja', 'id': lid, 'sala': nome, 'itens': itens,
                   'era_invisivel': era_invisivel, 'em': time.strftime('%Y-%m-%d %H:%M:%S')})
        resultado[lid] = len(itens)
        print('[MERCADO] %-20s %-30s %2d itens%s'
              % (lid, nome[:30], len(itens), ' (estava invisivel)' if era_invisivel else ''),
              flush=True)

    voltar_ao_templo()
    run('save')
    sem_itens = [k for k, v in resultado.items() if v == 0]
    print('[MERCADO] fim: %d lojas com itens | sem itens: %s'
          % (len([v for v in resultado.values() if v > 0]), sem_itens or 'nenhuma'), flush=True)
    return True


def main():
    return 0 if executar() else 1


if __name__ == '__main__':
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    sys.exit(main())
