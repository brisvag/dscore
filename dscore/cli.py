import click

from .dscore import dscore as _dscore


@click.command(name='dscore')
@click.argument('sequence')
@click.option('-n', '--name', help='base name to use for saved files')
@click.option('-d', '--dscore', is_flag=True, help='save result as simple dscore text format')
@click.option('-c', '--csv', is_flag=True, help='save result as csv')
@click.option('-o', '--output-dir', type=click.Path(file_okay=False), default='.', show_default=True,
              help='put saved files in this directory')
def cli(sequence, name, dscore, csv, output_dir):
    _dscore(sequence, save_as_dscore=dscore, save_as_csv=csv, save_path=output_dir, base_name=name)
