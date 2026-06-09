"""QR and barcode detection via pyzbar (optional)."""

from __future__ import annotations

from typing import Any


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
