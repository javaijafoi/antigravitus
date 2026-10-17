# -*- coding: utf-8 -*-
"""seguro.py - o gatinho: deixa a personagem SALVA e em local seguro se o agente morrer.

O problema que isto resolve: o fechamento correto ja existe (`_CLOSE` no driver faz
`stand` + `save` + `sleep` e confirma com o servidor). Mas ele so' acontece se ALGUEM
chamar. Se a sessao do agente acabar no meio (credito, timeout, processo morto), a
personagem fica parada onde estava - e parada em combate e' morte.

Como decide: o vigia NAO adivinha. Ele exige ociosidade comprovada - o transcript do
driver sem crescer por N segundos significa que ninguem esta' mandando comando. So'
entao age. Enquanto alguem (rotina ou agente) escreve no transcript, ele fica quieto:
mandar comando paralelo desincroniza a sessao, e isso o projeto ja' pagou caro.

Modos:
    --vigiar     (padrao) laco: a cada --intervalo, checa e so' age se abandonada
    --uma-vez    fecha agora, sem esperar ociosidade
    --simular    (padrao) NAO manda comando nenhum; so' imprime o que faria
    --executar   liga a acao real

Sequencia de encerramento: `recall` se estiver em combate/vida baixa -> `_CLOSE sleep`
(stand + save + sleep, com confirmacao textual do servidor). `quit` nunca: quit apaga
progresso de missao.

Uso:
    python automato/acoes/seguro.py                      # simula o vigia
    python automato/acoes/seguro.py --vigiar --executar  # o gatinho de verdade
    python automato/acoes/seguro.py --uma-vez --executar # fecha agora

Codigos de saida: 0 ok/nada a fazer | 1 falhou | 2 acao simulada | 3 sem sessao
(daemon fora do ar: nada a proteger).

IMPORTANTE: inicie este script FORA da arvore de jobs do agente (janela propria ou
processo destacado). Job gerenciado pelo agente morre junto com ele - e ai o gatinho
nao serve para nada.
"""
import argparse
import json
import socket
import sys
import time
from datetime import datetime
from pathlib import Path

AQUI = Path(__file__).resolve()
AUTOMATO = AQUI.parents[1]                  # automato/
RUNTIME = AUTOMATO / 'runtime'
TOKEN_FILE = RUNTIME / '.controller'
LOG = RUNTIME / 'seguro.log'

HOST = '127.0.0.1'
PORT = 14888
PORTA = PORT               # ajustavel por --porta (usado nos testes com driver falso)

OCIOSO_PADRAO = 900        # 15 min sem transcript crescer = agente abandonou
INTERVALO_PADRAO = 30      # consulta o _STATUS a cada 30 s
VIDA_BAIXA = 0.35


def agora():
    return datetime.now().astimezone().isoformat(timespec='seconds')


def registrar(msg):
    linha = f'{agora()} [SEGURO] {msg}'
    print(linha, flush=True)
    try:
        RUNTIME.mkdir(parents=True, exist_ok=True)
        with LOG.open('a', encoding='utf-8') as fh:
            fh.write(linha + '\n')
    except OSError:
        pass


def token():
    try:
        return (json.loads(TOKEN_FILE.read_text(encoding='utf-8')) or {}).get('token', '') or ''
    except Exception:
        return ''


def falar(comando, timeout=90.0):
    """Uma conexao por comando, como manda o protocolo do daemon. Devolve dict ou None."""
    tok = token()
    try:
        sock = socket.create_connection((HOST, PORTA), timeout=5.0)
        try:
            sock.settimeout(timeout)
            sock.sendall(f'{tok}\n{comando}\n'.encode('utf-8'))
            partes = []
            while True:
                bloco = sock.recv(65536)
                if not bloco:
                    break
                partes.append(bloco)
        finally:
            sock.close()
        dados = b''.join(partes).decode('utf-8', errors='replace').strip()
        if not dados:
            return None
        return json.loads(dados)
    except (OSError, ValueError):
        return None


def transcript_mais_novo():
    try:
        arquivos = list(RUNTIME.glob('transcript_*.jsonl'))
    except OSError:
        return None
    return max(arquivos, key=lambda p: p.stat().st_mtime) if arquivos else None


