#!/usr/bin/env python3
"""Shannon-entropy check of files recovered from the evidence image.
Encrypted/compressed content approaches 8.0 bits/byte; plain text is ~4-5."""
import math, sys, pathlib, collections
def entropy(b):
    if not b: return 0.0
    n = len(b)
    return -sum(c/n*math.log2(c/n) for c in collections.Counter(b).values())
root = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else "/tmp/extracted/Clinical")
print(f"{'FILE':<38} {'SIZE':>7} {'ENTROPY':>8}  VERDICT")
for p in sorted(root.iterdir()):
    d = p.read_bytes(); e = entropy(d)
    v = "HIGH - consistent with encrypted data" if e > 7.5 else "normal text"
    print(f"{p.name:<38} {len(d):>7} {e:>8.3f}  {v}")
