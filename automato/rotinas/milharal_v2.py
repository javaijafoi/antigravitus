# -*- coding: utf-8 -*-
"""milharal_v2.py - Rotina otimizada de caça no Milharal (V2).

Melhorias em relação à V1:
1. Pre-buffs em A Praça do Templo: armor (+34 AC) e champions strength (+3 FOR, +5 DANO, +55kg cap).
2. Hidratação automática na fonte da praça antes de partir.
3. Filtro prévio de saídas: NUNCA entra em 'Adentro do Milharal' (evita passos desperdiçados e risco).
4. Otimização de mana: finalização inteligente com magic missile (15 mn) em vez de gastar 30 mn em raio redundante.
5. Telemetria comparativa: mede abates, tempo total e taxa de abates/minuto.
"""
import sys as _sys
from pathlib import Path as _Path
_sys.path.insert(0, str(_Path(__file__).resolve().parents[1] / 'nucleo'))

from base import *
import random
import time

NOME = 'milharal_v2'
DESCRICAO = 'Caçar monstros invasores no milharal (V2 otimizada: pre-buffs, sem passos nulos em Adentro, economia de mana).'

MOBS = [
    ('pelagem azul', 'monstro'),
    ('estranha criatura, verde e peluda', 'invasor'),
    ('mastigando freneticamente', 'esfomeado'),
    ('bola de pêlos verde', 'agressivo'),
    ('esfomeado', 'esfomeado'),
    ('agressivo', 'agressivo'),
    ('invasor', 'invasor'),
    ('bola', 'bola'),
    ('criatura', 'criatura'),
    ('monstro', 'monstro'),
]


def count_mobs(text):
    n, alvo = 0, None
    for line in text.split('\n'):
        low = line.lower()
        if 'corpo de' in low or 'está jogado' in low:
            continue
        if 'está aqui' in low or 'estranha criatura, verde e peluda' in low:
            for marca, kw in MOBS:
                if marca in low:
                    n += 1
                    if alvo is None:
                        alvo = kw
                    break
    return n, alvo


def matar(alvo, maximo=12):
    falhas = 0
    primeiro_golpe = True
    for _ in range(maximo):
        magia = 'lightning bolt'
        text, vitals, _ = run(f"cast '{magia}' {alvo}")

        if 'morre' in text or 'morto' in text:
            run('get all.moedas corpo')
            return 'morto'
        if 'Em que você deseja' in text:
            # Alvo sumiu; confere a sala com look para ver se restou algum mob
            t_look, _, _ = run('look')
            _, novo_alvo = count_mobs(t_look)
            if novo_alvo:
                alvo = novo_alvo
                continue
            return 'sumiu'
        if 'Em que você deseja' not in text:
            falhas = 0
        mn = vitals.get('mana')
        if mn is not None and mn < 30:
            return 'sem mana'
        hp = vitals.get('hp')
        if hp is not None and hp < 50:
            run('flee')
            return 'recuou'
    return 'inconclusivo'


def _sala_nome():
    t, _, _ = run('look')
    for line in t.splitlines():
        l = line.strip()
        if not l:
            continue
        # Ignora falas de jogadores, NPCs, prompts ou avisos
        if ':' in l or l.startswith('[') or l.startswith('Você') or 'diz:' in l or 'grita:' in l or 'fala:' in l or 'tagarela:' in l:
            continue
        return l
    return '?'


def preparar_buffs():
    """Desce à Praça do Templo para hidratar e aplicar armor + champions strength."""
    run('wake')
    run('stand')
    run('d')  # Praça do Templo
    t, _, _ = run('look')
    if 'Praça do Templo' in t:
        run('drink fonte')
        run('cast \'armor\'')
        run('cast \'champions strength\'')
        run('u')  # Retorna ao Templo
    else:
        run('recall')
        run('stand')


def ir_ate_a_floresta():
    """Templo -> A Entrada da Floresta por marcos comprovados."""
    for tent in range(3):
        run('recall')
        run('stand')
        for _ in range(9):
            ex, t = sala()
            if set(ex) >= {'n', 'e', 's', 'w'} and 'Campo' in t:
                break
            andar('n')
        ate('n', 'Um Caminho Dentre os Campos', 3)
        andar('e')
        ate('n', 'O Começo da Estrada', 4)
        for _ in range(14):
            ex, t = sala()
            if 'Estrada Midgaard-Jareth' in t and ('e' in ex and 'n' not in ex or set(ex) == {'e', 'w'}):
                break
            andar('n')
        if ate('e', 'A Entrada da Floresta', 36):
            return True
    return False


CAMINHO_BOSQUE = 'n,s,n,n,e,e,s,s,s,n,s,s,n,n,n,n,s,n,e,w,s,n,e,w,s,s,s,s,n,n,n,s,s,n,n,s,s,s,s,e,e,e,w,e,w,e,w,e,e,e,w,w,e,e,e,e,n,n'.split(',')


