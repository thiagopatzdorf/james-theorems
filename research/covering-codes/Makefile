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
	cd preprint && SOURCE_DATE_EPOCH=1790812800 FORCE_SOURCE_DATE=1 pdflatex -interaction=nonstopmode -halt-on-error paper.tex
	cd preprint && SOURCE_DATE_EPOCH=1790812800 FORCE_SOURCE_DATE=1 pdflatex -interaction=nonstopmode -halt-on-error paper.tex

.PHONY: verify-computational verify-all-computational certificate
verify-computational:
	$(PYTHON) tools/verify_case.py q7_n9_r4_m1351 --computational-only
verify-all-computational:
	@for case in q7_n9_r4_m1351 q7_n9_r4_m1346 q7_n9_r4_m1345 q7_n9_r4_m1344 q4_n10_r4_m192 q5_n7_r2_m500 q5_n9_r3_m1250 q5_n10_r4_m625 q5_n9_r4_m250 q5_n9_r5_m50 q7_n8_r3_m1893; do $(PYTHON) tools/verify_case.py $$case --computational-only || exit $$?; done
certificate:
	$(PYTHON) tools/witness_certificate.py certificates/q7_n9_r4_m1351
	$(PYTHON) tools/partition_certificate.py certificates/q7_n9_r4_m1351

.PHONY: exact-q7-audit
# Audit evidence only; optimization and large formal benchmarks remain manual.
exact-q7-audit:
	$(PYTHON) experiments/exact-q7/test_new_certificate.py
	$(PYTHON) experiments/exact-q7/patch/verify_private_certificate.py
	$(PYTHON) experiments/exact-q7/lower/audit_lower.py
	OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 $(PYTHON) experiments/exact-q7/lower/audit_fixed_base.py

.PHONY: verify-q7-9-4-1344 verify-q7-9-4-1344-computational
verify-q7-9-4-1344:
	$(PYTHON) tools/verify_case.py q7_n9_r4_m1344
verify-q7-9-4-1344-computational:
	$(PYTHON) tools/verify_case.py q7_n9_r4_m1344 --computational-only
