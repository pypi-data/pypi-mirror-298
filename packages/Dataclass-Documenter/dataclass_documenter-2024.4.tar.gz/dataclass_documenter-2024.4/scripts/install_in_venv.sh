#!/usr/bin/env bash
set -euo pipefail

SELF=$(readlink -f "${BASH_SOURCE[0]}")
cd -- "${SELF%/*/*}"
python3 -m venv venv
source venv/bin/activate
pip install -q -U pip
pip install -q -U -e .
