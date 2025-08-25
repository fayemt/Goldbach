# Goldbach Project

This repository contains a consolidated distribution of the materials
supporting a proof of the even Goldbach conjecture. It aims to make the
numerical tail closure and its replication **transparent, reproducible, and
verifiable**.

> **Status**: public research artifact; includes full LaTeX source, replication
> scripts, and tests. See `CITATIONS.md` for provenance, and `RELEASE.md` for
> the release/verification checklist.

---

## Version

- **v1.0.0** — 2025-08-24 (first consolidated release)
  - Unified `main.tex` with integrated appendices C/S/T/U.
  - Set \(Q=5253\); harmonic sum \( \sum_{q\le 5253}\!1/(q\varphi(q))=1.20348665358 \).
  - Cleaned envelopes and constants; consistent notation and dashes.
  - Added replication appendix and minimal test suite.
  - Introduced `Makefile`, `CITATION.cff`, and release checklist.

See `CHANGELOG.md` for detailed history.

---

## Repository structure

- `paper/` — LaTeX sources (single-file `main.tex` with appendices)
- `scripts/` — replication scripts (e.g., `replicate_tail.py`, `constants.json`)
- `tests/` — sanity checks (`pytest`)
- `LICENSES/` — license texts (MIT for code, CC-BY-4.0 for paper)
- `CITATIONS.md` — references and provenance notes
- `README.md`, `CHANGELOG.md`, `RELEASE.md`, `CITATION.cff`

---

## Build the paper

Requires a reasonably recent TeX installation.

```bash
cd paper
make           # builds main.pdf via latexmk
# or: latexmk -pdf -interaction=nonstopmode main.tex
