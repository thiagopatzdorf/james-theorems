> Historical initial audit, frozen in commit36674025d9dd0c52242aa585d75d07fba6ea0054.
> The2026-10-02 follow-up improves the construction to1344; see experiments/exact-q7/REPORT.md.
> Paper and table at current paths have since been updated; historical hashes below refer to that frozen commit.

# Final audit report — 2026-10-01

Outcome **B: COMPUTATIONALLY_VERIFIED + explicitly incomplete formalization**.
Principal novelty classification: **CANDIDATE_NEW_UPPER_BOUND**, relative to the
best independently replayed prior bound found in this audit. No global record claim.

| Case | Verified LB | Prior verified UB | Our UB | Verifier A | Verifier B | Lean | Prior art | Status |
|---|---:|---:|---:|---|---|---|---|---|
| K_7(9,4) | 241 | 1475 | 1351 | PASS | PASS | cardinality + orbit algebra; coverage incomplete | published prior UB 1475 | COMPUTATIONALLY_VERIFIED + CANDIDATE_NEW_UPPER_BOUND |
| K_4(10,4) | 51 | — | 192 | PASS | PASS | not individually formalized | published prior UB 208 | COMPUTATIONALLY_VERIFIED + NOVELTY_UNRESOLVED |
| K_5(7,2) | 236 | — | 500 | PASS | PASS | not individually formalized | published prior UB 525 | COMPUTATIONALLY_VERIFIED + NOVELTY_UNRESOLVED |
| K_5(9,3) | 354 | — | 1250 | PASS | PASS | not individually formalized | published prior UB 1275 | COMPUTATIONALLY_VERIFIED + NOVELTY_UNRESOLVED |
| K_5(10,4) | 158 | — | 625 | PASS | PASS | not individually formalized | published prior UB 875 | COMPUTATIONALLY_VERIFIED + NOVELTY_UNRESOLVED |
| K_5(9,4) | 62 | — | 250 | PASS | PASS | not individually formalized | published prior UB 255 | COMPUTATIONALLY_VERIFIED + NOVELTY_UNRESOLVED |
| K_5(9,5) | 16 | — | 50 | PASS | PASS | not individually formalized | published prior UB 55 | COMPUTATIONALLY_VERIFIED + NOVELTY_UNRESOLVED |
| K_7(8,3) | 471 | — | 1893 | PASS | PASS | not individually formalized | published prior UB 2337 | COMPUTATIONALLY_VERIFIED + NOVELTY_UNRESOLVED |

Verified LB means independently rechecked sphere/rational-certificate evidence,
not the strongest merely published number. Published LBs are 264,62,236,354,177,
64,19,471 in row order. Secondary prior UBs are documentary table entries; their
constructions were not replayed, so the prior-verified column is deliberately empty.
See literature.md and generated bounds.json for source/evidence distinctions.

## Strongest defensible scientific statement

O arquivo original preservado de 1351 palavras distintas cobre exaustivamente
{0,...,6}^9 a raio 4, sustentando K_7(9,4)<=1351 e melhorando o bound 1475 revalidado
nesta auditoria, com prova Lean de cobertura ainda incompleta e novidade global
não estabelecida.

## Blocking issues

* Principal Lean coverage replay: packed witness exists and externally passes, but
  orbit algebra is kernel-proved; finite representative/exception payload checks and
  their linkage to the original code Finset remain unproved, with no unconditional principal theorem.
* Full generation reproducibility: original principal generator revision and seed
  are unknown; preserved Git object/raw/sorted hash consistency is established.
* Definitive novelty: partial forward-citation coverage and access failures
  (Scholar 429, zbMATH/MathSciNet 403); secondary same-size prior art remains unresolved.

No artifact is missing. Lean installation/build and computational coverage are
resolved, not blockers. No 1350 search/optimization jobs were run.

## Executed validation

* Twelve test methods PASS, including all 255 nonempty binary length-3 subsets at
  every radius, other alphabets, malformed parsers, duplicate handling and certificate attacks.
* `make covering-fast` PASS; generated table and fixture hashes checked.
* `make verify-all-computational` PASS on all eight actual artifacts.
* Real `lake update` PASS (optional cache disabled), `lake build` PASS (3335 jobs),
  16 printed theorem axiom groups standard only; zero sorry/admit/new axiom declarations.
  Ten orbit normalization/isometry/coset transport theorems are included; coverage is not.
* Principal full-chain command executes hash+A+B+flat and compact certificates+actual Lean build,
  then fails closed at missing principal replay (script exit 3 / make exit 2).
  This expected failure is not reported as a principal formal PASS.
* `make paper` PASS, five-page PDF. CI workflow authored; no unexecuted CI PASS claim.

* Compact partition validation PASS: 117649 representatives, 27 exceptional
  orbits / 9261 words, 253820 payload bytes; exact decomposition independently checked.
* All 21 recovered archive files match their original full Git blob identities.

## Artifacts: canonical files and SHA-256

Paths below are relative to `research/covering-codes/`.

