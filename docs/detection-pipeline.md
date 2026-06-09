# Detection pipeline — warstwowy plan img2nl

Heurystyczny pipeline **image → natural language** bez vision LLM. Cięższe moduły uruchamiane warunkowo.

## Warstwa 0 — core (Pillow + NumPy)

Już zaimplementowane w `src/img2nl/features/`:

| Moduł | Plik | Czas | Opis |
|-------|------|------|------|
| Kolory | `colors.py` | ~1–5 ms | monochrom, dominujące kolory, jasność |
| Dynamika | `dynamics.py` | ~1 ms | kontrast, stddev luminancji |
| Szum | `noise.py` | ~5–10 ms | płaskość vs tekstura (Gaussian blur residual) |
| Obiekty | `objects.py` | ~5 ms | duże regiony na siatce 32×32 |
| Wzorce | `patterns.py` | ~5 ms | pasy/siatka (periodyczność wariancji) |

Wynik: opis typu „pusty/ciemny ekran”, „UI z blokami”, „płaska powierzchnia”.

## Warstwa 1 — OpenCV (opcjonalna)

Extra: `pip install img2nl[opencv]`

| Algorytm | Moduł | Po co |
|----------|-------|-------|
| Laplacian variance | `edges.py` | ostrość / blur |
| Canny edge density | `edges.py` | tekst/UI vs płaska tapeta |
| Shannon entropy | `edges.py` | złożoność sceny |

Trigger OCR (warstwa 3): `text_likelihood == true`.

## Warstwa 2 — podobieństwo ekranów

Extra: `pip install img2nl[similarity]`

| Algorytm | Moduł | Po co |
|----------|-------|-------|
| pHash / dHash / wHash | `fingerprint.py` | deduplikacja ramek, cache VQL |
| SSIM (opcjonalnie) | `scikit-image` | drugi etap po hash |

Fingerprint trzymaj w `.vql.json` / wyniku `analyze_image()` → query bez ponownej analizy.

## Warstwa 3 — moduły specjalistyczne

Odpalane warunkowo (`features.special_hits`):

| Moduł | Plik | Paczka | Trigger |
|-------|------|--------|---------|
| QR/barcode | `barcodes.py` | `pyzbar` | nie `empty_dark_screen`; wysoki kontrast lub duże regiony |
| OCR | `ocr_text.py` | `rapidocr-onnxruntime` | `text_likelihood` lub scena UI z tekstem |

Extra: `pip install img2nl[scan]` / `[ocr]`.

## Warstwa 4 — semantyka (opcjonalna)

| Moduł | Plik | Paczka | Trigger |
|-------|------|--------|---------|
| YOLO | `semantic.py` | `ultralytics` | tylko `analyze_image(..., enable_detect=True)` |

Extra: `pip install img2nl[detect]`.

## Podobieństwo ekranów (`similarity.py`)

- `fingerprint_hamming(a, b)` — odległość pHash
- `compare_fingerprints(current, reference)` — match gdy distance ≤ 5
- `compare_images_ssim(im_a, im_b)` — drugi etap (scikit-image)
- `analyze_image(..., reference_fingerprint=prev_fp)` → `features.similarity` + scena `unchanged_screen`

## Klasy sceny (`scene.py`)

Reguły bez ML — pole `features.scene.scene_class`:

| Warunek | `scene_class` |
|---------|---------------|
| monochrom + ciemny + płaski | `empty_dark_screen` |
| `text_likelihood` + regular pattern | `ui_with_text` |
| duże obiekty + wysoki kontrast | `ui_blocks` |
| wysoka gęstość krawędzi | `dense_ui_or_code` |
| fingerprint ≈ poprzedni (VQL) | `unchanged_screen` |
| domyślnie | `general` |

## Schema JSON (rozszerzenie `features`)

