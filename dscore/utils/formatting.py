import pandas as pd
from tabulate import tabulate


def pre_format_result(result, seq):
    result = result.copy()
    # add dscore
    dscore = result.mean(axis=1)
    result['dscore'] = dscore
    result['dscore_cutoff'] = dscore >= 0.5
    # add residue column
    seq_column = pd.DataFrame({'residue': list(seq)})
    merged = pd.concat([seq_column, result], axis=1)
    # 1-numbered is convention
    merged.index += 1
    merged.index.name = 'resn'
    return merged


def as_csv(result):
    result = result.replace(True, 1)
    result = result.replace(False, 0)
    return result.infer_objects().to_csv(sep=' ')


def as_dscore(result):
    # header
    # D and - are more readable than True and False
    result = result.replace(True, 'D')
    result = result.replace(False, '-')
    header = [f'# {0}. {result.index.name}']
    for i, col_name in enumerate(result.columns):
        header.append(f'# {i + 1}. {col_name}')
    header = '\n'.join(header)
    # tabulated data
    tabulated = tabulate(result, headers=range(len(result.columns) + 1))
    text = header + '\n' + tabulated
    return text
