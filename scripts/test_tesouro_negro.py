# -*- coding: utf-8 -*-
"""Testes do automato/acoes/tesouro_negro.py (sem driver). Textos reais do Dia 161."""
import sys
import unittest
from pathlib import Path
from unittest import mock

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ / 'automato' / 'acoes'))
import tesouro_negro as T  # noqa: E402
import xadrez_cascata as xc  # noqa: E402

D8_FECHADA = ("Uma Casa Preta\n   Você está em um quadrado de mármore preto. Esta normalmente é a casa  \n"
              "da Rainha Negra.  \n[ Saídas: leste, sul, oeste e !baixo ]\nA Rainha Negra está dormindo aqui.\n"
              "...ela está protegida por uma luz muito forte!\n\n232hp 504mn 146mv >")
D8_ABERTA = D8_FECHADA.replace('!baixo', 'baixo')
D8_ACORDADA = D8_FECHADA.replace('está dormindo aqui', 'está aqui')
TESOURO_SALA = ("O Tesouro Negro\n   Você está perto do tesouro do Tribunal Preto. Esperançosamente ninguém   \n"
                "roubou o tesouro da Coroa.  \n[ Saídas: cima ]\nHá muitos objetos jogados aqui.\n")
PEGOU = "Você pega o Tesouro Negro da Realeza.\nHavia 20.000 moedas.\n"


class TestPuras(unittest.TestCase):
    def test_saidas_e_porta(self):
        self.assertEqual(T.saidas(D8_FECHADA), ['leste', 'sul', 'oeste', '!baixo'])
        self.assertEqual(T.porta_baixo(D8_FECHADA), 'fechada')
        self.assertEqual(T.porta_baixo(D8_ABERTA), 'aberta')
        self.assertIsNone(T.porta_baixo('[ Saídas: norte e sul ]'))
        self.assertEqual(T.saidas('sem linha de saidas'), [])

    def test_rainha_acordada_ou_dormindo(self):
        self.assertTrue(T.rainha_acordada(D8_ACORDADA))
        self.assertFalse(T.rainha_acordada(D8_FECHADA))

    def test_moedas_e_tomada(self):
        self.assertEqual(T.moedas_pegas(PEGOU), 20000)
        self.assertTrue(T.pegou(PEGOU))
        self.assertFalse(T.pegou('Você não vê nenhuma moeda aqui.'))
        self.assertIsNone(T.moedas_pegas('nada'))

    def test_tem_chave_so_com_o_nome_certo(self):
        self.assertTrue(T.tem_chave('Você está carregando:\na Chave do Tesouro Negro (invisível)\num cantil\n'))
        self.assertFalse(T.tem_chave('Você está carregando:\num cantil\n'))

    def test_espera_inicial_sem_intervalo_medido(self):
        self.assertEqual(T.proxima_espera_min([]), T.ESPERA_INICIAL_MIN)
        self.assertEqual(T.proxima_espera_min([1000.0]), T.ESPERA_INICIAL_MIN)

    def test_espera_pela_mediana_dos_intervalos_com_folga(self):
        t0 = 0.0
        tomadas = [t0, t0 + 20 * 60, t0 + 40 * 60, t0 + 70 * 60]       # intervalos 20, 20, 30: mediana 20
        self.assertAlmostEqual(T.proxima_espera_min(tomadas), 20 - T.FOLGA_MIN)

    def test_espera_nunca_abaixo_do_passo(self):
        self.assertEqual(T.proxima_espera_min([0.0, 60.0, 120.0]), T.PASSO_MIN)


SCORE_91 = (" Você está carregando 8 itens, num peso total de 91 kg.\n"
            " Você pode carregar no máximo 30 itens e um peso total de 115 kg.\n")
SCORE_115 = SCORE_91.replace('91 kg', '115 kg')
RECUSA_PESO = "Você já está carregando muito peso e não pode pegar o Tesouro Negro da Realeza.\n"


class TestPeso(unittest.TestCase):
    def test_le_peso_e_limite_do_score(self):
        self.assertEqual(T.peso_do_score(SCORE_91), (91, 115))
        self.assertIsNone(T.peso_do_score('nada'))

    def test_folga_para_o_tesouro(self):
        self.assertFalse(T.sem_folga(SCORE_91))            # 24 kg livres
        self.assertTrue(T.sem_folga(SCORE_115))            # 0 livres
        self.assertTrue(T.sem_folga(SCORE_91.replace('91 kg', '100 kg')))   # 15 < 18
        self.assertFalse(T.sem_folga('sem peso'))          # nao sei nao e' "sem folga"


