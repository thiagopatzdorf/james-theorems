#!/usr/bin/env python3
"""Certify a new completion of the unchanged original three-coset base.
Never overwrites original1351. This is external evidence, not a Lean proof.
"""
import argparse,hashlib,json,sys,time
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'verifiers'))
from verify_a import verify
from partition_certificate import ROWS,structure,exceptions
ORIGINAL=ROOT/'certificates/q7_n9_r4_m1351'
FROZEN='6d1b0e1abb8079df06a28d5301607d3d5247e0f2005d72e13f695ce26f6e6b52'
def sha(raw):return hashlib.sha256(raw).hexdigest()
def run(directory,generate=False):
 start=time.monotonic();d=Path(directory)
 if d.resolve()==ORIGINAL.resolve():raise ValueError('original artifact is immutable')
 raw=(d/'code.txt').read_bytes();orig=(ORIGINAL/'code.txt').read_bytes()
 if sha(orig)!=FROZEN:raise ValueError('original hash mismatch')
 parsed=verify(7,9,4,d/'code.txt',True);M=parsed['M_parsed']
 if not parsed['canonical'] or parsed['invalid_lines'] or parsed['duplicates'] or M<1029:raise ValueError('candidate parser/cardinality')
 if raw.splitlines()[:1029]!=orig.splitlines()[:1029]:raise ValueError('base changed')
 code=np.array([[int(c) for c in w] for w in raw.decode().splitlines()],dtype=np.uint8)
 original_meta=json.loads((ORIGINAL/'partition-metadata.json').read_text())
 L=structure(code,ROWS,original_meta['coset_representatives']);qraw=(ORIGINAL/'quotient.u16le').read_bytes()
 if sha(qraw)!=original_meta['quotient_sha256']:raise ValueError('original quotient hash')
 quotient=np.frombuffer(qraw,dtype='<u2');ids,words=exceptions(quotient,L)
 if generate:
  chosen=[]
  for lo in range(0,len(words),128):
   dist=np.count_nonzero(words[lo:lo+128,None,:]!=code[None,:,:],axis=2)
   witness=dist.argmin(axis=1)
   if np.any(dist[np.arange(len(witness)),witness]>4):raise ValueError('uncovered exception')
   chosen.extend(map(int,witness))
  if M>65535:raise ValueError('index capacity')
  eraw=np.array(chosen,dtype='<u2').tobytes();(d/'quotient.u16le').write_bytes(qraw);(d/'exceptions.u16le').write_bytes(eraw)
  meta=dict(original_meta,M=M,code_sha256=sha(raw),exceptions_sha256=sha(eraw),combined_payload_sha256=sha(qraw+eraw),parent_code_sha256=FROZEN,generator='tools/certify_fixed_base_candidate.py',formal_status='NOT_REPLAYED_IN_LEAN')
  (d/'partition-metadata.json').write_text(json.dumps(meta,indent=2)+'\n')
 meta=json.loads((d/'partition-metadata.json').read_text());eraw=(d/'exceptions.u16le').read_bytes()
 if [meta[k] for k in ('q','n','R','M')]!=[7,9,4,M] or meta['code_sha256']!=sha(raw):raise ValueError('identity')
 if (d/'quotient.u16le').read_bytes()!=qraw or sha(eraw)!=meta['exceptions_sha256'] or sha(qraw+eraw)!=meta['combined_payload_sha256']:raise ValueError('payload identity')
 if [meta.get(k) for k in ('base_prefix_size','quotient_words','exception_words','payload_bytes')]!=[1029,117649,len(ids),len(qraw)+len(eraw)]:raise ValueError('length/count')
 if meta.get('generator_rows')!=ROWS or meta.get('coset_representatives')!=original_meta['coset_representatives'] or meta.get('quotient_sha256')!=sha(qraw):raise ValueError('structure metadata')
 if len(eraw)!=2*len(ids):raise ValueError('length/count')
 witnesses=np.frombuffer(eraw,dtype='<u2')
 if np.any(witnesses>=M):raise ValueError('index out of range')
 if np.any(np.count_nonzero(words!=code[witnesses],axis=1)>4):raise ValueError('exception witness distance')
 # The unchanged quotient is already independently certified for the exact
 # unchanged base; no assertion that this is a kernel theorem is made.
 from partition_certificate import representatives
 good=quotient!=65535
 if np.any(quotient[good]>=1029) or np.any(np.count_nonzero(representatives()[good]!=code[quotient[good]],axis=1)>4):raise ValueError('quotient distance')
 covered=int(good.sum())*343+len(ids)
 if covered!=7**9:raise ValueError('partition count')
 result=dict(status='PASS',q=7,n=9,R=4,M=M,code_sha256=sha(raw),certificate_sha256=sha(qraw+eraw),parent_code_sha256=FROZEN,base_size=1029,quotient_words=117649,exception_words=len(ids),ambient_words=covered,payload_bytes=len(qraw)+len(eraw),formal_status='NOT_REPLAYED_IN_LEAN',runtime_seconds=time.monotonic()-start)
 (d/'partition-check.json').write_text(json.dumps(result,indent=2)+'\n');return result
if __name__=='__main__':
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('directory');p.add_argument('--generate',action='store_true');a=p.parse_args()
 try:print(json.dumps(run(a.directory,a.generate),indent=2))
 except (OSError,ValueError,KeyError) as e:print(json.dumps(dict(status='FAIL',error=str(e))));sys.exit(1)
