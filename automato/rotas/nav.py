"""LEGADO: avisa e repassa ao automato/camadas/navegar.py (a navegação canônica).

A rota fixa Templo -> Praça de Jareth que vivia aqui (26 passos, verificada ao vivo no Dia 157)
virou arestas do mapa.json no Dia 157 (Claude Opus 5.5): `navegar.py --para lb013` faz o mesmo
trajeto, conferindo cada sala. Não acrescente rotas aqui; corrija o mapa.json.

Uso: python automato/rotas/nav.py <rota>      (repassa ao navegar.py)
     python automato/rotas/nav.py --listar
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'camadas'))
import navegar  # noqa: E402

# rota antiga -> destino no mapa.json (a origem o navegar.py deduz pelo look)
ROTAS = {
    'templo-praca-jareth': 'lb013',   # "Uma Praça" (Avenida Floris com a Rua do Rio)
    'praca-floris1': 'lb014',         # a 1ª Avenida Floris a leste da Praça
}


def main(argv=None):
    argv = list(sys.argv[1:] if argv is None else argv)
    print('AVISO: rotas/nav.py é legado; use automato/camadas/navegar.py --para <id>.', file=sys.stderr)
    if not argv or argv[0] == '--listar':
        for nome, destino in ROTAS.items():
            print('%-20s -> navegar.py --para %s' % (nome, destino))
        return 0
    rota, resto = argv[0], argv[1:]
    if rota not in ROTAS:
        print('rota desconhecida: %s (use --listar)' % rota, file=sys.stderr)
        return 2
    indice = any(a == '--ate' or a.startswith('--ate=') for a in resto) or any(
        a == '--de' and i + 1 < len(resto) and resto[i + 1].isdigit() for i, a in enumerate(resto))
    if indice:
        print('--de N/--ate N por índice de passo não existem mais; o navegar.py parte da sala atual '
              '(ou de --de <id da sala>).', file=sys.stderr)
        return 2
    return navegar.main(['--para', ROTAS[rota]] + resto)


if __name__ == '__main__':
    sys.exit(main())
