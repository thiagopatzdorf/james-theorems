#!/usr/bin/env python3
"""Bounded exact replay of HHSP2009 partition game, Lemmas15/16 + Theorem9.
Timeout is UNKNOWN, never winning/nonexistence. No heuristic prune.
"""
import argparse,itertools,json,time,math
from functools import lru_cache
from pathlib import Path
class BudgetExceeded(Exception):pass
class Game:
 def __init__(self,n,M,q,k,m=0,seconds=180):
  self.n,self.M,self.q,self.k,self.m=n,M,q,k,m
  self.deadline=time.monotonic()+seconds;self.states=0;self.boxes=0;self.partitions=0
 def tick(self):
  if time.monotonic()>self.deadline:raise BudgetExceeded
 @lru_cache(None)
 def win(self,d,counts):
  self.tick();self.states+=1
  if d==self.n:return True
  # There is no legal partition if the mandatory minimum exceeds M.
  if self.q*self.m>self.M:return True
  # Exact final-step test: P can put one endangered row in every class iff
  # count[k-1]>=q (and pad every class to m using remaining rows).
  if counts[-1]>=self.q:return False
  if d==self.n-1:return True
  # HHSP Lemma11: sufficient exact winning condition for two steps left.
  r=self.q-counts[-1]
  if d==self.n-2 and (counts[-2]+counts[-1]<=self.q+r*r-r-1 or self.M<=counts[-1]*self.m+r*r-1):return True
  # Exact conditional-expectation potential: each future uniform class choice
  # increments each row with probability1/q, even for adaptive partitions.
  # T picks a class no worse than the average; terminal bad-count<1 means0.
  steps=self.n-d
  potential=sum(counts[j]*sum(math.comb(steps,t)*(self.q-1)**(steps-t) for t in range(max(0,self.k-j),steps+1)) for j in range(self.k))
  if potential<self.q**steps:return True
  losing=[]
  for box in itertools.product(*(range(c+1) for c in counts)):
   self.tick();self.boxes+=1
   if sum(box)<self.m:continue
   if box[-1]>0:losing.append(box);continue
   nxt=tuple(counts[j]-box[j]+(box[j-1] if j else 0) for j in range(self.k))
   if not self.win(d+1,nxt):losing.append(box)
  # Exact losing partition search. Sorted indices remove permutations of
  # partition classes while allowing repeated count profiles.
  @lru_cache(None)
  def split(remaining,r,start):
   self.tick();self.partitions+=1
   if r==0:return not any(remaining)
   if sum(remaining)<r*self.m:return False
   for index in range(start,len(losing)):
    box=losing[index]
    if all(b<=c for b,c in zip(box,remaining)):
     if split(tuple(c-b for b,c in zip(box,remaining)),r-1,index):return True
   return False
  return not split(counts,self.q,0)

def labeled_oracle(n,M,q,k,m):
 # Independent enumeration: q^M assignments, retain concrete row IDs.
 partitions=[]
 for assignment in itertools.product(range(q),repeat=M):
  if min((assignment.count(label) for label in range(q)),default=0)>=m:partitions.append(assignment)
 @lru_cache(None)
 def win(d,multiplicities):
  if d==n:return True
  for assignment in partitions:
   any_good=False
   for label in range(q):
    nxt=tuple(v+(assignment[i]==label) for i,v in enumerate(multiplicities))
    if max(nxt,default=0)<k and win(d+1,nxt):any_good=True;break
   if not any_good:return False
  return True
 return win(0,(0,)*M)

def tiny_checks():
 results=[]
 for q in [2,3]:
  for n in [2,3,4]:
   for k in range(2,min(n,3)+1):
    for M in range(5):
     for m in range(M//q+1):
      g=Game(n,M,q,k,m,seconds=10)
      actual=g.win(0,(M,)+(0,)*(k-1))
      expected=labeled_oracle(n,M,q,k,m)
      assert actual==expected,(n,M,q,k,m,actual,expected)
      results.append({'n':n,'M':M,'q':q,'k':k,'m':m,'T_wins':actual})
 assert Game(3,1,2,2).win(0,(1,0))
 assert not Game(3,2,2,2).win(0,(2,0))
 return results

def replay(seconds):
 start=time.monotonic();chain=[];m=0;M=263;n=9;q=7;k=5
 while True:
  remaining=seconds-(time.monotonic()-start)
  if remaining<=0:return {'status':'UNKNOWN_BUDGET_EXCEEDED','chain':chain}
  g=Game(n,M,q,k,m,remaining)
  try:
   if g.win(0,(M,0,0,0,0)):
    chain.append({'m':m,'initial_T_wins':True})
    return {'status':'PASS','global_lower_bound':264,'chain':chain}
   # By monotonicity Lemma8, winning first-set cardinalities form an initial
   # interval. Enumerate to exhibit the boundary without trusting heuristics.
   largest=-1
   for a in range(M+1):
    if g.win(1,(M-a,a,0,0,0)):largest=a
    else:break
   chain.append({'m':m,'initial_T_wins':False,'largest_winning_first_set_size':largest})
   if largest<m:return {'status':'STRATEGY_INSUFFICIENT','chain':chain}
   m=largest+1
  except BudgetExceeded:
   return {'status':'UNKNOWN_BUDGET_EXCEEDED','global_lower_bound_claimed':False,
    'chain':chain,'current_minimum_class_size':m,'states_entered':g.states,
    'box_profiles_enumerated':g.boxes,'partition_subproblems':g.partitions,
    'winning_cache':str(g.win.cache_info()),'runtime_seconds':time.monotonic()-start}

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--seconds',type=float,default=120);ap.add_argument('--tiny-only',action='store_true');args=ap.parse_args()
 tiny=tiny_checks();out={'tiny_crosschecks':'PASS','tiny_cases_checked':len(tiny),'tiny_results':tiny}
 print('Tiny abstract-versus-concrete partition checks PASS:',len(tiny),flush=True)
 if not args.tiny_only:out['principal_replay']=replay(args.seconds)
 out['method']='Exact histogram game recursion, losing-class partitions, sorted class symmetry, HHSP Theorem9 minimum-class chain'
 out['scope']='A proven winning chain implies global lower264. Timeout does not establish any bound.'
 out['paid_infrastructure_spend_usd']=0
 (Path(__file__).parent/'game-replay.json').write_text(json.dumps(out,indent=2)+'\n')
 print(json.dumps({k:v for k,v in out.items() if k!='tiny_results'},indent=2),flush=True)
if __name__=='__main__':main()
