import glob, os, subprocess
from Bio.PDB import PDBParser, PDBIO, Select

SRC_DIR = "data/raw/pdb"
CLEAN_DIR = "data/pdb_clean"
OUT_DIR = "data/pdbqt/receptors"
os.makedirs(CLEAN_DIR, exist_ok=True)
os.makedirs(OUT_DIR, exist_ok=True)

class ProteinOnly(Select):
    def accept_residue(self, residue):
        return residue.id[0] == " "

parser = PDBParser(QUIET=True)
io = PDBIO()

for pdb_file in glob.glob(f"{SRC_DIR}/*.pdb"):
    name = os.path.basename(pdb_file).replace(".pdb", "")
    structure = parser.get_structure(name, pdb_file)
    clean_path = f"{CLEAN_DIR}/{name}_clean.pdb"
    io.set_structure(structure)
    io.save(clean_path, ProteinOnly())

    out_path = f"{OUT_DIR}/{name}.pdbqt"
    r = subprocess.run(["obabel", clean_path, "-O", out_path, "-xr", "-p", "7.4"],
                        capture_output=True, text=True)
    print(name, "OK" if os.path.exists(out_path) else "FAILED")