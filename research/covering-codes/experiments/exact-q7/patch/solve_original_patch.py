#!/usr/bin/env python3
"""Solve set cover restricted to 322 original patch words, keeping 1029 fixed."""
import hashlib,importlib.util,itertools,json,time
from pathlib import Path
import numpy as np
from scipy.optimize import milp,linprog,Bounds,LinearConstraint
from scipy.sparse import csc_matrix
ROOT=Path(__file__).resolve().parents[3]
OUT=Path(__file__).resolve().parent
D=ROOT/'certificates/q7_n9_r4_m1351'
spec=importlib.util.spec_from_file_location('partition',ROOT/'tools/partition_certificate.py');p=importlib.util.module_from_spec(spec);spec.loader.exec_module(p)
raw=(D/'code.txt').read_bytes();code=np.array([list(map(int,w)) for w in raw.decode().splitlines()],dtype=np.uint8)
meta=json.loads((D/'partition-metadata.json').read_text());L=p.structure(code,meta['generator_rows'],meta['coset_representatives'])
q=np.frombuffer((D/'quotient.u16le').read_bytes(),dtype='<u2');ids,holes=p.exceptions(q,L)
A=np.count_nonzero(holes[:,None,:]!=code[None,1029:,:],axis=2)<=4
np.savez_compressed(OUT/'restricted-cover.npz',coverage=A,hole_ids=ids)
counts=A.sum(axis=1);cols=A.sum(axis=0);forced=np.unique(np.nonzero(A[counts==1])[1]);unique_rows=np.unique(A,axis=0)
sparse=csc_matrix(unique_rows.astype(float));lp=linprog(np.ones(322),A_ub=-sparse,b_ub=-np.ones(len(unique_rows)),bounds=(0,1),method='highs')
initial=dict(source_sha256=hashlib.sha256(raw).hexdigest(),holes=len(ids),fixed_base=1029,allowed_patch=322,unique_constraints=len(unique_rows),minimum_choices_per_hole=int(counts.min()),maximum_choices_per_hole=int(counts.max()),forced_patch_indices=forced.tolist(),column_min=int(cols.min()),column_max=int(cols.max()),lp_status=int(lp.status),lp_message=lp.message,lp_objective=float(lp.fun) if lp.success else None,scope='Restricted original-patch subset only; not global K optimality')
(OUT/'initial-analysis.json').write_text(json.dumps(initial,indent=2)+'\n');print(json.dumps(initial),flush=True)
start=time.monotonic();res=milp(c=np.ones(322),integrality=np.ones(322),bounds=Bounds(np.zeros(322),np.ones(322)),constraints=LinearConstraint(sparse,np.ones(len(unique_rows)),np.full(len(unique_rows),np.inf)),options={'time_limit':180,'mip_rel_gap':0,'presolve':True})
result=dict(initial,milp_status=int(res.status),milp_message=res.message,runtime_seconds=time.monotonic()-start,mip_gap=float(res.mip_gap) if getattr(res,'mip_gap',None) is not None else None,mip_dual_bound=float(res.mip_dual_bound) if getattr(res,'mip_dual_bound',None) is not None else None)
if res.x is not None:
 chosen=np.flatnonzero(res.x>.5);covered=A[:,chosen].any(axis=1);result.update(patch_size=len(chosen),uncovered_holes=int((~covered).sum()),original_indices=(chosen+1029).tolist())
 if covered.all():
  new=raw.decode().splitlines()[:1029]+[raw.decode().splitlines()[1029+i] for i in chosen]
  payload=('\n'.join(new)+'\n').encode();result.update(reconstructed_original_sha256=hashlib.sha256(payload).hexdigest(),improvement_found=len(new)<1351)
  if len(new)<1351:
   name=f'candidate-m{len(new)}.txt';(OUT/name).write_bytes(payload);result.update(candidate_file=name,candidate_sha256=hashlib.sha256(payload).hexdigest())
(OUT/'restricted-milp-result.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result),flush=True)
