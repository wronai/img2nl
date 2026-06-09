# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.10] - 2026-06-09

### Fixed
- Fix unused-imports issues (ticket-139c9530)
- Fix ai-boilerplate issues (ticket-bce7aa6e)
- Fix unused-imports issues (ticket-220eaf8d)
- Fix unused-imports issues (ticket-9ea89acf)
- Fix ai-boilerplate issues (ticket-0ba6c20f)
- Fix unused-imports issues (ticket-92e3c5dc)
- Fix string-concat issues (ticket-06f7ab4e)
- Fix unused-imports issues (ticket-a60ed97f)
- Fix unused-imports issues (ticket-54fb05d1)
- Fix unused-imports issues (ticket-5a13489e)
- Fix ai-boilerplate issues (ticket-f5b693f7)
- Fix string-concat issues (ticket-87b0230c)
- Fix unused-imports issues (ticket-7332c502)
- Fix string-concat issues (ticket-ac691aaa)
- Fix unused-imports issues (ticket-4a761d4c)
- Fix unused-imports issues (ticket-5487f74b)
- Fix unused-imports issues (ticket-3ec47c56)
- Fix ai-boilerplate issues (ticket-9e886d94)
- Fix unused-imports issues (ticket-548139fa)
- Fix magic-numbers issues (ticket-44f72d79)
- Fix unused-imports issues (ticket-e9b9fe09)
- Fix unused-imports issues (ticket-8696f9df)
- Fix string-concat issues (ticket-09ca11ae)
- Fix unused-imports issues (ticket-fa69ee00)
- Fix magic-numbers issues (ticket-492e639f)
- Fix unused-imports issues (ticket-f509fdb1)
- Fix magic-numbers issues (ticket-5bec9d4d)
- Fix unused-imports issues (ticket-0aa3d690)
- Fix magic-numbers issues (ticket-2a70043e)
- Fix unused-imports issues (ticket-75f681fd)
- Fix unused-imports issues (ticket-0c44e700)
- Fix magic-numbers issues (ticket-4f6afeee)
- Fix string-concat issues (ticket-2f18d019)
- Fix unused-imports issues (ticket-a5439835)
- Fix magic-numbers issues (ticket-b8b0717b)
- Fix string-concat issues (ticket-e1e82818)
- Fix unused-imports issues (ticket-06c7cc2d)
- Fix string-concat issues (ticket-fa4b6b97)
- Fix unused-imports issues (ticket-d7c71ecf)
- Fix magic-numbers issues (ticket-5daeeb94)
- Fix unused-imports issues (ticket-8a79c6fa)
- Fix unused-imports issues (ticket-05f8369a)
- Fix unused-imports issues (ticket-3ce7afb3)
- Fix unused-imports issues (ticket-38b6e465)
- Fix unused-imports issues (ticket-bff04c56)
- Fix unused-imports issues (ticket-101e9dc9)
- Fix unused-imports issues (ticket-9cc3766a)
- Fix unused-imports issues (ticket-093d7630)
- Fix unused-imports issues (ticket-f8e773c3)
- Fix unused-imports issues (ticket-ff54b96c)
- Fix unused-imports issues (ticket-53a6913a)
- Fix magic-numbers issues (ticket-b3debb5d)
- Fix unused-imports issues (ticket-680c740a)
- Fix unused-imports issues (ticket-45000d56)
- Fix unused-imports issues (ticket-18b0fefb)
- Fix unused-imports issues (ticket-0eebdabe)
- Fix unused-imports issues (ticket-2f96e332)
- Fix unused-imports issues (ticket-b6eaec88)

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

## [0.1.4] - 2026-06-09

### Docs
- Update CHANGELOG.md
- Update README.md
- Update SUMD.md
- Update SUMR.md
- Update TODO.md

### Test
- Update testql-scenarios/generated-cli-tests.testql.toon.yaml

### Other
- Update app.doql.less
- Update planfile.yaml
- Update project/logic.pl
- Update project/map.toon.yaml

## [0.1.3] - 2026-06-09

### Docs
- Update README.md
- Update project/README.md
- Update project/context.md

### Other
- Update prefact.yaml
- Update project/analysis.toon.yaml
- Update project/calls.mmd
- Update project/calls.png
- Update project/calls.toon.yaml
- Update project/calls.yaml
- Update project/compact_flow.mmd
- Update project/compact_flow.png
- Update project/duplication.toon.yaml
- Update project/evolution.toon.yaml
- ... and 8 more files

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
