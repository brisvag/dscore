from selenium import webdriver
import pandas as pd

from .utils import csv2frame


base_url = 'http://original.disprot.org/metapredictor.php'


def submit(seq, mode='long'):
    driver = webdriver.Firefox()
    driver.get(base_url)
    # tick all the boxes
    for name in ('VSL2', 'VL3', 'VLXT', 'PONDRFIT'):
        checkbox = driver.find_element_by_name(name)
        if not checkbox.is_selected():
            checkbox.click()
    # ">" symbol is needed for this server to recognise as fasta
    seq = '> none\n' + seq
    driver.find_element_by_name('query').send_keys(seq)
    # submit
    driver.find_element_by_xpath('/html/body/table[3]/tbody/tr[3]/td/input[1]').click()
    return driver


def get_results(driver):
    results = {}
    for name in ('VSL2', 'VSL3', 'VLXT', 'PONDR-FIT'):  # different from earlier, for some reason...
        element = driver.find_element_by_xpath(f'/html/body/center[1]/a[contains(text(), "{name}")]')
        result_url = element.get_property('href')
        driver.get(result_url)
        result = driver.find_element_by_xpath('/html/body/pre').text
        results[name] = result
    driver.quit()
    return results


def parse_results(results):
    # TODO
    dfs = []
    for result in results:
        dfs.append(csv2frame(result, comment='>'))
    return pd.concat(results)


def get_disprot(seq):
    submitted_driver = submit(seq)
    result = get_results(submitted_driver)
    return parse_results(result)
