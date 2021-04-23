import psycopg2

conn = psycopg2.connect("dbname=cars user=postgres password=Asude1608.")
cur = conn.cursor()
cur.execute("Select * from autos order by model")
records = cur.fetchall()
cur.close()
conn.commit()
conn.close()

data = []
for record in records:
    data.append(list(record))
