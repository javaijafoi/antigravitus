# -*- coding: utf-8 -*-
"""Testes do automato/acoes/identificar_itens.py (sem driver). Textos reais do jogo, Dias 156 a 161."""
import sys
import unittest
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ / 'automato' / 'acoes'))
import identificar_itens as I  # noqa: E402

INVENTARIO = """Você está carregando:
um diminuto brinco de novato ..Isso tem uma pequena aura! (novo)
um cajado retorcido
uma Lâmina Negra ..Isso emite um som estridente! (novo)(+44L)
(x4) um pão recheado
a mochila de Pellinore
o Cetro do Rei Negro (invisível) ..Isso emite um som estridente!
um tomo da sabedoria druídica(+3L)
um par de luvas de couro (muito gasto)

214hp 510mn 148mv >
[vitais hp=214 mn=510 mv=148 | fome=nao sede=nao | combate=False | estado=in_game | sala=None]"""

EQUIPAMENTO = ("Você está usando:\r\n"
               "  na cabeça          -> a Coroa da Rainha Branca ..Isso emite um som estridente! (novo)\r\n"
               "  na orelha direita  -> um diminuto brinco de novato ..Isso tem uma pequena aura! (novo)\r\n"
               "  nas mãos           -> um par de luvas de couro (muito gasto)\r\n\r\n212hp 480mn 149mv >")

CINTURAO = """Você se sente informado:
Objeto: 'um belo cinturão de rodeio', Tipo: ARMADURA
O item é: BRILHO
Peso: 5, Valor: 1250, Aluguel: 250, Nível: 15, Encarnação: 1
Pode ser vestido em: PEGAR CINTURA
A CA aplicada é -12
Afeta: ACERTO em 5 / DANO em 5 / DESTREZA em 1 / CARISMA em 1

214hp 510mn 148mv >"""

ANEL = """Certo.
Você se sente informado:
Objeto: 'um anel dourado' Tipo: WORN
O item é: MÁGICO NOBITS
Peso: 1, Valor: 10000, Aluguel: 10000, Nível: 0, Encarnação: 1
Pode ser vestido em: PEGAR DEDO

Isto pode te afetar :
   Modifica: ACERTO por 1
   Modifica: DANO por 1
"""

LANCA_MALDITA = """Objeto: 'a Lança do Cavaleiro Negro', Tipo: ARMA
O item é: ZUMBIDO MÁGICO ANTI-BOM AMALDIÇOADO
Peso: 12, Valor: 4000, Aluguel: 0, Nível: 0, Encarnação: 1
Pode ser vestido em: PEGAR EMPUNHAR
"""


class TestNomes(unittest.TestCase):
    def test_normaliza_artigo_marcas_e_acento(self):
        self.assertEqual(I.normalizar('uma Lâmina Negra ..Isso emite um som estridente! (novo)(+44L)'), 'lamina negra')
        self.assertEqual(I.normalizar("o Cetro do Rei Negro (invisível)"), 'cetro do rei negro')
        self.assertEqual(I.normalizar('(x4) um pão recheado'), 'pao recheado')
        self.assertEqual(I.normalizar('a Coroa da Rainha Branca'), I.normalizar('Coroa da Rainha Branca'))

    def test_inventario_com_quantidade_e_marcas(self):
        itens = I.itens_do_inventario(INVENTARIO)
        nomes = [n for n, _q, _m in itens]
        self.assertEqual(len(itens), 8)
        self.assertIn('um pão recheado', nomes)
        self.assertEqual([q for n, q, _m in itens if 'pão' in n], [4])
        lamina = next(i for i in itens if 'Lâmina' in i[0])
        self.assertIn('(+44L)', lamina[2])
        self.assertNotIn('(+44L)', lamina[0])

    def test_equipamento_slot_e_item(self):
        itens = I.itens_do_equipamento(EQUIPAMENTO)
        self.assertEqual([s for s, _n, _m in itens], ['na cabeça', 'na orelha direita', 'nas mãos'])
        self.assertEqual(itens[0][1], 'a Coroa da Rainha Branca')

    def test_palavras_chave_sem_artigos(self):
        self.assertEqual(I.palavras_chave('a Coroa da Rainha Branca'), ['coroa', 'rainha', 'branca'])
        self.assertEqual(I.palavras_chave('um par de luvas de couro (muito gasto)'), ['luvas', 'couro'])


