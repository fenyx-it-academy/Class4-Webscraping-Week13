#!/usr/bin/python3

import json
import psycopg2

conn = psycopg2.connect("dbname=cars user=abuzer password=admin")
cur = conn.cursor()

info = open('bmw_citroen_honda.json')
res = json.load(info)

for id, data in enumerate(res):
    command = """INSERT INTO public.bmw_citroen_honda(id, 
        model, year, km, color, price, city)
        VALUES (%s, %s, %s, %s, %s, %s, %s);"""
    cur.execute(command, (id+1, data['model'], data['year'], data['km'],
                data['color'], data['price'], data['city']))
    # print(id, data)

cur.close()
conn.commit()
conn.close()
info.close()
