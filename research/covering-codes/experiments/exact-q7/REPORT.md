# Exact K_7(9,4) investigation — final report, 2026-10-02

**Result: COMPUTATIONALLY_VERIFIED construction with 1344 words; exact value unresolved.**

| Quantity | Before | After | Evidence |
|---|---:|---:|---|
| Independently rechecked global LB | 241 | 241 | Exact rational SDP certificate |
| Primary published global LB | 264 | 264 | HHSP 2009 Table 5; game replay incomplete |
| Our verified UB | 1351 | 1344 | Full-space transform, BFS and ball enumeration |
| Fixed 1029-word base completion LB | — | 1182 | Rational dual for all possible patch centers |
| Principal Lean coverage | NOT_PROVED | NOT_PROVED | Conditional bridge and sampled distances |

## Strongest defensible scientific statement

The frozen 1344-word construction covers all 40,353,607 seven-ary length-nine words at radius four, establishing a computational upper bound K_7(9,4)<=1344 and improving our 1351 construction by seven words, while the independently rechecked global lower bound remains 241 and neither the exact value nor global novelty is established.

## Executed work

Four subagents investigated global lower bounds, patch replacement, orbit-pool search and kernel replay. The root independently froze and exhaustively checked every promoted construction. The original 1351 file remains unchanged.

* Each original patch word has a private witness. The original 322-word patch cannot be reduced by deletion alone. A separate scalar checker validates this obstruction.
* A pool of 17,668 radius-one neighbors reached the LP and MILP limits of 90 and 120 seconds, without improvement or a useful optimality bound.
* A pool of 9,947 centers from 29 quotient classes failed under greedy/MILP search; seeded destroy-and-repair then reduced the patch to 317 words, giving 1346 total.
* The expanded pool contains 21,266 centers from 62 classes. Seed 70941346 and 12,432 moves reduced the patch to 315 words. The 1344-word file first appears at iteration 4829. An isolated iteration-bounded replay reproduces its exact bytes.
* Intermediate constructions with 1346 and 1345 words and the final 1344 file all pass both exhaustive checkers, with zero malformed lines, duplicates or uncovered points and exact radius four. Their compact certificates also pass externally.
* Scoring all potential center orbits shows that one arbitrary word covers at most 68 of the 9261 holes. An independent literal-Hamming implementation reconstructs the kernel using 40,353,607 representative/span pairs, checks all 343 translations of the hole set, and cross-checks 200 random centers.
* The stronger rational dual gives 343 times the sum of weights equal to 76217001/500000 = 152.434002. Every completion retaining the original base therefore needs at least 153 patch words, or 1182 words total. All 117,649 constraints are checked exactly; the maximum load is 999974/1000000. Five forged certificates are rejected. This is not a global lower bound for K.
* A third C++ checker enumerates all radius-four balls of the final code: 182,791 points per ball, total multiplicity 245,671,104, zero uncovered points and 53,371 private points. A scalar Python checker verifies one private witness for each of the 1344 words. No word, including a base word, can be singly deleted.
* All 21,266 restricted-pool centers fail the necessary private-hole test for replacing two current patch words by one. This excludes that local move only; it does not prove optimality.
* The global SDP lower-bound certificate 241 passes exact rational replay and adversarial tests. The primary source for 264 is recovered. Two target game-recurrence runs time out at 120 and 60 seconds; both pass 80 independent small concrete-partition cross-checks. Their target status remains UNKNOWN.
* The actual default Lean library builds successfully with 3336 jobs. Twenty printed theorem axiom groups contain only standard logical axioms; there are no sorry/admit terms or new axiom declarations. The partition bridge is conditional. A chunked benchmark checks 2048 real witness distances in 52.83 seconds; full finite data and membership replay are still absent.
* Thirteen fast test methods pass, including real certificate forgeries. Generated table freshness and fixture hashes pass. The six-page paper builds successfully; two final builds produce identical PDF bytes.

## Blocking issues

* An unrestricted lower bound matching 1344 is absent. A fixed-base or candidate-pool optimum cannot close the global gap.
* The target game for 264 remains unreplayed. Histogram and class-partition recursion exhausts its time budget before completing the minimum-class-zero game. Compressed winning/losing frontiers and minimum-convolution acceleration are not implemented.
* Complete kernel replay requires all finite quotient/exception checks, coset inclusion and linkage to the original code Finset. The roughly 43-minute distance-only estimate is an extrapolation, not an executed run, and excludes membership and partition proofs.
* Global novelty review remains incomplete. The original 1351 generator revision and seed are unknown; the new search seed, source hashes and iteration provenance are recorded.

