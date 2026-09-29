import os
import anndata as ad

HIP_PATH = r"C:\sea_ad_download\abc_cache\expression_matrices\SEA-AD-Multiregion-10X\20260630\HIP-10X-raw.h5ad"

hip = ad.read_h5ad(HIP_PATH, backed="r")
print("Shape:", hip.shape)

# Search for VDAC1 by multiple methods
print("\n--- Searching for VDAC1 ---")
print("Full match ENSG00000183055:", "ENSG00000183055" in hip.var_names)
print("Partial match 183055:", [g for g in hip.var_names if "183055" in str(g)])
print("Any VDAC:", [g for g in hip.var_names if "VDAC" in str(g).upper()])

# Check var columns for gene symbols
print("\nvar columns:", list(hip.var.columns))
if "feature_name" in hip.var.columns:
    print("\nSearch feature_name for VDAC1:")
    hits = hip.var[hip.var["feature_name"].str.contains("VDAC1", case=False, na=False)]
    print(hits)

# Show all obs columns
print("\nAll obs columns:")
for c in hip.obs.columns:
    print(" ", c)

# Sample of obs to see how donor can be linked
print("\nFirst 3 rows of obs:")
print(hip.obs.head(3).to_string())

hip.file.close()
