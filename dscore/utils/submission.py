import asyncio
import logging
import time


def retry(max_time=600):
    """
    decorator that makes a request-based function run until it works
    if the failure is recognised simply as an incomplete job, continue indefinitely
    otherwise, stop after 10 failures
    """
    # need double wrapper to allow args in decorator
    def inner_decorator(func):
        # unit: seconds
        wait_time = 10
        max_fails = 10
        logger = logging.getLogger(func.__module__)

        async def wrapper(*args, **kwargs):
            failed = 0
            retries = []
            fails = []

            start_time = time.time()
            while True:
                elapsed = time.time() - start_time
                if elapsed >= max_time:
                    break
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
    return inner_decorator


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

        else:
            logger.info(f'"{coroutine.__name__}" finished')
        return result

    return wrapper
