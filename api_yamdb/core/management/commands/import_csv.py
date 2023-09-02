from django.core.management.base import BaseCommand
import csv
import sqlite3
import os

class Command(BaseCommand):
    help = 'Import data from csv files in DataBase'

    def handle(self, *args, **kwargs):
        con = sqlite3.connect('db.sqlite3')
        cur = con.cursor()
        os.chdir("static/data")
        with open('comments.csv', 'r', encoding="utf-8", newline="") as fin:
            get_column_names=con.execute("SELECT * FROM reviews_comment")
            col_name=[i[0] for i in get_column_names.description]
            print(col_name)

            r = csv.reader(fin, delimiter=",")
            dr = csv.DictReader(fin, delimiter=",") 
            count = 0
            #new_list = [0, 2, 4, 3, 1]
            new_list = []
            # 0, 4, 1, 3, 2
            l = []
            ttt = []
            long = 0
            for j in r:
                if count !=0:
                    c=0
                    # print(len(j))
                    for k in j:
                        #print(new_list[c])
                       # print(j[new_list[c]])
                        ttt.append(j[new_list[c]])
                        c =c + 1
                    t = tuple(ttt)
                    ttt = []
                    print(t)
                    # t = tuple(j)
                    l.append(t)
                else:
                    print(j)
                    long = len(j)
                    d = dict()
                    i = 0
                    long_c = long 
                    while(i <= long_c):
                        if i<5:
                            dd = j[i]
                            if i==3:
                                dd = dd + '_id'
                            d[dd] = i
                        i = i + 1
                    for g in col_name:
                        new_list.append(d.get(g))
                    print(new_list)
                count = count +1
            # print(l)
        q = '?'
        # print(f'count_: {count}, long_: {long}')
        # print(os.getcwd())
        # os.chdir("../..")
        # print(os.getcwd())
        # os.system('python manage.py what_time_is_it')
        i = 1
        while(i < long):
            i = i + 1
            q = q + ', ?'
        print(f'&_: {q}')
        name_table_db = 'reviews_comment'
        str = f"INSERT INTO {name_table_db} VALUES ({q});"
        # print(f'str_: {str}')      
        # cur.executemany("INSERT INTO reviews_category VALUES (?, ?, ?);", to_db)
        cur.executemany(str, l)
        # cur.executemany("INSERT INTO reviews_category (id, name, slug) VALUES (?, ?, ?);", to_db)
        con.commit()
        con.close()
        
