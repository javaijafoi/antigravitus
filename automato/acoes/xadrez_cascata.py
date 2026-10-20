# -*- coding: utf-8 -*-
"""xadrez_cascata.py - a cascata da autoquest Xeque-mate no Grande Tabuleiro, com rastreio de posicao.

Por que existe (Dia 157): os lacos em PowerShell do scratchpad perderam a posicao por respostas de `look`
atrasadas e mataram a personagem duas vezes (morte #10: Rainha + cavaleiro; morte #12: parada em E1, a
casa do REI BRANCO, que mata quem esta na Xeque-mate: "Herege! Voce deu xeque-mate no rei errado!").

Regras desta rotina:
  * cada passo e' verificado com o texto DA PROPRIA resposta do movimento (nunca com um look separado):
    cor da casa, frase da peca da casa ("casa do Bispo do Rei Branco") e numero de saidas;
  * a rota nunca passa por E8, E1, B1, G1 (casas proibidas) a menos que seja o destino explicito;
  * recall a qualquer divergencia; nunca anda "de volta" com a posicao incerta;
  * fala de NPC nao e' automatizada (AGENTS #14): o Bispo Branco e' aceito a mao; aqui so' se le o log.

Uso (o driver tem de estar no ar, a Xeque-mate ja' aceita com o Bispo Branco):
    python automato/acoes/xadrez_cascata.py --etapa peoes|bispos|cavalos|torres|rainha
    python automato/acoes/xadrez_cascata.py --etapa rei --rei     # kite no Rei Negro (exige --rei)
    python automato/acoes/xadrez_cascata.py --etapa f1            # leva a F1 e espera a ordem do Bispo
"""
import argparse
import re
import sys
import time
import unicodedata
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(RAIZ / 'automato' / 'nucleo'))
sys.path.insert(0, str(RAIZ / 'automato' / 'camadas'))

COLUNAS = 'ABCDEFGH'
DIRS = {'n': (0, 1), 's': (0, -1), 'e': (1, 0), 'w': (-1, 0)}
PROIBIDAS = {'E8', 'E1', 'B1', 'G1'}      # Rei Negro, Rei Branco, cavaleiros brancos
RECUSAS = ('nao pode ir', 'muito relaxado', 'muito ocupado', 'voce esta dormindo', 'nao pode fazer isso dormindo')

# frase que a casa mostra depois de "casa " (normalizada, sem acento); None = casa sem peca (fileiras 3 a 6)
HOME = {
    'A1': 'da torre da rainha branca', 'B1': 'do cavalo da rainha branca', 'C1': 'do bispo da rainha branca',
    'D1': 'da rainha branca', 'E1': 'do rei branco', 'F1': 'do bispo do rei branco',
    'G1': 'do cavalo do rei branco', 'H1': 'da torre do rei branco',
    'A8': 'da torre da rainha negra', 'B8': 'do cavalo da rainha negra', 'C8': 'do bispo da rainha negra',
    'D8': 'da rainha negra', 'E8': 'do rei negro', 'F8': 'do bispo do rei negro',
    'G8': 'do cavalo do rei negro', 'H8': 'da torre do rei negro',
}


class Perdida(Exception):
    """A posicao ficou incerta; o chamador faz recall."""


def normalizar(texto):
    t = unicodedata.normalize('NFKD', texto or '')
    return ''.join(c for c in t if not unicodedata.combining(c)).lower()


def nome_casa(col, fil):
    return '%s%d' % (COLUNAS[col], fil)


def parse_casa(nome):
    return COLUNAS.index(nome[0].upper()), int(nome[1])


def cor_casa(col, fil):
    """Soma (coluna + fileira), A=1: par = Preta, impar = Branca (H1 = 9 e' Branca)."""
    return 'Branca' if ((col + 1) + fil) % 2 == 1 else 'Preta'


def saidas_esperadas(col, fil):
    n = 0
    n += 1 if fil < 8 else 0
    n += 1 if fil > 1 else 0
    n += 1 if col < 7 else 0
    n += 1 if col > 0 else 0
    if nome_casa(col, fil) in ('H5', 'D8', 'D1'):
        n += 1  # H5: o portao a leste; D8 e D1 (rainhas): a escada oculta `!baixo` para a tesouraria
    return n


