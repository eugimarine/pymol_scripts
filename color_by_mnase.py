import pandas as pd
from pymol import cmd

def color_by_mnase(path, data_col, color_chain):
    '''
    :param path: path to tsv (tab separeted values) file with sequences
    :param data_col: column containing the b values for the selection (used when applied spectrum)
    '''
    pos_name = 'pos'
    chain_col = 'rname'
    df = pd.read_csv(path)

    mnase_groups = df.groupby("units_mnase")
    
    cmd.do(f'alter all, b=0')
    for mn_u, group in mnase_groups:
        max_val = group[data_col].max()
        min_val = group[data_col].min() 
        for row in group.iterrows():
            b_val = str(row[1][data_col])
            pos = str(row[1][pos_name])
            chain = row[1][chain_col]
            cmd.do(f'alter {chain} & resi {pos} ,b={b_val}')
        cmd.do(f'spectrum b, rainbow, {color_chain}')
        cmd.do(f"ramp_new cb_mn{round(mn_u,4)}, , [{min_val},{max_val}], rainbow ")
        cmd.scene(f"mn{round(mn_u, 5)}", action="store" )

cmd.extend('color_by_mnase', color_by_mnase)


# def color_by_mnase_allmolecules(path, data_col, color_chain):
#     '''
#     :param path: path to csv file
#     :param data_col: column containing the b values for the selection (used when applied spectrum)
#     '''
#     pos_name = 'pos'
#     chain_col = 'rname'
#     df = pd.read_csv(path)

#     mnase_groups = df.groupby("units_mnase")
    
#     cmd.do(f'alter all, b=0')
#     for mn_u, group in mnase_groups:
#         max_val = group[data_col].max()
#         min_val = group[data_col].min() 
#         for row in group.iterrows():
#             b_val = str(row[1][data_col])
#             pos = str(row[1][pos_name])
#             chain = row[1][chain_col]
#             cmd.do(f'alter {chain} & resi {pos} ,b={b_val}')
#         cmd.do(f'spectrum b, rainbow, {color_chain}')
#         cmd.do(f"ramp_new cb_mn{round(mn_u,4)}, , [{min_val},{max_val}], rainbow ")
#         cmd.scene(f"mn{round(mn_u, 5)}", action="store" )

# cmd.extend('color_by_mnase', color_by_mnase)