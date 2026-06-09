# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Layered detection pipeline (warstwy 0–4): `edges`, `fingerprint`, `similarity`, `special_hits`, `semantic`
- Scene classification: `empty_dark_screen`, `ui_blocks`, `ui_with_text`, `dense_ui_or_code`, `unchanged_screen`, `barcode_present`
- Optional extras: `opencv`, `similarity`, `scan`, `ocr`, `detect`, `full`
- `analyze_image()` params: `reference_fingerprint`, `enable_detect`
- i18n keys: scene classes, special_hits descriptions (38 langs)
- Tests: `test_detection_layers.py`, `test_special_layers.py`
- Docs: `docs/detection-pipeline.md`, `TODO.md`

### Changed
- `describe.py` / `llm_gate.py` — use `scene_class`, `special_hits`, `similarity`
- `README.md` — detection layers, VQL integration, API examples

## [0.1.2] - 2026-06-09

### Docs
- Update CHANGELOG.md
- Update README.md
- Update TODO.md
- Update docs/detection-pipeline.md
- Update packages/README.md

### Test
- Update tests/test_detection_layers.py
- Update tests/test_offline_translate.py
- Update tests/test_special_layers.py

### Other
- Update scripts/build_i18n_catalog.py
- Update src/img2nl/i18n/messages.json
- Update uv.lock

## [0.1.1] - 2026-06-08

### Added
- European i18n catalog (38 langs) + offline argostranslate
- `translate_mode` in analyze/describe

### Docs
- Update README.md
- Update docs/detection-pipeline.md
- Update packages/README.md

### Test
- Update tests/test_analyze.py
- Update tests/test_detection_layers.py
- Update tests/test_i18n.py
- Update tests/test_uri2img2nl.py
