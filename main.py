from fastapi import FastAPI, File, UploadFile
from pdf_utils import extract_text_from_pdf, extract_threat_actors, extract_cves
from db_helper import insert_pdf, insert_threat_actors, insert_cves
import os, re, json
from dotenv import load_dotenv
import asyncio


# file_path = '/Users/kritiagrawal/Documents/Data Science Prep/Projects/pdf_threat_extraction/threat-intel-reports/file1.pdf'
# text = extract_text_from_pdf(file_path)
# print(text)
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

app = FastAPI(
    title="Task Management API",
    description="API for managing tasks with FastAPI, Sqlite3",
    version="0.1.0"
)



@app.get("/")
async def root():
    """Health check endpoint for the API."""
    return {"message": "Welcome to the Task Management API"}

@app.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):
    

    content = await file.read()
    pdf_id = insert_pdf(file.filename)
    filepath = os.path.join(UPLOAD_DIR, file.filename)
    with open(filepath, "wb") as f:
        f.write(content)

    text = extract_text_from_pdf(filepath)

    cves = extract_cves(text)
    print(cves)
    await asyncio.sleep(60)  

    threat_json = extract_threat_actors(text)
    print(threat_json)

    
    if threat_json is not None:
        for threat in threat_json:
            try:
                threat_id = insert_threat_actors(pdf_id, threat['name'], threat['aliases'], threat['description'])
                print(threat_id)
            except:
                continue

    if cves is not None:
        
        for cve in cves:
            try:
                added = insert_cves(cve['cve_id'], pdf_id, cve['description'], cve['severity'])
            except:
                continue
    
    return  pdf_id
        
       
    
    




    

    # return {
    #     # "pdf_id": pdf_id,
    #    json_res
    #     }


