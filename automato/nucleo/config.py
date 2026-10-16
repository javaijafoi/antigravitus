# -*- coding: utf-8 -*-
"""config.py - o unico lugar onde o automato aponta caminhos e limites.

Para adaptar o automato a outro projeto/heroi, mude SO este arquivo.
"""
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]        # raiz do repositorio
DIR_DRIVER = RAIZ / "scripts" / "local"           # onde vivem o driver e o token
LOCK = DIR_DRIVER / ".controller"                 # arquivo com o token do driver
DIR_LOGS = DIR_DRIVER                             # logs de sessao session_live_*.log
LOG_ROTINA = DIR_DRIVER / "rotina.log"            # saida das rotinas
HOST = "127.0.0.1"
PORT = 14888

# --- limites de seguranca ---
LIMITE_REPETICAO = 3      # mesma resposta N vezes seguidas -> parar
LIMITE_TEMPO = 430        # segundos maximos de trabalho por rotina
RESERVA_OURO = 300        # ouro que fica na mao; o resto vai para o banco
VIDA_MINIMA = 0.45        # abaixo disso o cacador recua
VIDA_PARA_LUTAR = 0.70    # so entra em sala cheia com a vida acima disso
MAGIA_PRINCIPAL = "lightning bolt"
MAGIA_RESERVA = "burning hands"
