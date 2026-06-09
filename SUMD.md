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
- **version**: `0.1.5`
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
  version: 0.1.5
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
# img2nl | 66f 4751L | python:62,shell:3,less:1 | 2026-06-09
# stats: 211 func | 7 cls | 66 mod | CC̄=3.7 | critical:11 | cycles:0
# alerts[5]: CC parse_img2nl_uri=14; CC _largest_regions=14; CC analyze_colors=13; CC capture_screenshot=11; CC infer_source_type=11
# hotspots[5]: analyze_edges fan=16; analyze_objects fan=14; analyze_image fan=13; analyze_colors fan=13; analyze_patterns fan=13
# evolution: baseline
# Keys: M=modules, D=details, i=imports, e=exports, c=classes, f=functions, m=methods
M[66]:
  app.doql.less,73
  install-dev.sh,27
  packages/cli2img2nl/src/cli2img2nl/cli.py,33
  packages/dsl2img2nl/src/dsl2img2nl/__init__.py,7
  packages/dsl2img2nl/src/dsl2img2nl/bus.py,30
  packages/dsl2img2nl/src/dsl2img2nl/cli.py,34
  packages/dsl2img2nl/src/dsl2img2nl/grammar.py,119
  packages/dsl2img2nl/src/dsl2img2nl/handlers.py,149
  packages/dsl2img2nl/src/dsl2img2nl/result.py,27
  packages/uri2img2nl/src/uri2img2nl/__init__.py,21
  packages/uri2img2nl/src/uri2img2nl/cli.py,29
  packages/uri2img2nl/src/uri2img2nl/query.py,27
  packages/uri2img2nl/src/uri2img2nl/query_handlers.py,157
  packages/uri2img2nl/src/uri2img2nl/query_result.py,31
  packages/uri2img2nl/src/uri2img2nl/uri.py,149
  project.sh,59
  scripts/build_i18n_catalog.py,63
  src/img2nl/__init__.py,38
  src/img2nl/analyze.py,121
  src/img2nl/api.py,63
  src/img2nl/capture.py,92
  src/img2nl/cli.py,103
  src/img2nl/cli_commands.py,124
  src/img2nl/context.py,69
  src/img2nl/describe.py,180
  src/img2nl/features/__init__.py,32
  src/img2nl/features/adapters.py,10
  src/img2nl/features/barcodes.py,79
  src/img2nl/features/colors.py,52
  src/img2nl/features/dynamics.py,29
  src/img2nl/features/edges.py,55
  src/img2nl/features/extractors.py,58
  src/img2nl/features/fingerprint.py,31
  src/img2nl/features/identify_matchers.py,133
  src/img2nl/features/matchers_common.py,33
  src/img2nl/features/noise.py,30
  src/img2nl/features/objects.py,104
  src/img2nl/features/ocr_text.py,74
  src/img2nl/features/patterns.py,54
  src/img2nl/features/presence_matchers.py,135
  src/img2nl/features/router.py,102
  src/img2nl/features/scene.py,98
  src/img2nl/features/semantic.py,85
  src/img2nl/features/similarity.py,74
  src/img2nl/features/special_hits.py,20
  src/img2nl/features/targets.py,103
  src/img2nl/features/ui_adapter.py,81
  src/img2nl/i18n/__init__.py,27
  src/img2nl/i18n/catalog.py,17
  src/img2nl/i18n/locales.py,60
  src/img2nl/i18n/offline.py,190
  src/img2nl/i18n/translate.py,17
  src/img2nl/llm_gate.py,150
  src/img2nl/plan.py,112
  src/img2nl/profiles.py,99
  src/img2nl/result.py,43
  src/img2nl/thumbnail.py,30
  tests/test_analyze.py,66
  tests/test_detection_layers.py,88
  tests/test_dsl_screenshot.py,99
  tests/test_i18n.py,61
  tests/test_offline_translate.py,64
  tests/test_screenshot_pipeline.py,139
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
    e: split_command,_parse_bool,_normalize_token,_set_pair,_consume_kv,_try_kv_token,_try_bool_flag,_apply_positional,_consume_token,_finalize_cmd,parse_line
    split_command(line)
    _parse_bool(value)
    _normalize_token(token)
    _set_pair(cmd;tokens;index;key)
    _consume_kv(cmd;tokens;index)
    _try_kv_token(cmd;tokens;index)
    _try_bool_flag(cmd;tokens;index)
    _apply_positional(cmd;tokens;index)
    _consume_token(cmd;tokens;index)
    _finalize_cmd(cmd)
    parse_line(line)
  packages/dsl2img2nl/src/dsl2img2nl/handlers.py:
    e: _require_path,handle_analyze,handle_targets,handle_capture,handle_capture_analyze,handle_query,handle_llm_hint,handle_from_tokens
    _require_path(cmd)
    handle_analyze(cmd)
    handle_targets(cmd)
    handle_capture(cmd)
    handle_capture_analyze(cmd)
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
    e: query_uri
    query_uri(uri)
  packages/uri2img2nl/src/uri2img2nl/query_handlers.py:
    e: cmd_from_uri,_missing_path,_analyze_failure,handle_capture_analyze,handle_targets,handle_analyze,handle_llm_hint,handle_text
    cmd_from_uri(parsed)
    _missing_path(uri;parsed)
    _analyze_failure(uri;parsed;error)
    handle_capture_analyze(uri;parsed)
    handle_targets(uri;parsed)
    handle_analyze(uri;parsed)
    handle_llm_hint(uri;parsed)
    handle_text(uri;parsed)
  packages/uri2img2nl/src/uri2img2nl/query_result.py:
    e: QueryResult
    QueryResult: to_dict(0)
  packages/uri2img2nl/src/uri2img2nl/uri.py:
    e: is_img2nl_uri,_encode_params,uri_for_analyze,uri_for_targets,uri_for_capture_analyze,uri_for_llm_hint,_bool_param,parse_img2nl_uri,Img2NlUri
    Img2NlUri: target(0)
    is_img2nl_uri(uri)
    _encode_params(params)
    uri_for_analyze(path)
    uri_for_targets(path)
    uri_for_capture_analyze(out)
    uri_for_llm_hint(path)
    _bool_param(qs;key)
    parse_img2nl_uri(uri)
  scripts/build_i18n_catalog.py:
  src/img2nl/__init__.py:
  src/img2nl/analyze.py:
    e: _require_pillow,_open_image,_assemble_result,analyze_image
    _require_pillow()
    _open_image(path)
    _assemble_result()
    analyze_image(image_path)
  src/img2nl/api.py:
    e: analyze_from_cmd,targets_from_cmd,capture_from_cmd,capture_analyze_from_cmd,llm_hint_from_path,text_from_path
    analyze_from_cmd(cmd)
    targets_from_cmd(cmd)
    capture_from_cmd(cmd)
    capture_analyze_from_cmd(cmd)
    llm_hint_from_path(path)
    text_from_path(path)
  src/img2nl/capture.py:
    e: capture_screenshot,capture_and_analyze
    capture_screenshot(output)
    capture_and_analyze(output)
  src/img2nl/cli.py:
    e: _add_analyze_parser,_add_capture_parser,_add_capture_analyze_parser,_add_translate_install_parser,build_parser,main
    _add_analyze_parser(sub)
    _add_capture_parser(sub)
    _add_capture_analyze_parser(sub)
    _add_translate_install_parser(sub)
    build_parser()
    main(argv)
  src/img2nl/cli_commands.py:
    e: _target_list,_profile_kwargs,cmd_analyze,cmd_capture,cmd_capture_analyze,cmd_translate_install
    _target_list(raw)
    _profile_kwargs(cmd)
    cmd_analyze(args)
    cmd_capture(args)
    cmd_capture_analyze(args)
    cmd_translate_install(args)
  src/img2nl/context.py:
    e: default_targets,infer_source_type
    default_targets(source_type)
    infer_source_type()
  src/img2nl/describe.py:
    e: _describe_color_parts,_describe_brightness_dynamics,_describe_noise_objects_patterns,_describe_targets,_describe_scene_special_semantic,_describe_catalog,describe_image
    _describe_color_parts(colors;lang)
    _describe_brightness_dynamics(colors;dynamics;lang)
    _describe_noise_objects_patterns(noise;objects;patterns;lang)
    _describe_targets(features;lang)
    _describe_scene_special_semantic(scene;special;semantic;lang)
    _describe_catalog(features;lang)
    describe_image(features)
  src/img2nl/features/__init__.py:
  src/img2nl/features/adapters.py:
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
  src/img2nl/features/extractors.py:
    e: extract_base_features,apply_semantic_layer
    extract_base_features(im)
    apply_semantic_layer(im;features)
  src/img2nl/features/fingerprint.py:
    e: _unavailable,analyze_fingerprint
    _unavailable(reason)
    analyze_fingerprint(im)
  src/img2nl/features/identify_matchers.py:
    e: collect_barcodes,collect_ocr,collect_ui,collect_semantic,identify_from_features
    collect_barcodes(features;targets)
    collect_ocr(features;targets)
    collect_ui(features;targets)
    collect_semantic(features;targets)
    identify_from_features(features;targets)
  src/img2nl/features/matchers_common.py:
    e: match_ui_role,feature_slice
    match_ui_role(target;label;role)
    feature_slice(features;key)
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
  src/img2nl/features/presence_matchers.py:
    e: _absent,_best_semantic_object,match_qrcode,match_text,match_semantic,match_ui,presence_from_features
    _absent(target)
    _best_semantic_object(features;target)
    match_qrcode(features;target)
    match_text(features;target)
    match_semantic(features;target)
    match_ui(features;target)
    presence_from_features(features;targets)
  src/img2nl/features/router.py:
    e: execute_target_plan,_active_adapters,analyze_targets,resolve_targets,should_run_ui_detect,should_run_semantic
    execute_target_plan(image_path;features;plan)
    _active_adapters(features)
    analyze_targets(image_path;features)
    resolve_targets()
    should_run_ui_detect()
    should_run_semantic()
  src/img2nl/features/scene.py:
    e: _scene_from_similarity,_scene_from_special,_scene_dense_from_edges,_scene_general_fallback,_scene_from_heuristics,classify_scene
    _scene_from_similarity(features)
    _scene_from_special(features)
    _scene_dense_from_edges(edges)
    _scene_general_fallback(objects;patterns)
    _scene_from_heuristics(colors;noise;objects;patterns;dynamics;edges)
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
  src/img2nl/features/targets.py:
    e: best_detection,find_click_point,_bbox_center,build_target_report,TargetDetection
    TargetDetection: to_dict(0)
    best_detection(target_report;target)
    find_click_point(target_report;target)
    _bbox_center(bbox)
    build_target_report(presence;identifications)
  src/img2nl/features/ui_adapter.py:
    e: _from_imgl_elements,_try_img2vql,_try_imgl_bridge,_try_imgl_local,analyze_ui_targets
    _from_imgl_elements(elements)
    _try_img2vql(path)
    _try_imgl_bridge(path)
    _try_imgl_local(path)
    analyze_ui_targets(image_path)
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
    e: _llm_scene_adjustments,_llm_color_adjustments,_llm_dynamics_noise_adjustments,_llm_structure_adjustments,_llm_special_adjustments,_should_send_to_llm,llm_transport_hint
    _llm_scene_adjustments(scene)
    _llm_color_adjustments(colors)
    _llm_dynamics_noise_adjustments(dynamics;noise;colors)
    _llm_structure_adjustments(objects;patterns;edges)
    _llm_special_adjustments(special;semantic)
    _should_send_to_llm(score;scene;colors;noise)
    llm_transport_hint(features)
  src/img2nl/plan.py:
    e: resolve_targets,should_run_ui_detect,should_run_semantic,should_run_identify,build_execution_plan,ExecutionPlan
    ExecutionPlan:
    resolve_targets()
    should_run_ui_detect()
    should_run_semantic()
    should_run_identify()
    build_execution_plan()
  src/img2nl/profiles.py:
    e: list_profiles,get_profile,apply_profile,analyze_kwargs_from_cmd
    list_profiles()
    get_profile(name)
    apply_profile(name)
    analyze_kwargs_from_cmd(cmd)
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
  tests/test_dsl_screenshot.py:
    e: _desktop,test_dsl_analyze_with_profile,test_dsl_targets_command,test_dsl_capture_analyze_mock,test_uri_targets_query,test_find_click_point_from_ui_report,test_fast_ui_profile_defaults
    _desktop(path)
    test_dsl_analyze_with_profile(tmp_path)
    test_dsl_targets_command(tmp_path)
    test_dsl_capture_analyze_mock(tmp_path)
    test_uri_targets_query(tmp_path)
    test_find_click_point_from_ui_report()
    test_fast_ui_profile_defaults()
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
  tests/test_screenshot_pipeline.py:
    e: test_infer_source_type_from_ui_scene,test_infer_source_type_explicit_photo,test_resolve_targets_for_click_goal,test_should_run_ui_detect_for_screenshot_click,test_presence_from_features_qrcode_and_text,test_analyze_targets_on_desktop_screenshot,test_analyze_image_screenshot_profile,test_capture_and_analyze_uses_mock_capture,test_default_targets_include_ui_and_photo_classes
    test_infer_source_type_from_ui_scene()
    test_infer_source_type_explicit_photo()
    test_resolve_targets_for_click_goal()
    test_should_run_ui_detect_for_screenshot_click()
    test_presence_from_features_qrcode_and_text()
    test_analyze_targets_on_desktop_screenshot(tmp_path)
    test_analyze_image_screenshot_profile(tmp_path)
    test_capture_and_analyze_uses_mock_capture(tmp_path)
    test_default_targets_include_ui_and_photo_classes()
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
project_metadata('img2nl', '0.1.5', 'python').

