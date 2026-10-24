# -*- coding: utf-8 -*-
"""tesouro_negro.py - pega o Tesouro Negro da Realeza (20.000 moedas) varias vezes. ID: tesouro_negro

O que se sabe (conhecimento.md §91 e §92): a Tesouraria Negra e' o quarto abaixo de D8 (a Rainha Negra). Abre
com a Chave do Tesouro Negro (cai do Rei Negro, invisivel; a chave NAO e' consumida pela porta). O tesouro
"reaparece" e a porta tranca de novo quando a zona do tabuleiro reinicia; o periodo nao esta medido, entao a
rotina o mede: registra cada tomada e usa a mediana dos intervalos para espaçar as proximas sondas.

Cada ida: Templo -> H5 -> D5 -> D7 -> D8 (sem passar por E8, a casa do Rei), `cast 'sleep' rainha` (dorme a
Rainha e ainda rende ~750 de EXP), `unlock`/`open baixo` se a porta estiver `!baixo`, `down`, `get moedas`,
`up`, `recall`. A porta fica aberta de proposito: ver `!baixo` de novo em D8 e' o sinal de que a zona reiniciou.

Entre as idas NAO fica parada: empilha tarefas curtas do `aproveitar_tempo` (sem `vender_espolio`, que podia
vender a tunica do inventario) e dorme o resto. Para por conta propria se faltar a chave, se a vida cair, se a
posicao ficar incerta 3 vezes seguidas ou se passar do teto de minutos.

Uso:
    python automato/acoes/tesouro_negro.py --tomadas 5            # as proximas 5 tomadas
    python automato/acoes/tesouro_negro.py --tomadas 5 --simular  # so' mostra o plano
"""
import argparse
import json
import re
import statistics
import sys
import time
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]
for _p in ('nucleo', 'camadas', 'rotinas', 'acoes'):
    sys.path.insert(0, str(RAIZ / 'automato' / _p))
import xadrez_cascata as xc  # noqa: E402

LOG = RAIZ / 'automato' / 'runtime' / 'tesouro_negro.jsonl'
REI_BRANCO_MORTO = RAIZ / 'automato' / 'runtime' / 'rei_branco_morto.json'   # trava: o Rei Branco morre UMA vez (DECISOES §17)
# Os dois tesouros sao espelhos: a porta `!baixo` fica na casa da Rainha (D8 negra, D1 branca); a chave cai do Rei do mesmo lado.
TESOUROS = {
    'negro': {'acesso': ('D7', 'n'), 'rainha': 'D8', 'rei': 'E8'},
    'branco': {'acesso': ('D2', 's'), 'rainha': 'D1', 'rei': 'E1'},
}
LADO = 'negro'
ESPERA_INICIAL_MIN = 6      # antes de conhecer o periodo de reset: 1a sonda 6 min depois da tomada
PASSO_MIN = 3               # depois disso, sonda a cada 3 min ate' o tesouro voltar
FOLGA_MIN = 1.5             # com o periodo medido, sonda 1,5 min antes dele
FALHAS_SEGUIDAS_MAX = 3
PESO_FOLGA_KG = 18          # o tesouro pesa ~14 kg: abaixo desta folga o `get moedas` e' recusado (Dia 163)
# `vender_espolio` fica de fora: venderia a tunica dourada do inventario (decisao do autor pendente).
TAREFAS_OCIOSAS = ('comer_beber', 'cuidar', 'guardar_ouro', 'repor_pao', 'encher_cantil', 'descansar')


def _norm(texto):
    return xc.normalizar(texto)


# --------------------------------------------------------------------------- partes puras
def saidas(texto):
    """['leste', 'sul', 'oeste', '!baixo'] da linha `[ Saidas: ... ]`. Pura."""
    m = re.search(r'\[\s*Sa[ií]das:\s*([^\]]*)\]', texto or '')
    if not m:
        return []
    return [s.strip() for s in re.split(r',|\s+e\s+', m.group(1)) if s.strip()]


