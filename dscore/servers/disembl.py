import re
import requests

from .utils import csv2frame, retry


submit_base_url = 'http://dis.embl.de/cgiDict.py?key=process&sequence_string='
result_base_url = 'http://dis.embl.de/'


def submit(seq):
    submit_job = requests.get(submit_base_url + seq)
    submit_job.raise_for_status()
    result_url = result_base_url + re.search('DisEMBLout/\w+.disEMBL', submit_job.text).group()
    return result_url


@retry
def get_result(output_url):
    r = requests.get(output_url)
    r.raise_for_status()
    return r.text.strip()


def parse_result(text):
    # TODO
    return csv2frame(text)


def get_disembl(seq):
    result_url = submit(seq)
    raw_output = get_result(result_url)
    return parse_result(raw_output)
