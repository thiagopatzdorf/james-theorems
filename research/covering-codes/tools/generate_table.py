#!/usr/bin/env python3
"""Exact arithmetic; audit-verified bounds and documentary bounds stay distinct."""
import argparse
import csv
from fractions import Fraction
import io
import json
from math import comb
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
CASES=[(7,9,4,1351,264,1475,241),(4,10,4,192,62,208,51),
       (5,7,2,500,236,525,236),(5,9,3,1250,354,1275,354),
       (5,10,4,625,177,875,158),(5,9,4,250,64,255,62),
       (5,9,5,50,19,55,16),(7,8,3,1893,471,2337,471)]


def rows():
    out=[]
    for q,n,R,M,published_lb,published_ub,rechecked_lb in CASES:
        V=sum(comb(n,i)*(q-1)**i for i in range(R+1))
        S=Fraction(q**n,V)
        sphere=(q**n+V-1)//V
        # Secondary literature constructions were not replayed in this audit.
        prior=1475 if (q,n,R)==(7,9,4) else None
        # Unconditional explicit construction: free first n-R symbols, zero tail.
        fallback=q**(n-R)
        directory=ROOT/f'certificates/q{q}_n{n}_r{R}_m{M}'
        verified=False
        try:
            import hashlib
            a=json.loads((directory/'verification-a.json').read_text())
            b=json.loads((directory/'verification-b.json').read_text())
            sha=hashlib.sha256((directory/'code.txt').read_bytes()).hexdigest()
            keys=('q','n','R','M_parsed','M_unique','duplicates','invalid_lines','ambient_words','uncovered','max_min_distance','sha256')
            verified=all(a[k]==b[k] for k in keys) and a['sha256']==sha and a['uncovered']==0 and a['invalid_lines']==0 and a['M_parsed']==M and a['exhaustive'] and b['exhaustive'] and [a[k] for k in ('q','n','R')]==[q,n,R]
        except (OSError,KeyError,ValueError):
            pass
        ub=min(M,prior or fallback) if verified else (prior or fallback)
        d=dict(q=q,n=n,R=R,V_q_n_R=V,sphere_ratio=str(S),sphere_bound=sphere,
               strongest_verified_lower_bound=max(sphere,rechecked_lb),
               source_lb='sphere counting' if rechecked_lb==sphere else f'exact rational replay: literature-artifacts/marosi-v3/cert_q{q}_n{n}_R{R}.json',
               prior_verified_upper_bound=prior,
               source_ub='Marosi v3 ancillary code; independent BFS and published dilation checker' if prior else None,
               published_lower_bound=published_lb,published_upper_bound=published_ub,
               published_source='Marosi v3 / Gijswijt–Polak v2 / Kéri 2011; see literature.md',
               our_candidate_upper_bound=M,candidate_verified=verified,formal_verified=False,
               alpha_lower=str(Fraction(max(sphere,rechecked_lb),1)/S),
               alpha_upper=str(Fraction(ub,1)/S),upper_bound_used_for_alpha=ub,
               alpha_upper_evidence='two independent exhaustive candidate checks' if verified else ('rechecked prior code' if prior else 'elementary zero-tail construction'),
               candidate_alpha_if_valid=str(Fraction(M,1)/S),
               novelty_status='CANDIDATE_NEW_UPPER_BOUND' if verified and prior else 'NOVELTY_UNRESOLVED',status='COMPUTATIONALLY_VERIFIED' if verified else 'ARTIFACT_MISSING')
        out.append(d)
    return out


def artifacts():
    r=rows();j=json.dumps(r,indent=2,ensure_ascii=False)+'\n'
    stream=io.StringIO();w=csv.DictWriter(stream,fieldnames=list(r[0]),lineterminator="\n");w.writeheader();w.writerows(r)
    md='| q | n | R | V | sphere ratio S | sphere LB | rechecked LB | rechecked prior UB | published LB–UB | candidate | verified | alpha interval (verified) |\n'
    md+='|---:|---:|---:|---:|---|---:|---:|---:|---|---:|---|---|\n'
    tex='\\begin{tabular}{rrrrrrl}\n\\hline\n$q$ & $n$ & $R$ & Candidate & Rechecked LB & Rechecked UB & Published interval\\\\\n\\hline\n'
    for x in r:
        md+=f"| {x['q']} | {x['n']} | {x['R']} | {x['V_q_n_R']} | {x['sphere_ratio']} | {x['sphere_bound']} | {x['strongest_verified_lower_bound']} | {x['prior_verified_upper_bound'] or '—'} | {x['published_lower_bound']}–{x['published_upper_bound']} | {x['our_candidate_upper_bound']} | {x['candidate_verified']} | {x['alpha_lower']} ≤ alpha ≤ {x['alpha_upper']} |\n"
        tex+=f"{x['q']} & {x['n']} & {x['R']} & {x['our_candidate_upper_bound']} & {x['strongest_verified_lower_bound']} & {x['prior_verified_upper_bound'] or '--'} & {x['published_lower_bound']}--{x['published_upper_bound']}\\\\\n"
    tex+='\\hline\n\\end{tabular}\n'
    return {'bounds.json':j,'bounds.csv':stream.getvalue(),'bounds.md':md,'preprint/bounds-table.tex':tex}


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--check',action='store_true');a=p.parse_args()
    for path,content in artifacts().items():
        target=ROOT/path
        if a.check:
            if not target.exists() or target.read_text()!=content:raise SystemExit(f'stale table: {path}')
        else:target.write_text(content)
