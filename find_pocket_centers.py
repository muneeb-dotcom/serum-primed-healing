import glob, os, json
import numpy as np
from Bio.PDB import PDBParser

SRC_DIR = "data/raw/pdb"

IGNORE_RESIDUES = {
    "HOH", "WAT", "NA", "CL", "MG", "ZN", "CA", "K", "MN", "FE", "CO", "NI",
    "SO4", "PO4", "GOL", "EDO", "ACT", "DMS", "PEG", "PG4", "BME", "MPD",
    "TRS", "IMD", "FMT", "ACY", "1PE", "P6G", "EPE", "MES", "CIT", "MPO", "DTD",
    "MSE", "SEP", "TPO", "PTR", "CSO", "CSD", "MLY", "KCX", "PCA", "HYP",
    "NAG", "BMA", "MAN", "FUC", "GAL", "BGC", "GLC", "SIA", "NDG",
    "CLR", "CHS", "OLA", "OLB", "OLC", "LMT", "LDA", "LMN", "PLM", "MYR",
}

os.makedirs("data/pdbqt", exist_ok=True)
parser = PDBParser(QUIET=True)
configs = {}
flagged = []

for pdb_file in glob.glob(f"{SRC_DIR}/*.pdb"):
    name = os.path.basename(pdb_file).replace(".pdb", "")
    structure = parser.get_structure(name, pdb_file)

    hetero_groups = {}
    for residue in structure.get_residues():
        if residue.id[0] == " ":
            continue
        resname = residue.resname.strip()
        if resname in IGNORE_RESIDUES:
            continue
        coords = [atom.coord for atom in residue.get_atoms()]
        hetero_groups.setdefault(resname, []).extend(coords)

    if not hetero_groups:
        print(name, "-- no candidate ligand")
        flagged.append(name)
        continue

    best = max(hetero_groups, key=lambda r: len(hetero_groups[r]))
    coords = np.array(hetero_groups[best])
    center = coords.mean(axis=0)
    extent = coords.max(axis=0) - coords.min(axis=0)
    size = np.maximum(extent + 10, [20, 20, 20])

    if size.max() > 40:
        print(name, "->", best, "SUSPICIOUS (box too big, likely not a real ligand)")
        flagged.append(name)
        continue

    configs[name] = {
        "ligand_used": best,
        "center_x": round(float(center[0]), 2), "center_y": round(float(center[1]), 2), "center_z": round(float(center[2]), 2),
        "size_x": round(float(size[0]), 2), "size_y": round(float(size[1]), 2), "size_z": round(float(size[2]), 2),
    }
    print(name, "->", best, center.round(1), size.round(1))

with open("data/pdbqt/box_configs.json", "w") as f:
    json.dump(configs, f, indent=2)

if flagged:
    print("\nNeeds manual check:", ", ".join(flagged))