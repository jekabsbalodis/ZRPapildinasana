import csv
import sys
import requests
from tqdm import tqdm
import xml.etree.ElementTree as ET

url = 'https://dati.zva.gov.lv/zalu-registrs/export/HumanProducts.xml'
with requests.get(url, stream=True) as r:
    totalLength = int(requests.head(url).headers["Content-Length"])
    with open('HumanProducts.xml', 'wb') as HumanProducts:
        with tqdm(unit='B',
                  unit_scale=True,
                  unit_divisor=1024,
                  total=totalLength,
                  file=sys.stdout,
                  desc='HumanProducts.xml') as progress:
            for chunk in r.iter_content(chunk_size=1024):
                datasize = HumanProducts.write(chunk)
                progress.update(datasize)
drugRegisterName = 'HumanProducts.xml'
with open(drugRegisterName, encoding='utf-8')as drugRegister:
    allStuff = ET.parse(drugRegister)
products = allStuff.findall('products/product')

lineChecked = []
atcCodeChecked = []
i = 0
with open('20220509_antidopinga_vielas.csv', encoding='utf-8', newline='') as zaluRegistrs:
    csvreader = csv.reader(zaluRegistrs, dialect='excel', delimiter=',')
    for line in csvreader:
        if line[1] == 'authorisation_no':
            continue
        for product in products:
            if line[1] in lineChecked:
                continue
            authorisationNo = product.findtext('authorisation_no')
            if line[1] == authorisationNo:
                atcCode = product.findtext('atc_code')
                if atcCode in atcCodeChecked:
                    continue
                lineChecked.append(line[1])
                with open('piezimju lauki.csv', 'a', encoding='utf-8', newline='') as piezimjuLauki:
                    csvwriter = csv.writer(
                        piezimjuLauki, dialect='excel', delimiter=',')
                    csvwriter.writerow([atcCode, line[4], line[5], line[6],
                                       line[7], line[8], line[9], line[10], line[11], line[12]])
                    print('Wrote line ',i)
                    i+=1
                    atcCodeChecked.append(atcCode)
