#!/usr/bin/env python3
"""Deterministically generate distance-only kernel samples from frozen inputs."""
from pathlib import Path
import hashlib
import json
import struct

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
CERT = ROOT / 'certificates/q7_n9_r4_m1351'
code_bytes = (CERT / 'code.txt').read_bytes()
quotient_bytes = (CERT / 'quotient.u16le').read_bytes()
words = code_bytes.decode('ascii').splitlines()
indices = struct.unpack('<117649H', quotient_bytes)
selected = [i for i, v in enumerate(indices) if v != 65535][::57][:2048]


def literal(digits):
    return '![' + ','.join(map(str, digits)) + ']'


lines = []
for i in selected:
    t = i
    tail = []
    for _ in range(6):
        tail.append(t % 7)
        t //= 7
    lines.append('(' + literal([0, 0, 0] + tail[::-1]) + ', ' + literal(words[indices[i]]) + ')')
head = ('import CoveringRecords.Orbit\nset_option maxRecDepth 100000\n'
        'set_option maxHeartbeats 0\nnamespace CoveringRecords.BenchmarkChunked\n'
        'open CoveringCodes CoveringRecords.Orbit\n')
parts = []
for k in range(0, len(lines), 64):
    name = 'chunk' + str(k // 64)
    parts.append('def ' + name + ' : List (Word × Word) := [\n' + ',\n'.join(lines[k:k+64]) +
                 ']\ntheorem ' + name + '_checked : (' + name +
                 '.map (fun p => decide (hammingDist p.1 p.2 ≤ 4))).all id = true := by decide\n')
(HERE / 'BenchmarkChunked.lean').write_text(head + ''.join(parts) +
    '#print axioms chunk31_checked\nend CoveringRecords.BenchmarkChunked\n')
(HERE / 'benchmark-inputs.json').write_text(json.dumps({
    'code_sha256': hashlib.sha256(code_bytes).hexdigest(),
    'quotient_sha256': hashlib.sha256(quotient_bytes).hexdigest(),
    'sample_size': len(selected),
    'quotient_indices': selected,
    'codeword_indices': [indices[i] for i in selected],
    'scope': 'distance-only sample; not full coverage or Finset membership proof'
}, indent=2) + '\n')
