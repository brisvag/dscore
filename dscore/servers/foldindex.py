import requests
import json

from ..utils import retry, ensure_and_log


submit_base_url = 'https://fold.proteopedia.org/cgi-bin/findex?m=json&sq='


@retry()
def submit_and_get_result(seq):
    submit_url = submit_base_url + seq
    r = requests.get(submit_url)
    r.raise_for_status()
    data = json.loads(r.text)
    return data["findex"]


@ensure_and_log
async def get_foldindex(seq):
    return await submit_and_get_result(seq)
