#!/usr/bin/env python3
"""Preview by default. Live game execution requires --live and MUD_PASS."""
import argparse
from dataclasses import asdict
from datetime import datetime
import importlib.util
import json
import os
from pathlib import Path
import sys
import uuid

for stream in (sys.stdout,sys.stderr):
    if hasattr(stream,'reconfigure'):stream.reconfigure(encoding='utf-8',errors='replace')

from expedition.actions import Context, Observe, Fight, Camp, NeedsAgent
from expedition.adapters import LiveTransport, ReplayTransport
from expedition.engine import Expedition, Travel
from expedition.knowledge import CommandBook
from expedition.models import Config, PROFILES, Status
from expedition.guardian import ReactionGuard

ROOT=Path(__file__).resolve().parent.parent


def json_read(path,default):
    return json.loads(path.read_text(encoding='utf-8-sig')) if path.is_file() else default


def dictionary_path():
    full=ROOT/'maquina/dicionario_comandos.md'
    return full if full.is_file() and CommandBook(full).has('look') else ROOT/'docs/expedicao_comandos.md'


def live_transport(root,hero,day,output):
    credential=os.environ.get('MUD_PASS')
    if not credential:raise ValueError('Configure MUD_PASS; nenhuma procura de senhas em arquivos será feita.')
    local=root/'scripts/local'
    if not (local/'debo_bot.py').is_file():raise ValueError('Cliente Telnet local ausente.')
    sys.path.insert(0,str(local))
    from debo_bot import DeboClient
    profile=json_read(root/f'data/heroes/{hero}/state.json',{}).get('wimpy',17)

    class ProfileClient(DeboClient):
        def send(self,command,wait_sec=1.2):
            return super().send(f'wimpy {profile}' if command=='wimpy 13' else command,wait_sec)

    client=ProfileClient(password=credential)
    try:
        client.connect()  # One attempt. There is no automatic reconnect.
        client.login(hero.capitalize(),password=credential)
        return LiveTransport(client,output)
    except BaseException:
        client.close();raise


