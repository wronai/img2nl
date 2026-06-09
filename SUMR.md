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
- **version**: `0.1.5`
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
  version: 0.1.5;
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

tests {
  import: testql-scenarios/**/*.testql.toon.yaml;
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

*136 nodes · 145 edges · 43 modules · CC̄=3.7*

### Hubs (by degree)

| Function | CC | in | out | total |
|----------|----|----|-----|-------|
| `analyze_patterns` *(in src.img2nl.features.patterns)* | 8 | 1 | 31 | **32** |
| `analyze_objects` *(in src.img2nl.features.objects)* | 11 ⚠ | 1 | 26 | **27** |
| `t` *(in src.img2nl.i18n.translate)* | 5 | 19 | 8 | **27** |
| `analyze_colors` *(in src.img2nl.features.colors)* | 13 ⚠ | 1 | 25 | **26** |
| `_describe_catalog` *(in src.img2nl.describe)* | 1 | 3 | 21 | **24** |
| `analyze_image` *(in src.img2nl.analyze)* | 4 | 6 | 18 | **24** |
| `analyze_edges` *(in src.img2nl.features.edges)* | 6 | 1 | 21 | **22** |
| `capture_screenshot` *(in src.img2nl.capture)* | 11 ⚠ | 3 | 18 | **21** |

```toon markpact:analysis path=project/calls.toon.yaml
# code2llm call graph | /home/tom/github/wronai/img2nl
# generated in 0.06s
# nodes: 136 | edges: 145 | modules: 43
# CC̄=3.7

HUBS[20]:
  src.img2nl.features.patterns.analyze_patterns
    CC=8  in:1  out:31  total:32
  src.img2nl.features.objects.analyze_objects
    CC=11  in:1  out:26  total:27
  src.img2nl.i18n.translate.t
    CC=5  in:19  out:8  total:27
  src.img2nl.features.colors.analyze_colors
    CC=13  in:1  out:25  total:26
  src.img2nl.describe._describe_catalog
    CC=1  in:3  out:21  total:24
  src.img2nl.analyze.analyze_image
    CC=4  in:6  out:18  total:24
  src.img2nl.features.edges.analyze_edges
    CC=6  in:1  out:21  total:22
  src.img2nl.capture.capture_screenshot
    CC=11  in:3  out:18  total:21
  packages.uri2img2nl.src.uri2img2nl.uri.parse_img2nl_uri
    CC=14  in:1  out:19  total:20
  src.img2nl.llm_gate.llm_transport_hint
    CC=3  in:1  out:19  total:20
  src.img2nl.features.semantic.analyze_semantic
    CC=9  in:1  out:17  total:18
  src.img2nl.features.targets.build_target_report
    CC=8  in:1  out:16  total:17
  src.img2nl.features.identify_matchers.collect_ui
    CC=6  in:0  out:17  total:17
  src.img2nl.cli_commands.cmd_analyze
    CC=7  in:0  out:16  total:16
  src.img2nl.features.noise.analyze_noise
    CC=6  in:1  out:15  total:16
  src.img2nl.cli._add_analyze_parser
    CC=1  in:1  out:15  total:16
  packages.dsl2img2nl.src.dsl2img2nl.cli.main
    CC=8  in:0  out:15  total:15
  src.img2nl.profiles.analyze_kwargs_from_cmd
    CC=10  in:4  out:11  total:15
  src.img2nl.i18n.offline.translate_summary_offline
    CC=7  in:1  out:14  total:15
  packages.dsl2img2nl.src.dsl2img2nl.bus.dispatch
    CC=8  in:3  out:11  total:14

MODULES:
  packages.cli2img2nl.src.cli2img2nl.cli  [1 funcs]
    main  CC=6  out:11
  packages.dsl2img2nl.src.dsl2img2nl.bus  [2 funcs]
    dispatch  CC=8  out:11
    execute_dsl_line  CC=1  out:1
  packages.dsl2img2nl.src.dsl2img2nl.cli  [1 funcs]
    main  CC=8  out:15
  packages.dsl2img2nl.src.dsl2img2nl.grammar  [10 funcs]
    _apply_positional  CC=4  out:2
    _consume_kv  CC=2  out:1
    _consume_token  CC=3  out:2
    _finalize_cmd  CC=3  out:0
    _normalize_token  CC=1  out:2
    _parse_bool  CC=1  out:2
    _try_bool_flag  CC=4  out:5
    _try_kv_token  CC=3  out:4
    parse_line  CC=3  out:5
    split_command  CC=1  out:2
  packages.dsl2img2nl.src.dsl2img2nl.handlers  [8 funcs]
    _require_path  CC=5  out:2
    handle_analyze  CC=3  out:6
    handle_capture  CC=3  out:9
    handle_capture_analyze  CC=3  out:6
    handle_from_tokens  CC=2  out:8
    handle_llm_hint  CC=3  out:8
    handle_query  CC=6  out:8
    handle_targets  CC=4  out:7
  packages.uri2img2nl.src.uri2img2nl.cli  [1 funcs]
    main  CC=4  out:9
  packages.uri2img2nl.src.uri2img2nl.query  [1 funcs]
    query_uri  CC=3  out:6
  packages.uri2img2nl.src.uri2img2nl.query_handlers  [8 funcs]
    _analyze_failure  CC=1  out:1
    _missing_path  CC=1  out:1
    cmd_from_uri  CC=1  out:0
    handle_analyze  CC=3  out:7
    handle_capture_analyze  CC=3  out:7
    handle_llm_hint  CC=3  out:7
    handle_targets  CC=4  out:9
    handle_text  CC=3  out:5
  packages.uri2img2nl.src.uri2img2nl.uri  [6 funcs]
    _bool_param  CC=2  out:3
    _encode_params  CC=5  out:4
    parse_img2nl_uri  CC=14  out:19
    uri_for_analyze  CC=4  out:1
    uri_for_capture_analyze  CC=1  out:1
    uri_for_targets  CC=1  out:1
  src.img2nl.analyze  [4 funcs]
    _assemble_result  CC=2  out:6
    _open_image  CC=1  out:1
    _require_pillow  CC=2  out:0
    analyze_image  CC=4  out:18
  src.img2nl.api  [6 funcs]
    analyze_from_cmd  CC=1  out:2
    capture_analyze_from_cmd  CC=3  out:11
    capture_from_cmd  CC=3  out:7
    llm_hint_from_path  CC=2  out:1
    targets_from_cmd  CC=3  out:5
    text_from_path  CC=3  out:2
  src.img2nl.capture  [2 funcs]
    capture_and_analyze  CC=2  out:7
    capture_screenshot  CC=11  out:18
  src.img2nl.cli  [6 funcs]
    _add_analyze_parser  CC=1  out:15
    _add_capture_analyze_parser  CC=1  out:12
    _add_capture_parser  CC=1  out:6
    _add_translate_install_parser  CC=1  out:6
    build_parser  CC=1  out:6
    main  CC=1  out:3
  src.img2nl.cli_commands  [6 funcs]
    _profile_kwargs  CC=1  out:1
    _target_list  CC=4  out:3
    cmd_analyze  CC=7  out:16
    cmd_capture  CC=4  out:8
    cmd_capture_analyze  CC=6  out:13
    cmd_translate_install  CC=8  out:8
  src.img2nl.context  [2 funcs]
    default_targets  CC=1  out:2
    infer_source_type  CC=11  out:8
  src.img2nl.describe  [4 funcs]
    _describe_brightness_dynamics  CC=3  out:10
    _describe_catalog  CC=1  out:21
    _describe_color_parts  CC=3  out:10
    describe_image  CC=8  out:5
  src.img2nl.features.barcodes  [3 funcs]
    _should_scan  CC=3  out:7
    _suppress_zbar_stderr  CC=1  out:7
    analyze_barcodes  CC=5  out:9
  src.img2nl.features.colors  [1 funcs]
    analyze_colors  CC=13  out:25
  src.img2nl.features.dynamics  [1 funcs]
    analyze_dynamics  CC=1  out:5
  src.img2nl.features.edges  [1 funcs]
    analyze_edges  CC=6  out:21
  src.img2nl.features.extractors  [2 funcs]
    apply_semantic_layer  CC=1  out:1
    extract_base_features  CC=2  out:11
  src.img2nl.features.fingerprint  [2 funcs]
    _unavailable  CC=1  out:0
    analyze_fingerprint  CC=2  out:8
  src.img2nl.features.identify_matchers  [2 funcs]
    collect_ui  CC=6  out:17
    identify_from_features  CC=2  out:2
  src.img2nl.features.matchers_common  [1 funcs]
    match_ui_role  CC=2  out:4
  src.img2nl.features.noise  [1 funcs]
    analyze_noise  CC=6  out:15
  src.img2nl.features.objects  [1 funcs]
    analyze_objects  CC=11  out:26
  src.img2nl.features.ocr_text  [3 funcs]
    _preview  CC=2  out:3
    _should_ocr  CC=3  out:5
    analyze_ocr  CC=7  out:12
  src.img2nl.features.patterns  [1 funcs]
    analyze_patterns  CC=8  out:31
  src.img2nl.features.presence_matchers  [5 funcs]
    _absent  CC=1  out:1
    _best_semantic_object  CC=9  out:5
    match_semantic  CC=3  out:8
    match_ui  CC=7  out:14
    presence_from_features  CC=5  out:3
  src.img2nl.features.router  [3 funcs]
    _active_adapters  CC=3  out:6
    analyze_targets  CC=3  out:6
    execute_target_plan  CC=3  out:6
  src.img2nl.features.scene  [6 funcs]
    _scene_dense_from_edges  CC=4  out:5
    _scene_from_heuristics  CC=11  out:11
    _scene_from_similarity  CC=2  out:2
    _scene_from_special  CC=2  out:2
    _scene_general_fallback  CC=4  out:4
    classify_scene  CC=3  out:9
  src.img2nl.features.semantic  [3 funcs]
    _get_model  CC=2  out:1
    _should_detect  CC=2  out:2
    analyze_semantic  CC=9  out:17
  src.img2nl.features.similarity  [2 funcs]
    compare_fingerprints  CC=4  out:6
    fingerprint_hamming  CC=5  out:2
  src.img2nl.features.special_hits  [1 funcs]
    analyze_special_hits  CC=1  out:4
  src.img2nl.features.targets  [4 funcs]
    _bbox_center  CC=2  out:1
    best_detection  CC=8  out:12
    build_target_report  CC=8  out:16
    find_click_point  CC=5  out:9
  src.img2nl.features.ui_adapter  [4 funcs]
    _from_imgl_elements  CC=2  out:4
    _try_imgl_bridge  CC=3  out:2
    _try_imgl_local  CC=2  out:3
    analyze_ui_targets  CC=4  out:4
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
    llm_transport_hint  CC=3  out:19
  src.img2nl.plan  [5 funcs]
    build_execution_plan  CC=1  out:6
    resolve_targets  CC=6  out:4
    should_run_identify  CC=2  out:0
    should_run_semantic  CC=5  out:0
    should_run_ui_detect  CC=3  out:0
  src.img2nl.profiles  [4 funcs]
    analyze_kwargs_from_cmd  CC=10  out:11
    apply_profile  CC=5  out:2
    get_profile  CC=2  out:6
    list_profiles  CC=1  out:1
  src.img2nl.thumbnail  [1 funcs]
    make_thumbnail  CC=4  out:12

EDGES:
  packages.cli2img2nl.src.cli2img2nl.cli.main → packages.dsl2img2nl.src.dsl2img2nl.bus.dispatch
  packages.dsl2img2nl.src.dsl2img2nl.bus.dispatch → packages.dsl2img2nl.src.dsl2img2nl.grammar.split_command
  packages.dsl2img2nl.src.dsl2img2nl.bus.dispatch → packages.dsl2img2nl.src.dsl2img2nl.handlers.handle_from_tokens
  packages.dsl2img2nl.src.dsl2img2nl.bus.dispatch → packages.dsl2img2nl.src.dsl2img2nl.grammar.parse_line
  packages.dsl2img2nl.src.dsl2img2nl.bus.execute_dsl_line → packages.dsl2img2nl.src.dsl2img2nl.bus.dispatch
  packages.dsl2img2nl.src.dsl2img2nl.cli.main → packages.dsl2img2nl.src.dsl2img2nl.bus.dispatch
  packages.dsl2img2nl.src.dsl2img2nl.grammar._try_kv_token → packages.dsl2img2nl.src.dsl2img2nl.grammar._normalize_token
  packages.dsl2img2nl.src.dsl2img2nl.grammar._try_kv_token → packages.dsl2img2nl.src.dsl2img2nl.grammar._consume_kv
  packages.dsl2img2nl.src.dsl2img2nl.grammar._try_bool_flag → packages.dsl2img2nl.src.dsl2img2nl.grammar._normalize_token
  packages.dsl2img2nl.src.dsl2img2nl.grammar._try_bool_flag → packages.dsl2img2nl.src.dsl2img2nl.grammar._parse_bool
  packages.dsl2img2nl.src.dsl2img2nl.grammar._consume_token → packages.dsl2img2nl.src.dsl2img2nl.grammar._apply_positional
  packages.dsl2img2nl.src.dsl2img2nl.grammar.parse_line → packages.dsl2img2nl.src.dsl2img2nl.grammar.split_command
  packages.dsl2img2nl.src.dsl2img2nl.grammar.parse_line → packages.dsl2img2nl.src.dsl2img2nl.grammar._finalize_cmd
  packages.dsl2img2nl.src.dsl2img2nl.grammar.parse_line → packages.dsl2img2nl.src.dsl2img2nl.grammar._normalize_token
  packages.dsl2img2nl.src.dsl2img2nl.grammar.parse_line → packages.dsl2img2nl.src.dsl2img2nl.grammar._consume_token
  packages.uri2img2nl.src.uri2img2nl.cli.main → packages.uri2img2nl.src.uri2img2nl.query.query_uri
  packages.uri2img2nl.src.uri2img2nl.query.query_uri → packages.uri2img2nl.src.uri2img2nl.uri.parse_img2nl_uri
  packages.uri2img2nl.src.uri2img2nl.uri.uri_for_analyze → packages.uri2img2nl.src.uri2img2nl.uri._encode_params
  packages.uri2img2nl.src.uri2img2nl.uri.uri_for_targets → packages.uri2img2nl.src.uri2img2nl.uri._encode_params
  packages.uri2img2nl.src.uri2img2nl.uri.uri_for_capture_analyze → packages.uri2img2nl.src.uri2img2nl.uri._encode_params
  packages.uri2img2nl.src.uri2img2nl.uri.parse_img2nl_uri → packages.uri2img2nl.src.uri2img2nl.uri._bool_param
  src.img2nl.describe._describe_color_parts → src.img2nl.i18n.translate.t
  src.img2nl.describe._describe_brightness_dynamics → src.img2nl.i18n.translate.t
  src.img2nl.describe.describe_image → src.img2nl.i18n.locales.normalize_locale
  src.img2nl.describe.describe_image → src.img2nl.describe._describe_catalog
  src.img2nl.describe.describe_image → src.img2nl.i18n.offline.translate_summary_offline
  src.img2nl.cli.build_parser → src.img2nl.cli._add_analyze_parser
  src.img2nl.cli.build_parser → src.img2nl.cli._add_capture_parser
  src.img2nl.cli.build_parser → src.img2nl.cli._add_capture_analyze_parser
  src.img2nl.cli.build_parser → src.img2nl.cli._add_translate_install_parser
  src.img2nl.cli.main → src.img2nl.cli.build_parser
  src.img2nl.analyze._assemble_result → src.img2nl.describe.describe_image
  src.img2nl.analyze._assemble_result → src.img2nl.llm_gate.llm_transport_hint
  src.img2nl.analyze._assemble_result → src.img2nl.thumbnail.make_thumbnail
  src.img2nl.analyze.analyze_image → src.img2nl.analyze._require_pillow
  src.img2nl.analyze.analyze_image → src.img2nl.analyze._open_image
  src.img2nl.analyze.analyze_image → src.img2nl.features.extractors.extract_base_features
  src.img2nl.analyze.analyze_image → src.img2nl.plan.build_execution_plan
  src.img2nl.analyze.analyze_image → src.img2nl.features.extractors.apply_semantic_layer
  src.img2nl.analyze.analyze_image → src.img2nl.features.router.execute_target_plan
  src.img2nl.plan.resolve_targets → src.img2nl.context.default_targets
  src.img2nl.plan.build_execution_plan → src.img2nl.context.infer_source_type
  src.img2nl.plan.build_execution_plan → src.img2nl.plan.resolve_targets
  src.img2nl.plan.build_execution_plan → src.img2nl.plan.should_run_ui_detect
  src.img2nl.plan.build_execution_plan → src.img2nl.plan.should_run_semantic
  src.img2nl.plan.build_execution_plan → src.img2nl.plan.should_run_identify
  src.img2nl.capture.capture_and_analyze → src.img2nl.capture.capture_screenshot
  src.img2nl.capture.capture_and_analyze → src.img2nl.analyze.analyze_image
  src.img2nl.profiles.get_profile → src.img2nl.profiles.list_profiles
  src.img2nl.profiles.apply_profile → src.img2nl.profiles.get_profile
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
# generated in 0.06s
# nodes: 136 | edges: 145 | modules: 43
# CC̄=3.7

HUBS[20]:
  src.img2nl.features.patterns.analyze_patterns
    CC=8  in:1  out:31  total:32
  src.img2nl.features.objects.analyze_objects
    CC=11  in:1  out:26  total:27
  src.img2nl.i18n.translate.t
    CC=5  in:19  out:8  total:27
  src.img2nl.features.colors.analyze_colors
    CC=13  in:1  out:25  total:26
  src.img2nl.describe._describe_catalog
    CC=1  in:3  out:21  total:24
  src.img2nl.analyze.analyze_image
    CC=4  in:6  out:18  total:24
  src.img2nl.features.edges.analyze_edges
    CC=6  in:1  out:21  total:22
  src.img2nl.capture.capture_screenshot
    CC=11  in:3  out:18  total:21
  packages.uri2img2nl.src.uri2img2nl.uri.parse_img2nl_uri
    CC=14  in:1  out:19  total:20
  src.img2nl.llm_gate.llm_transport_hint
    CC=3  in:1  out:19  total:20
  src.img2nl.features.semantic.analyze_semantic
    CC=9  in:1  out:17  total:18
  src.img2nl.features.targets.build_target_report
    CC=8  in:1  out:16  total:17
  src.img2nl.features.identify_matchers.collect_ui
    CC=6  in:0  out:17  total:17
  src.img2nl.cli_commands.cmd_analyze
    CC=7  in:0  out:16  total:16
  src.img2nl.features.noise.analyze_noise
    CC=6  in:1  out:15  total:16
  src.img2nl.cli._add_analyze_parser
    CC=1  in:1  out:15  total:16
  packages.dsl2img2nl.src.dsl2img2nl.cli.main
    CC=8  in:0  out:15  total:15
  src.img2nl.profiles.analyze_kwargs_from_cmd
    CC=10  in:4  out:11  total:15
  src.img2nl.i18n.offline.translate_summary_offline
    CC=7  in:1  out:14  total:15
  packages.dsl2img2nl.src.dsl2img2nl.bus.dispatch
    CC=8  in:3  out:11  total:14

MODULES:
  packages.cli2img2nl.src.cli2img2nl.cli  [1 funcs]
    main  CC=6  out:11
  packages.dsl2img2nl.src.dsl2img2nl.bus  [2 funcs]
    dispatch  CC=8  out:11
    execute_dsl_line  CC=1  out:1
  packages.dsl2img2nl.src.dsl2img2nl.cli  [1 funcs]
    main  CC=8  out:15
  packages.dsl2img2nl.src.dsl2img2nl.grammar  [10 funcs]
    _apply_positional  CC=4  out:2
    _consume_kv  CC=2  out:1
    _consume_token  CC=3  out:2
    _finalize_cmd  CC=3  out:0
    _normalize_token  CC=1  out:2
    _parse_bool  CC=1  out:2
    _try_bool_flag  CC=4  out:5
    _try_kv_token  CC=3  out:4
    parse_line  CC=3  out:5
    split_command  CC=1  out:2
  packages.dsl2img2nl.src.dsl2img2nl.handlers  [8 funcs]
    _require_path  CC=5  out:2
    handle_analyze  CC=3  out:6
    handle_capture  CC=3  out:9
    handle_capture_analyze  CC=3  out:6
    handle_from_tokens  CC=2  out:8
    handle_llm_hint  CC=3  out:8
    handle_query  CC=6  out:8
    handle_targets  CC=4  out:7
  packages.uri2img2nl.src.uri2img2nl.cli  [1 funcs]
    main  CC=4  out:9
  packages.uri2img2nl.src.uri2img2nl.query  [1 funcs]
    query_uri  CC=3  out:6
  packages.uri2img2nl.src.uri2img2nl.query_handlers  [8 funcs]
    _analyze_failure  CC=1  out:1
    _missing_path  CC=1  out:1
    cmd_from_uri  CC=1  out:0
    handle_analyze  CC=3  out:7
    handle_capture_analyze  CC=3  out:7
    handle_llm_hint  CC=3  out:7
    handle_targets  CC=4  out:9
    handle_text  CC=3  out:5
  packages.uri2img2nl.src.uri2img2nl.uri  [6 funcs]
    _bool_param  CC=2  out:3
    _encode_params  CC=5  out:4
    parse_img2nl_uri  CC=14  out:19
    uri_for_analyze  CC=4  out:1
    uri_for_capture_analyze  CC=1  out:1
    uri_for_targets  CC=1  out:1
  src.img2nl.analyze  [4 funcs]
    _assemble_result  CC=2  out:6
    _open_image  CC=1  out:1
    _require_pillow  CC=2  out:0
    analyze_image  CC=4  out:18
  src.img2nl.api  [6 funcs]
    analyze_from_cmd  CC=1  out:2
    capture_analyze_from_cmd  CC=3  out:11
    capture_from_cmd  CC=3  out:7
    llm_hint_from_path  CC=2  out:1
    targets_from_cmd  CC=3  out:5
    text_from_path  CC=3  out:2
  src.img2nl.capture  [2 funcs]
    capture_and_analyze  CC=2  out:7
    capture_screenshot  CC=11  out:18
  src.img2nl.cli  [6 funcs]
    _add_analyze_parser  CC=1  out:15
    _add_capture_analyze_parser  CC=1  out:12
    _add_capture_parser  CC=1  out:6
    _add_translate_install_parser  CC=1  out:6
    build_parser  CC=1  out:6
    main  CC=1  out:3
  src.img2nl.cli_commands  [6 funcs]
    _profile_kwargs  CC=1  out:1
    _target_list  CC=4  out:3
    cmd_analyze  CC=7  out:16
    cmd_capture  CC=4  out:8
    cmd_capture_analyze  CC=6  out:13
    cmd_translate_install  CC=8  out:8
  src.img2nl.context  [2 funcs]
    default_targets  CC=1  out:2
    infer_source_type  CC=11  out:8
  src.img2nl.describe  [4 funcs]
    _describe_brightness_dynamics  CC=3  out:10
    _describe_catalog  CC=1  out:21
    _describe_color_parts  CC=3  out:10
    describe_image  CC=8  out:5
  src.img2nl.features.barcodes  [3 funcs]
    _should_scan  CC=3  out:7
    _suppress_zbar_stderr  CC=1  out:7
    analyze_barcodes  CC=5  out:9
  src.img2nl.features.colors  [1 funcs]
    analyze_colors  CC=13  out:25
  src.img2nl.features.dynamics  [1 funcs]
    analyze_dynamics  CC=1  out:5
  src.img2nl.features.edges  [1 funcs]
    analyze_edges  CC=6  out:21
  src.img2nl.features.extractors  [2 funcs]
    apply_semantic_layer  CC=1  out:1
    extract_base_features  CC=2  out:11
  src.img2nl.features.fingerprint  [2 funcs]
    _unavailable  CC=1  out:0
    analyze_fingerprint  CC=2  out:8
  src.img2nl.features.identify_matchers  [2 funcs]
    collect_ui  CC=6  out:17
    identify_from_features  CC=2  out:2
  src.img2nl.features.matchers_common  [1 funcs]
    match_ui_role  CC=2  out:4
  src.img2nl.features.noise  [1 funcs]
    analyze_noise  CC=6  out:15
  src.img2nl.features.objects  [1 funcs]
    analyze_objects  CC=11  out:26
  src.img2nl.features.ocr_text  [3 funcs]
    _preview  CC=2  out:3
    _should_ocr  CC=3  out:5
    analyze_ocr  CC=7  out:12
  src.img2nl.features.patterns  [1 funcs]
    analyze_patterns  CC=8  out:31
  src.img2nl.features.presence_matchers  [5 funcs]
    _absent  CC=1  out:1
    _best_semantic_object  CC=9  out:5
    match_semantic  CC=3  out:8
    match_ui  CC=7  out:14
    presence_from_features  CC=5  out:3
  src.img2nl.features.router  [3 funcs]
    _active_adapters  CC=3  out:6
    analyze_targets  CC=3  out:6
    execute_target_plan  CC=3  out:6
  src.img2nl.features.scene  [6 funcs]
    _scene_dense_from_edges  CC=4  out:5
    _scene_from_heuristics  CC=11  out:11
    _scene_from_similarity  CC=2  out:2
    _scene_from_special  CC=2  out:2
    _scene_general_fallback  CC=4  out:4
    classify_scene  CC=3  out:9
  src.img2nl.features.semantic  [3 funcs]
    _get_model  CC=2  out:1
    _should_detect  CC=2  out:2
    analyze_semantic  CC=9  out:17
  src.img2nl.features.similarity  [2 funcs]
    compare_fingerprints  CC=4  out:6
    fingerprint_hamming  CC=5  out:2
  src.img2nl.features.special_hits  [1 funcs]
    analyze_special_hits  CC=1  out:4
  src.img2nl.features.targets  [4 funcs]
    _bbox_center  CC=2  out:1
    best_detection  CC=8  out:12
    build_target_report  CC=8  out:16
    find_click_point  CC=5  out:9
  src.img2nl.features.ui_adapter  [4 funcs]
    _from_imgl_elements  CC=2  out:4
    _try_imgl_bridge  CC=3  out:2
    _try_imgl_local  CC=2  out:3
    analyze_ui_targets  CC=4  out:4
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
    llm_transport_hint  CC=3  out:19
  src.img2nl.plan  [5 funcs]
    build_execution_plan  CC=1  out:6
    resolve_targets  CC=6  out:4
    should_run_identify  CC=2  out:0
    should_run_semantic  CC=5  out:0
    should_run_ui_detect  CC=3  out:0
  src.img2nl.profiles  [4 funcs]
    analyze_kwargs_from_cmd  CC=10  out:11
    apply_profile  CC=5  out:2
    get_profile  CC=2  out:6
    list_profiles  CC=1  out:1
  src.img2nl.thumbnail  [1 funcs]
    make_thumbnail  CC=4  out:12

EDGES:
  packages.cli2img2nl.src.cli2img2nl.cli.main → packages.dsl2img2nl.src.dsl2img2nl.bus.dispatch
  packages.dsl2img2nl.src.dsl2img2nl.bus.dispatch → packages.dsl2img2nl.src.dsl2img2nl.grammar.split_command
  packages.dsl2img2nl.src.dsl2img2nl.bus.dispatch → packages.dsl2img2nl.src.dsl2img2nl.handlers.handle_from_tokens
  packages.dsl2img2nl.src.dsl2img2nl.bus.dispatch → packages.dsl2img2nl.src.dsl2img2nl.grammar.parse_line
  packages.dsl2img2nl.src.dsl2img2nl.bus.execute_dsl_line → packages.dsl2img2nl.src.dsl2img2nl.bus.dispatch
  packages.dsl2img2nl.src.dsl2img2nl.cli.main → packages.dsl2img2nl.src.dsl2img2nl.bus.dispatch
  packages.dsl2img2nl.src.dsl2img2nl.grammar._try_kv_token → packages.dsl2img2nl.src.dsl2img2nl.grammar._normalize_token
  packages.dsl2img2nl.src.dsl2img2nl.grammar._try_kv_token → packages.dsl2img2nl.src.dsl2img2nl.grammar._consume_kv
  packages.dsl2img2nl.src.dsl2img2nl.grammar._try_bool_flag → packages.dsl2img2nl.src.dsl2img2nl.grammar._normalize_token
  packages.dsl2img2nl.src.dsl2img2nl.grammar._try_bool_flag → packages.dsl2img2nl.src.dsl2img2nl.grammar._parse_bool
  packages.dsl2img2nl.src.dsl2img2nl.grammar._consume_token → packages.dsl2img2nl.src.dsl2img2nl.grammar._apply_positional
  packages.dsl2img2nl.src.dsl2img2nl.grammar.parse_line → packages.dsl2img2nl.src.dsl2img2nl.grammar.split_command
  packages.dsl2img2nl.src.dsl2img2nl.grammar.parse_line → packages.dsl2img2nl.src.dsl2img2nl.grammar._finalize_cmd
  packages.dsl2img2nl.src.dsl2img2nl.grammar.parse_line → packages.dsl2img2nl.src.dsl2img2nl.grammar._normalize_token
  packages.dsl2img2nl.src.dsl2img2nl.grammar.parse_line → packages.dsl2img2nl.src.dsl2img2nl.grammar._consume_token
  packages.uri2img2nl.src.uri2img2nl.cli.main → packages.uri2img2nl.src.uri2img2nl.query.query_uri
  packages.uri2img2nl.src.uri2img2nl.query.query_uri → packages.uri2img2nl.src.uri2img2nl.uri.parse_img2nl_uri
  packages.uri2img2nl.src.uri2img2nl.uri.uri_for_analyze → packages.uri2img2nl.src.uri2img2nl.uri._encode_params
  packages.uri2img2nl.src.uri2img2nl.uri.uri_for_targets → packages.uri2img2nl.src.uri2img2nl.uri._encode_params
  packages.uri2img2nl.src.uri2img2nl.uri.uri_for_capture_analyze → packages.uri2img2nl.src.uri2img2nl.uri._encode_params
  packages.uri2img2nl.src.uri2img2nl.uri.parse_img2nl_uri → packages.uri2img2nl.src.uri2img2nl.uri._bool_param
  src.img2nl.describe._describe_color_parts → src.img2nl.i18n.translate.t
  src.img2nl.describe._describe_brightness_dynamics → src.img2nl.i18n.translate.t
  src.img2nl.describe.describe_image → src.img2nl.i18n.locales.normalize_locale
  src.img2nl.describe.describe_image → src.img2nl.describe._describe_catalog
  src.img2nl.describe.describe_image → src.img2nl.i18n.offline.translate_summary_offline
  src.img2nl.cli.build_parser → src.img2nl.cli._add_analyze_parser
  src.img2nl.cli.build_parser → src.img2nl.cli._add_capture_parser
  src.img2nl.cli.build_parser → src.img2nl.cli._add_capture_analyze_parser
  src.img2nl.cli.build_parser → src.img2nl.cli._add_translate_install_parser
  src.img2nl.cli.main → src.img2nl.cli.build_parser
  src.img2nl.analyze._assemble_result → src.img2nl.describe.describe_image
  src.img2nl.analyze._assemble_result → src.img2nl.llm_gate.llm_transport_hint
  src.img2nl.analyze._assemble_result → src.img2nl.thumbnail.make_thumbnail
  src.img2nl.analyze.analyze_image → src.img2nl.analyze._require_pillow
  src.img2nl.analyze.analyze_image → src.img2nl.analyze._open_image
  src.img2nl.analyze.analyze_image → src.img2nl.features.extractors.extract_base_features
  src.img2nl.analyze.analyze_image → src.img2nl.plan.build_execution_plan
  src.img2nl.analyze.analyze_image → src.img2nl.features.extractors.apply_semantic_layer
  src.img2nl.analyze.analyze_image → src.img2nl.features.router.execute_target_plan
  src.img2nl.plan.resolve_targets → src.img2nl.context.default_targets
  src.img2nl.plan.build_execution_plan → src.img2nl.context.infer_source_type
  src.img2nl.plan.build_execution_plan → src.img2nl.plan.resolve_targets
  src.img2nl.plan.build_execution_plan → src.img2nl.plan.should_run_ui_detect
  src.img2nl.plan.build_execution_plan → src.img2nl.plan.should_run_semantic
  src.img2nl.plan.build_execution_plan → src.img2nl.plan.should_run_identify
  src.img2nl.capture.capture_and_analyze → src.img2nl.capture.capture_screenshot
  src.img2nl.capture.capture_and_analyze → src.img2nl.analyze.analyze_image
  src.img2nl.profiles.get_profile → src.img2nl.profiles.list_profiles
  src.img2nl.profiles.apply_profile → src.img2nl.profiles.get_profile
```

### Code Analysis (`project/analysis.toon.yaml`)

```toon markpact:analysis path=project/analysis.toon.yaml
# code2llm | 68f 7133L | python:54,yaml:4,toml:4,shell:3,json:2 | 2026-06-09
# generated in 0.01s
# CC̅=3.7 | critical:0/169 | dups:0 | cycles:0

HEALTH[0]: ok

REFACTOR[0]: none needed

PIPELINES[55]:
  [1] Src [main]: main → dispatch → split_command
      PURITY: 100% pure
  [2] Src [execute_dsl_line]: execute_dsl_line → dispatch → split_command
      PURITY: 100% pure
  [3] Src [main]: main → dispatch → split_command
      PURITY: 100% pure
  [4] Src [handle_analyze]: handle_analyze → _require_path
      PURITY: 100% pure
  [5] Src [handle_targets]: handle_targets → _require_path
      PURITY: 100% pure
  [6] Src [handle_capture]: handle_capture → _require_path
      PURITY: 100% pure
  [7] Src [handle_capture_analyze]: handle_capture_analyze → _require_path
      PURITY: 100% pure
  [8] Src [handle_query]: handle_query → query_uri → parse_img2nl_uri → _bool_param
      PURITY: 100% pure
  [9] Src [handle_llm_hint]: handle_llm_hint → _require_path
      PURITY: 100% pure
  [10] Src [_try_kv_token]: _try_kv_token → _normalize_token
      PURITY: 100% pure
  [11] Src [_try_bool_flag]: _try_bool_flag → _normalize_token
      PURITY: 100% pure
  [12] Src [handle_capture_analyze]: handle_capture_analyze → _missing_path
      PURITY: 100% pure
  [13] Src [handle_targets]: handle_targets → _missing_path
      PURITY: 100% pure
  [14] Src [handle_analyze]: handle_analyze → _missing_path
      PURITY: 100% pure
  [15] Src [handle_llm_hint]: handle_llm_hint → _missing_path
      PURITY: 100% pure
  [16] Src [handle_text]: handle_text → _missing_path
      PURITY: 100% pure
  [17] Src [main]: main → query_uri → parse_img2nl_uri → _bool_param
      PURITY: 100% pure
  [18] Src [is_img2nl_uri]: is_img2nl_uri
      PURITY: 100% pure
  [19] Src [uri_for_targets]: uri_for_targets → _encode_params
      PURITY: 100% pure
  [20] Src [uri_for_capture_analyze]: uri_for_capture_analyze → _encode_params
      PURITY: 100% pure
  [21] Src [uri_for_llm_hint]: uri_for_llm_hint
      PURITY: 100% pure
  [22] Src [main]: main → build_parser → _add_analyze_parser
      PURITY: 100% pure
  [23] Src [analyze_from_cmd]: analyze_from_cmd → analyze_image → _require_pillow
      PURITY: 100% pure
  [24] Src [targets_from_cmd]: targets_from_cmd → analyze_kwargs_from_cmd → get_profile → list_profiles
      PURITY: 100% pure
  [25] Src [capture_from_cmd]: capture_from_cmd → capture_screenshot
      PURITY: 100% pure
  [26] Src [capture_analyze_from_cmd]: capture_analyze_from_cmd → analyze_kwargs_from_cmd → get_profile → list_profiles
      PURITY: 100% pure
  [27] Src [llm_hint_from_path]: llm_hint_from_path → analyze_image → _require_pillow
      PURITY: 100% pure
  [28] Src [text_from_path]: text_from_path → analyze_image → _require_pillow
      PURITY: 100% pure
  [29] Src [apply_profile]: apply_profile → get_profile → list_profiles
      PURITY: 100% pure
  [30] Src [cmd_analyze]: cmd_analyze → _target_list
      PURITY: 100% pure
  [31] Src [cmd_capture]: cmd_capture → capture_screenshot
      PURITY: 100% pure
  [32] Src [cmd_capture_analyze]: cmd_capture_analyze → _target_list
      PURITY: 100% pure
  [33] Src [cmd_translate_install]: cmd_translate_install → ensure_language_pair → normalize_locale
      PURITY: 100% pure
  [34] Src [analyze_targets]: analyze_targets → build_execution_plan → infer_source_type
      PURITY: 100% pure
  [35] Src [resolve_targets]: resolve_targets
      PURITY: 100% pure
  [36] Src [should_run_ui_detect]: should_run_ui_detect
      PURITY: 100% pure
  [37] Src [should_run_semantic]: should_run_semantic
      PURITY: 100% pure
  [38] Src [collect_barcodes]: collect_barcodes
      PURITY: 100% pure
  [39] Src [collect_ocr]: collect_ocr
      PURITY: 100% pure
  [40] Src [collect_ui]: collect_ui → match_ui_role
      PURITY: 100% pure
  [41] Src [collect_semantic]: collect_semantic
      PURITY: 100% pure
  [42] Src [feature_slice]: feature_slice
      PURITY: 100% pure
  [43] Src [compare_images_ssim]: compare_images_ssim
      PURITY: 100% pure
  [44] Src [match_qrcode]: match_qrcode
      PURITY: 100% pure
  [45] Src [match_text]: match_text
      PURITY: 100% pure
  [46] Src [match_semantic]: match_semantic → _best_semantic_object
      PURITY: 100% pure
  [47] Src [match_ui]: match_ui → match_ui_role
      PURITY: 100% pure
  [48] Src [to_dict]: to_dict
      PURITY: 100% pure
  [49] Src [find_click_point]: find_click_point → best_detection → _bbox_center
      PURITY: 100% pure
  [50] Src [_try_img2vql]: _try_img2vql
      PURITY: 100% pure

LAYERS:
  src/                            CC̄=3.9    ←in:0  →out:0
  │ !! messages.json             1122L  0C    0m  CC=0.0    ←0
  │ offline                    189L  1C    8m  CC=11     ←2
  │ describe                   179L  0C    7m  CC=8      ←1
  │ llm_gate                   149L  0C    7m  CC=8      ←1
  │ presence_matchers          134L  0C    7m  CC=9      ←1
  │ identify_matchers          132L  0C    5m  CC=10     ←1
  │ cli_commands               123L  0C    6m  CC=8      ←0
  │ analyze                    120L  0C    4m  CC=4      ←3
  │ plan                       111L  1C    5m  CC=6      ←2
  │ objects                    103L  0C    2m  CC=14     ←1
  │ cli                        102L  0C    6m  CC=1      ←0
  │ targets                    102L  1C    5m  CC=8      ←1
  │ router                     101L  0C    6m  CC=3      ←1
  │ profiles                    98L  0C    4m  CC=10     ←2
  │ scene                       97L  0C    6m  CC=11     ←1
  │ capture                     91L  0C    2m  CC=11     ←2
  │ semantic                    84L  0C    3m  CC=9      ←1
  │ ui_adapter                  80L  0C    5m  CC=4      ←1
  │ barcodes                    78L  0C    3m  CC=5      ←1
  │ ocr_text                    73L  0C    3m  CC=7      ←1
  │ similarity                  73L  0C    3m  CC=5      ←1
  │ context                     68L  0C    2m  CC=11     ←1
  │ api                         62L  0C    6m  CC=3      ←0
  │ locales                     59L  0C    3m  CC=8      ←4
  │ extractors                  57L  0C    2m  CC=2      ←1
  │ edges                       54L  0C    2m  CC=6      ←1
  │ patterns                    53L  0C    1m  CC=8      ←1
  │ colors                      51L  0C    2m  CC=13     ←1
  │ result                      42L  1C    1m  CC=1      ←0
  │ __init__                    37L  0C    0m  CC=0.0    ←0
  │ matchers_common             32L  0C    2m  CC=2      ←2
  │ __init__                    31L  0C    0m  CC=0.0    ←0
  │ fingerprint                 30L  0C    2m  CC=2      ←1
  │ thumbnail                   29L  0C    1m  CC=4      ←1
  │ noise                       29L  0C    1m  CC=6      ←1
  │ dynamics                    28L  0C    1m  CC=1      ←1
  │ __init__                    26L  0C    0m  CC=0.0    ←0
  │ special_hits                19L  0C    1m  CC=1      ←1
  │ translate                   16L  0C    1m  CC=5      ←1
  │ catalog                     16L  0C    1m  CC=2      ←0
  │ adapters                     9L  0C    0m  CC=0.0    ←0
  │
  packages/                       CC̄=3.1    ←in:0  →out:0
  │ query_handlers             156L  0C    8m  CC=4      ←0
  │ handlers                   148L  0C    8m  CC=6      ←1
  │ uri                        148L  1C    8m  CC=14     ←2
  │ grammar                    118L  0C   11m  CC=4      ←1
  │ cli                         33L  0C    1m  CC=8      ←0
  │ cli                         32L  0C    1m  CC=6      ←0
  │ query_result                30L  1C    1m  CC=1      ←0
  │ bus                         29L  0C    2m  CC=8      ←2
  │ cli                         28L  0C    1m  CC=4      ←0
  │ result                      26L  1C    1m  CC=1      ←0
  │ query                       26L  0C    1m  CC=3      ←2
  │ __init__                    20L  0C    0m  CC=0.0    ←0
  │ pyproject.toml              18L  0C    0m  CC=0.0    ←0
  │ pyproject.toml              18L  0C    0m  CC=0.0    ←0
  │ pyproject.toml              18L  0C    0m  CC=0.0    ←0
  │ __init__                     6L  0C    0m  CC=0.0    ←0
  │
  ./                              CC̄=0.0    ←in:0  →out:0
  │ !! planfile.yaml             1033L  0C    0m  CC=0.0    ←0
  │ !! goal.yaml                  512L  0C    0m  CC=0.0    ←0
  │ prefact.yaml                94L  0C    0m  CC=0.0    ←0
  │ pyproject.toml              85L  0C    0m  CC=0.0    ←0
  │ project.sh                  59L  0C    0m  CC=0.0    ←0
  │ install-dev.sh              26L  0C    0m  CC=0.0    ←0
  │ Makefile                    21L  0C    0m  CC=0.0    ←0
  │ tree.sh                      1L  0C    0m  CC=0.0    ←0
  │
  scripts/                        CC̄=0.0    ←in:0  →out:0
  │ messages.extra.json        277L  0C    0m  CC=0.0    ←0
  │ build_i18n_catalog          62L  0C    0m  CC=0.0    ←0
  │
  testql-scenarios/               CC̄=0.0    ←in:0  →out:0
  │ generated-cli-tests.testql.toon.yaml    20L  0C    0m  CC=0.0    ←0
  │

COUPLING:
                       packages.dsl2img2nl  packages.uri2img2nl  packages.cli2img2nl
  packages.dsl2img2nl                   ──                    2                   ←1
  packages.uri2img2nl                   ←2                   ──                     
  packages.cli2img2nl                    1                                        ──
  CYCLES: none

EXTERNAL:
  validation: run `vallm batch .` → validation.toon
  duplication: run `redup scan .` → duplication.toon
```

### Duplication (`project/duplication.toon.yaml`)

```toon markpact:analysis path=project/duplication.toon.yaml
# redup/duplication | 2 groups | 54f 3829L | 2026-06-09

SUMMARY:
  files_scanned: 54
  total_lines:   3829
  dup_groups:    2
  dup_fragments: 4
  saved_lines:   22
  scan_ms:       3791

HOTSPOTS[2] (files with most duplication):
  packages/dsl2img2nl/src/dsl2img2nl/handlers.py  dup=35L  groups=1  frags=2  (0.9%)
  src/img2nl/features/scene.py  dup=11L  groups=1  frags=2  (0.3%)

DUPLICATES[2] (ranked by impact):
  [a145f7c8b4ef4787]   STRU  handle_analyze  L=15 N=2 saved=15 sim=1.00
      packages/dsl2img2nl/src/dsl2img2nl/handlers.py:23-37  (handle_analyze)
      packages/dsl2img2nl/src/dsl2img2nl/handlers.py:73-92  (handle_capture_analyze)
  [a4a4c87e8e1cb6fe]   STRU  _scene_from_similarity  L=7 N=2 saved=7 sim=1.00
      src/img2nl/features/scene.py:8-14  (_scene_from_similarity)
      src/img2nl/features/scene.py:17-20  (_scene_from_special)

REFACTOR[2] (ranked by priority):
  [1] ○ extract_function   → packages/dsl2img2nl/src/dsl2img2nl/utils/handle_analyze.py
      WHY: 2 occurrences of 15-line block across 1 files — saves 15 lines
      FILES: packages/dsl2img2nl/src/dsl2img2nl/handlers.py
  [2] ○ extract_function   → src/img2nl/features/utils/_scene_from_similarity.py
      WHY: 2 occurrences of 7-line block across 1 files — saves 7 lines
      FILES: src/img2nl/features/scene.py

QUICK_WINS[2] (low risk, high savings — do first):
  [1] extract_function   saved=15L  → packages/dsl2img2nl/src/dsl2img2nl/utils/handle_analyze.py
      FILES: handlers.py
  [2] extract_function   saved=7L  → src/img2nl/features/utils/_scene_from_similarity.py
      FILES: scene.py

EFFORT_ESTIMATE (total ≈ 0.7h):
  medium handle_analyze                      saved=15L  ~30min
  easy   _scene_from_similarity              saved=7L  ~14min

METRICS-TARGET:
  dup_groups:  2 → 0
  saved_lines: 22 lines recoverable
```

### Evolution / Churn (`project/evolution.toon.yaml`)

```toon markpact:analysis path=project/evolution.toon.yaml
# code2llm/evolution | 169 func | 47f | 2026-06-09
# generated in 0.00s

NEXT[3] (ranked by impact):
  [1] !! SPLIT           src/img2nl/i18n/messages.json
      WHY: 1122L, 0 classes, max CC=0
      EFFORT: ~4h  IMPACT: 0

  [2] !! SPLIT           planfile.yaml
      WHY: 1033L, 0 classes, max CC=0
      EFFORT: ~4h  IMPACT: 0

  [3] !! SPLIT           goal.yaml
      WHY: 512L, 0 classes, max CC=0
      EFFORT: ~4h  IMPACT: 0


RISKS[3]:
  ⚠ Splitting src/img2nl/i18n/messages.json may break 0 import paths
  ⚠ Splitting planfile.yaml may break 0 import paths
  ⚠ Splitting goal.yaml may break 0 import paths

METRICS-TARGET:
  CC̄:          3.7 → ≤2.6
  max-CC:      14 → ≤7
  god-modules: 3 → 0
  high-CC(≥15): 0 → ≤0
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
  prev CC̄=3.8 → now CC̄=3.7
```

## Intent

Image → natural language summary with heuristics, thumbnails, and LLM transport hints
