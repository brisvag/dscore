from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException

from .utils import csv2frame, retry, JobNotDone


base_url = 'http://prdos.hgc.jp/cgi-bin/top.cgi'


def submit(seq):
    driver = webdriver.Firefox()
    driver.get(base_url)
    driver.find_element_by_name('sequence').send_keys(seq)
    # submit and confirm
    driver.find_element_by_xpath('/html/body/div[4]/form/input[2]').click()
    driver.find_element_by_xpath('/html/body/div[2]/form/input[4]').click()
    return driver


@retry
def get_result(driver):
    try:
        download_button = driver.find_element_by_xpath('/html/body/div[3]/div/form/input[2]')
    except NoSuchElementException:
        raise JobNotDone('still waiting for PrDOS')
    # TODO: how do you download, or at least avoid having to do it?
    download_button.click()
    result = None
    driver.quit()
    return result


def parse_result(result):
    return csv2frame(result, header=0)


def get_pondr(seq):
    submitted_driver = submit(seq)
    result = get_result(submitted_driver)
    return parse_result(result)
