from collections import defaultdict
from io import StringIO
import re

import numpy as np
import pandas as pd
from slugify import slugify


def csv2frame(string, **kwargs):
    """
    read a csv string into a dataframe. Takes kwargs from pd.read_csv().
    """
    stream = StringIO(string)
    defaults = dict(delim_whitespace=True, header=None, comment='#')
    defaults.update(kwargs)
    return pd.read_csv(stream, **defaults)


def ranges2frame(ranges, seq, col_name):
    df = pd.DataFrame(np.zeros(len(seq)), dtype=bool, columns=[col_name])
    for rg in ranges:
        # convert in python range objects
        x, y = [int(n) for n in rg.split('-')]
        as_range = range(x - 1, y)
        df.iloc[as_range] = True
    return df


def parse_disembl_globplot(text, seq, modes, basename):
    """
    text is a page in disembl/globplot format
    """
    # we can't use the raw scores, cause the software uses internal hidden
    # thresholds that are even inconsistent within one sequence
    ranges = {}
    # get ranges of disordered regions
    for mode in modes:
        # find ranges in text
        regions = re.search(f'none_{mode}.*\n(.*)<br>', text).group(1).split(', ')
        ranges[f'{basename}_{mode}'] = regions

    dfs = []
    for mode, regions in ranges.items():
        df = ranges2frame(regions, seq, mode)
        dfs.append(df)
    return pd.concat(dfs, axis=1)


def parse_fasta(fasta_text, name=None):
    sequences = defaultdict(str)
    current_seq = None
    none_count = 0
    for line in fasta_text.split('\n'):
        line = line.strip()
        if not line:
            current_seq = None
        elif line.startswith(">"):
            current_seq = slugify(line[1:].strip(), separator='_', lowercase=False)
        else:
            if current_seq is None:
                current_seq = f'none_{none_count}'
                none_count += 1
            sequences[current_seq] += line.translate(str.maketrans('', '', ' \t')).upper()
    if name and len(sequences) == 1:
        sequences = {name: list(sequences.values())[0]}
    return sequences