class FalsoTab:
    """Substitui o Tabuleiro: o D8 devolve o texto escolhido pelo teste."""
    d8 = D8_FECHADA

    def __init__(self, casa, run):
        pass

    def ir(self, destino):
        return ('', {}, False)

    def passo(self, d):
        return (self.d8, {'hp': 232}, False)


class FalsoCtx:
    def __init__(self, respostas):
        self.respostas, self.enviados, self.recalls = respostas, [], 0
        self.run = lambda c: ('', {}, False)

    def garantir_templo(self):
        return True

    def comer_beber(self):
        pass

    def ir_h5(self):
        pass

    def cmd(self, c, espera=1.0):
        self.enviados.append(c)
        return (self.respostas.get(c, ''), {}, False)

    def recall(self):
        self.recalls += 1


class TestUmaIda(unittest.TestCase):
    def ida(self, respostas, d8=D8_FECHADA):
        FalsoTab.d8 = d8
        ctx = FalsoCtx(respostas)
        with mock.patch.object(xc, 'Tabuleiro', FalsoTab), mock.patch.object(T, 'socorrer'):
            r = T.uma_ida(ctx, log=lambda *_: None)
        return r, ctx

    def test_pegou_com_a_porta_fechada(self):
        r, ctx = self.ida({'unlock baixo': '*Click*', 'open baixo': 'Certo.', 'down': TESOURO_SALA, 'get moedas': PEGOU})
        self.assertEqual((r['resultado'], r['moedas'], r['porta']), ('pegou', 20000, 'fechada'))
        self.assertEqual(ctx.enviados, ["cast 'invisibility'", "cast 'sleep' rainha", 'unlock baixo', 'open baixo', 'down',
                                        'get moedas', 'up'])
        self.assertEqual(ctx.recalls, 1)

    def test_porta_aberta_nao_tenta_destrancar_e_sempre_dorme_a_rainha(self):
        r, ctx = self.ida({'down': TESOURO_SALA, 'get moedas': PEGOU}, d8=D8_ABERTA)
        self.assertEqual(r['resultado'], 'pegou')
        self.assertNotIn('unlock baixo', ctx.enviados)
        self.assertIn("cast 'sleep' rainha", ctx.enviados)

    def test_sem_tesouro_ainda(self):
        r, ctx = self.ida({'unlock baixo': '*Click*', 'open baixo': 'Certo.', 'down': TESOURO_SALA,
                           'get moedas': 'Você não vê nenhuma moedas aqui.'})
        self.assertEqual(r['resultado'], 'sem_tesouro')
        self.assertEqual(ctx.enviados[-1], 'up')

    def test_recusa_por_peso_nao_e_sem_tesouro(self):
        r, ctx = self.ida({'unlock baixo': '*Click*', 'open baixo': 'Certo.', 'down': TESOURO_SALA, 'get moedas': RECUSA_PESO})
        self.assertEqual(r['resultado'], 'peso')

    def test_nao_desceu_fica_sem_up_e_faz_recall(self):
        r, ctx = self.ida({'unlock baixo': 'Parece estar trancado.', 'open baixo': 'Parece estar trancado.',
                           'down': 'Não dá! Você está muito ocupado, lutando!'})
        self.assertEqual(r['resultado'], 'nao_desceu')
        self.assertNotIn('get moedas', ctx.enviados)
        self.assertEqual(ctx.recalls, 1)

    def test_posicao_incerta_vira_erro_e_faz_recall(self):
        class Quebra(FalsoTab):
            def ir(self, destino):
                raise xc.Perdida('H7 deveria ser casa de peao')
        ctx = FalsoCtx({})
        with mock.patch.object(xc, 'Tabuleiro', Quebra), mock.patch.object(T, 'socorrer'):
            r = T.uma_ida(ctx, log=lambda *_: None)
        self.assertEqual(r['resultado'], 'erro')
        self.assertIn('H7', r['erro'])
        self.assertEqual(ctx.recalls, 1)


INV_COM = 'Você está carregando:\na Chave do Tesouro Negro (invisível)\num cantil\n'
INV_SEM = 'Você está carregando:\num cantil\n'


