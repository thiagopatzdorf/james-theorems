#!/usr/bin/env python3
"""Verifier A (stdlib only): ball marking.

A code C subset of Z_q^n has covering radius <= R iff the union of the Hamming
balls B(c, R), c in C, is all of Z_q^n.  We mark every word of every ball in a
bytearray indexed by the mixed-radix integer sum d_j * q^j and count unmarked
words.  No syndromes, no linear algebra, no code shared with any generator.

usage: verify_cover.py Q N R CODEFILE      (exit 0 iff VERIFIED)
"""
import sys
from itertools import combinations, product


def main(argv):
    q, n, R = int(argv[1]), int(argv[2]), int(argv[3])
    lines = open(argv[4], encoding="ascii").read().split()
    seen = set()
    for w in lines:
        if len(w) != n or any(not ("0" <= ch < chr(ord("0") + q)) for ch in w):
            print(f"FAILED: malformed word {w!r}")
            return 2
        if w in seen:
            print(f"FAILED: duplicate word {w!r}")
            return 2
        seen.add(w)
    N = q**n
    pw = [q**j for j in range(n)]
    marked = bytearray(N)
    for w in lines:
        d = [int(ch) for ch in w]
        base = sum(d[j] * pw[j] for j in range(n))
        marked[base] = 1
        offs = [[(e - d[j]) * pw[j] for e in range(q) if e != d[j]] for j in range(n)]
        for k in range(1, min(R, n) + 1):
            for pos in combinations(range(n), k):
                for choice in product(*(offs[j] for j in pos)):
                    marked[base + sum(choice)] = 1
    uncovered = N - sum(marked)
    verdict = "VERIFIED" if uncovered == 0 else "FAILED"
    print(f"{verdict} impl=ballmark-py q={q} n={n} R={R} words={len(lines)} space={N} uncovered={uncovered}")
    return 0 if uncovered == 0 else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
