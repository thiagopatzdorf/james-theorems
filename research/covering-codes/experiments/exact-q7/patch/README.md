# Fixed-base patch experiments

The original artifact is never modified. The first 1029 words form the fixed
three-coset base. The 27 sentinel quotient orbits give 9261 exceptions.

## Original patch subset

`solve_original_patch.py` computes literal Hamming coverage of the exceptions by
the 322 original patch words, then solves the restricted set-cover LP/MILP.
Both optima are 322. There are 2450 exception words uniquely covered by one original patch word; each patch word has between two and eighteen such exceptions. Every original patch word has a private exception that no
other word in the original 1351 covers. Thus removing a patch word without
introducing another word is impossible. This does **not** establish a global
lower bound on K_7(9,4), nor exclude replacement or changes to the base.

`private-witnesses.json` contains 322 explicit ambient words and their unique
covering original indices. `verify_private_certificate.py` reads that certificate
and independently checks every distance against all original codewords using
Python scalar loops; it does not trust MILP, NumPy, or the partition generator.

Commands:

```sh
python research/covering-codes/experiments/exact-q7/patch/solve_original_patch.py
python research/covering-codes/experiments/exact-q7/patch/verify_private_certificate.py
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python research/covering-codes/experiments/exact-q7/patch/solve_neighbor_patch.py
```

## Radius-one candidate expansion

`solve_neighbor_patch.py` considers original patch words and every one-coordinate
replacement, excludes fixed-base words, drops empty/identical coverage columns,
and solves a finite restricted set-cover LP/MILP. LP is capped at 90 seconds; MILP is capped at 120 seconds. The LP reached its time limit without an objective certificate in the recorded expanded run.
Only local workspace computation is used; external paid infrastructure spend $0.
A restricted optimum, if obtained, concerns this pool and fixed base only.

A candidate file is not an exhaustive verification result. Any newly smaller
candidate must pass both full-space checkers before becoming an upper bound.

Recorded expanded MILP terminated at120.999944seconds, status1 (time limit),
with an inferior1258-word patch incumbent and no useful lower bound (0).
That incumbent was discarded; the known322-word patch remains best. No
smaller full code was obtained. Timeout is not infeasibility or optimality.
