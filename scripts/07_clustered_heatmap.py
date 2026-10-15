import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scipy.cluster.hierarchy import leaves_list, linkage
from scipy.spatial.distance import pdist
from config import CLEANED_CSV, TABLE_DIR, FIGURE_DIR, SAMPLE_COLUMNS, TOP_N_HEATMAP

def zscore_rows(matrix):
    mean = matrix.mean(axis=1)
    std = matrix.std(axis=1).replace(0, np.nan)
    z = matrix.sub(mean, axis=0).div(std, axis=0)
    return z.dropna(how="any")

def clustered_order(matrix, axis=0):
    data = matrix if axis == 0 else matrix.T
    if data.shape[0] <= 2:
        return list(range(data.shape[0]))
    clustering = linkage(pdist(data.values, metric="euclidean"), method="average")
    return list(leaves_list(clustering))

def main():
    df = pd.read_csv(CLEANED_CSV, index_col="GeneID")
    df_log = np.log2(df + 1)
    results = pd.read_csv(TABLE_DIR / "all_genes_log2fc.csv", index_col="GeneID")

    score = pd.concat([
        results["High_log2FC"].abs(),
        results["low_log2FC"].abs(),
    ], axis=1).max(axis=1)
    score = score.sort_values(ascending=False)
    top_genes = score.head(TOP_N_HEATMAP).index.tolist()

    heatmap_data = df_log.loc[top_genes, SAMPLE_COLUMNS]
    heatmap_z = zscore_rows(heatmap_data)
    heatmap_z.to_csv(TABLE_DIR / "top50_heatmap_zscores.csv")
    pd.DataFrame({"GeneID": top_genes}).to_csv(TABLE_DIR / "top50_genes.csv", index=False)

    row_order = clustered_order(heatmap_z, axis=0)
    col_order = clustered_order(heatmap_z, axis=1)
    plotted = heatmap_z.iloc[row_order, col_order]

    height = max(8, len(plotted) * 0.18)
    fig, ax = plt.subplots(figsize=(6.2, height))
    im = ax.imshow(plotted.values, cmap="RdBu_r", aspect="auto", vmin=-3, vmax=3)
    ax.set_xticks(range(plotted.shape[1]))
    ax.set_xticklabels(plotted.columns, rotation=35, ha="right")
    ax.set_yticks(range(plotted.shape[0]))
    ax.set_yticklabels(plotted.index, fontsize=6)
    ax.set_title(f"Top {len(plotted)} candidate genes, row Z-score")
    colorbar = fig.colorbar(im, ax=ax, shrink=0.45)
    colorbar.set_label("Row Z-score")
    fig.tight_layout()
    output = FIGURE_DIR / "fig07_top50_clustered_heatmap.png"
    fig.savefig(output, dpi=300, bbox_inches="tight")
    plt.close(fig)
    print(f"Saved: {output}")

if __name__ == "__main__":
    main()
