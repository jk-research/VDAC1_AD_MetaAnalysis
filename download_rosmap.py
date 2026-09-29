"""download_rosmap.py - download ROSMAP snRNA-seq from Synapse."""
import os
import synapseclient

AUTH_TOKEN = "eyJ0eXAiOiJKV1QiLCJraWQiOiJXN05OOldMSlQ6SjVSSzpMN1RMOlQ3TDc6M1ZYNjpKRU9VOjY0NFI6VTNJWDo1S1oyOjdaQ0s6RlBUSCIsImFsZyI6IlJTMjU2In0.eyJhY2Nlc3MiOnsic2NvcGUiOlsidmlldyJdLCJvaWRjX2NsYWltcyI6e319LCJ0b2tlbl90eXBlIjoiUEVSU09OQUxfQUNDRVNTX1RPS0VOIiwiaXNzIjoiaHR0cHM6Ly9yZXBvLXByb2QucHJvZC5zYWdlYmFzZS5vcmcvYXV0aC92MSIsImF1ZCI6IjAiLCJuYmYiOjE3ODk1Mzg2NTcsImlhdCI6MTc4OTUzODY1NywianRpIjoiNDcxNzYiLCJzdWIiOiIzNjExNTI5In0.im9aOOiN0OEcKKs1xcSJivSRFU8ggyjMjcjJDmX71hJoBY4m_bl1j4cKCJ1RecRNksJJ9ObmVy3IbeX2MHiMWKPbjyiGVxaQ57v28koDwVDMXL8iaaTLMnGlrdzUp-JItNPXt0YJ3KxZm1haBB3BWWKQoE2FjLDnP8rc6Fwx6jm0giZ3pcVViRIYTqBHcjSPdbySU9z67IO79ea4uDOv5eHTlCGarwWJia79deQGJ-RPwomtF00YZy9rPTiB4MRIKbe7Z0HhdbtBAXA_5NAix6rn0Mj9TI3ha-GhzJPMxIExM4WDDzGWq1i24CZRzQ6p5Rc9KYPiEU3CzPchvqH7dg"

syn = synapseclient.Synapse()
syn.login(authToken=AUTH_TOKEN, silent=True)
print("Login successful.")

BASE = r"C:\Users\jeyak\OneDrive\Documents\VDAC1_AD_Project\data\rosmap_snRNA"
os.makedirs(BASE, exist_ok=True)

regions = {
    "AG":  "syn52408594",
    "EC":  "syn52408588",
    "HC":  "syn52408592",
    "MT":  "syn52408595",
    "PFC": "syn52408599",
    "TH":  "syn52408586",
}

for reg, syn_id in regions.items():
    print("\n=== " + reg + " (" + syn_id + ") ===")
    dest = os.path.join(BASE, reg)
    os.makedirs(dest, exist_ok=True)
    try:
        entity = syn.get(syn_id, downloadLocation=dest)
        print("  Saved: " + str(entity.path))
    except Exception as e:
        print("  ERROR: " + str(e))

print("\n=== Done ===")
