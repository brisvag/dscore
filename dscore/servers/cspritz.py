from selenium import webdriver
import pandas as pd

from .utils import retry, JobNotDone, cs


base_url = 'http://old.protein.bio.unipd.it/cspritz/'


def submit(seq, mode='long'):
    # ">" symbol is needed for this server to recognise as fasta
    seq = '> none\n' + seq
    driver = webdriver.Firefox()
    driver.get(base_url)
    driver.find_element_by_id('sequence').send_keys(seq)
    # submit and confirm
    base_xpath = 'html/body/div[4]/form'
    mode_selector = base_xpath + f'/fieldset[3]/table/tbody/tr[2]/td/select/option[contains(text(), "{mode}")]'
    mode_selector.click()
    driver.find_element_by_xpath(base_xpath + '/input[1]').click()
    return driver


@retry
def get_result(driver):
    if driver.find_element_by_xpath('/html/body/div[4]/p/span') != 'finished':
        raise JobNotDone('still waiting')
    # open text results
    result_url = driver.find_element_by_xpath('/html/body/div[6]/center/b/table/tbody/tr[2]/td[2]/a').get_property('href')
    # open results
    driver.get(result_url)
    result = driver.find_element_by_xpath('/html/body/pre').text
    driver.quit()
    return result


def parse_result(result):
    # TODO
    return


def get_cspritz(seq):
    dfs = []
    for mode in ('long', 'short'):
        submitted_driver = submit(seq, mode=mode)
        result = get_result(submitted_driver)
        dfs.append(parse_result(result))
    return pd.concat(dfs, axis=1)
