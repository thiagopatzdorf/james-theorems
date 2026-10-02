# Audit preprint

`paper.tex` / `paper.pdf`: six-page technical draft, actual computational results
for all eight recovered codes. `make paper` from root regenerates the exact-bound
table and PDF (requires pdflatex).

Latest principal claim: computationally verified construction with 1344 unique words,
exact radius 4. It improves the verified 1475 bound found in this audit. Principal
Lean coverage replay is incomplete, and global novelty is not established.

No AI-discovery, optimality or world-record claim. Published documentary lower
bounds are distinct from independently rechecked ones; alpha is an interval.

The concurrent research-branch commit `f5129539417d55e4a91303a5f7fb0f7d7d06b7de` adds the classical sphere lower bound `QaryKLower 7 9 4 221`; its source is preserved and included in the actual final build. This is separate from principal upper-bound coverage and from the stronger computationally rechecked LB 241.

The paper target fixes SOURCE_DATE_EPOCH for reproducible PDF metadata; two consecutive builds produced identical bytes with the same TeX distribution. Scoped Git attributes enforce LF for canonical text and preserve binary/original-source archives exactly.

The original1351 remains preserved. The bounded follow-up obtains1344 by keeping
its1029-word base and substituting315patchwords, with fresh full-space A/B and
compact-certificate checks. Seed/iteration replay reproduces identical bytes.
No exactvalue or globaloptimality is claimed. See experiments/exact-q7/REPORT.md.
