# img2nl


## AI Cost Tracking

![PyPI](https://img.shields.io/badge/pypi-costs-blue) ![Version](https://img.shields.io/badge/version-0.1.8-blue) ![Python](https://img.shields.io/badge/python-3.9+-blue) ![License](https://img.shields.io/badge/license-Apache--2.0-green)
![AI Cost](https://img.shields.io/badge/AI%20Cost-$1.94-orange) ![Human Time](https://img.shields.io/badge/Human%20Time-3.9h-blue) ![Model](https://img.shields.io/badge/Model-openrouter%2Fqwen%2Fqwen3--coder--next-lightgrey)

- 🤖 **LLM usage:** $1.9425 (7 commits)
- 👤 **Human dev:** ~$387 (3.9h @ $100/h, 30min dedup)

Generated on 2026-06-09 using [openrouter/qwen/qwen3-coder-next](https://openrouter.ai/qwen/qwen3-coder-next)

---

Heuristic **image → natural language** summary for transport to LLM and other services.

No vision LLM required for the core path — uses layered heuristics (Pillow, optional OpenCV, perceptual hash, conditional OCR/QR/YOLO).

## Features

| Layer | Module | Extra | What it detects |
|-------|--------|-------|-----------------|
| 0 | `colors`, `dynamics`, `noise`, `objects`, `patterns` | `[analyze]` | palette, contrast, flat regions, UI blocks |
| 1 | `edges` | `[opencv]` | blur, edge density, text likelihood |
| 2 | `fingerprint`, `similarity` | `[similarity]` | pHash/dHash/wHash, screen match |
| 3 | `special_hits` | `[scan]` / `[ocr]` | QR/barcode, OCR (conditional) |
| 4 | `semantic_hits` | `[detect]` | YOLO labels (opt-in) |

Output includes `features.scene.scene_class`, `llm_hint`, and optional `similarity` when `reference_fingerprint` is passed.

Full architecture: **[docs/detection-pipeline.md](docs/detection-pipeline.md)**

## Install

```bash
pip install -e ".[analyze]"              # core (Pillow + NumPy)
pip install -e ".[full]"                 # analyze + opencv + similarity + scan
pip install -e ".[analyze,translate]"    # + argostranslate offline
bash install-dev.sh                        # full *2img2nl stack
```

Optional extras: `opencv`, `similarity`, `scan`, `ocr`, `detect` — see `pyproject.toml`.

## CLI

```bash
img2nl analyze photo.png --json
img2nl analyze photo.png --locale de --translate-mode offline
dsl2img2nl -c "ANALYZE photo.png" --json
uri2img2nl query "img2nl://analyze?path=photo.png&locale=pl"
python -c "from img2nl.i18n import supported_locales; print(supported_locales())"
```

### Offline translation (argostranslate)

Static catalog covers 38 European langs; for scalable updates use neural offline translation:

```bash
pip install img2nl[analyze,translate]
img2nl translate-install en pl
img2nl analyze photo.png --locale de --translate-mode offline
```

Modes: `auto` (catalog pl/en, else argos), `offline` (require argos), `catalog` (JSON only).

## Python API

```python
from img2nl import analyze_image

result = analyze_image("screen.png", skip_thumbnail=True)
print(result.text, result.features["scene"]["scene_class"], result.llm_hint)

# compare with previous capture
prev = analyze_image("screen_a.png", skip_thumbnail=True)
cur = analyze_image(
    "screen_b.png",
    skip_thumbnail=True,
    reference_fingerprint=prev.features["fingerprint"],
    enable_detect=False,  # True → YOLO (heavy)
)
print(cur.features.get("similarity", {}))
```

## Packages

| Package | Role |
|---------|------|
| `img2nl` | Core heuristics + describe + thumbnail + layered detection |
| `uri2img2nl` | `img2nl://` URI layer |
| `dsl2img2nl` | DSL bus (`ANALYZE`, `QUERY`, `LLM_HINT`) |
| `cli2img2nl` | Shell adapter |

See [packages/README.md](packages/README.md).

## VQL integration

Layered pipeline with `img2vql` in `oqlos/vql`:

```bash
pip install -e ".[analyze,similarity,opencv,scan]"
pip install -e ~/github/oqlos/vql/packages/img2vql

# adopt → metadata (fingerprint, special_hits, scene_class)
uri2vql analyze-window --image capture.png --out app.vql.json

# smart skip when screen unchanged
uri2vql analyze-window --image capture.png --out app.vql.json

uri2vql refresh-window --vql-program app.vql.json --image capture.png
uri2vql compare-window --vql-program app.vql.json --image capture.png
img2vql diagnose capture.png --vql-program app.vql.json --save
uri2vql resolve "odśwież metadata vql" --file app.vql.json --image capture.png

# end-to-end demo
bash ~/github/oqlos/vql/examples/img2nl-vql-flow.sh capture.png app.vql.json
```

## Docs

| Doc | Content |
|-----|---------|
| [docs/detection-pipeline.md](docs/detection-pipeline.md) | Warstwy 0–4, schema JSON, VQL cache |
| [CHANGELOG.md](CHANGELOG.md) | Historia zmian |
| [TODO.md](TODO.md) | Backlog |

## License

Licensed under Apache-2.0.
