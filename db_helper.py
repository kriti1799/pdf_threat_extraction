import sqlite3
import uuid
from datetime import datetime
import json

db_file = 'pdf_threat.db'

def get_conn():
    return sqlite3.connect(db_file)

def insert_pdf(filename):
    conn = get_conn()
    cursor = conn.cursor()
    pdf_id = str(uuid.uuid4())
    uploaded_at = datetime.utcnow()
   
    cursor.execute(
        "INSERT INTO pdf_documents (id, filename, uploaded_at, processed_at) VALUES (?, ?, ?, NULL)",
        (pdf_id, filename, uploaded_at)
    )
    conn.commit()
    conn.close()
    return pdf_id

def insert_threat_actors(pdf_id, name, aliases=None, description= None ):
    conn = get_conn()
    cursor = conn.cursor()
    actor_id = str(uuid.uuid4())
    extracted_at = datetime.utcnow()
    cursor.execute("INSERT INTO threat_actors(id, pdf_id, name, aliases, description, extracted_at) VALUES(?,?,?,?,?,?)",
                   (actor_id, pdf_id, name, aliases,description , extracted_at)
                   )
    conn.commit()
    conn.close()
    return actor_id

def insert_cves(cve_id, pdf_id, description=None, severity=None):
    conn = get_conn()
    cursor = conn.cursor()
    id = str(uuid.uuid4())
    extraced_at = datetime.utcnow()
    cursor.execute("INSERT INTO cves(id, pdf_id, cve_id, description, severity, extracted_at) VALUES(?,?,?,?,?,?)",
                   (id, pdf_id, cve_id, description, severity, extraced_at))
    conn.commit()
    conn.close()
    return cve_id








