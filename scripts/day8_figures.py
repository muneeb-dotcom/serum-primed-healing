import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

os.makedirs("results/figures", exist_ok=True)
df = pd.read_csv("results/de_tables/day8_mouse_human_cross_reference.csv")

fig, ax = plt.subplots(figsize=(6, 8))
data = df[["mouse_log2FC", "human_log2FC"]].values
im = ax.imshow(data, cmap="RdBu_r", vmin=-4, vmax=4, aspect="auto")
ax.set_yticks(range(len(df)))
ax.set_yticklabels(df["target"])
ax.set_xticks([0, 1])
ax.set_xticklabels(["Mouse", "Human"])
ax.set_title("log2FC by Target: Mouse vs Human\n(positive=regenerative/normal, negative=scarring/keloid)", fontsize=10)
for i in range(len(df)):
    for j, col in enumerate(["mouse_log2FC", "human_log2FC"]):
        val = df[col].iloc[i]
        txt = f"{val:.2f}" if not np.isnan(val) else "NA"
        ax.text(j, i, txt, ha="center", va="center", fontsize=8)
plt.colorbar(im, ax=ax, label="log2FoldChange")
plt.tight_layout()
plt.savefig("results/figures/day8_mouse_vs_human_heatmap.png", dpi=300)
plt.savefig("results/figures/day8_mouse_vs_human_heatmap.svg")
plt.close()
print("Saved: day8_mouse_vs_human_heatmap.png / .svg")

mouse_sig = (df["mouse_padj"] < 0.05).sum()
human_sig = (df["human_padj"] < 0.05).sum()
mouse_total = df["mouse_padj"].notna().sum()
human_total = df["human_padj"].notna().sum()

fig, ax = plt.subplots(figsize=(6, 5))
species = ["Mouse", "Human"]
sig_counts = [mouse_sig, human_sig]
total_counts = [mouse_total, human_total]
x = np.arange(len(species))
ax.bar(x, total_counts, color="#cccccc", label="Tested")
ax.bar(x, sig_counts, color="#2c7fb8", label="Significant (padj<0.05)")
ax.set_xticks(x)
ax.set_xticklabels(species)
ax.set_ylabel("Number of targets (out of 13)")
ax.set_title("Target Significance by Species")
ax.legend()
plt.tight_layout()
plt.savefig("results/figures/day8_significance_summary.png", dpi=300)
plt.savefig("results/figures/day8_significance_summary.svg")
plt.close()
print("Saved: day8_significance_summary.png / .svg")