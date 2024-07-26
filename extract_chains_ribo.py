from pymol import cmd
import pandas as pd

rnames_chains_coverter_4UG0 = {'rrna28s': 'L5', 'rrna18s': 'S2', 'rrna5s': 'L7', 'rrna58s': 'L8', 'trna':'S6'}
rnames_chains_coverter_6I7O_r2 = {'rrna28s': 'YQ', 'rrna18s': '2', 'rrna5s': 'YR', 'rrna58s': 'YS'}

model = {'4ug0': rnames_chains_coverter_4UG0, '6i7o': rnames_chains_coverter_6I7O_r2}

def extract_rrna(mol=None, struct='4ug0'):
    for rrna, nm in model[struct].items():
        if mol is not None:
            cmd.extract(rrna+'_'+mol, f"{mol} and chain {nm}")
        else:
            cmd.extract(rrna, f"chain {nm}")

cmd.extend("extract_rrna", extract_rrna)

def extract_L_S_subunit(name):
    chains = cmd.get_chains(name)
    small_su = []
    large_su = []
    for chain in chains:
        if chain[0] == "S":
            small_su.append(chain)
        elif chain[0] == "L" :
            large_su.append(chain)
        else:
            raise("ERROR L or S not found in chain name")
    parse_s = '+'.join(small_su)
    parse_l = '+'.join(large_su)
    cmd.extract(f'small_subunit_{name}', "chain "+parse_s)
    cmd.extract(f'large_subunit_{name}', "chain "+parse_l)


cmd.extend("extract_L_S_subunit", extract_L_S_subunit)