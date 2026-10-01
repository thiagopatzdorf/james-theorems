import hashlib
import importlib.util
from pathlib import Path
import tempfile
import unittest

ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('ingest',ROOT/'tools/ingest_original.py')
ingest=importlib.util.module_from_spec(spec);spec.loader.exec_module(ingest)


class Ingestion(unittest.TestCase):
    def test_preserves_bytes_order_and_unknown_fields(self):
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp)/'original';p.write_bytes(b'111\r\n000')
            d=Path(tmp)/'archive'
            m=ingest.ingest(p,d,2,3,1,2)
            self.assertEqual((d/'code.txt').read_bytes(),b'111\n000\n')
            self.assertEqual((d/'originals'/f"{m['original_sha256']}.bin").read_bytes(),p.read_bytes())
            self.assertEqual(m['code_sha256'],hashlib.sha256(b'111\n000\n').hexdigest())
            self.assertIsNone(m['seed']);self.assertIsNone(m['created_at'])
            p.write_bytes(b'000\n111\n')
            with self.assertRaises(ValueError):ingest.ingest(p,d,2,3,1,2)
            self.assertEqual((d/'code.txt').read_bytes(),b'111\n000\n')
            self.assertEqual(len(list((d/'originals').iterdir())),2)

    def test_rejects_malformed_and_wrong_size_but_preserves_original(self):
        for raw,M in [(b'00\n111\n',2),(b'000\n111\n',3),(b'000\n\n111\n',2)]:
            with tempfile.TemporaryDirectory() as tmp:
                p=Path(tmp)/'original';p.write_bytes(raw);d=Path(tmp)/'archive'
                with self.assertRaises(ValueError):ingest.ingest(p,d,2,3,1,M)
                self.assertFalse((d/'code.txt').exists())
                self.assertEqual(len(list((d/'originals').iterdir())),1)


if __name__=='__main__':unittest.main()
