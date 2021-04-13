from io import StringIO
import asyncio
import logging
import time
import re

import numpy as np
import pandas as pd


def retry(func):
    """
    decorator that makes a request-based function run until it works
    if the failure is recognised simply as an incomplete job, continue indefinitely
    otherwise, stop after 10 failures
    """
    # unit: seconds
    wait_time = 10
    max_fails = 10
    max_time = 600
    logger = logging.getLogger(func.__module__)

    async def wrapper(*args, **kwargs):
        failed = 0
        retries = []
        fails = []

        start_time = time.time()
        while True:
            elapsed = time.time() - start_time
            logger.debug(f'retrying: {elapsed=:.0f}, {max_time=:.0f}, {failed=}')
            try:
                ret = func(*args, **kwargs)
            except JobNotDone as e:
                retries.append(e)
                logger.debug(f'job not done yet. Retrying in {wait_time}')
                await asyncio.sleep(wait_time)
            except Exception as e:
                fails.append(e)
                logger.debug(f'failed with {e.__class__}. Retrying in {wait_time}')
                failed += 1
                if failed >= max_fails:
                    break
                await asyncio.sleep(wait_time)
            else:
                logger.debug('retrying succeeded')
                return ret
        raise IOError(f'could not get anything from {func.__name__}')

    return wrapper


class JobNotDone(RuntimeError):
    pass


def ensure_and_log(coroutine):
    """
    logs the execution of a coroutine and ensures that it fails gracefully
    """
    logger = logging.getLogger(coroutine.__module__)

    async def wrapper(*args, **kwargs):
        try:
            logger.info(f'"{coroutine.__name__}" started')
            result = await coroutine(*args, **kwargs)
        except Exception:
            logger.exception(f'"{coroutine.__name__}" failed, skipping from results')
            result = None

        logger.info(f'"{coroutine.__name__}" finished')
        return result

    return wrapper


def csv2frame(string, **kwargs):
    """
    read a csv string into a dataframe. Takes kwargs from pd.read_csv().
    """
    stream = StringIO(string)
    defaults = dict(delim_whitespace=True, header=None, comment='#')
    defaults.update(kwargs)
    return pd.read_csv(stream, **defaults)


def ranges2frame(ranges, seq, col_name):
    df = pd.DataFrame(np.zeros(len(seq)), dtype=bool, columns=[col_name])
    for rg in ranges:
        # convert in python range objects
        x, y = [int(n) for n in rg.split('-')]
        as_range = range(x - 1, y)
        df.iloc[as_range] = True
    return df


def parse_disembl_globplot(text, seq, modes, basename):
    """
    text is a page in disembl/globplot format
    """
    # we can't use the raw scores, cause the software uses internal hidden
    # thresholds that are even inconsistent within one sequence
    ranges = {}
    # get ranges of disordered regions
    for mode in modes:
        # find ranges in text
        regions = re.search(f'none_{mode}.*\n(.*)<br>', text).group(1).split(', ')
        ranges[f'{basename}_{mode}'] = regions

    dfs = []
    for mode, regions in ranges.items():
        df = ranges2frame(regions, seq, mode)
        dfs.append(df)
    return pd.concat(dfs, axis=1)
