from pathlib import Path
from abc_atlas_access.abc_atlas_cache.abc_project_cache import AbcProjectCache

CACHE = Path(r"C:\sea_ad_download\abc_cache")
abc_cache = AbcProjectCache.from_cache_dir(CACHE)

# Inspect the internal cache object
cc = abc_cache.cache
print("Cache type:", type(cc))
print("Cache attributes:")
for a in dir(cc):
    if not a.startswith("_"):
        print("  ", a)

# Try to find the manifest
if hasattr(cc, "manifest"):
    m = cc.manifest
    print("\nManifest type:", type(m))
    print("Manifest methods:")
    for a in dir(m):
        if not a.startswith("_") and callable(getattr(m, a)):
            print("  ", a)

    # Try to get file attributes
    try:
        attrs = m.get_file_attributes(
            directory="SEA-AD-Multiregion-10X",
            file_name="MTG-10X/raw"
        )
        print("\nFile attributes:")
        for k, v in attrs.items():
            print(f"  {k}: {v}")
    except Exception as e:
        print("get_file_attributes failed:", e)
else:
    # Check abc_cache for manifest methods
    print("\nNo direct manifest attr. Checking abc_cache:")
    for a in dir(abc_cache):
        if "manifest" in a.lower() or "file" in a.lower():
            print("  ", a)
