import inspect
from pathlib import Path
from abc_atlas_access.abc_atlas_cache.abc_project_cache import AbcProjectCache

CACHE = Path(r"C:\sea_ad_download\abc_cache")
abc_cache = AbcProjectCache.from_cache_dir(CACHE)

# --- Show the exact signature ---
print("Signature of get_directory_expression_matrices:")
print(inspect.signature(abc_cache.get_directory_expression_matrices))
print()
print("Docstring:")
print(inspect.getdoc(abc_cache.get_directory_expression_matrices))
print()
print("Signature of get_data_path:")
print(inspect.signature(abc_cache.get_data_path))
print()
print("Docstring of get_data_path:")
print(inspect.getdoc(abc_cache.get_data_path))
