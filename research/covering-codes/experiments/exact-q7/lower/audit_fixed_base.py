#!/usr/bin/env python3
"""Independent literal-Hamming audit of fixed-base quotient counting bound."""
from pathlib import Path
import hashlib,itertools,json,time,math,copy
from fractions import Fraction
import numpy as np
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
DATA=ROOT/'certificates/q7_n9_r4_m1351'
GLOBAL=HERE.parent/'global'
ROWS=np.array([[1,1,1,1,1,1,1,1,1],[0,2,3,2,3,6,0,1,1],[0,5,3,0,6,4,4,3,5]],dtype=np.int16)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 start=time.perf_counter();info=json.loads((GLOBAL/'kernel-analysis.json').read_text())
 code=np.array([[int(c) for c in s] for s in (DATA/'code.txt').read_text().splitlines()],dtype=np.int16)
 assert sha(DATA/'code.txt')==info['code_sha256']
 kernel=np.frombuffer((GLOBAL/'kernel.u16le').read_bytes(),dtype='<u2')
 coverage=np.frombuffer((GLOBAL/'center-coverage.u16le').read_bytes(),dtype='<u2')
 quotient=np.frombuffer((DATA/'quotient.u16le').read_bytes(),dtype='<u2')
 assert sha(GLOBAL/'kernel.u16le')==info['kernel_sha256']
 assert sha(GLOBAL/'center-coverage.u16le')==info['coverage_sha256']
 assert len(kernel)==len(coverage)==len(quotient)==7**6
 coefficients=np.array(list(itertools.product(range(7),repeat=3)),dtype=np.int16)
 span=(coefficients@ROWS)%7
 assert len(set(map(tuple,span)))==343
 assert set(map(tuple,span[:,:3]))==set(itertools.product(range(7),repeat=3))
 base=set(map(tuple,code[:1029])); assert len(base)==1029
 # Derive all cosets from actual code, independent of supplied metadata.
 remaining=base.copy(); representatives=[]
 while remaining:
  representative=np.array(min(remaining),dtype=np.int16)
  coset=set(map(tuple,(span+representative)%7))
  assert coset <= remaining
  representatives.append(representative.tolist());remaining-=coset
 assert len(representatives)==3
 ids=np.arange(7**6,dtype=np.int64)
 tail=np.stack([(ids//7**j)%7 for j in range(5,-1,-1)],axis=1).astype(np.int16)
 normalized=np.concatenate((np.zeros((7**6,3),dtype=np.int16),tail),axis=1)
 # Independent kernel: literal distances from every quotient representative
 # to all343spanwords; no Hamming-error-ball generator and no normalization.
 rebuilt=np.zeros(7**6,dtype=np.uint16)
 for word in span:
  rebuilt+=np.count_nonzero(normalized!=word,axis=1)<=4
 assert np.array_equal(rebuilt,kernel)
 assert int(rebuilt.sum())==182791
 hole_representatives=normalized[quotient==65535]
 assert len(hole_representatives)==27
 recomputed_coverage=np.zeros(7**6,dtype=np.uint32)
 packing_weights=np.array([7**j for j in range(5,-1,-1)],dtype=np.int64)
 for hole in hole_representatives:
  differences=(hole[3:]-tail)%7
  recomputed_coverage+=rebuilt[differences@packing_weights]
 assert np.array_equal(recomputed_coverage,coverage)
 words=np.concatenate([(span+r)%7 for r in hole_representatives],axis=0)
 assert len(set(map(tuple,words)))==9261
 # These are genuinely uncovered by the actual fixed1029wordbase.
 mindist=np.full(len(words),10,dtype=np.int16)
 for word in code[:1029]:
  mindist=np.minimum(mindist,np.count_nonzero(words!=word,axis=1))
 assert np.all(mindist>4)
 rng=np.random.default_rng(20261002)
 samples=rng.integers(0,7,size=(200,9),dtype=np.int16)
 samples=np.concatenate((samples,np.array([[int(c) for c in info['attaining_center']]],dtype=np.int16)))
 sample_checks=[]
 weights=np.array([7**j for j in range(5,-1,-1)],dtype=np.int64)
 for word in samples:
  # Obtain unique spanword with matching prefix by search, no coefficientformula.
  matches=span[np.all(span[:,:3]==word[:3],axis=1)]
  assert len(matches)==1
  normalized_word=(word-matches[0])%7
  packed=int(normalized_word[3:]@weights)
  count=int(np.count_nonzero(np.count_nonzero(words!=word,axis=1)<=4))
  assert count==int(coverage[packed])
  sample_checks.append({'center': ''.join(map(str,word)), 'quotient': packed, 'literal_count': count})
 # Direct check of the set's invariance under all343translations; then each
 # quotientcenterrep represents343ambientcenters with identical holecoverage.
 hole_set=set(map(tuple,words))
 for translation in span:
  assert set(map(tuple,(words+translation)%7))==hole_set
 histogram={str(k):int(v) for k,v in zip(*np.unique(coverage,return_counts=True))}
 assert histogram==info['coverage_histogram'] and sum(histogram.values())==117649
 assert int(coverage.max())==68
 patch=(9261+68-1)//68
 assert patch==137 and 1029+patch==1166
 dual=json.loads((GLOBAL/'dual-certificate.json').read_text())
 matrix=np.stack([rebuilt[((hole[3:]-tail)%7)@packing_weights] for hole in hole_representatives]).astype(np.int64)
 def check_dual(certificate):
  if certificate['original_code_sha256']!=sha(DATA/'code.txt'):raise ValueError('code hash')
  expected=[''.join(map(str,h)) for h in hole_representatives]
  if certificate['hole_orbit_representatives']!=expected:raise ValueError('orbit order')
  if len(certificate['weights'])!=27:raise ValueError('weights count')
  weights=[]
  for item in certificate['weights']:
   if not isinstance(item['numerator'],int) or not isinstance(item['denominator'],int):raise ValueError('noninteger fraction')
   if item['numerator']<0 or item['denominator']<=0:raise ValueError('weight sign')
   weights.append(Fraction(item['numerator'],item['denominator']))
  den=math.lcm(*(w.denominator for w in weights))
  nums=[w.numerator*(den//w.denominator) for w in weights]
  # Guaranteed safe exact machine-integer dot product, or explicitly reject.
  if sum(nums)*343 >= 2**63:raise ValueError('integer capacity')
  loads=np.array(nums,dtype=np.int64)@matrix
  if int(loads.max())>den:raise ValueError('constraint violation')
  objective=343*sum(weights,Fraction())
  bound=(objective.numerator+objective.denominator-1)//objective.denominator
  if str(objective)!=certificate['fractional_patch_bound']:raise ValueError('objective claim')
  if bound!=certificate['integer_patch_lower_bound'] or 1029+bound!=certificate['fixed_base_total_lower_bound']:raise ValueError('bound claim')
  return {'status':'PASS','scope':'FIXED_BASE_ONLY; not unrestricted K7(9,4)',
   'independent_kernel_strategy':'literal Hamming representative-span distances',
   'quotient_columns_checked':117649,'ambient_centers_represented':40353607,
   'integer_common_denominator':den,'exact_maximum_constraint_numerator':int(loads.max()),
   'minimum_constraint_slack_numerator':den-int(loads.max()),
   'fractional_patch_lower_bound':str(objective),'integer_patch_lower_bound':bound,
   'fixed_base_total_lower_bound':1029+bound,'certificate_sha256':sha(GLOBAL/'dual-certificate.json')}
 dual_result=check_dual(dual)
 mutations=[]
 forged=copy.deepcopy(dual);forged['weights'][0]['numerator']=-1;mutations.append(('negative_weight',forged))
 forged=copy.deepcopy(dual);forged['weights'][0]['denominator']=0;mutations.append(('zero_denominator',forged))
 forged=copy.deepcopy(dual);forged['hole_orbit_representatives'][0],forged['hole_orbit_representatives'][1]=forged['hole_orbit_representatives'][1],forged['hole_orbit_representatives'][0];mutations.append(('orbit_order_swapped',forged))
 forged=copy.deepcopy(dual)
 for item in forged['weights']:item['numerator']*=2
 mutations.append(('infeasible_doubled_weights',forged))
 forged=copy.deepcopy(dual);forged['integer_patch_lower_bound']=154;mutations.append(('inflated_bound_claim',forged))
 attacks={}
 for name,forged in mutations:
  try:check_dual(forged)
  except ValueError as err:attacks[name]=str(err)
  else:raise AssertionError('Forgery accepted: '+name)
 dual_result['forgeries_rejected']=attacks
 (HERE/'fixed-base-dual-audit.json').write_text(json.dumps(dual_result,indent=2)+'\n')
 result={'status':'PASS','scope':'FIXED_BASE_ONLY; no global K7(9,4) lower bound',
 'base_words':1029,'holes':9261,'hole_orbits':27,'kernel_rechecked_pairs':117649*343,
 'kernel_strategy':'literal Hamming distances representatives versus all343spanwords',
 'kernel_hash_matches':True,'center_coverage_hash_matches':True,
 'random_literal_centers_checked':200,'maximizer_literal_checked':True,
 'all343_hole_translations_checked':True,'each_hole_min_distance_to_actual_base':int(mindist.min()),
 'maximum_holes_covered_by_one_arbitrary_center':68,'fixed_base_patch_lower_bound':137,
 'fixed_base_total_lower_bound':1166,'global_lower_bound_claimed':False,
 'source_sha256':sha(GLOBAL/'analyze_kernel.py'),'analysis_json_sha256':sha(GLOBAL/'kernel-analysis.json'),
 'kernel_sha256':sha(GLOBAL/'kernel.u16le'),'coverage_sha256':sha(GLOBAL/'center-coverage.u16le'),
 'code_sha256':sha(DATA/'code.txt'),'quotient_sha256':sha(DATA/'quotient.u16le'),
 'derived_coset_representatives':representatives,'samples':sample_checks,
 'runtime_seconds':time.perf_counter()-start,'paid_infrastructure_spend_usd':0}
 (HERE/'fixed-base-audit.json').write_text(json.dumps(result,indent=2)+'\n')
 print(json.dumps({k:v for k,v in result.items() if k!='samples'},indent=2))
if __name__=='__main__':main()
