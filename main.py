import sqlite3
import xml.etree.ElementTree as ET
import shutil
import csv
import requests
from tqdm import tqdm
import sys
from Constants import INCLUDE_ERROR, INCLUDE_PROMPT, NO, NOTES_PROMPT, NOTES_PROMPT_EN, P1, PROHIBITED_CLASS_ERROR, PROHIBITED_CLASS_PROMPT, PROHIBITED_ERROR, PROHIBITED_IN_PROMPT, PROHIBITED_OUT_PROMPT
from helpers import prohibited, prohibitedClass, stringInput, toInclude

conn = sqlite3.connect('piezimju lauki.sqlite')
cur = conn.cursor()

deltaName = input('Ievadi nosaukumu .csv failam ar zāļu reģistra izmaiņām: ')
separator = input(
    '\n-----\nIevadi, kāds simbols atdala ierakstus .csv failā: ')
productsDeltaName = []
with open(deltaName, encoding='utf-8') as delta:
    csvreader = csv.reader(delta, dialect='excel', delimiter=separator)
    for line in csvreader:
        productsDeltaName.append(line[1])
print(productsDeltaName)

url = 'https://dati.zva.gov.lv/zalu-registrs/export/HumanProducts.xml'
with requests.get(url, stream=True) as r:
    totalLength = int(requests.head(url).headers["Content-Length"])
    with open('HumanProducts.xml', 'wb') as HumanProducts:
        with tqdm(unit_scale=True,
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

dataZVANameOld = input(
    'Ievadi nosaukumu failam, kas pēdējo reizi tika nodots nodots ZVA: ')
date = input('Ievadi šodienas datumu šādā formātā - YYYYMMDD: ')
dataZVAName = date + '_antidopinga_vielas.csv'
shutil.copyfile(dataZVANameOld, dataZVAName)

productsDeltaNameChecked = []

for productDeltaName in productsDeltaName:
    for product in products:
        if productDeltaName in productsDeltaNameChecked:
            continue
        nr = product.findtext('authorisation_no')
        if productDeltaName == nr:
            atcCode = product.findtext('atc_code')
            medicine_name = product.findtext('medicine_name')
            authorisation_no = product.findtext('authorisation_no')
            pharmaceutical_form_lv = product.findtext('pharmaceutical_form_lv')
            active_substance = product.findtext('active_substance')
            cur.execute(
                'SELECT atc_code FROM Piezimju_lauki WHERE atc_code = ? ', (atcCode,))
            checkAtcCode = cur.fetchone()
            if checkAtcCode:
                print('Līdzīgs medikaments jau iepriekš ir iekļauts')
            else:
                print('Šāds medikaments iepriekš nav ticis iekļauts')
            print(authorisation_no)
            print(active_substance)
            print(pharmaceutical_form_lv)
            toIncludeStr = toInclude(INCLUDE_PROMPT, INCLUDE_ERROR)
            if toIncludeStr == NO:
                productsDeltaNameChecked.append(productDeltaName)
                continue
            if checkAtcCode:
                cur.execute(
                    'SELECT prohibited FROM Piezimju_lauki WHERE atc_code = ? ', (atcCode,))
                prohibited_out_competition = str(cur.fetchone()).lstrip('(\'').rstrip('\',)')
                cur.execute(
                    'SELECT prohibited_comp FROM Piezimju_lauki WHERE atc_code = ? ', (atcCode,))
                prohibited_in_competition = cur.fetchone()
                cur.execute(
                    'SELECT prohibited_class FROM Piezimju_lauki WHERE atc_code = ? ', (atcCode,))
                prohibited_class = cur.fetchone()
                cur.execute(
                    'SELECT notes FROM Piezimju_lauki WHERE atc_code = ? ', (atcCode,))
                notes_lv = cur.fetchone()
                cur.execute(
                    'SELECT prohibited_sports FROM Piezimju_lauki WHERE atc_code = ? ', (atcCode,))
                sports_in_competition_lv = cur.fetchone()
                cur.execute(
                    'SELECT prohibited_comp_sports FROM Piezimju_lauki WHERE atc_code = ? ', (atcCode,))
                sports_out_competition_lv = cur.fetchone()
                cur.execute(
                    'SELECT notes_en FROM Piezimju_lauki WHERE atc_code = ? ', (atcCode,))
                notes_en = cur.fetchone()
                cur.execute(
                    'SELECT prohibited_sports_en FROM Piezimju_lauki WHERE atc_code = ? ', (atcCode,))
                sports_in_competition_en = cur.fetchone()
                cur.execute(
                    'SELECT prohibited_comp_sports_en FROM Piezimju_lauki WHERE atc_code = ? ', (atcCode,))
                sports_out_competition_en = cur.fetchone()
            text = '\"{a}\",\"{b}\",\"{c}\",\"{d}\",\"{e}\",\"{f}\",\"{g}\",\"{h}\",\"{i}\",\"{j}\",\"{k}\",\"{l}\",\"{m}\"\n'.format(
                a=medicine_name,
                b=authorisation_no,
                c=pharmaceutical_form_lv,
                d=active_substance,
                e=prohibited_out_competition,
                f=prohibited_in_competition,
                g=prohibited_class,
                h=notes_lv,
                i=sports_in_competition_lv,
                j=sports_out_competition_lv,
                k=notes_en,
                l=sports_in_competition_en,
                m=sports_out_competition_en)

            # with open(dataZVAName, 'a', encoding='utf-8') as dataZVA:
            #     dataZVA.write(text)
            print('Failam tiks pievienota šāda rinda:\n' + text)
            productsDeltaNameChecked.append(productDeltaName)
