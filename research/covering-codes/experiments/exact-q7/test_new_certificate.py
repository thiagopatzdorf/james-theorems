#!/usr/bin/env python3
"""Adversarial checks on actual new completion, no large exhaustive rerun."""
import hashlib,json,shutil,sys,tempfile,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'tools'))
from certify_fixed_base_candidate import run
DATA=ROOT/'certificates/q7_n9_r4_m1346'
class CertificateAttacks(unittest.TestCase):
 def test_real_and_forged_objects(self):
  mutations=['wrongM','wrongrows','wrongquotienthash','wronglength','outofrange','wronginrange','truncated','basechange']
  for attack in ['valid']+mutations:
   with self.subTest(attack=attack),tempfile.TemporaryDirectory() as td:
    d=Path(td)
    for name in ['code.txt','partition-metadata.json','quotient.u16le','exceptions.u16le']:shutil.copyfile(DATA/name,d/name)
    p=d/'partition-metadata.json';m=json.loads(p.read_text())
    if attack=='wrongM':m['M']+=1
    if attack=='wrongrows':m['generator_rows'][0][0]=2
    if attack=='wrongquotienthash':m['quotient_sha256']='0'*64
    if attack=='wronglength':m['payload_bytes']+=2
    if attack in ['outofrange','wronginrange','truncated']:
     ep=d/'exceptions.u16le';b=ep.read_bytes()
     if attack=='truncated':b=b[:-2]
     else:b=(65535 if attack=='outofrange' else 0).to_bytes(2,'little')+b[2:]
     ep.write_bytes(b);m['exceptions_sha256']=hashlib.sha256(b).hexdigest();m['combined_payload_sha256']=hashlib.sha256((d/'quotient.u16le').read_bytes()+b).hexdigest()
    if attack=='basechange':
     c=d/'code.txt';raw=c.read_bytes();c.write_bytes(b'1'+raw[1:]);m['code_sha256']=hashlib.sha256(c.read_bytes()).hexdigest()
    p.write_text(json.dumps(m))
    if attack=='valid':self.assertEqual(run(d)['status'],'PASS')
    else:
     with self.assertRaises(ValueError):run(d)
if __name__=='__main__':unittest.main(verbosity=2)
