# -*- coding: utf-8 -*-
"""config.py - o unico lugar onde o automato aponta caminhos e limites.

Para adaptar o automato a outro projeto/heroi, mude SO este arquivo.
"""
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]        # raiz do repositorio

# --- onde ficam os CONHECIMENTOS referenciados (nao copiados) ---
DIR_HEROI = RAIZ / "data" / "heroes" / "grebolius"
DOC_CONHECIMENTO = DIR_HEROI / "conhecimento.md"   # rotas, economia, DT, tudo aprendido
DOC_DIRETIVA = DIR_HEROI / "diretiva_de_jogo.md"   # as regras de como jogar
DOC_MAPA = DIR_HEROI / "mapa.json"                 # o mapa vivo das salas
DIR_DRIVER = RAIZ / "automato" / "nucleo" / "driver"   # o driver vive DENTRO do automato
RUNTIME = RAIZ / "automato" / "runtime"                # token, senha e logs (nao versionados)
LOCK = RUNTIME / ".controller"                         # token do driver (segredo, fora do git)
DIR_LOGS = RUNTIME                                     # logs de sessao session_live_*.log
LOG_ROTINA = RUNTIME / "rotina.log"                    # saida das rotinas
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
