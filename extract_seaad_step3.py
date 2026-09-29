import os
from pathlib import Path
from abc_atlas_access.abc_atlas_cache.abc_project_cache import AbcProjectCache

CACHE = Path(r"C:\sea_ad_download\abc_cache")
abc_cache = AbcProjectCache.from_cache_dir(CACHE)

# ---- List every metadata file in each SEA-AD directory ----
for directory in ["SEA-AD-Multiregion-10X", "SEA-AD-Multiregion-taxonomy"]:
    print("=" * 60)
    print("Directory:", directory)
    print("=" * 60)
    try:
        files = abc_cache.list_metadata_files(directory=directory)
        for f in files:
            print("  ", f)
    except Exception as e:
        print("  Error:", e)
    print()

# ---- Also list expression matrix files ----
for directory in ["SEA-AD-Multiregion-10X", "SEA-AD-CaH-10X"]:
    print("=" * 60)
    print("Expression matrix files in:", directory)
    print("=" * 60)
    try:
        files = abc_cache.list_expression_matrix_files(directory=directory)
        for f in files:
            print("  ", f)
    except Exception as e:
        print("  Error:", e)
    print()

# ---- Show the full donor metadata columns ----
import pandas as pd
donor_path = r"C:\Users\jeyak\OneDrive\Documents\VDAC1_AD_Project\data\sea_ad\sea_ad_donor_metadata.csv"
if os.path.exists(donor_path):
    d = pd.read_csv(donor_path)
    print("Donor metadata - ALL columns:")
    for c in d.columns:
        print("  ", c)
    print()
    print("First donor full row:")
    print(d.iloc[0].to_string())

print("=== Step 3 complete ===")
