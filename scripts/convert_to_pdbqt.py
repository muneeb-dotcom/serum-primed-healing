import glob
import os
import subprocess

os.makedirs("data/processed/pdbqt_ligands", exist_ok=True)
os.makedirs("data/processed/pdbqt_receptors", exist_ok=True)

# convert ligands (use trimmed sdf where available, else original)
sdf_files = glob.glob("data/raw/*_trimmed.sdf")
trimmed_names = {os.path.basename(f).replace("_trimmed.sdf", "") for f in sdf_files}
all_sdf = glob.glob("data/raw/*.sdf")
for f in all_sdf:
    base = os.path.basename(f).replace(".sdf", "").replace("_trimmed", "")
    if "_trimmed" not in f and base in trimmed_names:
        continue  # skip untrimmed if trimmed version exists
    out = f"data/processed/pdbqt_ligands/{base}.pdbqt"
    cmd = ["obabel", f, "-O", out, "--gen3d"]
    result = subprocess.run(cmd, capture_output=True, text=True)
    print(f"LIGAND {base}: {'OK' if os.path.exists(out) else 'FAILED'}")

# convert receptors
pdb_files = glob.glob("data/raw/pdb/*.pdb")
for f in pdb_files:
    base = os.path.basename(f).replace(".pdb", "")
    out = f"data/processed/pdbqt_receptors/{base}.pdbqt"
    cmd = ["obabel", f, "-O", out, "-xr"]  # -xr = treat as rigid receptor
    result = subprocess.run(cmd, capture_output=True, text=True)
    print(f"RECEPTOR {base}: {'OK' if os.path.exists(out) else 'FAILED'}")