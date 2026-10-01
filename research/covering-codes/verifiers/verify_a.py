#!/usr/bin/env python3
"""Exhaustive reference: every ambient word, every codeword, literal Hamming.
No early radius exit: max_min_distance is exact. The default literal scan is
cross-checked against the separable min-plus transform used for large spaces.
"""
import argparse
import hashlib
import itertools
import json
from pathlib import Path
import time


def verify(q, n, radius, path, parse_only=False, method='scan'):
    if not (2 <= q <= 10 and 1 <= n <= 32 and 0 <= radius <= n):
        raise ValueError('require 2<=q<=10, 1<=n<=32, 0<=R<=n')
    start = time.monotonic()
    raw = Path(path).read_bytes()
    lines = raw.split(b'\n')
    if raw.endswith(b'\n'):
        lines.pop()
    code, invalid = [], []
    for number, line in enumerate(lines, 1):
        if len(line) != n or any(c < 48 or c >= 48 + q for c in line):
            invalid.append(number)
        else:
            code.append(tuple(c - 48 for c in line))
    unique = list(dict.fromkeys(code))
    result = dict(q=q, n=n, R=radius, M_parsed=len(code), M_unique=len(unique),
                  duplicates=len(code)-len(unique), invalid_lines=len(invalid),
                  invalid_line_numbers=invalid, ambient_words=q**n,
                  sha256=hashlib.sha256(raw).hexdigest(),
                  canonical=bool(raw) and raw.endswith(b'\n') and not invalid,
                  covered=None, uncovered=None, max_min_distance=None,
                  first_uncovered=None, exhaustive=False)
    if not parse_only and not invalid and unique and method == 'transform':
        # Separable min-plus transform. After processing axes 0..k, each cell
        # holds min_c [processed mismatch count + unprocessed equality constraint].
        # Updating a coordinate costs 0 to stay, 1 to select any other symbol.
        # min(old[j], 1+min(old[:])) is exactly that coordinate's transform.
        import numpy as np
        if q**n > 250_000_000:
            raise ValueError('transform memory guard')
        distance = np.full((q,)*n, n+1, dtype=np.uint8)
        for c in unique:
            distance[c] = 0
        for axis in range(n):
            cheapest = distance.min(axis=axis, keepdims=True)
            np.minimum(distance, cheapest + np.uint8(1), out=distance)
        flat = distance.reshape(-1)
        covered = int(np.count_nonzero(flat <= radius))
        # Argmax gives the first True without allocating all uncovered indices.
        bad = flat > radius
        first = None
        if covered != q**n:
            index = int(bad.argmax())
            first = ''.join(str(int(d)) for d in np.unravel_index(index, (q,)*n))
        result.update(covered=covered, uncovered=q**n-covered,
                      max_min_distance=int(flat.max()), first_uncovered=first,
                      exhaustive=True)
    elif not parse_only and not invalid and unique:
        covered, maximum, first = 0, 0, None
        for word in itertools.product(range(q), repeat=n):
            nearest = min(sum(a != b for a, b in zip(word, c)) for c in unique)
            maximum = max(maximum, nearest)
            if nearest <= radius:
                covered += 1
            elif first is None:
                first = ''.join(map(str, word))
        result.update(covered=covered, uncovered=q**n-covered,
                      max_min_distance=maximum, first_uncovered=first, exhaustive=True)
    elif not parse_only and not invalid:
        result.update(covered=0, uncovered=q**n, first_uncovered='0'*n, exhaustive=True)
    result['runtime_seconds'] = time.monotonic()-start
    result['method'] = method
    return result


def main():
    p = argparse.ArgumentParser(description=__doc__)
    for name in ('q', 'n', 'R'):
        p.add_argument(name, type=int)
    p.add_argument('code')
    p.add_argument('--parse-only', action='store_true')
    p.add_argument('--expected-m', type=int)
    p.add_argument('--method', choices=('scan','transform'), default='scan')
    a = p.parse_args()
    try:
        r = verify(a.q, a.n, a.R, a.code, a.parse_only, a.method)
    except (OSError, ValueError) as e:
        print(json.dumps({'status': 'ERROR', 'error': str(e)}))
        return 2
    valid = (not r['invalid_lines'] and r['canonical'] and
             (a.expected_m is None or r['M_parsed'] == a.expected_m) and
             (a.parse_only or r['uncovered'] == 0))
    r['status'] = ('PARSED' if a.parse_only else 'PASS') if valid else 'FAIL'
    print(json.dumps(r, indent=2))
    return 0 if valid else 1


if __name__ == '__main__':
    raise SystemExit(main())
