"""Tests for screenshot-oriented DSL and URI extensions."""

from __future__ import annotations

from pathlib import Path
from unittest.mock import patch

import pytest

pytest.importorskip("PIL")
pytest.importorskip("dsl2img2nl")
pytest.importorskip("uri2img2nl")

from dsl2img2nl import dispatch
from img2nl import find_click_point, get_profile
from uri2img2nl import query_uri, uri_for_targets


def _desktop(path: Path) -> Path:
    from PIL import Image, ImageDraw

    im = Image.new("RGB", (400, 300), (30, 30, 40))
    draw = ImageDraw.Draw(im)
    draw.rectangle([20, 20, 180, 140], fill=(200, 50, 50))
    draw.rectangle([220, 80, 380, 260], fill=(50, 180, 90))
    im.save(path)
    return path


def test_dsl_analyze_with_profile(tmp_path: Path) -> None:
    p = _desktop(tmp_path / "ui.png")
    r = dispatch(f"ANALYZE {p} PROFILE fast_ui GOAL click")
    assert r.ok
    assert r.data["goal"] == "click"
    assert r.data["source_type"] == "screenshot"


def test_dsl_targets_command(tmp_path: Path) -> None:
    p = _desktop(tmp_path / "ui.png")
    r = dispatch(f"TARGETS {p} PROFILE fast_ui TARGETS button,panel")
    assert r.ok
    assert r.action == "targets"
    assert "presence" in r.data


def test_dsl_capture_analyze_mock(tmp_path: Path) -> None:
    image_path = _desktop(tmp_path / "screen.png")
    out = tmp_path / "out.png"

    with patch("img2nl.capture.capture_screenshot") as mock_capture:
        mock_capture.return_value = {
            "ok": True,
            "path": str(image_path),
            "backend": "vdisplay",
            "meta": {},
        }
        r = dispatch(f"CAPTURE-ANALYZE OUT {out} PROFILE fast_ui GOAL click")

    assert r.ok
    assert r.action == "capture_analyze"
    assert r.data["goal"] == "click"


def test_uri_targets_query(tmp_path: Path) -> None:
    p = _desktop(tmp_path / "shot.png")
    uri = uri_for_targets(str(p), goal="click", targets="button,panel")
    result = query_uri(uri)
    assert result.ok
    assert result.selector == "targets"
    assert "presence" in result.data


def test_find_click_point_from_ui_report() -> None:
    report = {
        "targets": [
            {
                "target": "button",
                "present": True,
                "confidence": 0.8,
                "detections": [
                    {
                        "target": "button",
                        "confidence": 0.9,
                        "bbox": [10, 20, 50, 40],
                        "center": [30, 30],
                    }
                ],
            }
        ]
    }
    point = find_click_point(report, "button")
    assert point == (30.0, 30.0)


def test_fast_ui_profile_defaults() -> None:
    profile = get_profile("fast_ui")
    assert profile["goal"] == "click"
    assert "button" in profile["targets"]
