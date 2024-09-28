#!/usr/bin/env bash
set -euo pipefail

SELF=$(readlink -f "${BASH_SOURCE[0]}")
cd -- "${SELF%/*/*}"

./scripts/run_in_venv.sh python3 -m unittest discover -v ./test
