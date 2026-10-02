# Research targets delegate to the separately pinned covering-code project.
.PHONY: verify-q7-9-4-1351 verify-computational verify-all-computational covering-fast covering-formal paper
verify-q7-9-4-1351 verify-computational verify-all-computational paper:
	$(MAKE) -C research/covering-codes $@
covering-fast:
	$(MAKE) -C research/covering-codes fast
covering-formal:
	$(MAKE) -C research/covering-codes formal

.PHONY: exact-q7-audit
exact-q7-audit:
	$(MAKE) -C research/covering-codes exact-q7-audit

.PHONY: verify-q7-9-4-1344 verify-q7-9-4-1344-computational
verify-q7-9-4-1344 verify-q7-9-4-1344-computational:
	$(MAKE) -C research/covering-codes $@
