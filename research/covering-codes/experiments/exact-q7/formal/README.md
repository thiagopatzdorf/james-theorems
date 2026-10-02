# Bounded kernel replay experiment

The new `formal/CoveringRecords/CompactReplay.lean` proves the exact mathematical
bridge needed by the existing compact partition certificate. Coverage follows
from three explicit hypotheses: the three complete cosets are included in the
original code, every nonexceptional normalized word has a base witness, and
every ambient word in an exceptional orbit has an original-code witness.
The resulting `principal_upper_of_partition` remains **conditional**: this
experiment does not establish those three hypotheses for the complete payload.

`Pilot.lean` kernel-checks 64 actual quotient/witness distances, spread uniformly
through the 117649 representative indices. Its generated inputs record the
original code and quotient hashes in `pilot-inputs.json`. No native evaluator,
additional axiom, external-checker oracle, or admitted proof is used. A Boolean
list checker proved by `decide` is converted to an ordinary quantified theorem.
A direct `decide` of the quantified proposition initially exceeded recursion
limits; using the Boolean checker avoids that elaboration route. The successful
final log contains only the standard axioms `propext`, `Classical.choice`, and
`Quot.sound` for both pilot theorems.

The bridge additionally proves membership of the first actual preserved word
and its self-distance bound. It does not prove membership for all 64 pilot
witnesses, full payload index correctness, all 117649 representative distances,
9261 exceptional witness checks, or complete coset inclusion in the original
Finset. Consequently the principal coverage status stays `NOT_PROVED`.

Reproduce from `research/covering-codes/formal`:

```
lake env lean CoveringRecords/CompactReplay.lean
lake env lean ../experiments/exact-q7/formal/Pilot.lean
```

No cloud resources were created by this experiment.

## Larger benchmark

`BenchmarkChunked.lean` successfully checks **2048 real witness distances**,
split into32chunks of64, in52.83seconds. It uses kernel `decide` and
standard axioms only. Source size is99279bytes. The monolithic2048
version was interrupted at52.48seconds due memorygrowth; its timing and
source are retained as an explicitly unsuccessful experiment. A fresh64
pilot took13.74seconds including imports and peaked at2.61GiB childRSS.
The chunked experiment remained below~3.1GiB LeanRSS in sampled process
observations (not a formally measured peak).

A rough linear extrapolation suggests~43minutes and~6.15MB Lean source
for126883 distance checks using this literal representation. This excludes
code membership, full coset inclusion, and partition reconstruction proofs.
Therefore a complete kernel replay was not attempted within this bounded
round, and the principal theorem remains unproved. These estimates are not
claims about an executed fullcheck or an unavoidable computational cost.