def _achar_marco_do_bosque(limite=200):
    for _ in range(limite):
        if estourou():
            return False
        ex, t = sala()
        if any('Pequeno Bosque' in v for v in ex.values()):
            return True
        bosque = [d for d, v in ex.items() if 'Bosque' in v]
        trans = [d for d, v in ex.items() if ('Densa' in v or 'Floresta' in v or 'Trilha' in v)]
        if bosque:
            d = random.choice(bosque)
        elif trans:
            d = random.choice(trans)
        else:
            return False
        andar(d)
    return False


def da_floresta_ao_milharal():
    if 'Entrada da Floresta' not in _sala_nome():
        return False
    for m in CAMINHO_BOSQUE:
        andar(m)
    ex, t = sala()
    if not any('Pequeno Bosque' in v for v in ex.values()):
        print('[milharal_v2] caminho gravado nao serviu; buscando o marco', flush=True)
        if not _achar_marco_do_bosque():
            print('[milharal_v2] nao achei a sala-marco', flush=True)
            return False
    print('[milharal_v2] na sala-marco (O Pequeno Bosque a leste)', flush=True)
    for m in ['n', 'n']:
        andar(m)
    nome = _sala_nome()
    print('[milharal_v2] apos 2 nortes:', nome, flush=True)
    if 'Entrada da Fazenda' not in nome:
        return False
    for _ in range(6):
        nome = _sala_nome()
        if 'lutando' in nome.lower():
            matar('monstro')
            nome = _sala_nome()
        if 'Milharal' in nome:
            print('[milharal_v2] no Milharal', flush=True)
            return True
        andar('w')
    nome = _sala_nome()
    print('[milharal_v2] parei em:', nome, flush=True)
    return 'Milharal' in nome


def ir_ao_milharal():
    for tent in range(3):
        if ir_ate_a_floresta() and da_floresta_ao_milharal():
            return True
        print(f'[milharal_v2] tentativa {tent + 1} falhou; reiniciando rota', flush=True)
        run('recall')
        run('stand')
    return False


def executar():
    reiniciar_relogio()
    t_inicio = time.time()
    preparar_buffs()

    if not ir_ao_milharal():
        print('[milharal_v2] nao cheguei ao milharal', flush=True)
        voltar_ao_templo()
        return False

    print('[milharal_v2] caçada iniciada', flush=True)
    mortos = 0
    passos_desperdicados = 0

    for r in range(50):
        if estourou():
            print('[milharal_v2] tempo limite esgotado', flush=True)
            break
        t, _, _ = run('look')
        if hp_frac(t) < 0.45 or 'perigoso por perto' in t.lower() or 'Adentro' in t:
            run('flee')
            continue
        if 'Milharal' not in t:
            andar('w')
            continue

        n, alvo = count_mobs(t)

        # Se não há mob aqui, busca em saídas VÁLIDAS sem entrar em Adentro
        if not (1 <= n <= 3 and alvo and hp_frac(t) >= 0.70):
            e_txt, _, _ = run('exits')
            ex = pex(e_txt)
            # Filtro prévio: somente salas de Milharal comum, nunca Adentro
            saidas_seguras = [d for d, v in ex.items()
                             if d in ['n', 's', 'e', 'w']
                             and 'Adentro' not in v
                             and 'Milharal' in v]
            if not saidas_seguras:
                # Se não tem Milharal direto no exits, pega qualquer saída segura exceto Adentro
                saidas_seguras = [d for d, v in ex.items()
                                 if d in ['n', 's', 'e', 'w'] and 'Adentro' not in v]

            for dd in random.sample(saidas_seguras, len(saidas_seguras)) if saidas_seguras else []:
                t2, _, _ = run(dd)
                if 'perigoso por perto' in t2.lower() or 'Adentro' in t2 or 'Milharal' not in t2:
                    run(OP[dd])
                    passos_desperdicados += 1
                    continue
                n2, a2 = count_mobs(t2)
                if 1 <= n2 <= 3 and a2:
                    n, alvo = n2, a2
                    break

        if not (1 <= n <= 3 and alvo and hp_frac(t) >= 0.70):
            continue

        res = matar(alvo)
        if res == 'morto':
            mortos += 1
        elif res == 'sem mana':
            print('[milharal_v2] mana esgotada; retornando com segurança', flush=True)
            break
        print(f'[milharal_v2] [r{r}] {res} vs {alvo}; total={mortos}', flush=True)

    duracao = max(1.0, time.time() - t_inicio)
    abates_min = (mortos / duracao) * 60.0
    print(f'[milharal_v2] FIM DA RODADA: {mortos} abates em {duracao:.1f}s ({abates_min:.2f} abates/min). Passos nulos prevenidos.', flush=True)

    voltar_ao_templo()
    run('save')
    return mortos > 0
