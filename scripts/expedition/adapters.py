import json
from pathlib import Path
import re
import time
from .observations import PROMPT


class ReplayTransport:
    """Deterministic transport; no imports or calls capable of opening a socket."""
    def __init__(self,steps):self.steps=list(steps);self.sent=[];self.connected=True;self.clock=0.;self.records=[];self.incoming=[]
    def now(self):return self.clock
    def wait(self,seconds):self.clock+=seconds
    def poll(self):return self.incoming.pop(0) if self.incoming else ''
    def command(self,command):
        self.sent.append(command);self.clock+=.1
        if not self.steps:raise AssertionError('Replay esgotado para '+command)
        expected=self.steps.pop(0)
        if expected['command']!=command:raise AssertionError(f"Esperado {expected['command']!r}; recebido {command!r}")
        return expected['response']
    def record(self,item):self.records.append(item)
    def close(self):self.connected=False


class LiveTransport:
    """One reader (DeboClient) and prompt-delimited replies; no fixed turn sleeps."""
    def __init__(self,client,log_path,timeout=6):
        self.client=client;self.path=Path(log_path);self.timeout=timeout;self.closed=False
        self.path.parent.mkdir(parents=True,exist_ok=True)
        self.file=self.path.open('x',encoding='utf-8')
    @property
    def connected(self):return not self.closed and self.client.sock is not None and self.client.sock.fileno()>=0 and self.client._reader_running
    def now(self):return time.monotonic()
    def wait(self,seconds):time.sleep(min(seconds,.2))
    def poll(self):return self.client.recv_chunk() if self.connected else ''
    def command(self,command):
        if not self.connected:return ''
        # Existing background thread owns recv; only send is performed here.
        self.client.sock.sendall((command+'\n').encode('latin-1'))
        start=self.now();text='';quiet_since=start;pager_closed=False
        while self.now()-start<self.timeout:
            chunk=self.poll()
            if chunk:text+=chunk;quiet_since=self.now()
            if PROMPT.search(text) and self.now()-quiet_since>=.15:return text
            if not pager_closed and 'aperte enter para continuar' in text.lower():
                self.client.sock.sendall(b's\n');pager_closed=True
            self.wait(.05)
            if not self.connected:break
        self.record({'event':'transport_incomplete','command':command,'response':text})
        raise TimeoutError('Resposta sem prompt completo; interromper e reavaliar, sem presumir efeito.')
    def record(self,item):
        # Logs never contain authentication commands or the environment credential.
        safe=self.client.sanitize_log(json.dumps(item,ensure_ascii=False))
        self.file.write(safe+'\n');self.file.flush()
    def close(self):
        if self.closed:return
        try:self.client.close()
        finally:self.closed=True;self.file.close()
