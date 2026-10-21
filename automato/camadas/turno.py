# -*- coding: utf-8 -*-
"""turno.py - o encarregado do turno.

Tres camadas, cada uma com um trabalho so':

    vigia.py    OBSERVA   - le o log e o driver (por IPC, sem falar com o MUD)
                            e diz o estado. Nunca age.
    cuidar.py   CUIDA     - em campo: come, bebe, veste armadura e
                            invisibilidade. Nunca vai a cidade.
    prepara.py  RECARREGA - a ida a cidade: padaria, fonte, banco, sono. So'
                            entra quando o cuidar avisa que o estoque acabou.

O turno roda a rotina em segundo plano e, A CADA MINUTO, pergunta ao vigia. Se o
vigia acusar problema, o turno mata o motor, manda o `cuidar` resolver e so'
manda o `prepara` se o cuidar disser que falta estoque.

Os codigos de saida do `cuidar.py` sao o contrato: 0 = resolvido em campo,
2 = precisa recarregar, 1 = nao resolveu sozinho.
"""
import sys as _sys
from pathlib import Path as _Path
_sys.path.insert(0, str(_Path(__file__).resolve().parents[1] / 'nucleo'))

import argparse
import os
import subprocess
import sys
import time
from pathlib import Path

LOCAL = Path(__file__).resolve().parents[1]        # automato/
PY = sys.executable
sys.path.insert(0, str(LOCAL / 'camadas'))
sys.path.insert(0, str(LOCAL / 'nucleo'))
import vigia  # noqa: E402

MINUTOS_POR_TURNO = 6
TURNOS = 4
PROBLEMAS = ('MORTA', 'FOME', 'SEDE', 'VIDA_BAIXA', 'MANA_BAIXA', 'TRAVADO', 'EM_COMBATE')
PRECISA_RECARGA = 2


def roda(relativo, extra=()):
    """Executa um script pelo caminho relativo a automato/.

    Antes isto montava `automato/prepara.py` e `automato/ressuscitar6.py`:
    nenhum dos dois existe (estao em camadas/ e acoes/). O prepara nunca rodou
    por aqui - o turno so' achava que sim.
    """
    alvo = LOCAL / relativo
    if not alvo.is_file():
        print(f'[turno] NAO EXISTE: {alvo}', flush=True)
        return 1
    print(f'[turno] rodando {relativo}', flush=True)
    return subprocess.run([PY, str(alvo), *extra], check=False).returncode


def motor_em_segundo_plano(rotina):
    log = open(LOCAL / 'rotina.log', 'a', encoding='utf-8', errors='replace')
    log.write(f'\n=== {time.strftime("%H:%M:%S")} rotina={rotina} ===\n')
    log.flush()
    # o transcript marca cada comando como "turno:<rotina>" (base.origem()): prova de jogo supervisionado
    env = dict(os.environ, MUD_ORIGEM='turno:' + rotina)
    return subprocess.Popen([PY, str(LOCAL / 'camadas' / 'trabalhar.py'), '--rotina', rotina],
                            stdout=log, stderr=subprocess.STDOUT, env=env)


def socorrer():
    """Cuidado em campo primeiro; a cidade so' se o estoque acabou."""
    if roda('camadas/cuidar.py') == PRECISA_RECARGA:
        print('[turno] cuidar pediu recarga -> prepara (viagem a cidade)', flush=True)
        roda('camadas/prepara.py')
        roda('camadas/cuidar.py')       # aplica o cuidado sobre o estoque novo


def main():
    ap = argparse.ArgumentParser(description='Encarregado do turno: vigia + cuidar + prepara + rotina.')
    ap.add_argument('--rotina', default='milharal', help='rotina a executar')
    ap.add_argument('--turnos', type=int, default=TURNOS)
    ap.add_argument('--socorrer', action='store_true',
                    help='aplica cuidado (e recarga, se preciso) antes de comecar')
    args = ap.parse_args()

    print(f'[turno] rotina={args.rotina}', flush=True)
    # Diretiva §26: o turno nao comeca com fome, sede ou sem armadura. O vigia
    # nao acusa armadura, entao o cuidado roda uma vez ANTES do laco, sempre.
    socorrer()
    for turno in range(1, args.turnos + 1):
        d = vigia.diagnosticar()
        print(f'[turno {turno}] vigia={d["estado"]} {d.get("vitais", "")} '
              f'fome={d.get("fome")} sede={d.get("sede")}', flush=True)
        for m in d.get('motivos', []):
            print('   -', m, flush=True)

        if args.socorrer or d['estado'] in PROBLEMAS:
            socorrer()

        p = motor_em_segundo_plano(args.rotina)
        estado = 'OK'
        for minuto in range(1, MINUTOS_POR_TURNO + 1):
            time.sleep(60)
            d = vigia.diagnosticar()
            estado = d['estado']
            print(f'   [min {minuto}] vigia={estado} {d.get("vitais", "")} '
                  f'fome={d.get("fome")} sede={d.get("sede")}', flush=True)
            if estado in PROBLEMAS:
                print(f'   !! problema ({estado}) - interrompendo o motor', flush=True)
                p.kill()
                socorrer()
                break
            if p.poll() is not None:
                print('   motor terminou sozinho - devolvendo ao vigia', flush=True)
                break
        if p.poll() is None:
            p.terminate()
            try:
                p.wait(timeout=20)
            except Exception:
                p.kill()
        if estado == 'MORTA':
            print('[turno] ressuscitando', flush=True)
            roda('acoes/ressuscitar.py')
    print('[turno] fim', flush=True)
    return 0


if __name__ == '__main__':
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    sys.exit(main())
