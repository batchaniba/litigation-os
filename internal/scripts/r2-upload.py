#!/usr/bin/env python3
"""Upload documents-branch PDFs to Cloudflare R2 (upload-only mirror).

Usage: r2-upload.py --list <file>   # newline-separated repo-relative paths

Key scheme: sha256/<first2>/<rest>.pdf (content-addressed, deterministic
from file bytes — the same scheme as the one-time migration, so keys
stay stable and `npm run docs:fetch <sha256>` keeps resolving).

Idempotent: HEAD each key first and skip when the ETag already matches
the local MD5. After PUT, HEAD again and require ETag == local MD5 hex
(byte verification, no re-download). PUT carries Content-MD5 so R2
rejects corrupt uploads server-side.

Never deletes from R2: removed branch paths leave their objects in place
(R2 is the durable store; the manifest on main is the index).
Exits non-zero if any file fails.
"""
import sys, os, json, hashlib, base64
from concurrent.futures import ThreadPoolExecutor

R2_KEY = os.environ["R2_ACCESS_KEY_ID"]
R2_SECRET = os.environ["R2_SECRET_ACCESS_KEY"]
R2_ACCOUNT = os.environ["R2_ACCOUNT_ID"]
R2_BUCKET = os.environ["R2_BUCKET"]
ENDPOINT = f"https://{R2_ACCOUNT}.r2.cloudflarestorage.com"
REPO_ROOT = os.environ.get("REPO_ROOT", os.getcwd())

import boto3
from botocore.config import Config
s3 = boto3.client(
    "s3", endpoint_url=ENDPOINT,
    aws_access_key_id=R2_KEY, aws_secret_access_key=R2_SECRET,
    config=Config(signature_version="s3v4", max_pool_connections=16),
)

def r2_key_for(sha256):
    return f"sha256/{sha256[:2]}/{sha256[2:]}.pdf"

def head_etag(key):
    try:
        r = s3.head_object(Bucket=R2_BUCKET, Key=key)
        return (r.get("ETag") or "").strip('"')
    except Exception as e:
        if "404" in str(e) or "Not Found" in str(e):
            return None
        raise

def process(rel):
    log = {"path": rel}
    try:
        with open(os.path.join(REPO_ROOT, rel), "rb") as f:
            data = f.read()
        sha256 = hashlib.sha256(data).hexdigest()
        md5hex = hashlib.md5(data).hexdigest()
        key = r2_key_for(sha256)
        log.update(size=len(data), sha256=sha256, r2_key=key)
        if head_etag(key) == md5hex:
            log["status"] = "skipped_already_present"
            return log
        for attempt in range(4):
            try:
                s3.put_object(
                    Bucket=R2_BUCKET, Key=key, Body=data,
                    ContentType="application/pdf",
                    ContentMD5=base64.b64encode(hashlib.md5(data).digest()).decode(),
                    Metadata={"source-path": rel[-900:], "repo": "newanforbi/interactive-litigation-portfolio"},
                )
                break
            except Exception:
                if attempt == 3:
                    raise
        if head_etag(key) != md5hex:
            raise RuntimeError("ETag mismatch after PUT")
        log["status"] = "uploaded"
        return log
    except Exception as e:
        log["status"] = "failed"
        log["error"] = str(e)[:300]
        return log

def main():
    if len(sys.argv) != 3 or sys.argv[1] != "--list":
        print("usage: r2-upload.py --list <file>", file=sys.stderr)
        sys.exit(2)
    with open(sys.argv[2]) as f:
        paths = [line.strip() for line in f if line.strip()]
    failed = 0
    with ThreadPoolExecutor(max_workers=8) as ex:
        for log in ex.map(process, paths):
            print(json.dumps(log), flush=True)
            if log["status"] == "failed":
                failed += 1
    print(f"done: {len(paths)} files, {failed} failed", file=sys.stderr)
    sys.exit(1 if failed else 0)

main()
