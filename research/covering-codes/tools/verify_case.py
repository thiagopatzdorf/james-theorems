#!/usr/bin/env python3
"""Fail-closed end-to-end case verification; no missing artifact becomes PASS."""
import argparse
import hashlib
import json
import re
from pathlib import Path
import subprocess
import sys

ROOT=Path(__file__).resolve().parents[1]


def run(case, computational_only=False):
    identity=re.fullmatch(r'q([0-9]+)_n([0-9]+)_r([0-9]+)_m([0-9]+)',case)
    if not identity:raise ValueError('invalid case identity')
    d=ROOT/'certificates'/case
    for f in ('code.txt','metadata.json','SHA256SUMS'):
        if not (d/f).is_file():
            print(json.dumps(dict(status='BLOCKED_BY_MISSING_ARTIFACT',missing=str(d/f))))
            return 2
    meta=json.loads((d/'metadata.json').read_text())
    if [meta.get(k) for k in ('q','n','R','M')]!=list(map(int,identity.groups())):
        raise ValueError('named-case parameters mismatch')
    sha=hashlib.sha256((d/'code.txt').read_bytes()).hexdigest()
    if sha!=meta['code_sha256']:raise ValueError('metadata hash mismatch')
    subprocess.run(['sha256sum','--check','SHA256SUMS'],cwd=d,check=True)
    (ROOT/'build').mkdir(exist_ok=True)
    binary=ROOT/'build/verify_b'
    subprocess.run(['g++','-std=c++17','-O3',str(ROOT/'verifiers/verify_b.cpp'),'-lcrypto','-o',str(binary)],check=True)
    params=[str(meta[k]) for k in ('q','n','R')]
    reports=[]
    commands=[['python3',str(ROOT/'verifiers/verify_a.py'),*params,str(d/'code.txt'),'--expected-m',str(meta['M']),'--method','transform'],
              [str(binary),*params,str(d/'code.txt')]]
    for name,command in zip(('a','b'),commands):
        proc=subprocess.run(command,capture_output=True,text=True)
        # Preserve failure reports too; a failed checker cannot promote the case.
        (d/f'verification-{name}.json').write_text(proc.stdout)
        if proc.returncode:print(proc.stderr,file=sys.stderr);return 1
        reports.append(json.loads(proc.stdout))
    for key in ('sha256','q','n','R','M_unique','M_parsed','duplicates','invalid_lines',
                'ambient_words','uncovered','max_min_distance'):
        if reports[0][key]!=reports[1][key]:raise ValueError(f'checker disagreement: {key}')
    if reports[0]['sha256']!=sha:raise ValueError('checker input mismatch')
    if reports[0]['uncovered']!=0 or reports[0]['M_parsed']!=meta['M']:return 1
    if case=='q7_n9_r4_m1351':
        subprocess.run([sys.executable,str(ROOT/'tools/witness_certificate.py'),str(d)],check=True)
        subprocess.run([sys.executable,str(ROOT/'tools/partition_certificate.py'),str(d)],check=True)
    elif (d/'partition-metadata.json').is_file():
        subprocess.run([sys.executable,str(ROOT/'tools/certify_fixed_base_candidate.py'),str(d)],check=True)
    if computational_only:
        print(json.dumps(dict(status='COMPUTATIONALLY_VERIFIED',formal='NOT_CLAIMED',sha256=sha)))
        return 0
    subprocess.run(['lake','build'],cwd=ROOT/'formal',check=True)
    subprocess.run(['lake','env','lean','Audit.lean'],cwd=ROOT/'formal',check=True)
    # Ordinary adapter/tiny build is NOT principal certification.
    manifest=ROOT/'formal/PrincipalManifest.json'
    if not manifest.is_file():
        print(json.dumps(dict(status='COMPUTATIONALLY_VERIFIED',formal='BLOCKED_MISSING_REPLAY',sha256=sha)))
        return 3
    m=json.loads(manifest.read_text())
    if m.get('code_sha256')!=sha:raise ValueError('formal certificate/code mismatch')
    proof=ROOT/'formal'/m['source']
    if hashlib.sha256(proof.read_bytes()).hexdigest()!=m['source_sha256']:
        raise ValueError('formal source hash mismatch')
    subprocess.run(['lake','build'],cwd=ROOT/'formal',check=True)
    subprocess.run(['lake','env','lean',m['source']],cwd=ROOT/'formal',check=True)
    # Require an unconditional theorem of the exact target type; no hypothesis adapter.
    import tempfile
    with tempfile.NamedTemporaryFile(mode='w',suffix='.lean',dir=ROOT/'formal') as f:
        f.write('import CoveringRecords\nimport '+m['module']+'\n')
        f.write('example : CoveringCodes.QaryKUpper '+ ' '.join(params)+f" {meta['M']} := {m['theorem']}\n")
        f.write('#print axioms '+m['theorem']+'\n');f.flush()
        result=subprocess.run(['lake','env','lean',f.name],cwd=ROOT/'formal',check=True,
                              capture_output=True,text=True)
        # Standard logical axioms only; reject native evaluator trust additions.
        groups=re.findall(r'depends on axioms:\s*\[([^\]]*)\]',result.stdout)
        if not groups and 'does not depend on any axioms' not in result.stdout:
            raise ValueError('could not audit theorem axioms')
        allowed={'propext','Classical.choice','Quot.sound'}
        for group in groups:
            if set(x.strip() for x in group.split(',') if x.strip())-allowed:
                raise ValueError('nonstandard theorem axiom dependencies')
    print(json.dumps(dict(status='FORMALLY_VERIFIED_CONSTRUCTION',sha256=sha)))
    return 0


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('case');p.add_argument('--computational-only',action='store_true');a=p.parse_args()
    try:sys.exit(run(a.case,a.computational_only))
    except (OSError,ValueError,KeyError,subprocess.CalledProcessError) as e:
        print(json.dumps({'status':'ERROR','error':str(e)}));sys.exit(1)
