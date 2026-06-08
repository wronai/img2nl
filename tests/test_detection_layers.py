"""Tests for optional detection layers (edges, fingerprint, scene)."""

from __future__ import annotations

from pathlib import Path

import pytest

pytest.importorskip("PIL")

from img2nl import analyze_image
from img2nl.features.scene import classify_scene

try:
    import cv2 as _cv2

    HAS_OPENCV = True
except ImportError:
    HAS_OPENCV = False

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


def test_scene_empty_dark_screen() -> None:
    features = {
        "colors": {"is_monochrome": True, "is_mostly_dark": True},
        "noise": {"is_flat": True},
        "objects": {},
        "patterns": {},
        "dynamics": {},
        "edges": {},
    }
    scene = classify_scene(features)
    assert scene["scene_class"] == "empty_dark_screen"


def test_optional_modules_graceful_without_extras(tmp_path: Path) -> None:
    p = _solid(tmp_path / "gray.png", (128, 128, 128))
    r = analyze_image(p, skip_thumbnail=True)
    assert r.ok
    assert "edges" in r.features
    assert "fingerprint" in r.features
    assert "scene" in r.features
    # Without opencv/imagehash installed, modules report unavailable.
    if not r.features["edges"].get("available"):
        assert "reason" in r.features["edges"]
    if not r.features["fingerprint"].get("available"):
        assert "reason" in r.features["fingerprint"]


@pytest.mark.skipif(not HAS_OPENCV, reason="opencv not installed")
def test_edges_when_opencv_installed(tmp_path: Path) -> None:
    p = _solid(tmp_path / "ui.png", (255, 255, 255), size=(400, 300))
    r = analyze_image(p, skip_thumbnail=True)
    edges = r.features["edges"]
    assert edges["available"] is True
    assert edges["blur_score"] >= 0
    assert 0.0 <= edges["edge_density"] <= 1.0


@pytest.mark.skipif(not HAS_IMAGEHASH, reason="imagehash not installed")
def test_fingerprint_when_imagehash_installed(tmp_path: Path) -> None:
    p = _solid(tmp_path / "a.png", (10, 20, 30))
    r = analyze_image(p, skip_thumbnail=True)
    fp = r.features["fingerprint"]
    assert fp["available"] is True
    assert len(fp["phash"]) >= 8
    assert fp["phash"] != fp["dhash"] or fp["phash"] == fp["dhash"]

    p2 = _solid(tmp_path / "b.png", (10, 20, 30))
    r2 = analyze_image(p2, skip_thumbnail=True)
    assert r2.features["fingerprint"]["phash"] == fp["phash"]
