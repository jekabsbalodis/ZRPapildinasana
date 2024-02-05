'''Functions to download data from multiple sources'''
import requests


def download_register():
    '''Return url for register of human medicines'''
    url = 'https://dati.zva.gov.lv/zalu-registrs/export/HumanProducts.json'
    return url


def download_register_delta(date_from, date_to):
    '''return url for file containing changes in register of human medicines
    date_to and date_from provides date selection'''
    url = 'https://dati.zva.gov.lv/zr-log/api/export/?s-ins=1&d-from=' + \
        str(date_from) + '&d-to=' + str(date_to)
    return url


def download_doping_substances():
    '''Download most recent file with information on medicines' use in sports'''
    url = 'https://data.gov.lv/dati/lv/api/3/action/package_show?id=medikamenti-kas-satur-dopinga-vielas'
    data = requests.get(url).json()
    file_name = 'antidopinga_vielas.csv'
    with requests.get(data.get('result').get('resources')[0].get('url')) as r:
        with open(file_name, 'wb') as f:
            f.write(r.content)
    return 'antidopinga_vielas.csv'
