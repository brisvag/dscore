import asyncio

import pandas as pd

from .servers import sequence_disorder

import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


async def event_loop(seq):
    tasks = [asyncio.create_task(func(seq)) for func in sequence_disorder]
    results = await asyncio.gather(*tasks)
    # discard failed ones
    results = [r for r in results if r is not None]
    seq_column = pd.DataFrame({'residue': list(seq)})
    merged = pd.concat([seq_column] + results, axis=1)
    return merged


def main(seq):
    result = asyncio.run(event_loop(seq))
    return result
