import json,sys,tempfile,unittest
from pathlib import Path
from unittest.mock import patch
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'tools'))
import verify_case

class PipelineTests(unittest.TestCase):
 def test_named_case_parameters_and_hash_reject_before_expensive_work(self):
  with tempfile.TemporaryDirectory() as tmp:
   root=Path(tmp);d=root/'certificates/q2_n3_r1_m2';d.mkdir(parents=True)
   (d/'code.txt').write_text('000\n111\n');(d/'SHA256SUMS').write_text('not used before validation\n')
   with patch.object(verify_case,'ROOT',root):
    with self.assertRaisesRegex(ValueError,'identity'):verify_case.run('../escape',True)
    (d/'metadata.json').write_text(json.dumps(dict(q=2,n=3,R=2,M=2,code_sha256='0'*64)))
    with self.assertRaisesRegex(ValueError,'parameters'):verify_case.run(d.name,True)
    (d/'metadata.json').write_text(json.dumps(dict(q=2,n=3,R=1,M=2,code_sha256='0'*64)))
    with self.assertRaisesRegex(ValueError,'hash mismatch'):verify_case.run(d.name,True)
    self.assertFalse((root/'build').exists())
