from pymol import cmd
import pandas as pd

rnames_chains_coverter_4UG0 = {'rrna28s': 'L5', 'rrna18s': 'S2', 'rrna5s': 'L7', 'rrna58s': 'L8', 'trna':'S6'}
rnames_chains_coverter_6I7O_r1 = {'rrna28s': 'BQ', 'rrna18s': '2b', 'rrna5s': 'BR', 'rrna58s': 'BS'}
rnames_chains_coverter_6I7O_r2 = {'rrna28s': 'YQ', 'rrna18s': '2', 'rrna5s': 'YR', 'rrna58s': 'YS'}

color_palette = ['red', 'orange', 'yellow', 'limegreen', 'cyan', 'marine', 'magenta']

model = {'4ug0': rnames_chains_coverter_4UG0, '6i7o': rnames_chains_coverter_6I7O_r1}

def read_csv_data(path, data_col, rname, cb_name='color_bar', spect_color="rainbow"):
    '''
    :param path: path to tsv (tab separeted values) file with sequences
    :param sel_name_col: column with the selection name
    :param data_col: column containing the b values for the selection (used when applied spectrum)
    :return: selection objects
    '''
    pos_name = 'pos'
    chain_col = 'rname'
    # rnames_conv = model[mod]
    df = pd.read_csv(path)
    # df[chain_col] = df[chain_col].map(rnames_conv)
    max_val = df[data_col].max()
    min_val = df[data_col].min() 
    cmd.do(f'alter all, b=0')
    for row in df.iterrows():
        b_val = str(row[1][data_col])
        pos = str(row[1][pos_name])
        chain = row[1][chain_col]
        cmd.do(f'alter {chain} & resi {pos} ,b={b_val}')
    cmd.do(f'spectrum b, rainbow, {rname}')
    # cmd.do(f'spectrum b, {spect_color}')
    # cmd.do(f"color yellow, chain {rnames_conv['trna']}")
    if spect_color != 'rainbow':
        spect_color = spect_color.split('_')
    cmd.do(f"ramp_new {cb_name}, , [{min_val},{max_val}], {spect_color} ")

def highlight_positions(path, color='red', rep='sphere', n='all', label='counts', mod="4ug0"):
    df = pd.read_csv(path)
    for i,row in df.iterrows():
        rname = row.rname
        if n != 'all' and i > int(n):
            break
        pos = row.pos
        if label is not None:
            lab = row[label]
            cmd.do(f"label chain {rname} and resi {pos} and n. P, '{lab}'")
        cmd.do(f'color {color}, chain {rname} and res {pos}')
        cmd.do(f'show {rep}, chain {rname} and res {pos}')

def set_tab10_colors():
    cmd.set_color('tab10_0', [0.12156862745098039, 0.4666666666666667, 0.7058823529411765])
    cmd.set_color('tab10_1', [1.0, 0.4980392156862745, 0.054901960784313725])
    cmd.set_color('tab10_2', [0.17254901960784313, 0.6274509803921569, 0.17254901960784313])
    cmd.set_color('tab10_3', [0.8392156862745098, 0.15294117647058825, 0.1568627450980392])
    cmd.set_color('tab10_4', [0.5803921568627451, 0.403921568627451, 0.7411764705882353])
    cmd.set_color('tab10_5', [0.5490196078431373, 0.33725490196078434, 0.29411764705882354])
    cmd.set_color('tab10_6', [0.8901960784313725, 0.4666666666666667, 0.7607843137254902])
    cmd.set_color('tab10_7', [0.4980392156862745, 0.4980392156862745, 0.4980392156862745])
    cmd.set_color('tab10_8', [0.7372549019607844, 0.7411764705882353, 0.13333333333333333])
    cmd.set_color('tab10_9', [0.09019607843137255, 0.7450980392156863, 0.8117647058823529])

def show_clusters(path, cluster='all', label='cluster', rrna='all', color_unselected='black'):
    # requires pymol map with subunits rrna extracted
    rrna = rrna.split(',')
    set_tab10_colors()
    color_palette = 'tab10_'
    df = pd.read_csv(path)
    if rrna[0]!='all':
        df = df.loc[df['rname'].isin(rrna)]
    for i,row in df.iterrows():
        rname = row.rname
        pos = row.pos
        cluster_id = row[label]
        c = color_palette + str(int(cluster_id[-1])%10)
        if cluster != 'all':
            # print(cluster_id)
            if cluster_id != cluster:
                c = color_unselected
        cmd.do(f'color {c}, {rname} and res {pos}')

def compare_clusters(path, label='cluster', rrna='all', color_unselected='black'):
    # requires pymol map with subunits rrna extracted. clusters should be nomitated 'C1', 'C2' etc
    rrna = rrna.split(',')
    set_tab10_colors()
    color_palette = 'tab10_'
    df = pd.read_csv(path)
    if rrna[0]!='all':
        df = df.loc[df['rname'].isin(rrna)]

    groups = df.groupby(['rname', label])
    for (rname, cluster_id), df in groups:
       cmd.do(f'color {color_unselected}, all')
       for i,row in df.iterrows():
        pos = row.pos
        c = color_palette + str(int(cluster_id[-1])%10)
        cmd.do(f'color {c}, {rname} and res {pos}')
        cmd.scene(f"{cluster_id}_{rname}", action="store" )



cmd.extend('read_csv_data', read_csv_data)
cmd.extend('highlight_positions', highlight_positions)
cmd.extend('show_clusters', show_clusters)
cmd.extend('set_tab10_colors', set_tab10_colors)
cmd.extend('compare_clusters', compare_clusters)