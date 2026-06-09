# img2nl — TODO

Śledzenie prac nad warstwowym pipeline detekcji i integracją VQL.

## Zrobione

- [x] Warstwa 0: heurystyki Pillow (`colors`, `dynamics`, `noise`, `objects`, `patterns`)
- [x] Warstwa 1: `edges.py` (OpenCV — blur, edge density, entropy)
- [x] Warstwa 2: `fingerprint.py`, `similarity.py` (pHash, SSIM helper)
- [x] Warstwa 3: `barcodes.py`, `ocr_text.py`, `special_hits.py` (warunkowe)
- [x] Warstwa 4: `semantic.py` (YOLO, opt-in `enable_detect=True`)
- [x] `scene.py` — klasy sceny + `unchanged_screen` / `barcode_present`
- [x] `analyze_image()` — `reference_fingerprint`, lazy extras
- [x] i18n — opisy sceny i special_hits (38 języków w katalogu)
- [x] Testy: `test_analyze`, `test_detection_layers`, `test_special_layers`
- [x] Dokumentacja: `docs/detection-pipeline.md`
- [x] Integracja VQL przez `img2vql` (fingerprint cache, compare/refresh/diagnose)

## Do zrobienia

- [ ] Hook OCR w VQL gdy `metadata.special_hits.has_text` (auto-read text boxes)
- [ ] `rest2vql` — endpointy `window/compare`, `window/refresh`
- [ ] Testy integracyjne z prawdziwym `rapidocr-onnxruntime` (obecnie skip bez paczki)
- [ ] Testy YOLO z mockiem (bez pobierania `yolov8n.pt` w CI)
- [ ] Eksport `features` do protobuf / EventStore (opcjonalnie)
- [ ] CLIP zero-shot tagi (warstwa 4 premium, opcjonalnie)

## Niski priorytet

- [ ] Twarze (`mediapipe` / OpenCV Haar) — trigger warunkowy
- [ ] Cache SSIM w `.vql.json` obok fingerprint (drugi etap compare)
- [ ] `img2nl analyze --enable-detect` w CLI (obecnie tylko Python API)
