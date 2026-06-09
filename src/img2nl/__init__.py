"""Image → NL summary with heuristics, thumbnails, and LLM transport hints."""

from img2nl.analyze import analyze_image
from img2nl.describe import describe_image
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
    "analyze_image",
    "describe_image",
    "llm_transport_hint",
    "make_thumbnail",
    "normalize_locale",
    "supported_locales",
    "t",
    "translate_summary_offline",
]
