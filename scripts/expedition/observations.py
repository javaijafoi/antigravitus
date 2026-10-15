import hashlib
import re
import unicodedata
from .models import Entity, Item, Room

PROMPT = re.compile(r'(-?\d+)\s*hp\s+(-?\d+)\s*mn\s+(-?\d+)\s*mv\s*>', re.I)
DIRECTIONS = {'norte':'n','north':'n','sul':'s','south':'s','leste':'e','east':'e','oeste':'w','west':'w','cima':'u','up':'u','baixo':'d','down':'d'}
OPPOSITE = {'n':'s','s':'n','e':'w','w':'e','u':'d','d':'u'}


def norm(value):
    value = re.sub(r'\x1b\[[0-?]*[ -/]*[@-~]', '', value)
    return ''.join(c for c in unicodedata.normalize('NFKD', value) if not unicodedata.combining(c)).lower()


def plain(value):
    return re.sub(r'\x1b\[[0-?]*[ -/]*[@-~]', '', value).replace('\r','')


def rejection(text):
    value=norm(text)
    return any(s in value for s in ('como?!','nao pode ir por ai','nao esta vendo','nao ve nada','nao tem esse','muito ocupado, lutando','nao consegue','nao conseguiu','nao ha espaco','nao pode carregar','nao tem mais espaco','fechada','esta trancad','voce nao pode'))


def saved(text):
    value=norm(text)
    if any(s in value for s in ('nao','falh','erro','ocupado','lutando','impossivel')):
        return False
    return bool(re.search(r'(?:salvando os seus atalhos|\bjogo salvo\b|^\s*salvo\.)',value))


def terminal_state(text):
    value=norm(text)
    # A score saying "Você morreu 3 vezes" is historical, not a death notification.
    if re.search(r'voce (?:esta mort[oa]|morreu[.!]|foi mort[oa])|menu principal|faca a sua escolha|fonte da vida',value):
        return 'dead_or_menu'
    last=PROMPT.findall(value)
    if last and int(last[-1][0]) <= 0:
        return 'incapacitated'
    return ''


def combat_signal(text):
    value=norm(text)
    return bool(re.search(r'(?:te|voce) (?:atinge|acerta)|(?:atinge|acerta|ataca) voce|voce (?:atinge|acerta)|voce esta lutando|voce esta em combate|muito ocupado, lutando',value))


def fled(text):
    value=norm(text)
    if any(s in value for s in ('nao consegue fugir','nao conseguiu fugir','tenta fugir','tentou fugir')):return False
    return any(s in value for s in ('voce foge','voce escapa','fugiu para','foge em direcao'))


def update_vitals(vitals, text, now):
    matches=PROMPT.findall(text)
    if matches:
        vitals.hp,vitals.mana,vitals.mv=map(int,matches[-1])
        vitals.observed_at=now
    for label,attribute in (('Vida','hp'),('Mana','mana'),('Movimento','mv')):
        match=re.search(label+r':\s*(?:\{[^}]*\})?\s*(-?\d+)\s+de\s+(\d+)',text,re.I)
        if match:
            setattr(vitals,attribute,int(match[1]));setattr(vitals,'max_'+attribute,int(match[2]))
            if not matches: vitals.observed_at=now


def update_supplies(supplies,text):
    value=norm(text)
    if '[situacao atual]' in value:
        tail=value.split('[situacao atual]',1)[1]
        supplies.hungry='fome' in tail
        supplies.thirsty='sede' in tail
    if 'morrendo de fome' in value: supplies.hungry=True
    if 'morrendo de sede' in value: supplies.thirsty=True
    match=re.search(r'carregando:.*?\s(\d[\d.]*)\s*-\s*total:',value)
    if match: supplies.gold=int(match[1].replace('.',''))
    match=re.search(r'carregando (\d+) itens.*?total de ([\d.,]+) kg',value)
    if match: supplies.count=int(match[1]);supplies.weight=float(match[2].replace(',','.'))
    match=re.search(r'maximo (\d+) itens e um peso total de ([\d.,]+) kg',value)
    if match: supplies.max_count=int(match[1]);supplies.max_weight=float(match[2].replace(',','.'))
    if 'voce esta carregando:' in value:
        supplies.food=0
        for line in value.splitlines():
            if 'pao recheado' in line:
                qty=re.search(r'\(x(\d+)\)',line);supplies.food+=int(qty[1]) if qty else 1
    if 'voce comprou um pao recheado' in value: supplies.food+=1
    if 'voce come um pao recheado' in value:
        supplies.food=max(0,supplies.food-1);supplies.hungry=False
    if 'voce bebe agua' in value:
        supplies.thirsty=False
        if supplies.water is not None: supplies.water=max(0,supplies.water-.1)
    if 'voce enche um cantil' in value: supplies.water=1.0
    elif 'cantil' in value or 'agua' in value:
        if 'esta vazio' in value or 'esta vazia' in value: supplies.water=0.0
        elif 'quase cheio' in value: supplies.water=.8
        elif re.search(r'\bcheio\b',value) and 'agua' in value: supplies.water=1.0
        elif 'metade' in value and 'agua' in value: supplies.water=.5


