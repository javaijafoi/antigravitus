import threading
from .actions import Fight, NeedsAgent


class ReactionGuard:
    """Idle-time watchdog. A shared lock gives a single owner to all game commands."""
    def __init__(self,context,interval=.1):
        self.ctx=context;self.interval=interval;self.stop_event=threading.Event();self.thread=None
        self.handled=False

    def tick(self):
        ctx=self.ctx
        if not ctx.io.connected:return
        with ctx.lock:
            try:
                ctx.poll()
                if self.handled:return
                reserve=ctx.policy.reserves(ctx.vitals,ctx.peak_damage,ctx.step_cost)
                urgent=ctx.in_combat and (not ctx.expected_combat or (reserve and ctx.vitals.hp<=reserve['hp']))
                if not urgent:return
                self.handled=True;ctx.interrupted=True
                ctx.record('guardian_interrupt',reason='Agressão inesperada ou reserva crítica; prioridade de reação.')
                result=Fight().retreat(ctx,'Interrupção de fundo')
                ctx.record('guardian_result',status=result.status.value,reason=result.reason)
            except NeedsAgent as error:
                self.handled=True;ctx.interrupted=True
                ctx.record('guardian_pause',reason=str(error))

    def _run(self):
        while not self.stop_event.wait(self.interval):self.tick()

    def start(self):
        if self.thread:return
        self.ctx.guard=self
        self.thread=threading.Thread(target=self._run,name='expedition-guardian',daemon=True)
        self.thread.start()

    def resume(self):
        with self.ctx.lock:
            self.ctx.fresh(safety=True)
            if self.ctx.terminal or self.ctx.in_combat:raise NeedsAgent('Não retomar plano em estado terminal ou combate.')
            self.ctx.interrupted=False;self.handled=False

    def stop(self):
        self.stop_event.set()
        if self.thread:self.thread.join(timeout=1)
