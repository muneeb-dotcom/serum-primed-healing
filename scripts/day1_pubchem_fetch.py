import requests, time, os, pandas as pd

COMPOUNDS = ["lactic acid", "salicylic acid", "ascorbic acid", "asiaticoside",
             "acemannan", "Pal-KTTKS", "GHK-Cu", "glycolic acid"]

BASE = "https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound"
os.makedirs("compounds", exist_ok=True)
rows = []

for name in COMPOUNDS:
    try:
        cid = requests.get(f"{BASE}/name/{name}/cids/JSON").json()["IdentifierList"]["CID"][0]
        smiles = requests.get(f"{BASE}/cid/{cid}/property/CanonicalSMILES/JSON").json()["PropertyTable"]["Properties"][0]["CanonicalSMILES"]
        sdf_path, sdf_type = None, None
        for rt in ("3d", "2d"):
            r = requests.get(f"{BASE}/cid/{cid}/record/SDF/", params={"record_type": rt})
            if r.ok and r.text.strip():
                sdf_path = f"compounds/{name.replace(' ','_')}.sdf"
                open(sdf_path, "w").write(r.text)
                sdf_type = rt
                break
        rows.append({"name": name, "cid": cid, "smiles": smiles, "sdf_path": sdf_path, "sdf_type": sdf_type})
        print(f"OK {name}: CID={cid} sdf={sdf_type}")
    except Exception as e:
        rows.append({"name": name, "cid": None, "smiles": None, "sdf_path": None, "sdf_type": None})
        print(f"FAIL {name}: {e}")
    time.sleep(0.3)

pd.DataFrame(rows).to_csv("compounds/day1_compounds.csv", index=False)