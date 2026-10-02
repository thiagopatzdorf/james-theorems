"""Include real new-certificate forgery checks in fast CI."""
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'experiments/exact-q7'))
from test_new_certificate import CertificateAttacks
