#!/usr/bin/env python3
"""Iteration-bounded search replay in isolated outputs; original objects unchanged."""
import hashlib,json,subprocess,tempfile,time
from pathlib import Path
HERE=Path(__file__).resolve().parent
source=HERE/'orbit-search/expanded60-search.py'
expected='6a1653b6697b4ed2c8753b2ae5f5a6c0878a05b7cc47873d11b0387b11703db9'
start=time.monotonic()
with tempfile.TemporaryDirectory() as out:
 original=source.read_text();needle="folder=Path(__file__).parent/'expanded60';"
 assert original.count(needle)==1
 replay=original.replace(needle,'folder=Path('+repr(out)+');')
 with tempfile.NamedTemporaryFile(mode='w',suffix='.py',prefix='.replay-',dir=source.parent,delete=False) as f:
  f.write(replay);path=Path(f.name)
 try:
  p=subprocess.run(['python3',str(path),'--iterations','4829'],capture_output=True,text=True,timeout=120,check=True)
 finally:path.unlink()
 actual=hashlib.sha256((Path(out)/'candidate.txt').read_bytes()).hexdigest()
 if actual!=expected:raise ValueError('iteration replay hash mismatch')
 (HERE/'replay-best.log').write_text(p.stdout+p.stderr)
 result=dict(status='PASS',iterations=4829,seed=70941346,code_sha256=actual,generator_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),only_source_change='output directory isolated; generation algorithm unchanged',source_artifacts_unchanged=True,runtime_seconds=time.monotonic()-start)
 (HERE/'replay-best.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))
