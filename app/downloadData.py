import requests


def download_register():
    url = 'https://dati.zva.gov.lv/zalu-registrs/export/HumanProducts.xml'
    with requests.get(url) as r:
        with open('HumanProducts.xml', 'wb') as HumanProducts:
            HumanProducts.write(r.content)
    return 'HumanProducts.xml'


def download_register_delta(dateFrom, dateTo):
    url = 'https://dati.zva.gov.lv/zr-log/api/export/?s-ins=1&d-from=' + str(dateFrom) + '&d-to=' + str(dateTo)
    with requests.get(url) as r:
        with open('delta.xml', 'wb') as delta:
            delta.write(r.content)
    return 'delta.xml'


def download_doping_substances():
    url = 'https://data.gov.lv/dati/lv/api/3/action/package_show?id=medikamenti-kas-satur-dopinga-vielas'
    data = requests.get(url).json()
    fileName = 'antidopinga_vielas.csv'
    with requests.get(data.get('result').get('resources')[0].get('url')) as r:
        with open(fileName, 'wb') as delta:
            delta.write(r.content)
