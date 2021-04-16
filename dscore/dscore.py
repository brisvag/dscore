import asyncio
from secrets import token_hex
from pathlib import Path

import pandas as pd

from .servers import sequence_disorder
from .utils import format_result, save_csv, save_dscore


import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def _run_all_servers(seq):
    tasks = [asyncio.create_task(func(seq)) for func in sequence_disorder]
    results = await asyncio.gather(*tasks)
    # discard failed ones and merge
    results = [r for r in results if r is not None]
    merged = pd.concat(results, axis=1)
    return merged


def run_all(seq):
    result = asyncio.run(_run_all_servers(seq))
    formatted = format_result(result)
    return formatted


def dscore(seq, save_as_dscore=False, save_as_csv=False, save_path='.', base_name=None):
    result = run_all(seq)
    if base_name is None:
        base_name = str(token_hex(4))
    save_path = Path(save_path)
    if save_as_dscore:
        path_dscore = save_path / (base_name + '.dscore')
        save_dscore(result, path_dscore)
    if save_as_csv:
        path_csv = save_path / (base_name + '.csv')
        save_csv(result, path_csv)
    return result
