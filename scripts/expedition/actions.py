from dataclasses import asdict
import re
import threading
from .models import Result, Status, Vitals, Supplies, PROFILES
from .observations import (norm, plain, PROMPT, rejection, saved, terminal_state, combat_signal,
                           fled, update_vitals, update_supplies, parse_room, named_exits, assess_consider)
from .policy import ResourcePolicy, WorldGraph, loot_decision


class NeedsAgent(RuntimeError):pass


class Context:
    def __init__(self,io,book,config,hero_state=None,map_data=None):
        self.io=io;self.book=book;self.config=config.validate();self.profile=PROFILES[config.mode]
        self.policy=ResourcePolicy(config);self.graph=WorldGraph();self.room=None
        self.vitals=Vitals();self.supplies=Supplies();self.in_combat=False
        self.peak_damage=0;self.step_cost=0;self.gross_mv_spent=0;self.commands=0
        self.moves=0;self.kills=[];self.started=io.now();self.prepared=False
        self.hero=hero_state or {};self.map_data=map_data or {'rooms':[]}
        self.journal=[];self.last_text='';self.closed=False
        self.lock=threading.RLock();self.guard=None;self.interrupted=False;self.terminal=False
        self.expected_combat=False;self.generation=0;self.carried=[]

    def consume(self,text,operational=True):
        previous=self.vitals.hp
        update_vitals(self.vitals,text,self.io.now());update_supplies(self.supplies,text)
        self.last_text=text
        if operational and terminal_state(text):
            self.terminal=True
            raise NeedsAgent('Morte, menu ou incapacidade detectada. Nenhuma sequência continuará.')
        if operational and combat_signal(text):self.in_combat=True
        if operational and fled(text):self.in_combat=False
        if previous is not None and self.vitals.hp is not None and self.vitals.hp<previous:
            self.peak_damage=max(self.peak_damage,previous-self.vitals.hp)
            if self.room:self.room.damage_seen=True
        if 'voce esta em pe.' in norm(text) and 'lutando' not in norm(text):self.in_combat=False

    def poll(self):
        with self.lock:
            text=self.io.poll()
            if text:self.record('unsolicited',response=text);self.consume(text)
            return text

    def record(self,event,**data):
        item={'at':self.io.now(),'event':event,**data};self.journal.append(item)
        self.io.record(item)

    def send(self,command,safety=False,guard=None):
        with self.lock:
            self.poll()
            if self.guard and not safety:self.guard.tick()
            if self.terminal:raise NeedsAgent('Estado terminal: não enviar comandos de jogo.')
            if self.interrupted and not safety:raise NeedsAgent('Vigilância interrompeu o plano; relocalizar e reavaliar antes de retomar.')
            if not self.io.connected:raise NeedsAgent('Conexão perdida; reconexão automática desativada.')
            if guard is not None and not guard():raise NeedsAgent('Condições mudaram imediatamente antes do comando.')
            try:self.book.validate_command(command)
            except ValueError as error:raise NeedsAgent(str(error)) from error
            limit=self.config.max_commands+(20 if safety else 0)
            if self.commands>=limit:raise NeedsAgent('Orçamento de comandos atingido.')
            self.commands+=1
            try:text=self.io.command(command)
            except (OSError,TimeoutError,ConnectionError) as error:
                raise NeedsAgent('Transporte interrompido ou resposta incompleta: '+str(error)) from error
            self.record('command',command=command,response=text)
            self.consume(text,operational=not command.startswith('help '))
            if command=='inventory':self.update_carried(text)
            if not text:raise NeedsAgent('Resposta ausente; não presumir êxito.')
            return text

    def update_carried(self,text):
        from .models import Item
        self.carried=[]
        for line in text.splitlines():
            for known in self.config.item_catalog:
                if known.get('pattern') and norm(known['pattern']) in norm(line):
                    values={k:v for k,v in known.items() if k in Item.__dataclass_fields__}
                    values['carried']=True
                    quantity=re.search(r'\(x(\d+)\)',line)
                    values['quantity']=int(quantity[1]) if quantity else 1
                    self.carried.append(Item(**values));break

    def fresh(self,safety=False):
        self.poll()
        if not self.vitals.fresh(self.io.now()):self.send('score tudo',safety=safety)
        if not self.vitals.fresh(self.io.now()):raise NeedsAgent('Atributos não puderam ser conferidos.')

    def annotate(self,room,expected_hint=None):
        matches=[r for r in self.map_data.get('rooms',[]) if norm(r['name'])==norm(room.title)]
        hint=next((r for r in matches if r['id']==expected_hint),None)
        if hint is None and len(matches)==1:hint=matches[0]
        if hint:
            room.hint_id=hint['id']
            room.city=hint.get('layer')=='superficie' and 'midgaard' in norm(hint.get('zone',''))
            if 'templo' in norm(hint.get('zone','')):room.city=True
        if room.title in self.config.outside_rooms:room.city=False
        room.known_shelter=room.title in self.config.verified_shelters

    def observe(self,origin=None,direction=None,expected_hint=None,safety=False):
        text=self.send('look',safety=safety)
        room=parse_room(text,self.config)
        if not room:raise NeedsAgent('Sala não reconhecida; resposta administrativa não vira localização.')
        self.annotate(room,expected_hint)
        if self.room and not origin and self.room.fingerprint==room.fingerprint:
            old=self.room;room.node_id=old.node_id;room.clean_checks=old.clean_checks
            room.damage_seen=old.damage_seen;self.graph.rooms[room.node_id]=room
        else:room=self.graph.arrive(room,origin,direction)
        self.room=room
        return room


