# Covering codes — audited status, 2026-10-01

**Principal outcome B: COMPUTATIONALLY_VERIFIED, formalization incomplete.**
Novelty: **CANDIDATE_NEW_UPPER_BOUND** relative to the independently replayed
1475 construction in Marosi v3. No global best-known claim.

All eight original-source files were recovered from Factory research branch
`research/preco-da-impossibilidade`, commit `e7f3ed9c52e6992eaa244fc75a04ed4abed89fd1`.
The earlier missing-artifact diagnosis is superseded. Exact Git blob hashes,
byte preservation and old raw/sorted principal hashes establish archive provenance;
original generation revision/seed remains incompletely documented.

The frozen principal has 1351 distinct nine-symbol words over 0..6; both exhaustive
checkers agree on SHA-256, 40,353,607 covered, zero uncovered, zero malformed lines,
zero duplicates and exact radius four. All seven secondary codes also pass A/B.
A packed selector for all principal ambient words passes independent external
validation. These are actual executed measurements, not earlier stdout claims.

Lean 4.30.0-rc2 was installed. Real `lake update` and `lake build` succeeded using
the pinned Florath library and source-built Mathlib (cache downloads had 403/429).
The tiny construction, generic selector bridge and loaded principal Finset's
cardinality are proved. **The unconditional theorem `QaryKUpper 7 9 4 1351`
is not present:** packed decoding/membership/coverage replay remains incomplete.
No sorry, admit or new axioms; actual theorem dependencies are standard logical
axioms only. See `formal-verification.json` and `audit/lean-axioms.log`.

`bounds.json` distinguishes independently rechecked lower/prior-upper bounds
from documentary published bounds, and computes exact rational alpha intervals.
`literature.md` records v3, historical primary/table evidence, searches and access
limits; secondary novelty remains unresolved.

From root: `make covering-fast`, `make verify-all-computational`,
`make covering-formal`, `make paper`.
`make verify-q7-9-4-1351` runs the complete principal chain and fails closed
(exit 3 from its script; make reports 2) until principal Lean coverage exists.
`make verify-computational` reproduces the completed B-level result successfully.
No optimization jobs were run. The next work is kernel replay of the frozen
certificate; 1350 is not approved by a claimed Lean success.

The concurrent research-branch commit `f5129539417d55e4a91303a5f7fb0f7d7d06b7de` adds the classical sphere lower bound `QaryKLower 7 9 4 221`; its source is preserved and included in the actual final build. This is separate from principal upper-bound coverage and from the stronger computationally rechecked LB 241.
