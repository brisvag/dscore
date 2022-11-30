from selenium import webdriver
from selenium.webdriver.common.by import By

from ..utils import csv2frame, ensure_and_log

import logging
logger = logging.getLogger(__name__)


base_url = 'https://iupred3.elte.hu/'
cutoff = 0.5


def submit_and_get_result(seq, mode):
    with webdriver.Firefox() as driver:
        driver.get(base_url)
        # submit sequence
        driver.find_element(By.ID, 'inp_seq').send_keys(seq)
        driver.find_element(By.ID, f'context_selector_{mode}').click()
        driver.find_element(By.CLASS_NAME, 'btn').click()
        # get raw text result link
        menu = driver.find_element(By.CLASS_NAME, 'dropdown-menu')
        result_url = menu.find_elements(By.TAG_NAME, 'a')[0].get_property('href')
        # open results
        driver.get(result_url)
        result = driver.find_element(By.XPATH, '//html/body/pre').text
    return result


def parse_result(result, mode):
    df = csv2frame(result)[[2]]
    df.columns = [f'iupred_{mode}']
    return df >= cutoff


def get_iupred_mode(seq, mode):
    logger.debug(f'submitting mode: {mode}')
    result_raw = submit_and_get_result(seq, mode)
    logger.debug('parsing results for mode: {mode}')
    result = parse_result(result_raw, mode)
    return result


@ensure_and_log
async def get_iupred_long(seq):
    return get_iupred_mode(seq, 'long')


@ensure_and_log
async def get_iupred_short(seq):
    return get_iupred_mode(seq, 'short')
