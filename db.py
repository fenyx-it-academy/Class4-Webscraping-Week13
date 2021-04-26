import psycopg2
import pandas as pd
import json

################################################## The information in the json file is saved to the database.

path="C:\\Users\\Beheerder\\VS_Code\\pyCoders\\myScrapyPro\\myScrapyP\\cars.json"
input_file = open (path,)
json_array = json.load(input_file)

conn = psycopg2.connect('dbname=auto user=postgres password=Fsm1453.')
cursor = conn.cursor()
for id,data in enumerate(json_array):
    command = """INSERT INTO cars (car_id,model,year,km,color,price,city) VALUES (%s,%s,%s,%s,%s,%s,%s);"""
    cursor.execute(command,(id+1,data['model'],data['year'],data['km'],data['color'],data['price'],data['city']))
    
cursor.close()
conn.commit()
conn.close()


