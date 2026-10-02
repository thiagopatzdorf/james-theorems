#!/usr/bin/env python3
"""Bounded fixed-base set-cover heuristic; cannot certify global optimality."""
import os
for key in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS'):os.environ[key]='1'
import hashlib,json,sys,time
from pathlib import Path
import numpy as np
from scipy.sparse import csr_matrix
from scipy.optimize import milp,Bounds,LinearConstraint
ROOT=Path(__file__).resolve().parents[3];sys.path.insert(0,str(ROOT/'tools'))
from partition_certificate import ROWS,representatives,structure,exceptions,word_ids
start=time.monotonic();folder=Path(__file__).parent;d=ROOT/'certificates/q7_n9_r4_m1351';raw=(d/'code.txt').read_bytes();code=np.array([[int(c) for c in w]for w in raw.decode().splitlines()],dtype=np.uint8)
meta=json.loads((d/'partition-metadata.json').read_text());L=structure(code,ROWS,meta['coset_representatives']);q=np.frombuffer((d/'quotient.u16le').read_bytes(),dtype='<u2');_,holes=exceptions(q,L)
coverage=np.frombuffer((ROOT/'experiments/exact-q7/global/center-coverage.u16le').read_bytes(),dtype='<u2');reps=representatives()[coverage>=61]
centers=((reps[:,None,:].astype(np.int16)+L[None,:,:])%7).astype(np.uint8).reshape(-1,9)
centers=np.vstack((centers,code[1029:]));ids=word_ids(centers);_,first=np.unique(ids,return_index=True);centers=centers[np.sort(first)]
rows=[];cols=[]
for lo in range(0,len(centers),128):
 block=centers[lo:lo+128];dist=np.zeros((len(block),len(holes)),dtype=np.uint8)
 for j in range(9):dist+=(block[:,j,None]!=holes[None,:,j])
 r,c=np.nonzero(dist<=4);rows.append(r+lo);cols.append(c)
A=csr_matrix((np.ones(sum(map(len,rows)),dtype=np.float64),(np.concatenate(rows),np.concatenate(cols))),shape=(len(centers),len(holes)));AT=A.T.tocsr();rng=np.random.default_rng(70941351)
lookup={tuple(x):i for i,x in enumerate(centers)};best=np.array([lookup[tuple(x)]for x in code[1029:]],dtype=int);history=[]
def save(chosen,method):
 global best
 if len(chosen)>=len(best):return
 best=np.array(chosen,dtype=int);new=np.vstack((code[:1029],centers[best]));payload=('\n'.join(''.join(map(str,x))for x in new)+'\n').encode();(folder/'candidate.txt').write_bytes(payload);history.append(dict(method=method,patch_words=len(best),M=len(new),sha256=hashlib.sha256(payload).hexdigest(),elapsed=time.monotonic()-start));print(json.dumps(history[-1]),flush=True)
for trial in range(12):
 counts=np.zeros(len(holes),dtype=np.int32);chosen=[];available=np.ones(len(centers),bool)
 while np.any(counts==0):
  scores=np.asarray(A@(counts==0)).ravel();scores[~available]=-1
  if trial: scores+=rng.random(len(scores))*(1 if trial<6 else 3)
  i=int(scores.argmax());chosen.append(i);available[i]=False;counts[A.indices[A.indptr[i]:A.indptr[i+1]]]+=1
 for i in rng.permutation(chosen):
  covered=A.indices[A.indptr[i]:A.indptr[i+1]]
  if np.all(counts[covered]>=2):counts[covered]-=1;chosen.remove(i)
 save(chosen,'greedy-'+str(trial))
 if time.monotonic()-start>60:break
print(json.dumps(dict(matrix_ready_seconds=time.monotonic()-start,centers=len(centers),nonzeros=A.nnz,best_patch=len(best))),flush=True)
remaining=max(1,min(110,175-(time.monotonic()-start)))
res=milp(c=np.ones(len(centers)),integrality=np.ones(len(centers)),bounds=Bounds(0,1),constraints=LinearConstraint(AT,1,np.inf),options=dict(time_limit=remaining,mip_rel_gap=.01,threads=1))
if res.x is not None:
 chosen=np.flatnonzero(res.x>.5)
 if np.all(np.asarray(AT[:,chosen].sum(axis=1)).ravel()>=1):save(chosen,'milp')
result=dict(scope='FIXED_BASE_RESTRICTED_POOL_ONLY',original_code_sha256=hashlib.sha256(raw).hexdigest(),quotient_classes_minimum_coverage=61,quotient_classes=len(reps),candidate_centers=len(centers),holes=len(holes),best_patch_words=len(best),best_total=1029+len(best),improvements=history,solver_status=int(res.status),solver_message=res.message,mip_dual_bound=float(res.mip_dual_bound) if getattr(res,'mip_dual_bound',None) is not None else None,runtime_seconds=time.monotonic()-start,optimality='NOT_ESTABLISHED',paid_resources_used=False)
(folder/'result.json').write_text(json.dumps(result,indent=2)+'\n');np.save(folder/'selected-centers.npy',centers[best]);print(json.dumps(result),flush=True)
