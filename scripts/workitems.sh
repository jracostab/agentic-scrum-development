#!/usr/bin/env bash
# Thin wrapper around workitems.py
set -euo pipefail
PACK="$(cd "$(dirname "$0")/.." && pwd)"
exec python3 "$PACK/scripts/workitems.py" "$@"
