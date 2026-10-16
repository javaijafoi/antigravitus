# -*- coding: utf-8 -*-
"""prepara.py - a viagem de recarga. So' isso.

    vigia.py    OBSERVA   - le o log e o driver, nunca manda comando
    cuidar.py   CUIDA     - come, bebe, veste armadura e invisibilidade, em campo
    prepara.py  RECARREGA - vai a cidade comprar pao, encher cantil, guardar ouro
                            e dormir, QUANDO O ESTOQUE ACABA

Antes este arquivo fazia as duas ultimas coisas: com fome, caminhava ate a
padaria mesmo com seis paes na bolsa. Agora ele nao decide por fome - decide por
ESTOQUE. Se ainda ha' pao e agua, nao ha' viagem: quem resolve fome e sede em
campo e' o cuidar.py.

Uso:
    python automato/camadas/prepara.py             # so' viaja se faltar estoque
    python automato/camadas/prepara.py --forcar    # viagem completa de reabastecimento
    python automato/camadas/prepara.py --dormir    # inclui o sono

Codigos de saida: 0 reposto (ou nada a fazer) | 1 falhou
"""
import argparse
import re
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'nucleo'))
sys.path.insert(0, str(Path(__file__).resolve().parent))
import config          # noqa: E402
import inventario      # noqa: E402
from base import run, andar, voltar_ao_templo   # noqa: E402

LIMIAR_PAO = 2      # abaixo disto a viagem se justifica
ALVO_PAO = 4        # quanto trazer quando for
RESERVA = config.RESERVA_OURO
IGNORAR = ('saidas:', 'voce ', 'vida:', 'mana:', 'movimento:', 'banco:',
           'carregando:', 'experiencia:', 'alinhamento:')


def sem_acento(texto):
    import unicodedata
    t = unicodedata.normalize('NFKD', (texto or '').lower())
    return ''.join(c for c in t if not unicodedata.combining(c))


def situacao(tentativas=3):
    """Le o score. Insiste: logo apos um `recall` a resposta pode nao chegar, e
    um texto vazio faz o chamador concluir 'sem fome' e pular a refeicao."""
    t = ''
    for _ in range(tentativas):
        t, _, _ = run('score tudo')
        if 'situa' in sem_acento(t) or 'vida:' in sem_acento(t):
            break
        print('[PREPARA] score nao chegou; tentando de novo', flush=True)
        time.sleep(0.5)
    b = sem_acento(t)
    d = {'texto': t,
         'fome': 'morrendo de fome' in b or 'com fome' in b or 'ficando com fome' in b,
         'sede': 'morrendo de sede' in b or 'com sede' in b or 'ficando com sede' in b}
    m = re.search(r'peso total de (\d+) kg', t)
    d['peso'] = int(m.group(1)) if m else None
    m = re.search(r'm\u00e1ximo (\d+) itens e um peso total de (\d+) kg', t)
    d['peso_max'] = int(m.group(2)) if m else None
    m = re.search(r'Carregando:\s*\{[^}]*\}\s*([\d.]+)', t)
    d['ouro'] = int(m.group(1).replace('.', '')) if m else None
    m = re.search(r'Banco:\s*\{[^}]*\}\s*([\d.]+)', t)
    d['banco'] = int(m.group(1).replace('.', '')) if m else None
    m = re.search(r'Movimento:\s*(?:\{[^}]*\})?\s*(-?\d+)\s+de\s+(\d+)', t)
    d['mv_frac'] = (int(m.group(1)) / int(m.group(2))) if m and int(m.group(2)) else None
    return d


def conta_pao():
    """Unidades de comida na bolsa. None = nao consegui ler (NAO e' zero)."""
    return inventario.contar_comida()


def agua_no_cantil():
    return inventario.agua_no_cantil()


def precisa_repor():
    """O que falta. Viagem so' quando ha' falta CONFIRMADA - fome nao e' falta."""
    s = situacao()
    pao = conta_pao()
    agua = agua_no_cantil()
    return {
        # None = leitura falhou: nao sei NAO vira viagem.
        'pao': pao is not None and pao < LIMIAR_PAO, 'pao_atual': pao,
        'agua': agua is not None and agua <= 0.0, 'agua_atual': agua,
        'banco': (s['ouro'] or 0) > RESERVA + 100, 'ouro': s['ouro'],
        'sono': s['mv_frac'] is not None and s['mv_frac'] < 0.5, 'mv_frac': s['mv_frac'],
    }


