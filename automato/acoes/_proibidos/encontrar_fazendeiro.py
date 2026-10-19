# -*- coding: utf-8 -*-
raise SystemExit('PROIBIDO: este script automatiza fala/entrega/compra de missao (AGENTS #13/#14). Veja automato/acoes/_proibidos/LEIA.md')  # trava: _proibidos
"""encontrar_fazendeiro.py - busca o fazendeiro nos comodos da casa e entrega a missao."""
import sys
from pathlib import Path

AQUI = Path(__file__).resolve()
sys.path.insert(0, str(AQUI.parents[1] / 'nucleo'))
sys.path.insert(0, str(AQUI.parents[1] / 'rotinas'))
import base
import milharal

def ir_ate_a_casa():
    if not milharal.ir_ate_a_floresta():
        print("[busca] Falha ao ir ate a floresta")
        return False
    for m in milharal.CAMINHO_BOSQUE:
        base.andar(m)
    ex, t = base.sala()
    if not any('Pequeno Bosque' in v for v in ex.values()):
        print("[busca] Buscando marco do bosque...")
        if not milharal._achar_marco_do_bosque():
            print("[busca] Marco nao encontrado")
            return False
    base.andar('n')
    base.andar('n')
    # w, s, w, s ate Entrada da Casa
    base.andar('w')
    base.andar('s')
    base.andar('w')
    base.andar('s')
    ex, t = base.sala()
    nome = next((l.strip() for l in t.split(chr(10)) if l.strip()), '?')
    print("[busca] Na casa:", nome)
    return 'Entrada da Casa' in nome

def dialogar():
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
        "say pronto",
        "say 10",
        "say dez"
    ]
    for c in cmds:
        txt, _, _ = base.run(c)
        print(f">>> {c}\n{txt.strip()}\n")

def main():
    try:
        base.voltar_ao_templo()
        print("[busca] Partindo do templo para a fazenda...")
        if not ir_ate_a_casa():
            print("[busca] Nao chegou a entrada da casa")
            return 1
        
        comodos = [
            ("A Entrada da Casa", []),
            ("A Sala de Estar", ['s']),
            ("Um Quarto", ['w']),
            ("De volta a Entrada", ['e', 'n']),
            ("A Cozinha", ['w'])
        ]
        
        for nome_comodo, passos in comodos:
            for p in passos:
                base.andar(p)
            ex, t = base.sala()
            nome_real = next((l.strip() for l in t.split(chr(10)) if l.strip()), '?')
            print(f"\n=== Comodo: {nome_real} ===")
            print(t.strip())
            low = t.lower()
            if 'fazendeiro' in low or 'dono' in low:
                print(f"[busca] FAZENDEIRO ENCONTRADO em {nome_real}!")
                dialogar()
                break
        else:
            print("[busca] Fazendeiro nao estava nos comodos principais; tentando falar onde estamos...")
            dialogar()
            
        print("\n=== Conferindo status final das autoquests ===")
        txt_aq, _, _ = base.run("autoquest todas")
        print(txt_aq.strip())
        txt_sc, _, _ = base.run("score tudo")
        print(txt_sc.strip())

    finally:
        print("[busca] Retornando ao templo...")
        base.voltar_ao_templo()
        base.run("save")
    return 0

if __name__ == '__main__':
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    sys.exit(main())
