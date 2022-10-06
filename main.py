import sqlite3
import xml.etree.ElementTree as ET
import shutil
import csv
import requests
from tqdm import tqdm
import sys
from Constants import DELTA_DATE_FROM_PROMPT, INCLUDE_ERROR, INCLUDE_PROMPT, NO, NOTES_PROMPT, NOTES_PROMPT_EN, P1, PROHIBITED_CLASS_ERROR, PROHIBITED_CLASS_PROMPT, PROHIBITED_ERROR, PROHIBITED_IN_PROMPT, PROHIBITED_OUT_PROMPT
from helpers import prohibited, prohibitedClass, stringInput, toInclude

conn = sqlite3.connect('piezimju lauki.sqlite')
cur = conn.cursor()

deltaDateFrom = stringInput(DELTA_DATE_FROM_PROMPT)
deltaUrl = 'https://dati.zva.gov.lv/zr-log/api/export/?s-ins=1&d-from=' + deltaDateFrom

with requests.get(deltaUrl,) as r:
    with open('delta.xml', 'wb') as delta:
        delta.write(r.content)
deltaFile = 'delta.xml'
with open(deltaFile, encoding='utf-8')as deltaRegister:
    allStuffDelta = ET.parse(deltaRegister)
productsDelta = allStuffDelta.findall('meds/med')
for productDelta in productsDelta:
    name = productDelta.findtext('med_name')
    print(name)

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
drugRegister = 'HumanProducts.xml'
with open(drugRegister, encoding='utf-8')as drugRegister:
    allStuff = ET.parse(drugRegister)
products = allStuff.findall('products/product')

dataZVANameOld = input(
    'Ievadi nosaukumu failam, kas pēdējo reizi tika nodots nodots ZVA: ')
date = input('Ievadi šodienas datumu šādā formātā - YYYYMMDD: ')
dataZVAName = date + '_antidopinga_vielas.csv'
shutil.copyfile(dataZVANameOld, dataZVAName)