def sacar_para_comprar(quanto=None):
    """Traz ouro do banco quando falta na mao. AVISA quando o banco nao cobre.

    O banco protege o ouro da morte, mas a padaria cobra da MAO. No Dia 156 ela
    ficou com fome, com 2 moedas no bolso e 369 no banco: o prepara foi ate' a
    padaria, nao conseguiu comprar e voltou com um pao so'. Depositar sem saber
    sacar e' meio caminho.

    O alvo vem de `config.SAQUE_PARA_COMPRAR`. Se o banco nao tiver o suficiente,
    isto NAO falha em silencio: imprime o aviso com os numeros, para o autor
    decidir. Falta de ouro e' decisao, nao erro de execucao.
    """
    alvo = config.SAQUE_PARA_COMPRAR if quanto is None else quanto
    s = situacao()
    na_mao = s['ouro'] or 0
    banco = s['banco'] or 0
    if na_mao >= alvo:
        return False
    if banco <= 0:
        print('[PREPARA] ATENCAO: sem ouro nenhum (mao %d, banco %d). Nao da para comprar '
              'pao nem encher o cantil. Decidir o que fazer.' % (na_mao, banco), flush=True)
        return False
    falta = alvo - na_mao
    tirar = min(falta, banco)
    run('withdraw %d' % tirar)
    if tirar < falta:
        print('[PREPARA] ATENCAO: o banco NAO cobriu. Queria %d, saquei %d (banco tinha %d). '
              'Ficou com %d na mao - decidir o que fazer.'
              % (falta, tirar, banco, na_mao + tirar), flush=True)
    else:
        print('[PREPARA] saquei %d do banco (tinha %d na mao, alvo %d)'
              % (tirar, na_mao, alvo), flush=True)
    return True


def ir_padaria():
    """Templo -> s,s,w,n. Compra ate' ALVO_PAO."""
    for m in ['s', 's', 'w', 'n']:
        andar(m)
    t, _, _ = run('look')
    if 'padaria' not in sem_acento(t):
        print('[PREPARA] padaria nao encontrada', flush=True)
        return False
    for _ in range(ALVO_PAO + 2):
        if conta_pao() >= ALVO_PAO:
            break
        run('buy pao')
    print('[PREPARA] padaria: %d paes' % conta_pao(), flush=True)
    return True


def ir_fonte():
    """A Fonte de Marmore Azul, na Praca do Templo, e' gratuita."""
    run('recall')
    run('stand')
    andar('s')
    t, _, _ = run('look')
    if 'fonte' not in sem_acento(t):
        print('[PREPARA] fonte nao encontrada', flush=True)
        return False
    run('fill cantil fonte')
    print('[PREPARA] cantil cheio na fonte', flush=True)
    return True


def guardar_ouro():
    s = situacao()
    ouro = s['ouro'] or 0
    if ouro <= RESERVA + 100:
        return False
    deposito = ouro - RESERVA
    run('recall')
    run('stand')
    run('deposit %d' % deposito)
    print('[PREPARA] depositadas %d moedas (reserva de %d na mao)' % (deposito, RESERVA), flush=True)
    return True


def dormir():
    """O sono recupera movimento e mana. 75 s de relogio real."""
    voltar_ao_templo()
    run('sleep')
    time.sleep(75)
    run('wake')
    run('stand')
    s = situacao()
    print('[PREPARA] apos o sono: mv=%s fome=%s sede=%s' % (s['mv_frac'], s['fome'], s['sede']), flush=True)
    return True


def main():
    ap = argparse.ArgumentParser(description='Viagem de recarga: padaria, fonte, banco e sono.')
    ap.add_argument('--forcar', action='store_true', help='reabastece mesmo com estoque')
    ap.add_argument('--dormir', action='store_true', help='inclui o sono')
    args = ap.parse_args()

    run('wake')
    run('stand')
    print('[PREPARA] inicio (recarga)', flush=True)

    falta = precisa_repor()
    if not args.forcar and not any(falta[k] for k in ('pao', 'agua', 'banco')):
        print('[PREPARA] nada a recarregar (paes=%s agua=%s) - fome e sede sao do cuidar.py'
              % (falta['pao_atual'], falta['agua_atual']), flush=True)
        return 0

    feito = False
    if args.forcar or falta['pao']:
        voltar_ao_templo()
        sacar_para_comprar()
        feito = ir_padaria() or feito
    if args.forcar or falta['agua']:
        feito = ir_fonte() or feito
    if args.forcar or falta['banco']:
        feito = guardar_ouro() or feito
    if args.dormir or falta['sono']:
        feito = dormir() or feito

    voltar_ao_templo()
    run('save')
    fim = precisa_repor()
    print('[PREPARA] fim: paes=%s agua=%s ouro=%s' % (fim['pao_atual'], fim['agua_atual'], fim['ouro']), flush=True)
    return 0


if __name__ == '__main__':
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    sys.exit(main())
