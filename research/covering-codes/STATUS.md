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

The adapter source contains no `sorry` or `admit`, but the current ChatGPT runtime does not have `lake` installed. Therefore the Lean build is **NOT EXECUTED**, not PASS.
