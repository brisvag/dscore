from io import StringIO
from time import sleep

import pandas as pd
from selenium import webdriver


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
    def wrapper(*args, **kwargs):
        attempt = 1
        retries = []
        fails = []
        while True:
            try:
                print(f'running {func} for the {attempt} time')
                ret = func(*args, **kwargs)
            except JobNotDone as e:
                retries.append(e)
                sleep(10)
            except Exception as e:
                attempt += 1
                fails.append(e)  # TODO do something with this
                if attempt >= 10:
                    break
                sleep(10)
            else:
                return ret
        else:
            raise IOError(f'could not get anything from {func.__name__}')

    return wrapper


class JobNotDone(RuntimeError):
    pass
