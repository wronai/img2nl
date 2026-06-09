"""Fingerprint distance and optional SSIM comparison."""

from __future__ import annotations

from typing import Any


def fingerprint_hamming(a: str, b: str) -> int | None:
    if not a or not b:
        return None
    try:
        import imagehash
    except ImportError:
        return None
    try:
        return imagehash.hex_to_hash(a) - imagehash.hex_to_hash(b)
    except (ValueError, TypeError):
        return None


def compare_fingerprints(
    current: dict[str, Any],
    reference: dict[str, Any],
    *,
    hash_threshold: int = 5,
) -> dict[str, Any]:
    if not current.get("available") or not reference.get("available"):
        return {
            "available": False,
            "reason": "fingerprint_unavailable",
            "match": False,
            "phash_distance": None,
        }

    dist = fingerprint_hamming(current.get("phash", ""), reference.get("phash", ""))
    match = dist is not None and dist <= hash_threshold
    return {
        "available": True,
        "match": match,
        "phash_distance": dist,
        "hash_threshold": hash_threshold,
        "reference_phash": reference.get("phash", ""),
    }


def compare_images_ssim(im_a, im_b, *, max_side: int = 512) -> dict[str, Any]:
    try:
        import cv2
        import numpy as np
        from skimage.metrics import structural_similarity as ssim
    except ImportError:
        return {
            "available": False,
            "reason": "opencv or scikit-image not installed: pip install img2nl[similarity,opencv]",
            "score": None,
        }

    def _gray(im) -> Any:
        gray = np.array(im.convert("L"))
        h, w = gray.shape
        scale = min(1.0, max_side / max(h, w))
        if scale < 1.0:
            gray = cv2.resize(gray, None, fx=scale, fy=scale, interpolation=cv2.INTER_AREA)
        return gray

    a = _gray(im_a)
    b = _gray(im_b)
    h = min(a.shape[0], b.shape[0])
    w = min(a.shape[1], b.shape[1])
    a = a[:h, :w]
    b = b[:h, :w]
    score = float(ssim(a, b))
    return {"available": True, "score": round(score, 4), "match": score >= 0.95}
