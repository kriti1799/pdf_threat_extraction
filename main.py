from fastapi import FastAPI, File, UploadFile
from pdf_utils import extract_text_from_pdf, extract_threat_actors, extract_cves, extract_json
from db_helper import insert_pdf, insert_threat_actors, insert_cves
import os


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
    cves_json = extract_json(cves)

    print(cves_json)

    threats = extract_threat_actors(text)
    threat_json = extract_json(threats)
    # print("CVEs are", cves)

    print(threat_json)

    # cves_json = [{'cve_id': 'CVE-2022-229476', 'severity': 'Medium', 'description': 'Arbitrary code execution vulnerability in Laravel, a popular web application framework, due to insufficient input validation (CWE-23).'}, {'cve_id': 'CVE-2021-442289', 'severity': 'High', 'description': "Remote code execution vulnerability in Android's MediaFramework, allowing attackers to execute arbitrary code via specially crafted media files."}, {'cve_id': 'CVE-2020-1488211', 'severity': 'Critical', 'description': "Zero-day vulnerability in Apple's iOS and iPadOS that could allow attackers to execute arbitrary code with kernel privileges."}, {'cve_id': 'CVE-2019-272513', 'severity': 'High', 'description': 'Remote code execution vulnerability in Adobe Acrobat and Reader due to a use-after-free issue in the JavaScript engine.'}, {'cve_id': 'CVE-2022-22947', 'severity': 'Medium', 'description': 'Command injection vulnerability in Laravel, a web application framework, due to insufficient input validation (CWE-77).'}, {'cve_id': 'CVE-2020-14882', 'severity': 'High', 'description': 'Remote code execution vulnerability in Microsoft Exchange Server due to a zero-day exploit in the ProxyLogon component.'}, {'cve_id': 'CVE-2022-26134', 'severity': 'High', 'description': 'Remote code execution vulnerability in Google Chrome due to a use-after-free issue in the V8 JavaScript engine.'}, {'cve_id': 'CVE-2019-2725', 'severity': 'Medium', 'description': 'Information disclosure vulnerability in the Apache Struts web application framework due to a deserialization issue.'}] 
    #   threat_json = [{'name': 'RomCom Threat Actor', 'aliases': [], 'description': 'A threat actor known for abusing popular mobile devices software brands to target Ukraine and potentially the United Kingdom with crypto miners and cryptojacking.'}, {'name': 'Mustang Panda', 'aliases': ['APT31', 'Chinese APT'], 'description': 'An advanced persistent threat (APT) group that uses the Russian-Ukrainian war as a theme to attack Europe and Asia Pacific targets with industry-specific attacks, including downloaders, infostealers, Emotet, ransomware (CryWiper), dual-use tools, and supply-chain attacks.'}, {'name': 'ARCrypter', 'aliases': [], 'description': 'A ransomware group that has expanded its operations from Latin America to the world.'}]

    if threat_json is not None:
        for threat in threat_json:
            try:
                threat_id = insert_threat_actors(pdf_id, threat['name'], threat['aliases'], threat['description'])
            except:
                continue

    if cves_json is not None:
    
        for cve in cves_json:
            try:
                added = insert_cves(cve['cve_id'], pdf_id, cve['description'], cve['severity'])
            except:
                continue
    
    return  pdf_id
       
    
    




    

    # return {
    #     # "pdf_id": pdf_id,
    #    json_res
    #     }