def main(argv=None):
    parser=argparse.ArgumentParser(description='Expedição modular V2; não joga por padrão.')
    parser.add_argument('--hero',default='grebolius')
    parser.add_argument('--day',type=int)
    parser.add_argument('--mode',choices=PROFILES)
    parser.add_argument('--config',type=Path)
    parser.add_argument('--destination',help='ID de destino no mapa, seguido por exploração sala a sala.')
    parser.add_argument('--dictionary',type=Path)
    parser.add_argument('--max-commands',type=int)
    group=parser.add_mutually_exclusive_group()
    group.add_argument('--live',action='store_true')
    group.add_argument('--replay',type=Path)
    group.add_argument('--dry-run',action='store_true')
    args=parser.parse_args(argv)
    if not __import__('re').fullmatch(r'[a-z0-9][a-z0-9_-]*',args.hero):parser.error('Identificador de personagem inválido.')
    config_values=json_read(args.config,{}) if args.config else {}
    config_values['mode']=args.mode or config_values.get('mode','dungeon_corajoso')
    if args.destination:config_values['destination_id']=args.destination
    if args.max_commands is not None:config_values['max_commands']=args.max_commands
    config=Config(**config_values).validate()
    args.mode=config.mode
    state=json_read(ROOT/f'data/heroes/{args.hero}/state.json',{})
    map_data=json_read(ROOT/f'data/heroes/{args.hero}/mapa.json',{'rooms':[]})
    book=CommandBook(args.dictionary or dictionary_path())
    required=('look','exits','score','inventory','equipment','consider','cast','flee','save','sleep','sit','rest','stand','north','south','east','west','up','down','buy','eat','drink','fill','list','examine','get','junk')
    missing=[verb for verb in required if not book.has(verb)]
    if not args.live and not args.replay:
        print(json.dumps({'execution':'preview_only','network':False,'mode':args.mode,'dictionary':str(book.path),
            'dictionary_entries':len(book.entries),'missing_commands':missing,
            'preparation':{'food_target':config.food_target,'water_fraction_min':.75,'spare_slots':config.spare_slots},
            'actions':['localizar','preparar','olhar_ao_redor','olhar_adiante','mover','ambientar_transito','ambientar_exploracao','lutar_'+PROFILES[args.mode].combat,'selecionar_espolios','recuperar','acampar_perto','vigiar_ataques'],
            'city_return':'Apenas para comida/água; outros impasses passam ao agente.',
            'legacy':'scripts/local/legacy/dungeon_v1',
            'limits':{'commands':config.max_commands,'seconds':config.max_seconds}},ensure_ascii=False,indent=2))
        return 0
    if missing:parser.error('Dicionário atual não confirma os comandos: '+', '.join(missing))
    if args.live and (args.day is None or args.day<=0):parser.error('--live exige --day positivo para registrar a sessão autorizada.')
    output=ROOT/'scripts/local'/f'expedition_{args.hero}_dia{args.day}_{datetime.now().strftime("%Y%m%d_%H%M%S")}_{uuid.uuid4().hex[:6]}.jsonl'
    io=ReplayTransport(json_read(args.replay,[])) if args.replay else live_transport(ROOT,args.hero,args.day,output)
    ctx=Context(io,book,config,state,map_data);engine=Expedition(ctx);guardian=ReactionGuard(ctx)
    if args.live:guardian.start()
    try:
        while True:
            result=engine.run()
            print(json.dumps({'status':result.status.value,'reason':result.reason,'data':result.data,
                              'moves':ctx.moves,'kills':ctx.kills,'observed_net_mv_spent':ctx.gross_mv_spent},ensure_ascii=False),flush=True)
            if result.status==Status.CAMPED:return 0
            if args.replay:return 2
            print('EXPEDITION_PAUSED: conexão preservada. JSON: {"action":"observe"}, {"action":"resume"}, {"action":"fight","target":"..."}, {"action":"camp"} ou {"action":"close"}.',flush=True)
            while True:
                line=sys.stdin.readline()
                if not line:
                    print('Entrada encerrada; conexão liberada sem declarar repouso/salvamento.',flush=True);return 2
                try:
                    request=json.loads(line);action=request.get('action')
                    if action=='resume':
                        guardian.resume();break
                    if action=='close':return 2
                    if action=='observe':response=Observe().execute(ctx)
                    elif action=='travel':response=Travel().execute(ctx,request['destination'])
                    elif action=='inspect':
                        target=request.get('target','')
                        if not __import__('re').fullmatch(r'[\w.-]+',target):raise ValueError('Alvo exige uma palavra observada.')
                        response={'response':ctx.send('examine '+target)}
                    elif action=='classify':
                        evidence=request.get('evidence','').strip()
                        target=request.get('target','');kind=request.get('kind')
                        entity=next((e for e in ctx.room.entities if e.description==request.get('description')),None)
                        if not entity or not evidence or kind not in ('friendly','hostile','player') or not __import__('re').fullmatch(r'[\w.-]+',target):raise ValueError('Classificação exige presença atual, alvo, categoria e evidência.')
                        entity.target=target;entity.kind=kind;entity.verified=True
                        ctx.config.known_entities.append({'patterns':[entity.description],'target':target,'kind':kind,'verified':True})
                        ctx.record('agent_classification',description=entity.description,target=target,kind=kind,evidence=evidence)
                        response={'classified':True}
                    elif action=='camp':response=Camp().execute(ctx)
                    elif action=='fight':
                        entity=next((e for e in ctx.room.entities if e.target==request.get('target')),None)
                        if not entity:raise ValueError('Alvo não está identificado na sala atual.')
                        response=Fight().execute(ctx,entity)
                    else:raise ValueError('Ação não reconhecida; nenhuma execução arbitrária.')
                    print(json.dumps(asdict(response) if hasattr(response,'status') else response,ensure_ascii=False),flush=True)
                    if getattr(response,'status',None)==Status.CAMPED:return 0
                except (ValueError,NeedsAgent) as error:print(str(error),flush=True)
    finally:
        guardian.stop()
        io.close()


if __name__=='__main__':
    raise SystemExit(main())