class TestParse(unittest.TestCase):
    def test_cinturao_formato_com_virgula(self):
        d = I.parse_identify(CINTURAO)
        self.assertTrue(d['identificado'])
        self.assertEqual((d['nome'], d['tipo'], d['peso'], d['valor'], d['nivel']),
                         ('um belo cinturão de rodeio', 'ARMADURA', 5, 1250, 15))
        self.assertEqual(d['vestir_em'], ['PEGAR', 'CINTURA'])
        self.assertTrue(any('ACERTO em 5' in e for e in d['efeitos']))

    def test_anel_formato_sem_virgula_e_modifica(self):
        d = I.parse_identify(ANEL)
        self.assertEqual((d['nome'], d['tipo'], d['valor']), ('um anel dourado', 'WORN', 10000))
        self.assertEqual(d['efeitos'], ['Modifica: ACERTO por 1', 'Modifica: DANO por 1'])
        self.assertFalse(I.amaldicoado(d))

    def test_resposta_sem_objeto_nao_e_identificada(self):
        self.assertFalse(I.parse_identify('Você não vê nenhum cetro aqui.')['identificado'])
        self.assertFalse(I.parse_identify(None)['identificado'])

    def test_amaldicoado_pelas_flags(self):
        self.assertTrue(I.amaldicoado(I.parse_identify(LANCA_MALDITA)))


class TestIdentificar(unittest.TestCase):
    def test_confere_o_nome_e_tenta_o_proximo_homonimo(self):
        respostas = {
            'identify cetro': "Objeto: 'o Cetro do Bispo Branco', Tipo: BASTAO\nPeso: 5, Valor: 22999\n",
            'identify 2.cetro': "Objeto: 'o Cetro do Bispo Negro', Tipo: BASTAO\nPeso: 5, Valor: 22999\n",
        }
        d, cmds = I.identificar('o Cetro do Bispo Negro', lambda c: (respostas.get(c, 'Você não vê nenhum.'), {}, False))
        self.assertEqual(d['nome'], 'o Cetro do Bispo Negro')
        self.assertEqual(cmds, ['identify cetro', 'identify 2.cetro'])

    def test_item_que_nao_existe_devolve_none(self):
        d, cmds = I.identificar('uma coisa estranha', lambda c: ('Você não vê nenhuma.', {}, False))
        self.assertIsNone(d)
        # cada palavra e' tentada duas vezes: o driver as vezes devolve a resposta do comando anterior
        self.assertEqual(cmds, ['identify coisa', 'identify coisa', 'identify estranha', 'identify estranha'])

    def test_resposta_atrasada_e_repetida_uma_vez(self):
        chamadas = []

        def run(cmd):
            chamadas.append(cmd)
            if len(chamadas) == 1:
                return ('212hp 510mn 149mv >', {}, False)       # resposta do comando anterior
            return ("Objeto: 'um cantil' Tipo: RECIPIENTE\nPeso: 40, Valor: 45\n", {}, False)
        d, cmds = I.identificar('um cantil', run)
        self.assertEqual(d['nome'], 'um cantil')
        self.assertEqual(cmds, ['identify cantil', 'identify cantil'])


