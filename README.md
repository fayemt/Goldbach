Important: This repo is missing some key files, which will be bundled and properly uploaded in the coming days. The majority of which can be
found in the temorary bundle Proof_Audit_Pack_v1.zip. These are logs from my personal tests and need to be repackaged, but for now, they
can be stand-in's.

#Foreword
Hi, I'm Faye, the "author" of this repo and paper, and i just wanted to note a few things about this proof. Firstly, sadly I can 
barely call myself the author of this paper, as I wrote very little of it. The majority of the actual work contained here was facilitated
by AI, as I started this project randomly a couple weeks ago just to see what the bot would say. however, as it kept working through issues
it seemed to make some legimate progress on notorious issues. Normally, I trust an AI to give me correct info just about as much as I trust
politics to cheer me up, but I thought "if this has even the slightest chance of being real, I have an obligation to at least check right?.
So I went and tried to find the flaw, but for every issue, it seemed to just have a (seemingly 100% mathematically sound, if weird) solution
to get around it. Eventually I decided that I had verified all I could with my limited education and decided to release this to see what
people who know what they're talking about think. So I look forward to seeing what anyone has to say, and you can reach me directly at
fayemt03@gmail.com

Unprofessional foreword over, from here on, this paper takes itself completely seriously.

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
