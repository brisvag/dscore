import requests

from .utils import csv2frame, retry, JobNotDone


submit_base_url = 'http://bioinf.cs.ucl.ac.uk/psipred/api/submission.json'
result_base_url = 'http://bioinf.cs.ucl.ac.uk/psipred_new/api'


def submit(seq):
    payload = {'input_data': ('prot.txt', seq)}
    data = {'job': 'disopred',
            'submission_name': 'dscore',
            'email': 'none@example.com'}
    r = requests.post(submit_base_url, data=data, files=payload)
    r.raise_for_status()
    UUID = r.json()['UUID']
    job_url = f'{result_base_url}/submission/{UUID}?format=json'
    return job_url


@retry
def get_result_location(job_url):
    r = requests.get(job_url)
    r.raise_for_status()
    if r['state'] != 'Complete':
        raise JobNotDone('Job is not complete yet')
    result_location = r['submissions'][0]['results'][-1]['data_path']
    result_url = f'{result_base_url}{result_location}'
    return result_url


@retry
def get_result(result_url):
    res = requests.get(result_url)
    res.raise_for_status()
    return res.text


def parse_result(result):
    data = csv2frame(result)
    return data


def get_disopred(seq):
    job_url = submit(seq)
    res_url = get_result_location(job_url)
    result = get_result(res_url)
    return parse_result(result)