% ── Project Files ────────────────────────────────────────
project_file('app.doql.less', 73, 'less').
project_file('install-dev.sh', 27, 'shell').
project_file('packages/cli2img2nl/src/cli2img2nl/cli.py', 33, 'python').
project_file('packages/dsl2img2nl/src/dsl2img2nl/__init__.py', 7, 'python').
project_file('packages/dsl2img2nl/src/dsl2img2nl/bus.py', 30, 'python').
project_file('packages/dsl2img2nl/src/dsl2img2nl/cli.py', 34, 'python').
project_file('packages/dsl2img2nl/src/dsl2img2nl/grammar.py', 119, 'python').
project_file('packages/dsl2img2nl/src/dsl2img2nl/handlers.py', 149, 'python').
project_file('packages/dsl2img2nl/src/dsl2img2nl/result.py', 27, 'python').
project_file('packages/uri2img2nl/src/uri2img2nl/__init__.py', 21, 'python').
project_file('packages/uri2img2nl/src/uri2img2nl/cli.py', 29, 'python').
project_file('packages/uri2img2nl/src/uri2img2nl/query.py', 27, 'python').
project_file('packages/uri2img2nl/src/uri2img2nl/query_handlers.py', 157, 'python').
project_file('packages/uri2img2nl/src/uri2img2nl/query_result.py', 31, 'python').
project_file('packages/uri2img2nl/src/uri2img2nl/uri.py', 149, 'python').
project_file('project.sh', 59, 'shell').
project_file('scripts/build_i18n_catalog.py', 63, 'python').
project_file('src/img2nl/__init__.py', 38, 'python').
project_file('src/img2nl/analyze.py', 121, 'python').
project_file('src/img2nl/api.py', 63, 'python').
project_file('src/img2nl/capture.py', 92, 'python').
project_file('src/img2nl/cli.py', 103, 'python').
project_file('src/img2nl/cli_commands.py', 124, 'python').
project_file('src/img2nl/context.py', 69, 'python').
project_file('src/img2nl/describe.py', 180, 'python').
project_file('src/img2nl/features/__init__.py', 32, 'python').
project_file('src/img2nl/features/adapters.py', 10, 'python').
project_file('src/img2nl/features/barcodes.py', 79, 'python').
project_file('src/img2nl/features/colors.py', 52, 'python').
project_file('src/img2nl/features/dynamics.py', 29, 'python').
project_file('src/img2nl/features/edges.py', 55, 'python').
project_file('src/img2nl/features/extractors.py', 58, 'python').
project_file('src/img2nl/features/fingerprint.py', 31, 'python').
project_file('src/img2nl/features/identify_matchers.py', 133, 'python').
project_file('src/img2nl/features/matchers_common.py', 33, 'python').
project_file('src/img2nl/features/noise.py', 30, 'python').
project_file('src/img2nl/features/objects.py', 104, 'python').
project_file('src/img2nl/features/ocr_text.py', 74, 'python').
project_file('src/img2nl/features/patterns.py', 54, 'python').
project_file('src/img2nl/features/presence_matchers.py', 135, 'python').
project_file('src/img2nl/features/router.py', 102, 'python').
project_file('src/img2nl/features/scene.py', 98, 'python').
project_file('src/img2nl/features/semantic.py', 85, 'python').
project_file('src/img2nl/features/similarity.py', 74, 'python').
project_file('src/img2nl/features/special_hits.py', 20, 'python').
project_file('src/img2nl/features/targets.py', 103, 'python').
project_file('src/img2nl/features/ui_adapter.py', 81, 'python').
project_file('src/img2nl/i18n/__init__.py', 27, 'python').
project_file('src/img2nl/i18n/catalog.py', 17, 'python').
project_file('src/img2nl/i18n/locales.py', 60, 'python').
project_file('src/img2nl/i18n/offline.py', 190, 'python').
project_file('src/img2nl/i18n/translate.py', 17, 'python').
project_file('src/img2nl/llm_gate.py', 150, 'python').
project_file('src/img2nl/plan.py', 112, 'python').
project_file('src/img2nl/profiles.py', 99, 'python').
project_file('src/img2nl/result.py', 43, 'python').
project_file('src/img2nl/thumbnail.py', 30, 'python').
project_file('tests/test_analyze.py', 66, 'python').
project_file('tests/test_detection_layers.py', 88, 'python').
project_file('tests/test_dsl_screenshot.py', 99, 'python').
project_file('tests/test_i18n.py', 61, 'python').
project_file('tests/test_offline_translate.py', 64, 'python').
project_file('tests/test_screenshot_pipeline.py', 139, 'python').
project_file('tests/test_special_layers.py', 154, 'python').
project_file('tests/test_uri2img2nl.py', 36, 'python').
project_file('tree.sh', 2, 'shell').

