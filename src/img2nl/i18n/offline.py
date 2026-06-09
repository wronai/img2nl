"""Offline neural translation via argostranslate (optional extra)."""

from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import Any

from img2nl.i18n.locales import EUROPEAN_LOCALES, normalize_locale

logger = logging.getLogger(__name__)

# Argos model index uses ISO 639-1; same as our European registry for most langs.
_ARGOS_SUPPORTED = EUROPEAN_LOCALES

_installed_pairs: set[tuple[str, str]] = set()
_index_updated = False


@dataclass
class TranslateResult:
    ok: bool
    text: str
    source_lang: str
    target_lang: str
    method: str = "argostranslate"
    error: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "ok": self.ok,
            "text": self.text,
            "source_lang": self.source_lang,
            "target_lang": self.target_lang,
            "method": self.method,
            "error": self.error,
        }


def argostranslate_available() -> bool:
    try:
        import argostranslate.package  # noqa: F401
        import argostranslate.translate  # noqa: F401

        return True
    except ImportError:
        return False


def _require_argos():
    try:
        import argostranslate.package
        import argostranslate.translate

        return argostranslate.package, argostranslate.translate
    except ImportError as exc:
        raise ImportError(
            "Offline translation requires argostranslate. "
            "Install with: pip install img2nl[translate]"
        ) from exc


def _update_index(package_mod) -> None:
    global _index_updated
    if _index_updated:
        return
    package_mod.update_package_index()
    _index_updated = True


def list_installed_pairs() -> list[tuple[str, str]]:
    """Return (from, to) language pairs with downloaded Argos models."""
    if not argostranslate_available():
        return []
    package_mod, _ = _require_argos()
    return sorted((p.from_code, p.to_code) for p in package_mod.get_installed_packages())


def list_available_pairs(*, refresh_index: bool = False) -> list[tuple[str, str]]:
    """Return (from, to) pairs available in the Argos package index."""
    package_mod, _ = _require_argos()
    if refresh_index:
        global _index_updated
        _index_updated = False
    _update_index(package_mod)
    return sorted(
        {
            (p.from_code, p.to_code)
            for p in package_mod.get_available_packages()
            if p.from_code in _ARGOS_SUPPORTED and p.to_code in _ARGOS_SUPPORTED
        }
    )


def ensure_language_pair(
    from_code: str,
    to_code: str,
    *,
    refresh_index: bool = False,
) -> bool:
    """Download and install Argos model for *from_code* → *to_code* if missing."""
    src = normalize_locale(from_code, default="en")
    dst = normalize_locale(to_code, default="en")
    if src == dst:
        return True

    pair = (src, dst)
    if pair in _installed_pairs:
        return True

    package_mod, _ = _require_argos()
    for inst in package_mod.get_installed_packages():
        if inst.from_code == src and inst.to_code == dst:
            _installed_pairs.add(pair)
            return True

    if refresh_index:
        global _index_updated
        _index_updated = False
    _update_index(package_mod)
    available = package_mod.get_available_packages()
    pkg = next((p for p in available if p.from_code == src and p.to_code == dst), None)
    if pkg is None:
        logger.warning("argos package missing for %s -> %s", src, dst)
        return False

    path = pkg.download()
    package_mod.install_from_path(path)
    _installed_pairs.add(pair)
    return True


def translate_summary_offline(
    text: str,
    target_lang: str,
    *,
    source_lang: str = "en",
    auto_install: bool = True,
) -> TranslateResult:
    """
    Translate summary text offline (default path: English → European target).

    Falls back to original *text* when argostranslate or the language pair is unavailable.
    """
    src = normalize_locale(source_lang, default="en")
    dst = normalize_locale(target_lang, default="en")
    if not text.strip() or src == dst:
        return TranslateResult(ok=True, text=text, source_lang=src, target_lang=dst, method="noop")

    if not argostranslate_available():
        return TranslateResult(
            ok=False,
            text=text,
            source_lang=src,
            target_lang=dst,
            method="fallback",
            error="argostranslate not installed (pip install img2nl[translate])",
        )

    package_mod, translate_mod = _require_argos()
    if auto_install and not ensure_language_pair(src, dst):
        return TranslateResult(
            ok=False,
            text=text,
            source_lang=src,
            target_lang=dst,
            method="fallback",
            error=f"no argos model for {src}->{dst}",
        )

    try:
        translated = translate_mod.translate(text, src, dst)
        return TranslateResult(
            ok=True,
            text=translated,
            source_lang=src,
            target_lang=dst,
            method="argostranslate",
        )
    except Exception as exc:
        logger.debug("argos translate failed %s->%s: %s", src, dst, exc)
        return TranslateResult(
            ok=False,
            text=text,
            source_lang=src,
            target_lang=dst,
            method="fallback",
            error=str(exc),
        )
