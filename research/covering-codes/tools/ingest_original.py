#!/usr/bin/env python3
"""Preserve original bytes first. Normalize only CRLF to LF; preserve word order."""
import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import sys

sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'verifiers'))
from verify_a import verify


def ingest(source, target, q, n, R, M, source_commit=None):
    source, target = Path(source), Path(target)
    raw = source.read_bytes()
    original_hash = hashlib.sha256(raw).hexdigest()
    target.mkdir(parents=True, exist_ok=True)
    archive = target/'originals'/f'{original_hash}.bin'
    archive.parent.mkdir(exist_ok=True)
    if not archive.exists():
        archive.write_bytes(raw)
    elif archive.read_bytes()!=raw:
        raise ValueError('original archive collision')
    canonical = raw.replace(b'\r\n',b'\n')
    if not canonical.endswith(b'\n'):
        canonical += b'\n'
    code = target/'code.txt'
    if code.exists() and code.read_bytes()!=canonical:
        raise ValueError('existing canonical code differs; preserve separate candidate directory')
    # Validate in a temporary file; no malformed code enters the canonical slot.
    import tempfile
    with tempfile.NamedTemporaryFile() as f:
        f.write(canonical);f.flush()
        parsed=verify(q,n,R,f.name,True)
    if parsed['invalid_lines'] or parsed['M_parsed']!=M or not parsed['canonical']:
        raise ValueError(f'original preserved, canonicalization rejected: {parsed}')
    code.write_bytes(canonical)
    metadata=dict(q=q,n=n,R=R,M=M,metric='Hamming',alphabet=list(range(q)),
                  code_sha256=parsed['sha256'],original_sha256=original_hash,
                  source_path=str(source.resolve()),source_commit=source_commit,
                  generator=None,seed=None,created_at=None,
                  canonicalized_at=datetime.now(timezone.utc).isoformat(),
                  provenance_status='SOURCE_BYTES_PRESERVED_GENERATION_UNKNOWN',
                  canonicalization='CRLF to LF; final LF added if absent; order unchanged',
                  M_unique=parsed['M_unique'],duplicates=parsed['duplicates'])
    (target/'metadata.json').write_text(json.dumps(metadata,indent=2)+'\n')
    (target/'SHA256SUMS').write_text(f"{parsed['sha256']}  code.txt\n{original_hash}  originals/{original_hash}.bin\n")
    return metadata


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('source');p.add_argument('target')
    for k in ('q','n','R','M'):p.add_argument(k,type=int)
    p.add_argument('--source-commit')
    a=p.parse_args()
    print(json.dumps(ingest(a.source,a.target,a.q,a.n,a.R,a.M,a.source_commit),indent=2))
