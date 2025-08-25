\
#!/usr/bin/env python3
from __future__ import annotations
import argparse, math
def phi(n:int)->int:
    x=n; r=n; p=2
    while p*p<=x:
        if x%p==0:
            while x%p==0: x//=p
            r-=r//p
        p+=1 if p==2 else 2
    if x>1: r-=r//x
    return r
def E_trivial(N,L): return N*L+N
def E_uniform(N,L): return N/(160.0*L)
if __name__=="__main__":
    ap=argparse.ArgumentParser()
    ap.add_argument("--N",type=float,default=4e18); ap.add_argument("--K",type=float,default=10.0)
    ap.add_argument("--S",type=float,default=1.2); ap.add_argument("--Wsup",type=float,default=1.0)
    ap.add_argument("--CW",type=float,default=None); ap.add_argument("--Rexp",type=float,default=0.6)
    ap.add_argument("--Qcap",type=int,default=None); ap.add_argument("--model",choices=["trivial","uniform"],default="uniform")
    ns=ap.parse_args(); N=ns.N; L=math.log(N); Qcap=ns.Qcap if ns.Qcap is not None else int(N**0.2)
    R=N**ns.Rexp; CW=ns.CW if ns.CW is not None else 2.0*ns.Wsup
    s=0.0
    for q in range(2,Qcap+1):
        ph=phi(q)
        if ph: s += 1.0/(q*ph)
    E=E_uniform(N,L) if ns.model=="uniform" else E_trivial(N,L)
    EMA=(CW/R)*E*s; share=(ns.S/(8.0*ns.K))*N/(L**2)
    print({"N":N,"Qcap":Qcap,"EMA":EMA,"Share":share,"Ratio":EMA/share})
