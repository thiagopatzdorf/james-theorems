# Exhaustive single-word deletion audit of the 1344 construction

This checks every word, including all 1029 base words. The original construction
is not modified. The C++ checker generates all radius-four balls in GF(7)^9,
counts coverage multiplicities, and scans every one of the 40353607 ambient ids.

Each recursion fixes coordinates in increasing order, either retaining the
center digit or selecting one of six different digits and consuming a radius
unit. Consequently each ambient word in a ball occurs exactly once. Each ball
has 182791 words, and the total multiplicity was checked to be
1344 * 182791 = 245671104. The maximum observed multiplicity is16; uint16 counts
cannot overflow even in the worst case of1344 balls. Owners are uint16 indices.
The two arrays use161414428bytes, below the500MB budget.

Result: uncovered0; **all1344 words have private ambient witnesses**. Private
points per word range from2 to83, totaling53371. Therefore no word can be
removed by itself while leaving the other1343 words unchanged. This is deletion minimality only; it is
**not** global optimality, a lower bound on K, or an obstruction to replacing
multiple words. No smaller candidate was generated.

`check_private_witnesses.py` reads the ball audit and independently verifies all
1344 private witnesses by scalar Hamming-distance comparisons against every
actual codeword. It uses neither C++ ball generation nor NumPy/solver results.
The code hash is recorded in `private-certificate-check.json`.

Actual C++ runtime:5.10141seconds. No external paid infrastructure provisioned.

```sh
g++ -std=c++17 -O3 audit_deletions.cpp -o /tmp/q7-audit-deletions
timeout 90 /tmp/q7-audit-deletions ../../../certificates/q7_n9_r4_m1344/code.txt > coverage-counts.json
python check_private_witnesses.py
```
