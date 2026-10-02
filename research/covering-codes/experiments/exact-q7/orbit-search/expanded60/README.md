# Expanded quotient-center pool

This follow-up starts from the preserved1346-word candidate, leaving the original1351 object unchanged. It includes every343-word translate of every quotient class that covers at least60 of the9261 fixed-base holes, together with the original322 patch centers.

One thread, no paid resources, seed70941346,180-second search cap after preprocessing. Moves remove4 through24 current patch centers and greedily repair uncovered holes; equally sized feasible solutions are accepted to diversify. Every strict improvement is saved as its own code file and SHA-256 recorded. All checks here are literal distances on the9261 holes; independent full-space verification remains mandatory.

For iteration-based reproduction, run `python ../expanded60-search.py --iterations N` with N from result.json, using the same NumPy/Python versions and unchanged input files. Run from the repository root using the full script path; output is placed beside this README. Timing changes may change how many iterations a time-limited run completes.

Neither failure to improve nor a restricted-pool optimum would prove the exact global covering number.
