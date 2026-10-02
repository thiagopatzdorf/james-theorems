#!/usr/bin/env python3
"""Finite deterministic radius-one expansion; no global optimality claim."""
import hashlib,json,os,time
os.environ['OPENBLAS_NUM_THREADS']='1'
from pathlib import Path
import numpy as np
from scipy.optimize import milp,linprog,Bounds,LinearConstraint
from scipy.sparse import csc_matrix
OUT=Path(__file__).resolve().parent;ROOT=OUT.parents[2];D=ROOT/'certificates/q7_n9_r4_m1351'
raw=(D/'code.txt').read_bytes();lines=raw.decode().splitlines();code=np.array([list(map(int,w)) for w in lines],dtype=np.uint8)
archive=np.load(OUT/'restricted-cover.npz');ids=archive['hole_ids'];v=ids.copy();holes=np.empty((len(v),9),dtype=np.uint8)
for i in range(8,-1,-1):holes[:,i]=v%7;v//=7
pool=set(lines[1029:])
for w in lines[1029:]:
 for axis in range(9):
  for symbol in '0123456':pool.add(w[:axis]+symbol+w[axis+1:])
base=set(lines[:1029]);pool=sorted(pool-base);candidates=np.array([list(map(int,w)) for w in pool],dtype=np.uint8)
print('pool',len(pool),flush=True);started=time.monotonic();chunks=[]
for lo in range(0,len(pool),128):
 distances=np.zeros((len(holes),len(candidates[lo:lo+128])),dtype=np.uint8)
 for coordinate in range(9):distances+=holes[:,None,coordinate]!=candidates[None,lo:lo+128,coordinate]
 chunks.append(distances<=4)
A=np.concatenate(chunks,axis=1);del chunks;print('literal coverage completed',flush=True)
nonzero=np.flatnonzero(A.any(axis=0));packed=np.packbits(A[:,nonzero].T,axis=1);_,unique=np.unique(packed,axis=0,return_index=True);keep=nonzero[np.sort(unique)];A=A[:,keep];pool=[pool[i] for i in keep]
print('coverage constructed; distinct columns',len(pool),flush=True)
unique_rows=A;sparse=csc_matrix(unique_rows.astype(float));print('LP begin; rows',len(unique_rows),flush=True);lp=linprog(np.ones(len(pool)),A_ub=-sparse,b_ub=-np.ones(len(unique_rows)),bounds=(0,1),method='highs',options={'time_limit':90})
initial=dict(source_sha256=hashlib.sha256(raw).hexdigest(),initial_pool=len(candidates),nonzero_pool=len(nonzero),distinct_coverage_pool=len(pool),holes=len(ids),unique_constraints=len(unique_rows),lp_status=int(lp.status),lp_objective=float(lp.fun) if lp.success else None,preprocessing_seconds=time.monotonic()-started,scope='1029 fixed base + original patch and radius-one neighbors only')
(OUT/'neighbor-initial.json').write_text(json.dumps(initial,indent=2)+'\n');print(json.dumps(initial),flush=True)
if lp.success and lp.fun>321+1e-7:
 result=dict(initial,milp_status='SKIPPED_LP_BOUND',numerical_integer_lower_bound=322,exact_dual_checked=False,improvement_found=False);(OUT/'neighbor-milp-result.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result),flush=True);raise SystemExit(0)
start=time.monotonic();res=milp(c=np.ones(len(pool)),integrality=np.ones(len(pool)),bounds=Bounds(0,1),constraints=LinearConstraint(sparse,np.ones(len(unique_rows)),np.full(len(unique_rows),np.inf)),options={'time_limit':120,'mip_rel_gap':0,'presolve':True})
result=dict(initial,milp_status=int(res.status),milp_message=res.message,runtime_seconds=time.monotonic()-start,mip_gap=float(res.mip_gap) if getattr(res,'mip_gap',None) is not None else None,mip_dual_bound=float(res.mip_dual_bound) if getattr(res,'mip_dual_bound',None) is not None else None)
if res.x is not None:
 chosen=np.flatnonzero(res.x>.5);covered=A[:,chosen].any(axis=1);result.update(patch_size=len(chosen),uncovered_holes=int((~covered).sum()))
 if covered.all() and 1029+len(chosen)<1351:
  patch=[pool[i] for i in chosen];new=lines[:1029]+patch;assert len(new)==len(set(new));payload=('\n'.join(new)+'\n').encode();name=f'neighbor-candidate-m{len(new)}.txt';(OUT/name).write_bytes(payload);result.update(candidate_file=name,candidate_sha256=hashlib.sha256(payload).hexdigest(),chosen_patch=patch)
(OUT/'neighbor-milp-result.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result),flush=True)
