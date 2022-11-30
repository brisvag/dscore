import requests

from ..utils import csv2frame, retry, JobNotDone, ensure_and_log

import logging
logger = logging.getLogger(__name__)


base_url = 'http://bioinf.cs.ucl.ac.uk/psipred/api'


def submit(seq):
    payload = {'input_data': ('prot.txt', seq)}
    data = {'job': 'disopred',
            'submission_name': 'dscore',
            'email': 'none@example.com'}
    r = requests.post(base_url + '/submission.json', data=data, files=payload)
    r.raise_for_status()
    UUID = r.json()['UUID']
    job_url = f'{base_url}/submission/{UUID}?format=json'
    return job_url


@retry()
def get_result_location(job_url):
    r = requests.get(job_url)
    r.raise_for_status()
    if r.json()['state'] != 'Complete':
        raise JobNotDone
    tasks = r.json()['submissions'][0]['results']
    tasks = {t['name']: t['data_path'] for t in tasks}
    return tasks['diso_combine']


@retry()
def get_result(result_url):
    res = requests.get(base_url + result_url)
    res.raise_for_status()
    return res.text


def parse_result(result):
    data = csv2frame(result)
    as_bool = data[[2]] == '*'
    as_bool.columns = ['disopred3.1']
    return as_bool


@ensure_and_log
async def get_disopred(seq):
    logger.debug('submitting')
    job_url = submit(seq)
    logger.debug('waiting for result')
    res_url = await get_result_location(job_url)
    logger.debug('fetching result')
    result = await get_result(res_url)
    return parse_result(result)
