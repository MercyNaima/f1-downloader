import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import webbrowser
import mimetypes
import json

BASE_DIR = 'f1_documents'
os.makedirs(BASE_DIR, exist_ok=True)

def get_gp_dir(grand_prix):
    safe_name = grand_prix.replace(" ", "_")
    gp_dir = os.path.join(BASE_DIR, safe_name)
    os.makedirs(gp_dir, exist_ok=True)
    return gp_dir

def fetch_documents(url, keyword=''):
    try:
        resp = requests.get(url)
        soup = BeautifulSoup(resp.text, 'html.parser')
        results = []
        for link in soup.find_all('a', href=True):
            href = link['href']
            text = link.get_text(strip=True)
            if any(href.endswith(ext) for ext in ['.pdf', '.doc', '.xls']) and keyword.lower() in text.lower():
                full_url = urljoin(url, href)
                results.append((text or os.path.basename(href), full_url))
        return results
    except Exception:
        return []

def download_and_open(name, url, grand_prix):
    gp_dir = get_gp_dir(grand_prix)
    response = requests.get(url, stream=True)
    content_disp = response.headers.get("Content-Disposition", "")
    if "filename=" in content_disp:
        name = content_disp.split("filename=")[-1].strip("\"'")
    else:
        if not name.lower().endswith(('.pdf', '.doc', '.xls')):
            guessed_ext = mimetypes.guess_extension(response.headers.get("Content-Type", "").split(";")[0])
            name += guessed_ext if guessed_ext else ".pdf"
    local_path = os.path.join(gp_dir, name)
    if not os.path.exists(local_path):
        with open(local_path, 'wb') as f:
            for chunk in response.iter_content(1024):
                f.write(chunk)
    try:
        os.startfile(local_path)
    except:
        webbrowser.open(local_path)

def list_local_files(grand_prix):
    gp_dir = get_gp_dir(grand_prix)
    return [f for f in os.listdir(gp_dir) if os.path.isfile(os.path.join(gp_dir, f))]

def delete_local_file(grand_prix, filename):
    gp_dir = get_gp_dir(grand_prix)
    file_path = os.path.join(gp_dir, filename)
    if os.path.exists(file_path):
        os.remove(file_path)
        return True
    return False

def load_local_grand_prix(json_path='grand_prix_list.json'):
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print("Failed to load Grand Prix list from JSON:", e)
        return {}
