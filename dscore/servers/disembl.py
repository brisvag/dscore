import re
import requests

import numpy as np
import pandas as pd


submit_base_url = 'http://dis.embl.de/cgiDict.py?key=process&sequence_string='


def submit_and_get_result(seq):
    submit_job = requests.get(submit_base_url + seq)
    submit_job.raise_for_status()
    result = submit_job.text
    return result


def parse_result(text, seq):
    # we can't use the raw scores, cause the software uses internal hidden
    # thresholds that are even inconsistent within one sequence
    ranges = {}
    modes = ['LOOPS', 'HOTLOOPS', 'REM465']
    # get ranges of disordered regions
    for mode in modes:
        # find ranges in text
        regions = re.search(f'none_{mode}.*\n(.*)<br>', text).group(1).split(', ')
        rg = []
        # convert in python range objects
        for r in regions:
            x, y = [int(n) for n in r.split('-')]
            rg.append(range(x - 1, y))
        ranges[f'disembl_{mode}'] = rg
    # construct dataframe with bool values
    modes_full = [f'disembl_{mode}' for mode in modes]
    df = pd.DataFrame(np.zeros((len(seq), len(modes)), dtype=bool), columns=modes_full)
    for mode, regions in ranges.items():
        for rg in regions:
            df[mode].iloc[rg] = True
    return df


def get_disembl(seq):
    result = submit_and_get_result(seq)
    return parse_result(result, seq)
