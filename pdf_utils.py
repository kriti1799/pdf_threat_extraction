import pdfplumber
from dotenv import load_dotenv
import re
import os
import json
import google.generativeai as genai

load_dotenv()
my_api_key = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=my_api_key)
model = genai.GenerativeModel('gemini-2.0-flash')

def extract_text_from_pdf(pdf_path):
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    return text

def extract_cves(text):
    cves = re.findall(r"CVE-\d{4}-\d{4,7}", text)
    prompt = f"""
    You are a cybersecurity analyst.

    Analyze the following report text and look for these CVEs: {cves}.

    Return **only** a valid JSON array, no explanations, no markdown code blocks.

    Each element in the array must be an object with keys:
    - "cve_id": string (e.g., "CVE-2022-22947")
    - "severity": one of ["Low", "Medium", "High", "Critical"]
    - "description": string summarizing the vulnerability

    If no CVEs are found, return an empty JSON array [].
    Text to analyze:
    {text}
    """
    response_text = model.generate_content(prompt).text
    if not response_text:
        return None

    # 1. Clean up Markdown/extra wrapping
    clean_text = response_text.strip()
    clean_text = re.sub(r"^(```json|```|'''json|''')|(```|''')$", "",clean_text,flags=re.MULTILINE).strip()

    try:
        return json.loads(clean_text)
    except json.JSONDecodeError:
        pass

    match = re.search(r"(\[.*\]|\{.*\})", clean_text, re.DOTALL)
    if match:
        try:
            return json.loads(match.group(1))
        except json.JSONDecodeError:
            pass

    return None



def extract_threat_actors(text:str):

    
    prompt = "You are an AI that extracts threat actors and CVE from text and returns them in JSON format. Extract all threat actors, their aliases and a short description mentioned in the following text:\n\n{text}\n\n \
     Return only a JSON object with the following keys: \n \
     -name (The name of the threat actor) \n \
     -aliases (Array of known aliases) \n \
     -description (Short summary about the group)\n \
     Return only the JSON object and nothing else. I need to further process your output \n" \
     "If no threat actors are found, return an empty JSON array []"
    
    response_text = model.generate_content(prompt).text
    if not response_text:
        return None

    # 1. Clean up Markdown/extra wrapping
    clean_text = response_text.strip()
    clean_text = re.sub(r"^(```json|```|'''json|''')|(```|''')$", "",clean_text,flags=re.MULTILINE).strip()

    try:
        return json.loads(clean_text)
    except json.JSONDecodeError:
        pass

    match = re.search(r"(\[.*\]|\{.*\})", clean_text, re.DOTALL)
    if match:
        try:
            return json.loads(match.group(1))
        except json.JSONDecodeError:
            pass

    return None











