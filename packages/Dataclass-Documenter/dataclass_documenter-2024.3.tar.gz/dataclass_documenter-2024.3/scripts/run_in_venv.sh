#!/usr/bin/env bash
set -euo pipefail

SELF=$(readlink -f "${BASH_SOURCE[0]}")
DIR=${SELF%/*/*}

"$DIR/scripts/install_in_venv.sh"
source "$DIR/venv/bin/activate"
"$@"
