"""Contrast and tonal dynamics."""

from __future__ import annotations

from typing import Any


def analyze_dynamics(im) -> dict[str, Any]:
    from PIL import Image, ImageStat

    gray = im.convert("L")
    stat = ImageStat.Stat(gray)
    mean = stat.mean[0]
    stddev = stat.stddev[0]
    extrema = stat.extrema[0]

    dynamic_range = extrema[1] - extrema[0]
    low_contrast = stddev < 12.0
    high_contrast = stddev > 55.0

    return {
        "luminance_mean": round(mean, 2),
        "luminance_stddev": round(stddev, 2),
        "luminance_extrema": list(extrema),
        "dynamic_range": dynamic_range,
        "low_contrast": low_contrast,
        "high_contrast": high_contrast,
    }
