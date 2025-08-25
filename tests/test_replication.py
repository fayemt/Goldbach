"""
Unit tests for the Goldbach tail replication scripts.

These tests exercise both the fast decimal and exact fraction modes of
compute_tail_margins, verify monotonicity properties of the harmonic sum,
and check that the computed harmonic sum at Q=5253 matches the published
baseline to 1e-10.  They also ensure that the major–arc error ratios are
sufficiently small at the default parameters.
"""

from scripts.replicate_tail import (
    compute_tail_margins,
    sieve_phi_sum,
    int_nth_root_floor,
    harmonic_sum_decimal,
    harmonic_sum_fraction,
)

def test_phi_sum_baseline() -> None:
    # The baseline is defined at Q = floor(N^{1/5}) for N=4e18.  We compute Q
    N = int("4000000000000000000")
    Q = int_nth_root_floor(N, 5)
    assert Q == 5253
    _, S = sieve_phi_sum(Q)
    # Known value for S(5253) computed deterministically
    assert abs(S - 1.203486653584392) < 1e-10

def test_tail_margins_sanity() -> None:
    res = compute_tail_margins(
        int(4.0e18), 10.0, 1.2, 2.0, method="decimal", prec=50
    )
    assert abs(res["logN"] - 42.832826035) < 1e-6
    assert res["Q"] == 5253
    assert abs(res["sum_q"] - 1.203486653584392) < 1e-10
    assert res["ratio_trivial"] < 1e-3
    assert res["ratio_uniform"] < 1e-8

def test_integer_fifth_root() -> None:
    N = int("4000000000000000000")
    Q = int_nth_root_floor(N, 5)
    assert Q == 5253

def test_harmonic_sum_monotone_decimal() -> None:
    import decimal
    decimal.getcontext().prec = 80
    Q = 5253
    S_Qm1 = harmonic_sum_decimal(Q - 1, prec=80)
    S_Q = harmonic_sum_decimal(Q, prec=80)
    S_Qp1 = harmonic_sum_decimal(Q + 1, prec=80)
    assert S_Qm1 < S_Q < S_Qp1

def test_harmonic_sum_fraction_exact() -> None:
    Q = 5253
    S_frac = harmonic_sum_fraction(Q)
    assert S_frac.numerator > 0 and S_frac.denominator > 0
    approx = float(S_frac)
    assert 1.1 < approx < 1.3

def test_tail_ratios_decimal_and_fraction() -> None:
    N_int = int("4000000000000000000")
    r_dec = compute_tail_margins(
        N_int, 10.0, 1.2, 2.0, method="decimal", prec=80
    )
    r_frac = compute_tail_margins(
        N_int, 10.0, 1.2, 2.0, method="fraction"
    )
    assert r_dec["Q"] == 5253 == r_frac["Q"]
    assert r_dec["ratio_trivial"] < 1e-3 and r_dec["ratio_uniform"] < 1e-8
    assert r_frac["ratio_trivial"] < 1e-3 and r_frac["ratio_uniform"] < 1e-8
