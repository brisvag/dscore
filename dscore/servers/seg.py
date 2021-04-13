import re

from selenium import webdriver

from ..utils import ranges2frame


base_url = 'https://mendel.imp.ac.at/METHODS/seg.server.html'


def submit_and_get_result(seq):
    with webdriver.Firefox() as driver:
        driver.get(base_url)
        driver.find_element_by_name('Sequence').send_keys(seq)
        driver.find_element_by_xpath('/html/body/a/form/pre/p[1]/input[1]').click()
        # get result text
        result = driver.find_element_by_xpath('/html/body/pre').text
    return result


def parse_result(result, seq):
    ranges = []
    for line in result.split('\n'):
        # TODO: now it's stuff on the right that's considered disordered. Is it correct?
        if rg := re.search(r'\s+(\d+-\d+)\s+\w+', line):
            ranges.append(rg.group(1))
    return ranges2frame(ranges, seq, 'seg')


def get_seg(seq):
    result = submit_and_get_result(seq)
    return parse_result(result)
