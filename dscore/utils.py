from io import StringIO
import asyncio

import pandas as pd


def csv2frame(string, **kwargs):
    """
    read a csv string into a dataframe. Takes kwargs from pd.read_csv().
    """
    stream = StringIO(string)
    defaults = dict(delim_whitespace=True, header=None, comment='#')
    defaults.update(kwargs)
    return pd.read_csv(stream, **defaults)


def retry(func):
    """
    decorator that makes a request-based function run until it works
    if the failure is recognised simply as an incomplete job, continue indefinitely
    otherwise, stop after 10 failures
    """
    async def wrapper(*args, **kwargs):
        attempt = 1
        retries = []
        fails = []
        while True:
            try:
                ret = func(*args, **kwargs)
            except JobNotDone as e:
                retries.append(e)
                await asyncio.sleep(10)
            except Exception as e:
                attempt += 1
                fails.append(e)  # TODO do something with this
                if attempt >= 10:
                    break
                await asyncio.sleep(10)
            else:
                return ret
        else:
            raise IOError(f'could not get anything from {func.__name__}')

    return wrapper


class JobNotDone(RuntimeError):
    pass
