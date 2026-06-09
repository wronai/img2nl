"""Rule-based scene classification from heuristic features."""

from __future__ import annotations

from typing import Any


def _scene_from_similarity(features: dict[str, Any]) -> dict[str, Any] | None:
    if features.get("similarity", {}).get("match"):
        return {
            "scene_class": "unchanged_screen",
            "labels": ["fingerprint_match"],
        }
    return None


def _scene_from_special(features: dict[str, Any]) -> dict[str, Any] | None:
    if features.get("special_hits", {}).get("has_qr"):
        return {"scene_class": "barcode_present", "labels": ["qr_or_barcode"]}
    return None


def _scene_dense_from_edges(edges: dict[str, Any]) -> dict[str, Any] | None:
    if not (edges.get("available") and edges.get("edge_density", 0.0) > 0.12):
        return None
    labels: list[str] = []
    if edges.get("text_likelihood"):
        labels.append("text_likelihood")
    labels.append("high_edge_density")
    return {"scene_class": "dense_ui_or_code", "labels": labels}


def _scene_general_fallback(
    objects: dict[str, Any],
    patterns: dict[str, Any],
) -> dict[str, Any]:
    labels: list[str] = []
    if patterns.get("has_regular_pattern"):
        labels.append("regular_pattern")
    if objects.get("has_large_objects"):
        labels.append("large_regions")
    return {"scene_class": "general", "labels": labels or ["unclassified"]}


def _scene_from_heuristics(
    colors: dict[str, Any],
    noise: dict[str, Any],
    objects: dict[str, Any],
    patterns: dict[str, Any],
    dynamics: dict[str, Any],
    edges: dict[str, Any],
) -> dict[str, Any]:
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

    if dense := _scene_dense_from_edges(edges):
        return dense

    if objects.get("has_large_objects") and dynamics.get("high_contrast"):
        return {
            "scene_class": "ui_blocks",
            "labels": ["large_regions", "high_contrast"],
        }

    if colors.get("is_monochrome") and noise.get("is_flat"):
        return {"scene_class": "flat_monochrome", "labels": ["monochrome", "flat"]}

    return _scene_general_fallback(objects, patterns)


def classify_scene(features: dict[str, Any]) -> dict[str, Any]:
    if result := _scene_from_similarity(features):
        return result
    if result := _scene_from_special(features):
        return result

    return _scene_from_heuristics(
        features.get("colors", {}),
        features.get("noise", {}),
        features.get("objects", {}),
        features.get("patterns", {}),
        features.get("dynamics", {}),
        features.get("edges", {}),
    )
