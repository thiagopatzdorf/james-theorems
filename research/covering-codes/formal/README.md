# Covering-code record certificates (Lean 4)

This is a **separate pinned Lean project** for record-candidate certificates. It intentionally does not modify the root `james-theorems` toolchain.

It depends on Andreas Florath's `covering-codes-lean` at commit:

`460df105545c2d6b04ba71f29de6b56dbda92825`

The upstream artifact defines `QaryKUpper q n r U` and `ExplicitQaryUpper q n r U`.
The local file `CoveringRecords/Candidate.lean` currently formalizes only the *shape* of the target claims and the bridge:

```lean
theorem principalClaim_of_explicit
    (E : ExplicitQaryUpper 7 9 4 1351) : QaryKUpper 7 9 4 1351
```

## What is proved

`CoveringRecords/HammingSphere.lean` proves the sphere-covering bound on the
principal parameters, by replaying Florath's `sphereLower_valid`:

```lean
theorem hammingSphere_q7_n9_r4 : QaryKLower 7 9 4 221
```

`sphereLower 7 9 4 = 221` is kernel `decide`, not `native_decide`.

## What is not proved

It does **not** claim `K_7(9,4) <= 1351` yet. That statement becomes formally certified only after the canonical 1351-word construction and a checked coverage certificate are ingested.

## Build

```bash
lake update
lake build
```

## Promotion rule

Do not add a theorem named `q7_n9_r4_m1351` until:

1. `certificates/q7_n9_r4_m1351/code.txt` exists;
2. its SHA-256 is frozen;
3. two independent exhaustive verifiers agree on `uncovered = 0`;
4. the Lean certificate is generated for exactly those bytes;
5. the project builds with no `sorry` or `admit`.

`lake build CoveringRecords.Candidate CoveringRecords.HammingSphere` passed on 2026-10-01 (Lean v4.30.0-rc2). That build does not include a 1351-word witness.
