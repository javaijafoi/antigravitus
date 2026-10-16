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


# ---------------------------------------------------------------------------
# Diretiva do autor (Dia 156):
#   *"coloca no preparar passar no donations e ver se tem itens melhores que o
#     dela, dai ela troca (se não der, não troca)"*
#
# O criterio e' EMPIRICO, nao leitura de descricao: veste a peca, le os numeros
# do `score tudo` e compara com os de antes. Decide o que o SERVIDOR diz, nao o
# que o nome do item promete - numa sala de doacoes o normal e' a peca ser pior,
# e nesse caso ela volta e devolve a peca a sala.
# ---------------------------------------------------------------------------

# palavra no nome do item -> como se coloca no corpo
SLOTS = {
    'veste': 'wear', 'jaqueta': 'wear', 'armadura': 'wear', 'manto': 'wear',
    'capa': 'wear', 'tunica': 'wear', 'peitoral': 'wear', 'couro': 'wear',
    'elmo': 'wear', 'capacete': 'wear', 'coroa': 'wear', 'gorro': 'wear',
    'luvas': 'wear', 'manoplas': 'wear', 'bracadeiras': 'wear',
    'perneiras': 'wear', 'calca': 'wear', 'botas': 'wear', 'escudo': 'wear',
    'rosario': 'wear', 'colar': 'wear', 'anel': 'wear', 'cinto': 'wear',
    'espada': 'wield', 'adaga': 'wield', 'punhal': 'wield', 'clava': 'wield',
    'maca': 'wield', 'mangual': 'wield', 'picareta': 'wield', 'cajado': 'wield',
    'bastao': 'wield', 'lamina': 'wield', 'arco': 'wield',
}
# nao se veste: consumivel, ferramenta ou entulho
NAO_VESTIR = ('pocao', 'pergaminho', 'garrafa', 'barril', 'pao', 'broa', 'tocha',
              'lanterna', 'cantil', 'chave', 'grampo', 'atadura', 'mala', 'mochila',
              'corpo', 'cadaver', 'osso', 'pele', 'chifre', 'casco')


def numeros_do_score(tentativas=3):
    """(CA, Acerto, Dano) como o servidor reporta, ou None se nao conseguiu ler."""
    for _ in range(tentativas):
        t, _, _ = run('score tudo')
        a = sem_acento(t)
        ca = re.search(r'classe de armadura:\s*(\d+)', a)
        ac = re.search(r'acerto:\s*(-?\d+)', a)
        dn = re.search(r'dano:\s*(-?\d+)', a)
        if ca and ac and dn:
            return int(ca.group(1)), int(ac.group(1)), int(dn.group(1))
        time.sleep(0.6)
    return None


def itens_no_chao():
    """Nomes dos itens largados na sala, das linhas de presenca do `look`."""
    t, _, _ = run('look')
    achados = []
    for linha in (t or '').split('\n'):
        l = re.sub(r'^\(x\d+\)\s*', '', linha.strip())
        m = re.match(r'^(.{4,60}?)\s+(?:est[aá]|foi|foram|repousa|est[aã]o)\b', l, re.I)
        if not m:
            continue
        nome = re.sub(r'\s*\.{2}.*$', '', m.group(1)).strip()
        a = sem_acento(nome).strip()
        # 'voce' e 'nada' entram por causa das linhas de prosa da sala
        if nome and a not in IGNORAR and a not in ('voce', 'nada', 'algo', 'tudo'):
            achados.append(nome)
    return achados


def palavras_chave(nome):
    """Candidatos a palavra-chave, do mais especifico ao mais generico.

    O servidor casa por palavra do nome, e nao da' para saber qual de antemao:
    'uma enfeitada jaqueta de couro' responde a `get jaqueta`, nao a `get couro`.
    Entao tentamos em ordem - do ultimo substantivo para tras - ate' o `get` pegar.
    """
    uteis = [p for p in sem_acento(nome).split() if len(p) > 2]
    return list(reversed(uteis)) or [sem_acento(nome)]