def frase_da_casa(texto):
    """'do Bispo do Rei Branco' (normalizada) a partir de '... normalmente e a casa do Bispo do Rei Branco.'"""
    t = ' '.join(normalizar(texto).split())
    m = re.search(r'normalmente e a casa (.+?)\.', t)
    return m.group(1).strip() if m else None


def titulo_sala(texto):
    for linha in (texto or '').splitlines():
        limpa = re.sub(r'^\s*\d+hp\s+\d+mn\s+\d+mv\s*>\s*', '', linha).strip()
        if limpa and not limpa.startswith('DICA') and not limpa.startswith('>>>') and not limpa.startswith('['):
            return limpa
    return ''


def contar_saidas(texto):
    m = re.search(r'Sa.{1,2}das:\s*([^\]]*)\]', texto or '')
    if not m:
        return None
    return len([p for p in re.split(r',| e ', m.group(1)) if p.strip()])


def verificar_casa(texto, col, fil):
    """Levanta Perdida se o texto de chegada nao e' o da casa (col, fil). Pura: testavel sem jogo."""
    t = titulo_sala(texto)
    if normalizar(t) != normalizar('Uma Casa %s' % cor_casa(col, fil)):
        raise Perdida('titulo "%s" nao e a cor de %s' % (t, nome_casa(col, fil)))
    nome = nome_casa(col, fil)
    frase = frase_da_casa(texto)
    if nome in HOME and frase != HOME[nome]:
        raise Perdida('%s deveria mostrar "%s", mostrou "%s"' % (nome, HOME[nome], frase))
    if nome not in HOME and fil in (2, 7):
        if not frase or 'peao' not in frase and 'peoes' not in frase:
            raise Perdida('%s deveria ser casa de peao, mostrou "%s"' % (nome, frase))
        lado = 'rainha' if col < 4 else 'rei'
        if lado not in frase:
            raise Perdida('%s: peao do lado errado ("%s")' % (nome, frase))
    if nome not in HOME and fil in (3, 4, 5, 6) and frase:
        raise Perdida('%s nao deveria ter peca, mostrou "%s"' % (nome, frase))
    n = contar_saidas(texto)
    if n is not None and n != saidas_esperadas(col, fil):
        raise Perdida('%s: %d saidas, esperava %d' % (nome, n, saidas_esperadas(col, fil)))


def caminho_grade(origem, destino, proibidas=PROIBIDAS):
    """Menor caminho (BFS) entre duas casas, sem pisar nas proibidas (exceto o destino). Lista de direcoes."""
    o, d = parse_casa(origem), parse_casa(destino)
    fila, visto = [(o, [])], {o}
    while fila:
        (c, f), rota = fila.pop(0)
        if (c, f) == d:
            return rota
        for letra, (dc, df) in DIRS.items():
            nc, nf = c + dc, f + df
            if not (0 <= nc < 8 and 1 <= nf <= 8) or (nc, nf) in visto:
                continue
            if nome_casa(nc, nf) in proibidas and (nc, nf) != d:
                continue
            visto.add((nc, nf))
            fila.append(((nc, nf), rota + [letra]))
    return None


class Tabuleiro:
    """Dead-reckoning com verificacao a cada passo."""

    def __init__(self, casa, run):
        self.col, self.fil = parse_casa(casa)
        self.run = run

    @property
    def casa(self):
        return nome_casa(self.col, self.fil)

    def passo(self, d):
        dc, df = DIRS[d]
        nc, nf = self.col + dc, self.fil + df
        if not (0 <= nc < 8 and 1 <= nf <= 8):
            raise Perdida('passo %s sai do tabuleiro a partir de %s' % (d, self.casa))
        texto, vitals, combate = self.run(d)
        baixo = normalizar(texto)
        if any(r in baixo for r in RECUSAS):
            raise Perdida('passo %s recusado: %r' % (d, titulo_sala(texto)[:60]))
        verificar_casa(texto, nc, nf)
        self.col, self.fil = nc, nf
        return texto, vitals, combate

    def ir(self, destino, proibidas=PROIBIDAS):
        rota = caminho_grade(self.casa, destino, proibidas)
        if rota is None:
            raise Perdida('sem caminho de %s a %s' % (self.casa, destino))
        ultimo = ('', {}, False)
        for d in rota:
            ultimo = self.passo(d)
            time.sleep(0.4)
        return ultimo