def porta_baixo(texto):
    """'fechada' se a saida aparece como `!baixo`, 'aberta' se aparece `baixo`, None se nao ha. Pura."""
    s = saidas(texto)
    if '!baixo' in s:
        return 'fechada'
    if 'baixo' in s:
        return 'aberta'
    return None


def rainha_acordada(texto):
    """True se a sala diz 'A Rainha Negra esta aqui' (acordada); 'esta dormindo aqui' nao conta. Pura."""
    return 'rainha negra esta aqui' in _norm(texto)


def moedas_pegas(texto):
    """Quantas moedas o `get moedas` informou ('Havia 20.000 moedas.'), ou None. Pura."""
    m = re.search(r'Havia\s+([\d\.]+)\s+moedas', texto or '')
    return int(m.group(1).replace('.', '')) if m else None


def pegou(texto):
    """True se a resposta do `get moedas` e' a tomada do tesouro. Pura."""
    return 'voce pega o tesouro' in _norm(texto)


def peso_do_score(texto):
    """(peso, limite) em kg do `score tudo` ('num peso total de 91 kg ... no maximo ... 115 kg'), ou None. Pura."""
    p = re.search(r'peso total de\s+(\d+)\s*kg', texto or '')
    m = re.search(r'm[aá]ximo[^\n]*?peso total de\s+(\d+)\s*kg', texto or '')
    if not p:
        return None
    return int(p.group(1)), (int(m.group(1)) if m else 115)


def sem_folga(texto, folga=PESO_FOLGA_KG):
    """True se o peso deixa menos de `folga` kg livres: o Tesouro Negro da Realeza nao cabe. Pura."""
    pl = peso_do_score(texto)
    return bool(pl) and (pl[1] - pl[0]) < folga


def tem_chave(inventario):
    """True se o `inventory` lista a Chave do Tesouro Negro. Pura."""
    return 'chave do tesouro' in _norm(inventario)


def proxima_espera_min(tomadas):
    """Minutos ate a proxima sonda depois de uma tomada, pela mediana dos intervalos medidos. Pura.

    `tomadas`: instantes (segundos) das tomadas em ordem. Sem dois pontos, usa ESPERA_INICIAL_MIN.
    """
    if len(tomadas) < 2:
        return ESPERA_INICIAL_MIN
    intervalos = [(b - a) / 60.0 for a, b in zip(tomadas, tomadas[1:])]
    return max(PASSO_MIN, statistics.median(intervalos) - FOLGA_MIN)


# --------------------------------------------------------------------------- jogo
class _Fim(Exception):
    """Encerra a ida com o resultado ja' decidido."""


def uma_ida(ctx, log=print):
    """Uma ida ao Tesouro Negro. Devolve {resultado, ...}; nunca levanta (a rotina decide pelo resultado)."""
    r = {'t': time.time(), 'resultado': 'erro'}
    try:
        if not ctx.garantir_templo():
            raise xc.Perdida('nao consegui confirmar o Templo')
        socorrer(log)
        guardar_espolio(ctx, log)
        ctx.ir_h5()
        ctx.cmd("cast 'invisibility'", 2)
        tab = xc.Tabuleiro('H5', ctx.run)
        cfg = TESOUROS[LADO]
        tab.ir(cfg['acesso'][0])
        texto, _vit, _c = tab.passo(cfg['acesso'][1])       # casa da Rainha (D8 negra, D1 branca)
        r['porta'], r['rainha_acordada'] = porta_baixo(texto), rainha_acordada(texto)
        ctx.cmd("cast 'sleep' rainha", 1.5)                 # sempre: dorme a Rainha e rende ~750 de EXP
        if r['porta'] == 'fechada':
            r['unlock'] = ' '.join(ctx.cmd('unlock baixo', 1)[0].split())[:80]
            r['open'] = ' '.join(ctx.cmd('open baixo', 1)[0].split())[:80]
        desceu = ctx.cmd('down', 1.2)[0]
        if 'tesouro' not in _norm(desceu):
            r['resultado'] = 'nao_desceu'
            raise _Fim()
        resposta = ctx.cmd('get moedas', 1)[0]
        if pegou(resposta):
            r.update(resultado='pegou', moedas=moedas_pegas(resposta))
        elif 'muito peso' in _norm(resposta):
            r.update(resultado='peso', resposta=' '.join(resposta.split())[:80])
        else:
            r.update(resultado='sem_tesouro', resposta=' '.join(resposta.split())[:80])
        ctx.cmd('up', 1)
    except _Fim:
        pass
    except xc.Perdida as e:
        r['erro'] = str(e)[:120]
    except Exception as e:      # noqa: BLE001 - a rotina decide; um erro de leitura nao derruba o loop
        r['erro'] = '%s: %s' % (type(e).__name__, str(e)[:100])
    finally:
        try:
            ctx.recall()
        except Exception:       # noqa: BLE001
            pass
    return r


