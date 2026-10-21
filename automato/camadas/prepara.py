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
import vigia           # noqa: E402
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


CA_COM_ARMOR = 140   # sem a magia a CA e' 112; com `armor`, 148 (dura horas)


def ca_do_score(texto):
    m = re.search(r'Classe de Armadura:\s*(-?\d+)', texto or '')
    return int(m.group(1)) if m else None


def garantir_armor():
    """Mantem a magia `armor` ligada, como a comida: confere a CA e relanca se caiu.

    O Templo bloqueia magia, entao o lance e' na Praca do Templo (`s` do Templo)."""
    ca = ca_do_score(situacao()['texto'])
    if ca is None or ca >= CA_COM_ARMOR:
        return False
    run('recall')
    run('stand')
    andar('s')
    run("cast 'armor'")
    nova = ca_do_score(situacao()['texto'])
    print('[PREPARA] armor lancado: CA %s -> %s' % (ca, nova), flush=True)
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


# O sono nao faz a mesma coisa para mana e para vida. Medido nos transcripts de
# 16 a 20/10 (374 episodios de sono, mediana de 3 min):
#   * mana: enche em ~3 min (mediana +18, ate +231 por episodio);
#   * vida: +0 na mediana; quando sobe, ~5 hp/min (34 de 591 intervalos fora de
#     combate tiveram ganho). Com 226 de vida maxima, a barra cheia custa ~45 min;
#   * com fome ou sede o ganho nao acontece: "morrendo de fome! (-3hp, -6mn)".
# Antes disto o `dormir` dormia 75 s fixos e a docstring dizia o alvo: "movimento
# e mana". A vida nunca foi objetivo, e por isso a personagem acordava achando
# que estava pronta com 100 de vida faltando.
TAXA_HP_POR_MINUTO = 5.0
SONO_FATIA_S = 120          # de quanto em quanto tempo o vigia olha os vitais
SONO_MINUTOS_MAX = 45
SONO_MINUTOS_MIN = 3


def hp_do_score(texto):
    """(atual, maximo) de vida no texto do `score`; (None, None) se nao veio."""
    m = re.search(r'Vida:\s*(?:\{[^}]*\})?\s*(-?\d+)\s+de\s+(\d+)', texto or '')
    return (int(m.group(1)), int(m.group(2))) if m else (None, None)


def minutos_de_sono(atual, maximo, taxa=None, alvo=0.98):
    """Quanto dormir para chegar a `alvo` da vida. Puro: nao fala com o MUD."""
    if not atual or not maximo or atual < 0:
        return 0
    falta = maximo * alvo - atual
    if falta <= 0:
        return 0
    return int(min(SONO_MINUTOS_MAX, max(SONO_MINUTOS_MIN, round(falta / (taxa or TAXA_HP_POR_MINUTO)))))


def comer_beber():
    """Come e bebe do que já está na bolsa. Devolve o que fez."""
    feito = []
    s = situacao()
    if s['fome'] and conta_pao() != 0:
        run('eat pao')
        feito.append('comeu')
    if s['sede'] and agua_no_cantil() != 0.0:
        run('drink cantil')
        feito.append('bebeu')
    return feito


def dormir():
    """Dorme para recuperar VIDA, olhando os vitais durante o sono.

    O `vigia.do_driver()` lê fome, sede e vida pelo IPC, **sem mandar comando ao
    MUD** — é o observador que já existe. Aqui ele é consultado a cada fatia, e é
    ele que decide acordar: se a fome aparece, o sono é interrompido, come-se e
    volta-se a dormir. Sem isso, o `time.sleep()` de antes dormia cego: passada a
    saciedade, os minutos finais eram com fome, e fome tira ~3 hp por tick
    (medido: `-3hp, -6mn`) — o fim do sono podia ser negativo.
    """
    voltar_ao_templo()
    s = situacao()
    hp, hp_max = hp_do_score(s['texto'])
    alvo_hp = (hp_max or 0) * 0.98
    limite = time.time() + (minutos_de_sono(hp, hp_max) or SONO_MINUTOS_MIN) * 60
    dormindo, ultimo_hp, sem_ganho = False, hp, 0
    while time.time() < limite:
        if not dormindo:
            run('sleep')
            dormindo = True
        time.sleep(SONO_FATIA_S)
        d = vigia.do_driver() or {}
        supply = d.get('supplies') or {}
        hp_agora = (d.get('vitals') or {}).get('hp')
        if supply.get('fome') or supply.get('sede'):
            run('wake')
            run('stand')
            dormindo = False
            feito = comer_beber()
            print('[PREPARA] fome/sede no meio do sono: acordou e %s'
                  % (', '.join(feito) or 'não havia estoque'), flush=True)
            continue
        if isinstance(hp_agora, int) and isinstance(ultimo_hp, int):
            sem_ganho = sem_ganho + 1 if hp_agora <= ultimo_hp else 0
            ultimo_hp = hp_agora
            if alvo_hp and hp_agora >= alvo_hp:
                break
            if sem_ganho >= 2:
                print('[PREPARA] a vida parou de subir (sem ganho em duas fatias): parar', flush=True)
                break
    if dormindo:
        run('wake')
        run('stand')
    depois = hp_do_score(situacao()['texto'])[0]
    print('[PREPARA] fim do sono: vida %s -> %s de %s (taxa ~%.1f hp/min)'
          % (hp, depois, hp_max, TAXA_HP_POR_MINUTO), flush=True)
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
        linha_crua = linha.strip()
        low = sem_acento(linha_crua)
        # NUNCA dar get em itens explicitamente amaldiçoados ou com aura vermelha/maligna:
        # Apenas barramos se houver sinal expresso de perigo na descrição, sem bloquear itens por nome
        if any(bad in low for bad in ['aura vermelha', 'amaldic', 'maldic', 'malign']):
            print('[PREPARA] doacoes: ignorando item com aura vermelha/maldição no chão: %r' % linha_crua, flush=True)
            continue
        l = re.sub(r'^\(x\d+\)\s*', '', linha_crua)
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
        t_id, _, _ = run('identify ' + chave, timeout=15.0)      # diretiva §10: identificar ANTES de vestir
        id_sem = sem_acento(t_id)
        if any(bad in id_sem for bad in ['maldic', 'amaldic', 'no_drop', 'nodrop', 'aura vermelha']):
            print('[PREPARA] doacoes: %r eh AMALDICOADO - devolvido sem vestir' % nome, flush=True)
            run('drop ' + chave)
            continue

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

    garantir_armor()
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