# ---------------------------------------------------------------- jogo (precisa do driver)

def _jogo():
    import config  # noqa: F401
    from base import run
    import navegar as nav
    return run, nav


def log_atual():
    import config
    logs = sorted(Path(config.DIR_LOGS).glob('session_live_*.log'), key=lambda p: p.stat().st_mtime)
    return logs[-1] if logs else None


def contar_no_log(padrao):
    p = log_atual()
    if not p:
        return 0
    return len(re.findall(padrao, p.read_text(encoding='utf-8', errors='replace')))


def mortes(tipo):
    return contar_no_log(r'%s Negr[oa] est.{1,2} mort[oa]!' % tipo)


def vida(vitals):
    return (vitals or {}).get('hp') or 0


def mana(vitals):
    return (vitals or {}).get('mana') or (vitals or {}).get('mn') or 0


# ---------------------------------------------------------------- etapas

# casa, palavra-chave do alvo, tipo no log, magias antes dos raios, quantas pecas podem empilhar
ETAPAS = {
    'bispos':  [('F8', 'bispo', 'Bispo', ['blindness', 'curse'], False), ('C8', 'bispo', 'Bispo', ['blindness', 'curse'], False)],
    'cavalos': [('G8', 'cavaleiro', 'Cavaleiro', ['blindness', 'curse'], False), ('B8', 'cavaleiro', 'Cavaleiro', ['blindness', 'curse'], False)],
    'torres':  [('A8', 'torre', 'Torre', [], True), ('H8', 'torre', 'Torre', [], True)],
    'rainha':  [('D8', 'rainha', 'Rainha', ['curse', 'blindness'], True)],
}
PRESENCA = {
    'bispo': r'(o|a) bispo negro est.{1,2} aqui',
    'cavaleiro': r'magn.fico cavaleiro negro|(o|a) cavaleiro negro est.{1,2} aqui',
    'torre': r'castelo negro',
    'rainha': r'a rainha negra est.{1,2} (aqui|dormindo)',
}
LIMITE_VIDA = 150
HP_MIN_ENTRAR = 215


class Ctx:
    def __init__(self):
        self.run, self.nav = _jogo()
        self.salas = self.nav.carregar_mapa()

    def cmd(self, c, espera=1.0):
        r = self.run(c)
        time.sleep(espera)
        return r

    def sala(self):
        return self.run('look')[0]

    def no_templo(self):
        return 'templo de midgaard' in normalizar(titulo_sala(self.sala()))

    def comer_beber(self):
        for c in ('eat pao', 'drink cantil'):
            self.cmd(c, 1.5)

    def descansar(self, hp_min=HP_MIN_ENTRAR, mn_min=440, max_s=420):
        self.cmd('wake', 1)
        self.cmd('rest', 1)
        t0, vit = time.time(), {}
        while time.time() - t0 < max_s:
            time.sleep(20)
            texto, vit, combate = self.run('look')
            if combate or 'lutando contra voce' in normalizar(texto):
                raise Perdida('atacada enquanto descansava')
            if vida(vit) >= hp_min and mana(vit) >= mn_min:
                break
        self.cmd('stand', 2)
        return vit

    def ir_h5(self):
        self.nav.navegar(self.salas, 'templo_midgaard', 'xadrez_H5', self.run)

    def recall(self):
        self.cmd('recall', 3)


