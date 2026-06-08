"""Tests for uri2img2nl."""

from __future__ import annotations

from pathlib import Path

import pytest

pytest.importorskip("PIL")
pytest.importorskip("uri2img2nl")

from img2nl import analyze_image
from uri2img2nl import query_uri, uri_for_analyze


def test_uri_query(tmp_path: Path) -> None:
    from PIL import Image

    p = tmp_path / "x.png"
    Image.new("RGB", (80, 60), (10, 100, 200)).save(p)
    uri = uri_for_analyze(str(p))
    result = query_uri(uri)
    assert result.ok
    assert result.data["width"] == 80


def test_dsl_analyze(tmp_path: Path) -> None:
    from PIL import Image
    from dsl2img2nl import dispatch

    p = tmp_path / "y.png"
    Image.new("RGB", (64, 64), (255, 0, 0)).save(p)
    r = dispatch(f"ANALYZE {p}")
    assert r.ok
    assert r.action == "analyze"
