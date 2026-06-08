#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")" && pwd)"
cd "$ROOT"

pip install -e ".[dev,analyze]"
pip install -e packages/uri2img2nl
pip install -e packages/dsl2img2nl
pip install -e packages/cli2img2nl

echo "img2nl dev stack installed"