def pegar_do_chao(nome):
    """Tenta `get` por cada palavra-chave. Devolve a palavra que funcionou, ou None."""
    for chave in palavras_chave(nome):
        t, _, _ = run('get ' + chave)
        if 'voce pega' in sem_acento(t):
            return chave
    return None


def equipado():
    """{nome_do_item: primeira_palavra_chave} do que ela veste agora."""
    t, _, _ = run('equipment')
    achados = {}
    for linha in (t or '').split('\n'):
        if '->' not in linha:
            continue
        item = linha.split('->', 1)[1].strip()
        item = re.sub(r'\s*\.{2}.*$', '', item).replace('(novo)', '').strip()
        if item:
            achados[item] = palavras_chave(item)[0]
    return achados


def ir_doacoes():
    """Do Templo a' Sala de Doacoes (a leste) e confirma por marco de sala."""
    voltar_ao_templo()
    run('stand')
    run('e')
    t, _, _ = run('look')
    return 'doacoes' in sem_acento(t or '')


def revisar_doacoes():
    """Troca SO' o que for melhor. Devolve quantas trocas fez."""
    antes = numeros_do_score()
    if antes is None:
        print('[PREPARA] doacoes: sem leitura do score - nao arrisco troca', flush=True)
        return 0
    if not ir_doacoes():
        print('[PREPARA] doacoes: nao cheguei', flush=True)
        return 0

    vestido = equipado()
    trocas = 0
    for nome in itens_no_chao():
        n = sem_acento(nome)
        if any(x in n for x in NAO_VESTIR):
            continue
        como = next((v for k, v in SLOTS.items() if k in n), None)
        if como is None:
            continue

        chave = pegar_do_chao(nome)
        if chave is None:
            continue
        run('identify ' + chave, timeout=15.0)      # diretiva §10: identificar ANTES de vestir

        antigo = next((k for k in vestido if chave in palavras_chave(k)), None)
        if antigo is None:
            for item in list(vestido):
                run('remove ' + vestido[item])
        run('%s %s' % (como, chave))

        depois = numeros_do_score() or antes
        if sum(depois) > sum(antes):
            trocas += 1
            ganho = (antes, depois)
            antes = depois
            vestido[chave] = chave
            print('[PREPARA] doacoes: TROQUEI por %r  %s -> %s' % (nome, ganho[0], ganho[1]), flush=True)
        else:
            run('remove ' + chave)
            run('wear all')
            if como == 'wield':
                run('wield ' + chave)
            run('drop ' + chave)
            print('[PREPARA] doacoes: %r nao superou %s - devolvido' % (nome, antes), flush=True)

    run('wear all')
    voltar_ao_templo()
    print('[PREPARA] doacoes: %d troca(s)' % trocas, flush=True)
    return trocas


def main():
    ap = argparse.ArgumentParser(description='Viagem de recarga: padaria, fonte, banco e sono.')
    ap.add_argument('--forcar', action='store_true', help='reabastece mesmo com estoque')
    ap.add_argument('--dormir', action='store_true', help='inclui o sono')
    ap.add_argument('--sem-doacoes', action='store_true',
                    help='nao revisar a Sala de Doacoes (a diretiva roda por padrao)')
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
    # Diretiva do autor: revisar a Sala de Doacoes procurando peca melhor que a
    # dela. Roda por padrao, junto da viagem de recarga; `--sem-doacoes` desliga.
    if not args.sem_doacoes:
        revisar_doacoes()

    voltar_ao_templo()
    run('save')
    fim = precisa_repor()
    print('[PREPARA] fim: paes=%s agua=%s ouro=%s' % (fim['pao_atual'], fim['agua_atual'], fim['ouro']), flush=True)
    return 0


if __name__ == '__main__':
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    sys.exit(main())
