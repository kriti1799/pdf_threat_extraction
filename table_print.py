import sqlite3

conn = sqlite3.connect("pdf_threat.db")
cursor = conn.cursor()

cursor.execute("SELECT * FROM cves ")
rows = cursor.fetchall()

if rows:
    print("Table CVES has data:")
    for row in rows:
        print(row)
else:
    print("Table CVES is empty.")

cursor.execute("SELECT * FROM  pdf_documents ")
rows = cursor.fetchall()

if rows:
    print("Table pdf_documents has data:")
    for row in rows:
        print(row)
else:
    print("Table pdf_documents is empty.")

cursor.execute("SELECT * FROM  threat_actors ")
rows = cursor.fetchall()

if rows:
    print("Table threat_actors has data:")
    for row in rows:
        print(row)
else:
    print("Table threat_actors is empty.")

conn.close()