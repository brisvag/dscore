from collections import defaultdict
from io import StringIO
import re

import numpy as np
import pandas as pd
from slugify import slugify


def csv2frame(string, header=None, **kwargs):
    """
    read a csv string into a dataframe. Takes kwargs from pd.read_csv().
    """
    stream = StringIO(string)
    defaults = dict(delim_whitespace=True, header=header, comment='#')
    defaults.update(kwargs)
    return pd.read_csv(stream, **defaults)


def frame_from_ranges(seq, ranges):
    empty = np.zeros((len(seq), len(ranges)), dtype=bool)
    result = pd.DataFrame(empty, columns=ranges.keys())
    for mode, regions in ranges.items():
        for region in regions:
            # convert in python range objects
            x, y = [int(n) for n in region.split('-')]
            as_range = range(x - 1, y)
            result[mode].iloc[as_range] = True
    return result


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
        regions = re.search(f'none_{mode}.*\n(.*)\n?<br>', text).group(1)
        if regions == 'none':
            regions = []
        else:
            regions = regions.split(', ')
        ranges[f'{basename}_{mode}'] = regions

    result = frame_from_ranges(seq, ranges)
    return result


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
