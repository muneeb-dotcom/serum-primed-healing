import pandas as pd
import matplotlib.pyplot as plt
import os

os.makedirs("results/figures", exist_ok=True)

df = pd.read_csv("results/docking/docking_scores_all.csv")
df = df.dropna(subset=["docking_score_kcal_mol"])
df["pair"] = df["compound"] + " + " + df["target"]
df = df.sort_values("docking_score_kcal_mol")

# --- Figure 1: bar chart, all pairs, sorted by strength ---
fig, ax = plt.subplots(figsize=(10, 6))
colors = ["#2c7fb8" if c == "asiaticoside" else "#41b6c4" for c in df["compound"]]
ax.barh(df["pair"], df["docking_score_kcal_mol"], color=colors)
ax.set_xlabel("Docking Score (kcal/mol)")
ax.set_title("AutoDock Vina Docking Scores by Compound-Target Pair")
ax.axvline(0, color="black", linewidth=0.8)
plt.tight_layout()
plt.savefig("results/figures/docking_scores_bar.png", dpi=300)
plt.savefig("results/figures/docking_scores_bar.svg")
plt.close()
print("Saved: docking_scores_bar.png / .svg")

# --- Figure 2: grouped by compound ---
fig, ax = plt.subplots(figsize=(10, 6))
compounds = df["compound"].unique()
colors_map = plt.cm.tab10.colors
for i, compound in enumerate(compounds):
    sub = df[df["compound"] == compound]
    ax.scatter(sub["docking_score_kcal_mol"], sub["target"] + " (" + compound + ")",
               s=100, color=colors_map[i % len(colors_map)], label=compound)
ax.set_xlabel("Docking Score (kcal/mol)")
ax.set_title("Docking Scores Grouped by Compound")
ax.legend(bbox_to_anchor=(1.02, 1), loc="upper left", fontsize=8)
plt.tight_layout()
plt.savefig("results/figures/docking_scores_by_compound.png", dpi=300)
plt.savefig("results/figures/docking_scores_by_compound.svg")
plt.close()
print("Saved: docking_scores_by_compound.png / .svg")

print("\nAll figures saved to results/figures/")