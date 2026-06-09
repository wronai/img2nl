"""Heuristic: is this image worth sending to a vision LLM?"""

from __future__ import annotations

from typing import Any


def _llm_scene_adjustments(scene: dict[str, Any]) -> tuple[float, list[str]]:
    score = 0.0
    reasons: list[str] = []
    cls = scene.get("scene_class")
    if cls == "empty_dark_screen":
        score -= 0.4
        reasons.append("empty_dark_screen")
    elif cls == "unchanged_screen":
        score -= 0.25
        reasons.append("unchanged_screen")
    return score, reasons


def _llm_color_adjustments(colors: dict[str, Any]) -> tuple[float, list[str]]:
    score = 0.0
    reasons: list[str] = []
    if colors.get("is_monochrome") or colors.get("is_mostly_dark"):
        score -= 0.35
        reasons.append("monochrome_or_dark")
    if colors.get("unique_colors_sampled", 0) >= 6:
        score += 0.15
        reasons.append("rich_palette")
    return score, reasons


def _llm_dynamics_noise_adjustments(
    dynamics: dict[str, Any],
    noise: dict[str, Any],
    colors: dict[str, Any],
) -> tuple[float, list[str]]:
    score = 0.0
    reasons: list[str] = []
    if dynamics.get("high_contrast"):
        score += 0.1
        reasons.append("high_contrast")
    if dynamics.get("low_contrast") and colors.get("is_monochrome"):
        score -= 0.15
        reasons.append("low_contrast_flat")
    if noise.get("is_flat") and colors.get("is_monochrome"):
        score -= 0.25
        reasons.append("flat_blank_like")
    if noise.get("is_noisy"):
        score += 0.05
        reasons.append("textured_noise")
    return score, reasons


def _llm_structure_adjustments(
    objects: dict[str, Any],
    patterns: dict[str, Any],
    edges: dict[str, Any],
) -> tuple[float, list[str]]:
    score = 0.0
    reasons: list[str] = []
    if objects.get("has_large_objects"):
        score += 0.2
        reasons.append("large_regions")
    if objects.get("many_objects"):
        score += 0.1
        reasons.append("multiple_regions")
    if patterns.get("has_regular_pattern"):
        score += 0.05
        reasons.append("regular_pattern")
    if edges.get("text_likelihood"):
        score += 0.15
        reasons.append("text_likelihood")
    if edges.get("is_blurry"):
        score -= 0.1
        reasons.append("blurry_capture")
    if edges.get("available") and edges.get("entropy", 0) > 5.0:
        score += 0.05
        reasons.append("high_entropy")
    return score, reasons


def _llm_special_adjustments(
    special: dict[str, Any],
    semantic: dict[str, Any],
) -> tuple[float, list[str]]:
    score = 0.0
    reasons: list[str] = []
    if special.get("has_text"):
        score -= 0.1
        reasons.append("ocr_text_available")
    if special.get("has_qr"):
        score -= 0.05
        reasons.append("barcode_decoded")
    if semantic.get("labels"):
        score -= 0.05
        reasons.append("semantic_labels_available")
    return score, reasons


def _should_send_to_llm(
    score: float,
    scene: dict[str, Any],
    colors: dict[str, Any],
    noise: dict[str, Any],
) -> bool:
    if score < 0.45:
        return False
    if scene.get("scene_class") in {"empty_dark_screen", "unchanged_screen"}:
        return False
    return not (
        colors.get("is_monochrome")
        and colors.get("is_mostly_dark")
        and noise.get("is_flat")
    )


def llm_transport_hint(features: dict[str, Any]) -> dict[str, Any]:
    colors = features.get("colors", {})
    dynamics = features.get("dynamics", {})
    noise = features.get("noise", {})
    objects = features.get("objects", {})
    patterns = features.get("patterns", {})
    edges = features.get("edges", {})
    scene = features.get("scene", {})
    special = features.get("special_hits", {})
    semantic = features.get("semantic_hits", {})

    score = 0.5
    reasons: list[str] = []
    for delta, group_reasons in (
        _llm_scene_adjustments(scene),
        _llm_color_adjustments(colors),
        _llm_dynamics_noise_adjustments(dynamics, noise, colors),
        _llm_structure_adjustments(objects, patterns, edges),
        _llm_special_adjustments(special, semantic),
    ):
        score += delta
        reasons.extend(group_reasons)

    score = max(0.0, min(1.0, score))
    send = _should_send_to_llm(score, scene, colors, noise)

    return {
        "send_to_llm": send,
        "confidence": round(score, 3),
        "reasons": reasons,
        "recommendation": "send" if send else "skip_or_use_thumbnail_only",
    }
