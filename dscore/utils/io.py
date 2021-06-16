from pathlib import Path


def save_file(text, path):
    path = Path(path)
    if path.exists():
        bak = path.with_suffix(path.suffix + '.bak')
        path.rename(bak)
    with open(path, 'w+') as f:
        f.write(text)
