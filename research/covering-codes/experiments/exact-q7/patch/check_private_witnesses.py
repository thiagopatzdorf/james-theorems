#!/usr/bin/env python3
"""Solver-independent impossibility of deleting any original patch word."""
import hashlib,json
from pathlib import Path
import numpy as np
OUT=Path(__file__).resolve().parent
ROOT=OUT.parents[2]
D=ROOT/'certificates/q7_n9_r4_m1351'
raw=(D/'code.txt').read_bytes();code=np.array([list(map(int,w)) for w in raw.decode().splitlines()],dtype=np.uint8)
archive=np.load(OUT/'restricted-cover.npz');A=archive['coverage'];ids=archive['hole_ids'];counts=A.sum(axis=1)
rows=[]
for j in range(322):
 matches=np.flatnonzero((counts==1)&A[:,j]);assert len(matches)>0
 ambient_id=int(ids[matches[0]]);k=ambient_id;word=[]
 for _ in range(9):word.append(k%7);k//=7
 word=np.array(word[::-1],dtype=np.uint8)
 distances=np.count_nonzero(code!=word,axis=1);cover=np.flatnonzero(distances<=4)
 assert cover.tolist()==[1029+j]
 rows.append(dict(original_code_index=1029+j,ambient_id=ambient_id,word=''.join(map(str,word)),distance=int(distances[1029+j]),other_codewords_min_distance=int(np.min(np.delete(distances,1029+j))),private_holes_in_exception_set=int(len(matches))))
result=dict(status='PASS',scope='Original code deletion only: not arbitrary replacement or global lower bound',source_sha256=hashlib.sha256(raw).hexdigest(),private_witnesses=rows,restricted_optimal_patch_size=322)
(OUT/'private-witnesses.json').write_text(json.dumps(result,indent=2)+'\n');print('PASS: 322 private witnesses checked against all1351 codewords by literal Hamming distance.')
