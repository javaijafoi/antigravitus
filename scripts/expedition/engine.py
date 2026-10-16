from collections import deque
import re
from .actions import Context, Observe, Localize, Ambient, Move, Fight, Recover, Loot, Camp, NeedsAgent
from .models import Result, Status
from .observations import norm, rejection


class Travel:
    """Point A to B: route hints never authorize a blind sequence of steps."""
    def execute(self,ctx,target_id,reason='destino'):
        return self.travel_to(ctx,lambda room:room.get('id')==target_id,reason)

    def travel_to(self,ctx,predicate,reason='comida_agua'):
        hints={room['id']:room for room in ctx.map_data.get('rooms',[])}
        if not ctx.room or ctx.room.hint_id not in hints:return Result(Status.PAUSED,'Localização ambígua; relocalizar antes de traçar uma rota.')
        start=ctx.room.hint_id;queue=deque([(start,[])]);seen={start};route=None
        translations={'l':'e','o':'w','c':'u','b':'d'}
        while queue:
            node,path=queue.popleft()
            if predicate(hints[node]):route=path;break
            for raw,target in hints[node].get('exits',{}).items():
                if target in hints and target not in seen:
                    seen.add(target);queue.append((target,path+[(translations.get(raw,raw),target)]))
        if route is None:return Result(Status.PAUSED,'Rota desconhecida; não completar lacunas do mapa por suposição.')
        outside=ctx.room.city is False
        for _,target in route:
            city=hints[target].get('layer')=='superficie' and ('midgaard' in norm(hints[target].get('zone','')) or 'templo' in norm(hints[target].get('zone','')))
            if outside and city and reason!='comida_agua':return Result(Status.PAUSED,'Rota voltaria à cidade sem necessidade de provisões.')
            outside=outside or not city
        ctx.record('transit_route',reason=reason,hint_edges=len(route))
        for direction,target in route:
            result=Move().execute(ctx,direction,expected_hint=target,arrival='transit')
            if not result.ok:return result
            if norm(ctx.room.title)!=norm(hints[target]['name']):
                return Result(Status.PAUSED,'Destino diverge do roteiro; rota cancelada antes do próximo passo.')
        return Result(Status.DONE,'Chegada ao destino conferida por etapas.')


class Prepare(Travel):
    """Provision first. Historical map edges are hints, checked after every actual step."""
    def execute(self,ctx):
        ctx.send('score tudo');ctx.send('inventory');ctx.send('equipment');ctx.observe()
        if 'cantil' not in norm(ctx.last_text):
            # last_text is the look reply, so inspect the complete inventory separately.
            inventory=ctx.send('inventory')
            if 'cantil' not in norm(inventory):return Result(Status.PAUSED,'Preparação exige recipiente de água; aquisição não será inventada.')
        water=ctx.send('look in cantil')
        if ctx.supplies.hungry and ctx.supplies.food:
            if rejection(ctx.send('eat pao')):return Result(Status.PAUSED,'Alimentação recusada.')
        if ctx.supplies.thirsty and ctx.supplies.water and ctx.supplies.water>0:
            if rejection(ctx.send('drink cantil')):return Result(Status.PAUSED,'Hidratação recusada.')
        needs_food=ctx.supplies.food<ctx.config.food_floor
        # Ir buscar agua so' quando o cantil ACABOU. O piso de .75 e' exigencia
        # de PARTIDA (ver a conferencia no fim), nao gatilho de retorno: com
        # meio cantil a resposta e' beber, nao atravessar a cidade.
        needs_water=ctx.supplies.water is None or ctx.supplies.water<=ctx.config.water_floor
        if needs_water:
            result=self.travel_to(ctx,lambda room:room.get('id')=='praca_templo')
            if not result.ok:return result
            if 'fonte' not in norm(ctx.room.raw):return Result(Status.PAUSED,'Fonte não observada ao chegar; não presumir recurso disponível.')
            if rejection(ctx.send('fill cantil fonte')) or ctx.supplies.water!=1.0:
                return Result(Status.PAUSED,'Recarga de água não confirmada.')
            if ctx.supplies.thirsty and rejection(ctx.send('drink cantil')):return Result(Status.PAUSED,'Água não consumida.')
        if needs_food:
            result=self.travel_to(ctx,lambda room:room.get('id')=='padaria')
            if not result.ok:return result
            listing=ctx.send('list')
            found=re.search(r'pao recheado\s+(\d+)',norm(listing))
            if not found:return Result(Status.PAUSED,'Preço do pão não foi confirmado na lista atual.')
            price=int(found[1])
            if price>ctx.config.food_price_ceiling:return Result(Status.PAUSED,'Preço acima do orçamento de provisões.')
            for _ in range(ctx.config.food_target+1):
                if ctx.supplies.food>=ctx.config.food_target:break
                ctx.send('score tudo')
                s=ctx.supplies
                if s.gold is None or s.gold<price:return Result(Status.PAUSED,'Moedas insuficientes ou saldo desconhecido.')
                if None in (s.count,s.max_count,s.weight,s.max_weight) or s.count>=s.max_count-ctx.config.spare_slots or s.weight+1>s.max_weight:
                    return Result(Status.PAUSED,'Não há espaço conferido para a preparação; organizar itens antes de partir.')
                before=s.food
                response=ctx.send('buy pao')
                if rejection(response) or s.food<=before:return Result(Status.PAUSED,'Compra não confirmada; não repetir cegamente.')
            if ctx.supplies.hungry:
                if rejection(ctx.send('eat pao')):return Result(Status.PAUSED,'Consumo recusado.')
                # Keep the travel stock after feeding, not before it.
                if ctx.supplies.food<ctx.config.food_target:
                    ctx.send('score tudo')
                    s=ctx.supplies
                    if None in (s.gold,s.count,s.max_count,s.weight,s.max_weight) or s.gold<price or s.count>=s.max_count-ctx.config.spare_slots or s.weight+1>s.max_weight:
                        return Result(Status.PAUSED,'Reposição após comer exige saldo e capacidade novamente conferidos.')
                    if rejection(ctx.send('buy pao')):return Result(Status.PAUSED,'Reposição após comer não confirmada.')
        ctx.send('inventory');ctx.send('score tudo')
        if ctx.supplies.food<ctx.config.food_target or ctx.supplies.water is None or ctx.supplies.water<.75 or ctx.supplies.hungry is not False or ctx.supplies.thirsty is not False:
            return Result(Status.PAUSED,'Preparação incompleta; não iniciar marcha prolongada.')
        ctx.prepared=True
        ctx.record('prepared',food=ctx.supplies.food,water=ctx.supplies.water)
        return Result(Status.DONE,'Alimentação, água e capacidade conferidas antes da expedição.')

