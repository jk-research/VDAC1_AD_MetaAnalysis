import os
from pathlib import Path
from abc_atlas_access.abc_atlas_cache.abc_project_cache import AbcProjectCache

CACHE = Path(r"C:\sea_ad_download\abc_cache")
abc_cache = AbcProjectCache.from_cache_dir(CACHE)

OUT = r"C:\Users\jeyak\OneDrive\Documents\VDAC1_AD_Project\data\sea_ad"
os.makedirs(OUT, exist_ok=True)

# ---- 1. Donor metadata (diagnosis, Braak, age, sex) ----
print("Downloading donor metadata...")
donor = abc_cache.get_metadata_dataframe(
    directory="SEA-AD-Multiregion-10X",
    file_name="donor"
)
print("Shape:", donor.shape)
print("Columns:", list(donor.columns))
print(donor.head())
donor.to_csv(os.path.join(OUT, "sea_ad_donor_metadata.csv"), index=False)

# ---- 2. Cell-type taxonomy ----
print("\nDownloading cell-type taxonomy...")
tax = abc_cache.get_metadata_dataframe(
    directory="SEA-AD-Multiregion-taxonomy",
    file_name="taxonomy"
)
print("Shape:", tax.shape)
print("Columns:", list(tax.columns))
print(tax.head())
tax.to_csv(os.path.join(OUT, "sea_ad_taxonomy.csv"), index=False)

# ---- 3. What else is available for us to use ----
print("\nFiles available in SEA-AD-Multiregion-10X:")
for f in abc_cache.list_metadata_files(directory="SEA-AD-Multiregion-10X"):
    print("  ", f)

print("\nFiles available in SEA-AD-Multiregion-taxonomy:")
for f in abc_cache.list_metadata_files(directory="SEA-AD-Multiregion-taxonomy"):
    print("  ", f)

print("\n=== Step 2 complete ===")