def esperar_presenca(ctx, tipo, max_s=720):
    """Fica na casa ate' a peca reaparecer. Devolve o texto da sala ou None."""
    padrao = re.compile(PRESENCA[normalizar(tipo)] if normalizar(tipo) in PRESENCA else PRESENCA['bispo'])
    ctx.cmd('rest', 1)
    t0 = time.time()
    while time.time() - t0 < max_s:
        texto, vit, combate = ctx.run('look')
        if combate or 'lutando contra voce' in normalizar(texto):
            ctx.cmd('stand', 1)
            return texto
        if padrao.search(normalizar(texto)):
            ctx.cmd('stand', 1)
            return texto
        time.sleep(20)
    ctx.cmd('stand', 1)
    return None


def atacar_peca(ctx, tab, casa, alvo, tipo, magias, dorme, meta, log=print):
    """Uma ida: chega na casa, dorme (se for o caso), debuffs, raios com limite de vida. Devolve o resultado."""
    tab.ir(casa)
    m0 = mortes(tipo)
    entrada = ctx.cmd('look', 0.5)[0]
    pat = PRESENCA[alvo]
    if not re.search(pat, normalizar(entrada)):
        log('  %s: sem %s agora; esperando o repop' % (casa, alvo))
        entrada = esperar_presenca(ctx, alvo)
        if entrada is None:
            return 'ausente'
    if dorme:
        ctx.cmd("cast 'sleep' %s" % ('1.' + alvo if alvo == 'torre' else alvo), 4)
        if alvo == 'torre' and len(re.findall('castelo negro', normalizar(entrada))) >= 2:
            ctx.cmd("cast 'sleep' 2.torre", 4)
    for m in magias:
        ctx.cmd("cast '%s' %s" % (m, alvo), 3)
    for i in range(1, 9):
        texto, vit, combate = ctx.cmd("cast 'lightning bolt' %s" % ('1.torre' if alvo == 'torre' else alvo), 3)
        h = vida(vit)
        log('  raio %d vida=%s mana=%s mortes=%d' % (i, h, mana(vit), mortes(tipo)))
        if mortes(tipo) > m0:
            return 'morto'
        if h and h <= LIMITE_VIDA:
            ctx.recall()
            return 'recall'
    return 'sem_morte'


def cumprir_etapa(nome, log=print):
    ctx = Ctx()
    alvos = ETAPAS[nome]
    tipo = alvos[0][2]
    meta = mortes(tipo) + len(alvos)
    log('etapa %s: mortes de %s agora=%d, meta=%d' % (nome, tipo, mortes(tipo), meta))
    for tentativa in range(1, 31):
        if mortes(tipo) >= meta:
            log('etapa %s cumprida' % nome)
            return 0
        if not ctx.no_templo():
            raise Perdida('as idas comecam no Templo; recall antes')
        ctx.comer_beber()
        ctx.descansar()
        ctx.ir_h5()
        ctx.cmd("cast 'invisibility'", 3)
        tab = Tabuleiro('H5', ctx.run)
        for casa, alvo, tp, magias, dorme in alvos:
            if mortes(tipo) >= meta:
                break
            try:
                res = atacar_peca(ctx, tab, casa, alvo, tp, magias, dorme, meta, log)
            except Perdida as e:
                log('POSICAO INCERTA: %s -> recall' % e)
                ctx.recall()
                return 3
            log('ida %d %s: %s' % (tentativa, casa, res))
            if res in ('recall', 'ausente'):
                break
        ctx.recall()
    return 1


