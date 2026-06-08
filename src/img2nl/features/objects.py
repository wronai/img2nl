"""Large region / blob heuristics."""

from __future__ import annotations

from collections import deque
from typing import Any


def _largest_regions(mask, *, min_area_ratio: float = 0.02) -> list[dict[str, Any]]:
    h = len(mask)
    w = len(mask[0]) if h else 0
    total = w * h
    min_area = max(4, int(total * min_area_ratio))
    seen = [[False] * w for _ in range(h)]
    regions: list[dict[str, Any]] = []

    for y in range(h):
        for x in range(w):
            if seen[y][x] or not mask[y][x]:
                continue
            q: deque[tuple[int, int]] = deque([(x, y)])
            seen[y][x] = True
            min_x = max_x = x
            min_y = max_y = y
            area = 0
            while q:
                cx, cy = q.popleft()
                area += 1
                min_x, max_x = min(min_x, cx), max(max_x, cx)
                min_y, max_y = min(min_y, cy), max(max_y, cy)
                for nx, ny in ((cx + 1, cy), (cx - 1, cy), (cx, cy + 1), (cx, cy - 1)):
                    if 0 <= nx < w and 0 <= ny < h and not seen[ny][nx] and mask[ny][nx]:
                        seen[ny][nx] = True
                        q.append((nx, ny))
            if area >= min_area:
                regions.append(
                    {
                        "area": area,
                        "area_ratio": round(area / total, 4),
                        "bbox": [min_x, min_y, max_x + 1, max_y + 1],
                    }
                )
    regions.sort(key=lambda r: r["area"], reverse=True)
    return regions[:8]


def analyze_objects(im, *, grid: int = 32) -> dict[str, Any]:
    from PIL import Image

    rgb = im.convert("RGB")
    w, h = rgb.size
    small = rgb.resize((grid, grid))
    pixels = list(small.get_flattened_data())

    # Quantize to coarse palette for region grouping
    quant = []
    for r, g, b in pixels:
        quant.append((r // 32, g // 32, b // 32))
    palette = sorted(set(quant))
    color_to_id = {c: i for i, c in enumerate(palette)}

    grid_h = grid
    grid_w = grid
    labels = [[0] * grid_w for _ in range(grid_h)]
    idx = 0
    for gy in range(grid_h):
        for gx in range(grid_w):
            labels[gy][gx] = color_to_id[quant[idx]] + 1
            idx += 1

    large_regions: list[dict[str, Any]] = []
    for label_id in range(1, len(palette) + 1):
        mask = [[labels[gy][gx] == label_id for gx in range(grid_w)] for gy in range(grid_h)]
        large_regions.extend(_largest_regions(mask, min_area_ratio=0.03))

    large_regions.sort(key=lambda r: r["area"], reverse=True)
    large_regions = large_regions[:6]

    has_large_objects = len(large_regions) >= 1 and large_regions[0]["area_ratio"] >= 0.08
    many_objects = len(large_regions) >= 3

    scaled = []
    for reg in large_regions:
        x0, y0, x1, y1 = reg["bbox"]
        scaled.append(
            {
                "area_ratio": reg["area_ratio"],
                "bbox_norm": [
                    round(x0 / grid_w, 3),
                    round(y0 / grid_h, 3),
                    round(x1 / grid_w, 3),
                    round(y1 / grid_h, 3),
                ],
            }
        )

    return {
        "large_regions": scaled,
        "large_region_count": len(scaled),
        "has_large_objects": has_large_objects,
        "many_objects": many_objects,
        "grid": grid,
    }
