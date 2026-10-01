# Covering-codes research status — 2026-10-01

## Principal target

`K_7(9,4) <= 1351` is a **candidate**, not yet a repository-backed theorem.

Current literature check:
- Marosi, arXiv:2608.19872v3 (2 Sep 2026), reports `K_7(9,4) <= 1475`.
- If the 1351-word code is independently validated, it improves that construction by 124 codewords (8.41%).

Blocking item: the actual 1351-word `pp1_*` output/certificate is not present in the connected GitHub repository. It must be copied from the machine/run that produced it; it must not be regenerated from memory.

## Verified current comparison points used in the draft

- `K_4(10,4) >= 62` and prior UB `208` (Gijswijt–Polak/current tables).
- `K_5(7,2) >= 236`, prior valid UB `525`; historical `500` claim requires special wording.
- `K_5(9,3) >= 354`, prior UB `1275`.
- `K_5(10,4) >= 177`, prior UB `875`.
- `K_7(8,3) >= 471` in Marosi v3.

## Formalization strategy

Do not reinvent covering-code foundations. Use Florath's proof-carrying Lean 4 artifact at fixed commit `460df105545c2d6b04ba71f29de6b56dbda92825` and add instance-specific explicit certificates.

Validity and novelty remain separate:
- Lean/exhaustive checking establishes **validity**.
- literature review establishes **novelty**.

## Local-build status

Executed on 2026-10-01 with Lean `v4.30.0-rc2`, Florath
`460df105545c2d6b04ba71f29de6b56dbda92825`, and the Mathlib cache for
`d9694e37437f9a5cb6f81f8b25c4c754b398e213`.

`lake build CoveringRecords.Candidate CoveringRecords.HammingSphere` — **PASS**.
No `sorry`, no `admit`, no `native_decide`.

`#print axioms` for `hammingSphere_q7_n9_r4` and `sphereLower_q7_n9_r4`:
`propext`, `Classical.choice`, `Quot.sound`. `Classical.choice` comes from
Mathlib's Hamming distance, which this layer imports on purpose.

## Hamming sphere bound — proved

`CoveringRecords.hammingSphere_q7_n9_r4`:

`QaryKLower 7 9 4 221`

That is `K_7(9,4) ≥ 221`, the classical sphere-covering (Hamming-ball) bound.
`sphereLower 7 9 4` reduces by kernel `decide` to `221`
(`V_7(9,4) = 182791`, `7^9 = 40353607`, `220 * 182791 = 40214020 < 7^9`).

## Still not a theorem

`K_7(9,4) ≤ 1351` is **not** asserted. `principalClaim_of_explicit` only
bridges an `ExplicitQaryUpper 7 9 4 1351` witness, and that witness is not in
the repository. It was not reconstructed.
