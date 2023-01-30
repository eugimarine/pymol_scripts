from pymol import cmd



def load_sequences(file, n_sequences='(all)'):
    """ file should be in the format of:
    [SEQUENCE]  [SUBUNIT]   [START]     [END]
    tab separated values"""
    with open(file) as f:
        i = 0
        for line in f:
            i += 1
            seq, chain, start, end = line.split()
            cmd.select(seq, f'chain {chain} & resi '+start+'-'+end)
            if i == n_sequences:
                return
cmd.extend('load_sequences', load_sequences)




