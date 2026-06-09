"""Conditional OCR via rapidocr-onnxruntime (optional)."""

from __future__ import annotations

from typing import Any


def _should_ocr(features: dict[str, Any]) -> bool:
    scene = features.get("scene", {})
    if scene.get("scene_class") == "empty_dark_screen":
        return False
    edges = features.get("edges", {})
    if edges.get("text_likelihood"):
        return True
    return scene.get("scene_class") in {"ui_with_text", "dense_ui_or_code"}


def _preview(lines: list[str], *, max_lines: int = 5, max_chars: int = 200) -> str:
    joined = " ".join(lines[:max_lines]).strip()
    if len(joined) > max_chars:
        return joined[: max_chars - 3] + "..."
    return joined


def analyze_ocr(
    im,
    *,
    features: dict[str, Any],
    max_lines: int = 5,
    max_chars: int = 200,
) -> dict[str, Any]:
    if not _should_ocr(features):
        return {
            "available": True,
            "skipped": True,
            "reason": "trigger_not_met",
            "lines": [],
            "text_preview": "",
            "line_count": 0,
            "has_text": False,
        }

    try:
        from rapidocr_onnxruntime import RapidOCR
        import numpy as np
    except ImportError:
        return {
            "available": False,
            "reason": "rapidocr-onnxruntime not installed: pip install img2nl[ocr]",
            "lines": [],
            "text_preview": "",
            "line_count": 0,
            "has_text": False,
        }

    rgb = im.convert("RGB")
    engine = RapidOCR()
    result, _elapsed = engine(np.array(rgb))
    lines: list[str] = []
    if result:
        for row in result:
            if len(row) >= 2 and row[1]:
                lines.append(str(row[1]).strip())

    preview = _preview(lines, max_lines=max_lines, max_chars=max_chars)
    return {
        "available": True,
        "skipped": False,
        "lines": lines[:max_lines],
        "text_preview": preview,
        "line_count": len(lines),
        "has_text": bool(lines),
    }
