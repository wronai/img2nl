"""Noise / grain estimation via high-frequency residual."""

from __future__ import annotations

from typing import Any


def analyze_noise(im, *, sample: int = 128) -> dict[str, Any]:
    from PIL import Image, ImageFilter

    rgb = im.convert("RGB").resize((sample, sample))
    blurred = rgb.filter(ImageFilter.GaussianBlur(radius=1.5))
    orig = list(rgb.get_flattened_data())
    blur = list(blurred.get_flattened_data())
    diffs = [abs(oc - bc) for o, b in zip(orig, blur) for oc, bc in zip(o, b)]
    if not diffs:
        return {"noise_score": 0.0, "is_noisy": False, "is_flat": True}

    avg_diff = sum(diffs) / len(diffs)
    max_diff = max(diffs)
    is_noisy = avg_diff > 18.0 or max_diff > 80
    is_flat = avg_diff < 2.5 and max_diff < 12

    return {
        "noise_score": round(avg_diff, 2),
        "noise_peak": max_diff,
        "is_noisy": is_noisy,
        "is_flat": is_flat,
    }