class Observe:
    def execute(self,ctx):
        room=ctx.observe()
        return Result(Status.DONE,'Sala observada.',{'room':room.title,'entities':[asdict(e) for e in room.entities]})


class Localize:
    def execute(self,ctx):
        ctx.send('score tudo');room=ctx.observe()
        exits=ctx.send('exits')
        room.exits.update(named_exits(exits))
        return Result(Status.DONE,'Posição, saídas e condição atual conferidas.',{'room':room.title,'hint_id':room.hint_id})


class Scout:
    def execute(self,ctx,direction,safety=False):
        ctx.fresh(safety=safety);ctx.observe(safety=safety)
        if ctx.in_combat:return Result(Status.PAUSED,'Agressão antes do passo; não continuar marcha.')
        if direction not in ctx.room.exits:return Result(Status.REJECTED,'Saída não observada após olhar ao redor.')
        response=ctx.send('look '+Move.WORDS[direction],safety=safety)
        value=norm(response)
        if any(s in value for s in ('morte certa','abismo sem fundo','voce caira','porta esta fechada','porta esta trancada')):
            return Result(Status.PAUSED,'Olhar adiante revelou um obstáculo ou perigo a reavaliar.')
        visibility='partial' if not rejection(response) and not any(s in value for s in ('nada de especial','nao ve nada')) else 'unknown'
        ctx.record('scout',direction=direction,visibility=visibility,response=response,
                   note='Ausência de informação não comprova ausência de perigo.')
        return Result(Status.DONE,'Arredores e direção observados; reação continua ativa.',{'visibility':visibility})


class Move:
    WORDS={'n':'north','s':'south','e':'east','w':'west','u':'up','d':'down'}
    def execute(self,ctx,direction,expected_hint=None,safety=False,arrival='transit'):
        ctx.fresh(safety=safety)
        if ctx.in_combat:return Result(Status.PAUSED,'Movimento comum bloqueado em combate; resolver ou fugir.')
        if not ctx.room or direction not in ctx.room.exits:return Result(Status.REJECTED,'Saída não observada.')
        if ctx.vitals.mv<=max(ctx.profile.escape_mv,ctx.step_cost,ctx.config.max_step_cost) and not safety:
            return Result(Status.PAUSED,'Movimento invadiria a reserva de reação.')
        scout=Scout().execute(ctx,direction,safety=safety)
        if not scout.ok:return scout
        origin=ctx.room.node_id;before=ctx.vitals.mv
        generation=ctx.generation
        response=ctx.send(self.WORDS[direction],safety=safety,
                          guard=lambda:not ctx.in_combat and ctx.generation==generation)
        if rejection(response):return Result(Status.REJECTED,'Movimento recusado; rota não avançou.')
        if fled(response):
            ctx.room=None;ctx.generation+=1
            ctx.observe(safety=True)
            return Result(Status.FLED,'Fuga detectada; plano anterior invalidado.')
        room=ctx.observe(origin,direction,expected_hint,safety=safety)
        ctx.moves+=1
        cost=max(0,before-ctx.vitals.mv);ctx.gross_mv_spent+=cost;ctx.step_cost=max(ctx.step_cost,cost)
        ambient=Ambient().execute(ctx,arrival)
        if not ambient.ok:return ambient
        return Result(Status.DONE,'Chegada conferida.',{'room':room.title,'observed_net_cost':cost})


