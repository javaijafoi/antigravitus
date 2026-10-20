# -*- coding: utf-8 -*-
"""verificar.py - autoexame do automato.

Responde uma pergunta so: "esta tudo no lugar para outro agente jogar?"
Checa ambiente, arquivos, driver, token, conhecimentos referenciados e rotinas.

Uso:
    python automato/verificar.py
"""
import importlib
import json
import socket
import sys
from pathlib import Path

AQUI = Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI / 'nucleo'))
sys.path.insert(0, str(AQUI / 'rotinas'))

OK, FALHA, AVISO = 'OK   ', 'FALHA', 'AVISO'
resultados = []


def checar(nome, condicao, detalhe='', critico=True):
    marca = OK if condicao else (FALHA if critico else AVISO)
    resultados.append((marca, nome, detalhe))
    return condicao


def main():
    import config

    # 1. ambiente
    checar('Python 3.10+', sys.version_info >= (3, 10), sys.version.split()[0])
    # `python` no PATH apontando para o atalho da Microsoft Store (WindowsApps) faz todo agente tropeçar.
    import shutil
    no_path = shutil.which('python') or ''
    checar('python no PATH', bool(no_path) and 'windowsapps' not in no_path.lower(),
           (no_path or 'ausente') + ('' if no_path and 'windowsapps' not in no_path.lower()
                                     else ' -> rode scripts\\configurar_python.ps1 -Aplicar'),
           critico=False)

    # 2. o core dentro da pasta
    nucleo = ['config.py', 'base.py', 'guarda.py']
    driver = ['debo_bot.py', 'parsers.py', 'live_daemon.py', 'play.py']
    checar('nucleo completo', all((AQUI / 'nucleo' / f).is_file() for f in nucleo),
           ', '.join(nucleo))
    checar('driver dentro do automato', all((AQUI / 'nucleo' / 'driver' / f).is_file() for f in driver),
           ', '.join(driver))
    checar('camadas', all((AQUI / 'camadas' / f).is_file() for f in
          ['vigia.py', 'prepara.py', 'trabalhar.py', 'turno.py']))
    checar('acoes', all((AQUI / 'acoes' / f).is_file() for f in ['mapear.py', 'ressuscitar.py']))

    # 3. runtime (segredos e logs) - nao versionado
    checar('runtime existe', config.RUNTIME.is_dir(), str(config.RUNTIME))
    checar('token do driver', config.LOCK.is_file(), str(config.LOCK), critico=False)
    senha = config.RUNTIME / '.mud_pass'
    checar('senha do MUD', senha.is_file() or bool(__import__('os').environ.get('MUD_PASS')),
           'automato/runtime/.mud_pass', critico=False)

    # 4. driver no ar?
    s = socket.socket()
    s.settimeout(3)
    try:
        s.connect((config.HOST, config.PORT))
        no_ar = True
    except Exception:
        no_ar = False
    finally:
        s.close()
    checar('driver escutando', no_ar, f'{config.HOST}:{config.PORT}', critico=False)

    # 5. conhecimentos referenciados
    checar('conhecimento.md', config.DOC_CONHECIMENTO.is_file(), 'rotas e economia')
    checar('diretiva_de_jogo.md', config.DOC_DIRETIVA.is_file(), 'regras de como jogar')
    checar('mapa.json', config.DOC_MAPA.is_file(), 'mapa vivo das salas')
    checar('plano do capitulo', (config.DIR_HEROI / 'plano_capitulo_03.md').is_file(),
           'plano_capitulo_03.md', critico=False)

    # 6. modulos carregam
    try:
        import base  # noqa: F401
        import guarda  # noqa: F401
        checar('nucleo importa', True)
    except Exception as e:
        checar('nucleo importa', False, str(e)[:60])
    rotinas = sorted(p.stem for p in (AQUI / 'rotinas').glob('*.py')
                     if p.stem not in ('base', '__init__'))
    falhas = []
    for r in rotinas:
        try:
            importlib.import_module(r)
        except Exception as e:
            falhas.append(f'{r}: {str(e)[:40]}')
    checar('rotinas importam', not falhas, '; '.join(falhas) or ', '.join(rotinas))

    # 7. documentacao
    for doc in ['README.md', 'CHANGELOG.md', 'DECISOES.md']:
        checar(doc, (AQUI / doc).is_file())

    print('AUTOEXAME DO AUTOMATO')
    print('=' * 68)
    for marca, nome, detalhe in resultados:
        print(f'  [{marca}] {nome:28s} {detalhe}')
    ruins = [r for r in resultados if r[0] == FALHA]
    print('=' * 68)
    print(f'{len(resultados) - len(ruins)}/{len(resultados)} itens OK' +
          ('' if not ruins else f'  |  {len(ruins)} FALHA(S)'))
    return 1 if ruins else 0


if __name__ == '__main__':
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    sys.exit(main())
