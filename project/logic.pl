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

