"""Shared helpers for target matchers."""

from __future__ import annotations

from typing import Any

ANIMAL_LABELS = {"dog", "cat", "horse", "cow", "sheep", "elephant", "bear", "zebra", "giraffe"}
BIRD_LABELS = {"bird"}
SEMANTIC_TARGETS = {"person", "animal", "bird", "house", "car"}

UI_ROLE_ALIASES: dict[str, set[str]] = {
    "button": {"button"},
    "input": {"input", "textbox", "textfield", "field"},
    "checkbox": {"checkbox", "check"},
    "dropdown": {"dropdown", "select", "combobox"},
    "window": {"window"},
    "panel": {"panel"},
    "titlebar": {"titlebar"},
    "icon": {"icon", "toolbar"},
    "text": {"text", "label"},
}


def match_ui_role(target: str, label: str, role: str = "") -> bool:
    key = target.lower()
    hay = f"{label} {role}".lower()
    aliases = UI_ROLE_ALIASES.get(key, {key})
    return any(alias in hay for alias in aliases)


def feature_slice(features: dict[str, Any], key: str) -> dict[str, Any]:
    return features.get(key, {})
