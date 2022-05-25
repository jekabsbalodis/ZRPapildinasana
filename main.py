import xml.etree.ElementTree as ET
import shutil
from Constants import INCLUDE_ERROR, INCLUDE_PROMPT, NO, NOTES_PROMPT, NOTES_PROMPT_EN, P1, PROHIBITED_CLASS_ERROR, PROHIBITED_CLASS_PROMPT, PROHIBITED_ERROR, PROHIBITED_IN_PROMPT, PROHIBITED_OUT_PROMPT
from helpers import prohibited, prohibitedClass, stringInput, toInclude

deltaName = input('Ievadi nosaukumu .csv failam ar zāļu reģistra izmaiņām: ')
separator = input('Ievadi, kāds simbols atdala ierakstus .csv failā: ')
productsDeltaName = []
with open(deltaName, encoding='utf-8') as delta:
    for line in delta:
        line.strip
        if line.startswith('Datums'):
            continue
        product = line.split(separator)
        productsDeltaName.append(product[1])
    print(productsDeltaName)

drugRegisterName = input('Ja failu ar zāļu reģistra atvērtajiem datiem sauc HumanProducts.xml, spied Enter\n'
                         'Ja failam ir cits nosaukums, ievadi to: ')
if len(drugRegisterName) < 1:
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
            medicine_name = product.findtext('medicine_name')
            authorisation_no = product.findtext('authorisation_no')
            pharmaceutical_form_lv = product.findtext('pharmaceutical_form_lv')
            active_substance = product.findtext('active_substance')
            print(authorisation_no)
            print(active_substance)
            print(pharmaceutical_form_lv)
            toIncludeStr = toInclude(INCLUDE_PROMPT, INCLUDE_ERROR)
            if toIncludeStr == NO:
                productsDeltaNameChecked.append(productDeltaName)
                continue
            prohibited_out_competition = prohibited(
                PROHIBITED_OUT_PROMPT, PROHIBITED_ERROR)
            prohibited_in_competition = prohibited(
                PROHIBITED_IN_PROMPT, PROHIBITED_ERROR)
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

            with open(dataZVAName, 'a', encoding='utf-8') as dataZVA:
                dataZVA.write(text)
            print('Failam pievienota šāda rinda:\n' + text)
            productsDeltaNameChecked.append(productDeltaName)