class Fight:
    """Same action with cautious/brave/avoid profiles; no blind fallback to a dagger."""
    def execute(self,ctx,entity):
        try:return self._execute(ctx,entity)
        finally:ctx.expected_combat=False

    def _execute(self,ctx,entity):
        if ctx.profile.combat=='evitar':return Result(Status.PAUSED,'Perfil batedor não inicia combate.')
        if entity.kind!='hostile' or not entity.verified or not re.fullmatch(r'[\w.-]+',entity.target):
            return Result(Status.PAUSED,'Alvo não identificado como hostil por evidência.')
        ctx.fresh()
        consideration=ctx.send('consider '+entity.target)
        verdict=assess_consider(consideration)
        ctx.record('consider',target=entity.target,verdict=verdict)
        if verdict!='favorable':return Result(Status.PAUSED,'Avaliação desfavorável, incompleta ou desconhecida: '+verdict)
        learned={s['id'] for s in ctx.hero.get('skills',[]) if s.get('proficiency',0)>0}
        if 'magic missile' not in learned:return Result(Status.PAUSED,'Míssil mágico não consta como aprendido pela personagem.')
        cast_budget=ctx.config.first_cast_budget
        for turn in range(ctx.config.max_combat_rounds):
            ctx.fresh()
            nearest=ctx.graph.nearest_camp(ctx.room.node_id)
            camp_cost=(nearest[0]*max(ctx.step_cost,ctx.config.max_step_cost)) if nearest else 0
            reserve=ctx.policy.reserves(ctx.vitals,ctx.peak_damage,ctx.step_cost,camp_cost)
            if not reserve:return Result(Status.PAUSED,'Recursos desconhecidos.')
            if ctx.vitals.hp<=reserve['hp'] or ctx.vitals.mv<=reserve['mv']:
                return self.retreat(ctx,'Reserva atingida durante a luta.') if ctx.in_combat else Result(Status.PAUSED,'Reserva insuficiente para abrir combate.')
            if ctx.vitals.mana<reserve['mana']+cast_budget:
                # Melee is optional and requires an explicit, measured enemy-hit budget.
                if ctx.config.allow_verified_melee and ctx.config.melee_max_enemy_hits is not None and ctx.peak_damage>0 and ctx.vitals.hp-reserve['hp']>ctx.peak_damage*ctx.config.melee_max_enemy_hits:
                    command='kill '+entity.target
                else:
                    return self.retreat(ctx,'Mana disponível não sustenta outro disparo com reserva.') if ctx.in_combat else Result(Status.PAUSED,'Mana insuficiente para começar.')
            else:command="cast 'magic missile' "+entity.target
            before=ctx.vitals.mana
            try:
                ctx.expected_combat=True
                response=ctx.send(command,guard=lambda:ctx.vitals.fresh(ctx.io.now()) and ctx.vitals.hp>reserve['hp'] and ctx.vitals.mv>reserve['mv'])
            except NeedsAgent:
                if ctx.terminal:raise
                if ctx.interrupted:return Result(Status.FLED,'A vigilância já interrompeu o combate e invalidou a rota.')
                return self.retreat(ctx,'Condição mudou antes do ataque.') if ctx.in_combat else Result(Status.PAUSED,'Condição mudou antes de abrir a luta.')
            ctx.record('combat_turn',turn=turn+1,target=entity.target,vitals=asdict(ctx.vitals),response=response)
            if fled(response):
                ctx.in_combat=False;ctx.room=None;ctx.generation+=1;ctx.observe(safety=True)
                return Result(Status.FLED,'Fuga automática observada; relocalização feita.')
            value=norm(response)
            target=norm(entity.target)
            death=bool(re.search(r'voce matou\b',value)) or any(target in line and re.search(r'esta mort[oa]|cai sem vida|morre[.!]',line) for line in value.splitlines())
            if death:
                ctx.in_combat=False;ctx.observe(safety=True)
                if any(e.target==entity.target for e in ctx.room.entities):return Result(Status.PAUSED,'Há outro alvo homônimo; não inferir fim do encontro.')
                ctx.kills.append(entity.target)
                return Result(Status.DONE,'Abate confirmado e sala reobservada.')
            if rejection(response):return self.retreat(ctx,'Ataque recusado.') if ctx.in_combat else Result(Status.REJECTED,'Ataque não executado; nenhuma vitória inferida.')
            ctx.in_combat=True
            cast_budget=max(cast_budget,before-ctx.vitals.mana)
        return self.retreat(ctx,'Limite de turnos sem desfecho comprovado.')

    def retreat(self,ctx,reason):
        if ctx.terminal:return Result(Status.PAUSED,'Estado terminal; não enviar fuga ao menu.')
        response=ctx.send('flee',safety=True)
        if not fled(response):return Result(Status.PAUSED,reason+' Fuga não confirmada; manter conexão e intervenção do agente.')
        ctx.in_combat=False;ctx.generation+=1;ctx.room=None;ctx.observe(safety=True)
        return Result(Status.FLED,reason+' Fuga confirmada e localização reobservada.')