class Expedition:
    def __init__(self,context):self.ctx=context;self.attempted=set();self.no_progress=0;self.last_recovery=None;self.deployed=False

    def run(self):
        ctx=self.ctx
        try:
            if not ctx.prepared:
                localized=Localize().execute(ctx)
                if not localized.ok:return localized
                result=Prepare().execute(ctx)
                if not result.ok:return result
            ctx.observe()
            if not self.deployed:
                if ctx.config.destination_id:
                    result=Travel().execute(ctx,ctx.config.destination_id,reason='expedicao')
                    if not result.ok:return result
                elif ctx.room.city is True:return Result(Status.PAUSED,'Preparação concluída na cidade; indicar destino da expedição antes de partir.')
                self.deployed=True
            while ctx.commands<ctx.config.max_commands and ctx.io.now()-ctx.started<ctx.config.max_seconds:
                ctx.fresh()
                # Hunger/thirst alone authorize a provisioning trip to town.
                if ctx.supplies.hungry or ctx.supplies.thirsty or ctx.supplies.food==0 or ctx.supplies.water==0:
                    return_hint=ctx.room.hint_id
                    ctx.prepared=False
                    result=Prepare().execute(ctx)
                    if not result.ok:return result
                    if ctx.room.city is True:
                        if not return_hint:return Result(Status.PAUSED,'Provisões repostas; localização anterior não individualizada. Orientar retorno à frente de exploração.')
                        result=Travel().execute(ctx,return_hint,reason='retomar_expedicao')
                        if not result.ok:return result
                    continue
                nearest=ctx.graph.nearest_camp(ctx.room.node_id)
                cost=nearest[0]*max(ctx.step_cost,ctx.config.max_step_cost) if nearest else 0
                useful,reason=ctx.policy.can_work(ctx.vitals,ctx.io.now(),ctx.peak_damage,ctx.step_cost,cost)
                if not useful:
                    marker=(ctx.room.node_id,ctx.moves,len(ctx.kills))
                    if marker!=self.last_recovery:
                        self.last_recovery=marker
                        result=Recover().execute(ctx)
                        if result.ok:continue
                    ctx.record('work_stopped',reason=reason)
                    return Camp().execute(ctx)
                if ctx.in_combat:return Fight().retreat(ctx,'Agressão inesperada antes da próxima ação.')
                ambient=Ambient().execute(ctx,'clear')
                if not ambient.ok:
                    # Se encontrou bicho risky/danger e há sala anterior observada, recua e faz contorno sem parar a expedição!
                    if ('Avaliação desfavorável' in ambient.detail or 'entidade não classificada' in ambient.detail) and ctx.graph.previous and ctx.graph.previous[1]==ctx.room.node_id:
                        origin_id,risky_id,back_dir=ctx.graph.previous
                        ctx.graph.avoided_nodes.add(risky_id)
                        for d in ctx.room.exits:
                            self.attempted.add((risky_id,d))
                        ctx.record('detour_risky_room',avoided_node=risky_id,room=ctx.room.title,back_dir=back_dir)
                        back_res=Move().execute(ctx,back_dir,safety=True,arrival='observe')
                        if back_res.ok:
                            continue
                    return ambient
                # Survey potential near-frontline shelters without ending the day early.
                if ctx.room.quiet() and (ctx.room.known_shelter or len(ctx.room.exits)<=1):
                    for _ in range(max(0,3-ctx.room.clean_checks)):
                        ctx.io.wait(.2);ctx.observe();ctx.room.clean_checks+=1
                        if not ctx.room.quiet():return Result(Status.PAUSED,'Condições mudaram durante observação do repouso.')
                for d in ctx.room.exits:
                    target=ctx.graph.edges.get((ctx.room.node_id,d))
                    if target and ctx.graph.rooms[target].city is True:self.attempted.add((ctx.room.node_id,d))
                    hint=next((r for r in ctx.map_data.get('rooms',[]) if r['id']==ctx.room.hint_id),{})
                    hinted=hint.get('exits',{}).get({'e':'l','w':'o'}.get(d,d),hint.get('exits',{}).get(d))
                    other=next((r for r in ctx.map_data.get('rooms',[]) if r['id']==hinted),{})
                    if ctx.room.city is False and other.get('layer')=='superficie' and ('midgaard' in norm(other.get('zone','')) or 'templo' in norm(other.get('zone',''))):self.attempted.add((ctx.room.node_id,d))
                direction=next((d for d in ctx.room.exits if (ctx.room.node_id,d) not in self.attempted and (ctx.room.node_id,d) not in ctx.graph.avoided_edges),None)
                if direction is None:
                    frontier=self.frontier_path()
                    if not frontier:return Camp().execute(ctx)
                    direction=frontier[0]
                key=(ctx.room.node_id,direction);self.attempted.add(key)
                result=Move().execute(ctx,direction,arrival='observe')
                if result.status==Status.REJECTED:
                    self.no_progress+=1
                    ctx.observe()
                    if self.no_progress>=ctx.config.max_no_progress:return Result(Status.PAUSED,'Tentativas sem avanço atingiram o limite; rever rota.')
                    continue
                if not result.ok:return result
                self.no_progress=0
            ctx.record('work_stopped',reason='Limite de duração/comandos; não foi imposto gasto inútil de recursos.')
            return Camp().execute(ctx)
        except NeedsAgent as error:
            return Result(Status.PAUSED,str(error))

    def frontier_path(self):
        ctx=self.ctx;candidates=[]
        for node,room in ctx.graph.rooms.items():
            if node in ctx.graph.avoided_nodes:continue
            if any((node,direction) not in self.attempted and (node,direction) not in ctx.graph.avoided_edges for direction in room.exits):
                path=ctx.graph.path(ctx.room.node_id,node)
                if path:candidates.append(path)
        return min(candidates,key=len,default=None)


