import re

import numpy as np
import pandas as pd
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from ..utils import retry, JobNotDone, ensure_and_log


base_url = 'http://prdos.hgc.jp/cgi-bin/top.cgi'
cutoff = 5


def submit(seq):
    driver = webdriver.Firefox()
    driver.get(base_url)
    driver.find_element(By.NAME, 'sequence').send_keys(seq)
    # workaround from https://stackoverflow.com/questions/49252880/element-is-not-clickable-at-point-x-y-5-because-another-element-obscures-it
    submit = driver.find_element(By.XPATH, '/html/body/div[4]/form/input[2]')
    driver.execute_script("arguments[0].click();", submit)
    # need to way a bit before confirm
    try:
        confirm = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/form/input[4]'))
        )
        driver.execute_script("arguments[0].click();", confirm)
    except Exception:
        raise IOError('failed running prdos; could not find submit button')
    return driver


@retry()
def get_result(driver):
    try:
        table = driver.find_element(By.XPATH, '/html/body/div[3]/form/div[2]/table/tbody')
    except NoSuchElementException:
        raise JobNotDone
    # downloading is a pain and I wasn't able to do it automatically. We'll extract from the page instead
    dis_raw = table.find_elements(By.CLASS_NAME, 'disorder')
    disordered = []
    for el in dis_raw:
        # get residue number
        info = el.get_attribute('onmouseover')
        if g := re.search(r'(\d+)', str(info)):
            disordered.append(int(g.group(1)))
    driver.quit()
    # zero-indexed
    result = np.array(disordered) - 1
    return result


def parse_result(result, seq):
    df = pd.DataFrame(np.zeros(len(seq), dtype=bool), columns=['prdos'])
    df.iloc[result] = True
    return df


@ensure_and_log
async def get_prdos(seq):
    submitted_driver = submit(seq)
    result = await get_result(submitted_driver)
    return parse_result(result, seq)
