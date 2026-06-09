# img2nl

Image → natural language summary with heuristics, thumbnails, and LLM transport hints

## Contents

- [Metadata](#metadata)
- [Architecture](#architecture)
- [Interfaces](#interfaces)
- [Workflows](#workflows)
- [Configuration](#configuration)
- [Dependencies](#dependencies)
- [Deployment](#deployment)
- [Environment Variables (`.env.example`)](#environment-variables-envexample)
- [Release Management (`goal.yaml`)](#release-management-goalyaml)
- [Makefile Targets](#makefile-targets)
- [Code Analysis](#code-analysis)
- [Call Graph](#call-graph)
- [Test Contracts](#test-contracts)
- [Intent](#intent)

## Metadata

- **name**: `img2nl`
- **version**: `0.1.3`
- **python_requires**: `>=3.10`
- **license**: Apache-2.0
- **ai_model**: `openrouter/qwen/qwen3-coder-next`
- **ecosystem**: SUMD + DOQL + testql + taskfile
- **generated_from**: pyproject.toml, Makefile, testql(1), app.doql.less, goal.yaml, .env.example, project/(3 analysis files)

## Architecture

```
SUMD (description) → DOQL/source (code) → taskfile (automation) → testql (verification)
```

### DOQL Application Declaration (`app.doql.less`)

```less markpact:doql path=app.doql.less
// LESS format — define @variables here as needed

app {
  name: img2nl;
  version: 0.1.3;
}

dependencies {
  analyze: "pillow>=10.0, numpy>=1.24";
  translate: argostranslate>=1.9.0;
  opencv: opencv-python>=4.8;
  similarity: "imagehash>=4.3, scikit-image>=0.22";
  scan: pyzbar>=0.1.9;
  ocr: rapidocr-onnxruntime>=1.3;
  detect: ultralytics>=8.2;
  full: "pillow>=10.0, numpy>=1.24, opencv-python>=4.8, imagehash>=4.3, scikit-image>=0.22, pyzbar>=0.1.9";
  dev: "pytest>=8.0, pillow>=10.0, numpy>=1.24, opencv-python>=4.8, imagehash>=4.3, pyzbar>=0.1.9, qrcode>=7.4, goal>=2.1.0, costs>=0.1.20, pfix>=0.1.60";
}

interface[type="cli"] {
  framework: argparse;
}
interface[type="cli"] page[name="img2nl"] {
  entry: img2nl.cli:main;
}

workflow[name="venv"] {
  trigger: manual;
  step-1: run cmd=test -d .venv || python3 -m venv .venv;
}

workflow[name="install"] {
  trigger: manual;
  step-1: run cmd=$(PIP) install -e ".[analyze]";
}

workflow[name="install-dev"] {
  trigger: manual;
  step-1: run cmd=$(PIP) install -e ".[dev,analyze]";
  step-2: run cmd=for pkg in $(PACKAGES); do $(PIP) install -e packages/$$pkg; done;
}

workflow[name="test"] {
  trigger: manual;
  step-1: run cmd=$(PYTHON) -m pytest tests/ -q --tb=short;
}

workflow[name="clean"] {
  trigger: manual;
  step-1: run cmd=rm -rf .pytest_cache **/__pycache__ dist build *.egg-info;
}

env_vars {
  keys: OPENROUTER_API_KEY, LLM_MODEL;
}

deploy {
  target: makefile;
}

environment[name="local"] {
  runtime: python;
  env_file: .env;
  template_file: .env.example;
  python_version: >=3.10;
  vars: LLM_MODEL, OPENROUTER_API_KEY;
  runtime_llm: OPENROUTER_API_KEY;
}
```

## Interfaces

### CLI Entry Points

- `img2nl`

### testql Scenarios

#### `testql-scenarios/generated-cli-tests.testql.toon.yaml`

```toon markpact:testql path=testql-scenarios/generated-cli-tests.testql.toon.yaml
# SCENARIO: CLI Command Tests
# TYPE: cli
# GENERATED: true

CONFIG[2]{key, value}:
  cli_command, python -m img2nl
  timeout_ms, 10000

# Test 1: CLI help command
SHELL "python -m img2nl --help" 5000
ASSERT_EXIT_CODE 0
ASSERT_STDOUT_CONTAINS "usage"

# Test 2: CLI version command
SHELL "python -m img2nl --version" 5000
ASSERT_EXIT_CODE 0

# Test 3: CLI main workflow (dry-run)
SHELL "python -m img2nl --help" 10000
ASSERT_EXIT_CODE 0
```

## Workflows

## Configuration

```yaml
project:
  name: img2nl
  version: 0.1.3
  env: local
```

## Dependencies

### Runtime

*(see pyproject.toml)*

### Development

```text markpact:deps python scope=dev
pytest>=8.0
pillow>=10.0
numpy>=1.24
opencv-python>=4.8
imagehash>=4.3
pyzbar>=0.1.9
qrcode>=7.4
goal>=2.1.0
costs>=0.1.20
pfix>=0.1.60
```

## Deployment

```bash markpact:run
pip install img2nl

# development install
pip install -e .[dev]
```

## Environment Variables (`.env.example`)

| Variable | Default | Description |
|----------|---------|-------------|
| `OPENROUTER_API_KEY` | `sk-or-v1-...` | OpenRouter API Key (required for real cost calculation) |
| `LLM_MODEL` | `openrouter/qwen/qwen3-coder-next` | Default AI model for cost analysis |

## Release Management (`goal.yaml`)

- **versioning**: `semver`
- **commits**: `conventional` scope=`img2nl`
- **changelog**: `keep-a-changelog`
- **build strategies**: `python`, `nodejs`, `rust`
- **version files**: `VERSION`, `pyproject.toml:version`, `venv/lib/python3.12/site-packages/mistune/__init__.py:__version__`

## Makefile Targets

- `PACKAGES`
- `venv`
- `install`
- `install-dev`
- `test`
- `clean`

## Code Analysis

### `project/map.toon.yaml`

```toon markpact:analysis path=project/map.toon.yaml
# img2nl | 48f 2710L | python:44,shell:3,less:1 | 2026-06-09
# stats: 90 func | 5 cls | 48 mod | CC̄=4.8 | critical:10 | cycles:0
# alerts[5]: CC llm_transport_hint=27; CC classify_scene=18; CC _describe_catalog=17; CC parse_line=14; CC main=14
# hotspots[5]: analyze_image fan=21; analyze_edges fan=16; main fan=14; analyze_objects fan=14; analyze_colors fan=13
# evolution: baseline
# Keys: M=modules, D=details, i=imports, e=exports, c=classes, f=functions, m=methods
M[48]:
  app.doql.less,69
  install-dev.sh,12
  packages/cli2img2nl/src/cli2img2nl/cli.py,33
  packages/dsl2img2nl/src/dsl2img2nl/__init__.py,7
  packages/dsl2img2nl/src/dsl2img2nl/bus.py,30
  packages/dsl2img2nl/src/dsl2img2nl/cli.py,34
  packages/dsl2img2nl/src/dsl2img2nl/grammar.py,46
  packages/dsl2img2nl/src/dsl2img2nl/handlers.py,78
  packages/dsl2img2nl/src/dsl2img2nl/result.py,27
  packages/uri2img2nl/src/uri2img2nl/__init__.py,7
  packages/uri2img2nl/src/uri2img2nl/cli.py,29
  packages/uri2img2nl/src/uri2img2nl/query.py,107
  packages/uri2img2nl/src/uri2img2nl/uri.py,47
  project.sh,59
  scripts/build_i18n_catalog.py,63
  src/img2nl/__init__.py,26
  src/img2nl/analyze.py,96
  src/img2nl/cli.py,86
  src/img2nl/describe.py,133
  src/img2nl/features/__init__.py,32
  src/img2nl/features/barcodes.py,79
  src/img2nl/features/colors.py,52
  src/img2nl/features/dynamics.py,29
  src/img2nl/features/edges.py,55
  src/img2nl/features/fingerprint.py,31
  src/img2nl/features/noise.py,30
  src/img2nl/features/objects.py,104
  src/img2nl/features/ocr_text.py,74
  src/img2nl/features/patterns.py,54
  src/img2nl/features/scene.py,66
  src/img2nl/features/semantic.py,85
  src/img2nl/features/similarity.py,74
  src/img2nl/features/special_hits.py,20
  src/img2nl/i18n/__init__.py,27
  src/img2nl/i18n/catalog.py,17
  src/img2nl/i18n/locales.py,60
  src/img2nl/i18n/offline.py,190
  src/img2nl/i18n/translate.py,17
  src/img2nl/llm_gate.py,89
  src/img2nl/result.py,35
  src/img2nl/thumbnail.py,30
  tests/test_analyze.py,66
  tests/test_detection_layers.py,88
  tests/test_i18n.py,61
  tests/test_offline_translate.py,64
  tests/test_special_layers.py,154
  tests/test_uri2img2nl.py,36
  tree.sh,2
D:
  packages/cli2img2nl/src/cli2img2nl/cli.py:
    e: main
    main(argv)
  packages/dsl2img2nl/src/dsl2img2nl/__init__.py:
  packages/dsl2img2nl/src/dsl2img2nl/bus.py:
    e: dispatch,execute_dsl_line
    dispatch(envelope)
    execute_dsl_line(line)
  packages/dsl2img2nl/src/dsl2img2nl/cli.py:
    e: main
    main(argv)
  packages/dsl2img2nl/src/dsl2img2nl/grammar.py:
    e: split_command,parse_line
    split_command(line)
    parse_line(line)
  packages/dsl2img2nl/src/dsl2img2nl/handlers.py:
    e: handle_analyze,handle_query,handle_llm_hint,handle_from_tokens
    handle_analyze(cmd)
    handle_query(cmd)
    handle_llm_hint(cmd)
    handle_from_tokens(line;tokens;cmd)
  packages/dsl2img2nl/src/dsl2img2nl/result.py:
    e: DslResult
    DslResult: to_dict(0)
  packages/uri2img2nl/src/uri2img2nl/__init__.py:
  packages/uri2img2nl/src/uri2img2nl/cli.py:
    e: main
    main(argv)
  packages/uri2img2nl/src/uri2img2nl/query.py:
    e: query_uri,QueryResult
    QueryResult: to_dict(0)
    query_uri(uri)
  packages/uri2img2nl/src/uri2img2nl/uri.py:
    e: is_img2nl_uri,uri_for_analyze,uri_for_llm_hint,parse_img2nl_uri,Img2NlUri
    Img2NlUri: target(0)
    is_img2nl_uri(uri)
    uri_for_analyze(path)
    uri_for_llm_hint(path)
    parse_img2nl_uri(uri)
  scripts/build_i18n_catalog.py:
  src/img2nl/__init__.py:
  src/img2nl/analyze.py:
    e: analyze_image
    analyze_image(image_path)
  src/img2nl/cli.py:
    e: main
    main(argv)
  src/img2nl/describe.py:
    e: _describe_catalog,describe_image
    _describe_catalog(features;lang)
    describe_image(features)
  src/img2nl/features/__init__.py:
  src/img2nl/features/barcodes.py:
    e: _suppress_zbar_stderr,_should_scan,analyze_barcodes
    _suppress_zbar_stderr()
    _should_scan(features)
    analyze_barcodes(im)
  src/img2nl/features/colors.py:
    e: _hex,analyze_colors
    _hex(rgb)
    analyze_colors(im)
  src/img2nl/features/dynamics.py:
    e: analyze_dynamics
    analyze_dynamics(im)
  src/img2nl/features/edges.py:
    e: _unavailable,analyze_edges
    _unavailable(reason)
    analyze_edges(im)
  src/img2nl/features/fingerprint.py:
    e: _unavailable,analyze_fingerprint
    _unavailable(reason)
    analyze_fingerprint(im)
  src/img2nl/features/noise.py:
    e: analyze_noise
    analyze_noise(im)
  src/img2nl/features/objects.py:
    e: _largest_regions,analyze_objects
    _largest_regions(mask)
    analyze_objects(im)
  src/img2nl/features/ocr_text.py:
    e: _should_ocr,_preview,analyze_ocr
    _should_ocr(features)
    _preview(lines)
    analyze_ocr(im)
  src/img2nl/features/patterns.py:
    e: analyze_patterns
    analyze_patterns(im)
  src/img2nl/features/scene.py:
    e: classify_scene
    classify_scene(features)
  src/img2nl/features/semantic.py:
    e: _should_detect,_get_model,analyze_semantic
    _should_detect(features)
    _get_model()
    analyze_semantic(im)
  src/img2nl/features/similarity.py:
    e: fingerprint_hamming,compare_fingerprints,compare_images_ssim
    fingerprint_hamming(a;b)
    compare_fingerprints(current;reference)
    compare_images_ssim(im_a;im_b)
  src/img2nl/features/special_hits.py:
    e: analyze_special_hits
    analyze_special_hits(im;features)
  src/img2nl/i18n/__init__.py:
  src/img2nl/i18n/catalog.py:
    e: _load_messages
    _load_messages()
  src/img2nl/i18n/locales.py:
    e: normalize_locale,supported_locales,is_european_locale
    normalize_locale(locale)
    supported_locales()
    is_european_locale(locale)
  src/img2nl/i18n/offline.py:
    e: argostranslate_available,_require_argos,_update_index,list_installed_pairs,list_available_pairs,ensure_language_pair,translate_summary_offline,TranslateResult
    TranslateResult: to_dict(0)
    argostranslate_available()
    _require_argos()
    _update_index(package_mod)
    list_installed_pairs()
    list_available_pairs()
    ensure_language_pair(from_code;to_code)
    translate_summary_offline(text;target_lang)
  src/img2nl/i18n/translate.py:
    e: t
    t()
  src/img2nl/llm_gate.py:
    e: llm_transport_hint
    llm_transport_hint(features)
  src/img2nl/result.py:
    e: Img2NlResult
    Img2NlResult: to_dict(0)
  src/img2nl/thumbnail.py:
    e: make_thumbnail
    make_thumbnail(image_path)
  tests/test_analyze.py:
    e: _solid,_desktop,test_monochrome_detected,test_multicolor_desktop,test_thumbnail_created,test_llm_hint_rich_image
    _solid(path;color;size)
    _desktop(path)
    test_monochrome_detected(tmp_path)
    test_multicolor_desktop(tmp_path)
    test_thumbnail_created(tmp_path)
    test_llm_hint_rich_image(tmp_path)
  tests/test_detection_layers.py:
    e: _solid,test_scene_empty_dark_screen,test_optional_modules_graceful_without_extras,test_edges_when_opencv_installed,test_fingerprint_when_imagehash_installed
    _solid(path;color;size)
    test_scene_empty_dark_screen()
    test_optional_modules_graceful_without_extras(tmp_path)
    test_edges_when_opencv_installed(tmp_path)
    test_fingerprint_when_imagehash_installed(tmp_path)
  tests/test_i18n.py:
    e: test_normalize_locale,test_all_european_locales_have_full_catalog,test_translate_not_english_copy,test_describe_german
    test_normalize_locale(raw;expected)
    test_all_european_locales_have_full_catalog()
    test_translate_not_english_copy(lang)
    test_describe_german()
  tests/test_offline_translate.py:
    e: test_translate_summary_no_argos_returns_fallback,test_translate_summary_same_lang_noop,test_translate_summary_with_mock_argos,test_describe_offline_mode_uses_translate
    test_translate_summary_no_argos_returns_fallback()
    test_translate_summary_same_lang_noop()
    test_translate_summary_with_mock_argos()
    test_describe_offline_mode_uses_translate(monkeypatch)
  tests/test_special_layers.py:
    e: _solid,_desktop,test_analyze_includes_special_and_semantic,test_barcode_skipped_on_dark_screen,test_scene_unchanged_from_similarity,test_compare_fingerprints_match,test_fingerprint_hamming_distance,test_qr_detected_on_desktop,test_reference_fingerprint_param,test_semantic_only_when_enabled
    _solid(path;color;size)
    _desktop(path)
    test_analyze_includes_special_and_semantic(tmp_path)
    test_barcode_skipped_on_dark_screen(tmp_path)
    test_scene_unchanged_from_similarity()
    test_compare_fingerprints_match()
    test_fingerprint_hamming_distance()
    test_qr_detected_on_desktop(tmp_path)
    test_reference_fingerprint_param(tmp_path)
    test_semantic_only_when_enabled(tmp_path)
  tests/test_uri2img2nl.py:
    e: test_uri_query,test_dsl_analyze
    test_uri_query(tmp_path)
    test_dsl_analyze(tmp_path)
```

### `project/logic.pl`

```prolog markpact:analysis path=project/logic.pl
% ── Project Metadata ─────────────────────────────────────
project_metadata('img2nl', '0.1.3', 'python').

% ── Project Files ────────────────────────────────────────
project_file('app.doql.less', 69, 'less').
project_file('install-dev.sh', 12, 'shell').
project_file('packages/cli2img2nl/src/cli2img2nl/cli.py', 33, 'python').
project_file('packages/dsl2img2nl/src/dsl2img2nl/__init__.py', 7, 'python').
project_file('packages/dsl2img2nl/src/dsl2img2nl/bus.py', 30, 'python').
project_file('packages/dsl2img2nl/src/dsl2img2nl/cli.py', 34, 'python').
project_file('packages/dsl2img2nl/src/dsl2img2nl/grammar.py', 46, 'python').
project_file('packages/dsl2img2nl/src/dsl2img2nl/handlers.py', 78, 'python').
project_file('packages/dsl2img2nl/src/dsl2img2nl/result.py', 27, 'python').
project_file('packages/uri2img2nl/src/uri2img2nl/__init__.py', 7, 'python').
project_file('packages/uri2img2nl/src/uri2img2nl/cli.py', 29, 'python').
project_file('packages/uri2img2nl/src/uri2img2nl/query.py', 107, 'python').
project_file('packages/uri2img2nl/src/uri2img2nl/uri.py', 47, 'python').
project_file('project.sh', 59, 'shell').
project_file('scripts/build_i18n_catalog.py', 63, 'python').
project_file('src/img2nl/__init__.py', 26, 'python').
project_file('src/img2nl/analyze.py', 96, 'python').
project_file('src/img2nl/cli.py', 86, 'python').
project_file('src/img2nl/describe.py', 133, 'python').
project_file('src/img2nl/features/__init__.py', 32, 'python').
project_file('src/img2nl/features/barcodes.py', 79, 'python').
project_file('src/img2nl/features/colors.py', 52, 'python').
project_file('src/img2nl/features/dynamics.py', 29, 'python').
project_file('src/img2nl/features/edges.py', 55, 'python').
project_file('src/img2nl/features/fingerprint.py', 31, 'python').
project_file('src/img2nl/features/noise.py', 30, 'python').
project_file('src/img2nl/features/objects.py', 104, 'python').
project_file('src/img2nl/features/ocr_text.py', 74, 'python').
project_file('src/img2nl/features/patterns.py', 54, 'python').
project_file('src/img2nl/features/scene.py', 66, 'python').
project_file('src/img2nl/features/semantic.py', 85, 'python').
project_file('src/img2nl/features/similarity.py', 74, 'python').
project_file('src/img2nl/features/special_hits.py', 20, 'python').
project_file('src/img2nl/i18n/__init__.py', 27, 'python').
project_file('src/img2nl/i18n/catalog.py', 17, 'python').
project_file('src/img2nl/i18n/locales.py', 60, 'python').
project_file('src/img2nl/i18n/offline.py', 190, 'python').
project_file('src/img2nl/i18n/translate.py', 17, 'python').
project_file('src/img2nl/llm_gate.py', 89, 'python').
project_file('src/img2nl/result.py', 35, 'python').
project_file('src/img2nl/thumbnail.py', 30, 'python').
project_file('tests/test_analyze.py', 66, 'python').
project_file('tests/test_detection_layers.py', 88, 'python').
project_file('tests/test_i18n.py', 61, 'python').
project_file('tests/test_offline_translate.py', 64, 'python').
project_file('tests/test_special_layers.py', 154, 'python').
project_file('tests/test_uri2img2nl.py', 36, 'python').
project_file('tree.sh', 2, 'shell').

% ── Python Functions ─────────────────────────────────────
python_function('packages/cli2img2nl/src/cli2img2nl/cli.py', 'main', 1, 6, 9).
python_function('packages/dsl2img2nl/src/dsl2img2nl/bus.py', 'dispatch', 1, 8, 9).
python_function('packages/dsl2img2nl/src/dsl2img2nl/bus.py', 'execute_dsl_line', 1, 1, 1).
python_function('packages/dsl2img2nl/src/dsl2img2nl/cli.py', 'main', 1, 8, 10).
python_function('packages/dsl2img2nl/src/dsl2img2nl/grammar.py', 'split_command', 1, 1, 2).
python_function('packages/dsl2img2nl/src/dsl2img2nl/grammar.py', 'parse_line', 1, 14, 4).
python_function('packages/dsl2img2nl/src/dsl2img2nl/handlers.py', 'handle_analyze', 1, 4, 5).
python_function('packages/dsl2img2nl/src/dsl2img2nl/handlers.py', 'handle_query', 1, 6, 5).
python_function('packages/dsl2img2nl/src/dsl2img2nl/handlers.py', 'handle_llm_hint', 1, 4, 4).
python_function('packages/dsl2img2nl/src/dsl2img2nl/handlers.py', 'handle_from_tokens', 3, 4, 8).
python_function('packages/uri2img2nl/src/uri2img2nl/cli.py', 'main', 1, 4, 9).
python_function('packages/uri2img2nl/src/uri2img2nl/query.py', 'query_uri', 1, 9, 6).
python_function('packages/uri2img2nl/src/uri2img2nl/uri.py', 'is_img2nl_uri', 1, 1, 2).
python_function('packages/uri2img2nl/src/uri2img2nl/uri.py', 'uri_for_analyze', 1, 2, 1).
python_function('packages/uri2img2nl/src/uri2img2nl/uri.py', 'uri_for_llm_hint', 1, 1, 1).
python_function('packages/uri2img2nl/src/uri2img2nl/uri.py', 'parse_img2nl_uri', 1, 5, 6).
python_function('src/img2nl/analyze.py', 'analyze_image', 1, 6, 21).
python_function('src/img2nl/cli.py', 'main', 1, 14, 14).
python_function('src/img2nl/describe.py', '_describe_catalog', 2, 17, 4).
python_function('src/img2nl/describe.py', 'describe_image', 1, 8, 3).
python_function('src/img2nl/features/barcodes.py', '_suppress_zbar_stderr', 0, 1, 5).
python_function('src/img2nl/features/barcodes.py', '_should_scan', 1, 3, 2).
python_function('src/img2nl/features/barcodes.py', 'analyze_barcodes', 1, 5, 7).
python_function('src/img2nl/features/colors.py', '_hex', 1, 1, 0).
python_function('src/img2nl/features/colors.py', 'analyze_colors', 1, 13, 13).
python_function('src/img2nl/features/dynamics.py', 'analyze_dynamics', 1, 1, 4).
python_function('src/img2nl/features/edges.py', '_unavailable', 1, 1, 0).
python_function('src/img2nl/features/edges.py', 'analyze_edges', 1, 6, 16).
python_function('src/img2nl/features/fingerprint.py', '_unavailable', 1, 1, 0).
python_function('src/img2nl/features/fingerprint.py', 'analyze_fingerprint', 1, 2, 6).
python_function('src/img2nl/features/noise.py', 'analyze_noise', 1, 6, 12).
python_function('src/img2nl/features/objects.py', '_largest_regions', 1, 14, 10).
python_function('src/img2nl/features/objects.py', 'analyze_objects', 1, 11, 14).
python_function('src/img2nl/features/ocr_text.py', '_should_ocr', 1, 3, 1).
python_function('src/img2nl/features/ocr_text.py', '_preview', 1, 2, 3).
python_function('src/img2nl/features/ocr_text.py', 'analyze_ocr', 1, 7, 11).
python_function('src/img2nl/features/patterns.py', 'analyze_patterns', 1, 8, 13).
python_function('src/img2nl/features/scene.py', 'classify_scene', 1, 18, 2).
python_function('src/img2nl/features/semantic.py', '_should_detect', 1, 2, 1).
python_function('src/img2nl/features/semantic.py', '_get_model', 0, 2, 1).
python_function('src/img2nl/features/semantic.py', 'analyze_semantic', 1, 9, 13).
python_function('src/img2nl/features/similarity.py', 'fingerprint_hamming', 2, 5, 1).
python_function('src/img2nl/features/similarity.py', 'compare_fingerprints', 2, 4, 2).
python_function('src/img2nl/features/similarity.py', 'compare_images_ssim', 2, 2, 9).
python_function('src/img2nl/features/special_hits.py', 'analyze_special_hits', 2, 1, 3).
python_function('src/img2nl/i18n/catalog.py', '_load_messages', 0, 2, 3).
python_function('src/img2nl/i18n/locales.py', 'normalize_locale', 1, 8, 4).
python_function('src/img2nl/i18n/locales.py', 'supported_locales', 0, 1, 1).
python_function('src/img2nl/i18n/locales.py', 'is_european_locale', 1, 1, 1).
python_function('src/img2nl/i18n/offline.py', 'argostranslate_available', 0, 2, 0).
python_function('src/img2nl/i18n/offline.py', '_require_argos', 0, 2, 1).
python_function('src/img2nl/i18n/offline.py', '_update_index', 1, 2, 1).
python_function('src/img2nl/i18n/offline.py', 'list_installed_pairs', 0, 3, 4).
python_function('src/img2nl/i18n/offline.py', 'list_available_pairs', 0, 5, 4).
python_function('src/img2nl/i18n/offline.py', 'ensure_language_pair', 2, 11, 10).
python_function('src/img2nl/i18n/offline.py', 'translate_summary_offline', 2, 7, 9).
python_function('src/img2nl/i18n/translate.py', 't', 0, 5, 4).
python_function('src/img2nl/llm_gate.py', 'llm_transport_hint', 1, 27, 5).
python_function('src/img2nl/thumbnail.py', 'make_thumbnail', 1, 4, 11).
python_function('tests/test_analyze.py', '_solid', 3, 1, 2).
python_function('tests/test_analyze.py', '_desktop', 1, 1, 4).
python_function('tests/test_analyze.py', 'test_monochrome_detected', 1, 5, 2).
python_function('tests/test_analyze.py', 'test_multicolor_desktop', 1, 6, 2).
python_function('tests/test_analyze.py', 'test_thumbnail_created', 1, 3, 4).
python_function('tests/test_analyze.py', 'test_llm_hint_rich_image', 1, 3, 3).
python_function('tests/test_detection_layers.py', '_solid', 3, 1, 2).
python_function('tests/test_detection_layers.py', 'test_scene_empty_dark_screen', 0, 2, 1).
python_function('tests/test_detection_layers.py', 'test_optional_modules_graceful_without_extras', 1, 11, 3).
python_function('tests/test_detection_layers.py', 'test_edges_when_opencv_installed', 1, 4, 3).
python_function('tests/test_detection_layers.py', 'test_fingerprint_when_imagehash_installed', 1, 5, 4).
python_function('tests/test_i18n.py', 'test_normalize_locale', 2, 2, 2).
python_function('tests/test_i18n.py', 'test_all_european_locales_have_full_catalog', 0, 5, 2).
python_function('tests/test_i18n.py', 'test_translate_not_english_copy', 1, 2, 2).
python_function('tests/test_i18n.py', 'test_describe_german', 0, 3, 1).
python_function('tests/test_offline_translate.py', 'test_translate_summary_no_argos_returns_fallback', 0, 4, 2).
python_function('tests/test_offline_translate.py', 'test_translate_summary_same_lang_noop', 0, 4, 1).
python_function('tests/test_offline_translate.py', 'test_translate_summary_with_mock_argos', 0, 3, 4).
python_function('tests/test_offline_translate.py', 'test_describe_offline_mode_uses_translate', 1, 2, 3).
python_function('tests/test_special_layers.py', '_solid', 3, 1, 2).
python_function('tests/test_special_layers.py', '_desktop', 1, 1, 4).
python_function('tests/test_special_layers.py', 'test_analyze_includes_special_and_semantic', 1, 5, 2).
python_function('tests/test_special_layers.py', 'test_barcode_skipped_on_dark_screen', 1, 3, 3).
python_function('tests/test_special_layers.py', 'test_scene_unchanged_from_similarity', 0, 2, 1).
python_function('tests/test_special_layers.py', 'test_compare_fingerprints_match', 0, 3, 2).
python_function('tests/test_special_layers.py', 'test_fingerprint_hamming_distance', 0, 2, 2).
python_function('tests/test_special_layers.py', 'test_qr_detected_on_desktop', 1, 4, 6).
python_function('tests/test_special_layers.py', 'test_reference_fingerprint_param', 1, 4, 3).
python_function('tests/test_special_layers.py', 'test_semantic_only_when_enabled', 1, 2, 4).
python_function('tests/test_uri2img2nl.py', 'test_uri_query', 1, 3, 5).
python_function('tests/test_uri2img2nl.py', 'test_dsl_analyze', 1, 3, 3).

% ── Python Classes ───────────────────────────────────────
python_class('packages/dsl2img2nl/src/dsl2img2nl/result.py', 'DslResult').
python_method('DslResult', 'to_dict', 0, 1, 0).
python_class('packages/uri2img2nl/src/uri2img2nl/query.py', 'QueryResult').
python_method('QueryResult', 'to_dict', 0, 1, 0).
python_class('packages/uri2img2nl/src/uri2img2nl/uri.py', 'Img2NlUri').
python_method('Img2NlUri', 'target', 0, 1, 0).
python_class('src/img2nl/i18n/offline.py', 'TranslateResult').
python_method('TranslateResult', 'to_dict', 0, 1, 0).
python_class('src/img2nl/result.py', 'Img2NlResult').
python_method('Img2NlResult', 'to_dict', 0, 1, 0).

% ── Dependencies ─────────────────────────────────────────

% ── Makefile Targets ─────────────────────────────────────
makefile_target('PACKAGES', '').
makefile_target('venv', '').
makefile_target('install', '').
makefile_target('install-dev', '').
makefile_target('test', '').
makefile_target('clean', '').

% ── Taskfile Tasks ───────────────────────────────────────

% ── Environment Variables ────────────────────────────────
env_variable('OPENROUTER_API_KEY', 'sk-or-v1-...', 'OpenRouter API Key (required for real cost calculation)').
env_variable('LLM_MODEL', 'openrouter/qwen/qwen3-coder-next', 'Default AI model for cost analysis').

% ── TestQL Scenarios ─────────────────────────────────────
testql_scenario('generated-cli-tests.testql.toon.yaml', 'cli').

% ── Semantic Facts from SUMD.md ──────────────────────────
```

## Call Graph

*43 nodes · 47 edges · 21 modules · CC̄=5.3*

### Hubs (by degree)

| Function | CC | in | out | total |
|----------|----|----|-----|-------|
| `_describe_catalog` *(in src.img2nl.describe)* | 17 ⚠ | 3 | 72 | **75** |
| `llm_transport_hint` *(in src.img2nl.llm_gate)* | 27 ⚠ | 1 | 54 | **55** |
| `analyze_image` *(in src.img2nl.analyze)* | 6 | 6 | 29 | **35** |
| `classify_scene` *(in src.img2nl.features.scene)* | 18 ⚠ | 2 | 28 | **30** |
| `t` *(in src.img2nl.i18n.translate)* | 5 | 19 | 8 | **27** |
| `query_uri` *(in packages.uri2img2nl.src.uri2img2nl.query)* | 9 | 2 | 17 | **19** |
| `analyze_semantic` *(in src.img2nl.features.semantic)* | 9 | 1 | 17 | **18** |
| `main` *(in packages.dsl2img2nl.src.dsl2img2nl.cli)* | 8 | 0 | 15 | **15** |

```toon markpact:analysis path=project/calls.toon.yaml
# code2llm call graph | /home/tom/github/wronai/img2nl
# generated in 0.07s
# nodes: 43 | edges: 47 | modules: 21
# CC̄=5.3

HUBS[20]:
  src.img2nl.describe._describe_catalog
    CC=17  in:3  out:72  total:75
  src.img2nl.llm_gate.llm_transport_hint
    CC=27  in:1  out:54  total:55
  src.img2nl.analyze.analyze_image
    CC=6  in:6  out:29  total:35
  src.img2nl.features.scene.classify_scene
    CC=18  in:2  out:28  total:30
  src.img2nl.i18n.translate.t
    CC=5  in:19  out:8  total:27
  packages.uri2img2nl.src.uri2img2nl.query.query_uri
    CC=9  in:2  out:17  total:19
  src.img2nl.features.semantic.analyze_semantic
    CC=9  in:1  out:17  total:18
  packages.dsl2img2nl.src.dsl2img2nl.cli.main
    CC=8  in:0  out:15  total:15
  src.img2nl.i18n.offline.translate_summary_offline
    CC=7  in:1  out:14  total:15
  packages.dsl2img2nl.src.dsl2img2nl.bus.dispatch
    CC=8  in:3  out:11  total:14
  src.img2nl.i18n.offline.ensure_language_pair
    CC=11  in:2  out:12  total:14
  src.img2nl.features.ocr_text.analyze_ocr
    CC=7  in:1  out:12  total:13
  src.img2nl.i18n.locales.normalize_locale
    CC=8  in:8  out:4  total:12
  packages.cli2img2nl.src.cli2img2nl.cli.main
    CC=6  in:0  out:11  total:11
  packages.dsl2img2nl.src.dsl2img2nl.grammar.parse_line
    CC=14  in:1  out:10  total:11
  src.img2nl.features.barcodes.analyze_barcodes
    CC=5  in:1  out:9  total:10
  src.img2nl.features.fingerprint.analyze_fingerprint
    CC=2  in:1  out:8  total:9
  packages.dsl2img2nl.src.dsl2img2nl.handlers.handle_from_tokens
    CC=4  in:1  out:8  total:9
  packages.uri2img2nl.src.uri2img2nl.cli.main
    CC=4  in:0  out:9  total:9
  packages.dsl2img2nl.src.dsl2img2nl.handlers.handle_query
    CC=6  in:1  out:8  total:9

MODULES:
  packages.cli2img2nl.src.cli2img2nl.cli  [1 funcs]
    main  CC=6  out:11
  packages.dsl2img2nl.src.dsl2img2nl.bus  [2 funcs]
    dispatch  CC=8  out:11
    execute_dsl_line  CC=1  out:1
  packages.dsl2img2nl.src.dsl2img2nl.cli  [1 funcs]
    main  CC=8  out:15
  packages.dsl2img2nl.src.dsl2img2nl.grammar  [2 funcs]
    parse_line  CC=14  out:10
    split_command  CC=1  out:2
  packages.dsl2img2nl.src.dsl2img2nl.handlers  [4 funcs]
    handle_analyze  CC=4  out:7
    handle_from_tokens  CC=4  out:8
    handle_llm_hint  CC=4  out:6
    handle_query  CC=6  out:8
  packages.uri2img2nl.src.uri2img2nl.cli  [1 funcs]
    main  CC=4  out:9
  packages.uri2img2nl.src.uri2img2nl.query  [1 funcs]
    query_uri  CC=9  out:17
  packages.uri2img2nl.src.uri2img2nl.uri  [2 funcs]
    parse_img2nl_uri  CC=5  out:7
    uri_for_analyze  CC=2  out:1
  src.img2nl.analyze  [1 funcs]
    analyze_image  CC=6  out:29
  src.img2nl.describe  [2 funcs]
    _describe_catalog  CC=17  out:72
    describe_image  CC=8  out:5
  src.img2nl.features.barcodes  [3 funcs]
    _should_scan  CC=3  out:7
    _suppress_zbar_stderr  CC=1  out:7
    analyze_barcodes  CC=5  out:9
  src.img2nl.features.fingerprint  [2 funcs]
    _unavailable  CC=1  out:0
    analyze_fingerprint  CC=2  out:8
  src.img2nl.features.ocr_text  [3 funcs]
    _preview  CC=2  out:3
    _should_ocr  CC=3  out:5
    analyze_ocr  CC=7  out:12
  src.img2nl.features.scene  [1 funcs]
    classify_scene  CC=18  out:28
  src.img2nl.features.semantic  [3 funcs]
    _get_model  CC=2  out:1
    _should_detect  CC=2  out:2
    analyze_semantic  CC=9  out:17
  src.img2nl.features.similarity  [2 funcs]
    compare_fingerprints  CC=4  out:6
    fingerprint_hamming  CC=5  out:2
  src.img2nl.features.special_hits  [1 funcs]
    analyze_special_hits  CC=1  out:4
  src.img2nl.i18n.locales  [2 funcs]
    is_european_locale  CC=1  out:1
    normalize_locale  CC=8  out:4
  src.img2nl.i18n.offline  [7 funcs]
    _require_argos  CC=2  out:1
    _update_index  CC=2  out:1
    argostranslate_available  CC=2  out:0
    ensure_language_pair  CC=11  out:12
    list_available_pairs  CC=5  out:4
    list_installed_pairs  CC=3  out:4
    translate_summary_offline  CC=7  out:14
  src.img2nl.i18n.translate  [1 funcs]
    t  CC=5  out:8
  src.img2nl.llm_gate  [1 funcs]
    llm_transport_hint  CC=27  out:54

EDGES:
  packages.dsl2img2nl.src.dsl2img2nl.handlers.handle_analyze → src.img2nl.analyze.analyze_image
  packages.dsl2img2nl.src.dsl2img2nl.handlers.handle_query → packages.uri2img2nl.src.uri2img2nl.query.query_uri
  packages.dsl2img2nl.src.dsl2img2nl.handlers.handle_query → packages.uri2img2nl.src.uri2img2nl.uri.uri_for_analyze
  packages.dsl2img2nl.src.dsl2img2nl.handlers.handle_llm_hint → src.img2nl.analyze.analyze_image
  packages.dsl2img2nl.src.dsl2img2nl.handlers.handle_from_tokens → packages.dsl2img2nl.src.dsl2img2nl.handlers.handle_analyze
  packages.dsl2img2nl.src.dsl2img2nl.handlers.handle_from_tokens → packages.dsl2img2nl.src.dsl2img2nl.handlers.handle_query
  packages.dsl2img2nl.src.dsl2img2nl.handlers.handle_from_tokens → packages.dsl2img2nl.src.dsl2img2nl.handlers.handle_llm_hint
  packages.dsl2img2nl.src.dsl2img2nl.cli.main → packages.dsl2img2nl.src.dsl2img2nl.bus.dispatch
  packages.dsl2img2nl.src.dsl2img2nl.bus.dispatch → packages.dsl2img2nl.src.dsl2img2nl.grammar.split_command
  packages.dsl2img2nl.src.dsl2img2nl.bus.dispatch → packages.dsl2img2nl.src.dsl2img2nl.handlers.handle_from_tokens
  packages.dsl2img2nl.src.dsl2img2nl.bus.dispatch → packages.dsl2img2nl.src.dsl2img2nl.grammar.parse_line
  packages.dsl2img2nl.src.dsl2img2nl.bus.execute_dsl_line → packages.dsl2img2nl.src.dsl2img2nl.bus.dispatch
  src.img2nl.features.ocr_text.analyze_ocr → src.img2nl.features.ocr_text._preview
  src.img2nl.features.ocr_text.analyze_ocr → src.img2nl.features.ocr_text._should_ocr
  src.img2nl.features.semantic.analyze_semantic → src.img2nl.features.semantic._get_model
  src.img2nl.features.semantic.analyze_semantic → src.img2nl.features.semantic._should_detect
  src.img2nl.features.fingerprint.analyze_fingerprint → src.img2nl.features.fingerprint._unavailable
  src.img2nl.features.similarity.compare_fingerprints → src.img2nl.features.similarity.fingerprint_hamming
  src.img2nl.features.special_hits.analyze_special_hits → src.img2nl.features.barcodes.analyze_barcodes
  src.img2nl.features.special_hits.analyze_special_hits → src.img2nl.features.ocr_text.analyze_ocr
  src.img2nl.i18n.translate.t → src.img2nl.i18n.locales.normalize_locale
  src.img2nl.features.barcodes.analyze_barcodes → src.img2nl.features.barcodes._suppress_zbar_stderr
  src.img2nl.features.barcodes.analyze_barcodes → src.img2nl.features.barcodes._should_scan
  src.img2nl.i18n.locales.is_european_locale → src.img2nl.i18n.locales.normalize_locale
  src.img2nl.analyze.analyze_image → src.img2nl.features.scene.classify_scene
  src.img2nl.analyze.analyze_image → src.img2nl.features.special_hits.analyze_special_hits
  src.img2nl.analyze.analyze_image → src.img2nl.i18n.locales.normalize_locale
  src.img2nl.analyze.analyze_image → src.img2nl.describe.describe_image
  src.img2nl.analyze.analyze_image → src.img2nl.llm_gate.llm_transport_hint
  packages.uri2img2nl.src.uri2img2nl.cli.main → packages.uri2img2nl.src.uri2img2nl.query.query_uri
  src.img2nl.i18n.offline.list_installed_pairs → src.img2nl.i18n.offline._require_argos
  src.img2nl.i18n.offline.list_installed_pairs → src.img2nl.i18n.offline.argostranslate_available
  src.img2nl.i18n.offline.list_available_pairs → src.img2nl.i18n.offline._require_argos
  src.img2nl.i18n.offline.list_available_pairs → src.img2nl.i18n.offline._update_index
  src.img2nl.i18n.offline.ensure_language_pair → src.img2nl.i18n.locales.normalize_locale
  src.img2nl.i18n.offline.ensure_language_pair → src.img2nl.i18n.offline._require_argos
  src.img2nl.i18n.offline.ensure_language_pair → src.img2nl.i18n.offline._update_index
  src.img2nl.i18n.offline.translate_summary_offline → src.img2nl.i18n.locales.normalize_locale
  src.img2nl.i18n.offline.translate_summary_offline → src.img2nl.i18n.offline._require_argos
  src.img2nl.i18n.offline.translate_summary_offline → src.img2nl.i18n.offline.argostranslate_available
  packages.dsl2img2nl.src.dsl2img2nl.grammar.parse_line → packages.dsl2img2nl.src.dsl2img2nl.grammar.split_command
  packages.cli2img2nl.src.cli2img2nl.cli.main → packages.dsl2img2nl.src.dsl2img2nl.bus.dispatch
  src.img2nl.describe.describe_image → src.img2nl.i18n.locales.normalize_locale
  src.img2nl.describe.describe_image → src.img2nl.describe._describe_catalog
  src.img2nl.describe.describe_image → src.img2nl.i18n.offline.translate_summary_offline
  packages.uri2img2nl.src.uri2img2nl.query.query_uri → packages.uri2img2nl.src.uri2img2nl.uri.parse_img2nl_uri
  packages.uri2img2nl.src.uri2img2nl.query.query_uri → src.img2nl.analyze.analyze_image
```

## Test Contracts

*Scenarios as contract signatures — what the system guarantees.*

### Cli (1)

**`CLI Command Tests`**

## Intent

Image → natural language summary with heuristics, thumbnails, and LLM transport hints
