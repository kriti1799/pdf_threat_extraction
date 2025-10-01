import sqlite3
import uuid
import datetime

conn = sqlite3.connect("pdf_threat.db")  # open or create DB
cursor = conn.cursor() 

# Creating tables 
cursor.execute("""create table if not exists pdf_documents(
               id text primary key,
               filename TEXT,
  uploaded_at TIMESTAMP,
  processed_at TIMESTAMP
               )""")

cursor.execute("""create table if not exists threat_actors(
              id text PRIMARY KEY,
              pdf_id text, 
              name TEXT,
              aliases TEXT, 
              description TEXT,
              extracted_at TIMESTAMP
               ,FOREIGN KEY (pdf_id) REFERENCES pdf_documents(id))
""")

cursor.execute("""create table if not exists cves(
               id text primary key,
               pdf_id text,
               cve_id text,
               description TEXT,
                severity TEXT,
              extracted_at TIMESTAMP
            ,FOREIGN KEY(pdf_id) REFERENCES pdf_documents(id)
               
               )""")

cursor.execute("""
INSERT INTO pdf_documents (id, filename, uploaded_at, processed_at)
VALUES (?, ?, ?, ?)
""", (str(uuid.uuid4()), "report.pdf", datetime.datetime.now().isoformat(), None))

conn.commit()
conn.close()