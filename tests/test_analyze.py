"""Tests for img2nl heuristics."""

from __future__ import annotations

from pathlib import Path

import pytest

pytest.importorskip("PIL")

from img2nl import analyze_image, llm_transport_hint


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


def test_monochrome_detected(tmp_path: Path) -> None:
    p = _solid(tmp_path / "black.png", (0, 0, 0))
    r = analyze_image(p, skip_thumbnail=True)
    assert r.ok
    assert r.features["colors"]["is_monochrome"] is True
    assert r.features["scene"]["scene_class"] == "empty_dark_screen"
    assert r.llm_hint["send_to_llm"] is False


def test_multicolor_desktop(tmp_path: Path) -> None:
    p = _desktop(tmp_path / "desktop.png")
    r = analyze_image(p, skip_thumbnail=True)
    assert r.ok
    assert r.features["colors"]["unique_colors_sampled"] >= 4
    assert r.features["objects"]["has_large_objects"] is True
    assert r.features["scene"]["scene_class"] in {"ui_blocks", "general", "dense_ui_or_code"}
    assert "Dominują" in r.text or "dużych" in r.text


def test_thumbnail_created(tmp_path: Path) -> None:
    p = _desktop(tmp_path / "shot.png")
    thumb = tmp_path / "shot.thumb.jpg"
    r = analyze_image(p, thumbnail=thumb)
    assert r.ok
    assert Path(r.thumbnail).is_file()


def test_llm_hint_rich_image(tmp_path: Path) -> None:
    p = _desktop(tmp_path / "rich.png")
    r = analyze_image(p, skip_thumbnail=True)
    hint = llm_transport_hint(r.features)
    assert hint["send_to_llm"] is True
    assert hint["confidence"] >= 0.45
