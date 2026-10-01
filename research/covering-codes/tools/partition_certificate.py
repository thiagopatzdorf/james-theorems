#!/usr/bin/env python3
"""Compact certificate for the recovered principal code; no new code/search.
Soundness: coordinate addition in Z/7Z is a Hamming isometry; a linear span
is closed under addition. A bijective first-three-coordinate projection gives
one unique prefix-zero representative in each orbit. Checked full cosets cover
all translates of checked representatives; remaining orbits are checked explicitly.
This argument/checker is not yet a Lean proof.
"""
import argparse,gzip,hashlib,itertools,json,sys,time
from pathlib import Path
import numpy as np
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'verifiers'))
from verify_a import verify
ROWS=[[1,1,1,1,1,1,1,1,1],[0,2,3,2,3,6,0,1,1],[0,5,3,0,6,4,4,3,5]]

def sha(raw):return hashlib.sha256(raw).hexdigest()
def word_ids(words):return words.astype(np.uint64) @ np.array([7**i for i in range(8,-1,-1)],dtype=np.uint64)
def representatives():
 ids=np.arange(7**6,dtype=np.uint64);result=np.zeros((len(ids),9),dtype=np.uint8)
 for i in range(8,2,-1):result[:,i]=ids%7;ids//=7
 return result

def structure(code,rows,reps):
 if len(rows)!=3 or any(len(r)!=9 or any(type(x)!=int or not 0<=x<7 for x in r) for r in rows):raise ValueError('generator dimensions/alphabet')
 G=np.array(rows,dtype=np.int16);coeff=np.array(list(itertools.product(range(7),repeat=3)),dtype=np.int16);L=(coeff@G)%7
 if len(set(map(tuple,L[:,:3])))!=343:raise ValueError('prefix projection not bijective')
 if len(reps)!=3 or any(len(r)!=9 or any(x not in '0123456' for x in r) for r in reps):raise ValueError('coset representatives')
 union=set()
 for r in reps:union.update(map(tuple,(np.array(list(map(int,r)),dtype=np.int16)+L)%7))
 base=set(map(tuple,code[:1029]))
 if len(base)!=1029 or union!=base:raise ValueError('base is not exactly three disjoint full cosets')
 return L.astype(np.uint8)
def exceptions(quotient,L):
 holes=representatives()[quotient==65535]
 words=((holes[:,None,:].astype(np.int16)+L[None,:,:])%7).astype(np.uint8).reshape(-1,9)
 ids=word_ids(words);order=np.argsort(ids);ids=ids[order];words=words[order]
 if len(np.unique(ids))!=len(ids):raise ValueError('exception orbits overlap')
 return ids,words

