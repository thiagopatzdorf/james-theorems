#!/usr/bin/env python3
"""Exhaustive reference: every ambient word, every codeword, literal Hamming.
No early radius exit: max_min_distance is exact. Large instances are costly.
"""
import argparse
import hashlib
import itertools
import json
from pathlib import Path
import time


def verify(q, n, radius, path, parse_only=False):
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
    if not parse_only and not invalid and unique:
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
    return result


def main():
    p = argparse.ArgumentParser(description=__doc__)
    for name in ('q', 'n', 'R'):
        p.add_argument(name, type=int)
    p.add_argument('code')
    p.add_argument('--parse-only', action='store_true')
    p.add_argument('--expected-m', type=int)
    a = p.parse_args()
    try:
        r = verify(a.q, a.n, a.R, a.code, a.parse_only)
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
