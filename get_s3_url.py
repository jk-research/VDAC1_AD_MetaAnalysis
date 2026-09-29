from pathlib import Path
from abc_atlas_access.abc_atlas_cache.abc_project_cache import AbcProjectCache

CACHE = Path(r"C:\sea_ad_download\abc_cache")
abc_cache = AbcProjectCache.from_cache_dir(CACHE)

attrs = abc_cache.cache.manifest.get_file_attributes(
    directory="SEA-AD-Multiregion-10X",
    file_name="MTG-10X/raw"
)
print("All attributes:")
for k, v in attrs.items():
    print(f"  {k}: {v}")
