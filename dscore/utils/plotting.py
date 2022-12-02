import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from matplotlib.cm import ScalarMappable


def dscore_plot(df, name, savepath=None):
    df.plot(y='dscore_raw', legend=False, ylim=(0, 1),
            xlabel='residue number', ylabel='dscore (order)', title=f'dscore - {name}\ndisordered below 0.5')
    plt.axhline(y=0.5, color='r', linestyle='--')
    if savepath is not None:
        plt.savefig(savepath / (name + '_dscore.png'), bbox_inches='tight')
    else:
        plt.show()


def servers_plot(df, name, savepath=None):
    server_data = df.drop(columns=['residue', 'dscore_raw'], errors='ignore')
    ylabels = server_data.columns
    data = server_data.to_numpy(int).T
    n_servers = len(ylabels)
    n_residues = len(data)

    # add lines to separate
    thick = 5
    data = data.repeat(thick, 0)
    data *= 2  # rescale to 0,2 from 0,1
    data[thick - 1::thick] = 1  # add lines (1 is white in colormap)
    data = data[:-1]  # remove trailing line

    # plot
    fig, ax = plt.subplots(figsize=(10, 0.2 * n_servers))
    plt.imshow(data, interpolation='none', aspect='auto', cmap=ListedColormap(['blue', 'white', 'red']))
    # labels
    ax.set_title(f'Disordered regions - {name}')
    ax.set_xlabel('residue number')
    ax.set_yticks((np.arange(n_residues) + 0.3) * thick)
    ax.set_yticklabels(ylabels)
    # colorbar legend
    formatter = plt.FixedFormatter(['disordered', 'ordered'])
    real_cmap = ListedColormap(['red', 'blue'])
    plt.colorbar(ScalarMappable(cmap=real_cmap), ticks=[0.25, 0.75], format=formatter, aspect=2, fraction=0.05)

    if savepath is not None:
        plt.savefig(savepath / (name + '_servers.png'), bbox_inches='tight')
    else:
        plt.show()


def consensus_plot(df, name, savepath=None):
    server_data = df.drop(columns=['residue', 'dscore_raw', 'dscore'], errors='ignore')
    # absolute deviation from consensus
    diff = np.abs(server_data.to_numpy(float) - df[['dscore']].to_numpy())
    diff = pd.DataFrame(diff, columns=server_data.columns)
    consensus = 1 - diff.mean()

    # plot
    fig, ax = plt.subplots(figsize=(10, 6))
    consensus.plot(kind='bar', legend=False, ylim=(0, 1),
                   xlabel='server', ylabel='consensus',
                   title=f'consensus - {name}')
    # rotate labels for legibility
    plt.xticks(rotation=60, ha='right')

    if savepath is not None:
        plt.savefig(savepath / (name + '_consensus.png'), bbox_inches='tight')
    else:
        plt.show()
