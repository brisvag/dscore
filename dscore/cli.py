import logging

import click
from .servers import sequence_disorder, by_speed

logger = logging.getLogger(__name__)


@click.command(name='dscore')
@click.argument('sequence')
@click.option('-c', '--csv', is_flag=True, help='save result as simple csv instead of dscore custom format')
@click.option('-s', '--speed', type=click.Choice(list(by_speed.keys())), default='fast', show_default=True,
              help='restrict servers by speed. Fast: 30s/sequence. Normal: include disopred and prdos, 5min/sequence. '
                   'Slow: include jpred, up to 10min/sequence.')
@click.option('-r', '--run-only', type=click.Choice(list(sequence_disorder.keys())), multiple=True,
              help='overrides SPEED. Run only the chosen server. Can be passed multiple times to run multiple servers.')
@click.option('-i', '--ignore', type=click.Choice(list(sequence_disorder.keys())), multiple=True,
              help='Ignore the chosen column when calculating dscore, but still include it in the servers plot. '
                   'Can be passed multiple times to ignore multiple columns.')
@click.option('-o', '--save-dir', type=click.Path(file_okay=False), default='.', show_default=True,
              help='put saved files in this directory')
@click.option('-n', '--name', help='filename to use if single sequence with no name')
@click.option('-v', '--verbose', count=True, help='set the log level; can be passed up to 3 times.')
@click.option('--complexity', is_flag=True, help='also calculate sequence complexity: cscore')
def dscore_run(sequence, csv, speed, run_only, ignore, save_dir, name, verbose, complexity):
    """
    Calculate disorder and complexity scores for one or more fasta sequences.

    SEQUENCE: sequence string or fasta file for submission

    Note: metapredict is automatically ignored for the calculation of dscore.
    """
    from .dscore import dscore, cscore

    logging.basicConfig(level=30 - verbose * 10)
    logger.debug(f'{sequence=}, {csv=}, {speed=}, '
                 f'{run_only=}, {save_dir=}, {name=}, {verbose=}')
    if run_only:
        servers = run_only
    else:
        servers = by_speed[speed]
    dscore(sequence, server_list=servers, save_as_csv=csv, save_dir=save_dir, name=name, ignore=ignore)
    if complexity:
        cscore(sequence, save_as_csv=csv, save_dir=save_dir, name=name)


@click.command(name='dscore_plot')
@click.argument('dscore', type=click.Path(exists=True, dir_okay=False))
@click.argument('columns', nargs=-1)
@click.option('-i', '--ignore', type=click.Choice(list(sequence_disorder.keys())), multiple=True,
              help='Ignore the chosen column when calculating dscore, but still include it in the servers plot. '
                   'Can be passed multiple times to ignore multiple columns.')
def dscore_plot(dscore, columns, ignore):
    """
    Recalculate dscore and plots from an existing .dscore file by using
    only a subset of servers.

    DSCORE: an existing .dscore file
    COLUMNS: any number of columns from the .dscore file to use

    Note: metapredict is automatically ignored for the calculation of dscore.
    """
    if not columns:
        return

    from dscore.utils.io import read_dscore
    from dscore.utils.plotting import dscore_plot, servers_plot, consensus_plot
    from pathlib import Path

    dscore_file = Path(dscore)
    df = read_dscore(dscore_file, score_type='d')
    name = dscore_file.stem + '_subset'
    save_path = dscore_file.parent

    columns = list(columns)
    ignore = ['metapredict'] + list(ignore)
    try:
        score = df[columns].drop(columns=ignore, errors='ignore').mean(axis=1).astype(float)
    except KeyError as e:
        raise KeyError(f'"{e.args[0]}" is not a valid column. Valid columns are: {list(df.columns[1:-2])}') from e
    df = df[['residue'] + columns]
    df['dscore_raw'] = 1 - score
    df['dscore'] = score >= 0.5

    dscore_plot(df, name, save_path)
    servers_plot(df, name, save_path)
    consensus_plot(df, name, save_path)
