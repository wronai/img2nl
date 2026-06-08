"""Regular pattern / stripe detection."""

from __future__ import annotations

from typing import Any


def analyze_patterns(im, *, sample: int = 64) -> dict[str, Any]:
    from PIL import Image

    gray = im.convert("L").resize((sample, sample))
    pixels = list(gray.get_flattened_data())
    w = h = sample

    def row_variance(y: int) -> float:
        row = pixels[y * w : (y + 1) * w]
        mean = sum(row) / len(row)
        return sum((v - mean) ** 2 for v in row) / len(row)

    def col_variance(x: int) -> float:
        col = [pixels[y * w + x] for y in range(h)]
        mean = sum(col) / len(col)
        return sum((v - mean) ** 2 for v in col) / len(col)

    row_vars = [row_variance(y) for y in range(h)]
    col_vars = [col_variance(x) for x in range(w)]

    def periodicity(vals: list[float]) -> float:
        if len(vals) < 8:
            return 0.0
        mean = sum(vals) / len(vals)
        if mean < 1.0:
            return 0.0
        # compare alternating segments
        even = vals[::2]
        odd = vals[1::2]
        e_mean = sum(even) / len(even)
        o_mean = sum(odd) / len(odd)
        return abs(e_mean - o_mean) / (mean + 1e-6)

    row_period = periodicity(row_vars)
    col_period = periodicity(col_vars)
    has_horizontal_bands = row_period > 0.35 and max(row_vars) > 200
    has_vertical_bands = col_period > 0.35 and max(col_vars) > 200
    has_regular_pattern = has_horizontal_bands or has_vertical_bands or (row_period > 0.5 or col_period > 0.5)

    return {
        "row_periodicity": round(row_period, 3),
        "col_periodicity": round(col_period, 3),
        "has_horizontal_bands": has_horizontal_bands,
        "has_vertical_bands": has_vertical_bands,
        "has_regular_pattern": has_regular_pattern,
    }
