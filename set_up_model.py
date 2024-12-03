import csv
import re
from pymol import cmd
import json 

anno_data = "/Users/eugeniomarinelli/HUBRECHT/pymol_scripts/annotations_structures.json"

def remove_bound_molecules(name, anno):
    "remove small particles and syntetic drugs that are in the annotations"
    bound = anno[name]['bound']
    for el in bound.keys():
        cmd.remove(f"resn {bound[el]['chem_comp_ids'][0]}")    


def annotate_model(name):
    with open(anno_data) as f:
        anno = json.load(f)
    struct = anno[name]
    remove_bound_molecules(name, anno)
    for rrna in struct['RNA'].keys():
        chain = struct['RNA'][rrna]['in_chains'][0]
        cmd.extract(rrna, f"chain {chain}")
    small_su = []
    large_su = []
    for rp in struct['RP'].keys():
        extr_name = struct['RP'][rp]['gene_name'][0]
        chain = struct['RP'][rp]['in_chains'][0]
        if "Small" in rp:
            small_su.append(extr_name)
        elif "Large" in rp:
            large_su.append(extr_name)
        else:
            print(f"can't determine association of {rp}")
        cmd.extract(extr_name, f"chain {chain}")
    cmd.group("LSU", " ".join(large_su))
    cmd.group("SSU", " ".join(small_su))

cmd.extend('annotate_model', annotate_model)





