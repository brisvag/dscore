import requests

from ..utils import parse_disembl_globplot, ensure_and_log

import logging
logger = logging.getLogger(__name__)


submit_base_url = 'http://dis.embl.de/cgiDict.py?key=process&sequence_string='


def submit_and_get_result(seq):
    submit_job = requests.get(submit_base_url + seq)
    submit_job.raise_for_status()
    result = submit_job.text
    return result


def parse_result(text, seq):
    modes = ['LOOPS', 'HOTLOOPS', 'REM465']
    basename = 'disembl'
    return parse_disembl_globplot(text, seq, modes, basename)


@ensure_and_log
async def get_disembl(seq):
    logger.debug('submitting')
    result = submit_and_get_result(seq)
    logger.debug('parsing')
    return parse_result(result, seq)
