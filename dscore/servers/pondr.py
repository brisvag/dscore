from selenium import webdriver
from selenium.webdriver.common.by import By

from ..utils import csv2frame, ensure_and_log


base_url = 'http://www.pondr.com/'
cutoff = 0.5
modes = ('VLXT', 'XL1', 'CAN', 'VL3', 'VSL2')
mode_headers = ('VLXT', 'XL1_XT', 'CAN_XT', 'VL3', 'VSL2')


def submit_and_get_result(seq):
    with webdriver.Firefox() as driver:
        driver.get(base_url)
        # enable all modes
        for mode in modes:
            checkbox = driver.find_element(By.NAME, mode)
            if not checkbox.is_selected():
                checkbox.click()

        base_xpath = '/html/body/form[2]/table/tbody'
        # dummy name
        driver.find_element(By.XPATH, base_xpath + '/tr[3]/td[2]/input').send_keys('none')
        # input sequence
        driver.find_element(By.XPATH, base_xpath + '/tr[8]/td[2]/textarea').send_keys(seq)
        # only raw data checkbox
        checkboxes_xpath = base_xpath + '/tr[9]/td[2]/table/tbody'
        for xpath in ('/tr[1]/td[1]/label/input', '/tr[1]/td[4]/label/input', '/tr[2]/td[1]/label/input'):
            checkbox = driver.find_element(By.XPATH, checkboxes_xpath + xpath)
            if checkbox.is_selected():
                checkbox.click()
        raw_checkbox = driver.find_element(By.XPATH, checkboxes_xpath + '/tr[2]/td[4]/label/input')
        if not raw_checkbox.is_selected():
            raw_checkbox.click()
        # submit
        driver.find_element(By.NAME, 'submit_result').click()

        # extract result text
        result = driver.find_element(By.XPATH, '/html/body/pre[6]').text
    return result


def parse_result(result):
    df = csv2frame(result, header=0)
    df = df[list(mode_headers)]
    df.columns = [f'pondr_{mode}' for mode in mode_headers]
    return df >= cutoff


@ensure_and_log
async def get_pondr(seq):
    result = submit_and_get_result(seq)
    return parse_result(result)
