import pymysql
import csv
from config import DB_HOST, DB_USER, DB_PASSWORD, DB_NAME, DB_PORT

# Asetukset
groupid = 15
tiedosto = "data_mysql.csv"

# Yhdistetään tietokantaan TCP-yhteydellä
print(f"Yhdistetään tietokantaan {DB_HOST}:{DB_PORT}...")
conn = pymysql.connect(
    host=DB_HOST,
    port=DB_PORT,
    user=DB_USER,
    password=DB_PASSWORD,
    database=DB_NAME
)

# Haetaan data
print(f"Haetaan dataa groupid={groupid}...")
cursor = conn.cursor()
query = """
SELECT timestamp, groupid, from_mac, to_mac, 
       sensorvalue_a, sensorvalue_b, sensorvalue_c, 
       sensorvalue_d, sensorvalue_e, sensorvalue_f 
FROM rawdata 
WHERE groupid = %s 
ORDER BY timestamp DESC 
LIMIT 100
"""
cursor.execute(query, (groupid,))
rows = cursor.fetchall()

# Tallennetaan CSV-tiedostoksi
with open(tiedosto, "w", newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['timestamp', 'groupid', 'from_mac', 'to_mac', 
                     'sensorvalue_a', 'sensorvalue_b', 'sensorvalue_c',
                     'sensorvalue_d', 'sensorvalue_e', 'sensorvalue_f'])
    writer.writerows(rows)

cursor.close()
conn.close()

print(f"Valmis! Tallennettu {len(rows)} riviä tiedostoon {tiedosto}")