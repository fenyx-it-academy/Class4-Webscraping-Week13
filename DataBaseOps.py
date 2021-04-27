import psycopg2

con = psycopg2.connect("dbname=dvdrental user=postgres password=1234")
cur = con.cursor()
cur.execute("create table arabam (model text, year integer, km integer, color text, price integer, city text)")
cur.execute("COPY arabam from 'C:\\Users\\kbc\\PycharmProjects\\Last\\Week14\\arabam\\new\\new\\spiders\\data.csv' DELIMITER ',' CSV HEADER")
con.commit()
cur.close()
con.close()
