import hashlib,json,shutil,sys,tempfile,unittest
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'tools'))
from partition_certificate import run

class PartitionTests(unittest.TestCase):
 def test_compact_partition_and_forged_payloads(self):
  original=ROOT/'certificates/q7_n9_r4_m1351'
  with tempfile.TemporaryDirectory() as tmp:
   d=Path(tmp)
   for name in ('code.txt','quotient.u16le','exceptions.u16le','partition-metadata.json'):shutil.copy(original/name,d/name)
   result=run(d);self.assertEqual(result['covered_by_symmetry']+result['checked_exception_words'],40353607)
   self.assertEqual((result['sentinel_orbits'],result['checked_exception_words']), (27,9261))
   qraw=(d/'quotient.u16le').read_bytes();eraw=(d/'exceptions.u16le').read_bytes();meta=json.loads((d/'partition-metadata.json').read_text())
   code=np.array([[int(c) for c in w] for w in (d/'code.txt').read_text().splitlines()])
   bad=int(np.flatnonzero(np.count_nonzero(code[:1029],axis=1)>4)[0])
   for q,e in ((qraw[:-2],eraw),(int(1100).to_bytes(2,'little')+qraw[2:],eraw),(bad.to_bytes(2,'little')+qraw[2:],eraw),(qraw,int(1351).to_bytes(2,'little')+eraw[2:])):
    (d/'quotient.u16le').write_bytes(q);(d/'exceptions.u16le').write_bytes(e)
    m=dict(meta,quotient_sha256=hashlib.sha256(q).hexdigest(),exceptions_sha256=hashlib.sha256(e).hexdigest(),combined_payload_sha256=hashlib.sha256(q+e).hexdigest(),payload_bytes=len(q)+len(e));(d/'partition-metadata.json').write_text(json.dumps(m))
    with self.assertRaises(ValueError):run(d)
   (d/'quotient.u16le').write_bytes(qraw);(d/'exceptions.u16le').write_bytes(eraw)
   m=dict(meta,generator_rows=[[0]*9 for _ in range(3)]);(d/'partition-metadata.json').write_text(json.dumps(m))
   with self.assertRaisesRegex(ValueError,'projection'):run(d)
