import unittest
from unittest.mock import MagicMock, patch
import pandas as pd
from ocfinance import download

class TestDownloadFunction(unittest.TestCase):

    @patch('ocfinance.scraper.checkonchain._download')
    def test_checkonchain_url(self, mock_checkonchain_download):
        url = "https://charts.checkonchain.com/test/example/"
        expected_data = pd.DataFrame({ 'Example': [1, 2, 3] }, index=[4, 5, 6])
        mock_checkonchain_download.return_value = expected_data

        result = download(url)

        mock_checkonchain_download.assert_called_once_with(url)
        pd.testing.assert_frame_equal(result, expected_data)
    
    @patch('ocfinance.scraper.chainexposed._download')
    def test_chainexposed_url(self, mock_chainexposed_download):
        url = "https://chainexposed.com/test"
        expected_data = pd.DataFrame({ 'Example': [1, 2, 3] }, index=[4, 5, 6])
        mock_chainexposed_download.return_value = expected_data
        
        result = download(url)

        mock_chainexposed_download.assert_called_once_with(url)
        pd.testing.assert_frame_equal(result, expected_data)
    
    def test_invalid_url(self):
        url = "https://invalid-url.com/test"

        with self.assertRaises(ValueError):
            download(url)
