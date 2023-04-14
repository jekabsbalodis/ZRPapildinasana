import requests
from datetime import date
import shutil


def download_register():
    url = 'https://dati.zva.gov.lv/zalu-registrs/export/HumanProducts.xml'
    with requests.get(url) as r:
        with open('HumanProducts.xml', 'wb') as HumanProducts:
            HumanProducts.write(r.content)
    return 'HumanProducts.xml'


def download_register_delta(dateFrom):
    url = 'https://dati.zva.gov.lv/zr-log/api/export/?s-ins=1&d-from=' + \
        str(dateFrom)
    with requests.get(url) as r:
        with open('delta.xml', 'wb') as delta:
            delta.write(r.content)
    return 'delta.xml'


def download_doping_substances():
    url = 'https://data.gov.lv/dati/lv/dataset/medikamenti-kas-satur-dopinga-vielas/resource/ee8f9b14-1eee-494a-b7f5-6777a8232dcb/download'
    fileName = 'antidopinga_vielas.csv'
    with requests.get(url) as r:
        with open(fileName, 'wb') as delta:
            delta.write(r.content)
    shutil.copyfile(fileName, date.today().strftime('%Y%m%d') + '_' + fileName)
