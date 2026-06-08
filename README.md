# img2nl


## AI Cost Tracking

![PyPI](https://img.shields.io/badge/pypi-costs-blue) ![Version](https://img.shields.io/badge/version-0.1.1-blue) ![Python](https://img.shields.io/badge/python-3.9+-blue) ![License](https://img.shields.io/badge/license-Apache--2.0-green)
![AI Cost](https://img.shields.io/badge/AI%20Cost-$0.15-orange) ![Human Time](https://img.shields.io/badge/Human%20Time-1.0h-blue) ![Model](https://img.shields.io/badge/Model-openrouter%2Fqwen%2Fqwen3--coder--next-lightgrey)

- 🤖 **LLM usage:** $0.1500 (1 commits)
- 👤 **Human dev:** ~$100 (1.0h @ $100/h, 30min dedup)

Generated on 2026-06-08 using [openrouter/qwen/qwen3-coder-next](https://openrouter.ai/qwen/qwen3-coder-next)

---

Heuristic **image → natural language** summary for transport to LLM and other services.

No vision LLM required — uses Pillow heuristics:

- monochrome vs multi-color palette
- dominant colors, brightness range, contrast
- large regions / objects
- noise vs flat surfaces
- regular patterns (bands/grid)
- thumbnail generation (JPEG)
- LLM transport hint (`send` vs `skip`)

## Install

```bash
pip install -e ".[analyze]"
bash install-dev.sh   # full *2img2nl stack
```

## CLI

```bash
img2nl analyze photo.png --json
dsl2img2nl -c "ANALYZE photo.png" --json
uri2img2nl query "img2nl://analyze?path=photo.png&locale=de"
img2nl analyze photo.png --locale fr
python -c "from img2nl.i18n import supported_locales; print(supported_locales())"
```

## Packages

| Package | Role |
|---------|------|
| `img2nl` | Core heuristics + describe + thumbnail |
| `uri2img2nl` | `img2nl://` URI layer |
| `dsl2img2nl` | DSL bus (`ANALYZE`, `QUERY`, `LLM_HINT`) |
| `cli2img2nl` | Shell adapter |

## VQL integration

Use `img2vql` in `oqlos/vql`:

```bash
img2vql diagnose capture.png --vql-program app.vql.json
uri2vql query "vql://window/diagnose?file=app.vql.json&image=capture.png"
```


## License

Licensed under Apache-2.0.
