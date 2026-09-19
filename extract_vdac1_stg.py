import os
import numpy as np
import pandas as pd
import h5py

REGION = "STG"
H5AD = r"C:\sea_ad_download\abc_cache\expression_matrices\SEA-AD-Multiregion-10X\20260630\STG-10X-raw.h5ad"
OUT = r"C:\Users\jeyak\OneDrive\Documents\VDAC1_AD_Project\data\sea_ad"

def decode(x):
    return x.decode() if isinstance(x, bytes) else x

with h5py.File(H5AD, "r") as f:
    symbols = [decode(x) for x in f["var/gene_symbol"][:]]
    vdac1_idx = symbols.index("VDAC1")
    print(f"{REGION}: VDAC1 index = {vdac1_idx}")

    cells = [decode(x) for x in f["obs/cell_label"][:]]
    n_cells = len(cells)
    print(f"{REGION}: cells = {n_cells}")

    lg = f["obs/library_label"]
    codes = lg["codes"][:]
    cats = [decode(x) for x in lg["categories"][:]]
    libs = [cats[int(c)] for c in codes]

    X = f["X"]
    idx = X["indices"]
    dat = X["data"]
    iptr = X["indptr"][:]
    nnz = len(idx)
    print(f"{REGION}: nnz = {nnz}")

    pos_l, val_l = [], []
    for s in range(0, nnz, 100_000_000):
        e = min(s + 100_000_000, nnz)
        ch = idx[s:e]
        loc = np.where(ch == vdac1_idx)[0]
        if len(loc) > 0:
            dc = dat[s:e]
            pos_l.append(loc + s)
            val_l.append(dc[loc])
    pos = np.concatenate(pos_l)
    val = np.concatenate(val_l)
    print(f"{REGION}: VDAC1 matches = {len(pos)}")

    rows = np.searchsorted(iptr, pos, side="right") - 1
    v = np.zeros(n_cells, dtype=np.int32)
    v[rows] = val

    df = pd.DataFrame({"cell_label": cells,
                       "library_label": libs,
                       "vdac1_raw": v})
    out = os.path.join(OUT, f"sea_ad_{REGION.lower()}_vdac1_raw.csv")
    df.to_csv(out, index=False)
    print(f"{REGION}: saved {len(df)} cells, mean = {v.mean():.3f}")
