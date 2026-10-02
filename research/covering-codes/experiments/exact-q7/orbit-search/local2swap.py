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
start=time.monotonic();folder=Path(__file__).parent/'local2swap';d=ROOT/'certificates/q7_n9_r4_m1351';raw=(d/'code.txt').read_bytes();code=np.array([[int(c) for c in w]for w in raw.decode().splitlines()],dtype=np.uint8)
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
lookup={tuple(x):i for i,x in enumerate(centers)};incumbent=np.array([[int(c) for c in w] for w in (Path(__file__).parent/'expanded60/candidate-m1344-6a1653b6697b4ed2.txt').read_text().splitlines()],dtype=np.uint8);best=np.array([lookup[tuple(x)]for x in incumbent[1029:]],dtype=int);history=[]
def save(chosen,method):
 global best
 if len(chosen)>=len(best):return
 best=np.array(chosen,dtype=int);new=np.vstack((code[:1029],centers[best]));payload=('\n'.join(''.join(map(str,x))for x in new)+'\n').encode();(folder/'candidate.txt').write_bytes(payload);(folder/f'candidate-m{len(new)}-{hashlib.sha256(payload).hexdigest()[:16]}.txt').write_bytes(payload);history.append(dict(method=method,patch_words=len(best),M=len(new),sha256=hashlib.sha256(payload).hexdigest(),elapsed=time.monotonic()-start));print(json.dumps(history[-1]),flush=True)


counts=np.asarray(AT[:,best].sum(axis=1)).ravel().astype(np.int32);assert np.all(counts>=1)
private_owner=np.full(len(holes),-1,dtype=np.int32);private_sizes=np.zeros(len(best),dtype=np.int32)
for k,i in enumerate(best):
 idx=A.indices[A.indptr[i]:A.indptr[i+1]];private=idx[counts[idx]==1];private_owner[private]=k;private_sizes[k]=len(private)
qualified_pairs=0;checked_centers=0;successful=[];deadline=time.monotonic()+30
for cid in range(len(centers)):
 if time.monotonic()>deadline:break
 checked_centers+=1;covered=A.indices[A.indptr[cid]:A.indptr[cid+1]];owners=private_owner[covered];n=np.bincount(owners[owners>=0],minlength=len(best));eligible=np.flatnonzero(n==private_sizes)
 for ai in range(len(eligible)):
  for bi in range(ai+1,len(eligible)):
   a,b=map(int,eligible[[ai,bi]]);qualified_pairs+=1
   old1=A.indices[A.indptr[best[a]]:A.indptr[best[a]+1]];old2=A.indices[A.indptr[best[b]]:A.indptr[best[b]+1]]
   rem=counts.copy();rem[old1]-=1;rem[old2]-=1;missing=np.flatnonzero(rem==0)
   if np.all(np.isin(missing,covered,assume_unique=True)):
    # cid already in the remaining code would not increase coverage of missing.
    successful.append(dict(removed_indices=[int(best[a]),int(best[b])],replacement_pool_index=cid,replacement_word=''.join(map(str,centers[cid])),residual_holes=len(missing)))
result=dict(scope='FIXED_BASE_RESTRICTED_POOL_2_REMOVE_1_ADD_ONLY',code_sha256=hashlib.sha256((Path(__file__).parent/'expanded60/candidate-m1344-6a1653b6697b4ed2.txt').read_bytes()).hexdigest(),pool_centers=len(centers),checked_centers=checked_centers,qualified_pairs_literal_checked=qualified_pairs,private_hole_sizes={str(k):int(v)for k,v in zip(*np.unique(private_sizes,return_counts=True))},zero_private_patch_centers=int(np.count_nonzero(private_sizes==0)),successful_moves=successful,scan_complete=checked_centers==len(centers),runtime_seconds=time.monotonic()-start,optimality='NOT_ESTABLISHED',seed=None,iterations=checked_centers,paid_resources_used=False)
(folder/'result.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result),flush=True)
