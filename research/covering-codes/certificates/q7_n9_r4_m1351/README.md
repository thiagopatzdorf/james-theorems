# K_7(9,4) <= 1351 — candidate certificate slot

**Status: artifact missing / theorem not yet asserted.**

The search report states that a 1351-word construction exists from a previous run, but the canonical `pp1_*` output file is not currently present in the connected GitHub repository. No codeword list is reconstructed from logs or memory.

Required files before promotion:

- `code.txt`
- `metadata.json`
- `SHA256SUMS`
- `verification-a.json`
- `verification-b.json`
- `provenance.md`
- `literature.md`
- a Lean instance certificate tied to the same hash

A valid certificate must establish that every one of the `7^9 = 40,353,607` ambient words is within Hamming distance at most 4 of one of the 1351 codewords.

The matching **lower** bound is no longer open: `K_7(9,4) ≥ 221` is
`CoveringRecords.hammingSphere_q7_n9_r4` (sphere-covering / Hamming ball,
kernel `decide`). The gap 221…1351 is only closed from above by the files
above.
