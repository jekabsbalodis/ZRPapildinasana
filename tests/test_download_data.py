import unittest
from datetime import date, timedelta
from app.download_data import download_doping_substances, download_register, download_register_delta


class DownloadDataTestCase(unittest.TestCase):
    def test_download_doping_substances(self):
        download_doping_substances()
        with open('antidopinga_vielas.csv', encoding='utf-8') as f:
            self.assertTrue('medicine_name' in f.read())

    def test_download_register(self):
        download_register()
        with open('HumanProducts.xml', encoding='utf-8') as f:
            self.assertTrue('State Agency of Medicines of Latvia' in f.read())

    def test_download_register_delta(self):
        download_register_delta(date_from=(date.today() - timedelta(days=1)), date_to=date.today())
        with open('delta.xml', encoding='utf-8') as f:
            self.assertTrue('State Agency of Medicines of Latvia' in f.read())
