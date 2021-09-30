from pathlib import Path
import pandas as pd
import re


def save_file(text, path):
    path = Path(path)
    if path.exists():
        bak = path.with_suffix(path.suffix + '.bak')
        path.rename(bak)
    with open(path, 'w+') as f:
        f.write(text)


def read_dscore(dscore_or_csv):
    path = Path(dscore_or_csv)
    with open(dscore_or_csv, 'r') as f:
        if path.suffix == '.dscore':
            columns = []
            while True:
                line = f.readline()
                if match := re.match('# \d+\. (.*)$', line):
                    columns.append(match.group(1))
                elif line.startswith('-'):
                    break
            df = pd.read_csv(f, sep='\s+', names=columns)
            df.iloc[:, 2:] = df.iloc[:, 2:].replace('-', False)
            df.iloc[:, 2:] = df.iloc[:, 2:].replace('D', True)
        else:
            df = pd.read_csv(path, sep=' ')
            df.iloc[:, 2:] = df.iloc[:, 2:].replace(0, False)
            df.iloc[:, 2:] = df.iloc[:, 2:].replace(1, True)

    # make sure to use float and not object
    df['dscore'] = df['dscore'].astype(float)
    return df
