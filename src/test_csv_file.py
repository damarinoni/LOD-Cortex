import sys
from pathlib import Path
import pandas as pd

# Define ROOT_DIR dynamically (points to 'LOD')
ROOT_DIR = Path(__file__).resolve().parent.parent.parent

# Paths based on tree.txt structure
DATASET_DIR = ROOT_DIR / "Dataset"
CSV_PATH = DATASET_DIR / "dataset_AOMIC.csv"

# ✅ Function to Check CSV File
def check_csv():
    if not CSV_PATH.exists():
        print(f"❌ ERROR: CSV file not found at {CSV_PATH}")
        return

    # Load CSV
    try:
        df = pd.read_csv(CSV_PATH)
    except Exception as e:
        print(f"❌ ERROR: Failed to load CSV. {e}")
        return

    # Check required columns
    required_columns = {"T1Path", "GTPath", "set"}
    if not required_columns.issubset(df.columns):
        print(f"❌ ERROR: CSV is missing required columns. Found: {df.columns}")
        return

    # Check if paths exist
    missing_t1 = [p for p in df["T1Path"] if not Path(p).exists()]
    missing_gt = [p for p in df["GTPath"] if not Path(p).exists()]

    if missing_t1:
        print(f"⚠ WARNING: {len(missing_t1)} T1 files are missing!")
    if missing_gt:
        print(f"⚠ WARNING: {len(missing_gt)} GT files are missing!")

    # Check dataset splits
    train_count = (df["set"] == "train").sum()
    valid_count = (df["set"] == "valid").sum()
    test_count = (df["set"] == "test").sum()

    print("✅ CSV File Check Passed!")
    print(f"📂 Found {len(df)} entries (Train: {train_count}, Valid: {valid_count}, Test: {test_count})")

    # Show first few entries
    print("\n🔹 Example Entries:")
    print(df.head())

# Run the check
if __name__ == "__main__":
    check_csv()
