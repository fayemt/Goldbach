#!/usr/bin/env python3
"""
replicate_tail.py — reproduce the tail inequality at a chosen even integer scale.

This script provides a unified interface for the numeric verification used in our
Goldbach project.  It combines the features of the original ``full`` and
``strict`` releases by allowing either a fast decimal computation or an exact
rational evaluation of the harmonic sum \sum_{q\le Q}1/(q\varphi(q)).  It
supports optional high–precision diagnostics, a baseline assertion at
N*=4×10^{18}, and the ability to override the target number N and
configurable constants via a JSON file.  All constants and their provenance are
documented in ``CITATIONS.md`` and Appendix C of the paper.  See the
repository ``README.md`` for usage examples.

Key features:

* Computes Q=floor(N^{1/5}) and R=N^{3/5}.
* Evaluates the harmonic sum S(Q) either exactly (fractions) or using Decimal.
* Uses explicit envelopes E_trivial and E_uniform.
* Calculates major–arc error and compares to the allowed share.
* Optional strict diagnostics: high‑precision vs fraction sums and monotonicity.
* Optional baseline assertion at N*=4×10^{18}.
"""

from __future__ import annotations
import argparse
import json
import math
import pathlib
import sys
from decimal import Decimal, getcontext, localcontext
from fractions import Fraction
from typing import Dict, List, Tuple

# --- number–theoretic helpers ---
def int_nth_root_floor(n: int, k: int) -> int:
    if n < 0 or k <= 0:
        raise ValueError("n must be ≥0 and k≥1")
    if n < 2:
        return n
    lo, hi = 0, 1
    while hi ** k <= n:
        hi <<= 1
    while hi - lo > 1:
        mid = (lo + hi) // 2
        if mid ** k <= n:
            lo = mid
        else:
            hi = mid
    return lo

def sieve_phi(Q: int) -> List[int]:
    if Q < 0:
        raise ValueError("Q must be non‑negative")
    phi = list(range(Q + 1))
    for p in range(2, Q + 1):
        if phi[p] == p:
            for k in range(p, Q + 1, p):
                phi[k] -= phi[k] // p
    return phi

def sieve_phi_sum(Q: int) -> Tuple[List[int], float]:
    if Q < 1:
        return [0, 1], 0.0
    phi = list(range(Q + 1))
    for p in range(2, Q + 1):
        if phi[p] == p:
            for k in range(p, Q + 1, p):
                phi[k] -= phi[k] // p
    S = 0.0
    for q in range(2, Q + 1):
        ph = phi[q]
        S += 1.0 / (q * ph)
    return phi, S

def harmonic_sum_decimal(Q: int, prec: int = 50) -> Decimal:
    if Q < 0:
        raise ValueError("Q must be non‑negative")
    getcontext().prec = prec
    phi = sieve_phi(Q)
    S = Decimal(0)
    for q in range(2, Q + 1):
        ph = phi[q]
        S += Decimal(1) / (Decimal(q) * Decimal(ph))
    return S

def harmonic_sum_fraction(Q: int) -> Fraction:
    if Q < 0:
        raise ValueError("Q must be non‑negative")
    phi = sieve_phi(Q)
    S = Fraction(0, 1)
    for q in range(2, Q + 1):
        ph = phi[q]
        S += Fraction(1, q * ph)
    return S

# --- envelope functions ---
def E_trivial(N: float, L: float) -> float:
    return N * L + N

def E_uniform(N: float, L: float) -> float:
    return N / (160.0 * L)

# --- core computation ---
def compute_tail_margins(
    N_int: int, K: float, S_floor: float, C_W: float,
    *, method: str = "decimal", prec: int = 50
) -> Dict[str, float]:
    if isinstance(N_int, float):
        N_int = int(N_int)
    if not isinstance(N_int, int) or N_int <= 0:
        raise ValueError("N must be a positive integer")

    Q = int_nth_root_floor(N_int, 5)
    if method == "fraction":
        S_Qm1 = harmonic_sum_fraction(Q - 1) if Q > 1 else Fraction(0, 1)
        S_Q = harmonic_sum_fraction(Q)
        S_Qp1 = harmonic_sum_fraction(Q + 1)
        if not (S_Qm1 < S_Q < S_Qp1):
            raise AssertionError("Harmonic sum is not strictly increasing")
        S_harm = float(S_Q)
    else:
        with localcontext() as ctx:
            ctx.prec = prec
            S_Qm1 = harmonic_sum_decimal(Q - 1, prec) if Q > 1 else Decimal(0)
            S_Q = harmonic_sum_decimal(Q, prec)
            S_Qp1 = harmonic_sum_decimal(Q + 1, prec)
        if not (S_Qm1 < S_Q < S_Qp1):
            raise AssertionError("Harmonic sum is not strictly increasing in decimal mode")
        S_harm = float(S_Q)

    N_float = float(N_int)
    L = math.log(N_float)
    R = N_float ** 0.6
    E_t = E_trivial(N_float, L)
    E_u = E_uniform(N_float, L)

    EMA_t = (C_W / R) * E_t * S_harm
    EMA_u = (C_W / R) * E_u * S_harm
    share = (S_floor / (8.0 * K)) * N_float / (L ** 2)

    return {
        "constants": {"K": K, "S_floor": S_floor, "C_W": C_W, "method": method, "prec": prec},
        "N": N_float,
        "logN": L,
        "Q": Q,
        "R": R,
        "sum_q": S_harm,
        "EMA_trivial": EMA_t,
        "EMA_uniform": EMA_u,
        "share": share,
        "ratio_trivial": EMA_t / share,
        "ratio_uniform": EMA_u / share,
    }

