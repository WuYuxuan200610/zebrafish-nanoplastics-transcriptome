import numpy as np
import pandas as pd
from config import (
    CLEANED_CSV, TABLE_DIR,
    LOG2FC_THRESHOLD, MIN_MAX_RAW_EXPRESSION,
)

def main():
    df = pd.read_csv(CLEANED_CSV, index_col="GeneID")
    df_log = np.log2(df + 1)

    results = pd.DataFrame({
        "High_log2FC": df_log["High"] - df_log["wt"],
        "low_log2FC": df_log["low"] - df_log["wt"],
        "High_raw": df["High"],
        "low_raw": df["low"],
        "wt_raw": df["wt"],
    })
    results.index.name = "GeneID"

    high_candidate = results[
        (results["High_log2FC"].abs() > LOG2FC_THRESHOLD)
        & (results[["High_raw", "wt_raw"]].max(axis=1) > MIN_MAX_RAW_EXPRESSION)
    ].copy()
    low_candidate = results[
        (results["low_log2FC"].abs() > LOG2FC_THRESHOLD)
        & (results[["low_raw", "wt_raw"]].max(axis=1) > MIN_MAX_RAW_EXPRESSION)
    ].copy()

    high_candidate.to_csv(TABLE_DIR / "high_vs_wt_candidate_genes.csv")
    low_candidate.to_csv(TABLE_DIR / "low_vs_wt_candidate_genes.csv")
    results.to_csv(TABLE_DIR / "all_genes_log2fc.csv")

    print(f"Input genes: {len(results)}")
    print(f"Candidate genes, High vs WT: {len(high_candidate)}")
    print(f"  Up: {(high_candidate['High_log2FC'] > LOG2FC_THRESHOLD).sum()}")
    print(f"  Down: {(high_candidate['High_log2FC'] < -LOG2FC_THRESHOLD).sum()}")
    print(f"Candidate genes, low vs WT: {len(low_candidate)}")
    print(f"  Up: {(low_candidate['low_log2FC'] > LOG2FC_THRESHOLD).sum()}")
    print(f"  Down: {(low_candidate['low_log2FC'] < -LOG2FC_THRESHOLD).sum()}")
    print(f"Saved tables to: {TABLE_DIR}")

if __name__ == "__main__":
    main()
