from base import *

NOME = 'xadrez'
DESCRICAO = 'Coletar armaduras de peao no Tabuleiro de Xadrez e vender ao armeiro (renda segura).'


def ir_ao_tabuleiro():
    run('recall'); run('stand')
    for _ in range(9):
        ex, t = sala()
        if set(ex) >= {'n', 'e', 's', 'w'} and 'Campo' in t:
            break
        andar('n')
    for m in ['w', 'w', 'w']:
        andar(m)
    ex, t = sala()
    return 'Tabuleiro' in t or 'Casa' in t


def coletar():
    pegas = 0
    for m in ['w', 'n', 'n', 's', 's', 'w', 'n', 'n']:
        andar(m)
        t, _, _ = run('look')
        while 'armadura' in t.lower():
            r, _, _ = run('get armadura')
            if 'pega' in r.lower() or 'pegou' in r.lower():
                pegas += 1
            else:
                break
            t, _, _ = run('look')
    return pegas


def vender():
    run('recall'); run('stand')
    for m in ['s', 's', 'w', 's']:
        andar(m)
    t, _, _ = run('look')
    if 'Armaduras' not in t and 'armaduras' not in t:
        print('[xadrez] nao cheguei ao armeiro', flush=True)
        return False
    for _ in range(4):
        r, _, _ = run('sell armadura')
        if 'nao tenho' in r.lower() or 'não tenho' in r.lower() or 'caro demais' in r.lower():
            break
    return True


def executar():
    run('wake'); run('stand')
    if not ir_ao_tabuleiro():
        print('[xadrez] nao cheguei ao tabuleiro', flush=True)
        return False
    pegas = coletar()
    print('[xadrez] armaduras coletadas:', pegas, flush=True)
    vender()
    voltar_ao_templo(); run('save')
    return pegas > 0