def strict_diagnostics(N_int: int, base_prec: int = 50, hi_prec: int = 120, kmax: int = 5) -> Dict[str, object]:
    if isinstance(N_int, float):
        N_int = int(N_int)
    if N_int <= 0:
        raise ValueError("N must be positive for diagnostics")
    Q = int_nth_root_floor(N_int, 5)
    S_dec: Dict[int, Dict[int, Decimal]] = {}
    for prec in (base_prec, hi_prec):
        S_dec[prec] = {}
        for k in range(-kmax, kmax + 1):
            q = Q + k
            if q < 1:
                continue
            S_dec[prec][q] = harmonic_sum_decimal(q, prec)
    S_frac_Q = harmonic_sum_fraction(Q)
    deltas: Dict[int, str] = {}
    for k in range(1, kmax + 1):
        d = S_dec[hi_prec][Q + k] - S_dec[hi_prec][Q + k - 1]
        deltas[k] = str(d)
    return {
        "Q": Q,
        "S_decimal_base": str(S_dec[base_prec][Q]),
        "S_decimal_hi": str(S_dec[hi_prec][Q]),
        "S_fraction_Q": f"{S_frac_Q.numerator}/{S_frac_Q.denominator}",
        "S_decimal_minus_fraction_abs": str(abs(
            Decimal(S_dec[hi_prec][Q]) -
            Decimal(S_frac_Q.numerator) / Decimal(S_frac_Q.denominator)
        )),
        "monotone_deltas_hi_prec": deltas,
    }

def main(argv: List[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--constants",
        type=pathlib.Path,
        default=pathlib.Path(__file__).with_name("constants.json"),
        help=("JSON file with keys N_star_str or N_star, K, S_floor, C_W."),
    )
    parser.add_argument(
        "--N",
        type=str,
        default=None,
        help=("Override N as an integer string or floating‑point literal."),
    )
    parser.add_argument(
        "--method",
        choices=["decimal", "fraction"],
        default="decimal",
        help="Method to compute S(Q): decimal (fast) or fraction (exact).",
    )
    parser.add_argument(
        "--prec",
        type=int,
        default=50,
        help="Decimal precision when method=decimal.",
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help=(
            "Run extra diagnostics: high‑precision decimal vs fraction sums and "
            "report monotone deltas around Q."
        ),
    )
    parser.add_argument(
        "--assert-baseline",
        action="store_true",
        help=(
            "At N*=4e18, assert that S(Q) matches the recorded baseline value "
            "1.20348665358 within 1e-10.  See Appendix C."
        ),
    )
    args = parser.parse_args(argv)

    defaults: Dict[str, object] = {
        "N_star_str": "4000000000000000000",
        "N_star": 4e18,
        "K": 10.0,
        "S_floor": 1.2,
        "C_W": 2.0,
    }
    if args.constants.exists():
        try:
            cfg = json.loads(args.constants.read_text())
            defaults.update(cfg)
        except Exception as e:
            print(f"[warn] Failed to read constants.json: {e}", file=sys.stderr)

    if args.N is not None:
        N_input = args.N
    else:
        N_input = str(defaults.get("N_star_str", defaults.get("N_star", "4000000000000000000")))
    try:
        if N_input.isdigit():
            N_int = int(N_input)
        else:
            N_int = int(float(N_input))
    except Exception:
        raise ValueError(f"Unable to parse N='{N_input}' as an integer")

    K = float(defaults.get("K", 10.0))
    S_floor = float(defaults.get("S_floor", 1.2))
    C_W = float(defaults.get("C_W", 2.0))

    result = compute_tail_margins(
        N_int,
        K,
        S_floor,
        C_W,
        method=args.method,
        prec=args.prec,
    )
    print(result)

    if args.strict:
        diagnostics = strict_diagnostics(
            N_int, base_prec=max(50, args.prec), hi_prec=max(120, args.prec + 70), kmax=5
        )
        print({"strict": diagnostics})

    if args.assert_baseline and abs(float(N_int) - 4.0e18) < 0.5e18:
        Q = int_nth_root_floor(N_int, 5)
        S_baseline = 1.20348665358
        _, S_value = sieve_phi_sum(Q)
        if abs(S_value - S_baseline) > 1e-10:
            raise AssertionError(
                f"S(Q) mismatch: got {S_value:.12f}, expected {S_baseline:.12f}"
            )

    ok = (result["ratio_trivial"] < 1e-3) and (result["ratio_uniform"] < 1e-8)
    return 0 if ok else 2

if __name__ == "__main__":
    sys.exit(main())
