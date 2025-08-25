\
#!/usr/bin/env bash
set -euo pipefail
echo "[1/3] Replicating tail inequality at N*=4e18..."
python scripts/replicate_tail.py
echo "[2/3] Verbose envelope (uniform AP, Qcap=1000)..."
python scripts/major_arc_envelope.py --model uniform --N 4e18 --K 10 --S 1.2 --Wsup 1.0 --Rexp 0.6 --Qcap 1000
echo "[3/3] Per-q CSV driver (fallback uniform, Qcap=1000)..."
python scripts/per_q_envelope.py --Qcap 1000 --fallback uniform
