# Literature audit — 2026-10-01

Validity, documentary prior art and global novelty are different questions.
The strongest **independently replayed prior upper bound found in this audit** for
K_7(9,4) is 1475. The recovered 1351 construction improves it by 124 words
(8.40678%). Its novelty classification is CANDIDATE_NEW_UPPER_BOUND, not a world
record claim. No accessible primary source at <=1351 was found in the searches
recorded below; that negative search is not a proof of absence.

## Principal primary source and replay

Márk Marosi, *New upper and lower bounds on covering codes K_q(n,R) for alphabets
of size 5 <= q <= 21*, [arXiv:2608.19872v3](https://arxiv.org/abs/2608.19872v3),
2 September 2026. The current arXiv listing checked on the audit date lists v3
as latest. Read the v3 article/source, its 26-code ancillary archive, standalone
checkers, rational dual certificates and public [Mapika/coldcase](https://github.com/Mapika/coldcase)
repository at 56a8cce68ec3f6f406c845f5cc3e51711e5b8294. Table 1 explicitly reports
K_7(9,4)<=1475, compared to 1843; its lower bound 264 is documentary evidence.

`literature-artifacts/marosi-v3/code-1475.txt` has SHA-256
`b3e6054913d7c0407546c82e0bf9755ad10a4fe9e0c2f68ab10a2cc707ac6ace`.
The independent BFS visits all 40,353,607 vertices and obtains exact radius 4.
The author's independent coordinate-dilation checker also reports complete
radius-4 coverage, with only 22,114,512 covered at radius 3. Logs are archived.
The 1475 bound is therefore computationally replayed, not accepted from a table.

## Backward and forward paths

Read the following primary texts or tables (not just search snippets):

* Dion Gijswijt and Sven Polak, *Semidefinite lower bounds for covering codes*,
  [arXiv:2504.01932v2](https://arxiv.org/abs/2504.01932v2), June 2026: the SDP
  theorem and tables, including stronger small-alphabet numerical lower bounds.
  The local source snapshot is `literature-artifacts/gijswijt-v2/`.
* Gerzson Kéri, [Tables for bounds on covering codes](https://old.sztaki.hu/~keri/codes/index.htm),
  tables revised November 2011: original quaternary/quinary and q=6..21 PDFs,
  their source keys and update notes. Extracted texts are archived.
* P. R. J. Östergård, *New constructions for q-ary covering codes*, Ars
  Combinatoria 52 (1999), 51–63: original scanned article. Page 12 OCR shows
  K_5(7,2)<=525 and an explicit construction, not a verified 500 statement.
  The initial draft's unspecified historical-500 caveat is not supported by
  an identified primary source in this audit; neither its validity nor its
  withdrawal is asserted.
* Kéri–Östergård (2005), Bhandari–Durairajan (1996), and
  Haas–Halupczok–Schlage-Puchta (2009) were followed through their citations,
  source keys and accessible bibliographic records. Their full construction
  proofs were not independently replayed. The source-key `m` in the Kéri
  **upper-bound** legend means Östergård 1991; it means Haas et al. 2009 in the
  **lower-bound** legend. A mirror that conflates those keys is not primary.
* Andreas Florath, [arXiv:2606.09600](https://arxiv.org/abs/2606.09600), and the
  pinned `covering-codes-lean` source: formal definitions, explicit-code interface,
  proof mode and certificates were inspected. This source supports the proof
  infrastructure, not novelty of the recovered cases.

Forward/current searches for Marosi, its arXiv ID, the exact K_7(9,4) cell,
1351/1475, and all secondary cardinalities were made through Exa and Crossref.
They returned Marosi/Kéri and older covering literature, without an accessible
primary <=1351 claim. Search responses are archived as `search-lit*.json`.
Crossref returned HTTP 200; Google Scholar returned 429, zbMATH and MathSciNet
403. These are real access limits, recorded in `bibliographic-access.json`;
there is no claim to a complete forward-citation graph or subscription search.

## Bounds by case and evidence level

| Case | Published LB | Published prior UB | Independently rechecked LB | Replayed prior UB | Our verified UB | Novelty |
|---|---:|---:|---:|---:|---:|---|
| K_7(9,4) | 264 | 1475 (Marosi v3) | 241 | 1475 | 1351 | CANDIDATE_NEW_UPPER_BOUND |
| K_4(10,4) | 62 | 208 (Kéri / Östergård 1999) | 51 | — | 192 | NOVELTY_UNRESOLVED |
| K_5(7,2) | 236 | 525 (Kéri / Östergård 1999) | 236 | — | 500 | NOVELTY_UNRESOLVED |
| K_5(9,3) | 354 | 1275 (Kéri / Bhandari–Durairajan) | 354 | — | 1250 | NOVELTY_UNRESOLVED |
| K_5(10,4) | 177 | 875 (Kéri / Bhandari–Durairajan) | 158 | — | 625 | NOVELTY_UNRESOLVED |
| K_5(9,4) | 64 | 255 (Kéri / Bhandari–Durairajan) | 62 | — | 250 | NOVELTY_UNRESOLVED |
| K_5(9,5) | 19 | 55 (Kéri / Bhandari–Durairajan) | 16 | — | 50 | NOVELTY_UNRESOLVED |
| K_7(8,3) | 471 | 2337 (Kéri) | 471 | — | 1893 | NOVELTY_UNRESOLVED |

The six archived rational certificates were validated by the standalone exact
`Fraction` checker (`certify.py`); no SDP optimizer was trusted or rerun. This
also checks the certificate arithmetic against the reconstructed constraints,
but is not a Lean proof of the SDP theorem. In particular its q7,n9,R4 bound is
241, weaker than the published 264. Do not silently relabel the latter as a
replayed certificate. For q4,n10 and q5,n10 only the elementary sphere bound was
rechecked. The generated table conservatively uses these independently rechecked
lower bounds and reports stronger published values in separate fields.

Secondary previous constructions were not exhaustively replayed here, so their
values are documentary prior UBs, not `prior_verified_upper_bound` measurements.
All eight **our** constructions were exhaustively replayed. Search for linear
covering-code/saturating-set literature was included, especially the five-ary
[10,4] case; absence of a same-size result in this search leaves secondary
novelty unresolved. No code is declared KNOWN_RESULT without identified evidence.

Machine-readable records with value, authors, date, version, source classification,
explicit-code availability and verification level are in `literature.json`.
