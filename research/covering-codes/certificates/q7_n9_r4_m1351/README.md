# K_7(9,4) <= 1351

COMPUTATIONALLY_VERIFIED: A/B independently cover the entire universe, with 1351 unique words. Lean coverage replay is incomplete. See provenance.md, SHA256SUMS and verification JSON. Novelty is separate; see ../../literature.md.

The concurrent research-branch commit `f5129539417d55e4a91303a5f7fb0f7d7d06b7de` adds the classical sphere lower bound `QaryKLower 7 9 4 221`; its source is preserved and included in the actual final build. This is separate from principal upper-bound coverage and from the stronger computationally rechecked LB 241.

Both a full-space packed witness (80707214 uncompressed bytes) and a compact orbit partition (253820 bytes) are externally checked. The latter uses 117649 representative witnesses and 9261 direct exceptions. Neither has Lean coverage replay yet. See ../../certificate-design.md.
