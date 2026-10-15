import numpy as np
import pandas as pd
from config import (
    RAW_COUNT_CSV, CLEANED_CSV, TABLE_DIR,
    LOW_EXPRESSION_CUTOFF, MIN_SAMPLES_ABOVE_CUTOFF,
)

def load_count_matrix(path):
    df = pd.read_csv(path)
    first_col = df.columns[0]
    if first_col != "GeneID":
        df = df.rename(columns={first_col: "GeneID"})
    df = df.set_index("GeneID")
    count_cols = [c for c in df.columns if pd.api.types.is_numeric_dtype(df[c])]
    df = df[count_cols].apply(pd.to_numeric, errors="coerce").fillna(0)
    if df.index.duplicated().any():
        df = df.groupby(level=0).sum()
    return df

def main():
    df = load_count_matrix(RAW_COUNT_CSV)
    keep = (df > LOW_EXPRESSION_CUTOFF).sum(axis=1) >= MIN_SAMPLES_ABOVE_CUTOFF
    df_filtered = df.loc[keep].copy()

    df_filtered.to_csv(CLEANED_CSV)

    summary_rows = []
    for sample in df.columns:
        values = df[sample]
        summary_rows.append({
            "sample": sample,
            "total_counts": int(values.sum()),
            "genes_with_any_expression": int((values > 0).sum()),
            f"genes_gt_{LOW_EXPRESSION_CUTOFF}": int((values > LOW_EXPRESSION_CUTOFF).sum()),
            "median": float(values.median()),
            "q1": float(values.quantile(0.25)),
            "q3": float(values.quantile(0.75)),
        })
    summary = pd.DataFrame(summary_rows)
    summary.to_csv(TABLE_DIR / "sample_summary.csv", index=False)

    print(f"Input genes: {len(df)}")
    print(f"Filter: expression > {LOW_EXPRESSION_CUTOFF} in at least {MIN_SAMPLES_ABOVE_CUTOFF} samples")
    print(f"Retained genes: {len(df_filtered)}")
    print(f"Saved cleaned matrix: {CLEANED_CSV}")
    print(f"Saved sample summary: {TABLE_DIR / 'sample_summary.csv'}")

if __name__ == "__main__":
    main()
