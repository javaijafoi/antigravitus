# -*- coding: utf-8 -*-
"""aproveitar_tempo.py - empilha tarefas curtas ate' um orcamento de minutos. ID: aproveitar_tempo

Doutrina do autor (2026-10-21): *"aproveitar 2 min -> faz X; aproveitar 4 min -> faz X, Y e Z"*.
Tempo ocioso (espera de repop de peca, fila, sono curto) tem de virar trabalho curto e util,
em vez de `sleep 720` parado.

Como funciona:
  * cada tarefa tem um custo **estimado** (so' para planejar) e e' executada **por inteiro**:
    nunca se corta uma acao no meio;
  * `selecionar()` empilha as que cabem no orcamento (pula a que nao cabe e continua);
  * `aproveitar()` mede o tempo real, roda as escolhidas em ordem e para quando o orcamento
    acaba; `GRACE_S` e' o teto de seguranca depois do pedido;
  * falha de uma tarefa nao aborta as seguintes.

CLI:
    python automato/acoes/aproveitar_tempo.py --minutos 2 --simular
    python automato/acoes/aproveitar_tempo.py --minutos 4 --tarefas cuidar,guardar_ouro
"""
import argparse
import sys
import time
from collections import namedtuple
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]
for _p in ('nucleo', 'camadas', 'rotinas', 'acoes'):
    sys.path.insert(0, str(RAIZ / 'automato' / _p))

GRACE_S = 30        # teto de seguranca acima do pedido: a tarefa em curso termina, outra nao comeca

Tarefa = namedtuple('Tarefa', 'nome custo_s prioridade pode executar')


# --------------------------------------------------------------------------- tarefas
def _prepara():
    import prepara
    return prepara


def _t_comer_beber(ctx=None):
    return bool(_prepara().comer_beber())


def _t_cuidar(ctx=None):
    import cuidar
    return bool(cuidar.cuidar())


def _t_guardar_ouro(ctx=None):
    return bool(_prepara().guardar_ouro())


def _t_falta_pao(ctx=None):
    try:
        return _prepara().precisa_repor().get('pao', False)
    except Exception:      # noqa: BLE001 - pre-condicao nunca derruba a pilha
        return True


def _t_falta_agua(ctx=None):
    try:
        return _prepara().precisa_repor().get('agua', False)
    except Exception:      # noqa: BLE001
        return True


def _t_repor_pao(ctx=None):
    return bool(_prepara().ir_padaria())


def _t_encher_cantil(ctx=None):
    return bool(_prepara().ir_fonte())


def _t_descansar(ctx=None):
    return bool(_prepara().dormir())


def _t_vender(ctx=None):
    import vender_espolio
    rel = vender_espolio.executar(max_itens=2, minimo=1000)
    return bool(rel.get('vendidos'))


def _t_varrer_peoes(ctx=None):
    import xadrez_cascata
    return bool(xadrez_cascata.varrer_peoes())


def catalogo():
    """Catalogo explicito (acrescentar tarefa e' decisao, como a lista de LOJAS do mercado)."""
    return [
        Tarefa('comer_beber', 10, 10, None, _t_comer_beber),
        Tarefa('cuidar', 20, 20, None, _t_cuidar),
        Tarefa('guardar_ouro', 30, 30, None, _t_guardar_ouro),
        Tarefa('vender_espolio', 60, 35, None, _t_vender),
        Tarefa('repor_pao', 40, 40, _t_falta_pao, _t_repor_pao),
        Tarefa('encher_cantil', 30, 50, _t_falta_agua, _t_encher_cantil),
        Tarefa('descansar', 45, 60, None, _t_descansar),
        Tarefa('varrer_peoes', 180, 90, None, _t_varrer_peoes),
    ]


def padrao():
    """Pilha padrao: tudo menos o que e' caro demais para uma espera (varrer_peoes)."""
    return [t for t in catalogo() if t.nome != 'varrer_peoes']


