import csv
import sqlite3
import sys
import requests
from tqdm import tqdm
import xml.etree.ElementTree as ET


conn = sqlite3.connect('piezimju lauki.sqlite')
cur = conn.cursor()

cur.executescript('''
    CREATE TABLE IF NOT EXISTS Prohibited (
        id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
        prohibited TEXT UNIQUE
    );
    CREATE TABLE IF NOT EXISTS Prohibited_comp (
        id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
        prohibited_comp TEXT UNIQUE
    );
    CREATE TABLE IF NOT EXISTS Prohibited_class (
        id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
        prohibited_class TEXT UNIQUE
    );
    CREATE TABLE IF NOT EXISTS Notes (
        id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
        notes TEXT UNIQUE
    );
    CREATE TABLE IF NOT EXISTS Prohibited_sports (
        id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
        prohibited_sports TEXT UNIQUE
    );
    CREATE TABLE IF NOT EXISTS Prohibited_comp_sports (
        id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
        prohibited_comp_sports TEXT UNIQUE
    );
    CREATE TABLE IF NOT EXISTS Notes_en (
        id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
        notes_en TEXT UNIQUE
    );
    CREATE TABLE IF NOT EXISTS Prohibited_sports_en (
        id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
        prohibited_sports_en TEXT UNIQUE
    );
    CREATE TABLE IF NOT EXISTS Prohibited_comp_sports_en (
        id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
        prohibited_comp_sports_en TEXT UNIQUE
    );
    CREATE TABLE IF NOT EXISTS Piezimju_lauki (
        atc_code TEXT UNIQUE,
        prohibited_id INTEGER,
        prohibited_comp_id INTEGER,
        prohibited_class_id INTEGER,
        notes_id INTEGER,
        prohibited_sports_id INTEGER,
        prohibited_comp_sports_id INTEGER,
        notes_en_id INTEGER,
        prohibited_sports_en_id INTEGER,
        prohibited_comp_sports_en_id INTEGER
)
''')


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
                cur.execute(
                    'INSERT OR IGNORE INTO Prohibited (prohibited) VALUES (?)', (line[4],))
                cur.execute(
                    'SELECT id FROM Prohibited WHERE prohibited = ?', (line[4],))
                prohibitedID = cur.fetchone()[0]
                cur.execute(
                    'INSERT OR IGNORE INTO Prohibited_comp (prohibited_comp) VALUES (?)', (line[5],))
                cur.execute(
                    'SELECT id FROM Prohibited_comp WHERE prohibited_comp = ?', (line[5],))
                prohibitedCompID = cur.fetchone()[0]
                cur.execute(
                    'INSERT OR IGNORE INTO Prohibited_class (prohibited_class) VALUES (?)', (line[6],))
                cur.execute(
                    'SELECT id FROM Prohibited_class WHERE prohibited_class = ?', (line[6],))
                prohibitedClassID = cur.fetchone()[0]
                cur.execute(
                    'INSERT OR IGNORE INTO Notes (notes) VALUES (?)', (line[7],))
                cur.execute('SELECT id FROM Notes WHERE notes = ?', (line[7],))
                notesID = cur.fetchone()[0]
                cur.execute(
                    'INSERT OR IGNORE INTO Prohibited_sports (prohibited_sports) VALUES (?)', (line[8],))
                cur.execute(
                    'SELECT id FROM Prohibited_sports WHERE prohibited_sports = ?', (line[8],))
                prohibitedSportsID = cur.fetchone()[0]
                cur.execute(
                    'INSERT OR IGNORE INTO Prohibited_comp_sports (prohibited_comp_sports) VALUES (?)', (line[9],))
                cur.execute(
                    'SELECT id FROM Prohibited_comp_sports WHERE prohibited_comp_sports = ?', (line[9],))
                prohibitedCompSportsID = cur.fetchone()[0]
                cur.execute(
                    'INSERT OR IGNORE INTO Notes_en (notes_en) VALUES (?)', (line[10],))
                cur.execute(
                    'SELECT id FROM Notes_en WHERE notes_en = ?', (line[10],))
                notesEnID = cur.fetchone()[0]
                cur.execute(
                    'INSERT OR IGNORE INTO Prohibited_sports_en (prohibited_sports_en) VALUES (?)', (line[11],))
                cur.execute(
                    'SELECT id FROM Prohibited_sports_en WHERE prohibited_sports_en = ?', (line[11],))
                prohibitedSportsEnID = cur.fetchone()[0]
                cur.execute(
                    'INSERT OR IGNORE INTO Prohibited_comp_sports_en (prohibited_comp_sports_en) VALUES (?)',
                    (line[12],))
                cur.execute(
                    'SELECT id FROM Prohibited_comp_sports_en WHERE prohibited_comp_sports_en = ?', (line[12],))
                prohibitedCompSportsEnID = cur.fetchone()[0]
                cur.execute('''INSERT OR IGNORE INTO Piezimju_lauki (atc_code, prohibited_id, prohibited_comp_id,
                prohibited_class_id, notes_id, prohibited_sports_id, prohibited_comp_sports_id, notes_en_id,
                prohibited_sports_en_id, prohibited_comp_sports_en_id) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', (
                    atcCode, prohibitedID, prohibitedCompID, prohibitedClassID, notesID, prohibitedSportsID,
                    prohibitedCompSportsID, notesEnID, prohibitedSportsEnID, prohibitedCompSportsEnID))
                lineChecked.append(line[1])
                atcCodeChecked.append(atcCode)
                i += 1
                if i == 100:
                    print('Commiting changes')
                    conn.commit()
                    i = 0
conn.commit()
conn.close()
