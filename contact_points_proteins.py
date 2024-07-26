from pymol import cmd

rnames_chains_coverter_6I7O_r1 = {'rrna28s': 'BQ', 'rrna18s': '2b', 'rrna5s': 'BR', 'rrna58s': 'BS'}
rnames_chains_coverter_6I7O_r2 = {'rrna28s': 'YQ', 'rrna18s': '2', 'rrna5s': 'YR', 'rrna58s': 'YS'}
rnames_chains_coverter_4UG0 = {'rrna28s': 'L5', 'rrna18s': 'S2', 'rrna5s': 'L7', 'rrna58s': 'L8'}


def rrna28s_contact_points(file_path, protein, color, sep=','):
    """ extract contact point from a file in the following format:
    [RESIDUE NUM]  ,  [CLOSE PROTEIN]
    default separator tab
    USAGE:
    extract_contact_points file_path, separator(=',' default)
    """

    with open(file_path) as f:
        data = [line.strip().rsplit(sep) for line in f if len(line) > 2]
    for cp in data:
        resi = cp[0]
        if cp[1] == protein:
            selection_name = 'cp_'+resi + '_' + cp[1]
            cmd.select(selection_name, f'chain L5 & resi {resi}')
            cmd.do(f'color {color},  {selection_name}')

cmd.extend('rrna28s_contact_points', rrna28s_contact_points)

