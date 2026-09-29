import os
from pathlib import Path
from abc_atlas_access.abc_atlas_cache.abc_project_cache import AbcProjectCache

CACHE = Path(r"C:\sea_ad_download\abc_cache")
abc_cache = AbcProjectCache.from_cache_dir(CACHE)

OUT = r"C:\Users\jeyak\OneDrive\Documents\VDAC1_AD_Project\data\sea_ad"
os.makedirs(OUT, exist_ok=True)

# ---- 1. Disease metadata (diagnosis, Braak, CERAD) ----
print("Downloading disease metadata...")
disease = abc_cache.get_metadata_dataframe(
    directory="SEA-AD-Multiregion-10X",
    file_name="disease"
)
print("Shape:", disease.shape)
print("Columns:", list(disease.columns))
print(disease.head())
disease.to_csv(os.path.join(OUT, "sea_ad_disease_metadata.csv"), index=False)

# ---- 2. Cell-to-cluster mapping ----
print("\nDownloading cell-to-cluster mapping...")
c2c = abc_cache.get_metadata_dataframe(
    directory="SEA-AD-Multiregion-taxonomy",
    file_name="cell_to_cluster_membership"
)
print("Shape:", c2c.shape)
print("Columns:", list(c2c.columns))
print(c2c.head())
c2c.to_csv(os.path.join(OUT, "sea_ad_cell_to_cluster.csv"), index=False)

# ---- 3. Cluster definitions (cell type names) ----
print("\nDownloading cluster definitions...")
cl = abc_cache.get_metadata_dataframe(
    directory="SEA-AD-Multiregion-taxonomy",
    file_name="cluster"
)
print("Shape:", cl.shape)
print("Columns:", list(cl.columns))
print(cl.head(20))
cl.to_csv(os.path.join(OUT, "sea_ad_cluster_definitions.csv"), index=False)

# ---- 4. NOW download the MTG expression matrix (only MTG, not all regions) ----
print("\nDownloading MTG-10X/raw expression matrix...")
print("(this is the big file — expect 2-4 GB, ~15-20 min)")
mtg = abc_cache.get_expression_matrix(
    directory="SEA-AD-Multiregion-10X",
    file_name="MTG-10X/raw"
)
print("MTG matrix shape:", mtg.shape)

# ---- 5. Extract VDAC1 ----
print("\nExtracting VDAC1...")
gene_col = "VDAC1" if "VDAC1" in mtg.var_names else None
if gene_col is None:
    # try ENSG ID
    matches = [g for g in mtg.var_names if "ENSG00000183055" in g]
    gene_col = matches[0] if matches else None

if gene_col:
    print("VDAC1 identifier:", gene_col)
    # get raw counts as dense array for VDAC1 only
    import numpy as np
    vdac1_idx = list(mtg.var_names).index(gene_col)
    vdac1_vals = mtg.X[:, vdac1_idx]
    if hasattr(vdac1_vals, "toarray"):
        vdac1_vals = vdac1_vals.toarray().flatten()
    else:
        vdac1_vals = np.asarray(vdac1_vals).flatten()

    import pandas as pd
    df = pd.DataFrame({
        "cell_label": mtg.obs_names,
        "vdac1_raw": vdac1_vals
    })
    df.to_csv(os.path.join(OUT, "sea_ad_mtg_vdac1_raw.csv"), index=False)
    print("Saved VDAC1 values for", len(df), "cells")
else:
    print("VDAC1 not found in var_names")
    print("First 10 var_names:", list(mtg.var_names)[:10])

print("\n=== Step 4 complete ===")
