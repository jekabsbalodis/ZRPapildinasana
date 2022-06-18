# Run 'generateATCcsv.py' before, to create .csv file from which to create sqlite file

import csv
import sqlite3


conn = sqlite3.connect('piezimju lauki.sqlite')
cur = conn.cursor()

cur.executescript('''
    CREATE TABLE IF NOT EXISTS Piezimju_lauki (
    atc_code TEXT UNIQUE,
    prohibited TEXT,
    prohibited_comp TEXT,
    prohibited_class TEXT,
    notes TEXT,
    prohibited_sports TEXT,
    prohibited_comp_sports TEXT,
    notes_en TEXT,
    prohibited_sports_en TEXT,
    prohibited_comp_sports_en TEXT
)
''')

with open('piezimju lauki.csv', encoding='utf-8', newline='') as piezimjuLauki:
    data = csv.DictReader(piezimjuLauki)
    toDB = [(i['atc_code'], i['prohibited'], i['prohibited_comp'], i['prohibited_class'], i['notes'],
             i['prohibited_sports'], i['prohibited_comp_sports'], i['notes_en'], i['prohibited_sports_en'],
             i['prohibited_comp_sports_en']) for i in data]

cur.executemany('''INSERT INTO Piezimju_lauki (atc_code,
                                               prohibited,
                                               prohibited_comp,
                                               prohibited_class,
                                               notes,
                                               prohibited_sports,
                                               prohibited_comp_sports,
                                               notes_en,
                                               prohibited_sports_en,
                                               prohibited_comp_sports_en) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                toDB)
conn.commit()
conn.close()
