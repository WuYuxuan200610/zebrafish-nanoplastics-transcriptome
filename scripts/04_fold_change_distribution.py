import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from config import (
    TABLE_DIR, FIGURE_DIR, LOG2FC_THRESHOLD,
)

def plot_comparison(ax, results, fc_col, candidate_df, title):
    y = -np.log10(results[fc_col].abs() + 0.01)
    ax.scatter(results[fc_col], y, s=7, c="#bdbdbd", alpha=0.35, linewidths=0, label="All genes")

    up = candidate_df[candidate_df[fc_col] > LOG2FC_THRESHOLD]
    down = candidate_df[candidate_df[fc_col] < -LOG2FC_THRESHOLD]
    ax.scatter(up[fc_col], y.loc[up.index], s=11, c="#d7301f", alpha=0.75, linewidths=0,
               label=f"Candidate up ({len(up)})")
    ax.scatter(down[fc_col], y.loc[down.index], s=11, c="#2166ac", alpha=0.75, linewidths=0,
               label=f"Candidate down ({len(down)})")

    cutoff_y = -np.log10(LOG2FC_THRESHOLD + 0.01)
    ax.axvline(-LOG2FC_THRESHOLD, color="black", linestyle="--", linewidth=0.8, alpha=0.6)
    ax.axvline(LOG2FC_THRESHOLD, color="black", linestyle="--", linewidth=0.8, alpha=0.6)
    ax.axhline(cutoff_y, color="black", linestyle=":", linewidth=0.8, alpha=0.6)
    ax.set_xlabel("log2 fold change")
    ax.set_ylabel("Fold-change magnitude: -log10(|log2FC| + 0.01)")
    ax.set_title(title)
    ax.grid(alpha=0.25)

def main():
    results = pd.read_csv(TABLE_DIR / "all_genes_log2fc.csv", index_col="GeneID")
    high = pd.read_csv(TABLE_DIR / "high_vs_wt_candidate_genes.csv", index_col="GeneID")
    low = pd.read_csv(TABLE_DIR / "low_vs_wt_candidate_genes.csv", index_col="GeneID")

    fig, axes = plt.subplots(1, 2, figsize=(13, 5.5), sharey=True)
    plot_comparison(axes[0], results, "High_log2FC", high,
                    f"High vs WT candidate genes\n(n={len(high)})")
    plot_comparison(axes[1], results, "low_log2FC", low,
                    f"Low vs WT candidate genes\n(n={len(low)})")
    axes[0].legend(loc="upper left", fontsize=8, frameon=False)
    fig.suptitle("Fold-change magnitude distribution (fold-change screening only)", y=0.98)
    fig.tight_layout()
    output = FIGURE_DIR / "fig05_fold_change_distribution.png"
    fig.savefig(output, dpi=300, bbox_inches="tight")
    plt.close(fig)
    print(f"Saved: {output}")

if __name__ == "__main__":
    main()
