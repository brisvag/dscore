import pandas as pd


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