def varrer_peoes(meta_mortes=9, log=print):
    """Etapa 1: varre as fileiras 7 a 2 matando peoes negros ate' somar `meta_mortes` mortes no log."""
    ctx = Ctx()
    base = contar_no_log(r'Pe.{1,2}o Negro do Tabuleiro est.{1,2} morto!')
    alvo = base + meta_mortes
    if not ctx.no_templo():
        raise Perdida('a varredura comeca no Templo; recall antes')
    ctx.comer_beber()
    ctx.descansar()
    ctx.ir_h5()
    ctx.cmd("cast 'invisibility'", 3)
    tab = Tabuleiro('H5', ctx.run)
    tab.ir('H7')
    sentido = -1
    for fil in (7, 6, 5, 4, 3, 2):
        cols = range(7, -1, -1) if sentido < 0 else range(0, 8)
        for col in cols:
            if nome_casa(col, fil) != tab.casa:
                tab.ir(nome_casa(col, fil))
            texto = ctx.cmd('look', 0.5)[0]
            if re.search(r'pe.{1,2}o negro aqui', normalizar(texto)) or 'peao negro aqui' in normalizar(texto):
                for _ in range(5):
                    t2, vit, _c = ctx.cmd("cast 'lightning bolt' peao negro", 2)
                    if 'em que voce' in normalizar(t2):
                        break
                time.sleep(2)
            feitas = contar_no_log(r'Pe.{1,2}o Negro do Tabuleiro est.{1,2} morto!') - base
            if feitas >= meta_mortes:
                log('peoes: %d mortes desde o inicio' % feitas)
                ctx.recall()
                return 0
            _t, vit, _c = ctx.cmd('look', 0.2)
            if (vida(vit) and vida(vit) < 120) or (mana(vit) and mana(vit) < 100):
                log('recursos baixos (vida=%s mana=%s); recall' % (vida(vit), mana(vit)))
                ctx.recall()
                return 1
        sentido = -sentido
    ctx.recall()
    return 1


def kite_rei(idas=1, log=print):
    """Etapa final, tatica do autor: chegar, sleep, curse, blind, 1 raio e recall (kite). Exige --rei."""
    ctx = Ctx()
    for n in range(1, idas + 1):
        if mortes('Rei') > 0:
            log('o Rei Negro ja morreu')
            return 0
        if not ctx.no_templo():
            raise Perdida('o kite comeca no Templo; recall antes')
        ctx.comer_beber()
        ctx.descansar(hp_min=222, mn_min=460)
        ctx.ir_h5()
        ctx.cmd("cast 'invisibility'", 3)
        tab = Tabuleiro('H5', ctx.run)
        try:
            tab.ir('E7')
            real = tab.run
            tab.run = lambda d: ctx.run(d + ";cast 'sleep' rei")   # entra e dorme no mesmo envio
            texto, vit, _c = tab.passo('n')
            tab.run = real
            log('E8: %s' % titulo_sala(texto))
            if 'dormindo' not in normalizar(texto) and 'vai dormir' not in normalizar(texto):
                log('o Rei nao dormiu; recall')
                ctx.recall()
                continue
            for magia in ('curse', 'blindness'):
                ctx.cmd("cast '%s' rei" % magia, 3)
            for i in (1, 2):
                _t, vit, _c = ctx.cmd("cast 'lightning bolt' rei", 3)
                h = vida(vit)
                log('  raio %d vida=%s mana=%s' % (i, h, mana(vit)))
                if mortes('Rei') > 0:
                    log('REI NEGRO MORTO; pegue o cetro a mao (get cetro corpo) e entregue ao Bispo')
                    return 0
                if h and h <= LIMITE_VIDA + 10:
                    break
        except Perdida as e:
            log('POSICAO INCERTA: %s -> recall' % e)
        ctx.recall()
        log('ida %d ao Rei concluida' % n)
    return 1


def main(argv=None):
    ap = argparse.ArgumentParser(description='Cascata da Xeque-mate no tabuleiro (rastreio de posicao).')
    ap.add_argument('--etapa', required=True, choices=sorted(ETAPAS) + ['f1', 'peoes', 'rei'])
    ap.add_argument('--rei', action='store_true', help='confirma o kite no Rei Negro (risco de morte)')
    ap.add_argument('--idas', type=int, default=1, help='idas do kite (so no Rei)')
    a = ap.parse_args(argv)
    try:
        if a.etapa == 'f1':
            ctx = Ctx()
            ctx.ir_h5()
            tab = Tabuleiro('H5', ctx.run)
            tab.ir('F1')
            print('em F1')
            return 0
        if a.etapa == 'peoes':
            return varrer_peoes()
        if a.etapa == 'rei':
            if not a.rei:
                print('o kite no Rei exige --rei (risco de morte; a morte cancela a missao)')
                return 2
            return kite_rei(a.idas)
        return cumprir_etapa(a.etapa)
    except Perdida as e:
        print('PARADO: %s' % e)
        return 3


if __name__ == '__main__':
    sys.exit(main())