productsDeltaChecked = []
i = 0
for productDelta in productsDelta:
    deltaNr = productDelta.findtext('reg_number')
    for product in products:
        if deltaNr in productsDeltaChecked:
            continue
        nr = product.findtext('authorisation_no')
        if deltaNr == nr:
            atcCode = product.findtext('atc_code')
            medicine_name = product.findtext('medicine_name')
            authorisation_no = product.findtext('authorisation_no')
            pharmaceutical_form_lv = product.findtext('pharmaceutical_form_lv')
            active_substance = product.findtext('active_substance')
            cur.execute(
                'SELECT EXISTS (SELECT atc_code FROM Piezimju_lauki WHERE atc_code = ? )', (atcCode,))
            checkAtcCode = cur.fetchone()[0]
            if checkAtcCode:
                print('Līdzīgs medikaments jau iepriekš ir iekļauts')
            else:
                print('Šāds medikaments iepriekš nav ticis iekļauts')
            print(authorisation_no)
            print(active_substance)
            print(pharmaceutical_form_lv)
            toIncludeStr = toInclude(INCLUDE_PROMPT, INCLUDE_ERROR)
            if toIncludeStr == NO:
                productsDeltaChecked.append(deltaNr)
                continue
            if checkAtcCode:
                cur.execute(
                    '''SELECT prohibited FROM Piezimju_lauki
                    JOIN prohibited ON Prohibited.id = Piezimju_lauki.prohibited_id
                    WHERE atc_code = ? ''', (atcCode,))
                prohibited_out_competition = cur.fetchone()[0]
                cur.execute(
                    '''SELECT prohibited_comp FROM Piezimju_lauki
                    JOIN prohibited_comp ON Prohibited_comp.id = Piezimju_lauki.prohibited_comp_id
                    WHERE atc_code = ? ''', (atcCode,))
                prohibited_in_competition = cur.fetchone()[0]
                cur.execute(
                    '''SELECT prohibited_class FROM Piezimju_lauki
                    JOIN prohibited_class ON Prohibited_class.id = Piezimju_lauki.prohibited_class_id
                    WHERE atc_code = ? ''', (atcCode,))
                prohibited_class = cur.fetchone()[0]
                cur.execute(
                    '''SELECT notes FROM Piezimju_lauki
                    JOIN notes ON Notes.id = Piezimju_lauki.notes_id
                    WHERE atc_code = ? ''', (atcCode,))
                notes_lv = cur.fetchone()[0]
                cur.execute(
                    '''SELECT prohibited_sports FROM Piezimju_lauki
                    JOIN prohibited_sports ON Prohibited_sports.id = Piezimju_lauki.prohibited_sports_id
                    WHERE atc_code = ? ''', (atcCode,))
                sports_in_competition_lv = cur.fetchone()[0]
                cur.execute(
                    '''SELECT prohibited_comp_sports FROM Piezimju_lauki
                    JOIN prohibited_comp_sports ON Prohibited_comp_sports.id = Piezimju_lauki.prohibited_comp_sports_id
                    WHERE atc_code = ? ''', (atcCode,))
                sports_out_competition_lv = cur.fetchone()[0]
                cur.execute(
                    '''SELECT notes_en FROM Piezimju_lauki
                    JOIN notes_en ON Notes_en.id = Piezimju_lauki.notes_en_id
                    WHERE atc_code = ? ''', (atcCode,))
                notes_en = cur.fetchone()[0]
                cur.execute(
                    '''SELECT prohibited_sports_en FROM Piezimju_lauki
                    JOIN prohibited_sports_en ON Prohibited_sports_en.id = Piezimju_lauki.prohibited_sports_en_id
                    WHERE atc_code = ? ''', (atcCode,))
                sports_in_competition_en = cur.fetchone()[0]
                cur.execute(
                    '''SELECT prohibited_comp_sports_en FROM Piezimju_lauki
                    JOIN prohibited_comp_sports_en ON Prohibited_comp_sports_en.id =
                                                                            Piezimju_lauki.prohibited_comp_sports_en_id
                    WHERE atc_code = ? ''', (atcCode,))
                sports_out_competition_en = cur.fetchone()[0]

                text = '''{a}\n{b}\n{c}\n{d}\n{e}\n{f}\n{g}\n{h}\n{i}\n{j}\n{k}\n{l}\n{m}\n'''.format(
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
                print('Failam tiks pievienota rinda ar šādiem laukiem:\n' + text)

                with open(dataZVAName, 'a', encoding='utf-8', newline='') as dataZVA:
                    csvwriter = csv.writer(
                        dataZVA, dialect='excel', delimiter=',')
                    csvwriter.writerow([medicine_name,
                                        authorisation_no,
                                        pharmaceutical_form_lv,
                                        active_substance,
                                        prohibited_out_competition,
                                        prohibited_in_competition,
                                        prohibited_class,
                                        notes_lv,
                                        sports_in_competition_lv,
                                        sports_out_competition_lv,
                                        notes_en,
                                        sports_in_competition_en,
                                        sports_out_competition_en])
                productsDeltaChecked.append(deltaNr)
            else:
                prohibited_out_competition = prohibited(
                    PROHIBITED_IN_PROMPT, PROHIBITED_ERROR)
                prohibited_in_competition = prohibited(
                    PROHIBITED_OUT_PROMPT, PROHIBITED_ERROR)
                prohibited_class = prohibitedClass(
                    PROHIBITED_CLASS_PROMPT, PROHIBITED_CLASS_ERROR)
                notes_lv = stringInput(NOTES_PROMPT)
                notes_en = stringInput(NOTES_PROMPT_EN)
                if 'P1' in prohibited_class:
                    sports_in_competition_lv = P1['sports_in_competition_lv']
                    sports_in_competition_en = P1['sports_in_competition_en']
                    sports_out_competition_lv = P1['sports_out_competition_lv']
                    sports_out_competition_en = P1['sports_out_competition_en']
                else:
                    sports_in_competition_lv = ''
                    sports_in_competition_en = ''
                    sports_out_competition_lv = ''
                    sports_out_competition_en = ''
                text = '''{a}\n{b}\n{c}\n{d}\n{e}\n{f}\n{g}\n{h}\n{i}\n{j}\n{k}\n{l}\n{m}\n'''.format(
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
                print('Failam tiks pievienota rinda ar šādiem laukiem:\n' + text)

                with open(dataZVAName, 'a', encoding='utf-8', newline='') as dataZVA:
                    csvwriter = csv.writer(
                        dataZVA, dialect='excel', delimiter=',')
                    csvwriter.writerow([medicine_name,
                                        authorisation_no,
                                        pharmaceutical_form_lv,
                                        active_substance,
                                        prohibited_out_competition,
                                        prohibited_in_competition,
                                        prohibited_class,
                                        notes_lv,
                                        sports_in_competition_lv,
                                        sports_out_competition_lv,
                                        notes_en,
                                        sports_in_competition_en,
                                        sports_out_competition_en])
                productsDeltaChecked.append(deltaNr)
    i += 1
    if i == 100:
        conn.commit()
        i = 0
conn.commit()
conn.close()