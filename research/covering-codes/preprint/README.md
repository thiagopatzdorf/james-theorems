# Candidate improved upper bounds for q-ary covering codes

**WORKING DRAFT — do not cite the candidate bounds as established until the canonical certificates are ingested.**

## Principal candidate

The working search report gives:

- candidate: `K_7(9,4) <= 1351`
- current verified comparison: Marosi, arXiv:2608.19872v3 (2 Sep 2026), gives `K_7(9,4) <= 1475`
- potential reduction: 124 codewords, or 8.41%
- ambient space: `7^9 = 40,353,607` words

The 1351 result is **not yet promoted** because its canonical `pp1_*` code file is not present in this repository.

## Working candidate table

| q | n | R | candidate UB | checked prior UB | working status |
|---:|---:|---:|---:|---:|---|
| 7 | 9 | 4 | 1351 | 1475 | principal artifact missing |
| 4 | 10 | 4 | 192 | 208 | reported checked; archive pending |
| 5 | 7 | 2 | 500 | 525 | historical 500 claim requires caveat |
| 5 | 9 | 3 | 1250 | 1275 | reported checked; archive pending |
| 5 | 10 | 4 | 625 | 875 | reported checked; archive pending |
| 5 | 9 | 4 | 250 | pending | prior-art audit pending |
| 5 | 9 | 5 | 50 | pending | prior-art audit pending |
| 7 | 8 | 3 | 1893 | pending | prior-art audit pending |

## Verification contract

A candidate becomes an established upper bound in this project only after:

1. the exact code is archived;
2. SHA-256 is frozen;
3. two independent exhaustive verifiers report zero uncovered ambient words;
4. parameters q, n, R and M are audited;
5. novelty is checked separately against current literature;
6. for the principal candidate, the certificate replays in Lean to `QaryKUpper 7 9 4 1351`.

Discovery and verification are deliberately separated. The heuristic generator is untrusted.

## Formal layer

The nested project in `../formal/` pins Andreas Florath's proof-carrying covering-code library at commit:

`460df105545c2d6b04ba71f29de6b56dbda92825`

The upstream library already defines `QaryKUpper`, `ExplicitQaryUpper`, Hamming coverage, and the bridge from an explicit covering certificate to an upper-bound proposition. We therefore add instance certificates instead of re-formalizing the foundations.

Current local runtime limitation: the environment used to prepare this branch has no `lake` executable, so the adapter has not been built here. It is intentionally marked **NOT EXECUTED**, not PASS.

## Literature anchors

- M. Marosi, *New upper and lower bounds on covering codes K_q(n,R) for alphabets of size 5 <= q <= 21*, arXiv:2608.19872v3, 2 Sep 2026.
- D. Gijswijt and S. Polak, *Semidefinite Lower Bounds for Covering Codes*, arXiv:2504.01932.
- A. Florath, *Formal Foundations and Proof-Carrying Certificates for q-ary Covering Codes in Lean 4*, arXiv:2606.09600.
- P. R. J. Ostergard, *New Constructions for q-ary Covering Codes*, Ars Combinatoria 52 (1999), 51–63.

## Draft PDF

A five-page PDF draft has been produced outside the repository for review. The intended paper is a narrow bounds-and-certificates paper, not a broad philosophical paper: explicit constructions, independent verification, formal replay, and prior-art comparison.
