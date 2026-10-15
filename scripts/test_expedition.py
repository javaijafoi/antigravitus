import json
from pathlib import Path
import socket
import tempfile
import unittest
from unittest.mock import patch

from expedition.models import Config, Entity, Item, Room, Supplies, Vitals, Status
from expedition.knowledge import CommandBook
from expedition.observations import (parse_room, assess_consider, terminal_state, saved,
                                    update_vitals, update_supplies)
from expedition.policy import ResourcePolicy, loot_decision, WorldGraph
from expedition.actions import Context, Move, Fight, Recover, Camp, Loot, Ambient, NeedsAgent
from expedition.adapters import ReplayTransport, LiveTransport
from expedition.engine import Prepare, Expedition, Travel
from expedition.guardian import ReactionGuard


COMMANDS='look exits score inventory equipment consider cast flee save sleep sit rest stand north south east west up down buy eat drink fill list examine get junk close'.split()
ROOM='Uma Câmara Resguardada\n   Paredes de pedra.\n[ Saídas: sul ]\n67hp 170mn 90mv >'
SCORE='Vida: 67 de 67\nMana: 170 de 170\nMovimento: 90 de 101\n[Situação atual]\nVocê está em pé.\n67hp 170mn 90mv >'
GREEN='Nível: 11 Perfeito!\nVida: 67 Perfeito!\nPoder: 21 Perfeito!\nPrecisão: 15 Perfeito!\nArmadura: 44 Perfeito!\n67hp 170mn 90mv >'


