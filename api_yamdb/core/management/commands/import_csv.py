from django.core.management.base import BaseCommand
import csv
import sqlite3
import os

class Command(BaseCommand):
    help = 'Import data from csv files in DataBase'

    def handle(self, *args, **kwargs):
        #con = sqlite3.connect('db.sqlite3')
        #cur = con.cursor()
        os.chdir("static/data")
        with open('category.csv', 'r', encoding="utf-8", newline="") as fin:
            dr = csv.DictReader(fin, delimiter=",") 
            # print(f'keys_: {dr.value()}')
            for row in dr:
                print(f'dr_: {row}')
            to_db = [(i['id'], i['name'], i['slug']) for i in dr]
            print(f'to_db_: {to_db}')       
        #cur.executemany("INSERT INTO reviews_category (id, name, slug) VALUES (?, ?, ?);", to_db)
        #con.commit()
        #con.close()
        
