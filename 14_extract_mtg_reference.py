import os
import numpy as np
import pandas as pd
import h5py

MTG = r"C:\sea_ad_download\abc_cache\expression_matrices\SEA-AD-Multiregion-10X\20260630\MTG-10X-raw.h5ad"
OUT = r"C:\Users\jeyak\OneDrive\Documents\VDAC1_AD_Project\data\sea_ad"

def decode(x):
    return x.decode() if isinstance(x, bytes) else x

with h5py.File(MTG, "r") as f:
    genes = [decode(x) for x in f["var/gene_symbol"][:]]
    cells = [decode(x) for x in f["obs/cell_label"][:]]
    n_cells = len(cells)
    n_genes = len(genes)
    print(f"Cells: {n_cells}, Genes: {n_genes}")

    # Cell type mapping
    c2c = pd.read_csv(os.path.join(OUT, "sea_ad_cell_to_cluster.csv")).drop_duplicates("cell_label")
    cta = pd.read_csv(os.path.join(OUT, "sea_ad_cluster_to_annotation.csv"))
    cta = cta[cta["cluster_annotation_term_set_name"] == "Subclass"].drop_duplicates("cluster_alias")
    c2c["cluster_alias"] = c2c["cluster_alias"].astype(str)
    cta["cluster_alias"] = cta["cluster_alias"].astype(str)
    cell_meta = c2c.merge(cta[["cluster_alias", "cluster_annotation_term_name"]],
                           on="cluster_alias", how="left")
    cell_to_type = dict(zip(cell_meta["cell_label"], cell_meta["cluster_annotation_term_name"]))
    type_labels = np.array([cell_to_type.get(c, "Unknown") for c in cells])

    unique_types = sorted([t for t in set(type_labels) if t != "Unknown"])
    print(f"Cell types: {len(unique_types)}")
    type_index = {ct: i for i, ct in enumerate(unique_types)}
    type_to_idx = np.array([type_index.get(t, -1) for t in type_labels])

    sums = np.zeros((len(unique_types), n_genes), dtype=np.float32)
    counts = np.zeros(len(unique_types), dtype=np.int64)

    print("\nReading indptr...")
    indptr = f["X/indptr"][:]

    BLOCK = 5000
    n_blocks = (n_cells + BLOCK - 1) // BLOCK
    print(f"Processing {n_blocks} blocks of {BLOCK} cells...")

    dset_indices = f["X/indices"]
    dset_data = f["X/data"]

    for b in range(n_blocks):
        start_cell = b * BLOCK
        end_cell = min(start_cell + BLOCK, n_cells)
        row_start = int(indptr[start_cell])
        row_end = int(indptr[end_cell])
        if row_end == row_start:
            continue

        # Read just this block
        idx_block = np.asarray(dset_indices[row_start:row_end], dtype=np.int32)
        dat_block = np.asarray(dset_data[row_start:row_end], dtype=np.float32)
        block_indptr = (indptr[start_cell:end_cell + 1] - row_start).astype(np.int64)

        # Accumulate per cell using bincount
        for local_i in range(len(block_indptr) - 1):
            a = int(block_indptr[local_i])
            e = int(block_indptr[local_i + 1])
            if e > a:
                ct = type_to_idx[start_cell + local_i]
                if ct < 0:
                    continue
                sums[ct] += np.bincount(idx_block[a:e], weights=dat_block[a:e],
                                         minlength=n_genes).astype(np.float32)
                counts[ct] += 1

        if (b + 1) % 25 == 0 or (b + 1) == n_blocks:
            print(f"  Block {b+1}/{n_blocks}")

    print("\nComputing means...")
    means = np.zeros_like(sums)
    for i in range(len(unique_types)):
        if counts[i] > 0:
            means[i] = sums[i] / counts[i]

    ref_df = pd.DataFrame(means, index=unique_types, columns=genes)
    out_file = os.path.join(OUT, "sea_ad_mtg_reference_matrix.csv")
    ref_df.to_csv(out_file)
    print(f"Saved: {ref_df.shape}")
    print(f"File size: {os.path.getsize(out_file)/1e6:.1f} MB")
