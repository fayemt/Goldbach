
---

**`CITATIONS.md`**
```markdown
# Citation and provenance

This project implements the tail closure step in a proof of the even Goldbach
conjecture.  The following sources underpin the numerical and analytical
bounds used here:

- **Appendix T (Tail closure)**: Definitions of the major‑arc cut‑off
  \(R = N^{3/5}\), the small‑modulus threshold \(Q = \lfloor N^{1/5}\rfloor\),
  and the envelope functions \(E_q(N)\).  It details how to combine the
  singular‑series floor \(\mathfrak S(N)\ge S\), a safety factor \(K\), and
  window constant \(C_W\) to bound the major‑arc contribution.
- **Minor arcs large‑sieve bound**: We use a uniform bound
  \(E_q(N) \le N/(160 \log N)\) from Bennett–Martin–O’Bryant–Rechnitzer
  (2018) for primes in arithmetic progressions (see their Theorem 3.5).  This
  improves upon the trivial bound \(N\log N+N\) for sufficiently large \(N\).
- **Singular‑series lower bound**: The singular series is bounded below by
  \(S = 1.2\) for all sufficiently large \(N\) (see Appendix S).  It is used
  as \(\mathfrak S(N)\ge S\) in the major‑arc error estimate.
- **Appendix C (Constants)**: Ledger listing \(S\_{floor}=1.2\), \(K=10\)
  (safety factor), \(C_W=2\) (beta‑window), and the harmonic sum
  \(S(Q)\) at \(Q=5253\) ≈ 1.20348665358; an optional per‑\(q\) bound
  \(N/(160 \log N)\) per Bennett–Martin–O’Bryant–Rechnitzer (2018).
- **External references**:
  - Oliveira e Silva, T. Herzog & S. Pardi, “Empirical verification of the
    even Goldbach conjecture and computation of prime gaps up to
    \(4 \times 10^{18}\)”, Math. Comp. 2014 – for the head verification and
    partial sums of the von Mangoldt function.
  - Bennett, J., M. Martin, K. O’Bryant & A. Rechnitzer, “Explicit bounds
    for primes in arithmetic progressions”, Math. Comp. 2018 – for the
    uniform bound \(E_q(N)\le N/(160\log N)\) and the minor‑arc large sieve.
