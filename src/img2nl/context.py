"""Analysis context: image source type and processing goal."""

from __future__ import annotations

from typing import Any, Literal

SourceType = Literal["auto", "photo", "screenshot", "document", "camera"]
AnalysisGoal = Literal["describe", "find", "click", "index"]
SpeedMode = Literal["fast", "balanced", "full"]

_SCREENSHOT_SCENES = {
    "ui_with_text",
    "dense_ui_or_code",
    "ui_blocks",
    "barcode_present",
    "unchanged_screen",
}

_DEFAULT_TARGETS: dict[str, list[str]] = {
    "screenshot": [
        "button",
        "input",
        "checkbox",
        "dropdown",
        "qrcode",
        "text",
        "window",
        "panel",
        "titlebar",
        "icon",
    ],
    "photo": ["qrcode", "person", "text", "animal", "bird", "house", "car"],
    "document": ["text", "qrcode"],
    "camera": ["person", "animal", "bird", "car", "house"],
}


def default_targets(source_type: str) -> list[str]:
    return list(_DEFAULT_TARGETS.get(source_type, _DEFAULT_TARGETS["photo"]))


def infer_source_type(
    *,
    explicit: SourceType = "auto",
    width: int = 0,
    height: int = 0,
    features: dict[str, Any] | None = None,
) -> str:
    if explicit != "auto":
        return explicit

    if features:
        scene_class = features.get("scene", {}).get("scene_class", "")
        if scene_class in _SCREENSHOT_SCENES:
            return "screenshot"
        edges = features.get("edges", {})
        patterns = features.get("patterns", {})
        if edges.get("text_likelihood") and patterns.get("has_regular_pattern"):
            return "screenshot"
        if edges.get("available") and edges.get("edge_density", 0.0) > 0.12:
            return "screenshot"

    if width >= 800 and height >= 600:
        ratio = width / height
        if 1.2 <= ratio <= 2.5:
            return "screenshot"

    return "photo"
