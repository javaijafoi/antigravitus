#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""mapear_tabuleiro.py - acrescenta ao mapa.json as 64 casas do Grande Tabuleiro de Xadrez (A1 a H8).

A zona 36 do CircleMUD e' uma grade 8x8 perfeita (docs/circlemud/05-mundo-padrao-vs-mapa.md, secao 5):
canto = 2 saidas, borda = 3, interior = 4. Convencao confirmada ao vivo (Dia 157, evidence/dia157-xadrez-*.json):

  colunas A..H de OESTE para LESTE, fileiras 1..8 de SUL para NORTE;
  H5 e' a casa de entrada (tem o portao a LESTE, que leva a `grande_tabuleiro_portao`);
  H1 = Torre do Rei Branco, F1 = Bispo Branco (patrono da Xeque-mate), A1 = Torre da Rainha Branca,
  fileira 8 preta: A8 Torre, B8 Cavalo, C8 Bispo, D8 Rainha (saida oculta `baixo`), E8 REI, F8 Bispo,
  G8 Cavalo, H8 Torre. Cor: soma (coluna + fileira) par = PRETA, impar = BRANCA (H1 = 8+1 e' branca).

Idempotente: reescreve as salas `xadrez_<Casa>` e religa o portao. Uso:

    python scripts/mapear_tabuleiro.py            # grava no mapa.json do heroi grebolius
    python scripts/mapear_tabuleiro.py --seco     # so' mostra o resumo
"""
import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MAPA = ROOT / 'data' / 'heroes' / 'grebolius' / 'mapa.json'
COLUNAS = 'ABCDEFGH'
ZONA = 'O Grande Tabuleiro de Xadrez'

# papel de cada casa especial (para o campo `notes` e o `risk`)
PECAS = {
    'A8': 'Torre da Rainha Negra (as torres empilham aqui)', 'B8': 'Cavalo da Rainha Negra',
    'C8': 'Bispo da Rainha Negra', 'D8': 'Rainha Negra; saida oculta `baixo` para a Tesouraria Negra',
    'E8': 'REI NEGRO: Santuario, ~1.500 de vida, ate 3 golpes mortais por rodada. NAO entrar sem plano',
    'F8': 'Bispo do Rei Negro', 'G8': 'Cavalo do Rei Negro', 'H8': 'Torre do Rei Negro',
    'A1': 'Torre da Rainha Branca', 'B1': 'Cavalo da Rainha Branca (o Cavaleiro Branco ataca quem entra visivel)',
    'C1': 'Bispo da Rainha Branca', 'D1': 'Rainha Branca', 'E1': 'REI BRANCO: mata quem esta na Xeque-mate ("Herege!")',
    'F1': 'Bispo Branco, patrono da Xeque-mate', 'G1': 'Cavalo do Rei Branco (o Cavaleiro Branco ataca quem entra visivel)',
    'H1': 'Torre do Rei Branco',
}
OPOSTO = {'n': 's', 's': 'n', 'e': 'w', 'w': 'e'}


def id_casa(col, fil):
    return 'xadrez_%s%d' % (COLUNAS[col], fil)


def cor(col, fil):
    # col 0..7, fil 1..8: A=1; H1 = 8+1 = 9 (impar) e' branca
    return 'Branca' if ((col + 1) + fil) % 2 == 1 else 'Preta'


def risco(col, fil):
    nome = COLUNAS[col] + str(fil)
    if nome == 'E8' or nome == 'E1':
        return 'Extremo', 'danger'
    if fil == 8 or (fil == 1 and nome not in ('F1', 'H1')):
        return 'Alto', 'danger'
    return 'Medio', 'medium'


def casas():
    """Lista de salas do tabuleiro, prontas para o mapa.json."""
    salas = []
    for fil in range(1, 9):
        for col in range(8):
            exits = {}
            if fil < 8:
                exits['n'] = id_casa(col, fil + 1)
            if fil > 1:
                exits['s'] = id_casa(col, fil - 1)
            if col < 7:
                exits['e'] = id_casa(col + 1, fil)
            if col > 0:
                exits['w'] = id_casa(col - 1, fil)
            nome = COLUNAS[col] + str(fil)
            if nome == 'H5':
                exits['e'] = 'grande_tabuleiro_portao'
            risk, code = risco(col, fil)
            salas.append({
                'id': id_casa(col, fil), 'name': 'Uma Casa %s' % cor(col, fil), 'layer': 'novatos',
                'zone': ZONA, 'risk': risk, 'risk_code': code, 'icon': '♟️',
                'coords': {'x': -(7 - col) * 120 + 600, 'y': fil * 120},
                'exits': exits, 'npcs': [],
                'notes': ('Casa %s do tabuleiro (zona 36). %s' % (nome, PECAS.get(nome, ''))).strip(),
                'discovered_in': 'Dia 157 (mapa por grade; confirmado ao vivo)',
                'fontes': ['docs/circlemud/05-mundo-padrao-vs-mapa.md', 'evidence/dia157-xadrez-etapa6.json'],
            })
    return salas


def aplicar(mapa):
    """Insere/atualiza as casas e religa o portao; devolve (acrescentadas, atualizadas)."""
    por_id = {r['id']: r for r in mapa['rooms']}
    novas, atual = 0, 0
    for sala in casas():
        if sala['id'] in por_id:
            idx = mapa['rooms'].index(por_id[sala['id']])
            mapa['rooms'][idx] = sala
            atual += 1
        else:
            mapa['rooms'].append(sala)
            novas += 1
    portao = next(r for r in mapa['rooms'] if r['id'] == 'grande_tabuleiro_portao')
    portao['exits']['w'] = 'xadrez_H5'
    portao['risk'] = 'Medio (so a passagem; o perigo esta em E8, E1, B1, G1 e na fileira 8)'
    portao['risk_code'] = 'medium'
    aliases = set(portao.get('aliases') or [])
    aliases.add('O Grande Tabuleiro de Xadrez de Midgaard')   # titulo real no jogo
    portao['aliases'] = sorted(aliases)
    portao['notes'] = (portao.get('notes', '') + ' | Dia 157: o oeste leva a casa H5 (xadrez_H5); '
                       'as 64 casas estao em xadrez_A1..xadrez_H8.').strip(' |')
    mapa['total_rooms'] = len(mapa['rooms'])
    return novas, atual


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    ap.add_argument('--seco', action='store_true', help='nao grava')
    a = ap.parse_args(argv)
    mapa = json.loads(MAPA.read_text(encoding='utf-8'))
    novas, atual = aplicar(mapa)
    print('casas novas=%d atualizadas=%d total_salas=%d' % (novas, atual, mapa['total_rooms']))
    if not a.seco:
        MAPA.write_text(json.dumps(mapa, ensure_ascii=False, indent=2), encoding='utf-8')
        print('gravado em', MAPA)
    return 0


if __name__ == '__main__':
    sys.exit(main())
