import os
import pandas as pd
from vina import Vina

os.makedirs("results/poses", exist_ok=True)

# remaining 8 pairs: (ligand_pdbqt_basename, receptor_pdbqt_basename)
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
MAX_BOX = 60.0  # cap box dimension in Angstrom to keep runtime reasonable
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
    return [cx, cy, cz], [sx, sy, sz]


rows = []
for lig_base, rec_base in pairs:
    lig_path = f"{LIG_DIR}/{lig_base}.pdbqt"
    rec_path = f"{REC_DIR}/{rec_base}.pdbqt"

    if not os.path.exists(lig_path) or not os.path.exists(rec_path):
        print(f"SKIP: missing file for {lig_base} / {rec_base}")
        continue

    center, box_size = compute_autobox(rec_path)

    try:
        v = Vina(sf_name="vina")
        v.set_receptor(rec_path)
        v.set_ligand_from_file(lig_path)
        v.compute_vina_maps(center=center, box_size=box_size)
        v.dock(exhaustiveness=8, n_poses=9)

        out_path = f"results/poses/{lig_base}_{rec_base}.pdbqt"
        v.write_poses(out_path, n_poses=1, overwrite=True)
        score = v.energies(n_poses=1)[0][0]

        print(f"{lig_base} {rec_base} {score:.2f}")
        rows.append({"compound": lig_base, "target": rec_base, "docking_score_kcal_mol": round(score, 2)})

    except Exception as e:
        print(f"FAILED: {lig_base} + {rec_base} - {e}")

df = pd.DataFrame(rows)
df.to_csv("results/docking/docking_scores_vina_batch2.csv", index=False)
print(df)