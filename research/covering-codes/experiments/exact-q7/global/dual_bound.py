#!/usr/bin/env python3
"""All-center symmetry-reduced fixed-base LP, rational certificate only."""
from pathlib import Path
import sys,json,math,hashlib,time
from fractions import Fraction
import numpy as np
from scipy.optimize import linprog
D=Path(__file__).resolve().parent;ROOT=D.parents[2];sys.path.insert(0,str(ROOT/'tools'))
from partition_certificate import representatives
start=time.monotonic();code=ROOT/'certificates/q7_n9_r4_m1351';q=np.frombuffer((code/'quotient.u16le').read_bytes(),dtype='<u2');reps=representatives().astype(np.int16);holes=reps[q==65535,3:];kernel=np.frombuffer((D/'kernel.u16le').read_bytes(),dtype='<u2');powers=np.array([7**i for i in range(5,-1,-1)],dtype=np.int64)
A=np.stack([kernel[((h-reps[:,3:])%7)@powers] for h in holes]).astype(np.int64)
# Exact symmetry: each hole orbit contains343points and column j gives number
# covered in eachorbitby ANYindividualcenterwithquotient j.
selected=set(np.argsort(-A.sum(axis=0))[:500].tolist());iterations=[]
for it in range(100):
 ids=sorted(selected);res=linprog(-343*np.ones(27),A_ub=A[:,ids].T,b_ub=np.ones(len(ids)),bounds=(0,None),method='highs',options={'time_limit':30})
 if not res.success:raise RuntimeError(res.message)
 loads=res.x@A;bad=np.flatnonzero(loads>1+1e-8);iterations.append(dict(iteration=it,constraints=len(ids),objective=-res.fun,violations=len(bad),max_load=float(loads.max())))
 if not len(bad):break
 selected.update(bad[np.argsort(-loads[bad])[:500]].tolist())
else:raise RuntimeError('cutting plane iterationcap')
weights=[Fraction(float(v)).limit_denominator(10**7) for v in res.x]
# Round-off cannot create fake feasibility: rescale by EXACT maximumload.
denom=math.lcm(*(w.denominator for w in weights));nums=[w.numerator*(denom//w.denominator) for w in weights]
loads_exact=[sum(int(A[i,j])*nums[i] for i in range(27)) for j in range(7**6)];scale=max(denom,max(loads_exact));weights=[Fraction(num,scale) for num in nums]
weights=[Fraction((w*10**6).numerator//(w*10**6).denominator,10**6) for w in weights]
objective=343*sum(weights,Fraction());lb=math.ceil(objective)
out=dict(scope='FIXED_BASE_ONLY; no globalK lower-bound claim',status='EXACT_RATIONAL_CERTIFICATE_PASS',original_code_sha256=hashlib.sha256((code/'code.txt').read_bytes()).hexdigest(),hole_orbit_representatives=['000'+''.join(map(str,h)) for h in holes],weights=[{'numerator':w.numerator,'denominator':w.denominator} for w in weights],fractional_patch_bound=str(objective),integer_patch_lower_bound=lb,fixed_base_total_lower_bound=1029+lb,all_quotient_centers_checked=7**6,max_constraint_before_safe_rescale=str(Fraction(max(loads_exact),denom)),iterations=iterations,runtime_seconds=time.monotonic()-start,argument='Give every point of hole orbit i weightlambda_i. Anyambientcenter coverssum_i A_ij lambda_i <=1. Covering9261holesthereforeneedsatleast343sum_i lambda_iwords.')
(D/'dual-certificate.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
