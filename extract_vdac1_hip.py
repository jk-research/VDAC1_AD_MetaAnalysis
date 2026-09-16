import os
import numpy as np
import pandas as pd
import h5py

HIP_PATH = r"C:\sea_ad_download\abc_cache\expression_matrices\SEA-AD-Multiregion-10X\20260630\HIP-10X-raw.h5ad"
OUT = r"C:\Users\jeyak\OneDrive\Documents\VDAC1_AD_Project\data\sea_ad"

def decode(x):
    return x.decode() if isinstance(x, bytes) else x

with h5py.File(HIP_PATH, "r") as f:
    # Gene symbols
    symbols = [decode(x) for x in f["var/gene_symbol"][:]]
    identifiers = [decode(x) for x in f["var/gene_identifier"][:]]
    print("Total genes:", len(symbols))

    vdac1_idx = symbols.index("VDAC1")
    print("VDAC1 gene index:", vdac1_idx)
    print("VDAC1 identifier:", identifiers[vdac1_idx])

    # Cells
    cell_labels = [decode(x) for x in f["obs/cell_label"][:]]
    n_cells = len(cell_labels)
    print("Cells:", n_cells)

    # library_label is categorical
    lib_grp = f["obs/library_label"]
    codes = lib_grp["codes"][:]
    cats = [decode(x) for x in lib_grp["categories"][:]]
    lib_labels = [cats[int(c)] for c in codes]
    print("Libraries:", len(cats))

    # CSR matrix
    X = f["X"]
    indices = X["indices"]
    data = X["data"]
    indptr = X["indptr"][:]
    nnz = len(indices)
    print("Sparse nnz:", nnz)

    # Chunked scan to find VDAC1 column positions
    CHUNK = 50_000_000
    match_positions = []
    for start in range(0, nnz, CHUNK):
        end = min(start + CHUNK, nnz)
        chunk = indices[start:end]
        local = np.where(chunk == vdac1_idx)[0] + start
        if len(local) > 0:
            match_positions.append(local)
    match_positions = np.concatenate(match_positions) if match_positions else np.array([], dtype=np.int64)
    print("VDAC1 matches:", len(match_positions))

    # Map positions to rows via indptr
    rows = np.searchsorted(indptr, match_positions, side="right") - 1

    # Read data at those positions
    vals = data[match_positions]

    # Dense per-cell array
    vdac1_vals = np.zeros(n_cells, dtype=np.int32)
    vdac1_vals[rows] = vals
    print("Nonzero cells:", int((vdac1_vals > 0).sum()))

    # Save
    df = pd.DataFrame({
        "cell_label": cell_labels,
        "library_label": lib_labels,
        "vdac1_raw": vdac1_vals
    })
    out_file = os.path.join(OUT, "sea_ad_hip_vdac1_raw.csv")
    df.to_csv(out_file, index=False)
    print("Saved", len(df), "cells to", out_file)
    print("Mean VDAC1:", round(df["vdac1_raw"].mean(), 3))
    print("Max VDAC1:", int(df["vdac1_raw"].max()))

print("=== Done ===")
