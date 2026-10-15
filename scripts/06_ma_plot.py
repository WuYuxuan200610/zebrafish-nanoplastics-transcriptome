import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from config import TABLE_DIR, FIGURE_DIR, LOG2FC_THRESHOLD

def plot_ma(ax, results, candidates, raw_treatment, fc_col, title):
    log_expr = np.log2(results[["High_raw", "low_raw", "wt_raw"]] + 1)
    control_col = "wt_raw"
    mean_expr = (log_expr[raw_treatment] + log_expr[control_col]) / 2
    fc = results[fc_col]

    ax.scatter(mean_expr, fc, s=6, c="#bdbdbd", alpha=0.35, linewidths=0, label="All genes")
    up = candidates[candidates[fc_col] > LOG2FC_THRESHOLD]
    down = candidates[candidates[fc_col] < -LOG2FC_THRESHOLD]
    ax.scatter(mean_expr.loc[up.index], fc.loc[up.index], s=10, c="#d7301f", alpha=0.8,
               linewidths=0, label=f"Candidate up ({len(up)})")
    ax.scatter(mean_expr.loc[down.index], fc.loc[down.index], s=10, c="#2166ac", alpha=0.8,
               linewidths=0, label=f"Candidate down ({len(down)})")
    ax.axhline(0, color="black", linewidth=0.8)
    ax.axhline(LOG2FC_THRESHOLD, color="black", linestyle="--", linewidth=0.8, alpha=0.6)
    ax.axhline(-LOG2FC_THRESHOLD, color="black", linestyle="--", linewidth=0.8, alpha=0.6)
    ax.set_xlabel("Mean expression: log2(count + 1)")
    ax.set_ylabel("log2 fold change")
    ax.set_title(title)
    ax.grid(alpha=0.25)

def main():
    results = pd.read_csv(TABLE_DIR / "all_genes_log2fc.csv", index_col="GeneID")
    high = pd.read_csv(TABLE_DIR / "high_vs_wt_candidate_genes.csv", index_col="GeneID")
    low = pd.read_csv(TABLE_DIR / "low_vs_wt_candidate_genes.csv", index_col="GeneID")

    fig, axes = plt.subplots(1, 2, figsize=(13, 5.5), sharey=True)
    plot_ma(axes[0], results, high, "High_raw", "High_log2FC",
            f"MA plot: High vs WT\nCandidate genes: {len(high)}")
    plot_ma(axes[1], results, low, "low_raw", "low_log2FC",
            f"MA plot: low vs WT\nCandidate genes: {len(low)}")
    axes[0].legend(loc="upper right", fontsize=8, frameon=False)
    fig.tight_layout()
    output = FIGURE_DIR / "fig06_ma_plots.png"
    fig.savefig(output, dpi=300, bbox_inches="tight")
    plt.close(fig)
    print(f"Saved: {output}")

if __name__ == "__main__":
    main()
