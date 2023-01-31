from pymol import cmd

def color_rna(ssu_color='palecyan', lsu_color='grey80', trna=None):
    # cmd.hide('spheres')
    cmd.color('grey')
    cmd.color(lsu_color,"chain L5 chain L7 chain L8")
    cmd.color(ssu_color,"chain S2")
    if trna is not None:
        cmd.color(trna, "chain S6")

cmd.extend('color_rna', color_rna)

def select_rrna():
    cmd.select('lsu_rrna', 'chain L5 chain L7 chain L8')
    cmd.select('ssu_rrna', 'chain S2')
    cmd.select('rrna', 'chain L5 chain L7 chain L8 chain S2')
    cmd.alter('rrna', 'b=0')

cmd.extend('select_rrna', select_rrna)
