#!/usr/bin/env python3
"""Exhaust all Hamming-ball errors, then all quotient centers: fixed-base LB only."""
import hashlib,itertools,json,math,sys,time
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[3]
sys.path.insert(0,str(ROOT/'tools'))
from partition_certificate import ROWS,representatives,structure,exceptions

def normalize(x):
 x=x.astype(np.int16)
 coeff=np.stack((x[:,0],(2*(x[:,1]-x[:,0])+6*(x[:,2]-x[:,0]))%7,(5*(x[:,1]-x[:,0])+6*(x[:,2]-x[:,0]))%7),axis=1)
 return (x-coeff@np.array(ROWS,dtype=np.int16))%7

def packed(tail):return tail.astype(np.int64)@np.array([7**i for i in range(5,-1,-1)],dtype=np.int64)

def main():
 start=time.monotonic();d=ROOT/'certificates/q7_n9_r4_m1351';raw=(d/'code.txt').read_bytes();code=np.array([[int(c) for c in w] for w in raw.decode().splitlines()],dtype=np.int16)
 meta=json.loads((d/'partition-metadata.json').read_text());L=structure(code,ROWS,meta['coset_representatives'])
 q=np.frombuffer((d/'quotient.u16le').read_bytes(),dtype='<u2');reps=representatives().astype(np.int16);holes=reps[q==65535];ids,words=exceptions(q,L)
 counts=np.zeros(7**6,dtype=np.int64);volume=0
 for weight in range(5):
  for positions in itertools.combinations(range(9),weight):
   changes=np.array(list(itertools.product(range(1,7),repeat=weight)),dtype=np.int16).reshape(-1,weight) if weight else np.empty((1,0),dtype=np.int16)
   errors=np.zeros((len(changes),9),dtype=np.int16)
   if weight:errors[:,positions]=changes
   norm=normalize(errors)
   assert np.all(norm[:,:3]==0)
   counts+=np.bincount(packed(norm[:,3:]),minlength=7**6);volume+=len(errors)
 assert volume==sum(math.comb(9,i)*6**i for i in range(5))==182791
 assert counts.sum()==volume
 coverage=np.zeros(7**6,dtype=np.int64)
 for hole in holes:
  # Number of radius-four errors with this normalized difference is number
  # of points covered in this343-word hole orbit by one center.
  coverage+=counts[packed((hole[3:]-reps[:,3:])%7)]
 maximum=int(coverage.max());best=int(coverage.argmax());center=reps[best]
 literal=int(np.count_nonzero(np.count_nonzero(words!=center,axis=1)<=4));assert literal==maximum
 for c in code[1029:]:
  t=int(packed(normalize(c[None,:])[:,3:])[0]);actual=int(np.count_nonzero(np.count_nonzero(words!=c,axis=1)<=4));assert actual==coverage[t]
 out=dict(scope='FIXED_BASE_ONLY; not a global lower bound for K7(9,4)',code_sha256=hashlib.sha256(raw).hexdigest(),base_size=1029,uncovered_words=len(words),uncovered_orbits=len(holes),all_ambient_centers=7**9,quotient_centers_checked=7**6,ball_volume=volume,maximum_holes_covered_by_one_arbitrary_word=maximum,attaining_center=''.join(map(str,center)),attaining_center_literal_coverage=literal,minimum_patch_words_by_counting=math.ceil(len(words)/maximum),fixed_base_total_lower_bound=1029+math.ceil(len(words)/maximum),coverage_histogram={str(k):int(v) for k,v in zip(*np.unique(coverage,return_counts=True))},original_patch_centers_literal_cross_checked=322,runtime_seconds=time.monotonic()-start,certificate='kernel.u16le + center-coverage.u16le',kernel_sha256=hashlib.sha256(counts.astype('<u2').tobytes()).hexdigest(),coverage_sha256=hashlib.sha256(coverage.astype('<u2').tobytes()).hexdigest())
 assert counts.max()<65536 and maximum<65536
 folder=Path(__file__).parent;(folder/'kernel.u16le').write_bytes(counts.astype('<u2').tobytes());(folder/'center-coverage.u16le').write_bytes(coverage.astype('<u2').tobytes());(folder/'kernel-analysis.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
if __name__=='__main__':main()