class TestObterChave(unittest.TestCase):
    """A chave deteriora entre sessoes (sumiu no login do Dia 163): chao de E8 primeiro, kite no Rei por ultimo."""

    def ctx(self, inventarios):
        c = FalsoCtx({'get chave': 'Você não vê nenhum chave aqui.', "cast 'sleep' rei": 'O Rei Negro vai dormir.'})
        it = iter(inventarios)
        c.run = lambda cmd: ((next(it) if cmd == 'inventory' else ''), {}, False)
        return c

    def obter(self, inventarios):
        ctx = self.ctx(inventarios)
        with mock.patch.object(xc, 'Tabuleiro', FalsoTab), mock.patch.object(xc, 'kite_rei') as kite, \
                mock.patch.object(T, 'socorrer'), mock.patch.object(T.time, 'sleep'), mock.patch.object(T, 'registrar'):
            ok = T.obter_chave(ctx, log=lambda *_: None)
        return ok, ctx, kite

    def test_ja_tem_a_chave_nao_anda(self):
        ok, ctx, kite = self.obter([INV_COM])
        self.assertTrue(ok)
        self.assertEqual(ctx.enviados, [])
        self.assertFalse(kite.called)

    def test_rei_acordado_que_nao_dorme_nao_pega_nada(self):
        ctx = self.ctx([INV_SEM, INV_SEM, INV_SEM, INV_SEM])
        ctx.respostas["cast 'sleep' rei"] = 'Você não conseguiu se concentrar!'
        with mock.patch.object(xc, 'Tabuleiro', FalsoTab), mock.patch.object(T.time, 'sleep'):
            self.assertFalse(T.chao_de_e8(ctx, log=lambda *_: None))
        self.assertNotIn('get all.chave', ctx.enviados)
        self.assertEqual(ctx.recalls, 1)

    def test_chao_de_e8_resolve_sem_kite(self):
        ok, ctx, kite = self.obter([INV_SEM, INV_COM])
        self.assertTrue(ok)
        self.assertIn('get all.chave', ctx.enviados)
        self.assertFalse(kite.called)
        self.assertEqual(ctx.recalls, 1)

    def test_sem_chave_no_chao_cai_no_kite_e_pega_do_corpo(self):
        ok, ctx, kite = self.obter([INV_SEM, INV_SEM, INV_COM])
        self.assertTrue(ok)
        self.assertEqual(kite.call_count, 1)
        self.assertIn('get all.chave corpo', ctx.enviados)

    def test_kite_sem_chave_devolve_false(self):
        ok, _ctx, kite = self.obter([INV_SEM, INV_SEM, INV_SEM, INV_SEM])      # +1: olhada final no chao de E8
        self.assertFalse(ok)
        self.assertEqual(kite.call_count, 1)

    def test_rei_sangrou_depois_do_recall_a_chave_esta_no_chao(self):
        ok, _ctx, kite = self.obter([INV_SEM, INV_SEM, INV_SEM, INV_COM])
        self.assertTrue(ok)
        self.assertEqual(kite.call_count, 1)


INV_DO_REI = ("Você está carregando:\num cantil\n(x4) um pão recheado\n(x2) a Chave do Tesouro Negro (invisível)\n"
               "o Cetro do Bispo Negro ..Isso tem uma pequena aura!\n(x2) a Armadura do Peão Negro (novo)\n"
               "(x2) o Cetro do Rei Negro (invisível)\numa túnica dourada (novo)\num tomo da sabedoria druídica(+2L)\n"
               "uma Cruz Ansada\na Lança do Cavaleiro Negro\n\n232hp 510mn 149mv >")


class TestGuardarNaMochila(unittest.TestCase):
    """O espolio vai para a mochila (padrao do projeto), nao fica no corpo: o peso estourou o tesouro no Dia 163."""

    def test_seletores_deixam_de_fora_so_o_essencial(self):
        sels = T.seletores_para_guardar(INV_DO_REI)
        self.assertEqual(sels, ['all.cetro', 'all.armadura', 'all.dourada', 'all.ansada', 'all.cavaleiro'])
        for essencial in ('cantil', 'pao', 'chave', 'tomo'):
            self.assertFalse(any(essencial in s for s in sels), essencial)

    def test_so_essencial_nao_gera_comando(self):
        self.assertEqual(T.seletores_para_guardar('Você está carregando:\num cantil\n(x2) um pão recheado\n'), [])

    def test_usa_o_guardar_do_projeto(self):
        ctx = FalsoCtx({})
        ctx.run = lambda c: (INV_DO_REI if c == 'inventory' else '', {}, False)
        with mock.patch('base.guardar_na_mochila') as g:
            T.guardar_espolio(ctx, log=lambda *_: None)
        self.assertEqual(g.call_args.args[0], 'all.cetro')
        self.assertEqual(len(g.call_args.args), 5)