def chao_de_e8(ctx, log=print):
    """Vai a E8 (invisivel, so' olha o chao) e tenta `get chave`; sai por recall (andar com o Rei acordado custa uma rodada)."""
    try:
        if not ctx.garantir_templo():
            return False
        ctx.ir_h5()
        ctx.cmd("cast 'invisibility'", 2)
        tab = xc.Tabuleiro('H5', ctx.run)
        tab.ir('E7')
        tab.passo('n')                                        # E8
        # O Rei acordado atacou mesmo a personagem invisivel (morte #16: -90, -91, -59 = 240 > 232 de vida): dorme-o ANTES
        # de pegar qualquer coisa e, se ele nao dormir, sai sem pegar (o kite faz o mesmo: sleep, e so' entao age).
        dormiu = _norm(ctx.cmd("cast 'sleep' rei", 1.2)[0])
        if 'vai dormir' not in dormiu and 'dormindo' not in dormiu:
            log('[TESOURO] o Rei nao dormiu: saio de E8 sem pegar nada')
            return tem_chave(ctx.run('inventory')[0])
        resposta = ctx.cmd('get all.chave', 0.8)[0]     # todas: cada unlock gasta uma
        log('[TESOURO] chao de E8: %s' % ' '.join(resposta.split())[:60])
    except Exception as e:      # noqa: BLE001
        log('[TESOURO] chao de E8 falhou (%s)' % e)
    finally:
        try:
            ctx.recall()
        except Exception:       # noqa: BLE001
            pass
    time.sleep(2)
    return tem_chave(ctx.run('inventory')[0])


ESSENCIAIS = ('cantil', 'pao recheado', 'chave do tesouro', 'tomo')      # o resto do inventario vai para a mochila


def seletores_para_guardar(inventario):
    """Seletores `all.<palavra>` do `put` para tudo que nao e' essencial. Pura.

    A palavra e' a mais longa e especifica do nome; item que nao cabe (NAO-GUARDAR, tomo) fica de fora.
    """
    import identificar_itens as ii
    sels = []
    for nome, _q, _m in ii.itens_do_inventario(inventario):
        k = ii.normalizar(nome)
        if any(e in k for e in ESSENCIAIS):
            continue
        palavras = sorted(ii.palavras_chave(nome), key=len, reverse=True)
        if palavras and 'all.' + palavras[0] not in sels:
            sels.append('all.' + palavras[0])
    return sels


def guardar_espolio(ctx, log=print):
    """Padrao do projeto (`base.guardar_na_mochila`): o que nao e' usado vai para a mochila VESTIDA, que reduz o peso."""
    import base
    sels = seletores_para_guardar(ctx.run('inventory')[0])
    if sels:
        log('[TESOURO] guardando na mochila: %s' % ', '.join(sels))
        base.guardar_na_mochila(*sels)


def socorrer(log=print):
    """Cuida de comida, agua e magias; se o cuidar pedir recarga, roda o prepara (o estoque de pao acaba no kite)."""
    import subprocess
    cuidar = RAIZ / 'automato' / 'camadas' / 'cuidar.py'
    if subprocess.run([sys.executable, str(cuidar)], check=False).returncode == 2:
        log('[TESOURO] cuidar pediu recarga -> prepara')
        subprocess.run([sys.executable, str(RAIZ / 'automato' / 'camadas' / 'prepara.py'), '--forcar', '--sem-doacoes'], check=False)


