import os
from pathlib import Path
from abc_atlas_access.abc_atlas_cache.abc_project_cache import AbcProjectCache

CACHE = Path(r"C:\sea_ad_download\abc_cache")
CACHE.mkdir(parents=True, exist_ok=True)

abc_cache = AbcProjectCache.from_cache_dir(CACHE)
print("Manifest:", abc_cache.current_manifest)

print("Directories:")
for d in abc_cache.list_directories:
    print(" ", d)

print("\nDownloading cell metadata...")
cell_meta = abc_cache.get_metadata_dataframe(
    directory="SEA-AD-Multiregion-10X",
    file_name="cell_metadata"
)
print("Shape:", cell_meta.shape)
print("Columns:", list(cell_meta.columns))

OUT = r"C:\Users\jeyak\OneDrive\Documents\VDAC1_AD_Project\data\sea_ad"
os.makedirs(OUT, exist_ok=True)
cell_meta.to_csv(os.path.join(OUT, "sea_ad_cell_metadata.csv"), index=False)
print("Saved cell metadata")
