"""QR and barcode detection via pyzbar (optional)."""

from __future__ import annotations

import contextlib
import os
import sys
from typing import Any


@contextlib.contextmanager
def _suppress_zbar_stderr():
    """Silence benign zbar C-library databar warnings on UI screenshots."""
    stderr_fd = sys.stderr.fileno()
    devnull = os.open(os.devnull, os.O_WRONLY)
    saved = os.dup(stderr_fd)
    try:
        os.dup2(devnull, stderr_fd)
        yield
    finally:
        os.dup2(saved, stderr_fd)
        os.close(saved)
        os.close(devnull)


def _should_scan(features: dict[str, Any]) -> bool:
    scene = features.get("scene", {})
    if scene.get("scene_class") == "empty_dark_screen":
        return False
    dynamics = features.get("dynamics", {})
    objects = features.get("objects", {})
    return bool(dynamics.get("high_contrast") or objects.get("has_large_objects"))


def analyze_barcodes(im, *, features: dict[str, Any] | None = None) -> dict[str, Any]:
    if features is not None and not _should_scan(features):
        return {
            "available": True,
            "skipped": True,
            "reason": "trigger_not_met",
            "codes": [],
            "count": 0,
            "has_codes": False,
        }

    try:
        from pyzbar.pyzbar import decode
        import numpy as np
    except ImportError:
        return {
            "available": False,
            "reason": "pyzbar not installed: pip install img2nl[scan]",
            "codes": [],
            "count": 0,
            "has_codes": False,
        }

    rgb = im.convert("RGB")
    with _suppress_zbar_stderr():
        decoded = decode(np.array(rgb))
    codes: list[dict[str, Any]] = []
    for item in decoded:
        rect = item.rect
        codes.append(
            {
                "type": item.type,
                "data": item.data.decode("utf-8", errors="replace"),
                "rect": [rect.left, rect.top, rect.width, rect.height],
            }
        )

    return {
        "available": True,
        "skipped": False,
        "codes": codes,
        "count": len(codes),
        "has_codes": len(codes) > 0,
    }
