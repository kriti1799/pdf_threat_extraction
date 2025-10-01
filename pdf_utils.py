import pdfplumber
from dotenv import load_dotenv
import re
import os
from huggingface_hub import InferenceClient
import json



load_dotenv()
api_key_ai = os.getenv("hf_api_key")
client = InferenceClient(
    model="mistralai/Mistral-7B-Instruct-v0.2",
    token=api_key_ai
)


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
    messages = [
    {"role": "system", "content": "You are a cybersecurity analyst.  "},
    {"role": "user", "content": f"I want you to look into the {text[1000:2000]}, look for the following CVES: {cves}  and return a nested JSON object with the following keys:\n  \
    - cve_id (the CVE number, e.g., CVE-2022-22947)\n  \
    - severity (Low, Medium, High, Critical; if not stated, infer based on description)\n  \
    - description (short summary of the vulnerability) \n \
       Return only the JSON object and nothing else. I need to further process your output"}]
    response = client.chat_completion(
    messages=messages,
    temperature=0.2)

    result = response.choices[0].message["content"]

    return result



def extract_threat_actors(text:str):

    
    messages = [
    {"role": "system", "content": "You are an AI that extracts threat actors from text and returns them in JSON format."},
    {"role": "user", "content": f"Extract all threat actors, their aliases and a short description mentioned in the following text:\n\n{text[1000:2000]}\n\n \
     Return only a JSON object with the following keys: \n \
     -name (The name of the threat actor) \n \
     -aliases (Array of known aliases) \n \
     -description (Short summary about the group)\n \
     Return only the JSON object and nothing else. I need to further process your output"}]

# Call mistral
    response = client.chat_completion(
        messages=messages,
        temperature=0.2,
    )

    # Get model output
    result = response.choices[0].message["content"]

    return result

 
def extract_json(response_text):
    """
    Extracts the first valid JSON array or object from model output.
    """
    try:
        # Use regex to capture JSON inside square or curly brackets
        match = re.search(r'(\[.*\]|\{.*\})', response_text, re.DOTALL)
        if match:
            json_str = match.group(1)
            return json.loads(json_str)
    except json.JSONDecodeError:
        pass
    return None