class CoreTests(unittest.TestCase):
    def setUp(self):
        self.no_network=patch.object(socket,'socket',side_effect=AssertionError('Rede proibida neste teste'))
        self.no_network.start();self.addCleanup(self.no_network.stop)
        self.temp=tempfile.TemporaryDirectory();self.addCleanup(self.temp.cleanup)
        path=Path(self.temp.name)/'dicionario.md'
        path.write_text('\n'.join(f'## `{c}`\n\n**Listado:** sim.\n' for c in COMMANDS),encoding='utf-8')
        self.book=CommandBook(path)

    def ctx(self,steps=(),config=None):
        config=config or Config(outside_rooms=['Uma Câmara Resguardada'])
        io=ReplayTransport(steps);ctx=Context(io,self.book,config,{'skills':[{'id':'magic missile','proficiency':95}]})
        ctx.vitals=Vitals(67,170,90,67,170,101,0)
        ctx.supplies=Supplies(food=4,water=1,hungry=False,thirsty=False)
        ctx.room=ctx.graph.arrive(parse_room(ROOM,config));ctx.annotate(ctx.room)
        return ctx

    def test_signed_hp_and_unknown_resources(self):
        v=Vitals();update_vitals(v,'-30hp 10mn 3mv >',0)
        self.assertEqual(v.hp,-30);self.assertFalse(v.known())
        self.assertFalse(ResourcePolicy(Config()).can_work(v,0)[0])

    def test_historical_deaths_are_not_current_death(self):
        self.assertEqual(terminal_state('Você morreu 3 vezes.\n67hp 170mn 90mv >'),'')
        self.assertEqual(terminal_state('Você está morto!'),'dead_or_menu')

    def test_negative_prompt_is_incapacitated(self):
        self.assertEqual(terminal_state('-3hp 50mn 10mv >'),'incapacitated')

    def test_louco_blocks_consider_even_other_axes_green(self):
        self.assertEqual(assess_consider(GREEN.replace('Vida: 67 Perfeito!','Vida: 67 Você é LOUCO!')),'danger')

    def test_partial_consider_is_not_permission(self):
        self.assertEqual(assess_consider('Você precisaria de sorte!'),'risky')
        self.assertEqual(assess_consider('Perfeito!'),'unknown')

    def test_full_favorable_matrix(self):self.assertEqual(assess_consider(GREEN),'favorable')

    def test_save_rejects_negative_and_unrelated_text(self):
        self.assertFalse(saved('Não foi salvo.'));self.assertFalse(saved('look'))
        self.assertTrue(saved('Salvando os seus atalhos.'))

    def test_admin_response_not_room(self):self.assertIsNone(parse_room('Salvando os seus atalhos.',Config()))

    def test_no_unknown_monster_attack(self):
        ctx=self.ctx();result=Fight().execute(ctx,Entity('Um ser espreita aqui.'))
        self.assertEqual(result.status,Status.PAUSED);self.assertEqual(ctx.io.sent,[])

    def test_brave_fight_rejects_dangerous_target(self):
        ctx=self.ctx([{'command':'consider zumbi','response':GREEN.replace('Vida: 67 Perfeito!','Vida: 67 Você é LOUCO!')}])
        result=Fight().execute(ctx,Entity('zumbi','zumbi','hostile',True))
        self.assertEqual(result.status,Status.PAUSED);self.assertEqual(ctx.io.sent,['consider zumbi'])

    def test_no_cast_of_unlearned_spell(self):
        ctx=self.ctx([{'command':'consider zumbi','response':GREEN}]);ctx.hero={'skills':[]}
        self.assertEqual(Fight().execute(ctx,Entity('zumbi','zumbi','hostile',True)).status,Status.PAUSED)

    def test_low_mana_does_not_become_blind_dagger(self):
        response=GREEN.replace('170mn','20mn')
        ctx=self.ctx([{'command':'consider zumbi','response':response}])
        result=Fight().execute(ctx,Entity('zumbi','zumbi','hostile',True))
        self.assertEqual(result.status,Status.PAUSED);self.assertFalse(any(s.startswith('kill') for s in ctx.io.sent))

    def test_batedor_does_not_start_combat(self):
        ctx=self.ctx(config=Config(mode='batedor'))
        self.assertEqual(Fight().execute(ctx,Entity('zumbi','zumbi','hostile',True)).status,Status.PAUSED)

    def test_blocked_move_does_not_advance(self):
        ctx=self.ctx([{'command':'look','response':ROOM},{'command':'look south','response':'Nada de especial.\n67hp 170mn 90mv >'}, {'command':'south','response':'Você não pode ir por aí...\n67hp 170mn 90mv >'}])
        node=ctx.room.node_id;result=Move().execute(ctx,'s')
        self.assertEqual(result.status,Status.REJECTED);self.assertEqual(ctx.moves,0);self.assertEqual(ctx.room.node_id,node)

    def test_missing_exit_never_sent(self):
        ctx=self.ctx();self.assertEqual(Move().execute(ctx,'n').status,Status.REJECTED);self.assertFalse(ctx.io.sent)

    def test_flee_relocalizes_and_never_claims_victory(self):
        ctx=self.ctx([{'command':'flee','response':'Você foge em direção ao sul.\n50hp 100mn 70mv >'}, {'command':'look','response':ROOM}])
        ctx.in_combat=True
        result=Fight().retreat(ctx,'teste')
        self.assertEqual(result.status,Status.FLED);self.assertEqual(ctx.kills,[]);self.assertEqual(ctx.io.sent,['flee','look'])

    def test_unknown_item_not_picked_or_destroyed(self):
        ctx=self.ctx();item=Item('anel','anel desconhecido')
        self.assertEqual(loot_decision(item,ctx.supplies,ctx.config)[0],'inspect')

    def test_quest_item_not_burned_even_marked_trash(self):
        ctx=self.ctx();item=Item('coleira','coleira',verified=True,quest=True,disposable=True,carried=True)
        self.assertEqual(loot_decision(item,ctx.supplies,ctx.config)[0],'keep')

    def test_unknown_container_contents_not_burned(self):
        ctx=self.ctx();item=Item('bolsa','bolsa',verified=True,disposable=True,contents_known=False,carried=True)
        self.assertEqual(loot_decision(item,ctx.supplies,ctx.config)[0],'keep')

    def test_verified_carried_trash_can_be_burned(self):
        ctx=self.ctx();item=Item('sucata','sucata',verified=True,disposable=True,carried=True)
        self.assertEqual(loot_decision(item,ctx.supplies,ctx.config)[0],'burn')

    def test_low_value_ground_loot_skipped(self):
        ctx=self.ctx();item=Item('sucata','sucata',verified=True,weight=10,sale_value=5)
        self.assertEqual(loot_decision(item,ctx.supplies,ctx.config)[0],'skip')

    def test_full_bag_does_not_force_city_return(self):
        ctx=self.ctx();ctx.supplies=Supplies(count=15,max_count=17,weight=110,max_weight=115)
        item=Item('espada','espada',verified=True,weight=2,sale_value=1000)
        self.assertEqual(loot_decision(item,ctx.supplies,ctx.config)[0],'skip')

    def test_unknown_mv_does_not_count_as_recovered(self):
        ctx=self.ctx();ctx.vitals.mv=None
        self.assertFalse(ctx.vitals.known())

    def test_reserve_scales_with_damage_and_camp_distance(self):
        policy=ResourcePolicy(Config());v=Vitals(67,170,101,67,170,101,0)
        low=policy.reserves(v,peak_damage=5,camp_cost=0)
        far=policy.reserves(v,peak_damage=22,camp_cost=30)
        self.assertGreater(far['hp'],low['hp']);self.assertGreater(far['mv'],low['mv'])

    def test_resource_gauge_does_not_count_as_daily_work(self):
        ctx=self.ctx();ctx.moves=50;ctx.gross_mv_spent=90;ctx.vitals.mv=101
        self.assertTrue(ctx.policy.can_work(ctx.vitals,0)[0]);self.assertEqual(ctx.gross_mv_spent,90)

    def test_city_camp_not_selected_for_resource_exhaustion(self):
        ctx=self.ctx();ctx.room.city=True;ctx.room.known_shelter=True;ctx.room.clean_checks=3
        self.assertIsNone(ctx.graph.nearest_camp(ctx.room.node_id))
        self.assertIsNotNone(ctx.graph.nearest_camp(ctx.room.node_id,True))

    def test_nearest_local_camp_beats_distant_one(self):
        ctx=self.ctx();ctx.room.clean_checks=3
        other=Room('Outro','other',{'n':''},node_id='other',city=False,known_shelter=True,clean_checks=3)
        ctx.graph.rooms['other']=other;ctx.graph.edges[(ctx.room.node_id,'s')]='other'
        self.assertEqual(ctx.graph.nearest_camp(ctx.room.node_id)[1],ctx.room.node_id)

    def test_no_inferred_reverse_edge(self):
        graph=WorldGraph();one=graph.arrive(Room('Sala','a',{'e':''}));two=graph.arrive(Room('Sala','b',{'w':''}),one.node_id,'e')
        self.assertIsNone(graph.path(two.node_id,one.node_id));self.assertNotEqual(one.node_id,two.node_id)

    def test_identical_titles_do_not_merge(self):
        graph=WorldGraph();one=graph.arrive(Room('Sala','same',{'n':''}));two=graph.arrive(Room('Sala','same',{'s':''}),one.node_id,'n')
        self.assertNotEqual(one.node_id,two.node_id)

    def test_recovery_interrupted_by_damage(self):
        ctx=self.ctx([{'command':'sit','response':'Você se senta.\n67hp 10mn 20mv >'},
                      {'command':'stand','response':'Você se levanta.\n50hp 10mn 20mv >'}])
        original=ctx.io.wait
        def wait(seconds):original(seconds);ctx.io.incoming.append('Um monstro ataca você!\n50hp 10mn 20mv >')
        ctx.io.wait=wait
        result=Recover().execute(ctx)
        self.assertEqual(result.status,Status.PAUSED);self.assertEqual(ctx.io.sent,['sit','stand'])

    def test_camp_needs_confirmed_sleep_and_save(self):
        steps=[{'command':'look','response':ROOM} for _ in range(3)]
        steps += [{'command':'save','response':'Salvando os seus atalhos.\n67hp 170mn 90mv >'},
                  {'command':'sleep','response':'Você se deita e dorme.\n67hp 170mn 90mv >'}]
        ctx=self.ctx(steps);result=Camp().execute(ctx)
        self.assertEqual(result.status,Status.CAMPED);self.assertNotIn('north',ctx.io.sent)

    def test_camp_refuses_negative_save(self):
        steps=[{'command':'look','response':ROOM} for _ in range(3)]+[{'command':'save','response':'Não foi salvo.\n67hp 170mn 90mv >'}]
        ctx=self.ctx(steps);self.assertEqual(Camp().execute(ctx).status,Status.PAUSED);self.assertNotIn('sleep',ctx.io.sent)

    def test_sufficient_stock_skips_shop_trip(self):
        inv='Você está carregando:\n(x4) um pão recheado\num cantil\n67hp 170mn 90mv >'
        steps=[{'command':'score tudo','response':SCORE},{'command':'inventory','response':inv},{'command':'equipment','response':'Um cajado está sendo usado.\n67hp 170mn 90mv >'},
               {'command':'look','response':ROOM},{'command':'inventory','response':inv},
               {'command':'look in cantil','response':'Um cantil está cheio de água cristalina.\n67hp 170mn 90mv >'},
               {'command':'inventory','response':inv},{'command':'score tudo','response':SCORE}]
        ctx=self.ctx(steps);self.assertTrue(Prepare().execute(ctx).ok);self.assertTrue(ctx.prepared)
        self.assertFalse(any(s.startswith('buy') for s in ctx.io.sent))

    def test_generic_manual_is_not_executable_dictionary(self):
        path=Path(self.temp.name)/'generic.md';path.write_text('## LOOK\nUsage: look',encoding='utf-8')
        self.assertFalse(CommandBook(path).has('look'))

    def test_dictionary_blocks_unlisted_and_command_injection(self):
        with self.assertRaises(ValueError):self.book.validate_command('teleport secreto')
        with self.assertRaises(ValueError):self.book.validate_command('look;kill jogador')

    def test_invalid_limits_rejected(self):
        with self.assertRaises(ValueError):Config(max_commands=0).validate()

    def test_move_observes_before_direction_and_after_arrival(self):
        destination=ROOM.replace('Uma Câmara Resguardada','Outra Câmara').replace('sul','norte')
        steps=[{'command':'look','response':ROOM},{'command':'look south','response':'Nada de especial.\n67hp 170mn 90mv >'},
               {'command':'south','response':destination},{'command':'look','response':destination}]
        ctx=self.ctx(steps);result=Move().execute(ctx,'s')
        self.assertTrue(result.ok);self.assertEqual(ctx.io.sent,['look','look south','south','look'])
        self.assertEqual(ctx.room.title,'Outra Câmara')

    def test_tip_does_not_change_room_identity(self):
        config=Config();one=parse_room(ROOM,config)
        two=parse_room('Dica: Você pode consultar comandos.\n'+ROOM,config)
        self.assertEqual(one.fingerprint,two.fingerprint);self.assertEqual(two.title,one.title)

    def test_unrecognized_presence_never_counts_as_empty_room(self):
        room=parse_room(ROOM.replace('67hp','Uma criatura desconhecida observa em silêncio.\n67hp'),Config())
        self.assertFalse(room.quiet());self.assertEqual(len(room.entities),1)

    def test_transit_encounter_does_not_start_room_clear(self):
        ctx=self.ctx();ctx.room.entities=[Entity('Um zumbi está aqui.','zumbi','hostile',True)]
        self.assertEqual(Ambient().execute(ctx,'transit').status,Status.PAUSED)
        self.assertEqual(ctx.io.sent,[])

    def test_exploration_resolves_hostile_before_room_clear(self):
        ctx=self.ctx();ctx.room.entities=[Entity('Um zumbi está aqui.','zumbi','hostile',True)]
        from expedition.models import Result
        def fight(context,entity):
            context.room.entities=[];context.kills.append(entity.target);return Result(Status.DONE,'confirmado')
        with patch.object(Fight,'execute',side_effect=fight) as action:
            self.assertTrue(Ambient().execute(ctx,'clear').ok);action.assert_called_once()
        self.assertEqual(ctx.journal[-1]['event'],'ambient_clear')

    def test_guard_reacts_while_idle_and_invalidates_plan(self):
        ctx=self.ctx([{'command':'flee','response':'Você foge em direção ao sul.\n50hp 100mn 70mv >'}, {'command':'look','response':ROOM}])
        ctx.io.incoming.append('Um monstro ataca você!\n50hp 100mn 70mv >')
        guard=ReactionGuard(ctx);guard.tick()
        self.assertTrue(ctx.interrupted);self.assertEqual(ctx.generation,1)
        self.assertEqual(ctx.io.sent,['flee','look'])
        with self.assertRaises(NeedsAgent):ctx.send('north')
        guard.tick();self.assertEqual(ctx.io.sent,['flee','look'])

    def test_guard_intercepts_attack_immediately_before_command(self):
        ctx=self.ctx([{'command':'flee','response':'Você foge em direção ao sul.\n50hp 100mn 70mv >'}, {'command':'look','response':ROOM}])
        ctx.guard=ReactionGuard(ctx);ctx.io.incoming.append('Um monstro ataca você!\n50hp 100mn 70mv >')
        with self.assertRaises(NeedsAgent):ctx.send('inventory')
        self.assertNotIn('inventory',ctx.io.sent)

    def test_guard_does_not_flee_healthy_planned_combat(self):
        ctx=self.ctx();ctx.in_combat=True;ctx.expected_combat=True
        ReactionGuard(ctx).tick();self.assertEqual(ctx.io.sent,[])

    def test_guard_reacts_to_critical_planned_combat(self):
        ctx=self.ctx([{'command':'flee','response':'Você foge em direção ao sul.\n20hp 100mn 70mv >'}, {'command':'look','response':ROOM}])
        ctx.in_combat=True;ctx.expected_combat=True;ctx.vitals.hp=20
        ReactionGuard(ctx).tick();self.assertEqual(ctx.io.sent,['flee','look'])

    def test_terminal_state_never_sends_flee_to_menu(self):
        ctx=self.ctx();ctx.io.incoming.append('Você morreu!\nFaça a sua escolha:')
        ReactionGuard(ctx).tick();self.assertTrue(ctx.terminal);self.assertEqual(ctx.io.sent,[])

    def test_attack_during_preflight_invalidates_step(self):
        ctx=self.ctx([{'command':'look','response':ROOM}, {'command':'look south','response':'Um monstro ataca você!\n50hp 100mn 70mv >'}])
        with self.assertRaises(NeedsAgent):Move().execute(ctx,'s')
        self.assertNotIn('south',ctx.io.sent)

    def test_xp_alone_is_not_a_confirmed_kill(self):
        ctx=self.ctx([{'command':'consider zumbi','response':GREEN},
            {'command':"cast 'magic missile' zumbi",'response':'Você recebe 10 pontos de experiência.\n67hp 150mn 90mv >'},
            {'command':'flee','response':'Você foge em direção ao sul.\n67hp 150mn 80mv >'}, {'command':'look','response':ROOM}],
            Config(max_combat_rounds=1))
        self.assertEqual(Fight().execute(ctx,Entity('zumbi','zumbi','hostile',True)).status,Status.FLED)
        self.assertEqual(ctx.kills,[])

    def test_full_day_offline_ends_at_local_camp_with_no_city_trip(self):
        room=ROOM.replace('sul','nenhuma')
        steps=[{'command':'look','response':room} for _ in range(7)]+[
            {'command':'save','response':'Salvando os seus atalhos.\n67hp 170mn 90mv >'},
            {'command':'sleep','response':'Você se deita e dorme.\n67hp 170mn 90mv >'}]
        ctx=self.ctx(steps);ctx.prepared=True
        result=Expedition(ctx).run()
        self.assertEqual(result.status,Status.CAMPED);self.assertEqual(ctx.io.steps,[])
        self.assertEqual(ctx.moves,0)

    def test_travel_cannot_return_to_city_for_loot(self):
        ctx=self.ctx();ctx.room.hint_id='outside'
        ctx.map_data={'rooms':[{'id':'outside','name':ctx.room.title,'layer':'novatos','exits':{'s':'city'}},
                              {'id':'city','name':'Cidade','layer':'superficie','zone':'Midgaard Urbana','exits':{}}]}
        self.assertEqual(Travel().execute(ctx,'city','vender_itens').status,Status.PAUSED)
        self.assertEqual(ctx.io.sent,[])

    def fake_live(self,chunks,timeout=1):
        from types import SimpleNamespace
        sent=[];queue=list(chunks)
        client=SimpleNamespace(sock=SimpleNamespace(fileno=lambda:1,sendall=sent.append),_reader_running=True,
            recv_chunk=lambda:queue.pop(0) if queue else '',sanitize_log=lambda text:text,close=lambda:None)
        io=LiveTransport(client,Path(self.temp.name)/'live.jsonl',timeout)
        clock=[0.];io.now=lambda:clock[0]
        def wait(seconds):clock[0]+=seconds
        io.wait=wait;self.addCleanup(io.close)
        return io,sent

    def test_live_transport_assembles_fragmented_prompt(self):
        io,sent=self.fake_live(['Resposta\n67hp 170','mn 90mv >'])
        self.assertIn('170mn 90mv >',io.command('look'));self.assertEqual(sent,[b'look\n'])

    def test_live_transport_exits_pager_once(self):
        io,sent=self.fake_live(['[ Aperte ENTER para continuar ]','','','67hp 170mn 90mv >'])
        io.command('look');self.assertEqual(sent,[b'look\n',b's\n'])

    def test_timeout_preserves_partial_response(self):
        io,sent=self.fake_live(['Resposta parcial sem prompt'])
        with self.assertRaises(TimeoutError):io.command('look')
        record=json.loads(io.path.read_text(encoding='utf-8').splitlines()[-1])
        self.assertEqual(record['event'],'transport_incomplete');self.assertIn('Resposta parcial',record['response'])

    def test_flee_attempt_is_not_success(self):
        from expedition.observations import fled
        self.assertFalse(fled('Você entra em pânico e tenta fugir, mas não consegue!'))
        self.assertTrue(fled('Você foge desesperadamente!'))

    def test_failed_flee_does_not_change_position(self):
        ctx=self.ctx([{'command':'flee','response':'Você tenta fugir, mas não consegue!\n40hp 100mn 70mv >'}]);ctx.in_combat=True
        node=ctx.room.node_id;result=Fight().retreat(ctx,'teste')
        self.assertEqual(result.status,Status.PAUSED);self.assertEqual(ctx.room.node_id,node)
        self.assertEqual(ctx.io.sent,['flee'])

    def test_same_title_after_flee_is_not_assumed_same_room(self):
        ctx=self.ctx([{'command':'flee','response':'Você foge em direção ao sul.\n50hp 100mn 70mv >'}, {'command':'look','response':ROOM}])
        node=ctx.room.node_id;Fight().retreat(ctx,'teste')
        self.assertNotEqual(ctx.room.node_id,node)

    def test_attack_while_saving_blocks_sleep(self):
        steps=[{'command':'look','response':ROOM} for _ in range(3)]+[
            {'command':'save','response':'Salvando os seus atalhos.\nUm monstro ataca você!\n50hp 100mn 70mv >'}]
        ctx=self.ctx(steps)
        with self.assertRaises(NeedsAgent):Camp().execute(ctx)
        self.assertNotIn('sleep',ctx.io.sent)


if __name__=='__main__':unittest.main()
