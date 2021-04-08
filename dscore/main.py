import asyncio

import pandas as pd

from .servers import get_functions


async def event_loop(seq):
    tasks = [asyncio.create_task(func(seq)) for func in get_functions.values()]
    results = await asyncio.gather(*tasks)
    merged = pd.concat(results, axis=1)
    return merged


def main(seq):
    result = asyncio.run(event_loop(seq))
    return result
