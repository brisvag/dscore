import asyncio
from pathlib import Path

import pandas as pd

from .servers import sequence_disorder
from .utils import pre_format_result, as_csv, as_dscore, save_file


import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def prepare_tasks(seq, server_list):
    tasks = []
    for server in server_list:
        if server not in sequence_disorder:
            raise ValueError(f'cannot recognize server "{server}"')
        coroutine = sequence_disorder.get(server)
        tasks.append(asyncio.create_task(coroutine(seq)))
    return tasks


async def run_servers_coroutine(seq, server_list):
    tasks = prepare_tasks(seq, server_list)
    results = await asyncio.gather(*tasks)
    # discard failed ones and merge
    results = [r for r in results if r is not None]
    merged = pd.concat(results, axis=1)
    return merged


def run_servers(seq, server_list):
    return asyncio.run(run_servers(seq, server_list))


def run_all(seq):
    return asyncio.run(run_servers(seq, sequence_disorder.keys()))


def dscore(seq, save_as_dscore=False, save_as_csv=False, save_path='.', name=None, server_list=None):
    if server_list is None:
        server_list = sequence_disorder.keys()
    result = pre_format_result(run_servers(seq, server_list))
    if name is None:
        name = f'{seq[:15]}'
    save_path = Path(save_path)
    to_save = {}
    if save_as_dscore:
        path_dscore = save_path / (name + '.dscore')
        to_save[path_dscore] = as_dscore(result, path_dscore)
    if save_as_csv:
        path_csv = save_path / (name + '.csv')
        to_save[path_csv] = as_csv(result, path_csv)

    for path, text in to_save.items():
        save_file(text, path)
    return result
