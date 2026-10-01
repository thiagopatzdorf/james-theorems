import gzip,hashlib,json,re,sys,tempfile,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'tools'))
from ingest_original import ingest
from witness_certificate import run

class CertificateTests(unittest.TestCase):
 def test_witness_roundtrip_and_adversarial_mutations(self):
  with tempfile.TemporaryDirectory() as tmp:
   root=Path(tmp);source=root/'original';source.write_bytes(b'000\n111\n');d=root/'certificate'
   ingest(source,d,2,3,1,2)
   self.assertEqual(run(d,True)['ambient_words'],8)
   payload=d/'witness.u16le.gz';meta=d/'witness-metadata.json'
   valid=gzip.decompress(payload.read_bytes());original=json.loads(meta.read_text())
   # Replace hashes too: these must fail mathematical/structural validation.
   for raw in (valid[:-2],valid+b'\x00\x00',b'\xff\xff'+valid[2:],b'\x01\x00'+valid[2:],valid[:-1]):
    compressed=gzip.compress(raw,mtime=0);payload.write_bytes(compressed)
    m=dict(original,payload_sha256=hashlib.sha256(raw).hexdigest(),gzip_sha256=hashlib.sha256(compressed).hexdigest());meta.write_text(json.dumps(m))
    with self.assertRaises(ValueError):run(d)

 def test_all_frozen_artifacts_and_large_lean_word_linkage(self):
  for d in (ROOT/'certificates').glob('q*_m*'):
   m=json.loads((d/'metadata.json').read_text());raw=(d/'code.txt').read_bytes()
   self.assertEqual(hashlib.sha256(raw).hexdigest(),m['code_sha256'])
   self.assertEqual(len(raw.splitlines()),m['M']);self.assertEqual(len(set(raw.splitlines())),m['M_unique'])
   for line in raw.splitlines():self.assertEqual(len(line),m['n']);self.assertTrue(all(48<=x<48+m['q'] for x in line))
   self.assertTrue(raw.endswith(b'\n'));self.assertNotIn(b'\r',raw)
  source=ROOT/'formal/CoveringRecords/PrincipalCode.lean'
  words=re.findall(r'!\[([0-6](?:, [0-6]){8})\]',source.read_text())
  rebuilt=''.join(w.replace(', ','')+'\n' for w in words).encode()
  self.assertEqual(rebuilt,(ROOT/'certificates/q7_n9_r4_m1351/code.txt').read_bytes())
  manifest=json.loads((ROOT/'formal/PrincipalCodeManifest.json').read_text())
  self.assertEqual(hashlib.sha256(source.read_bytes()).hexdigest(),manifest['source_sha256'])
