#!/usr/bin/env python3
"""Bounded fixed-base set-cover heuristic; cannot certify global optimality."""
import os
for key in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS'):os.environ[key]='1'
import argparse,hashlib,json,sys,time
from pathlib import Path
import numpy as np
from scipy.sparse import csr_matrix
from scipy.optimize import milp,Bounds,LinearConstraint
ROOT=Path(__file__).resolve().parents[3];sys.path.insert(0,str(ROOT/'tools'))
from partition_certificate import ROWS,representatives,structure,exceptions,word_ids
parser=argparse.ArgumentParser();parser.add_argument('--iterations',type=int);args=parser.parse_args()
start=time.monotonic();folder=Path(__file__).parent/'expanded60';d=ROOT/'certificates/q7_n9_r4_m1351';raw=(d/'code.txt').read_bytes();code=np.array([[int(c) for c in w]for w in raw.decode().splitlines()],dtype=np.uint8)
meta=json.loads((d/'partition-metadata.json').read_text());L=structure(code,ROWS,meta['coset_representatives']);q=np.frombuffer((d/'quotient.u16le').read_bytes(),dtype='<u2');_,holes=exceptions(q,L)
coverage=np.frombuffer((ROOT/'experiments/exact-q7/global/center-coverage.u16le').read_bytes(),dtype='<u2');reps=representatives()[coverage>=60]
centers=((reps[:,None,:].astype(np.int16)+L[None,:,:])%7).astype(np.uint8).reshape(-1,9)
centers=np.vstack((centers,code[1029:]));ids=word_ids(centers);_,first=np.unique(ids,return_index=True);centers=centers[np.sort(first)]
rows=[];cols=[]
for lo in range(0,len(centers),128):
 block=centers[lo:lo+128];dist=np.zeros((len(block),len(holes)),dtype=np.uint8)
 for j in range(9):dist+=(block[:,j,None]!=holes[None,:,j])
 r,c=np.nonzero(dist<=4);rows.append(r+lo);cols.append(c)
A=csr_matrix((np.ones(sum(map(len,rows)),dtype=np.float64),(np.concatenate(rows),np.concatenate(cols))),shape=(len(centers),len(holes)));AT=A.T.tocsr();seed=70941346;rng=np.random.default_rng(seed)
lookup={tuple(x):i for i,x in enumerate(centers)};incumbent=np.array([[int(c) for c in w] for w in (Path(__file__).parent/'candidate1346.txt').read_text().splitlines()],dtype=np.uint8);best=np.array([lookup[tuple(x)]for x in incumbent[1029:]],dtype=int);history=[]
def save(chosen,method):
 global best
 if len(chosen)>=len(best):return
 best=np.array(chosen,dtype=int);new=np.vstack((code[:1029],centers[best]));payload=('\n'.join(''.join(map(str,x))for x in new)+'\n').encode();(folder/'candidate.txt').write_bytes(payload);(folder/f'candidate-m{len(new)}-{hashlib.sha256(payload).hexdigest()[:16]}.txt').write_bytes(payload);history.append(dict(method=method,patch_words=len(best),M=len(new),sha256=hashlib.sha256(payload).hexdigest(),elapsed=time.monotonic()-start));print(json.dumps(history[-1]),flush=True)

counts=np.asarray(AT[:,best].sum(axis=1)).ravel().astype(np.int32)
assert np.all(counts>=1)
iterations=0;accepted_equal=0;repair_start=time.monotonic();initial=best.copy()
while (iterations<args.iterations if args.iterations is not None else time.monotonic()-repair_start<180):
 iterations+=1
 k=int(rng.integers(4,25));removed=rng.choice(best,size=k,replace=False);chosen=list(set(map(int,best))-set(map(int,removed)))
 cnt=counts.copy()
 for i in removed:cnt[A.indices[A.indptr[i]:A.indptr[i+1]]]-=1
 available=np.ones(len(centers),bool);available[chosen]=False
 while np.any(cnt==0) and len(chosen)<=len(best):
  scores=np.asarray(A@(cnt==0)).ravel();scores[~available]=-1;scores+=rng.random(len(scores))*float(rng.choice([.5,1,2,3]))
  i=int(scores.argmax());chosen.append(i);available[i]=False;cnt[A.indices[A.indptr[i]:A.indptr[i+1]]]+=1
 if np.any(cnt==0):continue
 for i in rng.permutation(chosen):
  covered=A.indices[A.indptr[i]:A.indptr[i+1]]
  if np.all(cnt[covered]>=2):cnt[covered]-=1;chosen.remove(i)
 if len(chosen)<len(best):save(chosen,'destroy-repair-'+str(iterations));counts=cnt
 elif len(chosen)==len(best):best=np.array(chosen);counts=cnt;accepted_equal+=1
out=dict(scope='FIXED_BASE_RESTRICTED_POOL_ONLY',method='seeded destroy4..24 and randomized greedy repair, neutral moves allowed',seed=seed,iteration_replay_note='Use --iterations recorded_iteration_count; Python3.12, NumPy2.3.5 and same incumbent/matrix/order required',initial_code_sha256=hashlib.sha256((Path(__file__).parent/'candidate1346.txt').read_bytes()).hexdigest(),minimum_quotient_coverage=60,quotient_classes=len(reps),candidate_centers=len(centers),iterations=iterations,accepted_equal=accepted_equal,best_patch=len(best),best_total=1029+len(best),improvements=history,runtime_seconds=time.monotonic()-start,optimality='NOT_ESTABLISHED',paid_resources_used=False)
(folder/'result.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out),flush=True)
