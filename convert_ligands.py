import glob, os, subprocess

SRC_DIR = "data/raw"
OUT_DIR = "data/pdbqt/ligands"
os.makedirs(OUT_DIR, exist_ok=True)

trimmed = glob.glob(f"{SRC_DIR}/*_trimmed.sdf")
trimmed_stems = {os.path.basename(f).replace("_trimmed.sdf", "") for f in trimmed}
originals = [f for f in glob.glob(f"{SRC_DIR}/*.sdf")
             if not f.endswith("_trimmed.sdf")
             and os.path.basename(f).replace(".sdf", "") not in trimmed_stems]

for sdf in trimmed + originals:
    name = os.path.basename(sdf).replace("_trimmed.sdf", "").replace(".sdf", "")
    out = f"{OUT_DIR}/{name}.pdbqt"
    r = subprocess.run(["obabel", sdf, "-O", out, "-p", "7.4", "--partialcharge", "gasteiger"],
                        capture_output=True, text=True)
    print(name, "OK" if os.path.exists(out) else "FAILED")