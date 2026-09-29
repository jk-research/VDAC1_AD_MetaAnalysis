from pathlib import Path
from abc_atlas_access.abc_atlas_cache.abc_project_cache import AbcProjectCache

CACHE = Path(r"C:\sea_ad_download\abc_cache")
abc_cache = AbcProjectCache.from_cache_dir(CACHE)

methods = [m for m in dir(abc_cache) if not m.startswith("_") and callable(getattr(abc_cache, m))]
print("Cache methods:")
for m in methods:
    print("  ", m)

print()
print("Attributes:")
attrs = [m for m in dir(abc_cache) if not m.startswith("_") and not callable(getattr(abc_cache, m))]
for a in attrs:
    print("  ", a)
