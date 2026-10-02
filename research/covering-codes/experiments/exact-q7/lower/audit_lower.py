#!/usr/bin/env python3
"""Recheck existing exact-rational lower bound; do not elevate printed claims."""
from pathlib import Path
from fractions import Fraction
from math import comb
import importlib.util
import hashlib
import json
import time

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
SRC = ROOT / 'literature-artifacts/marosi-v3'

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def main():
    start = time.perf_counter()
    spec = importlib.util.spec_from_file_location('covering_dual_checker', SRC / 'certify.py')
    checker = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(checker)
    path = SRC / 'cert_q7_n9_R4.json'
    cert = json.loads(path.read_text())
    assert cert['problem']['q'] == 7 and cert['problem']['n'] == 9 and cert['problem']['R'] == 4
    model = checker.build_model(7, 9, 4, lam=cert['problem']['lambda'], beta=cert['problem']['beta'])
    den = int(cert['den'])
    lin = [int(x) for x in cert['dual_lin']]
    psd = [[[int(x) for x in row] for row in block] for block in cert['dual_psd']]
    res = checker.evaluate_certificate(model, den, lin, psd)
    assert res['ok'] and res['K_lower_bound'] == 241
    num = res['bound_num']
    # This independently checks the actual integer implication K^3 >= num/den.
    assert 240**3 * den < num <= 241**3 * den
    assert cert['claim']['K_lower_bound'] == res['K_lower_bound']
    badlin = lin.copy(); badlin[0] = -1
    assert not checker.evaluate_certificate(model, den, badlin, psd)['ok']
    assert not checker.evaluate_certificate(model, 0, lin, psd)['ok']
    badpsd = [[row.copy() for row in block] for block in psd]
    badpsd[0][0][0] = -1
    assert not checker.evaluate_certificate(model, den, lin, badpsd)['ok']
    assert not checker.check_lambda_beta_valid(9, 4, [1,1,1,1,0,0,0,0,0,0], 1)[0]
    assert not checker.is_psd_exact([[1, 2], [2, 1]])[0]
    assert not checker.is_psd_exact([[0, 1], [1, 1]])[0]
    assert not checker.is_psd_exact([[1, 0], [1, 1]])[0]
    assert checker.is_psd_exact([[1, 1], [1, 1]])[0]
    ambient = 7**9
    volume = sum(comb(9, i) * 6**i for i in range(5))
    sphere = (ambient + volume - 1) // volume
    assert ambient == 40353607 and volume == 182791 and sphere == 221
    pdf = HERE / 'haas-halupczok-schlage-puchta-2009.pdf'
    text = HERE / 'haas-halupczok-schlage-puchta-2009.txt'
    row = next(line.strip() for line in text.read_text().splitlines() if 'K7 (9, 4)' in line)
    assert row.split()[-2] == '264'
    output = {
        'q': 7, 'n': 9, 'R': 4,
        'ambient_words': ambient, 'sphere_volume': volume,
        'sphere_bound': sphere, 'sphere_ratio': str(Fraction(ambient, volume)),
        'rechecked_sdp_lower_bound': 241,
        'rational_bound_on_K_cubed': {'numerator': str(num), 'denominator': str(den)},
        'integer_boundary_checks': {'240_cubed_den_lt_num': True, 'num_le_241_cubed_den': True},
        'exact_sdp_check': res,
        'model_size': {'variables': model.nvars, 'linear_constraints': len(model.lin), 'psd_blocks': len(model.psd)},
        'negative_tests_passed': ['negative_linear_multiplier', 'zero_denominator', 'negative_psd_pivot', 'unsound_covering_inequality', 'indefinite_matrix', 'zero_pivot_nonzero_offdiagonal', 'asymmetric_matrix'],
        'positive_test_passed': 'rank_one_singular_psd',
        'certificate_sha256': sha(path), 'checker_sha256': sha(SRC / 'certify.py'),
        'primary_documentary_lower_bound': 264,
        'primary_source': {'doi': '10.37236/222', 'authors': ['Wolfgang Haas', 'Immanuel Halupczok', 'Jan-Christoph Schlage-Puchta'], 'published': '2009-11-07', 'table': 5, 'printed_row': row, 'pdf_sha256': sha(pdf), 'pdf_bytes': pdf.stat().st_size, 'download_url': 'https://www.combinatorics.org/ojs/index.php/eljc/article/download/v16i1r133/pdf'},
        '264_independently_replayed': False,
        '264_blocker': 'No machine-readable winning-game certificate in retrieved paper. An independent exact histogram recursion passed80tinycrosschecks but bounded local target replay did not complete; see game-replay.json and README. Original C++ is not logically necessary, but compressed frontier/min-convolution machinery is not yet implemented.',
        'global_exact_value_established': False,
        'new_lower_bound_found': False,
        'scope': 'Exact arithmetic checks SDP dual against reconstructed upstream model; soundness additionally relies on Gijswijt–Polak Theorem4.18 and correctness of model transcription. Not a Lean lower-bound replay.',
        'runtime_seconds': time.perf_counter() - start,
        'paid_infrastructure_spend_usd': 0
    }
    (HERE / 'lower-audit.json').write_text(json.dumps(output, indent=2) + '\n')
    print(json.dumps({'status':'PASS', 'rechecked_lower':241, 'primary_documentary_lower':264, '264_independently_replayed':False, 'new_lower_bound_found':False, 'runtime_seconds':output['runtime_seconds']}))

if __name__ == '__main__':
    main()
