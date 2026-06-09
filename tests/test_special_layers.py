"""Tests for layer 3/4 detectors and similarity helpers."""

from __future__ import annotations

from pathlib import Path
from unittest.mock import patch

import pytest

pytest.importorskip("PIL")

from img2nl import analyze_image
from img2nl.features.barcodes import analyze_barcodes
from img2nl.features.scene import classify_scene
from img2nl.features.similarity import compare_fingerprints, fingerprint_hamming
from img2nl.features.special_hits import analyze_special_hits

try:
    import pyzbar  # noqa: F401

    HAS_PYZBAR = True
except ImportError:
    HAS_PYZBAR = False

try:
    import qrcode as _qrcode

    HAS_QRCODE = True
except ImportError:
    HAS_QRCODE = False

try:
    import imagehash as _imagehash

    HAS_IMAGEHASH = True
except ImportError:
    HAS_IMAGEHASH = False


def _solid(path: Path, color: tuple[int, int, int], size: tuple[int, int] = (200, 100)) -> Path:
    from PIL import Image

    im = Image.new("RGB", size, color=color)
    im.save(path)
    return path


def _desktop(path: Path) -> Path:
    from PIL import Image, ImageDraw

    im = Image.new("RGB", (400, 300), (30, 30, 40))
    d = ImageDraw.Draw(im)
    d.rectangle([20, 20, 180, 140], fill=(200, 50, 50))
    d.rectangle([220, 80, 380, 260], fill=(50, 180, 90))
    im.save(path)
    return path


def test_analyze_includes_special_and_semantic(tmp_path: Path) -> None:
    p = _solid(tmp_path / "black.png", (0, 0, 0))
    r = analyze_image(p, skip_thumbnail=True)
    assert r.ok
    assert "special_hits" in r.features
    assert "semantic_hits" in r.features
    assert r.features["semantic_hits"]["skipped"] is True


def test_barcode_skipped_on_dark_screen(tmp_path: Path) -> None:
    from PIL import Image

    p = _solid(tmp_path / "black.png", (0, 0, 0))
    im = Image.open(p)
    features = {
        "scene": {"scene_class": "empty_dark_screen"},
        "dynamics": {},
        "objects": {},
    }
    result = analyze_barcodes(im, features=features)
    assert result["skipped"] is True
    assert result["count"] == 0


def test_scene_unchanged_from_similarity() -> None:
    features = {
        "similarity": {"match": True},
        "special_hits": {},
        "colors": {},
        "noise": {},
        "objects": {},
        "patterns": {},
        "dynamics": {},
        "edges": {},
    }
    scene = classify_scene(features)
    assert scene["scene_class"] == "unchanged_screen"


@pytest.mark.skipif(not HAS_IMAGEHASH, reason="imagehash not installed")
def test_compare_fingerprints_match() -> None:
    fp = {
        "available": True,
        "phash": "0000000000000000",
        "dhash": "1111111111111111",
    }
    result = compare_fingerprints(fp, fp)
    assert result["match"]
    assert result["phash_distance"] == 0


@pytest.mark.skipif(not HAS_IMAGEHASH, reason="imagehash not installed")
def test_fingerprint_hamming_distance() -> None:
    dist = fingerprint_hamming("ffffffff00000000", "ffffffff00000000")
    assert dist == 0


@pytest.mark.skipif(not HAS_PYZBAR or not HAS_QRCODE, reason="pyzbar/qrcode not installed")
def test_qr_detected_on_desktop(tmp_path: Path) -> None:
    qr_path = tmp_path / "qr.png"
    img = _qrcode.make("img2nl-test")
    img.save(qr_path)

    from PIL import Image

    im = Image.open(qr_path)
    features = {
        "scene": {"scene_class": "general"},
        "dynamics": {"high_contrast": True},
        "objects": {"has_large_objects": True},
    }
    hits = analyze_special_hits(im, features)
    assert hits["has_qr"] is True
    assert hits["barcodes"]["count"] >= 1

    r = analyze_image(qr_path, skip_thumbnail=True)
    assert r.features["scene"]["scene_class"] == "barcode_present"


def test_reference_fingerprint_param(tmp_path: Path) -> None:
    p = _solid(tmp_path / "a.png", (10, 20, 30))
    r1 = analyze_image(p, skip_thumbnail=True)
    r2 = analyze_image(p, skip_thumbnail=True, reference_fingerprint=r1.features["fingerprint"])
    if r2.features.get("similarity", {}).get("available"):
        assert r2.features["similarity"]["match"]
        assert r2.features["scene"]["scene_class"] == "unchanged_screen"


def test_semantic_only_when_enabled(tmp_path: Path) -> None:
    p = _desktop(tmp_path / "desktop.png")
    with patch("img2nl.features.extractors.analyze_semantic") as mock_sem:
        mock_sem.return_value = {"available": True, "skipped": False, "labels": ["tv"], "objects": [], "object_count": 0, "model": "yolov8n.pt"}
        analyze_image(p, skip_thumbnail=True, enable_detect=True)
        mock_sem.assert_called_once()
        assert mock_sem.call_args.kwargs["send_to_llm"] is True
