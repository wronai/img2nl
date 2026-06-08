"""European locale normalization and registry."""

from __future__ import annotations

# ISO 639-1 codes for European languages (incl. regional/state languages).
EUROPEAN_LOCALES: frozenset[str] = frozenset(
    {
        "pl", "en", "de", "fr", "es", "it", "pt", "nl", "cs", "sk", "uk", "ru", "ro", "hu", "bg",
        "hr", "sr", "sl", "et", "lv", "lt", "fi", "sv", "da", "no", "is", "el", "ga", "mt", "sq",
        "mk", "be", "ca", "eu", "gl", "cy", "lb", "bs",
    }
)

# Norwegian Bokmål/Nynorsk → no
_LOCALE_ALIASES: dict[str, str] = {
    "nb": "no",
    "nn": "no",
    "pt-br": "pt",
    "pt-pt": "pt",
    "en-us": "en",
    "en-gb": "en",
    "de-at": "de",
    "de-ch": "de",
    "fr-fr": "fr",
    "fr-ca": "fr",
    "es-es": "es",
    "es-mx": "es",
    "ca-es": "ca",
    "eu-es": "eu",
    "gl-es": "gl",
    "cy-gb": "cy",
    "ga-ie": "ga",
    "lb-lu": "lb",
}


def normalize_locale(locale: str, *, default: str = "en") -> str:
    """Map locale tag to supported European ISO 639-1 code; fallback to *default*."""
    raw = (locale or default).strip().lower().replace("_", "-")
    if not raw:
        return default if default in EUROPEAN_LOCALES else "en"

    if raw in _LOCALE_ALIASES:
        return _LOCALE_ALIASES[raw]

    base = raw.split("-", 1)[0]
    if base in _LOCALE_ALIASES:
        return _LOCALE_ALIASES[base]
    if base in EUROPEAN_LOCALES:
        return base
    return default if default in EUROPEAN_LOCALES else "en"


def supported_locales() -> list[str]:
    return sorted(EUROPEAN_LOCALES)


def is_european_locale(locale: str) -> bool:
    return normalize_locale(locale, default="en") in EUROPEAN_LOCALES
