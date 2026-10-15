from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = BASE_DIR / "data"
RAW_COUNT_CSV = DATA_DIR / "raw" / "gene_expression_matrix.csv"
CLEANED_CSV = DATA_DIR / "processed" / "expression_cleaned.csv"

RESULTS_DIR = BASE_DIR / "results"
FIGURE_DIR = RESULTS_DIR / "figures"
TABLE_DIR = RESULTS_DIR / "tables"
ENRICHMENT_DIR = TABLE_DIR / "enrichment"

for path in [CLEANED_CSV.parent, FIGURE_DIR, TABLE_DIR, ENRICHMENT_DIR]:
    path.mkdir(parents=True, exist_ok=True)

SAMPLE_COLUMNS = ["wt", "low", "High"]
SAMPLE_LABELS = {
    "wt": "WT control",
    "low": "0.1 mg/L PS-NPs",
    "High": "10 mg/L PS-NPs",
}
LOG2FC_THRESHOLD = 1.0
MIN_MAX_RAW_EXPRESSION = 50
LOW_EXPRESSION_CUTOFF = 10
MIN_SAMPLES_ABOVE_CUTOFF = 2
TOP_N_HEATMAP = 50
TOP_N_ENRICHMENT = 50
