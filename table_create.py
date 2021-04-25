import psycopg2

################################################# Create cars table in database
conn = psycopg2.connect("dbname=auto user=postgres password=Fsm1453.")
cursor = conn.cursor()
command = (
        """
        CREATE TABLE cars (
            Car_id INTEGER PRIMARY KEY,
            Model VARCHAR(255) NOT NULL,
            Year INTEGER NOT NULL,
            Km INTEGER NOT NULL,
            Color VARCHAR(255) NOT NULL,
            Price INTEGER NOT NULL,
            City VARCHAR(255)
        )
        """)
cursor.execute(command)
cursor.close()
conn.commit()
conn.close()