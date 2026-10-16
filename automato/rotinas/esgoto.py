from base import *
import random

NOME = 'esgoto'
DESCRICAO = 'Reconhecer os esgotos sob o Laboratorio dos Magos com cuidado, sem entrar em luta desfavoravel.'
LOCAIS_VISTOS = []


def ir_ao_esgoto():
    run('recall'); run('stand')
    for m in ['s', 's', 'w', 'w', 's', 's', 'e']:
        andar(m)
    t, _, _ = run('look')
    if 'Laborat' not in t:
        return False
    andar('d')
    t, _, _ = run('look')
    return 'Esgoto' in t or 'Jun' in t


def executar():
    run('wake'); run('stand')
    if not ir_ao_esgoto():
        print('[esgoto] nao cheguei', flush=True)
        return False
    for i in range(12):
        if estourou(300):
            break
        t, _, _ = run('look')
        LOCAIS_VISTOS.append(next((l.strip() for l in t.split(chr(10)) if l.strip()), '?'))
        if hp_frac(t) < 0.70:
            print('[esgoto] vida baixa: recuando', flush=True)
            break
        run('exits')
        for d in random.sample(['n', 's', 'e', 'w'], 4):
            r, _, _ = run(d)
            if 'não pode ir' not in r:
                break
    print('[esgoto] salas vistas:', len(set(LOCAIS_VISTOS)), flush=True)
    voltar_ao_templo(); run('save')
    return True
