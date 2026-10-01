#!/usr/bin/env python3
"""Generate/check packed witnesses. External validation is NOT a Lean theorem."""
import argparse,gzip,hashlib,json,sys,tempfile,time
from pathlib import Path
import numpy as np
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'verifiers'))
from verify_a import verify

def run(directory,generate=False):
 d=Path(directory);meta=json.loads((d/'metadata.json').read_text());q,n,R,M=(meta[k] for k in ('q','n','R','M'));N=q**n
 if N>250_000_000 or M>=65535:raise ValueError('capacity guard')
 codepath=d/'code.txt';parsed=verify(q,n,R,codepath,True)
 if parsed['invalid_lines'] or not parsed['canonical'] or parsed['sha256']!=meta['code_sha256'] or parsed['M_parsed']!=M:raise ValueError('invalid input/hash')
 code=np.array([[int(c) for c in line] for line in codepath.read_text().splitlines()],dtype=np.uint8)
 payload=d/'witness.u16le.gz';info=d/'witness-metadata.json'
 if generate:
  dist=np.full((q,)*n,n+1,dtype=np.uint8);witness=np.full((q,)*n,65535,dtype=np.uint16)
  for i,c in enumerate(code):dist[tuple(c)]=0;witness[tuple(c)]=i
  for axis in range(n):
   cheapest=dist.min(axis=axis,keepdims=True);where=dist.argmin(axis=axis,keepdims=True)
   chosen=np.take_along_axis(witness,where,axis=axis)
   improve=cheapest+np.uint8(1)<dist
   np.copyto(witness,chosen,where=improve);np.minimum(dist,cheapest+np.uint8(1),out=dist)
  if int(dist.max())>R:raise ValueError('code does not cover')
  raw=witness.astype('<u2',copy=False).tobytes(order='C')
  with payload.open('wb') as f:
   with gzip.GzipFile(filename='',fileobj=f,mode='wb',mtime=0) as g:g.write(raw)
  record=dict(format='flat uint16 little-endian; no header',ambient_order='big-endian base-q, original line indices',q=q,n=n,R=R,M=M,code_sha256=parsed['sha256'],payload_bytes=2*N,payload_sha256=hashlib.sha256(raw).hexdigest(),gzip_sha256=hashlib.sha256(payload.read_bytes()).hexdigest(),formal_status='NOT_REPLAYED_IN_LEAN')
  info.write_text(json.dumps(record,indent=2)+'\n')
  del raw,dist,witness
 record=json.loads(info.read_text());start=time.monotonic();digest=hashlib.sha256();count=0;max_witness=0
 if record['code_sha256']!=parsed['sha256'] or [record[k] for k in ('q','n','R','M')]!=[q,n,R,M]:raise ValueError('certificate parameters mismatch')
 if hashlib.sha256(payload.read_bytes()).hexdigest()!=record['gzip_sha256']:raise ValueError('compressed hash mismatch')
 with gzip.open(payload,'rb') as f:
  while chunk:=f.read(2*65536):
   if len(chunk)%2:raise ValueError('odd payload length')
   digest.update(chunk);indices=np.frombuffer(chunk,dtype='<u2');size=len(indices)
   if count+size>N or np.any(indices>=M):raise ValueError('out-of-range witness')
   ids=np.arange(count,count+size,dtype=np.uint64);distance=np.zeros(size,dtype=np.uint8)
   # This checker decodes integers and checks literal coordinate mismatches;
   # it does not re-run the generating min-plus transform.
   for coordinate in range(n-1,-1,-1):
    distance+=(ids%q)!=code[indices,coordinate];ids//=q
   if np.any(ids):raise ValueError('ambient decode overflow')
   if np.any(distance>R):raise ValueError('invalid witness distance')
   max_witness=max(max_witness,int(distance.max()));count+=size
 if count!=N or record['payload_bytes']!=2*N or digest.hexdigest()!=record['payload_sha256']:raise ValueError('length/hash mismatch')
 result=dict(status='PASS',ambient_words=count,code_sha256=parsed['sha256'],certificate_sha256=digest.hexdigest(),max_witness_distance=max_witness,runtime_seconds=time.monotonic()-start,formal_status='NOT_REPLAYED_IN_LEAN')
 (d/'certificate-check.json').write_text(json.dumps(result,indent=2)+'\n');return result
if __name__=='__main__':
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('directory');p.add_argument('--generate',action='store_true');a=p.parse_args()
 try:print(json.dumps(run(a.directory,a.generate),indent=2))
 except (ValueError,OSError,KeyError) as e:print(json.dumps(dict(status='FAIL',error=str(e))));sys.exit(1)
