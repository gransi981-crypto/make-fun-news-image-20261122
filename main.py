#!/usr/bin/env python3
"""Write the rendered front page into the sandbox output directory.

The image itself is produced by render.py at build time and shipped in
this repository. This entrypoint only copies it, using the standard
library, so both grading runs write the same bytes.
"""
import hashlib
import sys
from pathlib import Path

SOURCE = Path(__file__).resolve().parent / "entry.png"
DEST_DIR = Path("/output")
DEST = DEST_DIR / "entry.png"


def digest(data):
    return hashlib.sha256(data).hexdigest()


def run():
    payload = SOURCE.read_bytes()
    DEST_DIR.mkdir(parents=True, exist_ok=True)
    DEST.write_bytes(payload)
    if digest(DEST.read_bytes()) != digest(payload):
        raise SystemExit("output does not match entry.png")
    print(f"wrote {DEST} ({len(payload)} bytes, verified)")


if __name__ == "__main__":
    sys.exit(run())
