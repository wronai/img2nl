"""Tests for European locale catalog."""

from __future__ import annotations

import pytest

from img2nl.i18n import normalize_locale, supported_locales, t
from img2nl.i18n.catalog import MESSAGES


@pytest.mark.parametrize(
    "raw,expected",
    [
        ("pl", "pl"),
        ("en-GB", "en"),
        ("de-AT", "de"),
        ("nb", "no"),
        ("fr", "fr"),
        ("xx", "en"),
    ],
)
def test_normalize_locale(raw: str, expected: str) -> None:
    assert normalize_locale(raw) == expected


def test_all_european_locales_have_full_catalog() -> None:
    langs = supported_locales()
    for key, bucket in MESSAGES.items():
        for lang in langs:
            assert lang in bucket, f"missing {lang} for {key}"
            assert bucket[lang], f"empty {lang} for {key}"


@pytest.mark.parametrize("lang", ["de", "fr", "cs", "uk", "fi", "el", "ca"])
def test_translate_not_english_copy(lang: str) -> None:
    en = t("monochrome", "en")
    loc = t("monochrome", lang)
    assert loc != en or lang == "en"


def test_describe_german() -> None:
    from img2nl.describe import describe_image

    features = {
        "colors": {
            "size": [100, 80],
            "is_monochrome": False,
            "unique_colors_sampled": 12,
            "dominant_colors": ["#AABBCC"],
            "brightness_range": [10, 200],
        },
        "dynamics": {"dynamic_range": 50, "low_contrast": False, "high_contrast": True},
        "noise": {"is_flat": False, "is_noisy": True},
        "objects": {"has_large_objects": True, "large_region_count": 2},
        "patterns": {"has_regular_pattern": False},
        "scene": {},
    }
    text = describe_image(features, locale="de")
    assert "Bild 100×80" in text
    assert "Kontrast" in text
