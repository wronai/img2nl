"""Color distribution and monochrome detection."""

from __future__ import annotations

from collections import Counter
from typing import Any


def _hex(rgb: tuple[int, int, int]) -> str:
    return f"#{rgb[0]:02X}{rgb[1]:02X}{rgb[2]:02X}"


def analyze_colors(im, *, sample: int = 64) -> dict[str, Any]:
    from PIL import Image

    rgb = im.convert("RGB")
    w, h = rgb.size
    small = rgb.resize((sample, sample))
    pixels = list(small.get_flattened_data())
    counter = Counter(pixels)
    unique = len(counter)
    dominant = counter.most_common(8)
    top_share = dominant[0][1] / len(pixels) if dominant else 1.0

    r_vals = [p[0] for p in pixels]
    g_vals = [p[1] for p in pixels]
    b_vals = [p[2] for p in pixels]

    brightness = [int(0.299 * r + 0.587 * g + 0.114 * b) for r, g, b in pixels]
    b_min, b_max = min(brightness), max(brightness)

    is_monochrome = unique <= 2 or top_share >= 0.92
    is_mostly_dark = sum(1 for b in brightness if b < 24) / len(brightness) >= 0.9
    is_mostly_bright = sum(1 for b in brightness if b > 230) / len(brightness) >= 0.9

    return {
        "unique_colors_sampled": unique,
        "dominant_colors": [_hex(c) for c, _ in dominant],
        "dominant_shares": [round(count / len(pixels), 4) for _, count in dominant],
        "top_color_share": round(top_share, 4),
        "is_monochrome": is_monochrome,
        "is_mostly_dark": is_mostly_dark,
        "is_mostly_bright": is_mostly_bright,
        "channel_range": {
            "r": [min(r_vals), max(r_vals)],
            "g": [min(g_vals), max(g_vals)],
            "b": [min(b_vals), max(b_vals)],
        },
        "brightness_range": [b_min, b_max],
        "size": [w, h],
    }
