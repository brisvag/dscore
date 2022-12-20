from hashlib import blake2b
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
import pandas as pd

from ..utils import ensure_and_log

import logging
logger = logging.getLogger(__name__)


base_url = 'https://metapredict.net/'
tmp_dir = "/tmp/dscore/"


def options_download_path(save_dir):
    options = Options()
    options.set_preference("browser.download.folderList", 2)
    options.set_preference("browser.download.manager.showWhenStarting", False)
    options.set_preference("browser.download.dir", tmp_dir + save_dir)
    options.set_preference("browser.helperApps.neverAsk.saveToDisk", "text/csv")
    return options


def submit(seq):
    save_dir = blake2b(seq.encode(), digest_size=20).hexdigest()
    driver = webdriver.Firefox(options=options_download_path(save_dir))
    driver.get(base_url)
    driver.find_element(By.ID, 'sequence_box').send_keys(seq)
    driver.find_element(By.NAME, 'vals').click()
    driver.quit()
    return save_dir


def parse_result(save_dir):
    file = Path(tmp_dir) / save_dir / 'disorder_scores.csv'
    raw_data = pd.read_csv(file, sep=', ', engine='python')
    dis_array = raw_data['Disorder'] >= 0.5
    df = pd.DataFrame({'metapredict': dis_array})
    return df


@ensure_and_log
async def get_metapredict(seq):
    logger.debug('submitting')
    save_dir = submit(seq)
    logger.debug('waiting for results')
    return parse_result(save_dir)
