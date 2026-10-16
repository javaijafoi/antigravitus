# -*- coding: utf-8 -*-
"""falar_fazendeiro.py - navega ate a casa da fazenda e dialoga com o fazendeiro."""
import sys
from pathlib import Path

AQUI = Path(__file__).resolve()
sys.path.insert(0, str(AQUI.parents[1] / 'nucleo'))
sys.path.insert(0, str(AQUI.parents[1] / 'rotinas'))
import base
import milharal

def ir_ate_a_casa():
    if not milharal.ir_ate_a_floresta():
        print("[falar] Falha ao ir ate a floresta")
        return False
    for m in milharal.CAMINHO_BOSQUE:
        base.andar(m)
    ex, t = base.sala()
    if not any('Pequeno Bosque' in v for v in ex.values()):
        print("[falar] Buscando marco do bosque...")
        if not milharal._achar_marco_do_bosque():
            print("[falar] Marco nao encontrado")
            return False
    print("[falar] No marco do bosque")
    base.andar('n')
    base.andar('n')
    ex, t = base.sala()
    print("[falar] Chegou em:", t.split('\n')[0].strip())
    # Rota exata comprovada pelo mapa:
    # Entrada da Fazenda -> w (Pequena Estrada) -> s (Gramado) -> w (Gramado frente casa) -> s (Entrada da Casa)
    base.andar('w')
    base.andar('s')
    base.andar('w')
    base.andar('s')
    ex, t = base.sala()
    nome = next((l.strip() for l in t.split(chr(10)) if l.strip()), '?')
    print("[falar] Chegou em:", nome)
    print("[falar] Saidas:", ex)
    return 'Casa' in nome or 'fazendeiro' in t.lower() or 'dono' in t.lower()

def main():
    try:
        base.voltar_ao_templo()
        print("[falar] Partindo do templo para a casa da fazenda...")
        if not ir_ate_a_casa():
            print("[falar] Nao foi possivel chegar a casa da fazenda")
            # Tenta buscar nas salas vizinhas
            for d in ['s', 'w', 's']:
                base.andar(d)
                ex, t = base.sala()
                nome = next((l.strip() for l in t.split(chr(10)) if l.strip()), '?')
                print(f"[falar] Tentativa extra ({d}): {nome}")
                if 'Casa' in nome or 'fazendeiro' in t.lower() or 'dono' in t.lower():
                    break
        
        cmds = [
            "look",
            "say ola",
            "say sim",
            "ask fazendeiro",
            "ask dono",
            "ask fazendeiro monstros",
            "ask fazendeiro invasores",
            "ask fazendeiro missao",
            "ask fazendeiro ajuda",
            "say terminei",
            "say matei os monstros",
            "autoquest todas",
            "score tudo"
        ]
        
        for c in cmds:
            txt, _, _ = base.run(c)
            print(f">>> {c}\n{txt.strip()}\n")
            
    finally:
        print("[falar] Retornando ao templo...")
        base.voltar_ao_templo()
        base.run("save")
    return 0

if __name__ == '__main__':
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    sys.exit(main())
