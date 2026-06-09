"""Tests for lazy feature extraction and click automation."""

from __future__ import annotations

from pathlib import Path
from unittest.mock import patch

import pytest

pytest.importorskip("PIL")

from img2nl.actions import build_click_action, click_target
from img2nl.plan import build_execution_plan, resolve_base_layers, should_run_special_hits


def test_fast_ui_plan_skips_heavy_layers() -> None:
    plan = build_execution_plan(
        explicit_source="screenshot",
        goal="click",
        targets=["button", "input"],
        speed="fast",
        enable_detect=False,
        enable_ui_detect=True,
        width=1920,
        height=1080,
        features={"colors": {"size": [1920, 1080]}},
    )
    assert plan.base_layers == frozenset({"colors", "objects", "patterns"})
    assert plan.run_special_hits is False


def test_document_plan_includes_text_layers() -> None:
    plan = build_execution_plan(
        explicit_source="document",
        goal="index",
        targets=["text"],
        speed="fast",
        enable_detect=False,
        enable_ui_detect=False,
        width=800,
        height=1100,
        features={},
    )
    assert "edges" in plan.base_layers
    assert plan.run_special_hits is True


def test_screenshot_with_text_target_adds_edges() -> None:
    layers = resolve_base_layers(
        source_type="screenshot",
        goal="click",
        speed="fast",
        resolved_targets=["button", "text"],
        run_semantic=False,
    )
    assert "edges" in layers
    assert should_run_special_hits(
        goal="click",
        source_type="screenshot",
        resolved_targets=["button", "text"],
        speed="fast",
    )


def test_fast_ui_skips_analyze_edges(tmp_path: Path) -> None:
    from img2nl import analyze_image

    from PIL import Image, ImageDraw

    p = tmp_path / "ui.png"
    im = Image.new("RGB", (640, 480), (240, 240, 240))
    draw = ImageDraw.Draw(im)
    draw.rectangle([40, 40, 180, 90], fill=(0, 120, 215))
    im.save(p)

    with (
        patch("img2nl.features.extractors.analyze_edges") as mock_edges,
        patch("img2nl.features.extractors.analyze_fingerprint") as mock_fp,
        patch("img2nl.features.extractors.analyze_noise") as mock_noise,
        patch("img2nl.features.extractors.analyze_dynamics") as mock_dyn,
    ):
        result = analyze_image(
            p,
            skip_thumbnail=True,
            source_type="screenshot",
            goal="click",
            targets=["button"],
            enable_ui_detect=False,
        )

    assert result.ok
    mock_edges.assert_not_called()
    mock_fp.assert_not_called()
    mock_noise.assert_not_called()
    mock_dyn.assert_not_called()


def test_click_target_dry_run() -> None:
    report = {
        "targets": [
            {
                "target": "button",
                "present": True,
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
    action = build_click_action(report, "button")
    assert action == {"action": "click", "x": 30, "y": 30, "target": "button", "button": 1}

    with patch("img2nl.actions.execute_click_action") as mock_exec:
        mock_exec.return_value = {"ok": True, "method": "dry-run", "dry_run": True}
        result = click_target(report, "button", dry_run=True)
    assert result["ok"] is True
    mock_exec.assert_called_once()


def test_capture_and_analyze_click_dry_run(tmp_path: Path) -> None:
    from img2nl.capture import capture_and_analyze

    from PIL import Image

    image_path = tmp_path / "screen.png"
    Image.new("RGB", (200, 100), (10, 20, 30)).save(image_path)

    report = {
        "targets": [
            {
                "target": "button",
                "present": True,
                "detections": [{"center": [50, 25], "bbox": [40, 20, 60, 30]}],
            }
        ]
    }

    with (
        patch("img2nl.capture.capture_screenshot") as mock_capture,
        patch("img2nl.analyze.analyze_image") as mock_analyze,
        patch("img2nl.actions.click_from_result") as mock_click,
    ):
        from img2nl.result import Img2NlResult

        mock_capture.return_value = {
            "ok": True,
            "path": str(image_path),
            "backend": "vdisplay",
            "meta": {},
        }
        mock_analyze.return_value = Img2NlResult(
            ok=True,
            path=str(image_path),
            targets=report,
            goal="click",
            source_type="screenshot",
        )
        mock_click.return_value = {"ok": True, "method": "dry-run", "dry_run": True}

        result = capture_and_analyze(
            tmp_path / "out.png",
            click_target="button",
            execute_click=False,
            skip_thumbnail=True,
        )

    assert result.ok
    assert result.click_result["dry_run"] is True
    mock_click.assert_called_once()
