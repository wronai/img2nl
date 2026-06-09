# img2nl

SUMD - Structured Unified Markdown Descriptor for AI-aware project refactorization

## Contents

- [Metadata](#metadata)
- [Architecture](#architecture)
- [Workflows](#workflows)
- [Dependencies](#dependencies)
- [Call Graph](#call-graph)
- [Test Contracts](#test-contracts)
- [Refactoring Analysis](#refactoring-analysis)
- [Intent](#intent)

## Metadata

- **name**: `img2nl`
- **version**: `0.1.3`
- **python_requires**: `>=3.10`
- **license**: Apache-2.0
- **ai_model**: `openrouter/qwen/qwen3-coder-next`
- **ecosystem**: SUMD + DOQL + testql + taskfile
- **generated_from**: pyproject.toml, Makefile, testql(1), app.doql.less, goal.yaml, .env.example, project/(5 analysis files)

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

## Workflows

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

## Refactoring Analysis

*Pre-refactoring snapshot — use this section to identify targets. Generated from `project/` toon files.*

### Call Graph & Complexity (`project/calls.toon.yaml`)

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

### Code Analysis (`project/analysis.toon.yaml`)

```toon markpact:analysis path=project/analysis.toon.yaml
# code2llm | 49f 4200L | python:38,toml:4,shell:3,json:2,yaml:1 | 2026-06-09
# generated in 0.03s
# CC̅=5.3 | critical:3/63 | dups:0 | cycles:0

HEALTH[3]:
  🟡 CC    classify_scene CC=18 (limit:15)
  🟡 CC    _describe_catalog CC=17 (limit:15)
  🟡 CC    llm_transport_hint CC=27 (limit:15)

REFACTOR[1]:
  1. split 3 high-CC methods  (CC>15)

PIPELINES[11]:
  [1] Src [main]: main → dispatch → split_command
      PURITY: 100% pure
  [2] Src [execute_dsl_line]: execute_dsl_line → dispatch → split_command
      PURITY: 100% pure
  [3] Src [main]: main → analyze_image → classify_scene
      PURITY: 100% pure
  [4] Src [compare_images_ssim]: compare_images_ssim
      PURITY: 100% pure
  [5] Src [_load_messages]: _load_messages
      PURITY: 100% pure
  [6] Src [supported_locales]: supported_locales
      PURITY: 100% pure
  [7] Src [is_european_locale]: is_european_locale → normalize_locale
      PURITY: 100% pure
  [8] Src [main]: main → query_uri → parse_img2nl_uri
      PURITY: 100% pure
  [9] Src [main]: main → dispatch → split_command
      PURITY: 100% pure
  [10] Src [is_img2nl_uri]: is_img2nl_uri
      PURITY: 100% pure
  [11] Src [uri_for_llm_hint]: uri_for_llm_hint
      PURITY: 100% pure

LAYERS:
  src/                            CC̄=5.7    ←in:0  →out:0
  │ !! messages.json             1122L  0C    0m  CC=0.0    ←0
  │ offline                    189L  1C    8m  CC=11     ←2
  │ !! describe                   132L  0C    2m  CC=17     ←1
  │ objects                    103L  0C    2m  CC=14     ←1
  │ analyze                     95L  0C    1m  CC=6      ←3
  │ !! llm_gate                    88L  0C    1m  CC=27     ←1
  │ cli                         85L  0C    1m  CC=14     ←0
  │ semantic                    84L  0C    3m  CC=9      ←1
  │ barcodes                    78L  0C    3m  CC=5      ←1
  │ ocr_text                    73L  0C    3m  CC=7      ←1
  │ similarity                  73L  0C    3m  CC=5      ←1
  │ !! scene                       65L  0C    1m  CC=18     ←1
  │ locales                     59L  0C    3m  CC=8      ←4
  │ edges                       54L  0C    2m  CC=6      ←1
  │ patterns                    53L  0C    1m  CC=8      ←1
  │ colors                      51L  0C    2m  CC=13     ←1
  │ result                      34L  1C    1m  CC=1      ←0
  │ __init__                    31L  0C    0m  CC=0.0    ←0
  │ fingerprint                 30L  0C    2m  CC=2      ←1
  │ noise                       29L  0C    1m  CC=6      ←1
  │ thumbnail                   29L  0C    1m  CC=4      ←1
  │ dynamics                    28L  0C    1m  CC=1      ←1
  │ __init__                    26L  0C    0m  CC=0.0    ←0
  │ __init__                    25L  0C    0m  CC=0.0    ←0
  │ special_hits                19L  0C    1m  CC=1      ←1
  │ translate                   16L  0C    1m  CC=5      ←1
  │ catalog                     16L  0C    1m  CC=2      ←0
  │
  packages/                       CC̄=4.4    ←in:0  →out:0
  │ query                      106L  1C    2m  CC=9      ←2
  │ handlers                    77L  0C    4m  CC=6      ←1
  │ uri                         46L  1C    4m  CC=5      ←2
  │ grammar                     45L  0C    2m  CC=14     ←1
  │ cli                         33L  0C    1m  CC=8      ←0
  │ cli                         32L  0C    1m  CC=6      ←0
  │ bus                         29L  0C    2m  CC=8      ←2
  │ cli                         28L  0C    1m  CC=4      ←0
  │ result                      26L  1C    1m  CC=1      ←0
  │ pyproject.toml              18L  0C    0m  CC=0.0    ←0
  │ pyproject.toml              18L  0C    0m  CC=0.0    ←0
  │ pyproject.toml              18L  0C    0m  CC=0.0    ←0
  │ __init__                     6L  0C    0m  CC=0.0    ←0
  │ __init__                     6L  0C    0m  CC=0.0    ←0
  │
  ./                              CC̄=0.0    ←in:0  →out:0
  │ !! goal.yaml                  512L  0C    0m  CC=0.0    ←0
  │ pyproject.toml              82L  0C    0m  CC=0.0    ←0
  │ project.sh                  59L  0C    0m  CC=0.0    ←0
  │ Makefile                    21L  0C    0m  CC=0.0    ←0
  │ install-dev.sh              11L  0C    0m  CC=0.0    ←0
  │ tree.sh                      1L  0C    0m  CC=0.0    ←0
  │
  scripts/                        CC̄=0.0    ←in:0  →out:0
  │ messages.extra.json        277L  0C    0m  CC=0.0    ←0
  │ build_i18n_catalog          62L  0C    0m  CC=0.0    ←0
  │

COUPLING:
                       packages.dsl2img2nl  packages.uri2img2nl           src.img2nl  packages.cli2img2nl
  packages.dsl2img2nl                   ──                    2                    2                   ←1
  packages.uri2img2nl                   ←2                   ──                    3                     
           src.img2nl                   ←2                   ←3                   ──                       hub
  packages.cli2img2nl                    1                                                             ──
  CYCLES: none
  HUB: src.img2nl/ (fan-in=5)

EXTERNAL:
  validation: run `vallm batch .` → validation.toon
  duplication: run `redup scan .` → duplication.toon
```

### Duplication (`project/duplication.toon.yaml`)

```toon markpact:analysis path=project/duplication.toon.yaml
# redup/duplication | 0 groups | 38f 2061L | 2026-06-09

SUMMARY:
  files_scanned: 38
  total_lines:   2061
  dup_groups:    0
  dup_fragments: 0
  saved_lines:   0
  scan_ms:       6353
```

### Evolution / Churn (`project/evolution.toon.yaml`)

```toon markpact:analysis path=project/evolution.toon.yaml
# code2llm/evolution | 63 func | 32f | 2026-06-09
# generated in 0.01s

NEXT[5] (ranked by impact):
  [1] !! SPLIT-FUNC      llm_transport_hint  CC=27  fan=14
      WHY: CC=27 exceeds 15
      EFFORT: ~1h  IMPACT: 378

  [2] !  SPLIT-FUNC      _describe_catalog  CC=17  fan=16
      WHY: CC=17 exceeds 15
      EFFORT: ~1h  IMPACT: 272

  [3] !  SPLIT-FUNC      classify_scene  CC=18  fan=10
      WHY: CC=18 exceeds 15
      EFFORT: ~1h  IMPACT: 180

  [4] !! SPLIT           src/img2nl/i18n/messages.json
      WHY: 1122L, 0 classes, max CC=0
      EFFORT: ~4h  IMPACT: 0

  [5] !! SPLIT           goal.yaml
      WHY: 512L, 0 classes, max CC=0
      EFFORT: ~4h  IMPACT: 0


RISKS[2]:
  ⚠ Splitting src/img2nl/i18n/messages.json may break 0 import paths
  ⚠ Splitting goal.yaml may break 0 import paths

METRICS-TARGET:
  CC̄:          5.3 → ≤3.7
  max-CC:      27 → ≤13
  god-modules: 2 → 0
  high-CC(≥15): 3 → ≤1
  hub-types:   0 → ≤0

PATTERNS (language parser shared logic):
  _extract_declarations() in base.py — unified extraction for:
    - TypeScript: interfaces, types, classes, functions, arrow funcs
    - PHP: namespaces, traits, classes, functions, includes
    - Ruby: modules, classes, methods, requires
    - C++: classes, structs, functions, #includes
    - C#: classes, interfaces, methods, usings
    - Java: classes, interfaces, methods, imports
    - Go: packages, functions, structs
    - Rust: modules, functions, traits, use statements

  Shared regex patterns per language:
    - import: language-specific import/require/using patterns
    - class: class/struct/trait declarations with inheritance
    - function: function/method signatures with visibility
    - brace_tracking: for C-family languages ({ })
    - end_keyword_tracking: for Ruby (module/class/def...end)

  Benefits:
    - Consistent extraction logic across all languages
    - Reduced code duplication (~70% reduction in parser LOC)
    - Easier maintenance: fix once, apply everywhere
    - Standardized FunctionInfo/ClassInfo models

HISTORY:
  (first run — no previous data)
```

## Intent

Image → natural language summary with heuristics, thumbnails, and LLM transport hints
