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
DOC_MAPA_VIVO = DIR_HEROI / "mapa_vivo.json"       # o levantamento digerido: grafo + portas por abrir
# Semear a cartografa com o levantamento das sessoes anteriores. Sem isto cada
# execucao redescobre o mesmo bolsao a partir do Templo; com isto ela planeja
# caminho direto ate' as portas que ainda nao abriu.
SEMEAR_LEVANTAMENTO = True
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

# --- modo batedor (mapeamento; capitulo 04) ---
# A cartografa nao caca: qualquer arranhao e' motivo de saida, entao o piso de
# vida e' bem mais alto que o VIDA_MINIMA do cacador (0.45).
LIMITE_TEMPO_BATEDOR = 900      # segundos; mapear e' lento (exits + look + passo por sala)
VIDA_MINIMA_BATEDOR = 0.80      # abaixo disso, recall e encerra
MANA_MINIMA_BATEDOR = 60        # invisibilidade e armadura custam mana; 260 e' finito
PASSOS_SEM_SALA_NOVA = 12       # detector de "perdida": N passos sem sala nova -> recall
MAX_VISITAS_LABIRINTO = 3       # salas homonimas: nao entrar mais que isso sem prova nova

# Titulos que se repetem em varias salas DIFERENTES. Onde o titulo nao
# identifica, a identidade e' a posicao - e estas salas ganham id proprio de
# labirinto (`lb###`) em vez do `lv###` comum, para nao confundir na hora de
# ler o mapa. Mora aqui porque duas ferramentas precisam da MESMA lista: a
# rotina de campo (para nao entrar mais que MAX_VISITAS_LABIRINTO) e a
# mesclagem (para escolher o prefixo do id).
TITULOS_LABIRINTO = {
    'num bosque iluminado', 'o milharal destruido', 'adentro do milharal destruido',
    'o gramado', 'avenida floris', 'a estrada midgaard-jareth',
    'uma parte densa da floresta', 'a trilha na floresta', 'um caminho dentre os campos',
    'o grande campo de midgaard', 'numa pequena vila', 'rua principal', 'a rua principal',
    'uma praca', 'o centro do vilarejo', 'um caminho', 'uma rua larga',
}

# --- relogio do jogo e duracao de magia (medido e provavel, Dia 156) ---
#
# ESCALA MEDIDA AO VIVO: a hora do jogo anda ~75 s reais. Transicoes
# cronometradas com o comando `time` (2026-10-16): 11h->meio-dia 61 s,
# meio-dia->13h 60 s, 13h->14h 78 s. Bate com o padrao do CircleMUD.
#
# ATENCAO A UNIDADE: o `score` fala em **horas de jogo** ("armor ( 24 horas )",
# "invisibility ( 12 horas )"). Quem ler "2 horas restantes" e esperar 2 horas
# REAIS erra por ~48x: 24 h de jogo = 24 x 75 s = 30 min reais.
SEGUNDOS_POR_HORA_DO_JOGO = 75
MARGEM_MAGIA = 0.83      # re-conjura antes de vencer: 24 h de jogo -> 25 min reais


def horas_de_jogo_para_segundos_reais(horas, escala=None):
    """HORAS DE JOGO (as do `score`) -> segundos REAIS. ID: horas_de_jogo_para_segundos_reais.

    Existe para o numero do `score` nao ser lido como relogio de parede. 24 horas de
    jogo dao ~30 minutos reais; 2 horas dao ~2,5 minutos.
    """
    return (horas or 0) * (escala or SEGUNDOS_POR_HORA_DO_JOGO)


def segundos_reais_para_horas_de_jogo(segundos, escala=None):
    """O inverso: quantas HORAS DE JOGO cabem em N segundos reais."""
    return (segundos or 0) / (escala or SEGUNDOS_POR_HORA_DO_JOGO)


