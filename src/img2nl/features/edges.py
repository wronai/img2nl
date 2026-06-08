"""Edge density, blur and entropy via OpenCV (optional)."""

from __future__ import annotations

from typing import Any


def _unavailable(reason: str) -> dict[str, Any]:
    return {
        "available": False,
        "reason": reason,
        "blur_score": 0.0,
        "is_blurry": False,
        "edge_density": 0.0,
        "entropy": 0.0,
        "text_likelihood": False,
    }


def analyze_edges(im, *, max_side: int = 512) -> dict[str, Any]:
    try:
        import cv2
        import numpy as np
    except ImportError:
        return _unavailable("opencv-python not installed: pip install img2nl[opencv]")

    gray = np.array(im.convert("L"))
    h, w = gray.shape
    scale = min(1.0, max_side / max(h, w))
    if scale < 1.0:
        gray = cv2.resize(gray, None, fx=scale, fy=scale, interpolation=cv2.INTER_AREA)

    lap_var = float(cv2.Laplacian(gray, cv2.CV_64F).var())
    edges = cv2.Canny(gray, 50, 150)
    edge_density = float(edges.mean()) / 255.0

    hist = cv2.calcHist([gray], [0], None, [256], [0, 256]).flatten()
    total = hist.sum()
    entropy = 0.0
    if total > 0:
        probs = hist[hist > 0] / total
        entropy = float(-(probs * np.log2(probs)).sum())

    is_blurry = lap_var < 80.0
    text_likelihood = edge_density > 0.08 and lap_var > 100.0 and not is_blurry

    return {
        "available": True,
        "blur_score": round(lap_var, 2),
        "is_blurry": is_blurry,
        "edge_density": round(edge_density, 4),
        "entropy": round(entropy, 3),
        "text_likelihood": text_likelihood,
    }
