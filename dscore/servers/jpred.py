import re
from pathlib import Path
import tempfile
import pandas as pd

import jpredapi

from ..utils import retry, JobNotDone, ensure_and_log

job_in_queue = re.compile(r'currently (\d+) jobs')
job_incomplete = re.compile(r'(\d+%) complete')
job_done = re.compile('Results available')


def submit(seq):
    # remove comments from sequence, not accepted
    clean_seq = ''.join([line for line in seq.split('\n') if not line.startswith('>')])
    request_job = jpredapi.submit(mode='single', user_format='raw', seq=clean_seq, silent=True)
    request_job.raise_for_status()
    job_id = re.search('jp_.*', request_job.headers['Location']).group()
    return job_id


@retry()
def get_result(job_id):
    with tempfile.TemporaryDirectory() as temp_dir:
        res = jpredapi.status(job_id, results_dir_path=temp_dir, extract=True, silent=True)
        res.raise_for_status()

        if match := job_in_queue.search(res.text):
            raise JobNotDone(f'job {job_id} is in queue after {match.group(1)} other jobs')
        elif match := job_incomplete.search(res.text):
            raise JobNotDone(f'job {job_id} is not complete yet ({match.group(1)})')
        elif job_done.search(res.text):
            result_file = Path(temp_dir) / job_id / f'{job_id}.concise.fasta'
            with open(result_file, 'r') as f:
                result = f.read()
        else:
            raise RuntimeError('request status was ok, but reponse was unrecognizable')
    return result


def parse_result(result):
    # split results and remove newlines from sequence
    all_results = [res.partition('\n') for res in result.split('>') if res]
    all_results = {k: v.replace('\n', '') for (k, _, v) in all_results}
    # anything non-structured (marked by a `-`) is disordered
    modes = ('jnetpred', 'JNETSOL25', 'JNETSOL5', 'JNETSOL0', 'JNETHMM', 'JNETPSSM')
    df = pd.DataFrame({f'jpred_{mode}': [data == '-' for data in all_results[mode]] for mode in modes})
    return df


@ensure_and_log
async def get_jpred(seq):
    job_id = submit(seq)
    result = await get_result(job_id)
    return parse_result(result)
