import threading
import asyncio
from pathlib import Path
from time import sleep

import pandas as pd

from .servers import sequence_disorder
from .utils import pre_format_result, as_csv, as_dscore, save_file, parse_fasta


import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def prepare_threads(seq, server_list, df):
    """
    for each server in the server list, create a thread
    with a target function that submits and receives from the server
    and updates the main df with the result
    """
    # may not be necessary, but better safe than sorry
    lock = threading.Lock()

    def update_df(coroutine, seq):
        """
        run server coroutine and dump results in the main dataframe
        """
        result = asyncio.run(coroutine(seq))
        if result is not None:
            lock.acquire()
            for colname, data in result.items():
                df[colname] = data
            lock.release()

    threads = []
    for server in server_list:
        if server not in sequence_disorder:
            raise ValueError(f'cannot recognize server "{server}"')
        func = sequence_disorder.get(server)
        threads.append(threading.Thread(target=update_df, args=(func, seq), name=server))
    return threads


def start_threads(seq, server_list, df):
    """
    start all the threads, using dataframe that will be updated live
    as results come in. Also return the threads.
    """
    threads = prepare_threads(seq, server_list, df)
    for thread in threads:
        thread.start()
    return threads


def wait_threads(threads):
    """
    wait for threads to finish, but fail gracefully if interrupted
    """
    try:
        while not_done := [thread.name for thread in threads if thread.is_alive()]:
            logger.info(f'the following servers are not yet done: {not_done}')
            sleep(5)
    except KeyboardInterrupt:
        return
    return


def run_multiple_sequences(sequences, server_list):
    results = {}
    for name, seq in sequences.items():
        df = pd.DataFrame()
        threads = start_threads(seq, server_list, df)
        wait_threads(threads)
        results[name] = df
    return results


def dscore(seq, save_as_dscore=False, save_as_csv=False, save_dir='.', name=None, server_list=None):
    save_path = Path(save_dir)
    if save_path.is_file():
        raise ValueError('target path must be a directory')

    if server_list is None:
        server_list = sequence_disorder.keys()
    if Path(seq).exists():
        with open(seq, 'r') as f:
            seq = f.read()
    sequences = parse_fasta(seq)

    results = run_multiple_sequences(sequences, server_list)

    for name, df in results.items():
        results[name] = pre_format_result(df, sequences[name])

    save_path.mkdir(parents=True, exist_ok=True)
    to_save = {}
    for name, df in results.items():
        if save_as_dscore:
            path_dscore = save_path / (name + '.dscore')
            to_save[path_dscore] = as_dscore(df)
        if save_as_csv:
            path_csv = save_path / (name + '.csv')
            to_save[path_csv] = as_csv(df)

    for path, text in to_save.items():
        save_file(text, path)
    return results
