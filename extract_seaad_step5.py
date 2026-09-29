import os
import numpy as np
import pandas as pd
from pathlib import Path
from abc_atlas_access.abc_atlas_cache.abc_project_cache import AbcProjectCache

CACHE = Path(r"C:\sea_ad_download\abc_cache")
abc_cache = AbcProjectCache.from_cache_dir(CACHE)

OUT = r"C:\Users\jeyak\OneDrive\Documents\VDAC1_AD_Project\data\sea_ad"
os.makedirs(OUT, exist_ok=True)

# ---- 1. Cell type names (cluster annotations) ----
print("Downloading cluster annotation terms...")
cat_term = abc_cache.get_metadata_dataframe(
    directory="SEA-AD-Multiregion-taxonomy",
    file_name="cluster_annotation_term"
)
print("Shape:", cat_term.shape)
print("Columns:", list(cat_term.columns))
print(cat_term.head(10))
cat_term.to_csv(os.path.join(OUT, "sea_ad_cluster_annotation_term.csv"), index=False)

print("\nDownloading cluster_to_cluster_annotation_membership...")
ctm = abc_cache.get_metadata_dataframe(
    directory="SEA-AD-Multiregion-taxonomy",
    file_name="cluster_to_cluster_annotation_membership"
)
print("Shape:", ctm.shape)
print("Columns:", list(ctm.columns))
print(ctm.head(10))
ctm.to_csv(os.path.join(OUT, "sea_ad_cluster_to_annotation.csv"), index=False)

# ---- 2. Load MTG raw expression matrix ----
print("\nLoading MTG-10X/raw expression matrix...")
print("(downloading ~2-4 GB, ~15 min at current speed)")
mtg_dict = abc_cache.get_directory_expression_matrices(
    directory="SEA-AD-Multiregion-10X",
    expression_matrix="MTG-10X/raw"
)
print("Returned type:", type(mtg_dict))
if isinstance(mtg_dict, dict):
    print("Keys:", list(mtg_dict.keys()))
    mtg = list(mtg_dict.values())[0]
else:
    mtg = mtg_dict
print("MTG shape:", mtg.shape)

# ---- 3. Find VDAC1 ----
print("\nSearching for VDAC1...")
candidates = [g for g in mtg.var_names if "VDAC1" in str(g).upper() or "ENSG00000183055" in str(g)]
print("Candidates:", candidates[:5])
gene_name = candidates[0] if candidates else None

if gene_name:
    print("Using:", gene_name)
    vdac1_vals = mtg[:, gene_name].X
    if hasattr(vdac1_vals, "toarray"):
        vdac1_vals = vdac1_vals.toarray().flatten()
    else:
        vdac1_vals = np.asarray(vdac1_vals).flatten()
    df = pd.DataFrame({"cell_label": mtg.obs_names, "vdac1_raw": vdac1_vals})
    df.to_csv(os.path.join(OUT, "sea_ad_mtg_vdac1_raw.csv"), index=False)
    print("Saved VDAC1 for", len(df), "cells")
else:
    print("VDAC1 not found. Showing first 20 var names:")
    print(list(mtg.var_names)[:20])

print("\n=== Step 5 complete ===")
