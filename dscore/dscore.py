import threading
import asyncio
from pathlib import Path
from time import sleep

import pandas as pd
from rich.progress import Progress

from .servers import sequence_disorder, sequence_complexity
from .utils import pre_format_result, parse_fasta, write_csv, write_score, dscore_plot, servers_plot, consensus_plot


import logging
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
        func = sequence_disorder.get(server, None)
        if func is None:
            func = sequence_complexity.get(server, None)
        if func is None:
            raise ValueError(f'cannot recognize server "{server}"')
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


def wait_threads(threads, progress, name):
    """
    wait for threads to finish, but fail gracefully if interrupted
    """
    all_threads = [thread.name for thread in threads]
    task = progress.add_task(f'querying servers for {name}', total=len(all_threads))
    try:
        while not_done := [thread.name for thread in threads if thread.is_alive()]:
            progress.update(task, completed=len(all_threads) - len(not_done))
            logger.info(f'the following servers are not yet done: {not_done}')
            sleep(3)
        else:
            progress.update(task, completed=len(all_threads))
    except KeyboardInterrupt:
        return
    return


def run_multiple_sequences(sequences, server_list, progress):
    results = {}
    for name, seq in sequences.items():
        df = pd.DataFrame()
        threads = start_threads(seq, server_list, df)
        wait_threads(threads, progress, name)
        results[name] = df
    return results


def _parse_inputs(seq, save_dir):
    save_path = Path(save_dir)
    if save_path.is_file():
        raise ValueError('target path must be a directory')

    if Path(seq).exists():
        with open(seq, 'r') as f:
            seq = f.read()
    sequences = parse_fasta(seq)
    return sequences, save_path


def dscore(seq, save_as_csv=False, save_dir='.', name=None, server_list=None, ignore=()):
    sequences, save_path = _parse_inputs(seq, save_dir)

    # metapredict is a meta-result and includes many servers we already use,
    # so it should be ignored for the purposes of dscore calculation
    ignore = ['metapredict'] + list(ignore)

    if server_list is None:
        server_list = sequence_disorder.keys()

    with Progress() as progress:
        results = run_multiple_sequences(sequences, server_list, progress)

        for name, df in progress.track(results.items(), description='interpreting results'):
            res = pre_format_result(df, sequences[name], score_type='d')
            # reorder columns so ignored and dscore at the end
            at_end = [col for col in ignore if col in res.columns] + ['dscore']
            columns = [col for col in res.columns if col not in at_end] + at_end
            results[name] = res[columns]

        save_path.mkdir(parents=True, exist_ok=True)
        for name, df in progress.track(results.items(), description='writing outputs and plotting'):
            if save_as_csv:
                write_csv(df, name, save_path, score_type='d')
            else:
                write_score(df, name, save_path, score_type='d')
            dscore_plot(df, name, save_path)
            servers_plot(df, name, save_path)
            consensus_plot(df, name, save_path)
    return results


def cscore(seq, save_as_csv=False, save_dir='.', name=None):
    sequences, save_path = _parse_inputs(seq, save_dir)

    server_list = sequence_complexity.keys()
    results = run_multiple_sequences(sequences, server_list)

    for name, df in results.items():
        results[name] = pre_format_result(df, sequences[name], score_type='c')

    save_path.mkdir(parents=True, exist_ok=True)
    for name, df in results.items():
        if save_as_csv:
            write_csv(df, name, save_path, score_type='c')
        else:
            write_score(df, name, save_path, score_type='c')
    return results
