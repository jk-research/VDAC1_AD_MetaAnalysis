"""download_seaad.py - download to local folder (bypasses OneDrive)."""
import os
import boto3
from botocore import UNSIGNED
from botocore.config import Config
from boto3.s3.transfer import TransferConfig

LOCAL = r"C:\sea_ad_download"
os.makedirs(LOCAL, exist_ok=True)

s3 = boto3.client("s3", config=Config(signature_version=UNSIGNED))
bucket = "sea-ad-single-cell-profiling"
target_key = "MTG/RNAseq/Reference_MTG_RNAseq_final-nuclei.2022-06-07.h5ad"
local_path = os.path.join(LOCAL, "SEAAD_MTG_RNAseq.h5ad")

if os.path.exists(local_path):
    size_gb = os.path.getsize(local_path) / 1e9
    print("Already downloaded: " + str(round(size_gb, 1)) + " GB")
else:
    print("Downloading to " + local_path)
    print("Expected size: ~6.4 GB")
    print("Watch progress in a separate PowerShell window:")
    print("  Get-ChildItem C:\\sea_ad_download -File | Select Name, Length")
    print("")
    cfg = TransferConfig(multipart_threshold=100*1024*1024,
                         multipart_chunksize=100*1024*1024,
                         max_concurrency=4)
    s3.download_file(bucket, target_key, local_path, Config=cfg)
    size_gb = os.path.getsize(local_path) / 1e9
    print("")
    print("Saved: " + local_path + "  (" + str(round(size_gb, 1)) + " GB)")

print("=== Done ===")
