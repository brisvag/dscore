import re
from collections import defaultdict

from selenium import webdriver
from selenium.webdriver.common.by import By

from ..utils import frame_from_ranges, ensure_and_log


base_url = 'https://mendel.imp.ac.at/METHODS/seg.server.html'


def submit_and_get_result(seq):
    with webdriver.Firefox() as driver:
        driver.get(base_url)
        input_el = driver.find_element(By.NAME, 'Sequence')
        input_el.click()  # needed otherwise clicks are not registered
        input_el.send_keys(seq)
        driver.find_element(By.XPATH, '/html/body/a/form/pre/p[1]/input[1]').click()
        # get result text
        result = driver.find_element(By.XPATH, '/html/body/pre').text
    return result


def parse_result(result, seq):
    regions = defaultdict(list)
    current = ''
    for line in result.split('\n'):
        if header := re.search(r'low complexity.*SEG\s+(\d+)', line):
            current = f'SEG_{header.group(1)}'
        # TODO: now it's stuff on the right that's considered disordered. Is it correct?
        if rg := re.search(r'\s+(\d+-\d+)\s+\w+', line):
            regions[current].append(rg.group(1))
    # compared to other servers using ranges, this gives the opposite, so we need to negate it
    return ~frame_from_ranges(seq, regions)


@ensure_and_log
async def get_seg(seq):
    result = submit_and_get_result(seq)
    return parse_result(result, seq)
