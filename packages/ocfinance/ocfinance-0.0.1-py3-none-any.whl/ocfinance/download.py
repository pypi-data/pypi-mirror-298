import pandas as pd

from . import scraper

def download(url, start=None, end=None):
    """
    Downloads the data from the given URL and returns a pandas DataFrame.
    """
    CHECKONCHAIN_BASE_URL = "https://charts.checkonchain.com"
    CHAINEXPOSED_BASE_URL = "https://chainexposed.com"

    data = pd.DataFrame()

    if url.startswith(CHECKONCHAIN_BASE_URL):
        data = scraper.checkonchain._download(url)
    elif url.startswith(CHAINEXPOSED_BASE_URL):
        data = scraper.chainexposed._download(url)
    else:
        raise ValueError("URL does not match any known provider.")
    
    return data
