import h5py

HIP_PATH = r"C:\sea_ad_download\abc_cache\expression_matrices\SEA-AD-Multiregion-10X\20260630\HIP-10X-raw.h5ad"

def show(name, obj, indent=0):
    pad = "  " * indent
    if isinstance(obj, h5py.Dataset):
        print(f"{pad}{name}  [Dataset shape={obj.shape} dtype={obj.dtype}]")
    else:
        print(f"{pad}{name}  [Group]")

with h5py.File(HIP_PATH, "r") as f:
    print("Top-level keys:", list(f.keys()))
    print()
    # var group structure
    print("var/ keys:", list(f["var"].keys()))
    print("var attrs:", dict(f["var"].attrs))
    print()
    # obs group structure
    print("obs/ keys:", list(f["obs"].keys())[:20])
    print()
    # X group structure
    print("X type:", type(f["X"]))
    if isinstance(f["X"], h5py.Group):
        print("X/ keys:", list(f["X"].keys()))
        print("X attrs:", dict(f["X"].attrs))
    print()
    # full tree (limited depth)
    print("--- Full tree ---")
    def walk(name, obj, depth=0, max_depth=3):
        if depth > max_depth:
            return
        show(name, obj, depth)
        if isinstance(obj, h5py.Group):
            for k in obj.keys():
                walk(k, obj[k], depth + 1, max_depth)
    for k in f.keys():
        walk(k, f[k], 0, 2)
