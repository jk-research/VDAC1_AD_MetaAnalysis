from pathlib import Path
from abc_atlas_access.abc_atlas_cache.abc_project_cache import AbcProjectCache

CACHE = Path(r"C:\sea_ad_download\abc_cache")
abc_cache = AbcProjectCache.from_cache_dir(CACHE)
cc = abc_cache.cache

# Print bucket and construct the S3 URL
bucket = cc.bucket_name
print("Bucket:", bucket)

# The file path within the bucket
file_key = "expression_matrices/SEA-AD-Multiregion-10X/20260630/MTG-10X-raw.h5ad"
url = f"https://{bucket}.s3.amazonaws.com/{file_key}"
print("\nDirect S3 URL:")
print(url)

# Verify with a HEAD request
import boto3
from botocore import UNSIGNED
from botocore.config import Config
s3 = boto3.client("s3", config=Config(signature_version=UNSIGNED))

try:
    resp = s3.head_object(Bucket=bucket, Key=file_key)
    size_gb = resp["ContentLength"] / 1e9
    print(f"\nFile exists. Size: {size_gb:.2f} GB")
    print("Content-Type:", resp.get("ContentType"))
except Exception as e:
    print(f"\nFailed: {e}")

# Also try listing what files exist in the folder
print("\nListing MTG-10X folder:")
try:
    resp = s3.list_objects_v2(
        Bucket=bucket,
        Prefix="expression_matrices/SEA-AD-Multiregion-10X/20260630/"
    )
    for obj in resp.get("Contents", []):
        print(f"  {obj['Key']}  ({obj['Size']/1e9:.2f} GB)")
except Exception as e:
    print("List failed:", e)
