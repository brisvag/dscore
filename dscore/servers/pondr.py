from selenium import webdriver

from .utils import csv2frame


base_url = 'http://www.pondr.com/'


def submit_and_get_result(seq, mode='long'):
    with webdriver.Firefox() as driver:
        driver.get(base_url)
        base_xpath = '/html/body/form[2]/table/tbody'
        # dummy name
        driver.find_element_by_xpath(base_xpath + '/tr[3]/td[2]/input').send_keys('none')
        # input sequence
        driver.find_element_by_xpath(base_xpath + '/tr[8]/td[2]/textarea').send_keys(seq)
        # only raw data checkbox
        checkboxes_xpath = base_xpath + '/tr[9]/td[2]/table/tbody'
        for xpath in ('/tr[1]/td[1]/label/input', '/tr[1]/td[4]/label/input', '/tr[2]/td[1]/label/input'):
            checkbox = driver.find_element_by_xpath(checkboxes_xpath + xpath)
            if checkbox.is_selected():
                checkbox.click()
        raw_checkbox = driver.find_element_by_xpath(checkboxes_xpath + '/tr[2]/td[4]/label/input')
        if not raw_checkbox.is_selected():
            raw_checkbox.click()
        # submit
        driver.find_element_by_xpath(base_xpath + '/tr[11]/td[2]/input[1]').click()

        # extract result text
        result = driver.find_element_by_xpath('/html/body/pre[6]').text
    return result


def parse_result(result):
    return csv2frame(result, header=0)


def get_pondr(seq):
    result = submit_and_get_result(seq)
    return parse_result(result)

