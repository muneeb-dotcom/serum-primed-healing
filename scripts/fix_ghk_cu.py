in_path = "data/processed/pdbqt_ligands/GHK-Cu_CID139035031_2d.pdbqt"

with open(in_path, "r") as f:
    content = f.read()

# split on the marker that starts the second (peptide) block's REMARK header
blocks = content.split("REMARK  Name = 139035031")
# blocks[0] is empty, blocks[1] is the Cu-only fragment, blocks[2] is the peptide
peptide_block = "REMARK  Name = 139035031" + blocks[2]

with open(in_path, "w") as f:
    f.write(peptide_block)

print("Done. GHK-Cu ligand file now contains only the peptide portion (Cu2+ ion removed).")