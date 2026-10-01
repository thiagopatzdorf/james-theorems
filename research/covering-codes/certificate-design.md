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

## Selected compact partition route (actual object, not a plan)

The original prefix of 1029 words is exactly three full cosets of the span over
Z/7Z of the three generator rows recorded in `audit/principal-structure.json`.
The span contains 343 words; projection to the first three coordinates is bijective.
Normalized representatives are 000000000, 000401620, 000622001. Their tail values
in the **old least-significant-first convention** are 0,6913,16925, exactly the
reported syndrome set. Our certificate uses most-significant-first ambient order.
The 322 remaining original words are preserved as the patch, with no new search.

Let L be this span and C0 the union of its three cosets. Coordinate-wise modular
translation is a Hamming isometry. C0+L=C0. Every ambient word x has exactly one
l in L whose first three coordinates equal those of x; hence r=x-l has prefix
000, and there are 7^6=117649 such representatives. A witness c in C0 for r
transports to c+l in C0 for x, with the same Hamming distance. A marked exceptional
representative instead requires direct witnesses for all 343 words in its orbit.
This gives an exhaustive disjoint partition of the entire space, independent of
the generator's search method. Closure follows from linear-span addition in Z/7Z,
not from trusting a heuristic. The checker confirms the actual complete cosets
against the frozen original file and confirms the prefix projection bijection.

The base alone leaves 9261 points, exactly 27 complete orbits, uncovered at R=4.
The **real compact certificate** consists of:

* `quotient.u16le`: 117649 uint16 indices, 235298 bytes. Each selects one of the
  first 1029 original codewords for its prefix-zero representative, or 65535 marks
  an exceptional orbit. The six remaining coordinates are big-endian base-7.
* `exceptions.u16le`: 9261 uint16 indices, 18522 bytes. These select any of the
  1351 original codewords for exceptional ambient words, in ascending ambient id.
  Those ids are regenerated from the marked representatives and L, not assumed.
* `partition-metadata.json`: generator/coset data, exact format/counts, original
  code hash, individual payload hashes and hash of quotient||exceptions.

Total payload: **253820 bytes**, compared to 80707214 bytes for the flat witness.
Generation computes literal nearest-base distances for all representatives and
reuses already checked full witnesses for the 9261 exceptions. Validation checks
all representative and exception witnesses, exact counts, hashes and structure;
40,344,346 ambient points are covered by the symmetry argument and 9261 explicitly.
The original flat witness remains preserved as a separate full-space certificate.

`partition-check.json` records PASS externally. Neither certificate is a Lean
coverage proof yet. The compact route is now preferred for future Lean replay:
prove the modular-translation isometry, normalization/partition and coset
membership once, then reflect about 1.14 million coordinate comparisons rather
than 363 million, plus original code linkage. The binary decoder and those
instance-specific proof obligations remain unimplemented. The generic upstream
selector bridge and actual principal cardinality proof are already built.
No new covering-code foundations are required; arithmetic/membership derivations
must be kernel checked, not imported as true JSON. External TCB includes Python,
NumPy and the mathematical implementation of the partition; the future Lean TCB
must be separately audited. Native evaluation remains disabled in the formal layer.
