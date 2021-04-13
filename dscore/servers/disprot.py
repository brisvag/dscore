from selenium import webdriver
import pandas as pd

from ..utils import csv2frame, ensure_and_log


base_url = 'http://original.disprot.org/metapredictor.php'
cutoff = 0.5


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
    driver.find_element_by_name('native_sequence').send_keys(seq)
    # submit
    driver.find_element_by_xpath('/html/body/table[3]/tbody/tr[3]/td/input[1]').click()
    return driver


def get_results(driver):
    names = ('VSL2', 'VSL3', 'VLXT', 'PONDR-FIT')
    results = {}
    urls = []
    for name in names:  # different from earlier, for some reason...
        element = driver.find_element_by_xpath(f'/html/body/center[1]/a[contains(text(), "{name}")]')
        result_url = element.get_property('href')
        # save all of them before moving away
        urls.append(result_url)
    for name, url in zip(names, urls):
        driver.get(result_url)
        result = driver.find_element_by_xpath('/html/body/pre').text
        results[name] = result
    driver.quit()
    return results


def parse_results(results):
    dfs = []
    for name, result in results.items():
        df = csv2frame(result, comment='>')[[2]]
        df.columns = [f'disprot_{name}']
        dfs.append(df >= cutoff)
    return pd.concat(dfs, axis=1)


@ensure_and_log
async def get_disprot(seq):
    submitted_driver = submit(seq)
    result = get_results(submitted_driver)
    return parse_results(result)
