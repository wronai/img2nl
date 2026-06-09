"""Full image analysis pipeline."""

from __future__ import annotations

from pathlib import Path

from img2nl.describe import TranslateMode, describe_image
from img2nl.i18n import normalize_locale
from img2nl.features import (
    analyze_colors,
    analyze_dynamics,
    analyze_edges,
    analyze_fingerprint,
    analyze_noise,
    analyze_objects,
    analyze_patterns,
    analyze_semantic,
    analyze_special_hits,
    classify_scene,
    compare_fingerprints,
)
from img2nl.llm_gate import llm_transport_hint
from img2nl.result import Img2NlResult
from img2nl.thumbnail import make_thumbnail


def analyze_image(
    image_path: str | Path,
    *,
    thumbnail: str | Path | None = None,
    thumbnail_max: int = 256,
    locale: str = "pl",
    translate_mode: TranslateMode = "auto",
    skip_thumbnail: bool = False,
    reference_fingerprint: dict | None = None,
    enable_detect: bool = False,
) -> Img2NlResult:
    try:
        from PIL import Image
    except ImportError as exc:
        return Img2NlResult(
            ok=False,
            path=str(image_path),
            error="pillow required: pip install img2nl[analyze]",
        )

    path = Path(image_path).expanduser()
    if not path.is_file():
        return Img2NlResult(ok=False, path=str(path), error=f"image not found: {path}")

    try:
        im = Image.open(path)
        w, h = im.size
        features = {
            "colors": analyze_colors(im),
            "dynamics": analyze_dynamics(im),
            "noise": analyze_noise(im),
            "objects": analyze_objects(im),
            "patterns": analyze_patterns(im),
            "edges": analyze_edges(im),
            "fingerprint": analyze_fingerprint(im),
        }
        features["scene"] = classify_scene(features)
        features["special_hits"] = analyze_special_hits(im, features)
        if reference_fingerprint:
            features["similarity"] = compare_fingerprints(
                features["fingerprint"],
                reference_fingerprint,
            )
        features["scene"] = classify_scene(features)
        loc = normalize_locale(locale)
        text = describe_image(features, locale=loc, translate_mode=translate_mode)
        llm_hint = llm_transport_hint(features)
        features["semantic_hits"] = analyze_semantic(
            im,
            features=features,
            send_to_llm=enable_detect,
        )
        thumb_path = ""
        if not skip_thumbnail:
            thumb_path = make_thumbnail(path, out=thumbnail, max_size=thumbnail_max)

        return Img2NlResult(
            ok=True,
            path=str(path),
            width=w,
            height=h,
            text=text,
            thumbnail=thumb_path,
            features=features,
            llm_hint=llm_hint,
            locale=loc,
        )
    except Exception as exc:
        return Img2NlResult(ok=False, path=str(path), error=str(exc))
