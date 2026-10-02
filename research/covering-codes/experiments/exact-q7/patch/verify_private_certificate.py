#!/usr/bin/env python3
"""Read-only private witness checker, no solver/NumPy/partition assumptions."""
import hashlib,json,sys
from pathlib import Path
OUT=Path(__file__).resolve().parent;ROOT=OUT.parents[2]
def check(path):
 raw=(ROOT/'certificates/q7_n9_r4_m1351/code.txt').read_bytes();code=raw.decode('ascii').splitlines();cert=json.loads(Path(path).read_text())
 if cert['source_sha256']!=hashlib.sha256(raw).hexdigest():raise ValueError('Wrong code hash')
 if len(code)!=1351 or len(set(code))!=1351 or any(len(w)!=9 or any(c not in '0123456' for c in w) for w in code):raise ValueError('Invalid code')
 witnesses=cert['private_witnesses']
 if sorted(w['original_code_index'] for w in witnesses)!=list(range(1029,1351)):raise ValueError('Missing/duplicate original indices')
 for record in witnesses:
  w=record['word'];j=record['original_code_index']
  if len(w)!=9 or any(c not in '0123456' for c in w) or int(w,7)!=record['ambient_id']:raise ValueError('Invalid ambient witness')
  cover=[i for i,c in enumerate(code) if sum(a!=b for a,b in zip(w,c))<=4]
  if cover!=[j]:raise ValueError('Not private witness')
 return {'status':'PASS','witness_count':322,'restricted_patch_minimum':322,'global_K_lower_bound_claimed':False}
if __name__=='__main__':
 try:print(json.dumps(check(sys.argv[1] if len(sys.argv)>1 else OUT/'private-witnesses.json')))
 except (ValueError,KeyError,OSError) as exc:print(json.dumps({'status':'FAIL','error':str(exc)}));sys.exit(1)
