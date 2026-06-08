"""Generate compact NL text from heuristic features."""

from __future__ import annotations

from typing import Any

from img2nl.i18n import normalize_locale, t


def describe_image(features: dict[str, Any], *, locale: str = "pl") -> str:
    colors = features.get("colors", {})
    dynamics = features.get("dynamics", {})
    noise = features.get("noise", {})
    objects = features.get("objects", {})
    patterns = features.get("patterns", {})
    scene = features.get("scene", {})
    w, h = colors.get("size", [0, 0])
    lang = normalize_locale(locale)

    parts: list[str] = [t("image_size", lang, w=w, h=h)]

    if colors.get("is_monochrome"):
        parts.append(t("monochrome", lang))
    else:
        n = colors.get("unique_colors_sampled", 0)
        parts.append(t("colors_count", lang, n=n))
        dom = colors.get("dominant_colors", [])[:3]
        if dom:
            parts.append(t("dominant_colors", lang, colors=", ".join(dom)))

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

    scene_class = scene.get("scene_class", "")
    scene_key = {
        "empty_dark_screen": "scene_empty_dark",
        "ui_blocks": "scene_ui_blocks",
        "ui_with_text": "scene_ui_text",
        "dense_ui_or_code": "scene_dense_ui",
        "flat_monochrome": "scene_flat_mono",
    }.get(scene_class)
    if scene_key:
        parts.append(t(scene_key, lang))

    return " ".join(parts)
