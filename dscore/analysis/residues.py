def compute_dscore(df):
    dscore = df.mean(axis=1) >= 0.5
    df['dscore'] = dscore
    return dscore
