import glob

valid_prefixes = ("ATOM", "HETATM", "TER", "ROOT", "ENDROOT", "BRANCH", "ENDBRANCH", "TORSDOF", "REMARK")

for fname in glob.glob("data/processed/pdbqt_receptors/*.pdbqt"):
    with open(fname, "r") as f:
        lines = f.readlines()

    clean_lines = [line for line in lines if line.startswith(valid_prefixes)]

    with open(fname, "w") as f:
        f.writelines(clean_lines)

    print(f"Cleaned: {fname} ({len(lines)} -> {len(clean_lines)} lines)")