```json
{
  "colors": {},
  "dynamics": {},
  "noise": {},
  "objects": {},
  "patterns": {},
  "edges": {
    "available": true,
    "blur_score": 412.5,
    "edge_density": 0.031,
    "entropy": 4.2,
    "text_likelihood": false
  },
  "fingerprint": {
    "available": true,
    "phash": "a1b2c3d4e5f6g7h8",
    "dhash": "...",
    "whash": "..."
  },
  "scene": {
    "scene_class": "empty_dark_screen",
    "labels": ["monochrome_or_dark", "flat_blank_like"]
  },
  "special_hits": {
    "barcodes": {"available": true, "has_codes": false, "count": 0},
    "ocr": {"available": true, "skipped": true, "has_text": false},
    "has_qr": false,
    "has_text": false
  },
  "semantic_hits": {
    "available": true,
    "skipped": true,
    "labels": [],
    "object_count": 0
  },
  "similarity": {
    "available": true,
    "match": false,
    "phash_distance": 12
  }
}
```

## Profile instalacji

```bash
pip install -e ".[analyze]"                    # Pillow + NumPy (core)
pip install -e ".[analyze,opencv]"            # + edges
pip install -e ".[analyze,similarity]"        # + fingerprint
pip install -e ".[full]"                      # analyze + opencv + similarity + scan
pip install -e ".[ocr]"                       # + OCR warunkowy
pip install -e ".[detect]"                    # + YOLO (enable_detect=True)
```

## API

```python
from img2nl import analyze_image

prev = analyze_image("screen.png")
cur = analyze_image(
    "screen2.png",
    reference_fingerprint=prev.features["fingerprint"],
    enable_detect=False,  # True → YOLO (ciężkie)
)
```

### VQL cache (img2vql)

Program `.vql.json` przechowuje w `metadata`:
- `fingerprint`, `special_hits`, `scene_class`, `llm_hint`, `img2nl_text`

`analyze_screenshot(..., skip_if_unchanged=True)` — gdy fingerprint match, pomija rebuild siatki i tylko odświeża metadata.

```bash
uri2vql analyze-window --image capture.png --out app.vql.json
uri2vql query "vql://window/compare?file=app.vql.json&image=capture.png"
uri2vql query "vql://window/refresh?file=app.vql.json&image=capture.png"
uri2vql query "vql://window/diagnose?file=app.vql.json&image=capture.png&save=1"
uri2vql query "vql://window/summary?file=app.vql.json"
```

CLI:

```bash
img2vql diagnose capture.png --vql-program app.vql.json --save
uri2vql refresh-window --vql-program app.vql.json --image capture.png
uri2vql compare-window --vql-program app.vql.json --image capture.png
uri2vql diagnose-window --image capture.png --vql-program app.vql.json --save
uri2vql resolve "odśwież metadata vql" --file app.vql.json --image capture.png
```

Demo: `oqlos/vql/examples/img2nl-vql-flow.sh capture.png app.vql.json`

## Powiązane projekty

| Repo | Pakiet | Rola |
|------|--------|------|
| `oqlos/vql` | `img2vql` | diagnose + metadata → `.vql.json` |
| `oqlos/vql` | `uri2vql` | `window/compare`, `window/refresh`, CLI |

## Kolejność implementacji

1. [x] Dokumentacja (`docs/detection-pipeline.md`)
2. [x] `edges.py`, `fingerprint.py`, `scene.py`
3. [x] `analyze_image()` — lazy optional modules
4. [x] `describe.py`, `llm_gate.py` — scene_class
5. [x] `pyzbar` / OCR (warstwa 3)
6. [x] `ultralytics` (warstwa 4, opt-in `enable_detect`)
7. [x] SSIM + `reference_fingerprint` w analyze
8. [x] integracja fingerprint cache w `img2vql`
9. [x] `window/refresh`, diagnose `--save`, NLP2URI, demo script

## Backlog

Zobacz [TODO.md](../TODO.md) — m.in. `rest2vql`, auto-OCR w VQL, testy CI dla YOLO/OCR.

## CLI (core)

```bash
img2nl analyze photo.png --json
# edges + fingerprint gdy zainstalowane extras
```
