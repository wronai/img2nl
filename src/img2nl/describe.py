"""Generate compact NL text from heuristic features."""

from __future__ import annotations

from typing import Any, Literal

from img2nl.i18n import normalize_locale, t

TranslateMode = Literal["auto", "catalog", "offline"]

_SCENE_KEYS = {
    "empty_dark_screen": "scene_empty_dark",
    "ui_blocks": "scene_ui_blocks",
    "ui_with_text": "scene_ui_text",
    "dense_ui_or_code": "scene_dense_ui",
    "flat_monochrome": "scene_flat_mono",
    "unchanged_screen": "scene_unchanged",
    "barcode_present": "scene_barcode",
}


def _describe_color_parts(colors: dict[str, Any], lang: str) -> list[str]:
    parts: list[str] = []
    if colors.get("is_monochrome"):
        parts.append(t("monochrome", lang))
    else:
        n = colors.get("unique_colors_sampled", 0)
        parts.append(t("colors_count", lang, n=n))
        dom = colors.get("dominant_colors", [])[:3]
        if dom:
            parts.append(t("dominant_colors", lang, colors=", ".join(dom)))
    return parts


def _describe_brightness_dynamics(
    colors: dict[str, Any],
    dynamics: dict[str, Any],
    lang: str,
) -> list[str]:
    parts: list[str] = []
    br = colors.get("brightness_range", [0, 255])
    parts.append(
        t(
            "brightness_range",
            lang,
            b_min=br[0],
            b_max=br[1],
            dynamic=dynamics.get("dynamic_range", 0),
        )
    )
    if dynamics.get("low_contrast"):
        parts.append(t("low_contrast", lang))
    elif dynamics.get("high_contrast"):
        parts.append(t("high_contrast", lang))
    return parts


def _describe_noise_objects_patterns(
    noise: dict[str, Any],
    objects: dict[str, Any],
    patterns: dict[str, Any],
    lang: str,
) -> list[str]:
    parts: list[str] = []
    if noise.get("is_flat"):
        parts.append(t("flat_surface", lang))
    elif noise.get("is_noisy"):
        parts.append(t("noisy", lang))

    if objects.get("has_large_objects"):
        parts.append(t("large_objects", lang, n=objects.get("large_region_count", 0)))
    else:
        parts.append(t("no_large_objects", lang))

    if patterns.get("has_regular_pattern"):
        hints: list[str] = []
        if patterns.get("has_horizontal_bands"):
            hints.append(t("pattern_horizontal", lang))
        if patterns.get("has_vertical_bands"):
            hints.append(t("pattern_vertical", lang))
        parts.append(
            t("regular_patterns", lang, hints=", ".join(hints) or t("pattern_grid", lang))
        )
    return parts


def _describe_targets(features: dict[str, Any], lang: str) -> list[str]:
    report = features.get("target_analysis", {})
    if not report.get("hit_count"):
        return []
    hits = [h for h in report.get("targets", []) if h.get("present")]
    if not hits:
        return []
    names = ", ".join(h["target"] for h in hits[:8])
    if lang == "pl":
        return [f"Wykryte elementy: {names}."]
    return [f"Detected targets: {names}."]


def _describe_scene_special_semantic(
    scene: dict[str, Any],
    special: dict[str, Any],
    semantic: dict[str, Any],
    lang: str,
) -> list[str]:
    parts: list[str] = []
    scene_key = _SCENE_KEYS.get(scene.get("scene_class", ""))
    if scene_key:
        parts.append(t(scene_key, lang))

    barcodes = special.get("barcodes", {})
    if barcodes.get("has_codes"):
        parts.append(t("special_qr_found", lang, n=barcodes.get("count", 0)))

    ocr = special.get("ocr", {})
    if ocr.get("has_text") and ocr.get("text_preview"):
        parts.append(t("special_text_found", lang, preview=ocr["text_preview"]))

    if semantic.get("labels"):
        parts.append(
            t("special_objects_found", lang, labels=", ".join(semantic["labels"][:6]))
        )
    return parts


def _describe_catalog(features: dict[str, Any], lang: str) -> str:
    colors = features.get("colors", {})
    dynamics = features.get("dynamics", {})
    noise = features.get("noise", {})
    objects = features.get("objects", {})
    patterns = features.get("patterns", {})
    scene = features.get("scene", {})
    special = features.get("special_hits", {})
    semantic = features.get("semantic_hits", {})
    w, h = colors.get("size", [0, 0])

    parts: list[str] = [t("image_size", lang, w=w, h=h)]
    parts.extend(_describe_color_parts(colors, lang))
    parts.extend(_describe_brightness_dynamics(colors, dynamics, lang))
    parts.extend(_describe_noise_objects_patterns(noise, objects, patterns, lang))
    parts.extend(_describe_scene_special_semantic(scene, special, semantic, lang))
    parts.extend(_describe_targets(features, lang))
    return " ".join(parts)


def describe_image(
    features: dict[str, Any],
    *,
    locale: str = "pl",
    translate_mode: TranslateMode = "auto",
) -> str:
    """
    Build image summary text.

    *translate_mode*:
    - ``catalog`` — static European message catalog only
    - ``offline`` — English catalog + argostranslate to target
    - ``auto`` — catalog for pl/en; offline en→target when argostranslate installed;
      else catalog fallback
    """
    lang = normalize_locale(locale)

    if translate_mode == "catalog":
        return _describe_catalog(features, lang)

    text_en = _describe_catalog(features, "en")
    if lang == "en":
        return text_en

    if translate_mode in {"auto", "offline"}:
        from img2nl.i18n.offline import translate_summary_offline

        result = translate_summary_offline(text_en, lang, source_lang="en")
        if result.ok and result.text:
            return result.text
        if translate_mode == "offline":
            return result.text or text_en

    return _describe_catalog(features, lang)