class TestLadoBranco(unittest.TestCase):
    """O Tesouro Branco e' o espelho: porta em D1, acesso por D2, chave do Rei Branco (UMA morte, excecao do autor)."""

    def setUp(self):
        self.addCleanup(setattr, T, 'LADO', T.LADO)

    def test_espelho_do_negro(self):
        self.assertEqual(T.TESOUROS['negro']['acesso'], ('D7', 'n'))
        self.assertEqual(T.TESOUROS['branco']['acesso'], ('D2', 's'))
        self.assertEqual(T.TESOUROS['branco']['rainha'], 'D1')

    def test_uma_ida_branca_vai_por_d2_e_desce(self):
        T.LADO = 'branco'
        passos = []

        class TabBranca(FalsoTab):
            def ir(self, destino):
                passos.append(('ir', destino))

            def passo(self, d):
                passos.append(('passo', d))
                return (D8_FECHADA.replace('Rainha Negra', 'Rainha Branca'), {'hp': 232}, False)
        ctx = FalsoCtx({'unlock baixo': '*Click*', 'open baixo': 'Certo.',
                        'down': TESOURO_SALA.replace('Negro', 'Branco'), 'get moedas': PEGOU.replace('Negro', 'Branco')})
        with mock.patch.object(xc, 'Tabuleiro', TabBranca), mock.patch.object(T, 'socorrer'), mock.patch.object(T, 'guardar_espolio'):
            r = T.uma_ida(ctx, log=lambda *_: None)
        self.assertEqual(passos, [('ir', 'D2'), ('passo', 's')])
        self.assertEqual(r['resultado'], 'pegou')

    def test_chave_do_tesouro_branco_conta_como_chave(self):
        self.assertTrue(T.tem_chave('Você está carregando:\na Chave do Tesouro Branco (invisível)\n'))

    def test_rei_branco_morre_uma_vez_so(self):
        T.LADO = 'branco'
        marcador = RAIZ / 'automato' / 'runtime' / 'rei_branco_morto_TESTE.json'
        marcador.unlink(missing_ok=True)
        self.addCleanup(marcador.unlink, True)
        ctx = FalsoCtx({})
        invs = iter([INV_COM])
        ctx.run = lambda cmd: ((next(invs) if cmd == 'inventory' else ''), {}, False)
        with mock.patch.object(T, 'REI_BRANCO_MORTO', marcador), mock.patch.object(xc, 'kite_rei', return_value=0) as kite,                 mock.patch.object(T.time, 'sleep'), mock.patch.object(T, 'registrar'):
            self.assertTrue(T.obter_chave_branca(ctx, log=lambda *_: None))
            self.assertEqual(kite.call_args.kwargs['lado'], 'branco')
            self.assertTrue(marcador.exists())
            kite.reset_mock()
            self.assertFalse(T.obter_chave_branca(ctx, log=lambda *_: None))     # 2a vez: nao mata de novo
            self.assertFalse(kite.called)


class TestSeguranca(unittest.TestCase):
    def test_tarefas_ociosas_nao_vendem_espolio(self):
        self.assertNotIn('vender_espolio', T.TAREFAS_OCIOSAS)

    def test_fala_com_o_jogo_so_por_ctx_e_nao_entra_em_e8(self):
        src = (RAIZ / 'automato' / 'acoes' / 'tesouro_negro.py').read_text(encoding='utf-8')
        self.assertNotIn("ir('E8')", src)       # a rota nunca anda PARA dentro da casa do Rei
        self.assertNotIn("ir('E1')", src)
        self.assertNotIn('import socket', src)
        for proibido in ("'drop", "'sell", "'buy", "'give", "'donate", "'junk", "'kill"):
            self.assertNotIn(proibido, src)


if __name__ == '__main__':
    unittest.main()
