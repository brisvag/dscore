import click

from .dscore import dscore as _dscore
from .servers import sequence_disorder, by_speed


@click.command(name='dscore')
@click.argument('sequence')
@click.option('-d', '--dscore', is_flag=True, help='save result as simple dscore text format')
@click.option('-c', '--csv', is_flag=True, help='save result as csv')
@click.option('-s', '--speed', type=click.Choice(list(by_speed.keys())), default='normal', show_default=True,
              help='restrict servers by speed. Fast: 30s/sequence. Normal: include disopred and prdos, 5min/sequence. '
                   'Slow: include cspritz, up to 30min/sequence.')
@click.option('-r', '--run-only', type=click.Choice(list(sequence_disorder.keys())), multiple=True,
              help='override SPEED. Run only the chosen servers. Can be passed multiple times.')
@click.option('-o', '--save-dir', type=click.Path(file_okay=False), default='.', show_default=True,
              help='put saved files in this directory')
@click.option('-n', '--name', help='filename to use if single sequence with no name')
def cli(sequence, dscore, csv, speed, run_only, save_dir, name):
    """
    SEQUENCE: sequence string or fasta file
    """
    if not dscore and not csv:
        click.UsageError('you must save your result somewhere')
    servers = by_speed[speed]
    if run_only is not None:
        servers = run_only
    _dscore(sequence, server_list=servers, save_as_dscore=dscore, save_as_csv=csv, save_dir=save_dir, name=name)