def por_nome(nomes):
    """Filtra o catalogo pela lista de nomes, na ordem dada (para --tarefas)."""
    idx = {t.nome: t for t in catalogo()}
    return [idx[n] for n in nomes if n in idx]


# --------------------------------------------------------------------------- planejamento
def selecionar(minutos, tarefas):
    """(escolhidas, planejado_s, restante_s): empilha por prioridade o que cabe. Pura."""
    orcamento = max(0, int(round(float(minutos) * 60)))
    restante = orcamento
    escolhidas = []
    for t in sorted(tarefas, key=lambda x: x.prioridade):
        if t.custo_s <= restante:
            escolhidas.append(t)
            restante -= t.custo_s
    return escolhidas, orcamento - restante, restante


def aproveitar(minutos, tarefas=None, ctx=None, log=print):
    """Executa as tarefas que couberem em `minutos` e devolve o relatorio."""
    lista = padrao() if tarefas is None else list(tarefas)
    escolhidas, planejado, _ = selecionar(minutos, lista)
    orcamento = max(0, int(round(float(minutos) * 60)))
    t0 = time.time()
    feitas, puladas = [], []
    for t in escolhidas:
        if time.time() - t0 >= orcamento:
            break
        if t.pode is not None:
            try:
                if not t.pode(ctx):
                    puladas.append({'nome': t.nome, 'motivo': 'pre-condicao falsa'})
                    continue
            except Exception as e:      # noqa: BLE001
                puladas.append({'nome': t.nome, 'motivo': 'pode() falhou: %s' % e})
                continue
        ini = time.time()
        try:
            ok = bool(t.executar(ctx))
            dur = time.time() - ini
            feitas.append({'nome': t.nome, 'dur_s': round(dur, 1), 'ok': ok})
            log('[APROVEITAR] %s: %.1fs ok=%s' % (t.nome, dur, ok))
        except Exception as e:          # noqa: BLE001 - uma tarefa nunca derruba a pilha
            feitas.append({'nome': t.nome, 'dur_s': round(time.time() - ini, 1),
                           'ok': False, 'erro': str(e)[:160]})
            log('[APROVEITAR] ATENCAO: %s falhou: %s' % (t.nome, e))
        if time.time() - t0 >= orcamento + GRACE_S:
            log('[APROVEITAR] teto de seguranca (%ds) atingido; parando' % (orcamento + GRACE_S))
            break
    usado = time.time() - t0
    relatorio = {
        'pedido_s': orcamento,
        'planejado_s': planejado,
        'usado_s': round(usado, 1),
        'feitas': feitas,
        'puladas': puladas,
        'restante_s': max(0, round(orcamento - usado)),
    }
    log('[APROVEITAR] pedido=%ds planejado=%ds usado=%.0fs feitas=%d'
        % (relatorio['pedido_s'], relatorio['planejado_s'], relatorio['usado_s'], len(feitas)))
    return relatorio


def main(argv=None):
    ap = argparse.ArgumentParser(description='Empilha tarefas curtas ate um orcamento de minutos.')
    ap.add_argument('--minutos', type=float, required=True)
    ap.add_argument('--tarefas', help='lista separada por virgula (default: pilha padrao)')
    ap.add_argument('--simular', action='store_true', help='so imprime a pilha, sem tocar no MUD')
    a = ap.parse_args(argv)
    lista = por_nome([n.strip() for n in a.tarefas.split(',') if n.strip()]) if a.tarefas else padrao()
    escolhidas, planejado, restante = selecionar(a.minutos, lista)
    if a.simular:
        print('orcamento %ds | planejado %ds | sobra %ds' % (int(a.minutos * 60), planejado, restante))
        for t in escolhidas:
            print('  %-16s %3ds  %s' % (t.nome, t.custo_s, (t.executar.__doc__ or '').strip()))
        if not escolhidas:
            print('  (nada coube no orcamento)')
        return 0
    rel = aproveitar(a.minutos, escolhidas)
    print(rel)
    return 0


if __name__ == '__main__':
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    sys.exit(main())
