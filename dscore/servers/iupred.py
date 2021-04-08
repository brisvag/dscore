from selenium import webdriver
import pandas as pd

from ..utils import csv2frame


base_url = 'https://iupred3.elte.hu/'


def submit_and_get_result(seq, mode='long'):
    with webdriver.Firefox() as driver:
        driver.get(base_url)
        # submit sequence
        driver.find_element_by_id('inp_seq').send_keys(seq)
        driver.find_element_by_id(f'context_selector_{mode}').click()
        driver.find_element_by_class_name('btn').click()
        # get raw text result link
        menu = driver.find_element_by_class_name('dropdown-menu')
        result_url = menu.find_elements_by_tag_name('a')[0].get_property('href')
        # open results
        driver.get(result_url)
        result = driver.find_element_by_xpath('//html/body/pre').text
    return result


def parse_result(result):
    return csv2frame(result)


def get_iupred(seq):
    dfs = []
    for mode in ('long', 'short'):
        result = submit_and_get_result(seq)
        dfs.append(parse_result(result))
    return pd.concat(dfs)
