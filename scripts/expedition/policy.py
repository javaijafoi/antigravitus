import math
from .models import PROFILES


class ResourcePolicy:
    def __init__(self,config):self.config=config;self.profile=PROFILES[config.mode]

    def reserves(self,vitals,peak_damage=0,observed_step_cost=0,camp_cost=0):
        if not vitals.known():return None
        hit=max(peak_damage,math.ceil(vitals.max_hp*.15))
        hp=max(math.ceil(vitals.max_hp*self.profile.hp_fraction),math.ceil(hit*self.profile.damage_turns))
        step=max(self.config.max_step_cost,observed_step_cost)
        mv=max(self.profile.escape_mv,3*step)+camp_cost
        return {'hp':hp,'mana':self.profile.mana_reserve,'mv':mv,'hit':hit}

    def can_work(self,vitals,now,peak_damage=0,observed_step_cost=0,camp_cost=0):
        if not vitals.fresh(now):return False,'Atributos ausentes ou antigos.'
        reserve=self.reserves(vitals,peak_damage,observed_step_cost,camp_cost)
        if vitals.hp<=reserve['hp']:return False,'Reserva para sobreviver a novos golpes atingida.'
        if vitals.mv<=reserve['mv']:return False,'Reserva para fuga e repouso próximo atingida.'
        if self.profile.combat!='evitar' and vitals.mana<=reserve['mana']:return False,'Reserva de defesa atingida.'
        return True,'Há recursos para trabalho útil.'


def loot_decision(item,supplies,config,owned=0):
    if not item.verified:return 'inspect','Item desconhecido: examinar, sem recolher nem destruir por suposição.'
    if not item.carried:
        if None in (supplies.weight,supplies.max_weight,supplies.count,supplies.max_count):return 'skip','Capacidade desconhecida.'
        if item.weight is None or supplies.weight+item.weight*item.quantity>supplies.max_weight or supplies.count+item.quantity>supplies.max_count-config.spare_slots:
            return 'skip','Item não cabe com a reserva para provisões; registrar sua localização.'
    protected=item.quest or item.rare or item.category in ('food','water','tool','quest','recall','potion') or item.upgrade
    if protected:return ('keep' if item.carried else 'take'),'Utilidade comprovada; preservar.'
    if item.category=='weapon' and ((item.carried and owned<=config.spare_weapons) or (not item.carried and owned<config.spare_weapons)):
        return ('keep' if item.carried else 'take'),'Reserva de arma dentro do limite.'
    if item.disposable and item.contents_known and config.burn_verified_trash:
        return ('burn' if item.carried else 'skip'),'Descarte autorizado somente de lixo conhecido já carregado.'
    if item.carried:return 'keep','Sem motivo comprovado para destruir.'
    if item.weight is None or item.sale_value is None:return 'skip','Valor de venda ou peso desconhecido.'
    if item.sale_value/max(item.weight,.1)<config.min_loot_value_per_weight:return 'skip','Baixo retorno por peso.'
    if None in (supplies.weight,supplies.max_weight,supplies.count,supplies.max_count):return 'skip','Capacidade desconhecida.'
    if supplies.weight+item.weight*item.quantity>supplies.max_weight or supplies.count+item.quantity>supplies.max_count-config.spare_slots:
        return 'skip','Preservar mobilidade e espaço para provisões.'
    return 'take','Valor e capacidade conferidos.'


class WorldGraph:
    """Directed observed edges. Repeated room names are never a global identity."""
    def __init__(self):self.rooms={};self.edges={};self.previous=None;self.avoided_nodes=set();self.avoided_edges=set()

    def arrive(self,room,origin=None,direction=None):
        candidate=self.edges.get((origin,direction)) if origin and direction else None
        if candidate and self.rooms[candidate].fingerprint!=room.fingerprint:candidate=None
        if self.previous and origin==self.previous[1] and direction==self.previous[2] and self.rooms[self.previous[0]].fingerprint==room.fingerprint:
            candidate=self.previous[0]
        if not candidate:candidate=f'room-{len(self.rooms)+1}'
        room.node_id=candidate
        old=self.rooms.get(candidate)
        if old:
            room.clean_checks=old.clean_checks;room.damage_seen=old.damage_seen
        self.rooms[candidate]=room
        if origin and direction:
            self.edges[(origin,direction)]=candidate
            from .observations import OPPOSITE
            self.previous=(origin,candidate,OPPOSITE[direction])
        return room

    def observe_room(self,room):
        if room and room.node_id:self.rooms[room.node_id]=room

    def link(self,origin,direction,dest):
        if origin and direction and dest:self.edges[(origin,direction)]=dest

    def mark_avoid_node(self,node):
        if node:self.avoided_nodes.add(node)

    def mark_avoid_edge(self,origin,direction):
        if origin and direction:self.avoided_edges.add((origin,direction))

    def path(self,start,target,avoid_nodes=None,avoid_edges=None):
        avoid_n=self.avoided_nodes if avoid_nodes is None else avoid_nodes
        avoid_e=self.avoided_edges if avoid_edges is None else avoid_edges
        queue=[(start,[])];seen={start}
        for node,path in queue:
            if node==target:return path
            for (source,direction),dest in self.edges.items():
                if source==node and (source,direction) not in avoid_e and dest not in avoid_n and dest not in seen:
                    seen.add(dest);queue.append((dest,path+[direction]))
        return None

    def nearest_camp(self,start,nutrition_reason=False):
        candidates=[]
        for node,room in self.rooms.items():
            if not room.suitable_camp():continue
            if room.city is True and not nutrition_reason:continue
            if room.city is None:continue
            path=self.path(start,node)
            if path is not None:candidates.append((len(path),node,path))
        return min(candidates,default=None,key=lambda item:(item[0],item[1]))
