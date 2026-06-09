#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")" && pwd)"
cd "$ROOT"

pip install -e ".[dev,analyze]"
pip install -e packages/uri2img2nl
pip install -e packages/dsl2img2nl
pip install -e packages/cli2img2nl

# Optional desktop pipeline siblings (local paths)
if [ -d "$ROOT/../vdisplay" ]; then
  pip install -e "$ROOT/../vdisplay[pillow]"
fi
if [ -d "$ROOT/../../semcod/imgl" ]; then
  pip install -e "$ROOT/../../semcod/imgl[capture,diagnose]"
elif [ -d "$ROOT/../imgl" ]; then
  pip install -e "$ROOT/../imgl[capture,diagnose]"
fi
if [ -d "$ROOT/../../oqlos/vql/packages/img2vql" ]; then
  pip install -e "$ROOT/../../oqlos/vql/packages/img2vql"
elif [ -d "$ROOT/../vql/packages/img2vql" ]; then
  pip install -e "$ROOT/../vql/packages/img2vql"
fi

echo "img2nl dev stack installed"
