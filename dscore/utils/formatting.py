import pandas as pd
from tabulate import tabulate


def pre_format_result(result, seq):
    result = result.copy()
    # D and - are more readable than True and False
    result[result == True] = 'D'  # noqa
    result[result == False] = '-'  # noqa
    # add residue column
    seq_column = pd.DataFrame({'residue': list(seq)})
    merged = pd.concat([seq_column, result], axis=1)
    # 1-numbered is convention
    merged.index += 1
    merged.index.name = 'resn'
    return merged


def as_csv(result):
    return result.to_csv(sep=' ')


def as_dscore(result):
    # header
    header = [f'# {0}. {result.index.name}']
    for i, col_name in enumerate(result.columns):
        header.append(f'# {i + 1}. {col_name}')
    header = '\n'.join(header)
    # tabulated data
    tabulated = tabulate(result, headers=range(len(result.columns) + 1))
    text = header + '\n' + tabulated
    return text
