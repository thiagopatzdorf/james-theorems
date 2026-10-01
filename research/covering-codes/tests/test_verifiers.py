import hashlib
import itertools
import json
from pathlib import Path
import random
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'verifiers'))
from verify_a import verify


class IndependentChecks(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp = tempfile.TemporaryDirectory()
        cls.binary = Path(cls.temp.name) / 'b'
        subprocess.run(['g++', '-std=c++17', '-O2', '-Wall', '-Wextra',
                        str(ROOT/'verifiers/verify_b.cpp'), '-lcrypto', '-o', str(cls.binary)], check=True)

    @classmethod
    def tearDownClass(cls):
        cls.temp.cleanup()

    def compare(self, q, n, R, raw):
        p = Path(self.temp.name)/'code.txt'
        p.write_bytes(raw)
        a = verify(q, n, R, p)
        transformed = verify(q, n, R, p, method='transform')
        proc = subprocess.run([str(self.binary), str(q), str(n), str(R), str(p)], capture_output=True, text=True)
        self.assertIn(proc.returncode, (0, 1), proc.stderr)
        b = json.loads(proc.stdout)
        for key in ('q','n','R','M_parsed','M_unique','duplicates','invalid_lines',
                    'ambient_words','sha256','canonical','exhaustive','covered',
                    'uncovered','max_min_distance','first_uncovered'):
            self.assertEqual(a[key], b[key], (key, q,n,R,raw))
            self.assertEqual(a[key], transformed[key], ('transform',key,q,n,R,raw))
        self.assertEqual(a['sha256'], hashlib.sha256(raw).hexdigest())
        return a

    def test_repetition_231(self):
        r = self.compare(2,3,1,b'000\n111\n')
        self.assertEqual((r['covered'],r['uncovered'],r['max_min_distance']), (8,0,1))

    def test_all_binary_length3_subsets_all_radii(self):
        # 255 nonempty subsets times four radii; no sampling of this universe.
        words = [''.join(w) for w in itertools.product('01', repeat=3)]
        for mask in range(1,256):
            raw = ''.join(w+'\n' for i,w in enumerate(words) if mask & (1<<i)).encode()
            for R in range(4):
                self.compare(2,3,R,raw)

    def test_other_alphabets_and_packing(self):
        rng = random.Random(20261001)
        for q,n in ((3,3),(4,3),(5,3),(7,3),(10,2)):
            words = [''.join(map(str,w)) for w in itertools.product(range(q), repeat=n)]
            for _ in range(8):
                sample = rng.sample(words, rng.randrange(1, min(len(words),12)))
                raw = ('\n'.join(sample)+'\n').encode()
                for R in range(n+1):
                    self.compare(q,n,R,raw)

    def test_duplicates_and_boundaries(self):
        r = self.compare(2,3,1,b'000\n111\n000\n')
        self.assertEqual((r['M_parsed'],r['M_unique'],r['duplicates']), (3,2,1))
        self.assertEqual(self.compare(7,3,0,b'666\n')['max_min_distance'],3)
        self.assertEqual(self.compare(7,3,3,b'666\n')['uncovered'],0)

    def test_adversarial_parser(self):
        for raw in (b'', b'\n', b'000\n\n111\n', b'000\r\n', b'000',
                    b'00\n', b'0000\n', b'007\n', b'0 0\n', b'#00\n',
                    b'\xef\xbb\xbf000\n', b'\xff00\n', b'00\x00\n'):
            self.compare(7,3,1,raw)

    def test_parameter_and_overflow_rejection(self):
        p = Path(self.temp.name)/'code.txt'; p.write_bytes(b'0\n')
        for args in ((1,1,0),(7,0,0),(7,9,10),(7,32,4)):
            b = subprocess.run([str(self.binary),*map(str,args),str(p)],capture_output=True)
            self.assertEqual(b.returncode,2)
        with self.assertRaises(ValueError):
            verify(1,1,0,p)


if __name__ == '__main__':
    unittest.main()
