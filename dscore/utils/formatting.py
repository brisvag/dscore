import pandas as pd


def pre_format_result(result, seq, score_type='d', exclude=()):
    result = result.copy()
    # ignore excluded columns from score and get score
    score = result.drop(columns=exclude, errors='ignore').mean(axis=1).astype(float)
    result[score_type + 'score_raw'] = 1 - score
    result[score_type + 'score'] = score >= 0.5
    # add residue column
    seq_column = pd.DataFrame({'residue': list(seq)})
    merged = pd.concat([seq_column, result], axis=1)
    # 1-numbered is convention
    merged.index += 1
    merged.index.name = 'resn'
    return merged
