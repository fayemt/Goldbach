\
#!/usr/bin/env python3
from __future__ import annotations
import argparse
def phi(n: int) -> int:
    x=n; r=n; p=2
    while p*p<=x:
        if x%p==0:
            while x%p==0: x//=p
            r-=r//p
        p+=1 if p==2 else 2
    if x>1: r-=r//x
    return r
def harmonic_sum_phi(Q: int) -> float:
    s=0.0
    for q in range(2,Q+1):
        ph=phi(q)
        if ph: s+=1.0/(q*ph)
    return s
if __name__=="__main__":
    ap=argparse.ArgumentParser(); ap.add_argument("Q",type=int,nargs="?",default=5300)
    ns=ap.parse_args(); print(f"S({ns.Q}) = {harmonic_sum_phi(ns.Q):.12f}")
