from pymol import cmd

def extract_contact_points(file_path, sep='\t'):
    """ extract contact point from a file in the following format:
    [COUNTS]    [CHAIN_1]   [RESIDUE NUM]   [CHAIN_2]   [RESIDUE NUM]
    default separator tab
    USAGE:
    extract_contact_points file_path, separator(='\t' default)
    """

    rnames_chains_coverter = {'rrna28s':'L5', 'rrna18s':'S2', 'rrna5s': 'L7' ,'rrna58s': 'L8'}
    with open(file_path) as f:
        data = [line.strip().rsplit(sep) for line in f if len(line) > 2]
    for cp in data:
        b_val = int(cp[0])
        chain_1 = rnames_chains_coverter[cp[1]]
        resi_1 = cp[2]
        chain_2 = rnames_chains_coverter[cp[3]]
        resi_2 = cp[4]
        selection_name = chain_1+'-'+resi_1+'_'+chain_2+'-'+resi_2
        cmd.select(selection_name, f'(chain {chain_1} & resi {resi_1}) | (chain {chain_2} & resi {resi_2})')
        cmd.do(f'alter {selection_name} ,b={b_val}')

cmd.extend('extract_contact_points', extract_contact_points)

def spectrum_frequency_contact_points(selection, spectrum='yellow_white_red'):
    cmd.spectrum('b', spectrum, selection)

cmd.extend('heatmap_frequency_contact_points', spectrum_frequency_contact_points)