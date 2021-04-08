import requests
from xml.etree import ElementTree

from .utils import retry


submit_base_url = 'https://fold.weizmann.ac.il/fldbin/findex?m=xml&sq='


@retry
def submit_and_get_result(seq):
    submit_url = submit_base_url + seq
    r = requests.get(submit_url)
    r.raise_for_status()
    tree = ElementTree(r.text)
    result = float(tree.find('findex').text)
    return result


def get_foldindex(seq):
    return submit_and_get_result(seq)
