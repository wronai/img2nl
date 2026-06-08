"""Rule-based scene classification from heuristic features."""

from __future__ import annotations

from typing import Any


def classify_scene(features: dict[str, Any]) -> dict[str, Any]:
    colors = features.get("colors", {})
    noise = features.get("noise", {})
    objects = features.get("objects", {})
    patterns = features.get("patterns", {})
    dynamics = features.get("dynamics", {})
    edges = features.get("edges", {})

    labels: list[str] = []

    if (
        colors.get("is_monochrome")
        and colors.get("is_mostly_dark")
        and noise.get("is_flat")
    ):
        return {
            "scene_class": "empty_dark_screen",
            "labels": ["monochrome_or_dark", "flat_blank_like"],
        }

    if edges.get("text_likelihood") and patterns.get("has_regular_pattern"):
        return {
            "scene_class": "ui_with_text",
            "labels": ["text_likelihood", "regular_pattern"],
        }

    if edges.get("available") and edges.get("edge_density", 0.0) > 0.12:
        if edges.get("text_likelihood"):
            labels.append("text_likelihood")
        labels.append("high_edge_density")
        return {"scene_class": "dense_ui_or_code", "labels": labels}

    if objects.get("has_large_objects") and dynamics.get("high_contrast"):
        return {
            "scene_class": "ui_blocks",
            "labels": ["large_regions", "high_contrast"],
        }

    if colors.get("is_monochrome") and noise.get("is_flat"):
        return {"scene_class": "flat_monochrome", "labels": ["monochrome", "flat"]}

    if patterns.get("has_regular_pattern"):
        labels.append("regular_pattern")
    if objects.get("has_large_objects"):
        labels.append("large_regions")

    return {"scene_class": "general", "labels": labels or ["unclassified"]}
