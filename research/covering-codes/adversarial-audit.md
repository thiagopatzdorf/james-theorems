# Adversarial audit — 2026-10-01

All eight recovered constructions were checked by both executables. The principal has 1351 parsed/unique words, zero duplicates/invalid lines, 40,353,607 covered words, zero uncovered, exact radius 4. Infrastructure tests compare literal scan, min-plus transform and BFS on all 255 nonempty binary length-3 codes at all four radii, plus seeded other alphabets. The separate published 1475 construction also passes independent replay.

| Attack | Evidence | Result |
|---|---|---|
| Wrong Hamming definition | A counts unequal coordinates; B uses single-coordinate edges; all 255 nonempty binary length-3 codes at four radii agree | PASS infrastructure |
| `<R` instead of `<=R` | Repetition code 000/111 covers eight words at R=1 and fails at R=0; radius-n singleton passes | PASS |
| Truncated / too-long word | Explicit 2- and 4-symbol lines for n=3 in parser tests | Rejected |
| Alphabet out of range | `007` with q=7, BOM, byte 255, NUL and whitespace tested | Rejected |
| Wrong universe | A full tensor (literal itertools scan used as test oracle); B iterates ids 0..q^n-1 and checks queue reaches all vertices for nonempty code | PASS: entire 40,353,607-word principal universe in both checkers |
| Missed enumeration / early exit | A transforms all coordinates without radius truncation; literal oracle has no early radius break; B exhausts graph independent of R | Exact radius, including invalid coverings |
| Overflow | B checks uint32 bound before multiplication, signed int64 neighbour delta, explicit memory guard | q=7,n=32 rejected |
| Duplicates hidden by Finset | Raw parsed and unique sizes reported separately; 000/111/000 test has M=3, unique=2 | PASS |
| Digit endian mismatch | A tuples vs B most-significant-first base-q packing; q=3,4,5,7,10 cross-checks | PASS tested |
| Ball/graph boundary wrap | B alters individual decoded digits; signed neighbour invariant tested | PASS tested |
| Parser normalizes invalid input | Verifiers read exact bytes; CRLF rejected; ingestion alone documents CRLF conversion | PASS |
| Wrong file/hash | Both independent hash implementations agree; pipeline checks metadata and SHA256SUMS | PASS all eight; exact metadata/canonical hash agreement |
| Canonicalization rearranges words | Ingestion tests 111 CRLF 000; original raw bytes archived by hash; differing replacement refused | PASS |
| Old stdout treated as construction | No codewords reconstructed from logs; missing files yield null measurements and nonzero exit | PASS policy |
| Adapter mistaken for principal proof | Conditional bridge has explicit hypothesis; pipeline requires exact unconditional type | No principal theorem asserted |
| `lake build` success with no jobs | Existing library lacked default target; initial success was 0 jobs; default target now explicit | Corrected; real build logged |
| `+kernel` secretly runs native mode | Upstream option reviewed; native option remains false; `#print axioms` is required | Principal replay still unavailable |
| Reference mistaken for candidate | 1475 code stored under literature-artifacts; principal slot contains original 1351, not the 1475 reference | PASS separation |
| Novelty from absence of search hits | Search coverage and access failures recorded; status NOVELTY_UNRESOLVED | No record claim |

Limit: exhaustive cross-checks on small spaces do not prove either executable
correct for all inputs. C++/OpenSSL/Python and operating system execution remain
computational TCB. No ASan/UBSan large-instance claim is made unless its log is
present. Original artifacts now pass all these checks. Generation provenance is partially known, distinct from byte provenance.

## Transform invariant and integer safety

Initialize D(c)=0 at codewords and D(x)=n+1 elsewhere. Processing coordinate i applies
D_new(x)=min(D_old(x),1+min_a D_old(x with coordinate i replaced by a)).
The recurrence is the exact min-plus Hamming transform on that coordinate: the
same-symbol term costs zero and a changed symbol costs one. Coordinate costs
add and the transforms commute; after all n coordinates, D(x)=min_c d_H(x,c).
The n+1 sentinel is above every realizable distance; intermediate values are
at most n+2<=34, so uint8 cannot overflow. Shape (q,)*n has exactly q^n entries.
The independent BFS computes shortest paths in the graph changing one coordinate,
whose distance is Hamming distance. It exhausts its queue regardless of R.
The certificate checker independently decodes every consecutive ambient integer
and checks its chosen original-order codeword, including witness length and hashes.
