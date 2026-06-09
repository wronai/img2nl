"""Execution profiles for fast screenshot vs photo analysis."""

from __future__ import annotations

from typing import Any

from img2nl.context import AnalysisGoal, SourceType, SpeedMode

ProfileName = str

_PROFILES: dict[ProfileName, dict[str, Any]] = {
    "fast_ui": {
        "source_type": "screenshot",
        "goal": "click",
        "speed": "fast",
        "enable_ui_detect": True,
        "enable_detect": False,
        "targets": ["button", "input", "checkbox", "dropdown", "text", "window"],
    },
    "fast_photo": {
        "source_type": "photo",
        "goal": "find",
        "speed": "fast",
        "enable_ui_detect": False,
        "enable_detect": False,
        "targets": ["qrcode", "person", "text", "animal", "bird"],
    },
    "fast_document": {
        "source_type": "document",
        "goal": "index",
        "speed": "balanced",
        "enable_ui_detect": False,
        "enable_detect": False,
        "targets": ["text", "qrcode"],
    },
    "full_desktop": {
        "source_type": "screenshot",
        "goal": "click",
        "speed": "full",
        "enable_ui_detect": True,
        "enable_detect": True,
        "targets": None,
    },
}


def list_profiles() -> list[str]:
    return sorted(_PROFILES)


def get_profile(name: ProfileName) -> dict[str, Any]:
    key = name.strip().lower()
    if key not in _PROFILES:
        raise KeyError(f"unknown profile: {name} (available: {', '.join(list_profiles())})")
    return dict(_PROFILES[key])


def apply_profile(
    name: ProfileName,
    *,
    overrides: dict[str, Any] | None = None,
) -> dict[str, Any]:
    params = get_profile(name)
    if overrides:
        for key, value in overrides.items():
            if value is not None and value != "":
                params[key] = value
    return params


def analyze_kwargs_from_cmd(cmd: dict[str, Any]) -> dict[str, Any]:
    """Build analyze_image kwargs from DSL/URI command dict."""
    kw: dict[str, Any] = {}
    if profile := cmd.get("profile"):
        kw.update(get_profile(str(profile)))

    for key in (
        "locale",
        "source_type",
        "goal",
        "speed",
        "enable_ui_detect",
        "enable_detect",
        "skip_thumbnail",
    ):
        if key in cmd and cmd[key] not in (None, ""):
            kw[key] = cmd[key]

    if targets := cmd.get("targets"):
        if isinstance(targets, str):
            kw["targets"] = [t.strip() for t in targets.split(",") if t.strip()]
        else:
            kw["targets"] = list(targets)

    if cmd.get("no_thumbnail"):
        kw["skip_thumbnail"] = True

    return kw