def obter_chave_branca(ctx, log=print):
    """Chave do Tesouro Branco: o Rei Branco (E1) morre UMA vez (excecao de moralidade do autor, 2026-10-22).

    Depois da morte o `kite_rei` pega TODAS as chaves (`get all.chave`); a trava em `rei_branco_morto.json` impede um
    segundo kill em outra execucao. Sem chave depois da morte unica, nao repete: devolve False.
    """
    if REI_BRANCO_MORTO.exists():
        log('[TESOURO] o Rei Branco ja foi morto uma vez (%s): nao repito' % REI_BRANCO_MORTO.name)
        return False
    log('[TESOURO] Rei Branco: kite (excecao do autor, UMA vez)')
    codigo = xc.kite_rei(idas=60, log=log, lado='branco')
    if codigo == 0:
        REI_BRANCO_MORTO.parent.mkdir(parents=True, exist_ok=True)
        REI_BRANCO_MORTO.write_text(json.dumps({'t': time.time(), 'por': 'tesouro_negro.py --lado branco'}), encoding='utf-8')
    ctx.cmd('get all.chave', 0.8)
    ctx.cmd('get all.chave corpo', 0.8)
    ctx.recall()
    time.sleep(3)
    ok = tem_chave(ctx.run('inventory')[0])
    registrar({'t': time.time(), 'resultado': 'chave', 'lado': 'branco', 'ok': ok})
    return ok


def obter_chave(ctx, log=print):
    """Garante a Chave do Tesouro Negro no inventario. A chave DETERIORA (~30 min; sumiu no login do Dia 163).

    1) ja' tem; 2) chao de E8 (o Rei morre as vezes sem credito e a chave cai la'); 3) kite no Rei (`xadrez_cascata`),
    e depois outra olhada no chao de E8 (o kite faz recall e o Rei pode sangrar depois). Devolve True se a chave ficou.
    """
    if tem_chave(ctx.run('inventory')[0]):
        return True
    socorrer(log)
    if LADO == 'branco':
        return obter_chave_branca(ctx, log)
    if chao_de_e8(ctx, log):
        return True
    log('[TESOURO] sem chave no chao: kite no Rei Negro (xadrez_cascata, so para a chave)')
    xc.kite_rei(idas=60, log=log)                             # pode deixar a personagem em E8 se o Rei morrer
    ctx.cmd('get all.chave', 0.8)
    ctx.cmd('get all.chave corpo', 0.8)
    ctx.recall()
    time.sleep(3)
    ok = tem_chave(ctx.run('inventory')[0]) or chao_de_e8(ctx, log)    # o Rei pode ter sangrado depois do recall
    registrar({'t': time.time(), 'resultado': 'chave', 'ok': ok})      # mede a vida util da chave (deteriora)
    return ok


def registrar(r):
    LOG.parent.mkdir(parents=True, exist_ok=True)
    with LOG.open('a', encoding='utf-8') as f:
        f.write(json.dumps(r, ensure_ascii=False) + '\n')


def ocioso(segundos, ctx, log=print):
    """Tempo entre sondas: tarefas curtas uteis e sono para o resto, nunca parado em silencio."""
    if segundos < 45:
        time.sleep(max(0, segundos))
        return
    import aproveitar_tempo
    try:
        aproveitar_tempo.aproveitar(min(segundos / 60.0, 3.0), tarefas=aproveitar_tempo.por_nome(TAREFAS_OCIOSAS),
                                    ctx=ctx, log=log)
    except Exception as e:      # noqa: BLE001
        log('[TESOURO] ATENCAO: tarefas ociosas falharam (%s); seguindo' % e)


