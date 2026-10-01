PYTHON ?= python3
.PHONY: fast formal verify-q7-9-4-1351 paper tables
fast:
	$(PYTHON) -m unittest discover -s tests -v
	$(PYTHON) tools/generate_table.py --check
	cd fixtures/q2_n3_r1 && sha256sum --check SHA256SUMS
formal:
	cd formal && MATHLIB_NO_CACHE_ON_UPDATE=1 lake update && lake build && lake env lean Audit.lean
verify-q7-9-4-1351:
	$(PYTHON) tools/verify_case.py q7_n9_r4_m1351
tables:
	$(PYTHON) tools/generate_table.py
paper: tables
	cd preprint && pdflatex -interaction=nonstopmode -halt-on-error paper.tex
	cd preprint && pdflatex -interaction=nonstopmode -halt-on-error paper.tex

.PHONY: verify-computational verify-all-computational certificate
verify-computational:
	$(PYTHON) tools/verify_case.py q7_n9_r4_m1351 --computational-only
verify-all-computational:
	@for case in q7_n9_r4_m1351 q4_n10_r4_m192 q5_n7_r2_m500 q5_n9_r3_m1250 q5_n10_r4_m625 q5_n9_r4_m250 q5_n9_r5_m50 q7_n8_r3_m1893; do $(PYTHON) tools/verify_case.py $$case --computational-only || exit $$?; done
certificate:
	$(PYTHON) tools/witness_certificate.py certificates/q7_n9_r4_m1351
