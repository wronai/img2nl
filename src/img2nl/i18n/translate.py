"""Lookup translated message templates."""

from __future__ import annotations

from img2nl.i18n.catalog import MESSAGES
from img2nl.i18n.locales import normalize_locale


def t(key: str, locale: str, /, **kwargs: object) -> str:
    lang = normalize_locale(locale)
    bucket = MESSAGES.get(key, {})
    template = bucket.get(lang) or bucket.get("en") or bucket.get("pl") or key
    try:
        return str(template).format(**kwargs)
    except (KeyError, ValueError):
        return str(template)
