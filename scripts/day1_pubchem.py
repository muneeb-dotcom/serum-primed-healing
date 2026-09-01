import requests
import pandas as pd
import time
from urllib.parse import quote

compounds = [
    "lactic acid",
    "salicylic acid",
    "ascorbic acid",
    "asiaticoside",
    "acemannan",
    "Pal-KTTKS",
    "GHK-Cu",
    "glycolic acid",
]

headers = {"User-Agent": "Mozilla/5.0"}
base = "https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/name/{}/{}/JSON"
sdf_base = "https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/cid/{}/SDF?record_type=3d"

rows = []

for name in compounds:
    enc = quote(name)
    row = {"name": name, "cid": None, "smiles": None, "sdf_file": None, "note": ""}
    try:
        cid_resp = requests.get(base.format(enc, "cids"), headers=headers, timeout=15).json()
        cid = cid_resp["IdentifierList"]["CID"][0]
        row["cid"] = cid

        prop_resp = requests.get(
            base.format(enc, "property/SMILES"), headers=headers, timeout=15
        ).json()
        row["smiles"] = prop_resp["PropertyTable"]["Properties"][0]["SMILES"]

        sdf_resp = requests.get(sdf_base.format(cid), headers=headers, timeout=15)
        if sdf_resp.status_code == 200 and sdf_resp.text.strip():
            fname = f"data/raw/{name.replace(' ', '_')}_CID{cid}_3d.sdf"
            with open(fname, "w") as f:
                f.write(sdf_resp.text)
            row["sdf_file"] = fname
        else:
            sdf2d_base = f"https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/cid/{cid}/SDF"
            sdf2d_resp = requests.get(sdf2d_base, headers=headers, timeout=15)
            if sdf2d_resp.status_code == 200 and sdf2d_resp.text.strip():
                fname = f"data/raw/{name.replace(' ', '_')}_CID{cid}_2d.sdf"
                with open(fname, "w") as f:
                    f.write(sdf2d_resp.text)
                row["sdf_file"] = fname
                row["note"] = "used 2D SDF (no 3D conformer on PubChem); CB-Dock2 can generate 3D itself"
            else:
                row["note"] = "no SDF (2D or 3D) available"

    except Exception as e:
        row["note"] = f"FAILED: {e}"

    rows.append(row)
    print(row)
    time.sleep(0.5)

df = pd.DataFrame(rows)
df.to_csv("data/processed/day1_compound_list.csv", index=False)
print("\nSaved: data/processed/day1_compound_list.csv")