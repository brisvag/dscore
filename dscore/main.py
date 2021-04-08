import asyncio

import pandas as pd

from .servers import get_functions


async def event_loop(seq):
    tasks = [asyncio.create_task(func(seq)) for func in get_functions.values()]
    results = await asyncio.gather(*tasks)
    seq_column = pd.DataFrame({'residue': list(seq)})
    merged = pd.concat([seq_column] + results, axis=1)
    return merged


def main(seq):
    result = asyncio.run(event_loop(seq))
    return result
