import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from config import CLEANED_CSV, TABLE_DIR, FIGURE_DIR, LOG2FC_THRESHOLD

def concentration_dependent(results):
    up = results[(results["low_log2FC"] > LOG2FC_THRESHOLD) & (results["High_log2FC"] > LOG2FC_THRESHOLD)]
    down = results[(results["low_log2FC"] < -LOG2FC_THRESHOLD) & (results["High_log2FC"] < -LOG2FC_THRESHOLD)]
    return up, down

def plot_panel(ax, genes, df_log, title, legend_loc):
    doses = [0, 0.1, 10]
    labels = ["wt", "low", "High"]
    for gene in genes:
        values = [df_log.loc[gene, label] for label in labels]
        ax.plot(doses, values, "o-", linewidth=1.4, markersize=4, alpha=0.85, label=gene)
    ax.set_xscale("symlog", linthresh=0.1)
    ax.set_xticks(doses)
    ax.set_xticklabels(["0", "0.1", "10"])
    ax.set_xlim(-0.01, 15)
    ax.set_xlabel("PS-NPs concentration (mg/L)")
    ax.set_ylabel("log2(count + 1)")
    ax.set_title(title)
    ax.grid(alpha=0.25)
    ax.legend(fontsize=7, loc=legend_loc, frameon=False)

def main():
    df = pd.read_csv(CLEANED_CSV, index_col="GeneID")
    df_log = np.log2(df + 1)
    results = pd.read_csv(TABLE_DIR / "all_genes_log2fc.csv", index_col="GeneID")

    up, down = concentration_dependent(results)
    up = up.sort_values("High_log2FC", ascending=False)
    down = down.sort_values("High_log2FC", ascending=True)

    up.to_csv(TABLE_DIR / "concentration_dependent_up_candidate_genes.csv")
    down.to_csv(TABLE_DIR / "concentration_dependent_down_candidate_genes.csv")

    top_up = up.head(5).index.tolist()
    top_down = down.head(5).index.tolist()

    fig, axes = plt.subplots(2, 1, figsize=(8, 9))
    plot_panel(axes[0], top_up, df_log,
               f"Concentration-dependent candidate up-regulation (n={len(up)})", "upper left")
    plot_panel(axes[1], top_down, df_log,
               f"Concentration-dependent candidate down-regulation (n={len(down)})", "lower left")
    fig.tight_layout()
    output = FIGURE_DIR / "fig08_dose_response.png"
    fig.savefig(output, dpi=300, bbox_inches="tight")
    plt.close(fig)

    print(f"Concentration-dependent candidate up-regulated genes: {len(up)}")
    print(f"Concentration-dependent candidate down-regulated genes: {len(down)}")
    print(f"Saved: {output}")

if __name__ == "__main__":
    main()
