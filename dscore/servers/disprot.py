from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
import pandas as pd

from ..utils import retry, JobNotDone, csv2frame, ensure_and_log


base_url = 'http://original.disprot.org/metapredictor.php'
cutoff = 0.5
modes = ('PONDRFIT',)
unwanted_modes = ('VSL2', 'VL3', 'VLXT')  # already done by pondr
mode_headers = ('PONDR-FIT',)


def submit(seq):
    driver = webdriver.Firefox()
    driver.get(base_url)
    # tick all the boxes
    for mode in modes + unwanted_modes:
        checkbox = driver.find_element(By.NAME, mode)
        if not checkbox.is_selected() and mode in modes:
            checkbox.click()
        elif checkbox.is_selected() and mode in unwanted_modes:
            checkbox.click()
    # ">" symbol is needed for this server to recognise as fasta
    seq = '> none\n' + seq
    driver.find_element(By.NAME, 'native_sequence').send_keys(seq)
    # submit
    driver.find_element(By.XPATH, '/html/body/table[3]/tbody/tr[3]/td/input[1]').click()
    return driver


@retry()
def get_results(driver):
    results = {}
    urls = []
    for mode in mode_headers:  # different from earlier, for some reason...
        try:
            element = driver.find_element(By.XPATH, f'/html/body/center[1]/a[contains(text(), "{mode}")]')
        except NoSuchElementException:
            raise JobNotDone
        result_url = element.get_property('href')
        # save all of them before moving away
        urls.append(result_url)
    for mode, url in zip(mode_headers, urls):
        driver.get(url)
        result = driver.find_element(By.XPATH, '/html/body/pre').text
        results[mode] = result
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
    result = await get_results(submitted_driver)
    return parse_results(result)