## Budget

The ceiling is USD 5 of additional infrastructure. No paid resources were created; additional provisioned infrastructure spend is USD 0. Computation used the existing three-core executor with approximately 9.7 GiB RAM. No GCP identity was configured. Model, subagent and session billing is not exposed to this ledger, so no total inference-cost claim is made.

## Reproduction

```sh
make verify-q7-9-4-1344-computational
make exact-q7-audit
make covering-fast
make covering-formal
make paper
python research/covering-codes/experiments/exact-q7/replay_best.py
```

The computational command checks hashes, A, B and the compact certificate. The executed formal chain `make verify-q7-9-4-1344` passes its computational checks and actual library build, then fails closed at the missing principal replay (script exit 3, Make exit 2); see full-chain.log. A conditional adapter cannot pass that gate. Searches remain manual bounded commands, rather than automatic PR jobs.

## Artifacts

| Path, relative to research/covering-codes | SHA-256 |
|---|---|
| `certificates/q7_n9_r4_m1351/code.txt` | `6d1b0e1abb8079df06a28d5301607d3d5247e0f2005d72e13f695ce26f6e6b52` |
| `certificates/q7_n9_r4_m1346/code.txt` | `3506511566dfa02adda6d2c6558e37ff136fdea38f79d0addef96b806ebdd882` |
| `certificates/q7_n9_r4_m1345/code.txt` | `a3cd245f28d4c0b745b7408f003485b5d887bea5dcd2c16276d342766bd4fea0` |
| `certificates/q7_n9_r4_m1344/code.txt` | `6a1653b6697b4ed2c8753b2ae5f5a6c0878a05b7cc47873d11b0387b11703db9` |
| `certificates/q7_n9_r4_m1344/quotient.u16le` | `a6db791fe5a6cfa8af603d5c4c4a4cbbd9342cb53900325001c1285b15ac8aef` |
| `certificates/q7_n9_r4_m1344/exceptions.u16le` | `fb0f865cc57c9d88ef64c0ea784a27f84031036079414c8141b86905a4a2ec2c` |
| `experiments/exact-q7/global/dual-certificate.json` | `55880f3fc837cea063da3530e68a89f9b2f0bd798f48712014d9ab188460db1f` |
| `experiments/exact-q7/deletion/coverage-counts.json` | `6c602a0ab7d64e0b8b591d1d47cf0bd4ce790bdf2c1296c46a6b88b7a2b8ddb0` |
| `formal/CoveringRecords/CompactReplay.lean` | `0aa3c43e942e78d32c9aead31832f1c13c6bce5da96504ec7dda891679573ec8` |
| `preprint/paper.tex` | `1d423ebd33e5427bcb080670d62c829a81ca8b68704ffaa7edaa339619dd5169` |
| `preprint/paper.pdf` | `4b6e46ef28a1381bf28f19228bbfe2f77f0567cc7f92bbc670216a032e1b9a45` |

The 1344 compact quotient||exception certificate SHA-256 is `a5df44128b6d9740fc5d712154f38fae37cbfd8518c7c995a9eb2d451f309aac`, 253820 bytes. Root ARTIFACTS.sha256 covers all tracked research artifacts except itself; smaller agent manifests are preserved too.

## Commits

Only research/covering-codes-preprint; no merge to main. Execution commits before this final report:

```text
f03223cca82a5d6bb868eb7fb6d0432db8f340b2 formal: add partition replay bridge and kernel-check 2048 real witness distances
950e41fe28246072f528fec1cc629ef6ba72770c research: verify improved q7 n9 r4 construction with 1346 words
54ef800eb3727a03d0411b4436c2c01afb74bcfb research: lower q7 n9 r4 upper bound to 1344 and audit restricted lower bound 1182
```

The final report/table/paper/hash-freeze commit is recorded in Git history and the final response, avoiding a self-referential SHA.

## Next experiment

Strengthen the global lower-bound machinery and permit wider base/coset changes; separately close the compact kernel replay. The current fixed-base lower bound 1182 versus upper bound 1344 and local obstructions direct the next search, without implying exact K.
