import requests

headers = {"User-Agent": "Mozilla/5.0"}

targets = {
    "PTGS2": "5F19",
    "CASP3": "2J32",
    "CASP8": "4JJ7",
    "MMP2": "3AYU",
    "P4HA1": "9HRE",
    "P4HA2": "6EVN",
    "HCAR2": "8J6P",
    "COL1A1": "5CTD",
}

base = "https://files.rcsb.org/download/{}.pdb"

for gene, pdb_id in targets.items():
    url = base.format(pdb_id)
    try:
        resp = requests.get(url, headers=headers, timeout=20)
        if resp.status_code == 200 and resp.text.strip():
            fname = f"data/raw/pdb/{gene}_{pdb_id}.pdb"
            with open(fname, "w") as f:
                f.write(resp.text)
            print(f"OK: {gene} -> {fname}")
        else:
            print(f"FAILED: {gene} ({pdb_id}) - status {resp.status_code}")
    except Exception as e:
        print(f"FAILED: {gene} ({pdb_id}) - {e}")