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
    # Entrada da Fazenda -> w (Pequena Estrada)
    base.andar('w')
    for passo in range(6):
        ex, t = base.sala()
        nome = next((l.strip() for l in t.split(chr(10)) if l.strip()), '?')
        print(f"[falar] Passo {passo}: {nome} | saidas: {ex}")
        if 'Entrada da Casa' in nome or 'Casa' in nome:
            print("[falar] Chegou na casa!")
            return True
        casa_dir = [d for d, v in ex.items() if 'Casa' in v]
        if casa_dir:
            base.andar(casa_dir[0])
        elif 's' in ex:
            base.andar('s')
        else:
            break
    ex, t = base.sala()
    nome = next((l.strip() for l in t.split(chr(10)) if l.strip()), '?')
    print("[falar] Parou em:", nome)
    return 'Casa' in nome

def main():
    try:
        base.voltar_ao_templo()
        print("[falar] Partindo do templo para a casa da fazenda...")
        if not ir_ate_a_casa():
            print("[falar] Nao foi possivel chegar a casa da fazenda")
            return 1
        
        cmds = [
            "look",
            "ask fazendeiro",
            "ask dono",
            "say sim",
            "ask fazendeiro ajuda",
            "ask fazendeiro monstros",
            "ask fazendeiro invasores",
            "say pronto"
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
