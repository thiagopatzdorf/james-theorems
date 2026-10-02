# Global lower-bound audit for K_7(9,4), 2026-10-02

**No new global lower bound was established. No exact value was established.**
The independently rerun rational SDP certificate proves `K_7(9,4) >= 241`
subject to the cited SDP theorem and its programmatic model transcription.
The primary 2009 source reports the stronger `K_7(9,4) >= 264`; this numerical
claim is now checked directly against its original published table, but its
winning-game computation has not been independently reproduced; bounded
reimplementation attempts are recorded below.

## Executed checks

Run from repository root:

```
python research/covering-codes/experiments/exact-q7/lower/audit_lower.py
```

The standard-library checker reconstructs all 189 variables, 2356 linear
constraints and 90 PSD blocks. Exact rational LDL-style elimination checks the
PSD dual blocks, and exact integer arithmetic checks every dual inequality.
Its full self-test on small actual covering codes also passed.

The certificate establishes

```
K^3 >= 1078169490279442539265627245374932 / 77371252455336267181195264
240^3 * 77371252455336267181195264 < 1078169490279442539265627245374932
1078169490279442539265627245374932 <= 241^3 * 77371252455336267181195264
```

Hence the integer lower bound is 241. This is weaker than the published 264.
Negative tests reject negative linear multipliers, zero denominators, negative
PSD pivots, invalid sphere-covering weights, indefinite/asymmetric matrices and
zero pivots with nonzero off-diagonals. A singular rank-one PSD matrix is accepted.
A printed claim is compared with the bound actually computed; merely changing
`claim.K_lower_bound` cannot establish a stronger theorem.

The classical sphere count is independently recomputed:
`7^9=40353607`, `V_7(9,4)=182791`, `ceil(7^9/V)=221`.
Neither bound has been newly replayed in Lean by this experiment.

## Primary source for 264

Wolfgang Haas, Immanuel Halupczok and Jan-Christoph Schlage-Puchta,
*Lower Bounds for q-ary Codes with Large Covering Radius*, Electronic Journal
of Combinatorics 16(1), R133, published 2009-11-07, DOI 10.37236/222.
The unchanged publisher PDF and extracted text are archived here. Table 5,
printed page 17, gives:

```
K7 (9, 4)    5         221       227       264    1843
```

The columns are `k=n-R`, sphere bound, old lower bound, new lower bound,
and old upper bound. The proof architecture is precise: for every hypothetical
M-word code, coordinate symbol classes give q-partitions of the M rows;
a transversal agreeing with each row in fewer than k coordinates is an
uncovered word. Theorem 6 converts a winning transversal-searcher strategy
into `K_q(n,n-k)>M`. Theorem 9 allows a chain of minimum class sizes to
exclude partitions lacking a uniform strategy at minimum zero.

To reproduce 264 one must exclude M=263 with actual winning-game data or
reimplement and validate that complete game calculation. The publisher paper
states its C++ implementation can be obtained from the authors; it does not
supply machine-readable strategy certificates. No messages to authors were
sent. The paper reports up to week-long individual games for its largest
k=5 cases; those historical timings are not estimates for this machine.

An important mathematical limitation: failure of the adaptive game strategy
is not existence of a code. The paper explicitly notes the converse of
Theorem 6 fails: a partition player may adapt to the transversal player's
choices, while a covering code requires fixed partitions. Therefore even an
optimal adaptive-game bound cannot by itself establish the exact global K.
The authors also say their table entries exhaust their specified strategy,
so repeating this architecture does not promise an improvement over 264.

## Remaining gap

Before any new upper-bound experiments, the audit supports `241 <= K <= 1351`
with independently rechecked certificates on both sides, and the primary
published interval is `264 <= K <= 1351`. Optimizing the added words around
one fixed three-coset base may yield an improved upper bound or a restricted
optimum. Such an optimum is not a lower bound for arbitrary covering codes.
Global equality requires an unrestricted lower-bound proof matching a
verified construction. A numerical solver status, search timeout or absence
of a better code does not supply that proof.

No paid infrastructure was used; this agent's incremental infrastructure
spend is $0. All evidence hashes and machine results are in `lower-audit.json`.

## Independent fixed-base kernel audit

