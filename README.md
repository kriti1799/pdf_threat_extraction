# PDF Threat Intelligence Extraction Service

This is a FastAPI microservice that extracts threat actors and CVEs from PDF threat intelligence reports using AI (Gemini/other LLMs) and stores the results in a database.

---

## Features

- Upload PDFs via FastAPI endpoint
- Extract text from PDFs
- Analyze text using Gemini API to extract:
  - CVEs (CVE ID, severity, description)
  - Threat actors (name, aliases, description)
- Store structured results in SQLite (or other DB)
- Supports robust parsing of AI outputs (handles Markdown/code fences)
- Handles rate-limited API calls gracefully with optional wait/retry

---

## Prerequisites

- Python 3.10+
- Gemini API key
- SQLite (or your preferred DB)
- `pip` for dependencies

---

## Setup Instructions

### 1. Clone the repository
```bash
git clone https://github.com/yourusername/pdf-threat-extraction.git
cd pdf-threat-extraction
``` 
### 2. Create a virtual environment
```bash
python3 -m venv env
source env/bin/activate   # macOS/Linux
# OR
env\Scripts\activate 
```

### 3. Install Dependencies
``` bash
pip install -r requirements.txt
```

### 4. Setup environment variables in a .env file
``` bash
GOOGLE_API_KEY = your api key here
```

### 5. Run the FASTAPI APP
``` bash
uvicorn main:app --reload
```

### 6. Visit the Swagger UI:
- Visit the Swagger UI: http://127.0.0.1:8000/docs
- Use /upload_pdf endpoint to upload a PDF.
- The service will analyze the PDF and store CVEs and threat actors in the database.

### 7. Database access
The tables are stored in a database named pdf_threat.db.
The values of all the tables can be printed by simply running:
``` bash
python table_print.py
```
ALternatively, table contents can also be chacked by
``` bash
sqlite3 database.db
.tables
SELECT * FROM pdf_documents;
SELECT * FROM cves ;
SELECT * FROM threat_actors ;
```
### 8. Notes:
- To handle rate limits, I have added a time.sleep between checking for CVEs and threat actors. The application might take a minute to fully load the results. 
- API Key can be obtained from "https://ai.google.dev/api"