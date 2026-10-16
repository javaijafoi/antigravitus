from base import *
import random

NOME = 'milharal'
DESCRICAO = 'Cacar monstros invasores no milharal da fazenda (Problemas Agricolas) e trazer espolio.'
MOBS = [('esfomeado', 'esfomeado'), ('agressivo', 'agressivo'), ('invasor', 'invasor'), ('bola', 'bola'), ('criatura', 'criatura'), ('monstro', 'monstro')]
CAMINHO = 's,n,e,e,w,w,e,w,s,n,e,w,e,w,s,n,e,e,w,e,e,w,w,w,e,e,w,e,w,e,w,w,e,e,w,e,e,e,e,w,w,e,e,w,w,w,e,e,w,e,w,w,e,e,w,e,e,e,e'.split(',')


def count_mobs(text):
    n, alvo = 0, None
    for line in text.split('\n'):
        low = line.lower()
        if 'está aqui' in low or 'está jogado' in low:
            for marca, kw in MOBS:
                if marca in low:
                    n += 1
                    if alvo is None:
                        alvo = kw
                    break
    return n, alvo


def matar(alvo, maximo=14):
    for _ in range(maximo):
        t, _, _ = run('look')
        if 'morre' in t or 'morto' in t:
            return 'morto'
        n, a = count_mobs(t)
        if n == 0:
            return 'sumiu'
        if a and a != alvo:
            alvo = a
        if mana_baixa():
            return 'sem mana'
        magia = 'burning hands' if mana_baixa() else 'lightning bolt'
        text, _, _ = run(f"cast '{magia}' {alvo}")
        if 'Em que você deseja' in text:
            trocou = False
            for _, kw in MOBS:
                if kw == alvo:
                    continue
                t2, _, _ = run(f"cast '{magia}' {kw}")
                if 'Em que você deseja' not in t2:
                    alvo, text, trocou = kw, t2, True
                    break
            if not trocou:
                return 'sem alvo valido'
        if 'morre' in text or 'morto' in text:
            return 'morto'
        if hp_frac(text) < 0.40:
            run('flee')
            return 'recuou'
    return 'inconclusivo'


def _entrar_fazenda(ex):
    for dd, v in ex.items():
        if 'Fazenda' in v:
            run(dd)
            for m in ['w', 'w', 'w']:
                tt, _, _ = run(m)
                if 'Milharal' in tt:
                    return True
            return 'Milharal' in run('look')[0]
    return False


def _bosque(modo_replay):
    ultimo = None
    passos = CAMINHO if modo_replay else [None] * 130
    for passo in passos:
        if estourou():
            print('[milharal] tempo esgotado no bosque', flush=True)
            return False
        e_txt, _, _ = run('exits')
        ex = pex(e_txt)
        if any('Fazenda' in v for v in ex.values()):
            return _entrar_fazenda(ex)
        if modo_replay:
            andar(passo)
            continue
        if passo is None or (isinstance(passo, int) and passo is None):
            pass
        bosq = [dd for dd, v in ex.items() if 'Bosque' in v]
        trans = [dd for dd, v in ex.items() if ('Densa' in v or 'Floresta' in v or 'Trilha' in v)]
        if bosq:
            d = random.choice(bosq)
        elif trans:
            d = random.choice(trans)
        elif ultimo:
            d = OP[ultimo]
        else:
            return False
        ultimo = d
        andar(d)
    return False


def _sala_nome():
    t, _, _ = run('look')
    return next((l.strip() for l in t.split(chr(10)) if l.strip()), '?')


def ir_ao_milharal():
    """Rota por CHECKPOINTS (a mesma que funcionou no viagem.py): cada etapa para
    quando a marca da sala aparece, em vez de contar passos."""
    for tent in range(3):
        run('recall'); run('stand')
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
            if 'Estrada Midgaard-Jareth' in t and set(ex) == {'e', 'w'}:
                break
            andar('n')
        print('[rota] aclive:', _sala_nome(), flush=True)
        if not ate('e', 'A Entrada da Floresta', 24):
            print('[rota] sem floresta nesta tentativa', flush=True)
            continue
        print('[rota] floresta ok:', _sala_nome(), flush=True)
        for m in ['n', 'n', 'e', 'e', 's']:
            andar(m)
        nome = _sala_nome()
        print('[rota] apos o bosque:', nome, flush=True)
        if 'Entrada da Fazenda' not in nome:
            continue
        for m in ['w', 'w', 'w']:
            andar(m)
        nome = _sala_nome()
        print('[rota] apos 3 oestes:', nome, flush=True)
        if 'Milharal' in nome:
            return True
    return False


def executar():
    run('wake'); run('stand')
    if not ir_ao_milharal():
        print('[milharal] nao cheguei ao milharal', flush=True)
        return False
    print('[milharal] no milharal', flush=True)
    mortos = 0
    for r in range(18):
        if estourou():
            print('[milharal] tempo esgotado na cacada', flush=True)
            break
        t, _, _ = run('look')
        if hp_frac(t) < 0.45 or 'perigoso por perto' in t.lower() or 'Adentro' in t:
            run('flee'); continue
        n, alvo = count_mobs(t)
        if not (1 <= n <= 3 and alvo and hp_frac(t) >= 0.70):
            for dd in random.sample(['n', 's', 'e', 'w'], 4):
                t2, _, _ = run(dd)
                if 'perigoso por perto' in t2.lower() or 'Adentro' in t2:
                    run(OP[dd]); continue
                n2, a2 = count_mobs(t2)
                if 1 <= n2 <= 3 and a2:
                    n, alvo = n2, a2
                    break
        if not (1 <= n <= 3 and alvo and hp_frac(t) >= 0.70):
            continue
        res = matar(alvo)
        if res == 'morto':
            mortos += 1
        print(f'[milharal] [r{r}] {res} vs {alvo}; total={mortos}', flush=True)
    print('[milharal] abates:', mortos, flush=True)
    voltar_ao_templo(); run('save')
    return mortos > 0