class TestVestidos(unittest.TestCase):
    """O identify so' enxerga o inventario: item vestido sai, e' identificado e volta (Dia 161)."""

    def jogo(self, respostas):
        log = []

        def run(cmd):
            log.append(cmd)
            return (respostas.get(cmd, 'Você não vê nenhum.'), {}, False)
        return run, log

    def test_tira_identifica_e_veste_de_novo(self):
        run, log = self.jogo({
            'remove rainha': 'Você pára de usar a Coroa da Rainha Branca ..Isso emite um som estridente! (novo)',
            'identify coroa': "Objeto: 'a Coroa da Rainha Branca' Tipo: ARMADURA\nO item é: ANTI-MAU\nPeso: 4, Valor: 3000\n",
        })
        d, estado = I.identificar_vestido('na cabeça', 'a Coroa da Rainha Branca', run)
        self.assertEqual(estado, 'ok')
        self.assertEqual(d['nome'], 'a Coroa da Rainha Branca')
        # tirar usa a palavra mais longa ('rainha'); identificar, a ordem do nome ('coroa'); vestir volta com a de tirar
        self.assertEqual(log, ['remove rainha', 'identify coroa', 'wear rainha'])

    def test_arma_volta_com_wield_e_bastao_com_hold(self):
        for slot, verbo in (('empunhando', 'wield'), ('segurando', 'hold')):
            run, log = self.jogo({'remove ferro': 'Você pára de usar uma lâmina de ferro',
                                  'identify ferro': "Objeto: 'uma lâmina de ferro' Tipo: ARMA\nPeso: 8, Valor: 50\n"})
            I.identificar_vestido(slot, 'uma lâmina de ferro', run)
            self.assertEqual(log[-1], f'{verbo} ferro')

    def test_item_que_nao_sai_e_preso_e_nao_e_identificado_nem_revestido(self):
        run, log = self.jogo({'remove lanca': 'Você não pode tirar a Lança, isso deve estar AMALDIÇOADO!'})
        d, estado = I.identificar_vestido('empunhando', 'a Lança do Cavaleiro Negro', run)
        self.assertEqual((d, estado), (None, 'preso'))
        self.assertFalse(any(c.startswith(('identify', 'wield', 'wear')) for c in log))

    def test_saiu_o_anel_errado_veste_de_volta_e_tenta_a_proxima_palavra(self):
        run, log = self.jogo({
            'remove anel': 'Você pára de usar um anel dourado',
            'remove rubi': 'Você pára de usar o anel de rubi do Cardeal ..Isso tem uma pequena aura! (novo)',
            'identify anel': "Objeto: 'um anel dourado' Tipo: WORN\nPeso: 1, Valor: 10000\n",
            'identify rubi': "Objeto: 'o anel de rubi' Tipo: ARMADURA\nPeso: 2, Valor: 5500\n",
        })
        d, estado = I.identificar_vestido('no dedo esquerdo', 'o anel de rubi', run)     # palavras empatadas: 'anel' vem primeiro
        self.assertEqual(estado, 'ok')
        self.assertEqual(d['nome'], 'o anel de rubi')
        self.assertEqual(log[:3], ['remove anel', 'wear anel', 'remove rubi'])
        self.assertEqual(log[-1], 'wear rubi')

    def test_tenta_primeiro_a_palavra_mais_especifica(self):
        run, log = self.jogo({'remove cardeal': 'Você pára de usar o anel de rubi do Cardeal',
                              'identify cardeal': "Objeto: 'o anel de rubi do Cardeal' Tipo: ARMADURA\nPeso: 2, Valor: 5500\n"})
        I.identificar_vestido('no dedo esquerdo', 'o anel de rubi do Cardeal', run)
        self.assertEqual(log[0], 'remove cardeal')
        self.assertNotIn('remove anel', log)

    def test_tirou(self):
        self.assertTrue(I.tirou('Você pára de usar um escudo de aço (novo).'))
        self.assertFalse(I.tirou('Você não está usando isso.'))


class TestCatalogo(unittest.TestCase):
    def test_gravar_atualiza_pela_chave(self):
        cat = {'itens': []}
        I.gravar_item(cat, I.parse_identify(ANEL), 'vestido: dedo', '2026-10-22', 'x')
        I.gravar_item(cat, I.parse_identify(ANEL), 'inventario', '2026-10-23', 'y')
        self.assertEqual(len(cat['itens']), 1)
        self.assertEqual(cat['itens'][0]['identificado_em'], '2026-10-23')

    def test_faltando_compara_por_chave_normalizada(self):
        cat = {'itens': [{'nome': 'um anel dourado'}]}
        self.assertEqual(I.faltando(['um anel dourado', 'o Anel Dourado', 'a Lança do Cavaleiro Negro'], cat),
                         ['a Lança do Cavaleiro Negro'])
        self.assertEqual(I.faltando(['x'], None), ['x'])


class TestUsaABase(unittest.TestCase):
    def test_fala_com_o_driver_so_por_base_run(self):
        src = (RAIZ / 'automato' / 'acoes' / 'identificar_itens.py').read_text(encoding='utf-8')
        self.assertIn('from base import run', src)
        self.assertNotIn('import socket', src)
        for proibido in ("run('drop", "run('sell", "run('buy", "run('give", "run('donate", "run('junk"):
            self.assertNotIn(proibido, src)


if __name__ == '__main__':
    unittest.main()