class HorizonExpander:
    """Modo Expandir Horizontes: transita rápido em salas conhecidas e cataloga profundamente salas inéditas em BFS/DFS dinâmico, contornando bichos risky/danger sem parar a expedição até atingir a reserva real de MV."""
    DETAIL_KEYWORDS = ('palavras','figura','parede','inscricao','placa','estatua','garrafa','altar','tabuleiro','portao','aviso','buraco','fenda')
    STOPWORDS = {'um','uma','os','as','esta','aqui','andando','por','olhando','para','voce','com','de','da','do','no','na','em','busca','desafios','segue','velho','apressado','pequeno','grande','muito','parece','coisa','assustadora'}
    OPPOSITE = {'n':'s','s':'n','e':'w','w':'e','u':'d','d':'u'}

    def __init__(self,ctx,min_mv=25):
        self.ctx=ctx
        self.min_mv=min_mv
        self.cataloged_rooms=[]
        self.cataloged_details=[]
        self.cataloged_entities=[]
        self.cataloged_fingerprints=set()
        self.attempted_edges=set()
        self.danger_edges=set()

    def dynamic_mv_reserve(self):
        ctx=self.ctx
        nearest=ctx.graph.nearest_camp(ctx.room.node_id,True) if ctx.room else None
        camp_steps=nearest[0] if nearest else 6
        step_cost=max(ctx.step_cost,1)
        return max(self.min_mv,camp_steps*step_cost+ctx.profile.escape_mv)

    def is_known_room(self,room):
        if room.fingerprint in self.cataloged_fingerprints:
            return True
        if room.hint_id:
            hint=next((r for r in self.ctx.map_data.get('rooms',[]) if r.get('id')==room.hint_id),None)
            if hint and not hint.get('unresolved_exits'):
                return True
        return False

    def catalog_current_room(self,tag='',came_from_dir=None,origin_node=None):
        ctx=self.ctx
        room=ctx.observe()
        self.cataloged_fingerprints.add(room.fingerprint)
        exits_txt=ctx.send('exits')
        from .observations import named_exits,plain,assess_consider
        ex_map=named_exits(exits_txt)
        for d,dest_name in ex_map.items():
            if d in room.exits:
                room.exits[d]=dest_name
        entry={
            'tag':tag or room.node_id,
            'title':room.title,
            'exits':dict(ex_map),
            'raw_description':plain(room.raw).strip(),
            'entities':[e.description for e in room.entities],
            'ground':[g.name for g in room.ground],
        }
        self.cataloged_rooms.append(entry)
        desc_norm=norm(room.raw)
        for kw in self.DETAIL_KEYWORDS:
            if kw in desc_norm:
                res=ctx.send(f'look {kw}')
                if not rejection(res):
                    self.cataloged_details.append({'room':room.title,'keyword':kw,'response':plain(res).strip()})
        for ent in list(room.entities):
            target=ent.target
            if not target:
                words=[w for w in re.findall(r'[a-z]+',norm(ent.description)) if len(w)>2 and w not in self.STOPWORDS]
                target=words[-1] if words else ''
            if target:
                l_res=ctx.send(f'look {target}')
                c_res=ctx.send(f'consider {target}')
                verdict=assess_consider(c_res)
                self.cataloged_entities.append({
                    'room':room.title,
                    'description':ent.description,
                    'target':target,
                    'look':plain(l_res).strip(),
                    'consider':plain(c_res).strip(),
                    'verdict':verdict,
                })
                if verdict in ('danger','risky') and ent.kind!='friendly':
                    # Marca o nó e a aresta para contorno (sem parar a expedição!) e recua para continuar por outras rotas
                    ctx.graph.avoided_nodes.add(room.node_id)
                    if origin_node and came_from_dir:
                        self.danger_edges.add((origin_node,came_from_dir))
                        ctx.graph.avoided_edges.add((origin_node,came_from_dir))
                    for d in room.exits:
                        self.attempted_edges.add((room.node_id,d))
                    ctx.record('horizon_detour',room=room.title,target=target,verdict=verdict)
                    if came_from_dir and self.OPPOSITE.get(came_from_dir) in room.exits:
                        Move().execute(ctx,self.OPPOSITE[came_from_dir],safety=True,arrival='observe')
                    return room,ex_map
                if ent.kind=='hostile' and ent.verified and verdict=='favorable':
                    Fight().execute(ctx,ent)
        ctx.record('horizon_catalog',room=room.title,exits=ex_map,details=len(self.cataloged_details),entities=len(self.cataloged_entities))
        return room,ex_map

    def next_frontier_path(self):
        ctx=self.ctx
        candidates=[]
        for node,room in ctx.graph.rooms.items():
            if node in ctx.graph.avoided_nodes:
                continue
            for d in room.exits:
                if (node,d) not in self.attempted_edges and (node,d) not in self.danger_edges:
                    if node==ctx.room.node_id:
                        return [d]
                    path=ctx.graph.path(ctx.room.node_id,node)
                    if path:
                        candidates.append(path+[d])
        return min(candidates,key=len,default=None)

    def execute(self,directions=()):
        ctx=self.ctx
        ctx.fresh()
        if not self.is_known_room(ctx.room):
            self.catalog_current_room('start')
        else:
            self.cataloged_fingerprints.add(ctx.room.fingerprint)

        queue=list(directions)
        while ctx.commands<ctx.config.max_commands and ctx.io.now()-ctx.started<ctx.config.max_seconds:
            ctx.fresh()
            if (ctx.vitals.mv or 0)<=self.dynamic_mv_reserve() or ctx.in_combat:
                break
            if not queue:
                path=self.next_frontier_path()
                if not path:
                    break
                queue=list(path)
            d=queue.pop(0)
            origin=ctx.room.node_id
            self.attempted_edges.add((origin,d))
            target_node=ctx.graph.edges.get((origin,d))
            target_known=bool(target_node and self.is_known_room(ctx.graph.rooms[target_node]))
            res=Move().execute(ctx,d,arrival='transit' if target_known else 'observe')
            if not res.ok:
                queue.clear()
                continue
            if not self.is_known_room(ctx.room):
                self.catalog_current_room(f'step_{d}',came_from_dir=d,origin_node=origin)
                if ctx.room.node_id==origin:
                    # Recuou de bicho risky/danger: limpa a fila atual para recalcular contorno (next_frontier_path)
                    queue.clear()
        return Result(Status.DONE,'Horizontes expandidos e catalogados até o limite de segurança.',{
            'rooms':self.cataloged_rooms,
            'details':self.cataloged_details,
            'entities':self.cataloged_entities,
        })