class Recover:
    def execute(self,ctx):
        ctx.fresh()
        if ctx.in_combat or not ctx.room.quiet():return Result(Status.PAUSED,'Recuperação exige ausência de ameaça observada.')
        if ctx.supplies.hungry or ctx.supplies.thirsty:return Result(Status.PAUSED,'Tratar fome/sede antes de esperar recuperação.')
        start=ctx.io.now();before=ctx.vitals.hp
        command='rest' if ctx.vitals.hp<ctx.vitals.max_hp*.65 else 'sit'
        if rejection(ctx.send(command)):return Result(Status.REJECTED,'Postura de recuperação recusada.')
        while ctx.io.now()-start<ctx.config.recovery_seconds:
            ctx.io.wait(.2);ctx.poll()
            if ctx.interrupted:return Result(Status.PAUSED,'Vigilância interrompeu a recuperação; reavaliar na nova posição.')
            if ctx.in_combat or (ctx.vitals.hp is not None and ctx.vitals.hp<before):
                ctx.send('stand',safety=True)
                return Result(Status.PAUSED,'Dano ou combate interrompeu imediatamente a recuperação.')
            if not ctx.vitals.fresh(ctx.io.now()):ctx.send('score tudo',safety=True)
            if ctx.vitals.known() and ctx.vitals.hp>=ctx.vitals.max_hp*.8 and ctx.vitals.mana>=ctx.vitals.max_mana*.7 and ctx.vitals.mv>=ctx.vitals.max_mv*.7:
                ctx.send('stand',safety=True)
                return Result(Status.DONE,'Recuperação observada suficiente para reavaliar a próxima ação.')
        ctx.send('stand',safety=True)
        return Result(Status.PAUSED,'Recuperação terminou sem atingir o necessário; não retomar por timeout.')


class Loot:
    def execute(self,ctx,item,owned=0):
        decision,reason=loot_decision(item,ctx.supplies,ctx.config,owned)
        ctx.record('loot_decision',item=asdict(item),decision=decision,reason=reason)
        if decision=='inspect':
            if item.target:ctx.send('examine '+item.target)
            return Result(Status.DONE,'Item desconhecido ficou no local; observação registrada, sem inventar seus atributos.')
        if decision in ('keep','skip'):return Result(Status.DONE,reason)
        if not re.fullmatch(r'[\w.-]+',item.target):return Result(Status.PAUSED,'Alvo do item ambíguo; nenhuma coleta ou destruição.')
        command=('junk ' if decision=='burn' else 'get ')+item.target
        response=ctx.send(command)
        if rejection(response):return Result(Status.REJECTED,'Coleta/destruição recusada; inventário precisa ser conferido.')
        verb_confirmed=('voce pega','voce recolhe','voce apanha') if decision=='take' else ('voce joga fora','voce destroi','voce queima','voce transforma')
        if not any(v in norm(response) for v in verb_confirmed):return Result(Status.PAUSED,'Resposta não comprova a alteração do item.')
        ctx.send('inventory');ctx.send('score tudo')
        ctx.observe()
        return Result(Status.DONE,'Alteração de inventário comprovada e capacidade atualizada.')


