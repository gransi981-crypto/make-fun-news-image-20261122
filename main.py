#!/usr/bin/env python3
"""Entrypoint: write the finished front page to /output/entry.png.

Standard library only. The image is drawn by render.py at build time and
shipped in this repository, so every run writes the same bytes.
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))


def main():
    src = os.path.join(HERE, "entry.png")
    os.makedirs("/output", exist_ok=True)
    dst = os.path.join("/output", "entry.png")
    with open(src, "rb") as handle:
        data = handle.read()
    with open(dst, "wb") as handle:
        handle.write(data)
    with open(dst, "rb") as handle:
        written = handle.read()
    if written != data:
        raise SystemExit("copy mismatch: output differs from entry.png")
    print(f"wrote {dst} ({len(data)} bytes, verified)")


if __name__ == "__main__":
    sys.exit(main())
