import pandas as pd
import tabulate


def format_result(result, seq):
    # 1-numbered is convention
    result.index += 1
    result.index.name = 'resn'
    # D and - are more readable than True and False
    result[result == True] = 'D'  # noqa
    result[result == False] = '-'  # noqa
    # add residue column
    seq_column = pd.DataFrame({'residue': list(seq)}, index=range(1, len(seq) + 1))
    merged = pd.concat([seq_column, result], axis=1)
    return merged


def save_csv(result, path):
    result.to_csv(path, sep=' ')


def save_dscore(result, path):
    # header
    header = []
    for i, col_name in enumerate(result.columns):
        header.append(f'# {i}. {col_name}')
    header = '\n'.join(header)
    # tabulated data
    tabulated = tabulate(result, headers=range(len(result.columns) + 1))
    text = header + '\n' + tabulated
    with open(path, 'w+') as f:
        f.write(text)
