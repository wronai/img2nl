"""Backward-compatible adapter exports."""

from __future__ import annotations

from img2nl.features.identify_matchers import identify_from_features
from img2nl.features.presence_matchers import presence_from_features
from img2nl.features.ui_adapter import analyze_ui_targets

__all__ = ["presence_from_features", "identify_from_features", "analyze_ui_targets"]
