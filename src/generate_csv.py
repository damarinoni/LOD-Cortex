import os
import pandas as pd
from pathlib import Path

# Set ROOT_DIR dynamically (now pointing to '/LOD' instead of 'Cortex')
ROOT_DIR = Path(__file__).resolve().parent.parent.parent  # Moves up two levels to get `/LOD`

# Dataset Paths
DATASET_DIR = ROOT_DIR / "Dataset"
T1_DIR = DATASET_DIR / "AOMIC_T1w"
GT_DIR = DATASET_DIR / "AOMIC_GT"
OUTPUT_CSV = DATASET_DIR / "dataset_AOMIC.csv"

# Ensure absolute paths
T1_DIR = T1_DIR.resolve()
GT_DIR = GT_DIR.resolve()

# List all T1w MRI files
t1_files = sorted([f for f in os.listdir(T1_DIR) if f.endswith(".nii.gz")])

# List all GT subfolders
gt_folders = sorted([f for f in os.listdir(GT_DIR) if os.path.isdir(os.path.join(GT_DIR, f))])

# Check that filenames match between T1w and GT
t1_filenames = {os.path.splitext(os.path.splitext(f)[0])[0] for f in t1_files}  # Remove .nii.gz
gt_filenames = set(gt_folders)  # GT folder names should match

# Ensure matching subjects
if t1_filenames != gt_filenames:
    print("⚠ WARNING: Some T1 files do not have matching GT folders!")
    unmatched_t1 = t1_filenames - gt_filenames
    unmatched_gt = gt_filenames - t1_filenames
    print(f"Unmatched T1 files: {unmatched_t1}")
    print(f"Unmatched GT folders: {unmatched_gt}")
else:
    print("✅ All T1 files have matching GT folders!")

# Split dataset into train, validation, and test sets
num_total = len(t1_files)
num_train = int(0.7 * num_total)  # 70% train
num_valid = int(0.15 * num_total)  # 15% validation
num_test = num_total - num_train - num_valid  # 15% test

# Assign dataset split
dataset_split = (["train"] * num_train) + (["valid"] * num_valid) + (["test"] * num_test)

# Create DataFrame
data = []
for i, t1_filename in enumerate(t1_files):
    subject_id = os.path.splitext(os.path.splitext(t1_filename)[0])[0]  # Remove .nii.gz
    t1_path = T1_DIR / t1_filename
    gt_path = GT_DIR / subject_id / "FS_aa_LODcortex_only_NS.nii.gz"  # GT file inside the subfolder

    # Check if GT file exists before adding
    if gt_path.exists():
        data.append([str(t1_path), str(gt_path), dataset_split[i]])
    else:
        print(f"⚠ WARNING: Missing GT file for {subject_id} (expected at {gt_path})")

df = pd.DataFrame(data, columns=["T1Path", "GTPath", "set"])

# Save CSV
df.to_csv(OUTPUT_CSV, index=False)
print(f"✅ CSV file saved at: {OUTPUT_CSV}")
