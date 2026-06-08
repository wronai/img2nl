"""Perceptual hashes for screen deduplication (optional)."""

from __future__ import annotations

from typing import Any


def _unavailable(reason: str) -> dict[str, Any]:
    return {
        "available": False,
        "reason": reason,
        "phash": "",
        "dhash": "",
        "whash": "",
    }


def analyze_fingerprint(im) -> dict[str, Any]:
    try:
        import imagehash
    except ImportError:
        return _unavailable("imagehash not installed: pip install img2nl[similarity]")

    rgb = im.convert("RGB")
    return {
        "available": True,
        "phash": str(imagehash.phash(rgb)),
        "dhash": str(imagehash.dhash(rgb)),
        "whash": str(imagehash.whash(rgb)),
    }
