#!/usr/bin/env python3
"""Run both independent verifiers on every code in data/cells.json and write
data/certificates/<cell>.json.  Certificates are overwritten only with --force.

    python scripts/certify.py [--only K5_7_2] [--force] [--skip-python]

A certificate is written only if the verifier results are recorded verbatim;
`python -m impossibility.provenance`-level validation then re-hashes the code.
"""
import argparse
import datetime
import json
import platform
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))
from impossibility.provenance import canonical_sha256  # noqa: E402

CEXE = ROOT / "bin" / ("verify_nearest.exe" if sys.platform == "win32" else "verify_nearest")


def run(cmd):
    t = time.time()
    p = subprocess.run(cmd, capture_output=True, text=True)
    return p.returncode, p.stdout.strip(), round(time.time() - t, 1)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--only")
    ap.add_argument("--force", action="store_true")
    ap.add_argument("--skip-python", action="store_true")
    a = ap.parse_args()
    cells = json.loads((ROOT / "data" / "cells.json").read_text(encoding="utf-8"))
    commit = subprocess.run(["git", "rev-parse", "HEAD"], capture_output=True, text=True, cwd=ROOT).stdout.strip()
    (ROOT / "data" / "certificates").mkdir(exist_ok=True)
    for c in cells:
        if a.only and c["id"] != a.only:
            continue
        out = ROOT / "data" / "certificates" / f"{c['id']}.json"
        if out.exists() and not a.force:
            print(f"{c['id']}: certificate exists (use --force)")
            continue
        code = ROOT / c["code_file"]
        words = code.read_text(encoding="ascii").split()
        q, n, R = str(c["q"]), str(c["n"]), str(c["R"])
        vs = []
        rc, txt, sec = run([str(CEXE), q, n, R, str(code)])
        vs.append({"impl": "nearest-c", "source": "verifier/verify_nearest.c", "result": "VERIFIED" if rc == 0 else "FAILED", "rc": rc, "output": txt, "seconds": sec})
        print(c["id"], vs[-1]["result"], txt, sec, "s", flush=True)
        if not a.skip_python:
            rc, txt, sec = run([sys.executable, str(ROOT / "verifier" / "verify_cover.py"), q, n, R, str(code)])
            vs.append({"impl": "ballmark-py", "source": "verifier/verify_cover.py", "result": "VERIFIED" if rc == 0 else "FAILED", "rc": rc, "output": txt, "seconds": sec})
            print(c["id"], vs[-1]["result"], txt, sec, "s", flush=True)
        cert = {
            "schema": "impossibility/certificate/1",
            "cell": c["id"], "q": c["q"], "n": c["n"], "R": c["R"],
            "size": len(words),
            "code_file": c["code_file"],
            "canonical_sha256": canonical_sha256(words),
            "canonical_form": "sha256 of sorted codewords joined by LF with trailing LF",
            "generator": c["generator"],
            "verifiers": vs,
            "repo_base_commit": commit,
            "created_utc": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "host": platform.platform(),
            "claim": f"K_{c['q']}({c['n']},{c['R']}) <= {len(words)}",
        }
        out.write_text(json.dumps(cert, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