def parse_room(text,config):
    text=plain(text)
    if not re.search(r'\[\s*Sa[ií]das\s*:',text,re.I): return None
    clean=PROMPT.sub('',text)
    raw_lines=[s for s in clean.splitlines() if s.strip()]
    # A room title directly precedes its indented description. Discard tips and
    # unsolicited messages before it instead of including them in room identity.
    exits_at=next(i for i,s in enumerate(raw_lines) if re.search(r'\[\s*Sa[ií]das\s*:',s,re.I))
    starts=[i for i,s in enumerate(raw_lines[:max(0,exits_at-1)]) if not s[0].isspace() and raw_lines[i+1][0].isspace() and not s.strip().startswith('[')]
    if starts:raw_lines=raw_lines[starts[-1]:]
    lines=[s.strip() for s in raw_lines]
    exit_index=next(i for i,s in enumerate(lines) if re.search(r'\[\s*Sa[ií]das\s*:',s,re.I))
    candidates=[s for s in lines[:exit_index] if len(s)<85 and not norm(s).startswith(('voce ','dica:','>>>','salvando','como','certo','uma carroca'))]
    if not candidates: return None
    title=candidates[0]
    exit_text=norm(lines[exit_index])
    exits={code:'' for word,code in DIRECTIONS.items() if re.search(r'\b'+word+r'\b',exit_text)}
    entities=[];ground=[]
    for line in lines[exit_index+1:]:
        value=norm(line)
        if value.startswith(('dica:','voce ')):continue
        if any(s in value for s in ('foi deixad','foi abandonad','esta jogad')):
            known=next((item for item in config.item_catalog if norm(item.get('pattern','')) and norm(item['pattern']) in value),None)
            if known:
                allowed={k:v for k,v in known.items() if k in Item.__dataclass_fields__}
                ground.append(Item(**allowed))
            else: ground.append(Item('',line))
        elif re.search(r'esta aqui|esta andando|zanza|rastej|espreita|esta procurando|esta chorando|esta gritando',value):
            match=next((e for e in config.known_entities if any(norm(p) in value for p in e.get('patterns',[]))),None)
            if match: entities.append(Entity(line,match.get('target',''),match.get('kind','unknown'),bool(match.get('verified'))))
            elif any(s in value for s in ('foi deixad','uma caixa','um aviso','uma fonte')):continue
            else: entities.append(Entity(line))
        elif line and not re.fullmatch(r'[\s\-_=]+',line):
            # An unrecognized presence is not proof of an empty room.
            entities.append(Entity(line))
    body='\n'.join(lines[:exit_index+1])
    fingerprint=hashlib.sha256(norm(body).encode()).hexdigest()[:20]
    return Room(title,fingerprint,exits,entities,ground,text)


def named_exits(text):
    result={}
    for line in plain(text).splitlines():
        match=re.match(r'\s*(Norte|Sul|Leste|Oeste|Cima|Baixo)\s*-\s*(.+)',line,re.I)
        if match:result[DIRECTIONS[norm(match[1])]]=match[2].strip()
    return result


def assess_consider(text):
    value=norm(text)
    if rejection(text): return 'unknown'
    if any(s in value for s in ('louco','suicid','mataria','menor chance','muito superior','sem chance')):return 'danger'
    if any(s in value for s in ('sorte','dificil','arriscad')):return 'risky'
    axes=re.findall(r'(?im)^\s*(?:nivel|vida|poder|precisao|armadura):\s*\d+\s+(.+)',value)
    if len(axes)<3:return 'unknown'
    green=('perfeito','perda de tempo','facil','moleza','mais fraco','sem dificuldade','sem problema')
    return 'favorable' if all(any(token in axis for token in green) for axis in axes) else 'unknown'
