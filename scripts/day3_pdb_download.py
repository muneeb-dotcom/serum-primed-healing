import requests

headers = {"User-Agent": "Mozilla/5.0"}

targets = {
    "ICAM1": "1IAM",
    "NFKB1": "1SVC",
    "TLR4": "3FXI",
    "MRC1": "6INN",
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