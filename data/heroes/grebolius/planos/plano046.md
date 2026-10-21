# Plano 046 — Pós-Xeque-mate: ganhar o nível 35 e escolher a próxima missão (Ajuda Mágica ou Tesouraria Negra)

| | |
|---|---|
| **Criado em** | 2026-10-21 · Dia 160 |
| **Por** | Claude Sonnet 5.5 (claude-sonnet-5-5) |
| **Herói** | grebolius |
| **Objetivo** | Subir ao nível 35 (faltam 84.222 de EXP) e abrir a próxima frente de missão |
| **Sessão encerrada?** | sim — Templo de Midgaard, `save` e `sleep` confirmados, driver parado, sem `quit` |

Substitui o plano 045 (meu antecessor, não é editado).

## 1. Onde o objetivo está
**A Xeque-mate está CONCLUÍDA** (`autoquest todas` = Concluída): o Cetro do Rei Negro foi entregue ao Bispo Branco em F1 com o `score tudo` mostrando "Você deve entregar objeto ao personagem", e a entrega rendeu +256 mil de EXP (9.659.707 para 9.915.778). Falta pouco para o nível 35 (84.222 de EXP). As frentes abertas são a Ajuda Mágica (sem tomo) e a Tesouraria Negra (porta `baixo` de D8).

## 2. Estado exato
- **Local:** Templo de Midgaard, dormindo.
- **Nível 34** · EXP 9.915.778 (faltam **84.222** para o 35) · HP 214/214 · mana 510/510 · MV 148 · alinhamento 382 (Bom) · CA 178 com buffs (`armor` + `invisibility`). Morreu 13 vezes e 1 DT.
- **Ouro:** 41.806 (40.256 banco + 1.550 mão). Diretriz: nenhuma compra acima de 5% do ouro total (~2.090) sem pedir ao autor.
- **Inventário:** 1 Cetro do Rei Negro e 2 Chaves do Tesouro Negro (ambos **invisíveis**; `detect invisibility` mostra, e falha no Templo), cantil **vazio** (encher na fonte), 3 a 4 pães, mochila de Pellinore com uma Lança do Cavaleiro Negro amaldiçoada (não doa), tomo druídico, cajado retorcido. Equipamento todo vestido.
- **Autoquests:** Xeque-mate Concluída; Ajuda Mágica não ativa. Fonte: `state.json`; conferir com `score tudo`.

## 3. O que já foi descoberto
- **Ordens do Bispo Branco:** conhecimento §89 (as seis ordens da cascata, cada uma ~100 s depois de voltar a F1).
- **Roubo de abate:** o jogador **Keen** fica no tabuleiro; se ele der o golpe final num alvo da missão, o abate não conta (§89). A prova é o `score tudo`.
- **Chave do Tesouro Negro:** deteriora; abre o `baixo` de D8 (Tesouraria Negra), ainda não aberto. A Rainha reaparece em ~20 min e atrapalha D8.
- **Cetro:** vale 85.000 de valor, ANTI-BOM, não vestir.

## 4. Os bloqueios, e o que já foi tentado
- **Auditor da sessão:** 2 FALHAS `alinhamento-caiu` (de 393 para 388 e para 358): o alinhamento caiu por matar peças pretas e outros monstros na cascata (487 para 382 ao longo do dia). Não é bug; a cascata exige matar. Subir de novo doando (`donate`) itens do chão, como no Dia 159 (+56).
- **Driver:** cai a cada ~1 h; reiniciar só o `live_daemon` por PID (nunca todos os Python) manteve a missão.
- **Ajuda Mágica:** sem tomo; fonte original desconhecida (Escriba/Albernathy em Silverthorne sem rota; Torre da Magia).

## 5. O próximo passo, e só ele
Conectar (`mandabala.py`; `cota_claude.py --registrar`; subir o `live_daemon` com `MUD_DAY=161 MUD_WIMPY=45`; `quality_run.py --loop --intervalo 30`), `score tudo`, `prepara.py --forcar --sem-doacoes` (encher o cantil) e `cuidar.py`. Depois, **modo moer** pelo dono: `turno.py --rotina milharal_v2 --turnos 3 --socorrer` até o nível 35. Opções seguintes, a padrão primeiro: (a) **Ajuda Mágica**: reabrir a investigação do tomo (`mandabala.py --sobre ajuda`); (b) Tesouraria Negra: ir a E8 invisível com `detect invisibility`, pegar uma Chave do chão e abrir `baixo` de D8 com a Rainha morta.

## 6. NÃO REPITA
- **Não montar laço em PowerShell** (§26 da diretiva): cada etapa à mão, lendo o retorno; moer = `turno.py`.
- Não entrar em E1 (Rei Branco) nem passar pela fileira 1 do lado branco; não pegar a Armadura da Torre Negra (maldita) em H8.
- Não concluir que a Rainha foi morta pelo contador do `xadrez_cascata.py`: conferir o `score tudo`.
- Vida abaixo de 100 só `recall`; nenhuma compra acima de 5% do ouro sem pedir; não derrubar todos os Python.

## 7. Ferramentas e comandos
Python: `C:\Users\peter\AppData\Local\Programs\Python\Python312\python.exe`. `play.py "<cmd>"` (`_CLOSE sleep`), `navegar.py`, `prepara.py`, `cuidar.py`, `turno.py`, `vigia.py`, `aproveitar_tempo.py`, `xadrez_cascata.py` (`--etapa peoes|bispos|cavalos|torres|rainha|f1|rei`), `mandabala.py --sobre <termo>`, `cota_claude.py`, `quality_run.py --loop`.

## 8. Devolutiva técnica
| Descobri | Registrei em | O quê |
|---|---|---|
| mapa | `mapa.json` | nada novo |
| referência do servidor | `maquina/verificacoes.md` | nada: tudo no conhecimento §89 |
| fato do mundo | `conhecimento.md` §89 | ordens do Bispo, roubo de abate do Keen, `detect invisibility` falha no Templo, cetro entregue |
| erro do motor | `automato/CHANGELOG.md` | nada novo: nenhum código alterado nesta parte |

## 9. Como encerrar a sua sessão
Siga `docs/agentes/PROTOCOLO.md` §3: `_CLOSE sleep` no Templo, evidência com `agent`, `python scripts/encerrar.py --agente "<modelo/versão>"`, preencher o plano 047, `python scripts/encerrar.py --agente "<modelo/versão>" --fechar --avanco sim|nao`.

