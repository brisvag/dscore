import requests
from xml.dom.minidom import parseString

import numpy as np
import pandas as pd

from ..utils import retry, ensure_and_log


submit_base_url = 'https://fold.proteopedia.org/cgi-bin/findex?m=xml&sq='


@retry()
def submit_and_get_result(seq):
    submit_url = submit_base_url + seq
    r = requests.get(submit_url)
    r.raise_for_status()
    xml = parseString(r.text)
    segments = xml.getElementsByTagName('segment')
    result = np.zeros(len(seq), dtype=bool)
    for seg in segments:
        start = int(seg.getAttribute('start'))
        end = int(seg.getAttribute('end'))
        result[start - 1: end] = True

    return pd.DataFrame({'foldindex': result})


@ensure_and_log
async def get_foldindex(seq):
    return await submit_and_get_result(seq)
