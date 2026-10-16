# -*- coding: utf-8 -*-
"""turno.py - o encarregado do turno.

Junta as tres pecas:
  1. VIGIA (vigia.py)      - le o log e diz se esta tudo bem (leitura pura, nao interfere);
  2. PREPARA (prepara.py)  - conserta: come, bebe, guarda o ouro no banco, dorme e volta ao Templo;
  3. MOTOR (motor.py)      - trabalha na missao (sabe sempre partir do Templo).

O turno roda o motor em segundo plano e, A CADA MINUTO, pergunta ao vigia.
Se o vigia acusar problema, o turno MATA o motor, manda o prepara resolver e
recomeca - exatamente o "monitora status que sobrepoe o motor" pedido pelo autor.
"""
import argparse
import subprocess
import sys
import time
from pathlib import Path

LOCAL = Path(__file__).resolve().parents[1]
PY = sys.executable
sys.path.insert(0, str(LOCAL / 'camadas'))
sys.path.insert(0, str(LOCAL / 'nucleo'))
import vigia  # noqa: E402

MINUTOS_POR_TURNO = 6
TURNOS = 4
PROBLEMAS = ('MORTA', 'FOME', 'SEDE', 'VIDA_BAIXA', 'MANA_BAIXA', 'TRAVADO')


def roda(nome):
    print(f'[turno] rodando {nome}', flush=True)
    return subprocess.run([PY, str(LOCAL / nome)], check=False).returncode


def motor_em_segundo_plano(rotina):
    log = open(LOCAL / 'rotina.log', 'a', encoding='utf-8', errors='replace')
    log.write(f'\n=== {time.strftime("%H:%M:%S")} rotina={rotina} ===\n')
    log.flush()
    return subprocess.Popen([PY, str(LOCAL / 'camadas' / 'trabalhar.py'), '--rotina', rotina],
                            stdout=log, stderr=subprocess.STDOUT)


def main():
    ap = argparse.ArgumentParser(description='Encarregado do turno: vigia + prepara + rotina.')
    ap.add_argument('--rotina', default='milharal', help='rotina a executar')
    ap.add_argument('--turnos', type=int, default=TURNOS)
    args = ap.parse_args()
    print(f'[turno] rotina={args.rotina}', flush=True)
    for turno in range(1, args.turnos + 1):
        d = vigia.diagnosticar()
        print(f'[turno {turno}] vigia={d["estado"]} {d.get("vitais", "")}', flush=True)
        for m in d.get('motivos', []):
            print('   -', m, flush=True)
        if d['estado'] != 'OK':
            roda('prepara.py')
        p = motor_em_segundo_plano(args.rotina)
        estado = 'OK'
        for minuto in range(1, MINUTOS_POR_TURNO + 1):
            time.sleep(60)
            d = vigia.diagnosticar()
            estado = d['estado']
            print(f'   [min {minuto}] vigia={estado} {d.get("vitais", "")}', flush=True)
            if estado in PROBLEMAS:
                print(f'   !! problema ({estado}) - interrompendo o motor', flush=True)
                p.kill()
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
            roda('ressuscitar6.py')
    print('[turno] fim', flush=True)
    return 0


if __name__ == '__main__':
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    sys.exit(main())
