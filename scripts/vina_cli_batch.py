import os
import subprocess
import pandas as pd

os.makedirs("results/poses", exist_ok=True)
os.makedirs("results/docking", exist_ok=True)

pairs = [
    ("salicylic_acid_CID338_3d", "PTGS2_5F19"),
    ("ascorbic_acid_CID54670067_3d", "P4HA1_9HRE"),
    ("ascorbic_acid_CID54670067_3d", "P4HA2_6EVN"),
    ("asiaticoside_CID11954171_2d", "CASP3_2J32"),
    ("asiaticoside_CID11954171_2d", "NFKB1_1SVC"),
    ("asiaticoside_CID11954171_2d", "ICAM1_1IAM"),
    ("Pal-KTTKS_CID9897237_2d", "COL1A1_5CTD"),
    ("GHK-Cu_CID139035031_2d", "MMP2_3AYU"),
]

LIG_DIR = "data/processed/pdbqt_ligands"
REC_DIR = "data/processed/pdbqt_receptors"
VINA_EXE = "vina.exe"  # must be on PATH or in this folder
MAX_BOX = 60.0
PADDING = 8.0


def compute_autobox(pdbqt_path):
    xs, ys, zs = [], [], []
    with open(pdbqt_path, "r") as f:
        for line in f:
            if line.startswith(("ATOM", "HETATM")):
                xs.append(float(line[30:38]))
                ys.append(float(line[38:46]))
                zs.append(float(line[46:54]))
    cx, cy, cz = (max(xs) + min(xs)) / 2, (max(ys) + min(ys)) / 2, (max(zs) + min(zs)) / 2
    sx = min(max(xs) - min(xs) + PADDING, MAX_BOX)
    sy = min(max(ys) - min(ys) + PADDING, MAX_BOX)
    sz = min(max(zs) - min(zs) + PADDING, MAX_BOX)
    return cx, cy, cz, sx, sy, sz


rows = []
for lig_base, rec_base in pairs:
    lig_path = f"{LIG_DIR}/{lig_base}.pdbqt"
    rec_path = f"{REC_DIR}/{rec_base}.pdbqt"
    out_path = f"results/poses/{lig_base}_{rec_base}.pdbqt"
    log_path = f"results/poses/{lig_base}_{rec_base}.log"

    if not os.path.exists(lig_path) or not os.path.exists(rec_path):
        print(f"SKIP: missing file for {lig_base} / {rec_base}")
        continue

    cx, cy, cz, sx, sy, sz = compute_autobox(rec_path)

    cmd = [
        VINA_EXE,
        "--receptor", rec_path,
        "--ligand", lig_path,
        "--center_x", str(cx), "--center_y", str(cy), "--center_z", str(cz),
        "--size_x", str(sx), "--size_y", str(sy), "--size_z", str(sz),
        "--out", out_path,
        "--exhaustiveness", "8",
        "--num_modes", "9",
    ]

    print(f"Running: {lig_base} + {rec_base} ...")
    result = subprocess.run(cmd, capture_output=True, text=True)

    with open(log_path, "w") as f:
        f.write(result.stdout)
        f.write(result.stderr)

        score = None
    capture = False
    for line in result.stdout.splitlines():
        if line.strip().startswith("mode"):
            capture = True
            continue
        if capture and line.strip().startswith("1"):
            parts = line.split()
            try:
                score = float(parts[1])
            except (ValueError, IndexError):
                pass
            break

    print(f"{lig_base} {rec_base} score={score}")
    rows.append({"compound": lig_base, "target": rec_base, "docking_score_kcal_mol": score})

df = pd.DataFrame(rows)
df.to_csv("results/docking/docking_scores_vina_batch2.csv", index=False)
print(df)