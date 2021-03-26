import re
from time import sleep
from pathlib import Path
import tempfile
import shutil

import jpredapi

seq = 'MQVWPIEGIKKFETLSYLPP'
silent = True
dest_dir = Path('.')
dest_file = dest_dir / 'jpred.fasta'

wait = 10


request_job = jpredapi.submit(mode='single', user_format='raw', seq='MQVWPIEGIKKFETLSYLPP', silent=silent)

if not request_job:
    raise ConnectionError(request_job.status_code)

jobid = re.search('jp_.*', request_job.headers['Location']).group()

with tempfile.TemporaryDirectory() as temp_dir:
    finished = False
    while not finished:
        sleep(wait)
        result = jpredapi.get_results(jobid, results_dir_path=temp_dir, extract=True, silent=silent)
        finished = 'finished' in result.text.lower()

    jobdir = Path(temp_dir) / jobid
    fasta = jobdir / f'{jobid}.concise.fasta'

    shutil.copy(fasta, dest_file)
