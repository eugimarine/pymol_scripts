from pymol import cmd
import pandas as pd

rnames_chains_coverter_4UG0 = {'rrna28s': 'L5', 'rrna18s': 'S2', 'rrna5s': 'L7', 'rrna58s': 'L8'}
rnames_chains_coverter_6I7O_r1 = {'rrna28s': 'BQ', 'rrna18s': '2b', 'rrna5s': 'BR', 'rrna58s': 'BS'}
rnames_chains_coverter_6I7O_r2 = {'rrna28s': 'YQ', 'rrna18s': '2', 'rrna5s': 'YR', 'rrna58s': 'YS'}


def read_tsv_sequences(path, sel_name_col, bvalues=None):
    '''

    :param path: path to tsv (tab separeted values) file with sequences
    :param sel_name_col: column with the selection name
    :param bvalues: column containing the b values for the selection (used when applied spectrum)
    :return: selection objects
    '''
    start_seq_col = 'START'
    end_seq_col = 'END'
    chain_col = 'RNAME'
    df = pd.read_csv(path, sep='\t' )
    df.columns = df.columns.str.upper()
    df[chain_col] = df[chain_col].map(rnames_chains_coverter_4UG0)
    for row in df.iterrows():
        sel_name = row[1][sel_name_col]
        b_val = str(row[1][bvalues])
        start = str(row[1][start_seq_col])
        chain = row[1][chain_col]
        end = str(row[1][end_seq_col])
        cmd.select(sel_name, f'chain {chain} & resi '+start+'-'+end)
        cmd.do(f'alter {sel_name} ,b={b_val}')

cmd.extend('read_tsv_sequences', read_tsv_sequences)

def color_all_tsv_sequences(path, color, selection_name, bvalues=None):
    '''

    :param path: path to tsv (tab separeted values) file with sequences
    :param color: color name
    :param selection_name: selection name as it will appear on pymol
    :return: selection objects
    '''
    start_seq_col = 'START'
    end_seq_col = 'END'
    chain_col = 'RNAME'
    df = pd.read_csv(path, sep='\t' )
    rnames_chains_coverter = {'rrna28s': 'L5', 'rrna18s': 'S2', 'rrna5s': 'L7', 'rrna58s': 'L8'}
    df[chain_col] = df[chain_col].map(rnames_chains_coverter)
    for row in df.iterrows():
        if bvalues is not None:
            b_val = str(row[1][bvalues])
        start = str(row[1][start_seq_col])
        chain = row[1][chain_col]
        end = str(row[1][end_seq_col])
        cmd.select(selection_name,  f'chain {chain} & resi '+start+'-'+end)
        cmd.color(color, f'chain {chain} & resi '+start+'-'+end)

cmd.extend('color_all_tsv_sequences', color_all_tsv_sequences)
