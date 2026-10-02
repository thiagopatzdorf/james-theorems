# Exhaustive local two-remove/one-add obstruction

The unchanged1344-word candidate has315 patch centers. Every patch center has at least2 private holes (holes covered by exactly that patch center). Any replacement of two patch centers by one must cover all private holes of both removed centers.

Using literal distance-derived sparse incidences, `local2swap.py` checked all21266 centers in the expanded restricted pool. No center covers the complete private-hole sets of two distinct current patch centers: zero pairs pass the necessary private-hole filter, so zero residual-pair literal checks were required. The scan is complete, not timed out.

This excludes only this particular two-remove/one-add move for this fixed base and finite pool. It establishes neither optimality in the pool nor optimality of K7(9,4). No input code is changed. The scan is deterministic (no random seed).