class Ambient:
    def execute(self,ctx,variant='transit'):
        if ctx.in_combat:return Fight().retreat(ctx,'Ataque detectado na ambientação da chegada.')
        if variant=='transit':
            if any(e.kind!='friendly' or not e.verified for e in ctx.room.entities):
                return Result(Status.PAUSED,'Encontro durante o trânsito: avaliar passagem sem iniciar uma limpeza de sala.',{'entities':[asdict(e) for e in ctx.room.entities]})
            ctx.record('ambient_transit',room=ctx.room.title,entities=[asdict(e) for e in ctx.room.entities],
                       decision='Seguir o destino sem iniciar limpeza ou coleta oportunista.')
            return Result(Status.DONE,'Ambientação de trânsito concluída; ameaças reativas continuam monitoradas.')
        if variant=='observe':
            return Result(Status.DONE,'Observação de chegada concluída.')
        if variant!='clear':return Result(Status.PAUSED,'Variação de ambientação desconhecida.')
        for _ in range(ctx.config.max_room_encounters):
            unknown=[e for e in ctx.room.entities if e.kind in ('unknown','player') or not e.verified]
            if unknown:return Result(Status.PAUSED,'Ambientação encontrou entidade não classificada; agente deve inspecionar.',{'entities':[e.description for e in unknown]})
            hostile=next((e for e in ctx.room.entities if e.kind=='hostile'),None)
            if not hostile:break
            result=Fight().execute(ctx,hostile)
            if not result.ok:return result
        else:return Result(Status.PAUSED,'Novos encontros continuam aparecendo; reavaliar a sala antes de avançar.')
        if ctx.profile.loot:
            for item in list(ctx.carried):
                result=Loot().execute(ctx,item,owned=item.quantity)
                if not result.ok:return result
            for item in list(ctx.room.ground):
                owned=sum(i.quantity for i in ctx.carried if i.category=='weapon') if item.category=='weapon' else 0
                result=Loot().execute(ctx,item,owned=owned)
                if not result.ok:return result
                if any(e.kind!='friendly' or not e.verified for e in ctx.room.entities):
                    return Result(Status.PAUSED,'Presença mudou durante a coleta; refazer ambientação antes de avançar.')
        ctx.record('ambient_clear',room=ctx.room.title,decision='Ameaças resolvidas ou ausentes; espólios classificados antes de avançar.')
        return Result(Status.DONE,'Ambientação de exploração concluída.')


class Camp:
    def execute(self,ctx,nutrition_reason=False):
        if ctx.interrupted:return Result(Status.PAUSED,'Retomar após relocalização antes de escolher o repouso.')
        if ctx.in_combat:return Result(Status.PAUSED,'Não dormir em combate.')
        for _ in range(3):
            ctx.fresh(safety=True);room=ctx.observe(safety=True)
            if not room.quiet():return Result(Status.PAUSED,'Ameaça ou criatura desconhecida impede estabelecer repouso automático.')
            room.clean_checks+=1
            ctx.io.wait(.2);ctx.poll()
        nearest=ctx.graph.nearest_camp(ctx.room.node_id,nutrition_reason)
        if nearest is None:return Result(Status.PAUSED,'Nenhum repouso próximo adequado e alcançável foi comprovado; não voltar à cidade por outro motivo.')
        _,node,path=nearest
        for direction in path:
            result=Move().execute(ctx,direction,safety=True)
            if not result.ok:return result
        room=ctx.room
        if not room.suitable_camp():return Result(Status.PAUSED,'Condições do repouso mudaram ao chegar.')
        if room.city is True and not nutrition_reason:return Result(Status.PAUSED,'Retorno à cidade permitido apenas por necessidade de provisões.')
        # Closing doors is attempted only when an actual closed-door affordance was observed.
        if len(room.exits)==1 and 'porta' in norm(room.raw):
            direction=next(iter(room.exits))
            response=ctx.send('close '+Move.WORDS[direction],safety=True)
            if rejection(response):ctx.record('camp_door_unconfirmed',response=response)
        generation=ctx.generation
        unchanged=lambda:not ctx.in_combat and not ctx.interrupted and ctx.generation==generation
        response=ctx.send('save',safety=True,guard=unchanged)
        if not saved(response):return Result(Status.PAUSED,'Salvamento não confirmado; não declarar encerramento.')
        response=ctx.send('sleep',safety=True,guard=unchanged)
        if not any(s in norm(response) for s in ('voce se deita e dorme','voce dorme','voce ja esta dormindo')):
            return Result(Status.PAUSED,'Sono não confirmado; manter controle disponível.')
        ctx.record('camp_confirmed',room=room.title,node_id=room.node_id,certainty='Condições observadas, sem garantia de imunidade.',save_response='Resposta positiva registrada.')
        return Result(Status.CAMPED,'Sono e salvamento confirmados no repouso adequado mais próximo.',{'room':room.title})