def run(directory,generate=False):
 start=time.monotonic();d=Path(directory);parsed=verify(7,9,4,d/'code.txt',True)
 if parsed['invalid_lines'] or not parsed['canonical'] or parsed['M_parsed']!=1351 or parsed['M_unique']!=1351:raise ValueError('invalid principal code')
 code=np.array([[int(c) for c in w] for w in (d/'code.txt').read_text().splitlines()],dtype=np.uint8)
 meta_path=d/'partition-metadata.json';qp=d/'quotient.u16le';ep=d/'exceptions.u16le'
 if generate:
  # Recover coset representatives from the actual original-order base prefix.
  G=np.array(ROWS,dtype=np.int16);coeff=np.array(list(itertools.product(range(7),repeat=3)),dtype=np.int16);L=(coeff@G)%7;remaining=set(map(tuple,code[:1029]));reps=[]
  while remaining:
   rep=min(remaining);coset=set(map(tuple,(np.array(rep,dtype=np.int16)+L)%7))
   if not coset<=remaining:raise ValueError('reported structure does not match original')
   reps.append(''.join(map(str,rep)));remaining-=coset
  L=structure(code,ROWS,reps);ambient=representatives();quotient=np.full(7**6,65535,dtype='<u2')
  # Literal nearest-base-word computation, independent of the full transform.
  for lo in range(0,len(ambient),512):
   distances=np.count_nonzero(ambient[lo:lo+512,None,:]!=code[None,:1029,:],axis=2)
   indices=distances.argmin(axis=1);good=distances[np.arange(len(indices)),indices]<=4
   block=quotient[lo:lo+len(indices)];block[good]=indices[good]
  ids,_=exceptions(quotient,L)
  # Reuse the already checked flat witness at precisely the exceptional ids.
  flat=np.frombuffer(gzip.decompress((d/'witness.u16le.gz').read_bytes()),dtype='<u2');patch=flat[ids].astype('<u2')
  qraw=quotient.tobytes();eraw=patch.tobytes();qp.write_bytes(qraw);ep.write_bytes(eraw)
  meta=dict(q=7,n=9,R=4,M=1351,base_prefix_size=1029,code_sha256=parsed['sha256'],generator_rows=ROWS,coset_representatives=reps,quotient_words=7**6,exception_words=len(ids),quotient_sha256=sha(qraw),exceptions_sha256=sha(eraw),combined_payload_sha256=sha(qraw+eraw),payload_bytes=len(qraw)+len(eraw),format='uint16 little-endian; quotient index <1029 or sentinel65535; exceptions original codeword index <1351',quotient_order='prefix000 followed by six base7 digits, most-significant first',exception_order='ascending ambient base7 integer over all sentinel orbits',formal_status='NOT_REPLAYED_IN_LEAN')
  meta_path.write_text(json.dumps(meta,indent=2)+'\n')
 meta=json.loads(meta_path.read_text())
 if [meta.get(k) for k in ('q','n','R','M','base_prefix_size','quotient_words')]!=[7,9,4,1351,1029,7**6] or meta['code_sha256']!=parsed['sha256']:raise ValueError('partition/code identity mismatch')
 L=structure(code,meta['generator_rows'],meta['coset_representatives']);qraw=qp.read_bytes();eraw=ep.read_bytes()
 if len(qraw)!=2*7**6 or len(eraw)%2:raise ValueError('payload length')
 if [sha(qraw),sha(eraw),sha(qraw+eraw)]!=[meta['quotient_sha256'],meta['exceptions_sha256'],meta['combined_payload_sha256']]:raise ValueError('payload hash')
 quotient=np.frombuffer(qraw,dtype='<u2');covered=quotient!=65535
 if np.any(quotient[covered]>=1029):raise ValueError('invalid quotient code index')
 distance=np.count_nonzero(representatives()[covered]!=code[quotient[covered]],axis=1)
 if np.any(distance>4):raise ValueError('quotient witness distance')
 ids,words=exceptions(quotient,L);patch=np.frombuffer(eraw,dtype='<u2')
 if len(patch)!=len(ids) or meta['exception_words']!=len(ids) or meta['payload_bytes']!=len(qraw)+len(eraw):raise ValueError('exception count/length')
 if np.any(patch>=1351):raise ValueError('invalid exception index')
 if np.any(np.count_nonzero(words!=code[patch],axis=1)>4):raise ValueError('exception witness distance')
 result=dict(status='PASS',code_sha256=parsed['sha256'],certificate_sha256=sha(qraw+eraw),quotient_words=7**6,sentinel_orbits=int(np.count_nonzero(~covered)),checked_exception_words=len(ids),covered_by_symmetry=int(np.count_nonzero(covered))*343,ambient_words=7**9,payload_bytes=len(qraw)+len(eraw),runtime_seconds=time.monotonic()-start,formal_status='NOT_REPLAYED_IN_LEAN')
 if result['covered_by_symmetry']+len(ids)!=7**9:raise ValueError('partition not exhaustive')
 (d/'partition-check.json').write_text(json.dumps(result,indent=2)+'\n');return result
if __name__=='__main__':
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('directory');p.add_argument('--generate',action='store_true');a=p.parse_args()
 try:print(json.dumps(run(a.directory,a.generate),indent=2))
 except (ValueError,OSError,KeyError) as e:print(json.dumps(dict(status='FAIL',error=str(e))));sys.exit(1)
