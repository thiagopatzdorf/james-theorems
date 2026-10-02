#!/usr/bin/env python3
"""Independent scalar-distance replay of every provided private witness."""
import hashlib,json
from pathlib import Path
OUT=Path(__file__).resolve().parent;ROOT=OUT.parents[2];D=ROOT/'certificates/q7_n9_r4_m1344'
raw=(D/'code.txt').read_bytes();code=raw.decode('ascii').splitlines();result=json.loads((OUT/'coverage-counts.json').read_text())
assert len(code)==1344 and len(set(code))==1344
assert raw.endswith(b'\n') and b'\r' not in raw and all(len(w)==9 and all(c in '0123456' for c in w) for w in code)
assert result['M']==1344 and result['ambient_words']==7**9 and result['ball_volume']==182791 and result['sum_coverage_multiplicities']==1344*182791
assert result['uncovered']==0
assert sorted(r['index'] for r in result['words'])==list(range(1344))
checked=0;removable=[]
for row in result['words']:
 j=row['index'];w=row['first_private']
 if row['private_points']==0:
  assert w is None;removable.append(j);continue
 assert len(w)==9 and all(c in '0123456' for c in w)
 covered=[i for i,c in enumerate(code) if sum(x!=y for x,y in zip(w,c))<=4]
 assert covered==[j],(j,covered)
 checked+=1
check=dict(status='PASS',source_sha256=hashlib.sha256(raw).hexdigest(),private_witnesses_checked=checked,removable_word_indices=removable,global_optimality_claimed=False,exhaustive_ball_audit_used_for_zero_private_claim=True)
if removable:
 # Delete exactly one: simultaneous deletion of multiple zero-private words is not justified.
 j=removable[0];payload=('\n'.join(code[:j]+code[j+1:])+'\n').encode();name='candidate-m1343.txt';(OUT/name).write_bytes(payload);check.update(candidate_file=name,candidate_sha256=hashlib.sha256(payload).hexdigest(),deleted_original_index=j,requires_full_verifier_replay=True)
(OUT/'private-certificate-check.json').write_text(json.dumps(check,indent=2)+'\n');print(json.dumps(check))
