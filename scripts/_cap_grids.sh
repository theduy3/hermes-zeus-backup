#!/usr/bin/env bash
set -e
cd /home/hermes/.hermes/projects/remarkable-mcp
export PATH="$HOME/.local/bin:$PATH"
D=2026-08-20
mkdir -p /vault/Tasks/planning/remarkable/assets/$D
echo "=== capture p963 (exercise grid) ==="
timeout 200 python3 rm_capture.py "2026 Planner" 963 /vault/Tasks/planning/remarkable/assets/$D/963.png 2>&1 | tail -3
echo "=== capture p964 (meditation grid) ==="
timeout 200 python3 rm_capture.py "2026 Planner" 964 /vault/Tasks/planning/remarkable/assets/$D/964.png 2>&1 | tail -3
echo "=== sizes ==="
ls -la /vault/Tasks/planning/remarkable/assets/$D/963.png /vault/Tasks/planning/remarkable/assets/$D/964.png
