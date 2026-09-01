import requests
from urllib.parse import quote

name = quote("lactic acid")
headers = {"User-Agent": "Mozilla/5.0"}
url = f"https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/name/{name}/cids/JSON"
r = requests.get(url, headers=headers, timeout=15)
print(r.status_code)
print(r.text)