def segundos_parado():
    """Ha' quanto tempo ninguem escreve no transcript (= ninguem esta' dirigindo)."""
    arq = transcript_mais_novo()
    if arq is None:
        return None, None
    try:
        return time.time() - arq.stat().st_mtime, arq
    except OSError:
        return None, None


def vida_baixa(status):
    vitais = status.get('vitals') or {}
    hp, hmax = vitais.get('hp'), vitais.get('hp_max') or vitais.get('max_hp')
    if not isinstance(hp, (int, float)) or not isinstance(hmax, (int, float)) or hmax <= 0:
        return False
    return (hp / hmax) < VIDA_BAIXA


def plano_encerramento(status):
    """Devolve a lista de comandos a enviar, na ordem."""
    passos = []
    if status.get('in_combat') or vida_baixa(status):
        passos.append('recall')          # saida de emergencia; gratuita ate' o nivel 70
    passos.append('_CLOSE sleep')        # stand + save + sleep, com confirmacao
    return passos


def executar(passos, simular):
    for comando in passos:
        if simular:
            registrar(f'[SIMULADO] enviaria: {comando}')
            continue
        resposta = falar(comando)
        if resposta is None:
            registrar(f'{comando}: sem resposta do driver')
            return 1
        if comando.startswith('_CLOSE'):
            ok = bool(resposta.get('save_confirmed'))
            registrar(f'_CLOSE save_confirmed={ok} sleep_confirmed={resposta.get("sleep_confirmed")}'
                      f' estado={resposta.get("state") or (resposta.get("steps") or {}).get("state")}')
            return 0 if ok else 1
        registrar(f'{comando}: ok')
    return 0


def quadro(status):
    vitais = status.get('vitals') or {}
    return (f"estado={status.get('state')} combate={status.get('in_combat')} "
            f"hp={vitais.get('hp')}/{vitais.get('hp_max') or vitais.get('max_hp')} "
            f"mana={vitais.get('mana')} mv={vitais.get('mv')} sala={status.get('room')!r}")


def uma_vez(simular):
    status = falar('_STATUS')
    if status is None:
        registrar('sem sessao: driver fora do ar, nada a proteger')
        return 3
    registrar('estado agora: ' + quadro(status))
    if status.get('state') == 'dead_or_menu':
        registrar('personagem morta/em menu: nao ha o que salvar aqui; seguir o fluxo de ressurreicao')
        return 1
    passos = plano_encerramento(status)
    registrar('plano: ' + ' -> '.join(passos))
    return executar(passos, simular)


def vigiar(simular, ocioso, intervalo):
    registrar(f'vigia iniciado (ocioso={ocioso}s intervalo={intervalo}s simular={simular})')
    while True:
        status = falar('_STATUS')
        if status is None:
            registrar('sem sessao: driver fora do ar; encerrando o vigia')
            return 3
        parado, arq = segundos_parado()
        if parado is not None and parado >= ocioso:
            registrar(f'ABANDONADA: {int(parado)}s sem transcript ({arq.name}); {quadro(status)}')
            if status.get('state') == 'dead_or_menu':
                registrar('morta/em menu: nao age; precisa de ressurreicao')
                return 1
            passos = plano_encerramento(status)
            registrar('plano: ' + ' -> '.join(passos))
            return executar(passos, simular)
        time.sleep(intervalo)


def main():
    p = argparse.ArgumentParser(description='Deixa a personagem salva e segura se o agente morrer.')
    p.add_argument('--vigiar', action='store_true', help='laco de vigilancia (padrao)')
    p.add_argument('--uma-vez', action='store_true', help='fecha agora, sem esperar ociosidade')
    p.add_argument('--executar', action='store_true', help='manda os comandos de verdade')
    p.add_argument('--simular', action='store_true', help='so imprime (padrao)')
    p.add_argument('--ocioso', type=int, default=OCIOSO_PADRAO, help='segundos sem transcript para considerar abandonada')
    p.add_argument('--intervalo', type=int, default=INTERVALO_PADRAO, help='segundos entre checagens')
    p.add_argument('--porta', type=int, default=PORT, help='porta do driver (padrao 14888; util em teste)')
    a = p.parse_args()
    global PORTA
    PORTA = a.porta
    simular = not a.executar
    if a.uma_vez:
        return uma_vez(simular)
    return vigiar(simular, a.ocioso, a.intervalo)


if __name__ == '__main__':
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    sys.exit(main())

