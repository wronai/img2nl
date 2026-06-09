"""Image → NL summary with heuristics, thumbnails, and LLM transport hints."""

from img2nl import api
from img2nl.analyze import analyze_image
from img2nl.capture import capture_and_analyze, capture_screenshot
from img2nl.describe import describe_image
from img2nl.actions import build_click_action, click_from_result, click_target
from img2nl.features.targets import best_detection, find_click_point
from img2nl.profiles import apply_profile, get_profile, list_profiles
from img2nl.i18n import (
    normalize_locale,
    supported_locales,
    t,
    translate_summary_offline,
)
from img2nl.llm_gate import llm_transport_hint
from img2nl.result import Img2NlResult
from img2nl.thumbnail import make_thumbnail

__all__ = [
    "Img2NlResult",
    "api",
    "analyze_image",
    "apply_profile",
    "best_detection",
    "build_click_action",
    "capture_and_analyze",
    "click_from_result",
    "click_target",
    "capture_screenshot",
    "describe_image",
    "find_click_point",
    "get_profile",
    "list_profiles",
    "llm_transport_hint",
    "make_thumbnail",
    "normalize_locale",
    "supported_locales",
    "t",
    "translate_summary_offline",
]