# Duracao de ARMOR e INVISIBILITY: **24 horas de jogo**, segundo o manual
# importado do CircleMUD (`maquina/spells.md`). E' PROVAVEL, nao confirmado
# para o DeBo - a ajuda e' do CircleMUD e o servidor pode divergir.
# Derivado da escala medida, nao escrito a mao: 24 x 75 s x 0,83 = 1494 -> 25 min.
# ATENCAO: isto e' REFERENCIA, nao criterio. Quem decide recastar e' o `cuidar.py`,
# lendo as horas restantes do `score` (`horas_restantes()`); o timer de 25 min
# deixou de ser usado em 2026-10-21 porque era um chute sobre a duracao real.
VALIDADE_MAGIAS_SEGUNDOS = int(horas_de_jogo_para_segundos_reais(24) * MARGEM_MAGIA)

# --- invisibilidade: opcional, e NAO e' mais a protecao padrao (Dia 156) ---
#
# Decisao do autor: *"ela nao precisa estar mais invisivel, e' so nao andar pelos
# lugares perigosos entre um lugar e outro; e se der merda, acontece, aprendemos"*.
#
# O motivo e' concreto: **invisibilidade bloqueia comercio** - o balconista
# responde "Nao negocio com quem nao vejo!" e o `list` nao devolve nada. Isso
# obrigava a alternar `visible`/conjurar a cada loja. A protecao agora vem de
# ESCOLHER A ROTA, evitando as salas de risco alto, em vez de se esconder.
USAR_INVISIBILIDADE = False

# Codigos de risco que a rota deve evitar. Vem do campo `risk_code` do mapa.
RISCO_A_EVITAR = ('danger', 'high', 'fatal', 'critical')

# Quanto o prepara deve ter NA MAO para comprar. O banco protege o ouro da
# morte, mas a padaria cobra da mao: no Dia 156 ela ficou com fome, com 2
# moedas no bolso e 369 no banco, porque o prepara depositava e nunca sacava.
# 300 cobre pao, cantil e sobra para imprevisto. Se o banco nao cobrir, o
# prepara AVISA em vez de seguir calado - a decisao e' do autor.
SAQUE_PARA_COMPRAR = 300


# --- espolios: pegar dos corpos IMPORTA (diretiva do autor, Dia 157/158) ---
#
# O autor cobrou: pegar os itens dos corpos e' parte do trabalho, nao so' o ouro.
# O que decide se um item pode ser pego e' o `identify` DO PROPRIO OBJETO no chao
# (flag AMALDICOADO / NODROP = proibido; AGENTS #10 e diretiva_de_jogo.md par.15).
#
# Medido ao vivo (conhecimento.md par.68), nome como aparece no jogo:
#   PROIBIDO  - Armadura da Torre Negra: BRILHO AMALDICOADO, peso 60, valor 17000.
#   PERMITIDO - Lanca do Cavaleiro Negro (18 kg, valor 10000; ferreiro paga 4000),
#               Armadura/Espada do Peao Negro (ANTI-BOM, sem maldicao),
#               Coroa da Rainha Negra (ANTI-BOM, nao NODROP).
# Item que nao esta nas duas listas: `cast 'identify'` no chao antes do `get`.
ESPOLIOS_PROIBIDOS = ('torre negra',)
ESPOLIOS_LIMPOS = ('lanca do cavaleiro', 'armadura de um peao', 'armadura do peao',
                   'espada do peao', 'coroa da rainha')
FLAGS_DE_MALDICAO = ('amaldi', 'nodrop', 'no-drop', 'nao-largar', 'nao-doar')

# --- mochila de Pellinore: so' REDUZ PESO quando esta VESTIDA (par.68) ---
# Slot "sobre o corpo" (o mesmo do manto). Vestida, 4 lancas (72 kg) pesam ~6 kg;
# na mao, pesam cheio. `put` NAO enxerga a mochila vestida: tirar, guardar, vestir.
MOCHILA = 'mochila'