| Path | SHA-256 |
|---|---|
| `certificates/q4_n10_r4_m192/code.txt` | `83c0f109876b9773867e2e3680e2e04862c3ad641df47d8c56139445403d7410` |
| `certificates/q5_n10_r4_m625/code.txt` | `ba1ec554be784e105c9c729c0cb5ea08c5cf10d120ee617ede96d864a83e53b9` |
| `certificates/q5_n7_r2_m500/code.txt` | `52a85f1b069e06df3c8503a3001e90d8d8170139e05b4ced05c5b8dabe5c27c3` |
| `certificates/q5_n9_r3_m1250/code.txt` | `334d055a45bcc7fffd7cc7ed5cefd719e8787587ced1b66b44cc85785a6bdea6` |
| `certificates/q5_n9_r4_m250/code.txt` | `c605e57c41117da0141fdd88dc3972598fb4dd6e02bedc3edd477330f3bf5922` |
| `certificates/q5_n9_r5_m50/code.txt` | `136e55ebc1151ce5b1eaac414f6735209e8d4f4136352018b516d65140b58499` |
| `certificates/q7_n8_r3_m1893/code.txt` | `07e2f3c1c65608b037fb13a2e85fd9ea25c2ace2bcc9e30a128e1833c2d06e28` |
| `certificates/q7_n9_r4_m1351/code.txt` | `6d1b0e1abb8079df06a28d5301607d3d5247e0f2005d72e13f695ce26f6e6b52` |
| `certificates/q7_n9_r4_m1351/witness.u16le.gz` | `6f91c10f75e6d3e27a0539b1d74a799e42f79638e024551efbde6ef2d069db7a` |
| `certificates/q7_n9_r4_m1351/quotient.u16le` | `a6db791fe5a6cfa8af603d5c4c4a4cbbd9342cb53900325001c1285b15ac8aef` |
| `certificates/q7_n9_r4_m1351/exceptions.u16le` | `201de24a8fd5597fd6e61a08b8a520dbf8f93fd1814160591072c2458bd7a538` |
| `preprint/paper.tex` | `5efafff64706c3f6cdfcb9de4fd57edf183f95ab0c43b0f536d67cfd3a3cf496` |
| `preprint/paper.pdf` | `85f1cf4f26ab619d9c98751546a2577fd4ecaf3eaef52d77d30e398d77e15118` |

Uncompressed witness payload SHA-256:
`6f4425a72b66efa284e7ffc1bfd20117fc058e44bb46b37650f2c9dca5a72d2a`.
Flat payload length 80,707,214 bytes. Compact quotient/exception concatenation
SHA-256: `014e806eaec285341392cbc2df13043e3d44612070c77215486d6432d2fe76e1`. `ARTIFACTS.sha256` covers archived objects,
checkers, sources, certificates, metadata, reports and paper; it excludes itself.
Source Git archive commit: `e7f3ed9c52e6992eaa244fc75a04ed4abed89fd1`.
All 21 retrieved files match their full Git blob identities, not just API text.

## Commits

Branch: `research/covering-codes-preprint`, no merge to main.
The execution commits preceding this final report are (the research-only merge
preserves concurrent sphere-proof commit f5129539417d55e4a91303a5f7fb0f7d7d06b7de):

```text
758f866cd93cbdaa67730ca61c85f3016385fb51 research: add independent exhaustive covering verifiers and adversarial tests
a848b1baca77bf73aa9fcc78f8a53dea251d9c66 research: exclude local checker and build caches
3f11ca5bb22db3b717d7bf0993345a45d3899431 research: recover and freeze all eight original covering constructions
f5bbc084a813d253883b05ad558098e116d152b3 research: cross-check exact Hamming transforms and freeze byte ingestion
835f11e3f142790b3d58b2172ae646f1d583f145 formal: build kernel-checked tiny code and principal cardinality at pinned upstream
cfc3f54d6292d49c956701edddb845b376baceb9 research: add and validate packed witnesses for every principal ambient word
aa79145e191dab9309e0308f6a5a0cd477d5c58e research: audit primary prior art and distinguish replayed bounds from tables
32db6bc46a023283b886b61518376a44d6b9e194 paper: report audited constructions, formal gap and one-command reproduction
13746ee897d99b27ab410b985b70d9979e9d3251 research: freeze final audit reports and full artifact hash manifest
9e94957a265a7ebd4dda25d0048919e0a0b201b5 research: integrate concurrent sphere-bound proof on the research branch
51cbe4a34d473afc10671d03b540a8b4e2393864 research: verify compact orbit partition with only 253820 payload bytes
c163d9599518dd52d20d5ce22ca1dd2b45dc4069 formal: prove orbit normalization, Hamming isometry and coset witness transport
38775ed7921c0a1e703429ef8f31301255bbc1e6 ci: cache pinned Mathlib and accommodate measured source-build cost
```

The final report/hash-freeze commit is intentionally not self-referential; obtain
its SHA from this branch's Git history and the final response.

## Paper

`preprint/paper.tex` and `preprint/paper.pdf` (actual generated five-page PDF).
Title: Improved Upper Bounds for q-ary Covering Codes with Reproducible and
Proof-Carrying Verification. Its principal theorem is explicitly labelled
computationally verified; its Lean gap is explicit.

## Next experiment

Replay the frozen compact orbit partition in Lean with a proved decoder, finite representative/exception checks and original-Finset linkage; normalization and coset transport are already proved, keeping the code hash fixed. The principal computational gate has
passed; no claimed formal gate or global novelty gate is manufactured to launch 1350.