% ── Python Functions ─────────────────────────────────────
python_function('packages/cli2img2nl/src/cli2img2nl/cli.py', 'main', 1, 6, 9).
python_function('packages/dsl2img2nl/src/dsl2img2nl/bus.py', 'dispatch', 1, 8, 9).
python_function('packages/dsl2img2nl/src/dsl2img2nl/bus.py', 'execute_dsl_line', 1, 1, 1).
python_function('packages/dsl2img2nl/src/dsl2img2nl/cli.py', 'main', 1, 8, 10).
python_function('packages/dsl2img2nl/src/dsl2img2nl/grammar.py', 'split_command', 1, 1, 2).
python_function('packages/dsl2img2nl/src/dsl2img2nl/grammar.py', '_parse_bool', 1, 1, 2).
python_function('packages/dsl2img2nl/src/dsl2img2nl/grammar.py', '_normalize_token', 1, 1, 2).
python_function('packages/dsl2img2nl/src/dsl2img2nl/grammar.py', '_set_pair', 4, 1, 0).
python_function('packages/dsl2img2nl/src/dsl2img2nl/grammar.py', '_consume_kv', 3, 2, 1).
python_function('packages/dsl2img2nl/src/dsl2img2nl/grammar.py', '_try_kv_token', 3, 3, 4).
python_function('packages/dsl2img2nl/src/dsl2img2nl/grammar.py', '_try_bool_flag', 3, 4, 4).
python_function('packages/dsl2img2nl/src/dsl2img2nl/grammar.py', '_apply_positional', 3, 4, 1).
python_function('packages/dsl2img2nl/src/dsl2img2nl/grammar.py', '_consume_token', 3, 3, 2).
python_function('packages/dsl2img2nl/src/dsl2img2nl/grammar.py', '_finalize_cmd', 1, 3, 0).
python_function('packages/dsl2img2nl/src/dsl2img2nl/grammar.py', 'parse_line', 1, 3, 5).
python_function('packages/dsl2img2nl/src/dsl2img2nl/handlers.py', '_require_path', 1, 5, 1).
python_function('packages/dsl2img2nl/src/dsl2img2nl/handlers.py', 'handle_analyze', 1, 3, 5).
python_function('packages/dsl2img2nl/src/dsl2img2nl/handlers.py', 'handle_targets', 1, 4, 5).
python_function('packages/dsl2img2nl/src/dsl2img2nl/handlers.py', 'handle_capture', 1, 3, 6).
python_function('packages/dsl2img2nl/src/dsl2img2nl/handlers.py', 'handle_capture_analyze', 1, 3, 5).
python_function('packages/dsl2img2nl/src/dsl2img2nl/handlers.py', 'handle_query', 1, 6, 5).
python_function('packages/dsl2img2nl/src/dsl2img2nl/handlers.py', 'handle_llm_hint', 1, 3, 5).
python_function('packages/dsl2img2nl/src/dsl2img2nl/handlers.py', 'handle_from_tokens', 3, 2, 7).
python_function('packages/uri2img2nl/src/uri2img2nl/cli.py', 'main', 1, 4, 9).
python_function('packages/uri2img2nl/src/uri2img2nl/query.py', 'query_uri', 1, 3, 5).
python_function('packages/uri2img2nl/src/uri2img2nl/query_handlers.py', 'cmd_from_uri', 1, 1, 0).
python_function('packages/uri2img2nl/src/uri2img2nl/query_handlers.py', '_missing_path', 2, 1, 1).
python_function('packages/uri2img2nl/src/uri2img2nl/query_handlers.py', '_analyze_failure', 3, 1, 1).
python_function('packages/uri2img2nl/src/uri2img2nl/query_handlers.py', 'handle_capture_analyze', 2, 3, 7).
python_function('packages/uri2img2nl/src/uri2img2nl/query_handlers.py', 'handle_targets', 2, 4, 7).
python_function('packages/uri2img2nl/src/uri2img2nl/query_handlers.py', 'handle_analyze', 2, 3, 7).
python_function('packages/uri2img2nl/src/uri2img2nl/query_handlers.py', 'handle_llm_hint', 2, 3, 6).
python_function('packages/uri2img2nl/src/uri2img2nl/query_handlers.py', 'handle_text', 2, 3, 5).
python_function('packages/uri2img2nl/src/uri2img2nl/uri.py', 'is_img2nl_uri', 1, 1, 2).
python_function('packages/uri2img2nl/src/uri2img2nl/uri.py', '_encode_params', 1, 5, 4).
python_function('packages/uri2img2nl/src/uri2img2nl/uri.py', 'uri_for_analyze', 1, 4, 1).
python_function('packages/uri2img2nl/src/uri2img2nl/uri.py', 'uri_for_targets', 1, 1, 1).
python_function('packages/uri2img2nl/src/uri2img2nl/uri.py', 'uri_for_capture_analyze', 1, 1, 1).
python_function('packages/uri2img2nl/src/uri2img2nl/uri.py', 'uri_for_llm_hint', 1, 1, 1).
python_function('packages/uri2img2nl/src/uri2img2nl/uri.py', '_bool_param', 2, 2, 3).
python_function('packages/uri2img2nl/src/uri2img2nl/uri.py', 'parse_img2nl_uri', 1, 14, 9).
python_function('src/img2nl/analyze.py', '_require_pillow', 0, 2, 0).
python_function('src/img2nl/analyze.py', '_open_image', 1, 1, 1).
python_function('src/img2nl/analyze.py', '_assemble_result', 0, 2, 6).
python_function('src/img2nl/analyze.py', 'analyze_image', 1, 4, 13).
python_function('src/img2nl/api.py', 'analyze_from_cmd', 1, 1, 2).
python_function('src/img2nl/api.py', 'targets_from_cmd', 1, 3, 4).
python_function('src/img2nl/api.py', 'capture_from_cmd', 1, 3, 4).
python_function('src/img2nl/api.py', 'capture_analyze_from_cmd', 1, 3, 6).
python_function('src/img2nl/api.py', 'llm_hint_from_path', 1, 2, 1).
python_function('src/img2nl/api.py', 'text_from_path', 1, 3, 2).
python_function('src/img2nl/capture.py', 'capture_screenshot', 1, 11, 7).
python_function('src/img2nl/capture.py', 'capture_and_analyze', 1, 2, 5).
python_function('src/img2nl/cli.py', '_add_analyze_parser', 1, 1, 3).
python_function('src/img2nl/cli.py', '_add_capture_parser', 1, 1, 3).
python_function('src/img2nl/cli.py', '_add_capture_analyze_parser', 1, 1, 3).
python_function('src/img2nl/cli.py', '_add_translate_install_parser', 1, 1, 3).
python_function('src/img2nl/cli.py', 'build_parser', 0, 1, 6).
python_function('src/img2nl/cli.py', 'main', 1, 1, 3).
python_function('src/img2nl/cli_commands.py', '_target_list', 1, 4, 2).
python_function('src/img2nl/cli_commands.py', '_profile_kwargs', 1, 1, 1).
python_function('src/img2nl/cli_commands.py', 'cmd_analyze', 1, 7, 8).
python_function('src/img2nl/cli_commands.py', 'cmd_capture', 1, 4, 4).
python_function('src/img2nl/cli_commands.py', 'cmd_capture_analyze', 1, 6, 8).
python_function('src/img2nl/cli_commands.py', 'cmd_translate_install', 1, 8, 5).
python_function('src/img2nl/context.py', 'default_targets', 1, 1, 2).
python_function('src/img2nl/context.py', 'infer_source_type', 0, 11, 1).
python_function('src/img2nl/describe.py', '_describe_color_parts', 2, 3, 4).
python_function('src/img2nl/describe.py', '_describe_brightness_dynamics', 3, 3, 3).
python_function('src/img2nl/describe.py', '_describe_noise_objects_patterns', 4, 8, 4).
python_function('src/img2nl/describe.py', '_describe_targets', 2, 7, 2).
python_function('src/img2nl/describe.py', '_describe_scene_special_semantic', 4, 6, 4).
python_function('src/img2nl/describe.py', '_describe_catalog', 2, 1, 9).
python_function('src/img2nl/describe.py', 'describe_image', 1, 8, 3).
python_function('src/img2nl/features/barcodes.py', '_suppress_zbar_stderr', 0, 1, 5).
python_function('src/img2nl/features/barcodes.py', '_should_scan', 1, 3, 2).
python_function('src/img2nl/features/barcodes.py', 'analyze_barcodes', 1, 5, 7).
python_function('src/img2nl/features/colors.py', '_hex', 1, 1, 0).
python_function('src/img2nl/features/colors.py', 'analyze_colors', 1, 13, 13).
python_function('src/img2nl/features/dynamics.py', 'analyze_dynamics', 1, 1, 4).
python_function('src/img2nl/features/edges.py', '_unavailable', 1, 1, 0).
python_function('src/img2nl/features/edges.py', 'analyze_edges', 1, 6, 16).
python_function('src/img2nl/features/extractors.py', 'extract_base_features', 1, 2, 10).
python_function('src/img2nl/features/extractors.py', 'apply_semantic_layer', 2, 1, 1).
python_function('src/img2nl/features/fingerprint.py', '_unavailable', 1, 1, 0).
python_function('src/img2nl/features/fingerprint.py', 'analyze_fingerprint', 1, 2, 6).
python_function('src/img2nl/features/identify_matchers.py', 'collect_barcodes', 2, 4, 4).
python_function('src/img2nl/features/identify_matchers.py', 'collect_ocr', 2, 3, 2).
python_function('src/img2nl/features/identify_matchers.py', 'collect_ui', 2, 6, 7).
python_function('src/img2nl/features/identify_matchers.py', 'collect_semantic', 2, 10, 8).
python_function('src/img2nl/features/identify_matchers.py', 'identify_from_features', 2, 2, 2).
python_function('src/img2nl/features/matchers_common.py', 'match_ui_role', 3, 2, 3).
python_function('src/img2nl/features/matchers_common.py', 'feature_slice', 2, 1, 1).
python_function('src/img2nl/features/noise.py', 'analyze_noise', 1, 6, 12).
python_function('src/img2nl/features/objects.py', '_largest_regions', 1, 14, 10).
python_function('src/img2nl/features/objects.py', 'analyze_objects', 1, 11, 14).
python_function('src/img2nl/features/ocr_text.py', '_should_ocr', 1, 3, 1).
python_function('src/img2nl/features/ocr_text.py', '_preview', 1, 2, 3).
python_function('src/img2nl/features/ocr_text.py', 'analyze_ocr', 1, 7, 11).
python_function('src/img2nl/features/patterns.py', 'analyze_patterns', 1, 8, 13).
python_function('src/img2nl/features/presence_matchers.py', '_absent', 1, 1, 1).
python_function('src/img2nl/features/presence_matchers.py', '_best_semantic_object', 2, 9, 3).
python_function('src/img2nl/features/presence_matchers.py', 'match_qrcode', 2, 3, 2).
python_function('src/img2nl/features/presence_matchers.py', 'match_text', 2, 3, 2).
python_function('src/img2nl/features/presence_matchers.py', 'match_semantic', 2, 3, 6).
python_function('src/img2nl/features/presence_matchers.py', 'match_ui', 2, 7, 6).
python_function('src/img2nl/features/presence_matchers.py', 'presence_from_features', 2, 5, 3).
python_function('src/img2nl/features/router.py', 'execute_target_plan', 3, 3, 6).
python_function('src/img2nl/features/router.py', '_active_adapters', 1, 3, 2).
python_function('src/img2nl/features/router.py', 'analyze_targets', 2, 3, 4).
python_function('src/img2nl/features/router.py', 'resolve_targets', 0, 1, 1).
python_function('src/img2nl/features/router.py', 'should_run_ui_detect', 0, 1, 1).
python_function('src/img2nl/features/router.py', 'should_run_semantic', 0, 1, 1).
python_function('src/img2nl/features/scene.py', '_scene_from_similarity', 1, 2, 1).
python_function('src/img2nl/features/scene.py', '_scene_from_special', 1, 2, 1).
python_function('src/img2nl/features/scene.py', '_scene_dense_from_edges', 1, 4, 2).
python_function('src/img2nl/features/scene.py', '_scene_general_fallback', 2, 4, 2).
python_function('src/img2nl/features/scene.py', '_scene_from_heuristics', 6, 11, 3).
python_function('src/img2nl/features/scene.py', 'classify_scene', 1, 3, 4).
python_function('src/img2nl/features/semantic.py', '_should_detect', 1, 2, 1).
python_function('src/img2nl/features/semantic.py', '_get_model', 0, 2, 1).
python_function('src/img2nl/features/semantic.py', 'analyze_semantic', 1, 9, 13).
python_function('src/img2nl/features/similarity.py', 'fingerprint_hamming', 2, 5, 1).
python_function('src/img2nl/features/similarity.py', 'compare_fingerprints', 2, 4, 2).
python_function('src/img2nl/features/similarity.py', 'compare_images_ssim', 2, 2, 9).
python_function('src/img2nl/features/special_hits.py', 'analyze_special_hits', 2, 1, 3).
python_function('src/img2nl/features/targets.py', 'best_detection', 2, 8, 3).
python_function('src/img2nl/features/targets.py', 'find_click_point', 2, 5, 6).
python_function('src/img2nl/features/targets.py', '_bbox_center', 1, 2, 1).
python_function('src/img2nl/features/targets.py', 'build_target_report', 2, 8, 11).
python_function('src/img2nl/features/ui_adapter.py', '_from_imgl_elements', 1, 2, 4).
python_function('src/img2nl/features/ui_adapter.py', '_try_img2vql', 1, 3, 2).
python_function('src/img2nl/features/ui_adapter.py', '_try_imgl_bridge', 1, 3, 2).
python_function('src/img2nl/features/ui_adapter.py', '_try_imgl_local', 1, 2, 3).
python_function('src/img2nl/features/ui_adapter.py', 'analyze_ui_targets', 1, 4, 4).
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
python_function('src/img2nl/llm_gate.py', '_llm_scene_adjustments', 1, 3, 2).
python_function('src/img2nl/llm_gate.py', '_llm_color_adjustments', 1, 4, 2).
python_function('src/img2nl/llm_gate.py', '_llm_dynamics_noise_adjustments', 3, 7, 2).
python_function('src/img2nl/llm_gate.py', '_llm_structure_adjustments', 3, 8, 2).
python_function('src/img2nl/llm_gate.py', '_llm_special_adjustments', 2, 4, 2).
python_function('src/img2nl/llm_gate.py', '_should_send_to_llm', 4, 5, 1).
python_function('src/img2nl/llm_gate.py', 'llm_transport_hint', 1, 3, 11).
python_function('src/img2nl/plan.py', 'resolve_targets', 0, 6, 3).
python_function('src/img2nl/plan.py', 'should_run_ui_detect', 0, 3, 0).
python_function('src/img2nl/plan.py', 'should_run_semantic', 0, 5, 0).
python_function('src/img2nl/plan.py', 'should_run_identify', 0, 2, 0).
python_function('src/img2nl/plan.py', 'build_execution_plan', 0, 1, 6).
python_function('src/img2nl/profiles.py', 'list_profiles', 0, 1, 1).
python_function('src/img2nl/profiles.py', 'get_profile', 1, 2, 6).
python_function('src/img2nl/profiles.py', 'apply_profile', 1, 5, 2).
python_function('src/img2nl/profiles.py', 'analyze_kwargs_from_cmd', 1, 10, 8).
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
python_function('tests/test_dsl_screenshot.py', '_desktop', 1, 1, 4).
python_function('tests/test_dsl_screenshot.py', 'test_dsl_analyze_with_profile', 1, 4, 2).
python_function('tests/test_dsl_screenshot.py', 'test_dsl_targets_command', 1, 4, 2).
python_function('tests/test_dsl_screenshot.py', 'test_dsl_capture_analyze_mock', 1, 4, 4).
python_function('tests/test_dsl_screenshot.py', 'test_uri_targets_query', 1, 4, 4).
python_function('tests/test_dsl_screenshot.py', 'test_find_click_point_from_ui_report', 0, 2, 1).
python_function('tests/test_dsl_screenshot.py', 'test_fast_ui_profile_defaults', 0, 3, 1).
python_function('tests/test_i18n.py', 'test_normalize_locale', 2, 2, 2).
python_function('tests/test_i18n.py', 'test_all_european_locales_have_full_catalog', 0, 5, 2).
python_function('tests/test_i18n.py', 'test_translate_not_english_copy', 1, 2, 2).
python_function('tests/test_i18n.py', 'test_describe_german', 0, 3, 1).
python_function('tests/test_offline_translate.py', 'test_translate_summary_no_argos_returns_fallback', 0, 4, 2).
python_function('tests/test_offline_translate.py', 'test_translate_summary_same_lang_noop', 0, 4, 1).
python_function('tests/test_offline_translate.py', 'test_translate_summary_with_mock_argos', 0, 3, 4).
python_function('tests/test_offline_translate.py', 'test_describe_offline_mode_uses_translate', 1, 2, 3).
python_function('tests/test_screenshot_pipeline.py', 'test_infer_source_type_from_ui_scene', 0, 2, 1).
python_function('tests/test_screenshot_pipeline.py', 'test_infer_source_type_explicit_photo', 0, 2, 1).
python_function('tests/test_screenshot_pipeline.py', 'test_resolve_targets_for_click_goal', 0, 3, 1).
python_function('tests/test_screenshot_pipeline.py', 'test_should_run_ui_detect_for_screenshot_click', 0, 2, 1).
python_function('tests/test_screenshot_pipeline.py', 'test_presence_from_features_qrcode_and_text', 0, 5, 1).
python_function('tests/test_screenshot_pipeline.py', 'test_analyze_targets_on_desktop_screenshot', 1, 5, 5).
python_function('tests/test_screenshot_pipeline.py', 'test_analyze_image_screenshot_profile', 1, 6, 5).
python_function('tests/test_screenshot_pipeline.py', 'test_capture_and_analyze_uses_mock_capture', 1, 4, 5).
python_function('tests/test_screenshot_pipeline.py', 'test_default_targets_include_ui_and_photo_classes', 0, 3, 1).
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
python_class('packages/uri2img2nl/src/uri2img2nl/query_result.py', 'QueryResult').
python_method('QueryResult', 'to_dict', 0, 1, 0).
python_class('packages/uri2img2nl/src/uri2img2nl/uri.py', 'Img2NlUri').
python_method('Img2NlUri', 'target', 0, 1, 0).
python_class('src/img2nl/features/targets.py', 'TargetDetection').
python_method('TargetDetection', 'to_dict', 0, 1, 1).
python_class('src/img2nl/i18n/offline.py', 'TranslateResult').
python_method('TranslateResult', 'to_dict', 0, 1, 0).
python_class('src/img2nl/plan.py', 'ExecutionPlan').
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
sumd_declared_file('app.doql.less', 'doql').
sumd_declared_file('testql-scenarios/generated-cli-tests.testql.toon.yaml', 'testql').
sumd_declared_file('project/map.toon.yaml', 'analysis').
sumd_declared_file('project/logic.pl', 'analysis').
sumd_declared_file('project/calls.toon.yaml', 'analysis').
sumd_interface('cli', 'argparse').
sumd_interface('cli', '').
sumd_workflow('venv', 'manual').
sumd_workflow_step('venv', 1, 'test -d .venv || python3 -m venv .venv').
sumd_workflow('install', 'manual').
sumd_workflow_step('install', 1, '$(PIP) install -e ".[analyze]"').
sumd_workflow('install-dev', 'manual').
sumd_workflow_step('install-dev', 1, '$(PIP) install -e ".[dev,analyze]"').
sumd_workflow_step('install-dev', 2, 'for pkg in $(PACKAGES)').
sumd_workflow('test', 'manual').
sumd_workflow_step('test', 1, '$(PYTHON) -m pytest tests/ -q --tb=short').
sumd_workflow('clean', 'manual').
sumd_workflow_step('clean', 1, 'rm -rf .pytest_cache **/__pycache__ dist build *.egg-info').
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

## Intent

Image → natural language summary with heuristics, thumbnails, and LLM transport hints
