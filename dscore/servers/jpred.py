import re
from pathlib import Path
import tempfile

import jpredapi

from ..utils import retry, csv2frame, JobNotDone


job_in_queue = re.compile(r'currently (\d+) jobs')
job_incomplete = re.compile(r'(\d+%) complete')
job_done = re.compile('Results available')


def submit(seq):
    request_job = jpredapi.submit(mode='single', user_format='raw', seq=seq, silent=True)
    request_job.raise_for_status()
    job_id = re.search('jp_.*', request_job.headers['Location']).group()
    return job_id


@retry
def get_result(job_id):
    with tempfile.TemporaryDirectory() as temp_dir:
        res = jpredapi.status(job_id, results_dir_path=temp_dir, extract=True, silent=True)
        res.raise_for_status()

        if match := job_in_queue.search(res.text):
            raise JobNotDone(f'job {job_id} is in queue after {match.group(1)} other jobs')
        elif match := job_incomplete.search(res.text):
            raise JobNotDone(f'job {job_id} is not complete yet {match.group(1)}')
        elif job_done.search(res.text):
            result_file = Path(temp_dir) / job_id / f'{job_id}.concise.fasta'   # TODO which file? how to parse?
            with open(result_file, 'r') as f:
                result = f.read()
        else:
            raise RuntimeError('request status was ok, but reponse was unrecognizable')
    return result


# def parse_result(result):
    # data = csv2frame(result)
    # return data


def get_jpred(seq):
    job_id = submit(seq)
    result = get_result(job_id)
    # return parse_result(result)
