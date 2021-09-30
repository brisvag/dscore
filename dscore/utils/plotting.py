import numpy as np
import matplotlib.pyplot as plt


def save_dscore_plot(df, image_path, name):
    df.plot(y='dscore', legend=False, ylim=(0, 1),
            xlabel='resid', ylabel='dscore', title=name)
    plt.savefig(image_path, bbox_inches='tight')


def save_servers_plot(df, image_path, name):
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
    plt.savefig(image_path, bbox_inches='tight')
