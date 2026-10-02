# Bounded fixed-base search

No change to the original 1351 construction. This experiment preserves its first1029 words and searches for a smaller patch covering the independently verified9261 holes. Pool: all343 linear-span translates of each of29 quotient classes covering at least61 holes, plus the original322 patch words (9947 distinct candidates).

`search.py` constructs literal Hamming incidences, tries12 seeded greedy variants, then bounds SciPy/HiGHS integer set cover to110 seconds and one thread. `repair.py` uses seeded destroy-and-repair moves for55 seconds. Scripts regenerate their matrix in about3 seconds. The original322-word feasible patch is retained unless a literal-hole-checked improvement is found; any improvement still requires independent full-space verification.

A solver dual bound here only pertains to this restricted pool, not arbitrary centers and not K7(9,4). Timeouts and lack of improvements establish no optimality. No paid resources were used.
