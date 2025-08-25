\
#!/usr/bin/env python3
from __future__ import annotations
import argparse, csv, math, pathlib
def phi(n:int)->int:
    x=n; r=n; p=2
    while p*p<=x:
        if x%p==0:
            while x%p==0: x//=p
            r-=r//p
        p+=1 if p==2 else 2
    if x>1: r-=r//x
    return r
def E_trivial(N,L): return N*L + N
def E_uniform(N,L): return N/(160.0*L)
class PerQ:
    def __init__(self): self.rows={}
    def load(self, path:pathlib.Path):
        with path.open(newline="") as f:
            rd=csv.DictReader(f)
            for row in rd: self.rows[int(row["q"])]=row
    def Eq(self,q,N,L):
        r=self.rows.get(q)
        if not r: raise KeyError(q)
        form=r["form"]; c1=float(r["c1"]); c2=float(r["c2"])
        if form=="cNoverlog": return c1*N/L
        if form=="cNlog": return c1*N*L
        if form=="affine": return c1*N*L + c2*N
        return c1*N/L
if __name__=="__main__":
    ap=argparse.ArgumentParser()
    ap.add_argument("--N",type=float,default=4e18); ap.add_argument("--K",type=float,default=10.0); ap.add_argument("--S",type=float,default=1.2)
    ap.add_argument("--Wsup",type=float,default=1.0); ap.add_argument("--CW",type=float,default=None); ap.add_argument("--Rexp",type=float,default=0.6)
    ap.add_argument("--Qcap",type=int,default=1000); ap.add_argument("--csv",type=pathlib.Path,default=pathlib.Path(__file__).with_name("data").joinpath("per_q_constants.csv"))
    ap.add_argument("--fallback",choices=["uniform","trivial"],default="uniform")
    ns=ap.parse_args()
    N=ns.N; L=math.log(N); Qcap=ns.Qcap; R=N**ns.Rexp; CW=ns.CW if ns.CW is not None else 2.0*ns.Wsup
    perq=PerQ(); 
    if ns.csv.exists(): perq.load(ns.csv)
    ema=0.0; missing=0
    for q in range(2,Qcap+1):
        try: Eq=perq.Eq(q,N,L)
        except KeyError:
            missing+=1; Eq = E_uniform(N,L) if ns.fallback=="uniform" else E_trivial(N,L)
        ema += Eq/(q*phi(q))
    ema *= (CW/R); share=(ns.S/(8.0*ns.K))*N/(L**2)
    print({"N":N,"Qcap":Qcap,"Missing":missing,"EMA":ema,"Share":share,"Ratio":ema/share})
