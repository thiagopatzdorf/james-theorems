# Certificate design and trust boundary

The pinned upstream uses proof-carrying **Lean objects** (`UpperCert` / `UpperTrace`),
not a general reader that makes arbitrary external JSON a theorem. `ExplicitQaryUpper`
contains a `Finset (Fin n → Fin q)`, `card_le`, and `CoversFinset`. `toUpper` supplies
the existential witness for `QaryKUpper`. This audit reuses these definitions.

## Selected route

For the tiny fixture, an explicit two-word Finset and `covering_decide +kernel`
are simplest. For the principal instance, the proposed scalable route is a
**selector certificate**: one codeword index for every ambient word. The generic
`covers_of_selector` bridge checks membership and distance; it does not assume
that a suitable selector exists. A principal selector has now been generated and externally validated for every ambient word; its Lean decoder/replay remains incomplete.

Binary payload format: q, n, R, M and code SHA-256 in metadata; an array of
unsigned 16-bit **little-endian** indices in [0,M). Ambient index
`sum(x[i]*q^(n-1-i))` is big-endian base-q packing. Each index selects the codeword
in original canonical line order. For the principal case the payload is
`2*7^9 = 80,707,214` bytes (~76.97 MiB); code.txt is 13,510 bytes. A witness for
each word reduces distance work from N*M*n to N*n. A future chunked Lean replay
must prove decoding, exhaustive partition, index bounds, membership and distance;
an external checker or a SHA declaration alone does not discharge those goals.

Untrusted generation can use nearest-codeword search or propagate a source index
through BFS. The B checker computes exact distances, not a selector file. `tools/witness_certificate.py` propagates indices through a separable min-plus transform and writes deterministic gzip. Its independent streaming validation decodes ambient integers and tests literal Hamming distance; it does not repeat the generating transform.
Hash linkage must include original bytes, canonical bytes, selector payload and
generated Lean source. A flat witness cannot certify minimality of the code size.

## Alternatives and cost

| Design | Cost / risk | Decision |
|---|---|---|
| Direct finite existential decide | 40,353,607 * 1351 distance choices; >490 billion coordinate comparisons in a naive scan | Tiny only |
| Generate all radius-4 balls | 1351 * 182,791 = 246,950,641 generated visits before deduplication | Useful external validation; not yet a Lean replay |
| Selector uint16 | ~77 MiB, ~363 million coordinate checks plus decoding/proof overhead | Real externally validated payload; Lean decoder/chunk replay unimplemented |
| Partition certificate | Potential compression, but requires proof that blocks exhaust space | Potential future compression; original artifact recovered |
| Native decide | Faster compiled evaluation; enlarged trust boundary | May support B-level computational evidence, never silently label kernel-only |
| External JSON says PASS | No Lean proof of coverage | Reject |

`covering_decide` defaults to ordinary `decide`. Its `+kernel` mode forces kernel
reduction **only when the native option is false**: upstream's implementation
uses `kernel := forceKernel && !native`. Therefore explicitly enabling native
mode overrides even `+kernel`. Our project does not enable native mode. Kernel
mode trusts Lean's kernel, standard logical axioms and the stated mathematics;
native mode additionally trusts compiled evaluation/runtime mechanisms, which
must appear in the axiom dependency audit. The compiler, parser and SHA tooling
are outside the mathematical kernel and remain part of artifact linkage.

The pipeline refuses promotion without the principal source/manifest, exact type
checking of an unconditional theorem, hash agreement and a standard-axiom audit.
The generic adapter, tiny theorem, principal Finset definition and cardinality bound can build while principal coverage remains unproved. They are reported separately.

The actual compressed payload, byte lengths and both hashes are recorded in `certificates/q7_n9_r4_m1351/witness-metadata.json`; `certificate-check.json` records external validation. The gzip payload is versioned. A proof-carrying construction requires discharge of selector decoding/membership/coverage inside Lean; neither this JSON nor generic selector lemmas supply that proof.
