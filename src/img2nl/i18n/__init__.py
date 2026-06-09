"""European locale catalog for img2nl descriptions."""

from img2nl.i18n.locales import EUROPEAN_LOCALES, is_european_locale, normalize_locale, supported_locales
from img2nl.i18n.offline import (
    TranslateResult,
    argostranslate_available,
    ensure_language_pair,
    list_available_pairs,
    list_installed_pairs,
    translate_summary_offline,
)
from img2nl.i18n.translate import t

__all__ = [
    "EUROPEAN_LOCALES",
    "TranslateResult",
    "argostranslate_available",
    "ensure_language_pair",
    "is_european_locale",
    "list_available_pairs",
    "list_installed_pairs",
    "normalize_locale",
    "supported_locales",
    "t",
    "translate_summary_offline",
]
