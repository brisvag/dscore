from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import pandas as pd
import numpy as np

from ..utils import retry, JobNotDone, ensure_and_log

import logging
logger = logging.getLogger(__name__)


base_url = 'http://old.protein.bio.unipd.it/espritz/'


def submit(seq, mode='X-Ray'):
    # ">" symbol is needed for this server to recognise as fasta
    seq = '> none\n' + seq
    driver = webdriver.Firefox()
    driver.get(base_url)
    driver.find_element(By.ID, 'sequence').send_keys(seq)
    mode_selector = Select(driver.find_element(By.NAME, 'model'))
    mode_selector.select_by_visible_text('NMR')
    submit = driver.find_element(By.NAME, 'Submit Query')
    # workaround from https://stackoverflow.com/questions/49252880/element-is-not-clickable-at-point-x-y-5-because-another-element-obscures-it
    driver.execute_script("arguments[0].click();", submit)
    return driver


@retry(max_time=3600)   # 30 minutes! This is very slow...
def get_result(driver):
    if driver.find_element(By.XPATH, '/html/body/div[4]/p/span').text != 'finished':
        raise JobNotDone
    # open text results
    result_url = driver.find_element(By.XPATH, '/html/body/div[6]/table/tbody/tr[3]/td[2]/a').get_property('href')
    # open results
    driver.get(result_url)
    result = driver.find_element(By.XPATH, '/html/body/pre').text
    driver.quit()
    return result


def parse_result(result, mode):
    dis_seq = result.split()[::2]  # a bit ugly, but works
    dis_array = np.array([x == 'D' for x in dis_seq])
    df = pd.DataFrame({f'espritz_{mode}': dis_array})
    return df


async def get_espritz_mode(seq, mode):
    logger.debug(f'submitting mode: {mode}')
    submitted_driver = submit(seq, mode=mode)
    logger.debug(f'waiting for results mode: {mode}')
    result = await get_result(submitted_driver)
    return parse_result(result, mode)


@ensure_and_log
async def get_espritz_xray(seq):
    return await get_espritz_mode(seq, 'X-Ray')


@ensure_and_log
async def get_espritz_disprot(seq):
    return await get_espritz_mode(seq, 'Disprot')


@ensure_and_log
async def get_espritz_nmr(seq):
    return await get_espritz_mode(seq, 'NMR')
