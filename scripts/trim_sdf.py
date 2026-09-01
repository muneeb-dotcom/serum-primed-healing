import glob
import os

for fname in glob.glob("data/raw/*.sdf"):
    with open(fname, "r") as f:
        lines = f.readlines()

    out_lines = []
    for line in lines:
        out_lines.append(line)
        if line.startswith("M  END"):
            break
    out_lines.append("$$$$\n")

    out_fname = fname.replace(".sdf", "_trimmed.sdf")
    with open(out_fname, "w") as f:
        f.writelines(out_lines)

    orig_size = os.path.getsize(fname)
    new_size = os.path.getsize(out_fname)
    print(f"{fname}: {orig_size} bytes -> {out_fname}: {new_size} bytes")