import requests


def download_register(url):
    url = 'https://dati.zva.gov.lv/zalu-registrs/export/HumanProducts.xml'
    with requests.get(url) as r:
        with open('HumanProducts.xml', 'wb') as HumanProducts:
            HumanProducts.write(r.content)