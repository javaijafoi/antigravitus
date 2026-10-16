# -*- coding: utf-8 -*-
"""
debo_bot.py - Cliente de conexão Telnet e automação para o Devil's Bob MUD (CircleMUD 3.x).

Arquitetura Milestones M1/M2:
- Context manager (__enter__ / __exit__) e encerramento seguro à prova de vazamentos (close).
- Thread daemon assíncrona contínua (_reader_thread) para recepção ininterrupta de stream.
- Desfragmentador Telnet IAC em nível de bytes com acumulação entre fronteiras de pacotes TCP.
- Reconstrução de caracteres multi-byte UTF-8 e preservação de prompts fatiados.
- Rastreamento dinâmico de vitais assinados (-30hp) e classificação de estados (in_game, in_combat, etc.).
- Detecção espontânea de ameaças (mobs agressivos) mesmo com o cliente ocioso.
- Sanitização rigorosa de credenciais (sanitize_log) para prevenir vazamento de senhas em logs e console.
"""

import socket
import time
import sys
import unicodedata
import re
import os
import json
import errno
import threading
from collections import deque
from typing import Optional, Dict, Any, List, Tuple

# Garantir saída UTF-8 no Windows
if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass
if sys.stderr.encoding != 'utf-8':
    try:
        sys.stderr.reconfigure(encoding='utf-8')
    except Exception:
        pass

from parsers import (
    strip_accents,
    parse_room as parse_room_pure,
    parse_vitals as parse_vitals_pure,
    parse_supplies as parse_supplies_pure,
    parse_exits as parse_exits_pure,
    detect_rejection as detect_rejection_pure,
    classify_game_state,
    verify_save_confirmation,
    detect_combat_target_absence,
    DIRECTION_OPPOSITES
)

DEFAULT_CREDENTIALS: List[str] = []  # Sem segredo embutido: a senha vem de MUD_PASS ou scripts/local/.mud_pass.

# Linhas de ficha/score. Elas NUNCA sao evento de combate, mas enganavam a
# leitura em dois pontos do rastreio de estado: os medidores '{<<<<<>>>>>}'
# contam como gatilho '>>' e 'Voce morreu 7 vezes' conta como terminador de
# combate. Como o historico vem ANTES dos medidores, todo 'score' era lido
# como combate em andamento.
_ROTULO_SCORE = re.compile(
    r'^\s*(?:vida|mana|movimento|experiencia|proximo nivel|alinhamento|banco|carregando'
    r'|forca|sabedoria|destreza|constituicao|inteligencia|carisma|acerto|dano'
    r'|classe de armadura|pontos de aventura)\s*:')
_MORREU_HISTORICO = re.compile(r'voce\s+morreu\s+\d+\s+vezes')


def sem_score(texto: str) -> str:
    """Remove as linhas de ficha, que nao descrevem combate."""
    if not texto:
        return ""
    manter = []
    for linha in texto.splitlines():
        limpa = strip_accents(linha.lower())
        if _ROTULO_SCORE.match(limpa) or _MORREU_HISTORICO.search(limpa):
            continue
        manter.append(linha)
    return '\n'.join(manter)


def sanitize_log(text: str, extra_passwords=None) -> str:
    """
    Sanitiza strings de log, stdout e histórico para garantir que credenciais nunca vazem.
    Substitui ocorrências de senhas reais, MUD_PASS e fallback padrão ('169933715') por '***REDACTED***'.
    """
    if not text:
        return ""
    targets = set(DEFAULT_CREDENTIALS)
    env_pass = os.environ.get("MUD_PASS")
    if env_pass:
        targets.add(env_pass)
    if extra_passwords:
        for p in extra_passwords:
            if p:
                targets.add(p)

    # Ordenar por tamanho decrescente para substituir substrings mais longas primeiro
    for target in sorted(targets, key=len, reverse=True):
        if target:
            text = text.replace(target, "***REDACTED***")
    return text


