import logging

import click

from .dscore import dscore, cscore
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
@click.option('-o', '--save-dir', type=click.Path(file_okay=False), default='.', show_default=True,
              help='put saved files in this directory')
@click.option('-n', '--name', help='filename to use if single sequence with no name')
@click.option('-v', '--verbose', count=True, help='set the log level; can be passed up to 3 times.')
@click.option('--complexity', is_flag=True, help='also calculate sequence complexity: cscore')
def cli(sequence, csv, speed, run_only, save_dir, name, verbose, complexity):
    """
    Calculate disorder and complexity scores for one or more fasta sequences.

    SEQUENCE: sequence string or fasta file for submission
    """
    logging.basicConfig(level=30 - verbose * 10)
    logger.debug(f'{sequence=}, {csv=}, {speed=}, '
                 f'{run_only=}, {save_dir=}, {name=}, {verbose=}')
    if run_only:
        servers = run_only
    else:
        servers = by_speed[speed]
    dscore(sequence, server_list=servers, save_as_csv=csv, save_dir=save_dir, name=name)
    if complexity:
        cscore(sequence, save_as_csv=csv, save_dir=save_dir, name=name)
