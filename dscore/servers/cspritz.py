from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
import numpy as np

from ..utils import retry, JobNotDone, ensure_and_log

import logging
logger = logging.getLogger(__name__)


base_url = 'http://old.protein.bio.unipd.it/cspritz/'


def submit(seq, mode='long'):
    # ">" symbol is needed for this server to recognise as fasta
    seq = '> none\n' + seq
    driver = webdriver.Firefox()
    driver.get(base_url)
    driver.find_element(By.ID, 'sequence').send_keys(seq)
    # submit. This is an ugly xpath... I hope it stays as is
    xpath = f'html/body/div[4]/form/fieldset[3]/table/tbody/tr[2]/td/select/option[contains(text(), "{mode}")]'
    mode_selector = driver.find_element(By.XPATH, xpath)
    mode_selector.click()
    driver.find_element(By.NAME, 'Submit Query').click()
    return driver


@retry(max_time=3600)   # 30 minutes! This is very slow...
def get_result(driver):
    if driver.find_element(By.XPATH, '/html/body/div[4]/p/span').text != 'finished':
        raise JobNotDone
    # open text results
    result_url = driver.find_element(By.XPATH, '/html/body/div[6]/center/b/table/tbody/tr[2]/td[2]/a').get_property('href')
    # open results
    driver.get(result_url)
    result = driver.find_element(By.XPATH, '/html/body/pre').text
    driver.quit()
    return result


def parse_result(result, mode):
    dis_seq = result.split()[-3]  # a bit ugly, but works
    dis_array = np.array([x == 'D' for x in dis_seq])
    df = pd.DataFrame({f'cspritz_{mode}': dis_array})
    return df


async def get_cspritz_mode(seq, mode):
    logger.debug(f'submitting mode: {mode}')
    submitted_driver = submit(seq, mode=mode)
    logger.debug(f'waiting for results mode: {mode}')
    result = await get_result(submitted_driver)
    return parse_result(result, mode)


@ensure_and_log
async def get_cspritz_long(seq):
    return await get_cspritz_mode(seq, 'long')


@ensure_and_log
async def get_cspritz_short(seq):
    return await get_cspritz_mode(seq, 'short')