`audit_fixed_base.py` checks the root agent's `global/analyze_kernel.py`
producer and its binary data without sharing its Hamming-error enumeration.
It recomputes the kernel using literal distances between all 117649 quotient
representatives and all 343 span words (40353607 pairs). It derives the
three cosets from the actual first 1029 words without using coset metadata;
reconstructs all 9261 exceptional points; checks that each is indeed at
minimum distance five from the actual base; and directly checks hole-set
invariance under each of the 343 span translations.

The entire 117649-entry center-coverage array is recomputed from this independent
kernel. Two hundred seeded arbitrary ambient centers, plus the maximizing
center, also pass literal distance-to-all-holes cross-checks. Binary data
hashes, producer script hash, JSON hash and original code hash are recorded.

Every arbitrary additional center covers at most 68 of these 9261 holes.
Therefore any completion **retaining the original 1029-word base** needs
at least `ceil(9261/68)=137` additional words, for total at least **1166**.
The witness center `000314403` covers exactly 68 holes. This is a valid counting
lower bound for the fixed-base architecture, not for unrestricted `K_7(9,4)`.
It does not assume patch centers are drawn from the original322-word patch.
Any stronger exact weighted dual supplied later must be audited separately.

### Stronger exact weighted fixed-base dual: 1182

The same independent literal-Hamming kernel checks the later weighted
certificate `global/dual-certificate.json`: its 27 nonnegative rational
weights match the exact hole-orbit order, and every one of the 117649
quotient-center constraints is checked in integer arithmetic. Because the
holes are invariant under all span translations, these constraints cover
all 40353607 ambient centers, not only the original patch candidates.

Assign each point of orbit i the weight lambda_i. Any additional codeword
covers weight at most one. Thus any patch has cardinality at least
`343 * sum(lambda_i) = 76217001/500000 = 152.434002`, implying at least
153 added words, and fixed-base total at least **1182**. This improves the
simple fixed-base counting bound1166; it is still not a global lower bound
on K_7(9,4).

`fixed-base-dual-audit.json` records the independently recomputed constraints,
exact maximum load/slack, certificate hash and five rejected forgeries:
negative weights, zero denominators, swapped orbit order, doubled infeasible
weights and an inflated integer bound claim. No numerical solver output is
trusted by this replay; no solver is required to run the checker.

## Bounded attempt to reproduce264 without original C++

The missing original implementation is not a logical obstruction: the paper's
recurrences can be reimplemented. `game_replay.py` does so from Lemmas15/16 and
Theorem9, with exact game states `(d,c0,c1,c2,c3,c4)`, where c_j counts rows
matched exactly j times so far. A next partition class is a profile b_j with
`0<=b_j<=c_j` and total at least m. Selecting a class with b4>0 immediately
loses; otherwise it sends counts to `c'_j=c_j-b_j+b_(j-1)`.
The partition player wins exactly when these rows admit q classes all losing
for the transversal player. The checker enumerates these partitions with
nondecreasing class-profile indices, removing only permutation symmetry.

The Theorem9 loop starts m=0, determines a winning interval of first-selected
class sizes by Lemma8, and raises the minimum class size to the end of that
interval plus one. A successful winning chain would prove global264, without
assuming any particular code or fixed base. A timeout gives UNKNOWN.

Independent tiny tests enumerate the actual q^M labeled partitions, retaining
row identities. Eighty cases with q2/3, n2..4 and M0..4 agree with the histogram
algorithm. They also agree after adding HHSP Lemma11, the immediate danger-row
pigeonhole test and a sound conditional-expectation pruning certificate.
The latter assigns each row the exact probability that a Binomial(n-d,1/q)
number of later matches will reach k; if the total is below one, selecting a
class no worse than the conditional mean maintains that property until the
terminal integer bad-row count is zero.

For M263,k5 the unpruned histogram space contains `binomial(267,4)=207029130`
possible profiles before depth or danger restrictions. Each profile's losing
partition subproblem additionally combines q7 class profiles. Avoiding the
full space requires compressed losing/winning frontiers and minimum-convolution
pruning such as the paper's Section4. The bounded reference replay is intended
to identify this actual computational obstacle, not to replace the paper's
numerical claim with unexecuted assertions.

Actual baseline measurement: 120.000 seconds, 276554 states, 105964141 class profiles, 2099 partition subproblems; UNKNOWN_BUDGET_EXCEEDED before closing the m=0 game.

Actual pruned measurement: 60.0002739890042 seconds, 32417 states, 129523 class profiles, 1221 partition subproblems; UNKNOWN_BUDGET_EXCEEDED. No Theorem9 chain completed and no 264 replay claim is made.
