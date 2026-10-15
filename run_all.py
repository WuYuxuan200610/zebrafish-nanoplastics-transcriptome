from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parent
SCRIPTS = [
    "01_data_exploration.py",
    "02_preprocess_qc.py",
    "03_fold_change_analysis.py",
    "04_fold_change_distribution.py",
    "05_sample_qc.py",
    "06_ma_plot.py",
    "07_clustered_heatmap.py",
    "08_dose_response.py",
    "09_prepare_enrichment_input.py",
]

for script in SCRIPTS:
    path = ROOT / "scripts" / script
    print(f"\n===== Running {script} =====")
    subprocess.run([sys.executable, str(path)], cwd=ROOT, check=True)

print("\nAll analysis scripts completed successfully.")
