import os
import numpy as np
import pandas as pd
import anndata as ad
from pathlib import Path
from abc_atlas_access.abc_atlas_cache.abc_project_cache import AbcProjectCache

CACHE = Path(r"C:\sea_ad_download\abc_cache")
abc_cache = AbcProjectCache.from_cache_dir(CACHE)

OUT = r"C:\Users\jeyak\OneDrive\Documents\VDAC1_AD_Project\data\sea_ad"
os.makedirs(OUT, exist_ok=True)

# ---- Download MTG raw expression matrix ----
print("Downloading MTG-10X/raw (this is the big one, ~2-4 GB)...")
mtg_path = abc_cache.get_data_path(
    directory="SEA-AD-Multiregion-10X",
    file_name="MTG-10X/raw"
)
print("Saved to:", mtg_path)
print("File size:", round(os.path.getsize(mtg_path) / 1e9, 2), "GB")

# ---- Load as AnnData ----
print("\nLoading MTG matrix...")
mtg = ad.read_h5ad(mtg_path)
print("MTG shape:", mtg.shape)
print("First 10 var_names:", list(mtg.var_names)[:10])
print("First 3 obs cols:", list(mtg.obs.columns)[:10])

# ---- Find VDAC1 ----
print("\nSearching for VDAC1...")
candidates = [g for g in mtg.var_names if "VDAC1" in str(g).upper()
              or "ENSG00000183055" in str(g)]
print("Candidates:", candidates[:5])

if not candidates:
    print("VDAC1 not found. First 20 var_names:")
    print(list(mtg.var_names)[:20])
else:
    gene = candidates[0]
    print("Using:", gene)
    vals = mtg[:, gene].X
    if hasattr(vals, "toarray"):
        vals = vals.toarray().flatten()
    else:
        vals = np.asarray(vals).flatten()

    df = pd.DataFrame({
        "cell_label": mtg.obs_names,
        "vdac1_raw": vals
    })
    out_file = os.path.join(OUT, "sea_ad_mtg_vdac1_raw.csv")
    df.to_csv(out_file, index=False)
    print("Saved VDAC1 for", len(df), "cells to", out_file)

print("\n=== Done ===")
