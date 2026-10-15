import pandas as pd
from config import RAW_COUNT_CSV, TABLE_DIR

def main():
    df = pd.read_csv(RAW_COUNT_CSV)
    first_col = df.columns[0]
    if first_col != "GeneID":
        df = df.rename(columns={first_col: "GeneID"})

    report = []
    report.append(f"Raw file: {RAW_COUNT_CSV}")
    report.append(f"Shape: {df.shape[0]} genes x {df.shape[1] - 1} samples")
    report.append(f"Columns: {', '.join(df.columns)}")
    report.append("\nFirst rows:")
    report.append(df.head(10).to_string(index=False))
    report.append("\nDtypes:")
    report.append(df.dtypes.to_string())
    report.append("\nSummary of count columns:")
    report.append(df.drop(columns=["GeneID"]).describe().to_string())

    duplicated = df["GeneID"].duplicated().sum()
    report.append(f"\nDuplicated GeneID rows: {duplicated}")

    output = TABLE_DIR / "raw_data_summary.txt"
    output.write_text("\n".join(report), encoding="utf-8")
    print("\n".join(report))
    print(f"\nSaved: {output}")

if __name__ == "__main__":
    main()