def rodar(tomadas_alvo=5, max_min=240, log=print, ocioso_fn=None):
    import base
    ctx = xc.Ctx()
    brief_antes = base.brief(False)         # a rota confere a casa pela descricao: o modo breve a esconderia
    ocioso_fn = ocioso_fn or ocioso
    tomadas, falhas, proxima, total = [], 0, 0.0, 0
    inicio = time.time()
    try:
        ctx.run('hold cajado')                  # o login solta o item da mao (Dia 163)
        if not obter_chave(ctx, log):
            log('[TESOURO] sem a Chave do Tesouro Negro: nao consegui obter (Rei Negro ou chao de E8)')
            return 2
        while len(tomadas) < tomadas_alvo and (time.time() - inicio) / 60.0 < max_min:
            agora = time.time()
            if agora < proxima:
                # a chave deteriora em ~30 min e o reset leva ~13: se ela sumiu, a espera e' o momento do kite no Rei
                if not tem_chave(ctx.run('inventory')[0]):
                    obter_chave(ctx, log)
                else:
                    ocioso_fn(proxima - agora, ctx, log)
                if time.time() < proxima:
                    time.sleep(min(30, max(0, proxima - time.time())))
                continue
            if not tem_chave(ctx.run('inventory')[0]) and not obter_chave(ctx, log):
                log('[TESOURO] PARANDO: a chave deteriorou e nao consegui outra')
                return 2
            guardar_espolio(ctx, log)
            if sem_folga(ctx.run('score tudo')[0]):
                log('[TESOURO] PARANDO: sem folga de peso (< %d kg) para o tesouro; guarde itens na mochila' % PESO_FOLGA_KG)
                return 4
            r = uma_ida(ctx, log)
            registrar(r)
            log('[TESOURO] ida: %s %s' % (r['resultado'], {k: v for k, v in r.items() if k in ('moedas', 'porta', 'erro')}))
            if r['resultado'] == 'pegou':
                tomadas.append(r['t'])
                total += r.get('moedas') or 0
                falhas = 0
                proxima = time.time() + proxima_espera_min(tomadas) * 60
                log('[TESOURO] %d de %d tomadas, +%d moedas; proxima sonda em %.1f min'
                    % (len(tomadas), tomadas_alvo, total, (proxima - time.time()) / 60))
            elif r['resultado'] == 'sem_tesouro':
                falhas = 0
                proxima = time.time() + PASSO_MIN * 60
            else:
                falhas += 1
                if falhas >= FALHAS_SEGUIDAS_MAX:
                    log('[TESOURO] PARANDO: %d idas seguidas sem sucesso (%s)' % (falhas, r.get('erro') or r['resultado']))
                    return 3
                proxima = time.time() + 60
        log('[TESOURO] fim: %d tomadas, +%d moedas, %.0f min' % (len(tomadas), total, (time.time() - inicio) / 60))
        return 0 if len(tomadas) >= tomadas_alvo else 1
    finally:
        base.brief(brief_antes)


def main(argv=None):
    ap = argparse.ArgumentParser(description='Pega o Tesouro Negro da Realeza varias vezes.')
    ap.add_argument('--tomadas', type=int, default=5)
    ap.add_argument('--max-min', type=int, default=240, help='teto de minutos da rotina')
    ap.add_argument('--simular', action='store_true')
    ap.add_argument('--lado', choices=sorted(TESOUROS), default='negro')
    ap.add_argument('--excecao-rei-branco', action='store_true', help='autorizacao do autor (DECISOES §17): mata o Rei Branco UMA vez')
    args = ap.parse_args(argv)
    global LADO
    LADO = args.lado
    if LADO == 'branco' and not args.excecao_rei_branco and not REI_BRANCO_MORTO.exists():
        print('o Tesouro Branco exige a chave do Rei Branco: --excecao-rei-branco (DECISOES §17, mata UMA vez)')
        return 2
    if args.simular:
        print('plano: %d tomadas; 1a sonda %d min depois da tomada, depois a cada %d min; periodo medido substitui o inicial; '
              'teto %d min; ocioso = %s' % (args.tomadas, ESPERA_INICIAL_MIN, PASSO_MIN, args.max_min, ', '.join(TAREFAS_OCIOSAS)))
        return 0
    try:
        return rodar(args.tomadas, args.max_min)
    except xc.Perdida as e:     # driver caiu (resposta vazia): sai limpo, sem traceback, para o supervisor reiniciar so' o live_daemon
        print('[TESOURO] PARANDO: %s' % e, flush=True)
        return 5


if __name__ == '__main__':
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    sys.exit(main())
