from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException

from .utils import csv2frame, retry, JobNotDone


base_url = 'https://www.reading.ac.uk/bioinf/IntFOLD/IntFOLD5_form.html'


# TODO: this is really slow, even with almost no queue... maybe should not use it

def submit(seq):
    driver = webdriver.Firefox()
    driver.get(base_url)
    driver.find_element_by_name('SEQUENCE').send_keys(seq)
    driver.find_element_by_xpath('/html/body/div/div[2]/div/div[1]/div/form/input[4]').click()
    result_url = driver.find_element_by_xpath('/html/body/div/div[2]/div/div[1]/div/a').get_property('href')
    driver.get(result_url)
    return driver


@retry
def get_result(driver):
    driver.refresh()
    status = driver.find_element_by_xpath('/html/body/div/div[2]/div/div[1]/div/b[1]')
    if status != 'complete':
        raise JobNotDone()
    result = None
    driver.quit()
    return result


def parse_result(result):
    return csv2frame(result)


def get_intfold(seq):
    submitted_driver = submit(seq)
    result = get_result(submitted_driver)
    return parse_result(result)
