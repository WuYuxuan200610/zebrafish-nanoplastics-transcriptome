import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from scipy.spatial.distance import pdist, squareform
from config import CLEANED_CSV, FIGURE_DIR, TABLE_DIR, SAMPLE_COLUMNS, SAMPLE_LABELS

def correlation_heatmap(df_log, output):
    corr = df_log.corr()
    corr.to_csv(TABLE_DIR / "sample_correlation.csv")
    fig, ax = plt.subplots(figsize=(5.2, 4.5))
    im = ax.imshow(corr.values, cmap="RdYlGn", vmin=max(0, corr.values.min() - 0.02), vmax=1)
    ax.set_xticks(range(len(corr.columns)))
    ax.set_yticks(range(len(corr.columns)))
    ax.set_xticklabels(corr.columns, rotation=35, ha="right")
    ax.set_yticklabels(corr.columns)
    ax.set_title("Sample correlation, log2(count + 1)")
    for i in range(corr.shape[0]):
        for j in range(corr.shape[1]):
            ax.text(j, i, f"{corr.iloc[i, j]:.3f}", ha="center", va="center", fontsize=9)
    fig.colorbar(im, ax=ax, shrink=0.8)
    fig.tight_layout()
    fig.savefig(output, dpi=300, bbox_inches="tight")
    plt.close(fig)

def expression_distribution(df_log, output):
    fig, ax = plt.subplots(figsize=(6.2, 4.5))
    data = [df_log[s] for s in SAMPLE_COLUMNS]
    box = ax.boxplot(data, tick_labels=SAMPLE_COLUMNS, patch_artist=True, showfliers=False)
    for patch in box["boxes"]:
        patch.set_facecolor("#c6dbef")
        patch.set_alpha(0.8)
    ax.set_ylabel("log2(count + 1)")
    ax.set_title("Gene expression distribution by sample")
    ax.grid(axis="y", alpha=0.25)
    fig.tight_layout()
    fig.savefig(output, dpi=300, bbox_inches="tight")
    plt.close(fig)

def pca_plot(df_log, output):
    X = df_log[SAMPLE_COLUMNS].T
    X_scaled = StandardScaler(with_mean=True, with_std=False).fit_transform(X)
    n_components = min(2, X_scaled.shape[0], X_scaled.shape[1])
    pca = PCA(n_components=n_components)
    scores = pca.fit_transform(X_scaled)
    variance = pca.explained_variance_ratio_

    fig, ax = plt.subplots(figsize=(5.6, 4.8))
    ax.scatter(scores[:, 0], scores[:, 1], s=70, c="#4292c6", edgecolor="white", linewidth=1)
    for label, (x, y) in zip(X.index, scores):
        ax.annotate(label, (x, y), xytext=(5, 5), textcoords="offset points")
    ax.axhline(0, color="black", linewidth=0.6, alpha=0.4)
    ax.axvline(0, color="black", linewidth=0.6, alpha=0.4)
    ax.set_xlabel(f"PC1 ({variance[0] * 100:.1f}% variance)" if len(variance) > 0 else "PC1")
    ax.set_ylabel(f"PC2 ({variance[1] * 100:.1f}% variance)" if len(variance) > 1 else "PC2")
    ax.set_title("PCA of samples, centered log-expression")
    ax.grid(alpha=0.25)
    fig.tight_layout()
    fig.savefig(output, dpi=300, bbox_inches="tight")
    plt.close(fig)

def sample_distance(df_log, output):
    X = df_log[SAMPLE_COLUMNS].T
    X_scaled = StandardScaler(with_mean=True, with_std=False).fit_transform(X)
    distances = squareform(pdist(X_scaled, metric="euclidean"))
    dist_df = pd.DataFrame(distances, index=X.index, columns=X.index)
    dist_df.to_csv(TABLE_DIR / "sample_distance_euclidean.csv")

    fig, ax = plt.subplots(figsize=(5.2, 4.5))
    im = ax.imshow(dist_df.values, cmap="magma_r")
    ax.set_xticks(range(len(dist_df.columns)))
    ax.set_yticks(range(len(dist_df.index)))
    ax.set_xticklabels(dist_df.columns, rotation=35, ha="right")
    ax.set_yticklabels(dist_df.index)
    ax.set_title("Sample distance, Euclidean")
    for i in range(dist_df.shape[0]):
        for j in range(dist_df.shape[1]):
            ax.text(j, i, f"{dist_df.iloc[i, j]:.1f}", ha="center", va="center",
                    color="white" if dist_df.iloc[i, j] > np.nanmax(dist_df.values) * 0.55 else "black",
                    fontsize=9)
    fig.colorbar(im, ax=ax, shrink=0.8)
    fig.tight_layout()
    fig.savefig(output, dpi=300, bbox_inches="tight")
    plt.close(fig)

def main():
    df = pd.read_csv(CLEANED_CSV, index_col="GeneID")
    df_log = np.log2(df + 1)
    correlation_heatmap(df_log, FIGURE_DIR / "fig01_sample_correlation.png")
    expression_distribution(df_log, FIGURE_DIR / "fig02_expression_distribution.png")
    pca_plot(df_log, FIGURE_DIR / "fig03_pca.png")
    sample_distance(df_log, FIGURE_DIR / "fig04_sample_distance.png")
    print(f"Saved QC figures to: {FIGURE_DIR}")

if __name__ == "__main__":
    main()
