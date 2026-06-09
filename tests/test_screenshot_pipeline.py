"""Tests for screenshot routing, targets, and capture integration."""

from __future__ import annotations

from pathlib import Path
from unittest.mock import patch

import pytest

pytest.importorskip("PIL")

from img2nl.context import default_targets, infer_source_type
from img2nl.features.presence_matchers import presence_from_features
from img2nl.features.router import analyze_targets, resolve_targets, should_run_ui_detect


def test_infer_source_type_from_ui_scene() -> None:
    features = {"scene": {"scene_class": "ui_with_text"}}
    assert infer_source_type(explicit="auto", width=1920, height=1080, features=features) == "screenshot"


def test_infer_source_type_explicit_photo() -> None:
    assert infer_source_type(explicit="photo", width=1920, height=1080) == "photo"


def test_resolve_targets_for_click_goal() -> None:
    targets = resolve_targets(source_type="screenshot", goal="click", targets=None)
    assert "button" in targets
    assert "input" in targets


def test_should_run_ui_detect_for_screenshot_click() -> None:
    assert should_run_ui_detect(source_type="screenshot", goal="click", explicit=False) is True


def test_presence_from_features_qrcode_and_text() -> None:
    features = {
        "special_hits": {
            "barcodes": {"has_codes": True, "codes": [{"type": "QRCODE", "data": "x", "bbox": [1, 2, 3, 4]}]},
            "ocr": {"has_text": True, "text_preview": "Save"},
        },
        "semantic_hits": {"objects": []},
        "ui_targets": {"ok": False},
    }
    hits = presence_from_features(features, ["qrcode", "text", "button"])
    by_target = {h.target: h for h in hits}
    assert by_target["qrcode"].present is True
    assert by_target["text"].present is True
    assert by_target["button"].present is False


def test_analyze_targets_on_desktop_screenshot(tmp_path: Path) -> None:
    from PIL import Image, ImageDraw

    p = tmp_path / "desktop.png"
    im = Image.new("RGB", (400, 300), (30, 30, 40))
    draw = ImageDraw.Draw(im)
    draw.rectangle([20, 20, 180, 140], fill=(200, 50, 50))
    draw.rectangle([220, 80, 380, 260], fill=(50, 180, 90))
    im.save(p)

    features = {
        "scene": {"scene_class": "ui_blocks"},
        "special_hits": {"barcodes": {"has_codes": False}, "ocr": {"has_text": False}},
        "semantic_hits": {"objects": []},
    }
    report = analyze_targets(
        p,
        features,
        source_type="screenshot",
        goal="click",
        targets=["button", "panel", "window"],
        speed="fast",
        enable_ui_detect=True,
    )
    assert report["source_type"] == "screenshot"
    assert report["goal"] == "click"
    assert "presence" in report
    assert "adapters" in report


def test_analyze_image_screenshot_profile(tmp_path: Path) -> None:
    from img2nl import analyze_image

    from PIL import Image, ImageDraw

    p = tmp_path / "ui.png"
    im = Image.new("RGB", (640, 480), (240, 240, 240))
    draw = ImageDraw.Draw(im)
    draw.rectangle([40, 40, 180, 90], fill=(0, 120, 215))
    im.save(p)

    result = analyze_image(
        p,
        skip_thumbnail=True,
        source_type="screenshot",
        goal="click",
        targets=["button", "text"],
        enable_ui_detect=True,
    )
    assert result.ok
    assert result.source_type == "screenshot"
    assert result.goal == "click"
    assert "target_analysis" in result.features
    assert result.targets["goal"] == "click"


def test_capture_and_analyze_uses_mock_capture(tmp_path: Path) -> None:
    from img2nl.capture import capture_and_analyze

    from PIL import Image

    image_path = tmp_path / "screen.png"
    Image.new("RGB", (200, 100), (10, 20, 30)).save(image_path)

    with patch("img2nl.capture.capture_screenshot") as mock_capture:
        mock_capture.return_value = {
            "ok": True,
            "path": str(image_path),
            "backend": "vdisplay",
            "meta": {},
        }
        result = capture_and_analyze(
            tmp_path / "out.png",
            goal="click",
            skip_thumbnail=True,
        )

    assert result.ok
    assert result.capture["backend"] == "vdisplay"
    assert result.goal == "click"


def test_default_targets_include_ui_and_photo_classes() -> None:
    ui_targets = default_targets("screenshot")
    photo_targets = default_targets("photo")
    assert "button" in ui_targets
    assert "person" in photo_targets
