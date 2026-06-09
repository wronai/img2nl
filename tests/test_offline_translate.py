"""Tests for offline argostranslate integration."""

from __future__ import annotations

from unittest.mock import MagicMock, patch

import pytest

from img2nl.describe import describe_image
from img2nl.i18n.offline import TranslateResult, translate_summary_offline


def test_translate_summary_no_argos_returns_fallback() -> None:
    with patch("img2nl.i18n.offline.argostranslate_available", return_value=False):
        result = translate_summary_offline("Hello world", "de")
    assert result.ok is False
    assert result.text == "Hello world"
    assert "argostranslate" in (result.error or "")


def test_translate_summary_same_lang_noop() -> None:
    result = translate_summary_offline("Hello", "en", source_lang="en")
    assert result.ok is True
    assert result.text == "Hello"
    assert result.method == "noop"


def test_translate_summary_with_mock_argos() -> None:
    fake_pkg = MagicMock()
    fake_pkg.get_installed_packages.return_value = [
        MagicMock(from_code="en", to_code="de"),
    ]
    fake_translate = MagicMock()
    fake_translate.translate.return_value = "Hallo Welt"

    with (
        patch("img2nl.i18n.offline.argostranslate_available", return_value=True),
        patch("img2nl.i18n.offline._require_argos", return_value=(fake_pkg, fake_translate)),
        patch("img2nl.i18n.offline.ensure_language_pair", return_value=True),
    ):
        result = translate_summary_offline("Hello world", "de", auto_install=False)

    assert result.ok is True
    assert result.text == "Hallo Welt"
    fake_translate.translate.assert_called_once_with("Hello world", "en", "de")


def test_describe_offline_mode_uses_translate(monkeypatch: pytest.MonkeyPatch) -> None:
    features = {
        "colors": {"size": [100, 80], "is_monochrome": True, "brightness_range": [0, 10]},
        "dynamics": {"dynamic_range": 10},
        "noise": {"is_flat": True},
        "objects": {},
        "patterns": {},
        "scene": {},
    }

    with patch(
        "img2nl.i18n.offline.translate_summary_offline",
        return_value=TranslateResult(ok=True, text="DE TEXT", source_lang="en", target_lang="de"),
    ):
        text = describe_image(features, locale="de", translate_mode="offline")
    assert text == "DE TEXT"