class DeboClient:
    """
    Cliente Telnet de alta confiabilidade para Devil's Bob MUD.
    Suporta recepção contínua em background, lifecycle seguro e conformidade Zero-Network.
    """

    def __init__(self, host: str = "debomud.org", port: int = 4000, log_path: Optional[str] = None, password: Optional[str] = None):
        self.host = host
        self.port = port
        self.password = password or os.environ.get("MUD_PASS")
        self.sock: Optional[socket.socket] = None
        self.log_history: List[str] = []
        self.log_path = log_path
        self.log_file = None
        if log_path:
            try:
                self.log_file = open(log_path, "a", encoding="utf-8")
            except Exception:
                self.log_file = None

        # Vitais e estados da personagem
        self.hp: Optional[int] = None
        self.mana: Optional[int] = None
        self.mv: Optional[int] = None
        self.vitals: Dict[str, Optional[int]] = {"hp": None, "mana": None, "mv": None}
        # Fome e sede NAO sao vitais de combate, mas decidem provisao: sem elas o
        # daemon nao tinha como saber que a personagem estava morrendo de fome.
        self.supplies: Dict[str, Optional[bool]] = {"fome": None, "sede": None}
        self.current_state: str = "disconnected"
        self.in_combat: bool = False

        # Navegação, salas e histórico de affordance
        self.last_room_info: Optional[Dict[str, Any]] = None
        self.last_move: Optional[str] = None
        self.last_rejection: Optional[Dict[str, Any]] = None
        self.rejection_history: List[Dict[str, Any]] = []

        # Sincronização de threads e desfragmentação de buffers
        self._lock = threading.RLock()
        self._reader_thread: Optional[threading.Thread] = None
        self._reader_running: bool = False
        self._incoming_queue: deque = deque()
        self._iac_buffer: bytearray = bytearray()
        self._decode_residual: bytes = b""
        self._text_accumulator: str = ""

    # Protocolo Context Manager
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
        return False

    def sanitize_log(self, text: str) -> str:
        """Sanitiza texto com conhecimento da senha desta instância."""
        extras = []
        if getattr(self, "password", None):
            extras.append(self.password)
        return sanitize_log(text, extra_passwords=extras)

    def connect(self):
        """Estabelece conexão TCP com o servidor MUD e dispara a thread receptora contínua."""
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.settimeout(25)
        self.sock.connect((self.host, self.port))
        self.current_state = "in_game"
        self.start_reader()

    def close(self):
        """
        Rotina unificada e à prova de falhas de encerramento da conexão e liberação de recursos.
        Garante que socket, thread de recepção e descritores de arquivos abertos sejam
        completamente finalizados sem vazamento sob qualquer circunstância (EOF, exceção ou saída normal).
        """
        try:
            self.stop_reader()
        except Exception:
            pass

        try:
            if self.log_file and not getattr(self.log_file, "closed", True):
                try:
                    self.log_file.flush()
                except Exception:
                    pass
                try:
                    self.log_file.close()
                except Exception:
                    pass
                self.log_file = None
        except Exception:
            pass

        if self.sock:
            try:
                try:
                    self.sock.shutdown(socket.SHUT_RDWR)
                except Exception:
                    pass
                try:
                    self.sock.close()
                except Exception:
                    pass
            finally:
                self.sock = None
                self.current_state = "disconnected"
                self.in_combat = False

    def start_reader(self):
        """Inicia a thread contínua de recepção em segundo plano se houver socket ativo."""
        with self._lock:
            if self._reader_running and self._reader_thread and self._reader_thread.is_alive():
                return
            if not self.sock:
                return
            self._reader_running = True
            self._reader_thread = threading.Thread(
                target=self._reader_loop,
                name="DeboClient-ReaderThread",
                daemon=True
            )
            self._reader_thread.start()

    # Alias conforme PROJECT.md
    start_receiver_thread = start_reader

    def stop_reader(self):
        """Para a thread de recepção e aguarda sua conclusão limpa."""
        self._reader_running = False
        thread = self._reader_thread
        if thread and thread.is_alive():
            if threading.current_thread() != thread:
                thread.join(timeout=1.0)
        self._reader_thread = None

    # Alias conforme PROJECT.md
    stop_receiver_thread = stop_reader

    def _reader_loop(self):
        """Loop contínuo de background para leitura assíncrona do socket."""
        while self._reader_running:
            sock = self.sock
            if not sock:
                break

            data = None
            try:
                orig_timeout = None
                try:
                    orig_timeout = sock.gettimeout()
                except Exception:
                    pass

                try:
                    if orig_timeout is None or orig_timeout > 0.5:
                        sock.settimeout(0.2)
                    data = sock.recv(4096)
                finally:
                    if orig_timeout is not None:
                        try:
                            sock.settimeout(orig_timeout)
                        except Exception:
                            pass
            except (socket.timeout, TimeoutError):
                continue
            except (BlockingIOError, InterruptedError):
                time.sleep(0.02)
                continue
            except (ConnectionResetError, BrokenPipeError, ConnectionAbortedError):
                with self._lock:
                    self.current_state = "disconnected"
                    self.in_combat = False
                break
            except OSError as e:
                if getattr(e, "winerror", None) == 10054 or getattr(e, "errno", None) in (errno.ECONNRESET, errno.EBADF):
                    with self._lock:
                        self.current_state = "disconnected"
                        self.in_combat = False
                    break
                break
            except Exception:
                break

            if data is None:
                continue

            if data == b"":
                # Em MockSocket sem trigger_eof, recv retorna b"" quando a fila está vazia
                is_mock = hasattr(sock, "_chunk_queue")
                if is_mock and not getattr(sock, "_eof", False):
                    time.sleep(0.02)
                    continue

                # EOF real ou trigger_eof ativo
                with self._lock:
                    self.current_state = "disconnected"
                    self.in_combat = False
                break

            self._process_incoming_bytes(data)

    def _process_telnet_bytes(self, new_bytes: bytes) -> bytes:
        """
        Máquina de estados para desfragmentação e limpeza de sequências Telnet IAC (0xFF ...).
        Acumula bytes parciais através de fronteiras de pacotes TCP para não vazar 0xFF ou corromper o texto.
        """
        self._iac_buffer += new_bytes
        cleaned = bytearray()
        i = 0
        buf_len = len(self._iac_buffer)

        while i < buf_len:
            b = self._iac_buffer[i]
            if b == 0xFF:
                # Precisa de pelo menos 2 bytes para determinar comando IAC
                if i + 1 >= buf_len:
                    break
                cmd = self._iac_buffer[i + 1]
                if cmd == 0xFF:
                    # IAC escapado (0xFF 0xFF) -> literal 0xFF
                    cleaned.append(0xFF)
                    i += 2
                elif cmd in (0xFB, 0xFC, 0xFD, 0xFE):  # WILL, WONT, DO, DONT
                    if i + 2 >= buf_len:
                        break
                    i += 3
                elif cmd == 0xFA:  # SB (Subnegotiation)
                    se_pos = self._iac_buffer.find(b"\xff\xf0", i + 2)
                    if se_pos == -1:
                        break
                    i = se_pos + 2
                else:
                    i += 2
            else:
                cleaned.append(b)
                i += 1

        self._iac_buffer = self._iac_buffer[i:]
        return bytes(cleaned)

    def _decode_bytes(self, clean_bytes: bytes) -> str:
        """
        Decodifica bytes limpos para string acumulando caracteres multi-byte UTF-8 divididos entre chunks.
        Fallback transparente para Latin-1 com preservação de caracteres acentuados do CircleMUD.
        """
        raw = self._decode_residual + clean_bytes
        self._decode_residual = b""

        try:
            return raw.decode('utf-8')
        except UnicodeDecodeError as e:
            if e.end == len(raw) and e.start < len(raw):
                self._decode_residual = raw[e.start:]
                try:
                    return raw[:e.start].decode('utf-8')
                except UnicodeDecodeError:
                    pass
            return raw.decode('latin-1', errors='replace')

    def _process_incoming_bytes(self, raw_bytes: bytes) -> str:
        """Processa bytes brutos recebidos, atualiza vitais, estado de jogo e enfileira."""
        with self._lock:
            clean_bytes = self._process_telnet_bytes(raw_bytes)
            if not clean_bytes:
                return ""

            text = self._decode_bytes(clean_bytes)
            if not text:
                return ""

            # Acumulador textual para remontagem de palavras e prompts fatiados
            self._text_accumulator += text
            if len(self._text_accumulator) > 8192:
                self._text_accumulator = self._text_accumulator[-2048:]

            # Atualizar vitais a partir do acumulador recente e do chunk
            v = parse_vitals_pure(self._text_accumulator)
            if v and (v.get("hp") is not None or v.get("mana") is not None or v.get("mv") is not None):
                if v.get("hp") is not None:
                    self.hp = v["hp"]
                    self.vitals["hp"] = v["hp"]
                if v.get("mana") is not None:
                    self.mana = v["mana"]
                    self.vitals["mana"] = v["mana"]
                if v.get("mv") is not None:
                    self.mv = v["mv"]
                    self.vitals["mv"] = v["mv"]

            # Fome e sede, do mesmo acumulador: o bloco '[Situacao atual]' manda.
            s = parse_supplies_pure(self._text_accumulator)
            if s.get("fome") is not None:
                self.supplies["fome"] = s["fome"]
            if s.get("sede") is not None:
                self.supplies["sede"] = s["sede"]

            # Atualizar estado operacional dinamicamente (incluindo emboscadas espontâneas e combate)
            is_conn = bool(self.sock and getattr(self.sock, "connected", True) and not getattr(self.sock, "closed", False))
            recent_window = self._text_accumulator[-2000:] if len(self._text_accumulator) > 2000 else self._text_accumulator
            raw_state = classify_game_state(self.vitals, recent_window, is_connected=is_conn)
            if raw_state != "in_combat":
                chunk_state = classify_game_state(self.vitals, text, is_connected=is_conn)
                if chunk_state == "in_combat":
                    raw_state = "in_combat"

            if not is_conn:
                self.current_state = "disconnected"
                self.in_combat = False
            elif raw_state in ("dead_or_menu", "incapacitated"):
                self.current_state = raw_state
                self.in_combat = False
            else:
                norm_recent = strip_accents(sem_score(recent_window).lower())
                terminator_patterns = [
                    "esta morto", "esta morta", "caiu morto", "caiu morta",
                    "morreu", "voce matou", "pontos de experiencia",
                    "entra em panico e tenta fugir", "voce foge", "foge em direcao", "fugiu para", "voce escapa"
                ]
                last_term_pos = -1
                for pat in terminator_patterns:
                    pos = norm_recent.rfind(pat)
                    if pos > last_term_pos:
                        last_term_pos = pos

                if last_term_pos != -1:
                    trigger_patterns = [
                        "ataca voce", "acerta voce", "arrebenta voce", "massacra voce",
                        "golpeia", "tenta acertar", "erra voce", "muito ocupado, lutando",
                        "voce arrebenta", "voce massacra", "voce acerta", "voce golpeia",
                        "voce desfere", "seu missil magico"
                    ]
                    last_trig_pos = -1
                    for pat in trigger_patterns:
                        pos = norm_recent.rfind(pat)
                        if pos > last_trig_pos:
                            last_trig_pos = pos

                    if last_term_pos > last_trig_pos:
                        self.in_combat = False
                        hp = self.vitals.get("hp")
                        if hp is not None and hp > 0:
                            self.current_state = "in_game"
                        else:
                            self.current_state = raw_state
                    else:
                        self.in_combat = True
                        self.current_state = "in_combat"
                else:
                    # Sem terminador no buffer recente. O flag segue o que o
                    # accumulador mostra AGORA; antes havia 'or self.in_combat',
                    # que transformava o flag numa catraca: ligava uma vez e
                    # nunca mais desligava ate cair a conexao.
                    if raw_state == "in_combat":
                        self.in_combat = True
                        self.current_state = "in_combat"
                    else:
                        self.current_state = raw_state
                        self.in_combat = False

            # Sanitizar credenciais para log e saída pública
            sanitized = self.sanitize_log(text)
            self.log_history.append(sanitized)

            if self.log_file and not getattr(self.log_file, "closed", True):
                try:
                    self.log_file.write(sanitized)
                    self.log_file.flush()
                except Exception:
                    pass

            try:
                sys.stdout.write(sanitized)
                sys.stdout.flush()
            except Exception:
                pass

            self._incoming_queue.append(sanitized)
            return sanitized

    def recv_chunk(self) -> str:
        """
        Retorna o próximo bloco de texto recebido.
        Se a thread de segundo plano estiver ativa, drena a fila assíncrona.
        Caso contrário, realiza a leitura pontual direta do socket.
        """
        if self._reader_running and self._reader_thread and self._reader_thread.is_alive():
            chunks = []
            with self._lock:
                while self._incoming_queue:
                    chunks.append(self._incoming_queue.popleft())
            return "".join(chunks)

        return self._recv_chunk_direct()

    def _recv_chunk_direct(self) -> str:
        """Leitura pontual direta do socket quando a thread de background não está ativa."""
        if not self.sock:
            return ""

        data = b""
        is_mock = hasattr(self.sock, "_chunk_queue")
        try:
            if is_mock:
                try:
                    c = self.sock.recv(4096)
                    if c:
                        data += c
                except BlockingIOError:
                    pass
            else:
                self.sock.setblocking(False)
                try:
                    while True:
                        c = self.sock.recv(4096)
                        if not c:
                            break
                        data += c
                finally:
                    try:
                        self.sock.setblocking(True)
                    except Exception:
                        pass
        except (BlockingIOError, socket.timeout):
            pass
        except (ConnectionResetError, BrokenPipeError, ConnectionAbortedError):
            with self._lock:
                self.current_state = "disconnected"
                self.in_combat = False
            return ""
        except OSError as e:
            if getattr(e, "winerror", None) == 10054 or getattr(e, "errno", None) in (errno.ECONNRESET, errno.EBADF):
                with self._lock:
                    self.current_state = "disconnected"
                    self.in_combat = False
                return ""
            return ""
        except Exception:
            return ""

        if not data:
            return ""

        return self._process_incoming_bytes(data)

    def wait_for(self, targets: List[str], timeout: float = 12.0) -> str:
        """
        Aguarda até que uma das strings alvos apareça no fluxo do socket ou ocorra timeout.
        """
        start = time.time()
        buf = ""
        while time.time() - start < timeout:
            chunk = self.recv_chunk()
            if chunk:
                buf += chunk
                norm_buf = strip_accents(buf.lower())
                for t in targets:
                    if strip_accents(t.lower()) in norm_buf:
                        return buf
            time.sleep(0.05)
        return buf

    def send(self, cmd: str, wait_sec: float = 1.2) -> str:
        """
        Envia um comando para o servidor MUD, sanitizando saídas e gerenciando pagers.
        """
        norm_cmd = cmd.strip().lower()
        if norm_cmd in ["n", "s", "e", "w", "u", "d", "norte", "sul", "leste", "oeste", "cima", "baixo"]:
            self.last_move = norm_cmd

        sanitized_cmd = self.sanitize_log(cmd)
        sys.stdout.write(f"\n>>> SEND: {sanitized_cmd}\n")
        sys.stdout.flush()

        if self.sock:
            try:
                self.sock.sendall((cmd + "\n").encode('latin-1'))
            except (ConnectionResetError, BrokenPipeError, OSError):
                with self._lock:
                    self.current_state = "disconnected"
                    self.in_combat = False
                return ""

        if wait_sec > 0:
            time.sleep(wait_sec)

        res = self.recv_chunk()

        # Rastrear recusas de comando automaticamente
        rej = detect_rejection_pure(res)
        if rej.get("is_rejected"):
            self.last_rejection = rej
            self.rejection_history.append({
                "cmd": cmd,
                "reason": rej.get("reason"),
                "message": rej.get("message")
            })

        # Se entrar em pager de mural/quadro, dispensar automaticamente com 's'
        if "para paginar" in res.lower() or "aperte enter para continuar" in res.lower():
            sys.stdout.write("\n[PAGER DETECTADO]: Enviando 's' para sair do leitor de quadro...\n")
            sys.stdout.flush()
            if self.sock:
                try:
                    self.sock.sendall(b"s\n")
                except Exception:
                    pass
            time.sleep(0.5)
            res += self.recv_chunk()

        return res

    def send_prompt(self, cmd: str, timeout: float = 8.0, quiet: float = 0.18) -> Dict[str, Any]:
        """
        Envia um comando e só retorna quando o prompt de vitais reaparece E o fluxo
        silencia por `quiet` segundos. Correlaciona a resposta ao seu comando, dispensa
        pagers e sinaliza timeout em vez de devolver texto pertencente a outro comando.
        """
        prompt_re = re.compile(r'(-?\d+)\s*hp\s+(-?\d+)\s*mn\s+(-?\d+)\s*mv\s*>', re.I)
        if not self.sock:
            return {"cmd": cmd, "text": "", "prompt": False, "timeout": False, "disconnected": True}
        try:
            self.sock.sendall((cmd + "\n").encode("latin-1"))
        except (ConnectionResetError, BrokenPipeError, OSError):
            with self._lock:
                self.current_state = "disconnected"
                self.in_combat = False
            return {"cmd": cmd, "text": "", "prompt": False, "timeout": False, "disconnected": True}
        start = time.monotonic()
        last_data = start
        text = ""
        pager_sent = False
        while time.monotonic() - start < timeout:
            chunk = self.recv_chunk()
            now = time.monotonic()
            if chunk:
                text += chunk
                last_data = now
            low = text.lower()
            if not pager_sent and ("aperte enter para continuar" in low or "para paginar" in low):
                try:
                    self.sock.sendall(b"s\n")
                except Exception:
                    pass
                pager_sent = True
            match = prompt_re.search(text)
            if match and now - last_data >= quiet:
                return {
                    "cmd": cmd, "text": text, "prompt": True, "timeout": False,
                    "vitals": {"hp": int(match.group(1)), "mana": int(match.group(2)), "mv": int(match.group(3))},
                    "in_combat": bool(self.in_combat), "state": self.current_state,
                    "supplies": dict(self.supplies),
                }
            time.sleep(0.04)
        return {
            "cmd": cmd, "text": text, "prompt": False, "timeout": True,
            "vitals": dict(self.vitals), "in_combat": bool(self.in_combat), "state": self.current_state,
            "supplies": dict(self.supplies),
        }

    def login(self, username: str = "Grebolius", password: Optional[str] = None, wimpy: int = 30):
        """
        Executa a sequência canônica de autenticação no CircleMUD sem expor senhas.
        """
        if password is None:
            password = self.password or os.environ.get("MUD_PASS")
        if not password:
            raise ValueError("Credencial ausente: defina MUD_PASS antes de conectar.")

        self.password = password

        self.wait_for(["nome", "personagem", "qual o seu nome"])
        if self.sock:
            self.sock.sendall((username + "\n").encode('latin-1'))
        self.wait_for(["senha", "password"])
        if self.sock:
            self.sock.sendall((password + "\n").encode('latin-1'))

        res = self.wait_for(["pressione enter", "escolha", "reconectando", "hp"], 8)
        norm_res = strip_accents(res.lower())
        if "pressione enter" in norm_res:
            if self.sock:
                self.sock.sendall(b"\n")
            res2 = self.wait_for(["escolha", "menu", "hp"], 8)
            norm_res2 = strip_accents(res2.lower())
            if "escolha" in norm_res2 or "menu" in norm_res2:
                if self.sock:
                    self.sock.sendall(b"1\n")
                self.wait_for(["hp", ">"], 8)
        elif "escolha" in norm_res or "menu" in norm_res:
            if self.sock:
                self.sock.sendall(b"1\n")
            self.wait_for(["hp", ">"], 8)

        self.send_prompt("", timeout=3.0)
        self.send_prompt("wake", timeout=3.0)
        self.send_prompt("stand", timeout=3.0)
        if wimpy:
            self.send_prompt(f"wimpy {wimpy}", timeout=3.0)

    def parse_room(self, text: str) -> Dict[str, Any]:
        """
        Analisa o texto retornado pelo comando look/movimento e separa:
        - title: nome da sala
        - exits: dicionário {direção: destino}
        - exit_directions: lista de direções ['norte', 'oeste', ...]
        - exit_codes: códigos telnet ['n', 'w', ...]
        - live_mobs: criaturas vivas
        - ground_items: itens no chão
        - raw: texto original
        """
        room_info = parse_room_pure(text)
        if room_info.get("title"):
            self.last_room_info = room_info
        return room_info

    def check_anomaly(self, room_info: Dict[str, Any], allowed_mobs: Optional[List[str]] = None) -> List[str]:
        """
        Retorna lista de anomalias encontradas na sala:
        - Mobs que não estejam na whitelist (allowed_mobs)
        - Presença de criaturas não previstas
        """
        if allowed_mobs is None:
            allowed_mobs = []

        anomalies = []
        for mob in room_info.get("live_mobs", []):
            norm_mob = strip_accents(mob.lower())
            is_allowed = False
            for allowed in allowed_mobs:
                if strip_accents(allowed.lower()) in norm_mob:
                    is_allowed = True
                    break
            if not is_allowed:
                anomalies.append(mob)
        return anomalies

    def interactive_loop(self, reason: str = "Anomalia detectada") -> bool:
        """
        Mantém a conexão viva sem desconectar e permite que o agente envie comandos
        improvisados em tempo real até normalizar a situação.
        Digite 'resume' para voltar ao script planejado, ou 'done' para encerrar com save/rest.
        """
        sys.stdout.write(f"\n[ALERTA PAUSA TÁTICA]: {reason}\n")
        sys.stdout.write("Aguardando comando do agente ('resume' para continuar rota, 'done' para salvar e fechar):\n")
        sys.stdout.flush()

        while True:
            try:
                line = sys.stdin.readline()
                if not line:
                    break
                cmd = line.strip()
                if not cmd:
                    continue
                if cmd.lower() == "resume":
                    sys.stdout.write("\n>>> Retomando fluxo planejado...\n")
                    sys.stdout.flush()
                    break
                if cmd.lower() in ("done", "exit", "quit"):
                    sys.stdout.write("\n>>> Salvando e encerrando com segurança...\n")
                    self.send("stand", 0.8)
                    save_res = self.send("save", 1.2)
                    if verify_save_confirmation(save_res):
                        sys.stdout.write("\n[SAVE CONFIRMADO]: Jogo salvo com sucesso pelo servidor.\n")
                        self.send("rest", 1.0)
                    else:
                        sys.stdout.write(f"\n[ALERTA SAVE NÃO CONFIRMADO]: Resposta do servidor não confirmou salvamento: {save_res}\n")
                    sys.stdout.flush()
                    return False
                self.send(cmd, 1.2)
            except Exception as e:
                sys.stdout.write(f"\nErro no loop interativo: {e}\n")
                sys.stdout.flush()
                break
        return True

    def check_resource_budget(self, min_mv: int = 25, min_hp: int = 35, min_mana: int = 40) -> Tuple[bool, str]:
        """
        Avalia o orçamento de autonomia da expedição:
        - Se vitais ou HP forem desconhecidos (None), bloqueia avanço automático.
        - Avançar enquanto MV > min_mv (usando estamina ativamente)
        - Retornar se HP <= min_hp, Mana <= min_mana ou MV <= min_mv
        Retorna (pode_avancar: bool, motivo: str)
        """
        eff_hp = self.hp if self.hp is not None else (self.vitals.get("hp") if self.vitals else None)
        if eff_hp is None:
            return False, "Vitais desconhecidos: avanço automático bloqueado"
        if eff_hp <= min_hp:
            return False, f"HP em nível de alerta tático ({eff_hp} <= {min_hp})"

        eff_mana = self.mana if self.mana is not None else (self.vitals.get("mana") if self.vitals else None)
        if eff_mana is not None and eff_mana <= min_mana:
            return False, f"Mana em nível de reserva para defesa/fuga ({eff_mana} <= {min_mana})"

        eff_mv = self.mv if self.mv is not None else (self.vitals.get("mv") if self.vitals else None)
        if eff_mv is not None and eff_mv <= min_mv:
            return False, f"Estamina consumida até a margem de retorno seguro ({eff_mv} <= {min_mv})"

        return True, "Recursos adequados para continuar explorando"

    def safe_save(self) -> bool:
        """
        Executa salvamento seguro com postura adequada (stand) e validação de confirmação textual canônica.
        """
        self.send("stand", 0.6)
        res = self.send("save", 1.2)
        return verify_save_confirmation(res)

    def get_last_state(self) -> str:
        """Retorna o estado operacional classificado mais recente da personagem."""
        return self.current_state

    @staticmethod
    def get_opposite_dir(direction: str) -> Optional[str]:
        if not direction:
            return None
        norm = strip_accents(direction.strip().lower())
        return DIRECTION_OPPOSITES.get(norm, None)

    def export_rejections_jsonl(self, filepath: str):
        """Exporta o histórico de recusas (Affordance QA) para arquivo JSONL."""
        with open(filepath, "w", encoding="utf-8") as f:
            for item in self.rejection_history:
                f.write(json.dumps(item, ensure_ascii=False) + "\n")

    def tactical_rest(self, target_hp: int = 45, target_mana: int = 100, max_seconds: float = 35.0) -> bool:
        """
        Executa uma pausa tática de repouso em sala limpa para regenerar HP e Mana.
        Rejeita descanso se estiver em combate ativo.
        """
        if self.current_state == "in_combat":
            sys.stdout.write("\n[ALERTA TÁTICO]: Impossível descansar em combate ativo!\n")
            sys.stdout.flush()
            return False

        sys.stdout.write(f"\n[PAUSA TÁTICA DE RECUPERAÇÃO: HP={self.hp}, Mana={self.mana}]\n")
        sys.stdout.flush()
        self.send("rest", 1.0)
        start = time.time()
        while time.time() - start < max_seconds:
            self.send("", 3.0)  # pulso para captar prompt e vitais atualizados
            if (self.hp is not None and self.hp >= target_hp) and (self.mana is not None and self.mana >= target_mana):
                sys.stdout.write("\n[RECUPERAÇÃO CONCLUÍDA]: HP e Mana restaurados. Levantando e retomando marcha!\n")
                sys.stdout.flush()
                break
        self.send("stand", 1.0)
        return True


__all__ = [
    "DeboClient",
    "sanitize_log",
    "strip_accents",
    "parse_room_pure",
    "parse_vitals_pure",
    "parse_exits_pure",
    "detect_rejection_pure",
    "classify_game_state",
    "verify_save_confirmation",
    "detect_combat_target_absence",
    "DIRECTION_OPPOSITES",
    "DEFAULT_CREDENTIALS"
]
