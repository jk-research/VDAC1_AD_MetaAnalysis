import os
import numpy as np
import pandas as pd
import h5py

MTG_PATH = r"C:\sea_ad_download\abc_cache\expression_matrices\SEA-AD-Multiregion-10X\20260630\MTG-10X-raw.h5ad"
OUT = r"C:\Users\jeyak\OneDrive\Documents\VDAC1_AD_Project\data\sea_ad"

def decode(x):
    return x.decode() if isinstance(x, bytes) else x

with h5py.File(MTG_PATH, "r") as f:
    symbols = [decode(x) for x in f["var/gene_symbol"][:]]
    vdac1_idx = symbols.index("VDAC1")
    print("VDAC1 gene index:", vdac1_idx)

    cell_labels = [decode(x) for x in f["obs/cell_label"][:]]
    n_cells = len(cell_labels)
    print("Cells:", n_cells)

    lib_grp = f["obs/library_label"]
    codes = lib_grp["codes"][:]
    cats = [decode(x) for x in lib_grp["categories"][:]]
    lib_labels = [cats[int(c)] for c in codes]

    X = f["X"]
    indices = X["indices"]
    data = X["data"]
    indptr = X["indptr"][:]
    nnz = len(indices)
    print("Sparse nnz:", nnz)

    CHUNK = 100_000_000
    match_positions = []
    match_vals = []
    for start in range(0, nnz, CHUNK):
        end = min(start + CHUNK, nnz)
        idx_chunk = indices[start:end]
        local = np.where(idx_chunk == vdac1_idx)[0]
        if len(local) > 0:
            data_chunk = data[start:end]
            match_positions.append(local + start)
            match_vals.append(data_chunk[local])
        print("  scanned", end, "/", nnz)
    match_positions = np.concatenate(match_positions)
    match_vals = np.concatenate(match_vals)
    print("VDAC1 matches:", len(match_positions))

    rows = np.searchsorted(indptr, match_positions, side="right") - 1

    vdac1_vals = np.zeros(n_cells, dtype=np.int32)
    vdac1_vals[rows] = match_vals

    df = pd.DataFrame({"cell_label": cell_labels,
                       "library_label": lib_labels,
                       "vdac1_raw": vdac1_vals})
    out_file = os.path.join(OUT, "sea_ad_mtg_vdac1_raw.csv")
    df.to_csv(out_file, index=False)
    print("Saved", len(df), "cells. Mean VDAC1:", round(df["vdac1_raw"].mean(), 3))
