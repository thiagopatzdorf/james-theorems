# Separately pinned Lean project

Florath upstream: `460df105545c2d6b04ba71f29de6b56dbda92825`.
Toolchain: Lean 4.30.0-rc2, as pinned upstream; nested lake-manifest pins dependencies.
The root repository toolchain is unchanged.

Actual library build: PASS. Principal **coverage** theorem: NOT_PROVED.

* `Candidate.lean`: conditional adapters/proposition shapes, not witnesses.
* `Tiny.lean`: 000/111 gives `QaryKUpper 2 3 1 2` with `covering_decide +kernel`.
* `Selector.lean`: existing upstream CoversFinset from checked membership/distance.
* `PrincipalCode.lean`: original-order 1351 words and cardinality <=1351; no coverage assertion.
* `PrincipalCodeManifest.json`: exact source/code hash linkage, expressly coverage=false.
* `Audit.lean`: printed dependencies for actual theorems. Standard logical axioms only.

```
elan toolchain install leanprover/lean4:v4.30.0-rc2
MATHLIB_NO_CACHE_ON_UPDATE=1 lake update
lake build
lake env lean Audit.lean
```

The upstream-supported environment setting bypasses only optional cache download,
not source/proof verification. In this environment initial caches failed 403/429;
dependencies were fetched at manifest pins and compiled from source. The first
build attempted before a newly added Selector module was scheduled failed; the
subsequent clean dependency graph build succeeded. Earlier no-op `lake build`
without a default target was not accepted; the library now has an explicit default.

`formal-verification.json` reports build scope. A principal proof would need an
unconditional `q7_n9_r4_m1351`, with original byte linkage and coverage proof;
`tools/verify_case.py` then checks its exact type and standard-axiom dependencies.
No PrincipalManifest.json is fabricated for the conditional adapters.
