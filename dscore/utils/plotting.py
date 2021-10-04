import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def dscore_plot(df, name, savepath=None):
    fig, ax = plt.subplots(figsize=(10, 6))
    df.plot(y='dscore', legend=False, ylim=(0, 1),
            xlabel='resid', ylabel='dscore', title=f'dscore - {name}')
    if savepath is not None:
        plt.savefig(savepath / (name + '_dscore.png'), bbox_inches='tight')
    else:
        plt.show()


def servers_plot(df, name, savepath=None):
    server_data = df.iloc[:, 2:-3]
    ylabels = server_data.columns
    data = server_data.to_numpy(int).T
    n_servers = len(ylabels)
    n_residues = len(data)

    # add lines to separate
    thick = 5
    data = data.repeat(thick, 0)
    data *= 2  # rescale to 0,2 from 0,1
    data[thick - 1::thick] = 1  # add lines (1 is white in brw colormap)
    data = data[:-1]  # remove trailing line

    # plot
    fig, ax = plt.subplots(figsize=(10, 0.2 * n_servers))
    plt.imshow(data, interpolation='none', aspect='auto', cmap='bwr')
    # labels
    ax.set_title(f'Disordered regions - {name}')
    ax.set_xlabel('residue number')
    ax.set_yticks((np.arange(n_residues) + 0.3) * thick)
    ax.set_yticklabels(ylabels)
    # colorbar legend
    formatter = plt.FixedFormatter(['disordered', 'ordered'])
    plt.colorbar(ticks=[0.5, 1.5], format=formatter, drawedges=True, values=[0, 2])

    if savepath is not None:
        plt.savefig(savepath / (name + '_servers.png'), bbox_inches='tight')
    else:
        plt.show()


def consensus_plot(df, name, savepath=None):
    data = df.iloc[:, 2:-3]
    # absolute deviation from consensus
    diff = np.abs(data.to_numpy(float) - df[['dscore_cutoff']].to_numpy())
    diff = pd.DataFrame(diff, columns=data.columns)
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
